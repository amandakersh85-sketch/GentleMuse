#!/usr/bin/env python3
"""Blotato queue refill for The Gentle Muse.

Does the daily top-up with rules instead of judgment: reads the wave libraries,
the load logs and the live queue, decides what goes where, and loads it.
Propose-only unless --execute is passed.

  python3 refill.py plan  --lib DIR [--queue-file F] [--out plan.json] [--report R.md]
  python3 refill.py apply --lib DIR [--execute] [--report R.md]      (REST, needs BLOTATO_API_KEY)
  python3 refill.py log   --lib DIR --plan plan.json --ids GW0001,GW0002   (after MCP loads)

DIR is a checkout of branch claude/club-target-game-plan-9xs2du (it holds
content/wave1-staging-library.txt and friends). The queue file is a JSON list
of compact rows: {id, accountId, platform, scheduledAt, text, media}.
Rules and their reasons live in README.md next to this file.
"""
import argparse, datetime as dt, json, os, re, subprocess, sys, urllib.error, urllib.parse, urllib.request
from collections import Counter

API = 'https://backend.blotato.com/v2'
MEDIA_BASE = 'https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/'
QUEUE_CAP = 200
MIN_FREE = 10
DST_END = dt.date(2026, 11, 1)
ACCOUNTS = {'facebook': '30840', 'instagram': '45886', 'youtube': '36129',
            'tiktok': '41488', 'twitter': '21430', 'linkedin': '20723'}
FB_PAGE = '1086399221215093'
SLOTS = {  # UTC, chosen to hold Central time constant across the 1 Nov change
    'before': {'instagram': ['15:00', '23:00'], 'tiktok': ['15:00'], 'facebook': ['17:10', '22:00'],
               'youtube': ['17:20'], 'twitter': ['13:30'], 'linkedin': ['13:30']},
    'after':  {'instagram': ['16:00', '23:00'], 'tiktok': ['16:00'], 'facebook': ['18:10', '23:00'],
               'youtube': ['18:20'], 'twitter': ['14:30'], 'linkedin': ['14:30']},
}
# The Halloween evening series runs on top of the business caps, not inside them.
# Its posts still occupy their timestamp, so nothing else can land on it.
EVENING = {'start': dt.date(2026, 9, 28), 'end': dt.date(2026, 10, 31),
           'times': {'instagram': '23:00', 'tiktok': '23:00', 'facebook': '23:30', 'youtube': '23:30'}}
# Slots held back for the Halloween series until it is fully scheduled.
DEFAULT_RESERVE = {'until': dt.date(2026, 10, 31), 'slots': 40}
X_LIMIT = 280


def slots(plat, day):
    return SLOTS['before' if day < DST_END else 'after'][plat]


def cap(plat, day):
    if plat == 'instagram':
        return 1 if day.weekday() >= 5 else 2
    return 2 if plat == 'facebook' else 1


def row_text(t):
    """A standalone forward slash in library text means a line break. URLs keep theirs."""
    return re.sub(r' ?(?<!\S)/(?!\S) ?', '\n', t).strip()


def norm(t):
    return re.sub(r'\s+', ' ', t or '').strip()[:120].lower()


def media_name(url):
    return (url or '').rsplit('/', 1)[-1]


def exempt(post):
    """True for a Halloween evening post on a main account: it does not count toward caps."""
    ts = post['ts']
    return (EVENING['start'] <= ts.date() <= EVENING['end']
            and EVENING['times'].get(post['platform']) == ts.strftime('%H:%M')
            and post['accountId'] == ACCOUNTS.get(post['platform']))


# ---------- inputs ----------

def read_library(lib, wave):
    path = os.path.join(lib, 'content', f'{wave}-staging-library.txt')
    with open(path, encoding='utf-8') as f:
        body = f.read().split('=== ROWS ===', 1)[-1]
    rows = []
    for line in body.split('\n'):
        if line.strip() and line.count('|') == 5:
            rid, ts, plat, media, yt, text = line.split('|')
            rows.append(dict(id=rid.strip(), ts=dt.datetime.fromisoformat(ts.strip()), platform=plat.strip(),
                             media=media.strip(), title=yt.strip(), text=row_text(text), wave=wave))
    return rows


