#!/usr/bin/env python3
"""Load the 33 Nights countdown into Blotato, 7 days ahead at a time.

  BLOTATO_API_KEY=... python3 load.py [--execute] [--days 7] [--report R.md]

Idempotent: a post already in the queue (same platform, same opening text) is
never created twice, so it is safe to run every day. For each night it loads,
the old Halloween repeats queued that same day are removed first; every one of
them is backed up in backup/queue-2026-09-23-full.json. Propose-only without
--execute.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.error, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://backend.blotato.com/v2'
CAP = 200


def api(method, path, key, body=None, query=None):
    url = API + path + ('?' + urllib.parse.urlencode(query) if query else '')
    headers = {'blotato-api-key': key}
    if body is not None:  # Blotato rejects a JSON content type with no body (DELETE)
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path} {e.code}: {e.read().decode(errors="replace")[:300]}')


def norm(t):
    return re.sub(r'\s+', ' ', t or '').strip()[:120].lower()


def queue(key):
    items, cursor = [], None
    while True:
        q = {'limit': 50, **({'cursor': cursor} if cursor else {})}
        page = api('GET', '/schedules', key, query=q)
        items += page.get('items', [])
        cursor = page.get('cursor')
        if not cursor or not page.get('items'):
            return items


def body(p):
    t = {'targetType': p['platform']}
    for k in ('pageId', 'mediaType', 'shareToFeed', 'title'):
        if k in p:
            t[k] = p[k]
    if p['platform'] == 'tiktok':
        t.update(privacyLevel='PUBLIC_TO_EVERYONE', disabledComments=False, disabledDuet=False, disabledStitch=False,
                 isBrandedContent=False, isYourBrand=False, isAiGenerated=True)
    if p['platform'] == 'youtube':
        t.update(privacyStatus='public', shouldNotifySubscribers=False)
    return {'post': {'accountId': p['accountId'], 'target': t,
                     'content': {'text': p['text'], 'mediaUrls': [p['mediaUrl']], 'platform': p['platform']}},
            'scheduledTime': p['scheduledTime']}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true')
    ap.add_argument('--days', type=int, default=7)
    ap.add_argument('--report')
    ap.add_argument('--now', help='ISO time, for tests')
    a = ap.parse_args()
    key = os.environ.get('BLOTATO_API_KEY') or sys.exit('BLOTATO_API_KEY is not set')
    sched = json.load(open(os.path.join(HERE, 'schedule.json')))
    now = dt.datetime.fromisoformat(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
    until = now + dt.timedelta(days=a.days)
    q = queue(key)
    live = {x['id']: x for x in q}
    have = {(x['draft']['content'].get('platform'), norm(x['draft']['content'].get('text'))) for x in q}
    count = len(q)
    L, created, removed, retimed, problems = [], [], [], [], []
    c, r_, t_ = ('Created', 'Removed', 'Retimed') if a.execute else ('Would create', 'Would remove', 'Would retime')

    for p in sched['posts']:
        at = dt.datetime.fromisoformat(p['scheduledTime'].replace('Z', '+00:00'))
        if not (now + dt.timedelta(minutes=30) < at <= until):
            continue
        if (p['platform'], norm(p['text'])) in have:
            continue
        if not p.get('mediaUrl'):
            problems.append(f"{p['key']}: no video yet, not loaded")
            continue
        for old in p.get('replaces', []):
            if old in live:
                if a.execute:
                    try:
                        api('DELETE', f'/schedules/{old}', key)
                    except RuntimeError as e:
                        problems.append(f"remove {old}: {e}")
                        continue
                live.pop(old)
                count -= 1
                removed.append(old)
        if count >= CAP:
            problems.append(f"{p['key']}: queue is full at {CAP}, not loaded. It will go in when room opens.")
            continue
        if a.execute:
            try:
                api('POST', '/posts', key, body=body(p))
            except RuntimeError as e:
                problems.append(f"{p['key']}: {e}")
                continue
        count += 1
        have.add((p['platform'], norm(p['text'])))
        created.append(p['key'])

    for r in sched.get('retimes', []):
        x = live.get(r['id'])
        if x and x['scheduledAt'][:16] != r['scheduledTime'][:16]:
            if a.execute:
                try:
                    api('PATCH', f"/schedules/{r['id']}", key, body={'patch': {'scheduledTime': r['scheduledTime']}})
                except RuntimeError as e:
                    problems.append(f"{r['key']}: {e}")
                    continue
            retimed.append(r['key'])

    L.append(f"# Halloween 33 Nights loader, {now:%Y-%m-%d}")
    L.append('')
    L.append(f"- Window: through {until:%b %-d} UTC. Queue before: {len(q)} of {CAP}, after: {count}.")
    L.append(f"- {c} {len(created)}: {', '.join(created) or 'none'}")
    L.append(f"- {r_} {len(removed)} old Halloween repeats: {', '.join(removed) or 'none'}")
    L.append(f"- {t_}: {', '.join(retimed) or 'none'}")
    for m in problems:
        L.append(f"- PROBLEM {m}")
    text = '\n'.join(L) + '\n'
    if a.report:
        open(a.report, 'w').write(text)
    print(text)
    if problems and any('queue is full' not in m for m in problems):
        sys.exit(1)


if __name__ == '__main__':
    main()
