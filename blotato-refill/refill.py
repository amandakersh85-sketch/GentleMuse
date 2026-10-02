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
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'filing-system', 'scripts'))
import gm_keyword_check as K  # noqa: E402  the same keyword gate every other loader answers to

API = 'https://backend.blotato.com/v2'
MEDIA_BASE = 'https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/'
QUEUE_CAP = 200
MIN_FREE = 10
# Kept free for the loaders that post on a promise: the nightly seasonal run and
# the daily trivia. They need about 4 a day, and the queue frees more than that
# every day. 40 held here from 09/23 to 09/28 stopped every run cold.
KEEP_FREE = 10
# The queue holds 200, about 10 days at full volume, so it fills the near days
# first and never reaches further than this. Amanda, 09/28: "we don't put it all
# in the queue, obviously".
HORIZON_DAYS = 7
DAY_CAP = 3                          # per account per Central day, everything counted
GAP = dt.timedelta(minutes=120)      # between posts on 1 account, as gm_cadence_check C05
DST_END = dt.date(2026, 11, 1)
DST_END_UTC = dt.datetime(2026, 11, 1, 7, 0)   # 2:00 AM Central daylight time
ACCOUNTS = {'facebook': '30840', 'instagram': '45886', 'youtube': '36129',
            'tiktok': '41488', 'linkedin': '20723'}
# Rows for these are skipped and counted, never loaded.
DROPPED = {'twitter': ('X', 'X is 0 a day since 09/08')}
FB_PAGE = '1086399221215093'
# Central time, so the clock time holds when the clocks go back on 1 Nov. The
# day's times (09/28): 10 AM trivia, noon Amanda, 2 PM newsletter or evergreen,
# 4 PM Club Target, 6 PM seasonal. The refill owns 2 PM only. Noon Central was
# retired on 24 Aug after a pileup (wave 1 header, validate-wave.py), and the
# other times belong to the lanes named. LinkedIn is 8:30 AM.
SLOTS = {'instagram': ['14:00'], 'tiktok': ['14:00'], 'facebook': ['14:00'], 'youtube': ['14:00'],
         'linkedin': ['08:30']}
CAPS = {'linkedin': 1}
# The 6 PM seasonal post: Halloween 33 Nights to 31 Oct, then The Real One to
# 1 Jan. It is held 2 hours clear even before its own loader has put it in.
EVENING = {'start': dt.date(2026, 9, 28), 'end': dt.date(2027, 1, 1),
           'times': {'instagram': '18:00', 'tiktok': '18:00', 'facebook': '18:30', 'youtube': '18:30'}}
# A caption that names a day of the week only goes out on that day. "Just
# Another Tuesday" is the newsletter's name, and TUESDAY in capitals is its
# keyword, so neither counts.
WEEKDAYS = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')


def to_central(ts):
    """A naive UTC datetime as Central wall-clock time."""
    return ts - dt.timedelta(hours=6 if ts >= DST_END_UTC else 5)


def utc_of(day, hhmm):
    """A Central day and clock time as naive UTC."""
    return dt.datetime.combine(day, dt.time.fromisoformat(hhmm)) + dt.timedelta(hours=6 if day >= DST_END else 5)


def cap(plat):
    return CAPS.get(plat, DAY_CAP)


def weekdays_named(text):
    t = re.sub(r'(?i)just another tuesday', '', text or '')
    return {i for i, w in enumerate(WEEKDAYS) if re.search(r'\b' + w + r'\b', t)}


def evening_clear(plat, day, ts):
    hhmm = EVENING['times'].get(plat)
    if not hhmm or not EVENING['start'] <= day <= EVENING['end']:
        return True
    return abs(ts - utc_of(day, hhmm)) >= GAP


def row_text(t):
    """A standalone forward slash in library text means a line break. URLs keep theirs."""
    return re.sub(r' ?(?<!\S)/(?!\S) ?', '\n', t).strip()


def norm(t):
    return re.sub(r'\s+', ' ', t or '').strip()[:120].lower()


def media_name(url):
    return (url or '').rsplit('/', 1)[-1]


def has_media(name):
    """A text-only row is written '-'. 2 text-only rows are not copies of each other."""
    return bool(name) and name != '-'


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
    headers = {'blotato-api-key': key}
    if body is not None:  # Blotato rejects a JSON content type with no body
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, method=method, headers=headers,
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

