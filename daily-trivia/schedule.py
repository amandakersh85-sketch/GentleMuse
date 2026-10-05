#!/usr/bin/env python3
"""Schedule approved trivia into Blotato.

  BLOTATO_API_KEY=... python3 schedule.py [--execute] [--report R.md] PACKAGE.json ...

The GitHub job `Daily trivia, schedule approved` runs this when a daily trivia
pull request is merged. The merge is Amanda's approval, and the package it adds
is what gets scheduled. With no package named, it looks at the packages made in
the last 7 days.

Each of the 4 posts goes into the first daytime slot on its account that is at
least an hour away and 2 hours clear of every other post on that account,
today first. Blotato publishes a post at once if it is sent without a time, so
every post here carries one, and a post without one is never sent.

Idempotent: a post whose video is already queued or was published in the last
14 days on that platform is never created twice. A package goes in whole or
not at all, so the 4 platforms stay together, and it leaves 10 of the 200
queue slots free for the Halloween countdown's next load. Propose-only without
--execute. Rules and their reasons are in README.md next to this file.
"""
import argparse, datetime as dt, glob, json, os, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'filing-system', 'scripts'))
from gm_cadence_check import MIN_GAP_MIN  # noqa: E402  2 hours between posts on 1 account

try:
    from zoneinfo import ZoneInfo
    CENTRAL = ZoneInfo('America/Chicago')
except ImportError:  # Python 3.8. The GitHub runner has 3.12, where this never runs.
    CENTRAL = dt.timezone(dt.timedelta(hours=-5))

API = os.environ.get('BLOTATO_API_BASE', 'https://backend.blotato.com/v2')
CAP = 200
KEEP_FREE = 10        # room for the Halloween loader, which adds at most 4 posts a night
SLOTS = ('09:30', '12:00', '14:30', '16:00')   # Central. Daytime, and 2 hours clear of the 6 PM Halloween posts
LEAD = dt.timedelta(minutes=60)
DAYS_AHEAD = 7
APPROVED = os.path.join(HERE, 'approved')


def api(method, path, key, body=None, query=None):
    url = API + path + ('?' + urllib.parse.urlencode(query) if query else '')
    headers = {'blotato-api-key': key}
    if body is not None:  # Blotato rejects a JSON content type with no body
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, method=method, headers=headers,
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path} {e.code}: {e.read().decode(errors="replace")[:300]}')


def pages(path, key, query):
    items, cursor = [], None
    while True:
        page = api('GET', path, key, query=dict(query, **({'cursor': cursor} if cursor else {})))
        items += page.get('items', [])
        cursor = page.get('cursor')
        if not cursor or not page.get('items'):
            return items


def media_name(url):
    return (url or '').rsplit('/', 1)[-1]


def when(s):
    return dt.datetime.fromisoformat(s.replace('Z', '+00:00'))