def read_logs(lib):
    done = set()
    for wave in ('wave1', 'wave2'):
        p = os.path.join(lib, 'content', f'{wave}-loaded.log')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                done |= {l.split()[0] for l in f if l.strip() and not l.startswith('#')}
    return done


def validate(lib):
    out = []
    for wave in ('wave1', 'wave2'):
        r = subprocess.run([sys.executable, os.path.join(lib, 'scripts', 'validate-wave.py'),
                            os.path.join(lib, 'content', f'{wave}-staging-library.txt')],
                           capture_output=True, text=True)
        if r.returncode != 0:
            out.append(f'{wave}: ' + '; '.join(l.strip() for l in r.stdout.splitlines() if 'FAIL' in l))
    return out


def api(method, path, key, body=None, query=None):
    url = API + path + ('?' + urllib.parse.urlencode(query, doseq=True) if query else '')
    req = urllib.request.Request(url, method=method, headers={'blotato-api-key': key, 'Content-Type': 'application/json'},
                                 data=json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'{method} {path} {e.code}: {e.read().decode(errors="replace")[:300]}')


def fetch_queue(key):
    items, cursor = [], None
    while True:
        q = {'limit': 50}
        if cursor:
            q['cursor'] = cursor
        page = api('GET', '/schedules', key, query=q)
        for s in page.get('items', []):
            d = s.get('draft') or {}
            c = d.get('content') or {}
            items.append(dict(id=s['id'], accountId=str(d.get('accountId') or (s.get('account') or {}).get('id')),
                              platform=c.get('platform') or (d.get('target') or {}).get('targetType'),
                              scheduledAt=s['scheduledAt'], text=c.get('text', ''),
                              media=media_name((c.get('mediaUrls') or [''])[0])))
        cursor = page.get('cursor')
        if not cursor or not page.get('items'):
            return items


def fetch_recent(key, status, days_back):
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days_back)).isoformat()
    until = dt.datetime.now(dt.timezone.utc).isoformat()
    out, cursor = [], None
    while True:
        q = {'status': status, 'since': since, 'until': until, 'limit': 250}
        if cursor:
            q['cursor'] = cursor
        page = api('GET', '/posts', key, query=q)
        out += page.get('items', [])
        cursor = page.get('cursor')
        if not cursor or not page.get('items'):
            return out


# ---------- the plan ----------

def plan(lib, queue, now, published=(), reserve=None):
    """Return (loads, report dict). Pure: no network, no writes."""
    rep = dict(now=now.isoformat(), queued=len(queue), moved=[], dupes=[], skipped=[], hold_soon=[], stop=None)
    bad = validate(lib)
    if bad:
        rep['stop'] = 'Library check failed, loaded nothing: ' + ' | '.join(bad)
        return [], rep
    if reserve is None:
        reserve = DEFAULT_RESERVE['slots'] if now.date() <= DEFAULT_RESERVE['until'] else 0
    rep['reserve'] = reserve
    room = QUEUE_CAP - len(queue) - reserve
    rep['free'] = QUEUE_CAP - len(queue)
    if room < MIN_FREE:
        rep['stop'] = f'Only {max(room, 0)} slots free after holding {reserve} for Halloween, so nothing loaded.'
        return [], rep

    posts = []
    for q in queue:
        ts = dt.datetime.fromisoformat(q['scheduledAt'].replace('Z', '+00:00')).replace(tzinfo=None)
        posts.append(dict(q, ts=ts))
    taken = {(p['platform'], p['accountId'], p['ts']) for p in posts}
    per_day = Counter((p['platform'], p['accountId'], p['ts'].date()) for p in posts if not exempt(p))
    seen = set()
    for p in list(posts) + [dict(x) for x in published]:
        if p.get('media'):
            seen.add((p['platform'], 'm', p['media']))
        if p.get('text'):
            seen.add((p['platform'], 't', norm(p['text'])))

    done = read_logs(lib)
    w1, w2 = read_library(lib, 'wave1'), read_library(lib, 'wave2')
    wave1_open = [r for r in w1 if r['id'] not in done and not r['id'].startswith('HOLD-')]
    rows = sorted(wave1_open if wave1_open else [r for r in w2 if r['id'] not in done], key=lambda r: r['id'])
    rep['wave'] = 'wave1' if wave1_open else 'wave2'
    for r in w1 + w2:
        if r['id'].startswith('HOLD-') and now <= r['ts'] <= now + dt.timedelta(days=14):
            rep['hold_soon'].append((r['id'], r['ts'].isoformat()))
    rep['left'] = sum(1 for r in w1 + w2 if r['id'] not in done and not r['id'].startswith('HOLD-'))

    earliest = now + dt.timedelta(hours=1)
    loads = []
    for r in rows:
        if sum(1 for x in loads if not x.get('present')) >= room:
            break
        if r['id'].startswith('HOLD-'):
            continue
        plat, acct = r['platform'], ACCOUNTS.get(r['platform'])
        if not acct:
            rep['skipped'].append((r['id'], f'unknown platform {plat}'))
            continue
        if plat == 'twitter' and len(r['text']) > X_LIMIT:
            rep['skipped'].append((r['id'], f'X post is {len(r["text"])} characters, over {X_LIMIT}'))
            continue
        if (plat, 'm', r['media']) in seen or (plat, 't', norm(r['text'])) in seen:
            rep['dupes'].append(r['id'])
            loads.append(dict(row=r, present=True))
            continue
        placed = None
        day = max(r['ts'].date(), now.date())
        for _ in range(90):
            options = slots(plat, day)
            own = r['ts'].strftime('%H:%M')
            if own in options:
                options = [own] + [s for s in options if s != own]
            if per_day[(plat, acct, day)] < cap(plat, day):
                for s in options:
                    ts = dt.datetime.combine(day, dt.time.fromisoformat(s))
                    if ts > earliest and (plat, acct, ts) not in taken:
                        placed = ts
                        break
            if placed:
                break
            day += dt.timedelta(days=1)
        if not placed:
            rep['skipped'].append((r['id'], 'no open slot in the next 90 days'))
            continue
        taken.add((plat, acct, placed))
        per_day[(plat, acct, placed.date())] += 1
        seen.add((plat, 'm', r['media']))
        seen.add((plat, 't', norm(r['text'])))
        if placed != r['ts']:
            rep['moved'].append((r['id'], r['ts'].isoformat(), placed.isoformat()))
        loads.append(dict(row=r, at=placed, args=create_args(r, placed)))
    return loads, rep