def plan(lib, queue, now, published=(), reserve=None, registry=None, cta=None):
    """Return (loads, report dict). Pure: no network, no writes."""
    rep = dict(now=now.isoformat(), queued=len(queue), dupes=[], skipped=[], refused=[], waiting=[],
               dropped=Counter(), hold_soon=[], stop=None)
    bad = validate(lib)
    if bad:
        rep['stop'] = 'Library check failed, loaded nothing: ' + ' | '.join(bad)
        return [], rep
    reserve = KEEP_FREE if reserve is None else reserve
    rep['reserve'] = reserve
    room = QUEUE_CAP - len(queue) - reserve
    rep['free'] = QUEUE_CAP - len(queue)
    if room < MIN_FREE:
        rep['stop'] = (f'Only {max(room, 0)} slots free after keeping {reserve} for the nightly run '
                       'and the daily trivia, so nothing loaded.')
        return [], rep
    registry = K.load_registry() if registry is None else registry
    cta = K.load_platform_cta() if cta is None else cta

    posts = []
    for q in queue:
        ts = dt.datetime.fromisoformat(q['scheduledAt'].replace('Z', '+00:00')).replace(tzinfo=None)
        posts.append(dict(q, ts=ts))
    taken = {(p['platform'], p['accountId'], p['ts']) for p in posts}
    on_day = defaultdict(list)  # (platform, account, Central day) -> UTC times, everything counted
    for p in posts:
        on_day[(p['platform'], p['accountId'], to_central(p['ts']).date())].append(p['ts'])
    seen = set()
    for p in list(posts) + [dict(x) for x in published]:
        if has_media(p.get('media')):
            seen.add((p['platform'], 'm', p['media']))
        if p.get('text'):
            seen.add((p['platform'], 't', norm(p['text'])))

    done = read_logs(lib)
    w1, w2 = read_library(lib, 'wave1'), read_library(lib, 'wave2')
    # Wave 1 first, then wave 2. Row dates are advisory: a row goes to the
    # nearest day with room, so a row that can never load (X, a dead keyword)
    # no longer holds wave 2 back.
    rows = sorted((r for r in w1 + w2 if r['id'] not in done and not r['id'].startswith('HOLD-')),
                  key=lambda r: (r['wave'], r['id']))
    for r in w1 + w2:
        if r['id'].startswith('HOLD-') and now <= r['ts'] <= now + dt.timedelta(days=14):
            rep['hold_soon'].append((r['id'], r['ts'].isoformat()))
    rep['left'] = sum(1 for r in rows if r['platform'] not in DROPPED)

    earliest = now + dt.timedelta(hours=1)
    first = to_central(now).date()
    days = [first + dt.timedelta(days=i) for i in range(HORIZON_DAYS + 1)]
    loads = []
    for r in rows:
        if sum(1 for x in loads if not x.get('present')) >= room:
            break
        plat = r['platform']
        if plat in DROPPED:
            rep['dropped'][plat] += 1
            continue
        acct = ACCOUNTS.get(plat)
        if not acct:
            rep['skipped'].append((r['id'], f'unknown platform {plat}'))
            continue
        if (has_media(r['media']) and (plat, 'm', r['media']) in seen) or (plat, 't', norm(r['text'])) in seen:
            rep['dupes'].append(r['id'])
            loads.append(dict(row=r, present=True))
            continue
        found = K.check_post(dict(id=r['id'], platform=plat, accountId=acct, text=r['text']), registry, cta)
        if found:
            rep['refused'].append((r['id'], '; '.join(f['detail'] for f in found)))
            continue
        named = weekdays_named(r['text'])
        placed = None
        for day in days:
            here = on_day[(plat, acct, day)]
            if (named and day.weekday() not in named) or len(here) >= cap(plat):
                continue
            for s in SLOTS[plat]:
                ts = utc_of(day, s)
                if (ts > earliest and (plat, acct, ts) not in taken
                        and all(abs(ts - t) >= GAP for t in here) and evening_clear(plat, day, ts)):
                    placed = ts
                    break
            if placed:
                break
        if not placed:
            rep['waiting'].append(r['id'])
            continue
        taken.add((plat, acct, placed))
        on_day[(plat, acct, to_central(placed).date())].append(placed)
        if has_media(r['media']):
            seen.add((plat, 'm', r['media']))
        seen.add((plat, 't', norm(r['text'])))
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

def central(t):
    if isinstance(t, str):
        t = dt.datetime.fromisoformat(t.replace('Z', ''))
    return to_central(t).strftime('%a %b %-d, %-I:%M %p') + ' Central'


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
        L += [f'- Queue before: {rep["queued"]} of {QUEUE_CAP}, {rep["free"]} free, '
              f'{rep.get("reserve", 0)} kept free for the nightly run and the daily trivia',
              f'- {verb}: {len(loaded)}, into the next {HORIZON_DAYS} days, up to {DAY_CAP} posts '
              'per account per day',
              f'- Rows left to load across both waves: {rep.get("left")}']
        if rep.get('left', 99) <= 30:
            L.append('- Fewer than 30 rows left. Wave 3 needs building.')
    for x in sorted(loaded, key=lambda x: x['at']):
        L.append(f'- {x["row"]["id"]} {x["row"]["platform"]}, {central(x["at"])}')
    if rep['dupes']:
        L.append(f'- Already in the queue or already posted, so skipped and marked done: {len(rep["dupes"])} ({", ".join(rep["dupes"])})')
    for rid, why in rep.get('refused', []):
        L.append(f'- Refused {rid}. It asks for a keyword nothing answers there: {why}')
    for plat, n in sorted(rep.get('dropped', {}).items()):
        name, why = DROPPED[plat]
        L.append(f'- Skipped {n} {name} rows. {why}.')
    if rep.get('waiting'):
        L.append(f'- {len(rep["waiting"])} rows wait for room in the next {HORIZON_DAYS} days. The next run tries again.')
    for rid, why in rep['skipped']:
        L.append(f'- Did not load {rid}: {why}')
    for rid, when in rep['hold_soon']:
        L.append(f'- {rid} is a HOLD row due {central(when)}. It waits for you.')
    for f in failed_new:
        loud = 'TIKTOK, costs points. ' if f.get('platform') == 'tiktok' else ''
        err = (f.get('state') or {}).get('errorMessage') or f.get('errorMessage', '')
        L.append(f'- FAILED {loud}{f.get("platform")} {central(f["postTime"][:16]) if f.get("postTime") else ""}: {err}')
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
