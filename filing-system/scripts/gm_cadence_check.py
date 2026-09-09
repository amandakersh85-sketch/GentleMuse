#!/usr/bin/env python3
"""
gm_cadence_check.py - the follower-growth gate.

Amanda's target is 3 to 5 posts per platform per day. Her words,
Sep 8 2026. The 200 post Blotato cap is a throughput valve, not a
ceiling on the plan, and the wave refill is what answers it.

What actually killed reach was never volume. It was 15 posts stacked on
1 timestamp, and 2 reels published 2 seconds apart taking 1818 views and
162. So the rules that matter are spacing and the live hours, not a
count of 1.

  C01_DAY_STARVED     fewer than 3 posts on a day, under target
  C01_DAY_OVER        more than 5 posts on a day, over target
  C02_SLOT_COLLISION  2 posts at the exact same minute
  C05_TOO_CLOSE       2 posts less than 2 hours apart on 1 account
  C06_DEAD_HOUR       a post in the hours the audience is not there
  C04_COUNTDOWN_DRIFT a caption counting down to a date that no longer
                      matches the day it is scheduled on

Exit code 1 when anything is flagged, so it can gate a scheduling run.

Usage:
  gm_cadence_check.py <snapshot.csv> [--anchor 15:00] [--target 2026-10-31]

Snapshot columns: id, postTimeUTC, label
postTimeUTC is UTC. The anchor default 15:00 UTC is 10:00 America/Chicago
during daylight time, which is the whole September and October window.
"""
import csv
import re
import sys
from collections import defaultdict
from datetime import date, datetime

ANCHOR_DEFAULT = "15:00"

# her targets and her measured limits
MIN_PER_DAY = 3
MAX_PER_DAY = 5
MIN_GAP_MIN = 120          # 2 hours between posts on 1 account
DEAD_FROM, DEAD_TO = "02:00", "13:00"   # 21:00 to 08:00 Central, the hours nobody is there
DEAD_START, DEAD_END = 2 * 60, 13 * 60


def _mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def load(path):
    rows = []
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            stamp = r["postTimeUTC"].strip()
            day, _, hhmm = stamp.partition("T")
            rows.append({
                "id": r["id"].strip(),
                "day": day,
                "time": hhmm[:5],
                "label": r.get("label", "").strip(),
            })
    return rows


def countdown_days(label):
    """Pull an explicit countdown number out of a label, if it carries one."""
    m = re.search(r"countdown(\d+)", label, re.I)
    return int(m.group(1)) if m else None


def check(rows, anchor=ANCHOR_DEFAULT, target=None):
    findings = []
    by_day = defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)

    for day in sorted(by_day):
        posts = sorted(by_day[day], key=lambda r: r["time"])

        if len(posts) < MIN_PER_DAY:
            findings.append({
                "rule": "C01_DAY_STARVED",
                "day": day,
                "detail": "%d post(s), target is %d to %d" % (len(posts), MIN_PER_DAY, MAX_PER_DAY),
                "ids": [p["id"] for p in posts],
            })
        if len(posts) > MAX_PER_DAY:
            findings.append({
                "rule": "C01_DAY_OVER",
                "day": day,
                "detail": "%d posts, target is %d to %d" % (len(posts), MIN_PER_DAY, MAX_PER_DAY),
                "ids": [p["id"] for p in posts],
            })

        seen = defaultdict(list)
        for p in posts:
            seen[p["time"]].append(p["id"])
        for t, ids in sorted(seen.items()):
            if len(ids) > 1:
                findings.append({
                    "rule": "C02_SLOT_COLLISION",
                    "day": day,
                    "detail": "%d posts at exactly %s UTC" % (len(ids), t),
                    "ids": ids,
                })

        # 2 posts on 1 account inside 2 hours bury each other. Measured:
        # 2 reels 2 seconds apart took 1818 views and 162.
        for a, b in zip(posts, posts[1:]):
            gap = _mins(b["time"]) - _mins(a["time"])
            if gap < MIN_GAP_MIN:
                findings.append({
                    "rule": "C05_TOO_CLOSE",
                    "day": day,
                    "detail": "%s and %s are %d min apart, minimum is %d"
                              % (a["time"], b["time"], gap, MIN_GAP_MIN),
                    "ids": [a["id"], b["id"]],
                })

        for p in posts:
            if DEAD_START <= _mins(p["time"]) < DEAD_END:
                findings.append({
                    "rule": "C06_DEAD_HOUR",
                    "day": day,
                    "detail": "%s UTC falls in the dead window %s to %s, nobody is awake for it"
                              % (p["time"], DEAD_FROM, DEAD_TO),
                    "ids": [p["id"]],
                })

    if target:
        tgt = date.fromisoformat(target)
        for r in rows:
            n = countdown_days(r["label"])
            if n is None:
                continue
            actual = (tgt - date.fromisoformat(r["day"])).days
            if actual != n:
                findings.append({
                    "rule": "C04_COUNTDOWN_DRIFT",
                    "day": r["day"],
                    "detail": "caption says %d days out, the date is %d days out" % (n, actual),
                    "ids": [r["id"]],
                })

    return findings


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    anchor = ANCHOR_DEFAULT
    target = None
    for i, a in enumerate(argv):
        if a == "--anchor" and i + 1 < len(argv):
            anchor = argv[i + 1]
        if a == "--target" and i + 1 < len(argv):
            target = argv[i + 1]

    rows = load(args[0])
    findings = check(rows, anchor=anchor, target=target)

    days = len({r["day"] for r in rows})
    print("%d Instagram posts across %d days (%.1f per day, target is %d to %d)"
          % (len(rows), days, len(rows) / days if days else 0, MIN_PER_DAY, MAX_PER_DAY))
    print()

    if not findings:
        print("cadence clean")
        return 0

    for f in findings:
        print("%-19s %s  %s" % (f["rule"], f["day"], f["detail"]))
        print("%-19s   %s" % ("", " ".join(f["ids"])))

    print()
    print("%d findings" % len(findings))
    return 1


if __name__ == "__main__":
    # piping into head closes the pipe early; that is not an error worth a stack trace
    try:
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
