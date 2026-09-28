#!/usr/bin/env python3
"""Make the day's trivia: 1 checked fact, 1 HeyGen video, 4 captions, 1 PR.

  python3 make.py                     propose: the fact and captions, nothing made
  python3 make.py --execute --out D   render, host on Blotato, write the package

The GitHub job `Daily trivia` runs this every morning, then opens a pull
request with the video and the captions. Amanda approves by merging it, and
the merge is what schedules the posts (schedule.py). Nothing posts without her.
Rules and their reasons are in README.md next to this file.

The fact, the platforms and the words come from filing-system/scripts/
gm_trivia_pick.py, which only reads data that already governs them. No model
writes anything. Every caption passes the trivia gate and the keyword gate
before a render is paid for.

The video is made with the HeyGen CLI, the same tool her own sessions use,
with HEYGEN_API_KEY from the environment. It is then copied to Blotato's own
storage, because a HeyGen link expires and approval can take days.

Exit 0 made or proposed, 1 refused or a gate failed, 2 nothing to make or it
could not be made. Nothing is written unless the whole day succeeded.
"""
import argparse, datetime as dt, json, os, subprocess, sys, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'filing-system', 'scripts'))
import gm_trivia_bank as B  # noqa: E402
import gm_trivia_pick as P  # noqa: E402

try:
    from zoneinfo import ZoneInfo
    CENTRAL = ZoneInfo('America/Chicago')
except ImportError:  # Python 3.8 has no zoneinfo. Central daylight time is close enough to name a day.
    CENTRAL = dt.timezone(dt.timedelta(hours=-5))

APPROVED = os.path.join(HERE, 'approved')
BLOTATO = os.environ.get('BLOTATO_API_BASE', 'https://backend.blotato.com/v2')


def as_json(text):
    try:
        return json.loads(text)
    except ValueError:
        return None


def heygen(cmd, args):
    """Run the HeyGen CLI and return its JSON. A result comes on stdout. An
    error comes on stderr as {"error": {"code": ..., "message": ...}} with a
    non-zero exit, followed by a long hint that is not worth repeating."""
    r = subprocess.run([cmd] + args, capture_output=True, text=True, timeout=120)
    out = as_json(r.stdout)
    if r.returncode != 0 or not isinstance(out, dict) or 'error' in out:
        blob = as_json(r.stderr) or out or {}
        err = blob.get('error') if isinstance(blob, dict) else None
        why = (f"{err.get('code', 'error')}: {err.get('message')}" if isinstance(err, dict)
               else (r.stderr or r.stdout).strip()[:200])
        raise RuntimeError(f'heygen {args[0]} {args[1]} failed, {why}')
    return out


def render(pkg, cmd, poll_seconds, wait_minutes):
    """Make the video and wait for it. Returns HeyGen's finished video record."""
    h = pkg['heygen']
    body = {'type': 'avatar', 'avatar_id': h['avatarId'], 'script': pkg['script'],
            'voice_id': h['voiceId'], 'voice_settings': {'speed': h['voiceSpeed']},
            'aspect_ratio': h['aspectRatio'], 'title': f"Trivia {pkg['factId']} {pkg['madeOn']}"}
    made = heygen(cmd, ['video', 'create', '-d', json.dumps(body)])
    vid = (made.get('data') or {}).get('video_id')
    if not vid:
        raise RuntimeError(f'heygen video create returned no video_id: {json.dumps(made)[:200]}')
    deadline = time.time() + wait_minutes * 60
    while True:
        got = (heygen(cmd, ['video', 'get', vid]).get('data') or {})
        status = got.get('status')
        if status == 'completed' and got.get('video_url'):
            return dict(got, id=vid)
        if status == 'failed':
            raise RuntimeError(f"HeyGen could not make {vid}: {got.get('failure_message') or got.get('failure_code') or 'no reason given'}")
        if time.time() > deadline:
            raise RuntimeError(f'{vid} was still {status} after {wait_minutes} minutes. It may still finish in HeyGen.')
        time.sleep(poll_seconds)


