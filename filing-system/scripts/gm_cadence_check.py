#!/usr/bin/env python3
"""
gm_cadence_check.py - the follower-growth gate.

Amanda's 500 to 1000 Instagram goal has one measured rule behind it,
recorded in posting-cadence.csv: 1 reel a day, at 10:00 America/Chicago.
Her own numbers are the reason. 15 reels in a single day produced 1330
views. 1 good reel produced 7726. Posting more does not add reach on
Instagram, it splits it.

Guidance did not hold that line. Three separate build waves each added
posts to the same days and nothing refused them, so the queue drifted to
2 and 3 and 6 posts on a day. This script is the missing check, not
another reminder.

It reads a queue snapshot and reports:

  C01_DAY_OVERLOAD    more than 1 Instagram post on a calendar day
  C02_SLOT_COLLISION  2 posts at the exact same minute
  C03_ANCHOR_MISSING  a day with posts but none in the 10:00 slot
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

        if len(posts) > 1:
            findings.append({
                "rule": "C01_DAY_OVERLOAD",
                "day": day,
                "detail": "%d Instagram posts on 1 day, the rule is 1" % len(posts),
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

        if posts and not any(p["time"] == anchor for p in posts):
            findings.append({
                "rule": "C03_ANCHOR_MISSING",
                "day": day,
                "detail": "nothing in the %s UTC slot, the best hour goes unused" % anchor,
                "ids": [p["id"] for p in posts],
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
    print("%d Instagram posts across %d days (%.1f per day, the rule is 1.0)"
          % (len(rows), days, len(rows) / days if days else 0))
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
    sys.exit(main(sys.argv))