def body(p, media, at):
    """The request Blotato takes, the same shape the Halloween loader sends."""
    t = {'targetType': p['platform']}
    for k in ('pageId', 'mediaType', 'shareToFeed', 'title'):
        if k in p:
            t[k] = p[k]
    if p['platform'] == 'tiktok':
        # The video is a HeyGen avatar, so TikTok's AI-generated label applies.
        t.update(privacyLevel='PUBLIC_TO_EVERYONE', disabledComments=False, disabledDuet=False, disabledStitch=False,
                 isBrandedContent=False, isYourBrand=False, isAiGenerated=True)
    if p['platform'] == 'youtube':
        t.update(privacyStatus='public', shouldNotifySubscribers=False)
    return {'post': {'accountId': p['accountId'], 'target': t,
                     'content': {'text': p['text'], 'mediaUrls': [media], 'platform': p['platform']}},
            'scheduledTime': at.astimezone(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}


def slot(taken, now):
    """The first daytime slot at least an hour away and 2 hours clear of every
    time already taken on the account. None if the week is full."""
    start = now.astimezone(CENTRAL).date()
    for d in range(DAYS_AHEAD + 1):
        day = start + dt.timedelta(days=d)
        for hhmm in SLOTS:
            h, m = map(int, hhmm.split(':'))
            local = dt.datetime(day.year, day.month, day.day, h, m, tzinfo=CENTRAL)
            if local < now + LEAD:
                continue
            if all(abs((local - t).total_seconds()) >= MIN_GAP_MIN * 60 for t in taken):
                return local
    return None


def plan(packages, queue, published, now):
    """Pure: no network. Returns (creates, report lines, problems)."""
    count = len(queue)
    taken, have = {}, set()
    for x in queue:
        d = x.get('draft') or {}
        c = d.get('content') or {}
        taken.setdefault(str(d.get('accountId')), []).append(when(x['scheduledAt']))
        for u in c.get('mediaUrls') or []:
            have.add((c.get('platform'), media_name(u)))
    for p in published:
        c = p.get('content') or {}
        for u in c.get('mediaUrls') or p.get('mediaUrls') or []:
            have.add((p.get('platform'), media_name(u)))

    creates, lines, problems = [], [], []
    for pkg in packages:
        fid = pkg.get('factId', '?')
        media = (pkg.get('video') or {}).get('url')
        if not media:
            problems.append(f'{fid}: the package has no video, so nothing from it was scheduled.')
            continue
        todo = [p for p in pkg.get('posts', []) if (p['platform'], media_name(media)) not in have]
        for p in pkg.get('posts', []):
            if p not in todo:
                lines.append(f"- Already queued or published: {fid} {p['platform']}")
        if not todo:
            continue
        if count + len(todo) > CAP - KEEP_FREE:
            problems.append(f'{fid}: the queue holds {count} of {CAP}, and {KEEP_FREE} stay free for the '
                            f'Halloween countdown, so nothing from it was scheduled. It goes in on a later '
                            f'run, once posts publish and room opens.')
            continue
        picked = []
        for p in todo:
            at = slot(taken.get(str(p['accountId']), []), now)
            if at is None:
                break
            picked.append((p, at))
        if len(picked) < len(todo):
            problems.append(f'{fid}: no open daytime slot in the next {DAYS_AHEAD} days on '
                            f"{todo[len(picked)]['platform']}, so nothing from it was scheduled.")
            continue
        for p, at in picked:
            taken.setdefault(str(p['accountId']), []).append(at)
            have.add((p['platform'], media_name(media)))
            count += 1
            creates.append((fid, p, body(p, media, at), at))
    return creates, lines, problems, count


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('packages', nargs='*', help='package files. Default: made in the last 7 days')
    ap.add_argument('--execute', action='store_true')
    ap.add_argument('--report')
    ap.add_argument('--now', help='ISO time, for tests')
    ap.add_argument('--approved', default=APPROVED)
    a = ap.parse_args(argv)

    key = os.environ.get('BLOTATO_API_KEY')
    if not key:
        print('BLOTATO_API_KEY is not set, so nothing was scheduled.')
        return 2
    now = when(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    paths = a.packages or [p for p in sorted(glob.glob(os.path.join(a.approved, '*.json')))
                           if os.path.basename(p)[:10] >= (now - dt.timedelta(days=7)).strftime('%Y-%m-%d')]
    packages = []
    for p in paths:
        if p.endswith('.json'):
            with open(p, encoding='utf-8') as f:
                packages.append(json.load(f))

    queue = pages('/schedules', key, {'limit': 50})
    since = (now - dt.timedelta(days=14)).isoformat()
    published = pages('/posts', key, {'status': 'published', 'since': since, 'until': now.isoformat(), 'limit': 250})
    creates, lines, problems, _ = plan(packages, queue, published, now)

    verb = 'Scheduled' if a.execute else 'Would schedule'
    made = []
    for fid, p, req, at in creates:
        if not req.get('scheduledTime'):
            problems.append(f"{fid} {p['platform']}: no time, and Blotato would publish it at once. Not sent.")
            continue
        if a.execute:
            try:
                api('POST', '/posts', key, body=req)
            except RuntimeError as e:
                problems.append(f"{fid} {p['platform']}: {e}")
                continue
        local = at.astimezone(CENTRAL)
        made.append(f"- {verb} {fid} {p['platform']}: {local:%a %m/%d} "
                    f"{local.strftime('%I:%M %p').lstrip('0')} Central")

    L = [f'# Daily trivia scheduler, {now.astimezone(CENTRAL):%Y-%m-%d}', '',
         f'- Packages: {len(packages)}. Queue before: {len(queue)} of {CAP}, after: '
         f'{len(queue) + len(made) if a.execute else len(queue)}.']
    L += made + lines + [f'- PROBLEM {m}' for m in problems]
    text = '\n'.join(L) + '\n'
    if a.report:
        open(a.report, 'w').write(text)
    print(text)
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