def host(url, key):
    """Copy the video to Blotato's storage and return its permanent link."""
    req = urllib.request.Request(BLOTATO + '/media', method='POST', data=json.dumps({'url': url}).encode(),
                                 headers={'blotato-api-key': key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            out = json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'Blotato would not take the video, HTTP {e.code}: {e.read().decode(errors="replace")[:200]}')
    if not out.get('url'):
        raise RuntimeError(f'Blotato returned no media url: {json.dumps(out)[:200]}')
    return out['url']


def pr_body(pkg):
    day = dt.date.fromisoformat(pkg['madeOn']).strftime('%A %m/%d')
    L = [f"## Trivia for {day}: {pkg['factId']}", '',
         f"**Watch the video:** {pkg['video']['url']}", '',
         f"> {pkg['fact']}", '>', f"> {pkg['backbone']}", '',
         f"Source: [{pkg['source']}]({pkg['sourceUrl']}), read {pkg['verifiedOn']}. "
         f"{pkg['heygen']['avatarName']}, voice at {pkg['heygen']['voiceSpeed']}.", '',
         '**Merge to approve.** The 4 posts go into the next open daytime slots. '
         '**Close to skip** this fact. It will not be made again.', '']
    for p in pkg['posts']:
        L += [f"### {p['platform'].capitalize()}", '```', p['text'], '```', '']
    L += ['Every caption passed the trivia gate and the keyword gate before the video was made.']
    return '\n'.join(L) + '\n'


def outputs(**kv):
    path = os.environ.get('GITHUB_OUTPUT')
    if path:
        with open(path, 'a') as f:
            for k, v in kv.items():
                f.write(f'{k}={v}\n')


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--execute', action='store_true', help='render and host. Without it nothing is made')
    ap.add_argument('--fact', help='make this fact instead of the next one')
    ap.add_argument('--skip', default='', help='fact ids to pass over, comma separated (declined ones)')
    ap.add_argument('--date', help='the day, YYYY-MM-DD. Default today in Central time')
    ap.add_argument('--out', default='out', help='where the PR text goes')
    ap.add_argument('--heygen', default='heygen', help='the HeyGen CLI')
    ap.add_argument('--poll-seconds', type=int, default=20)
    ap.add_argument('--wait-minutes', type=int, default=30)
    ap.add_argument('--approved', default=APPROVED)
    ap.add_argument('--bank', default=B.DEFAULT_BANK)
    ap.add_argument('--sources', default=B.DEFAULT_SOURCES)
    ap.add_argument('--pr-body', metavar='PACKAGE', help='only write the PR text for a package already made')
    a = ap.parse_args(argv)

    if a.pr_body:
        # A day made on an earlier run whose pull request never opened. No new video.
        with open(a.pr_body, encoding='utf-8') as f:
            pkg = json.load(f)
        os.makedirs(a.out, exist_ok=True)
        with open(os.path.join(a.out, 'pr-body.md'), 'w', encoding='utf-8') as f:
            f.write(pr_body(pkg))
        return 0

    day = dt.date.fromisoformat(a.date) if a.date else dt.datetime.now(CENTRAL).date()
    skip = P.approved_ids(a.approved) | {s.strip().upper() for s in a.skip.split(',') if s.strip()}
    pkg, code, lines = P.build(B.load_bank(a.bank), day, fact_id=a.fact, skip=skip, sources=a.sources)
    for line in lines:
        print(line)
    if pkg is None:
        return code

    if not a.execute:
        print('PROPOSED. Nothing was made. Add --execute to render it.\n')
        print(json.dumps(pkg, indent=2, ensure_ascii=False))
        return 0

    missing = [k for k in ('HEYGEN_API_KEY', 'BLOTATO_API_KEY') if not os.environ.get(k)]
    if missing:
        print(f"{' and '.join(missing)} not set, so nothing was made.")
        return 2
    try:
        print(f"Rendering {pkg['factId']} as {pkg['heygen']['avatarName']}")
        video = render(pkg, a.heygen, a.poll_seconds, a.wait_minutes)
        print(f"Rendered {video['id']}, {video.get('duration', '?')} seconds. Hosting it on Blotato.")
        pkg['video'] = {'heygenVideoId': video['id'], 'duration': video.get('duration'),
                        'url': host(video['video_url'], os.environ['BLOTATO_API_KEY'])}
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as e:
        print(f'Nothing was made. {e}')
        return 2

    name = f"{pkg['madeOn']}-{pkg['factId']}"
    os.makedirs(a.approved, exist_ok=True)
    with open(os.path.join(a.approved, name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(pkg, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, 'pr-body.md'), 'w', encoding='utf-8') as f:
        f.write(pr_body(pkg))
    title = f"Daily trivia for {dt.date.fromisoformat(pkg['madeOn']):%a %m/%d}: {pkg['factId']}"
    outputs(made='true', branch=f'daily-trivia/{name}', title=title, file=f'daily-trivia/approved/{name}.json')
    print(f"Made {name}. Video: {pkg['video']['url']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
