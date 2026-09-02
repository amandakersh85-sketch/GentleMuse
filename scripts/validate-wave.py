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

# US Central drops to CST (UTC-6) on 1 Nov 2026, so a fixed UTC slot silently
# shifts an hour in local terms. Slots are defined to hold LOCAL time constant.
DST_END = '2026-11-01'


def ig_slots(day):
    """Allowed Instagram UTC slots for a given ISO date. 10:00 and evening Central."""
    return ('15:00', '23:00') if day < DST_END else ('16:00', '23:00')


def retired_noon(day):
    """The UTC value that equals noon Central, which is the retired slot."""
    return '17:00' if day < DST_END else '18:00'


def load(path):
    raw = open(path, encoding='utf-8').read()
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
    chk(not [(d, t) for d, v in ig.items() for t in v if t not in ig_slots(d)],
        'Instagram slots hold 10:00 Central across the DST change')
    chk(not [p for p in parsed if p['plat'] == 'instagram'
             and p['ts'][11:] == retired_noon(p['ts'][:10])],
        'no Instagram at the retired noon Central slot')

    chk(not [p for p in parsed if any(x in p['text'] for x in DEAD)],
        'no dead or superseded links')
    chk(not [p for p in parsed if len(p['text'].strip()) < 20],
        'no empty or stub text')

    # Seasonal campaign copy is newly written rather than recombined from posts
    # Amanda already published, so it must never auto-load unreviewed.
    SEASONAL = re.compile(
        r'(black ?friday|cyber ?monday|small business saturday|thanksgiving|'
        r'halloween|on sale|sale closes|sale is over|last call)', re.I)
    unheld = [p['id'] for p in parsed
              if SEASONAL.search(p['text']) and not p['id'].startswith('HOLD-')]
    chk(not unheld,
        f'all seasonal campaign rows are marked HOLD for review ({len(unheld)} loose)')

    # The Payhip sale_price field is stuck at a default; a row must never quote a
    # figure that could contradict the live listing.
    chk(not [p for p in parsed if re.search(r'\d+\s*%\s*off', p['text'], re.I)],
        'no row quotes a discount percentage')

    # Club Target pays points on TikTok only while Amanda is under 500 IG
    # followers. A theme scheduled to Instagram or Facebook with no TikTok twin
    # is a silent loss of the entire 30 points for that theme. This is exactly
    # how #TargetLittleFinds was nearly missed on 30 Aug 2026: 2 Instagram rows
    # and 1 Facebook row, zero TikTok.
    THEME = re.compile(r'#(Target(?!Partner\b)\w+|HeyDay\w+)')
    themes = {}
    for row in parsed:
        if 'ClubTarget' not in row['text'] and 'club.target.com' not in row['text']:
            continue
        for tag in THEME.findall(row['text']):
            themes.setdefault(tag, set()).add(row['plat'])
    orphans = sorted(t for t, plats in themes.items() if 'tiktok' not in plats)
    chk(not orphans,
        'every Club Target theme has a TikTok row, the only placement that '
        f'earns points ({len(orphans)} theme(s) with no TikTok: '
        f'{", ".join(orphans) if orphans else "none"})')

    print()
    if fails:
        print(f'RESULT: {len(fails)} FAILURES')
        return 1
    print('RESULT: ALL CHECKS PASSED')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1
                  else 'content/wave1-staging-library.txt'))