def create_args(r, at):
    """Arguments for the blotato_create_post MCP tool."""
    a = dict(accountId=ACCOUNTS[r['platform']], platform=r['platform'], text=r['text'],
             mediaUrls=[MEDIA_BASE + r['media']] if r['media'] and r['media'] != '-' else [],
             scheduledTime=at.strftime('%Y-%m-%dT%H:%M:00Z'))
    if r['platform'] == 'facebook':
        a['pageId'] = FB_PAGE
    if r['platform'] == 'youtube':
        a.update(title=r['title'] if r['title'] != '-' else r['text'][:90], privacyStatus='public',
                 shouldNotifySubscribers=False)
    if r['platform'] == 'tiktok':
        a['privacyLevel'] = 'PUBLIC_TO_EVERYONE'
    return a


def rest_body(a):
    """The same post in the REST API's shape."""
    target = {'targetType': a['platform']}
    for k in ('pageId', 'title', 'privacyStatus', 'shouldNotifySubscribers', 'privacyLevel'):
        if k in a:
            target[k] = a[k]
    if a['platform'] == 'tiktok':
        target.update(disabledComments=False, disabledDuet=False, disabledStitch=False,
                      isBrandedContent=False, isYourBrand=False, isAiGenerated=False)
    return {'post': {'accountId': a['accountId'], 'target': target,
                     'content': {'text': a['text'], 'mediaUrls': a['mediaUrls'], 'platform': a['platform']}},
            'scheduledTime': a['scheduledTime']}


# ---------- outputs ----------

def central(iso):
    t = dt.datetime.fromisoformat(iso)
    off = 6 if t.date() >= DST_END else 5
    c = t - dt.timedelta(hours=off)
    return c.strftime('%a %b %-d, %-I:%M %p') + ' Central'


def append_log(lib, entries, today):
    for wave in ('wave1', 'wave2'):
        lines = [f'{rid} {how} {today}' for rid, w, how in entries if w == wave]
        if lines:
            with open(os.path.join(lib, 'content', f'{wave}-loaded.log'), 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines) + '\n')


