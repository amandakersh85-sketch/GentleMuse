#!/usr/bin/env python3
"""Validate a Gentle Muse wave staging library against the SOP v3 rules.

Usage: python3 scripts/validate-wave.py content/wave1-staging-library.txt

Exits non-zero if any check fails. Run after any edit to a library file, before
letting the daily Blotato top-up near it. Every rule here traces to a real
incident, not a preference.
"""
import re, sys
from collections import Counter, defaultdict
from datetime import datetime

DEAD = ['reset-guide.subscribepage.io', 'preview.mailerlite.io', 'gentlemuse.co/reset-guide']
FIELDS = ['id', 'ts', 'plat', 'media', 'yt', 'text']
IG_SLOTS = ('15:00', '23:00')


def load(path):
    raw = open(path).read()
    body = raw.split('=== ROWS ===', 1)[-1]
    return [l for l in body.split('\n') if l.strip() and l.count('|') == 5]


def main(path):
    rows = load(path)
    parsed = [dict(zip(FIELDS, r.split('|'))) for r in rows]
    fails = []

    def chk(ok, msg):
        print(('  PASS  ' if ok else '  FAIL  ') + msg)
        if not ok:
            fails.append(msg)

    print(f'Validating {len(parsed)} rows from {path}\n')

    chk(bool(parsed), 'file contains rows')

    slots = Counter((p['plat'], p['ts']) for p in parsed)
    chk(not [k for k, v in slots.items() if v > 1],
        'no two rows share a platform and timestamp')

    chk(not [p for p in parsed if re.search(r'day\s*\d+\s*of\s*60', p['text'], re.I)],
        'no Day X of 60 content')
    chk(not [p for p in parsed if re.search(
        r'(octopus|fluffy cloud|52-card|nerve signals|neuroplasticity|birthday paradox)',
        p['text'], re.I)], 'no trivia filler')

    chk(not [p for p in parsed if p['plat'] == 'instagram'
             and len(re.findall(r'#\w+', p['text'])) > 5],
        'Instagram rows carry 5 hashtags or fewer')
    chk(not [p for p in parsed if p['plat'] in ('facebook', 'linkedin')
             and re.findall(r'#\w+', p['text'])],
        'Facebook and LinkedIn rows carry no hashtags')

    aff = [p for p in parsed if 'club.target.com' in p['text'] or 'TargetPartner' in p['text']]
    chk(all('#TargetPartner' in p['text'] and '#ad' in p['text'] for p in aff),
        f'all {len(aff)} affiliate rows keep #TargetPartner and #ad')
    chk(not [p for p in parsed if re.search(r'\$\d', p['text'])],
        'no row states a price (open TikTok Shop violation, 04 Aug 2026)')

    ig = defaultdict(list)
    for p in parsed:
        if p['plat'] == 'instagram':
            ig[p['ts'][:10]].append(p['ts'][11:])
    chk(not [d for d, v in ig.items() if len(v) > 2], 'max 2 Instagram posts a day')
    chk(not [d for d, v in ig.items()
             if datetime.fromisoformat(d).weekday() >= 5 and len(v) > 1],
        'weekends carry 1 Instagram post')
    chk(not [t for v in ig.values() for t in v if t not in IG_SLOTS],
        'Instagram only at 15:00 or 23:00 UTC')
    chk(not [p for p in parsed if p['plat'] == 'instagram' and p['ts'][11:] == '17:00'],
        'no Instagram at the retired 17:00 UTC noon slot')

    chk(not [p for p in parsed if any(x in p['text'] for x in DEAD)],
        'no dead or superseded links')
    chk(not [p for p in parsed if len(p['text'].strip()) < 20],
        'no empty or stub text')

    print()
    if fails:
        print(f'RESULT: {len(fails)} FAILURES')
        return 1
    print('RESULT: ALL CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else 'content/wave1-staging-library.txt'))