def write_report(path, rep, loaded, failed_new, executed):
    L = [f'# Blotato refill, {rep["now"][:10]}', '']
    if rep.get('stop'):
        L += [rep['stop'], '']
    else:
        verb = 'Loaded' if executed else 'Would load (propose only, nothing sent)'
        L += [f'- Queue before: {rep["queued"]} of {QUEUE_CAP}, {rep["free"]} free, {rep.get("reserve", 0)} held for Halloween',
              f'- {verb}: {len(loaded)} from {rep.get("wave")}', f'- Rows left to load across both waves: {rep.get("left")}']
        if loaded:
            last = max(loaded, key=lambda x: x['at'])
            L.append(f'- Last row reached: {loaded[-1]["row"]["id"]}, queue now runs to {central(last["at"].isoformat())}')
        if rep.get('left', 99) <= 30:
            L.append('- Fewer than 30 rows left. Wave 3 needs building.')
    for rid, a, b in rep['moved']:
        L.append(f'- Moved {rid} from {central(a)} to {central(b)}')
    if rep['dupes']:
        L.append(f'- Already in the queue or already posted, so skipped and marked done: {len(rep["dupes"])} ({", ".join(rep["dupes"])})')
    for rid, why in rep['skipped']:
        L.append(f'- Did not load {rid}: {why}')
    for rid, when in rep['hold_soon']:
        L.append(f'- {rid} is a HOLD row due {central(when)}. It waits for you.')
    for f in failed_new:
        loud = 'TIKTOK, costs points. ' if f.get('platform') == 'tiktok' else ''
        L.append(f'- FAILED {loud}{f.get("platform")} {f.get("postTime", "")}: {f.get("errorMessage", "")}')
    text = '\n'.join(L) + '\n'
    if path:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        open(path, 'w', encoding='utf-8').write(text)
    print(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['plan', 'apply', 'log'])
    ap.add_argument('--lib', required=True)
    ap.add_argument('--queue-file')
    ap.add_argument('--out')
    ap.add_argument('--plan')
    ap.add_argument('--ids', default='')
    ap.add_argument('--report')
    ap.add_argument('--reserve', type=int)
    ap.add_argument('--execute', action='store_true')
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None, second=0, microsecond=0)
    today = now.date().isoformat()

    if a.cmd == 'log':
        p = json.load(open(a.plan))
        want = set(filter(None, a.ids.split(',')))
        entries = [(x['id'], x['wave'], 'present' if x.get('present') else 'loaded') for x in p
                   if x.get('present') or x['id'] in want]
        append_log(a.lib, entries, today)
        print(f'logged {len(entries)}')
        return

    key = os.environ.get('BLOTATO_API_KEY')
    if a.queue_file:
        queue, published, failed = json.load(open(a.queue_file)), [], []
    elif key:
        queue = fetch_queue(key)
        published = [dict(platform=p.get('platform'), text=(p.get('content') or {}).get('text', p.get('text', '')),
                          media=media_name(((p.get('content') or {}).get('mediaUrls') or p.get('mediaUrls') or [''])[0]))
                     for p in fetch_recent(key, 'published', 30)]
        failed = [f for f in fetch_recent(key, 'failed', 3)]
    else:
        sys.exit('Need --queue-file or BLOTATO_API_KEY')

    loads, rep = plan(a.lib, queue, now, published, a.reserve)
    new = [x for x in loads if not x.get('present')]
    if a.cmd == 'plan':
        if a.out:
            json.dump([dict(id=x['row']['id'], wave=x['row']['wave'], present=bool(x.get('present')),
                            args=x.get('args')) for x in loads], open(a.out, 'w'), indent=1)
        write_report(a.report, rep, new, failed, False)
        return

    if not key:
        sys.exit('apply needs BLOTATO_API_KEY')
    done = [(x['row']['id'], x['row']['wave'], 'present') for x in loads if x.get('present')]
    sent = []
    if a.execute:
        for x in new:
            try:
                api('POST', '/posts', key, body=rest_body(x['args']))
            except RuntimeError as e:
                if 'maximum number of scheduled posts' in str(e):
                    rep['stop'] = 'Queue reached 200, which means full, not broken.'
                    break
                rep['skipped'].append((x['row']['id'], str(e)))
                continue
            sent.append(x)
            done.append((x['row']['id'], x['row']['wave'], 'loaded'))
        append_log(a.lib, done, today)
    write_report(a.report, rep, sent if a.execute else new, failed, a.execute)


if __name__ == '__main__':
    main()
