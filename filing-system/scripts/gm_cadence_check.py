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
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime

ANCHOR_DEFAULT = "15:00"

# her targets and her measured limits
MIN_PER_DAY = 3
MAX_PER_DAY = 5

# Per channel overrides, because 3 to 5 is not the rule everywhere.
# LinkedIn is 1 a day and always business. X is 0, dropped 09/08 because it
# was not serving. Keeping these in a CSV rather than in this file means the
# rule can be read by anything, and changed without touching the gate.
CHANNEL_RULES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "channel-rules.csv")


def load_channel_rules(path=CHANNEL_RULES):
    """Channel -> (min, max). Falls back to 3 to 5 for anything unlisted."""
    rules = {}
    try:
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh):
                ch = (r.get("Channel") or "").strip().lower()
                if not ch:
                    continue
                try:
                    rules[ch] = (int(r["MinPerDay"]), int(r["MaxPerDay"]))
                except (KeyError, ValueError):
                    continue
    except OSError:
        pass
    return rules
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
                # Every rule here is per platform or per account. Without these
                # 2 columns the checks collapse into 1 stream and start
                # contradicting the doctrine they exist to enforce: 4 platforms
                # posting 4 times each reads as 16 posts in a day, and
                # Instagram at 15:00 alongside TikTok at 15:00 reads as a
                # collision. A file without them is checked as a single lane,
                # which is right for 1 account and wrong for a board.
                "platform": (r.get("platform") or "").strip().lower(),
                "account": (r.get("accountId") or r.get("account") or "").strip(),
            })
    return rows


def countdown_days(label):
    """Pull an explicit countdown number out of a label, if it carries one."""
    m = re.search(r"countdown(\d+)", label, re.I)
    return int(m.group(1)) if m else None


def check(rows, anchor=ANCHOR_DEFAULT, target=None):
    findings = []

    # 3 to 5 a day is 3 to 5 *per platform*. Counting a board of 4 platforms
    # as 1 stream is what made a full day look overloaded and started a queue
    # being thinned that was already starved.
    # Counted per account, not per platform: the 2 Instagram accounts are 2
    # audiences, and 3 to 5 is what each of them gets. Platform is the label
    # in the message; the account is the thing being saturated.
    by_lane = defaultdict(list)
    for r in rows:
        by_lane[(r["day"], r["account"] or r["platform"])].append(r)

    rules = load_channel_rules()
    for day, lane in sorted(by_lane):
        posts = sorted(by_lane[(day, lane)], key=lambda r: r["time"])
        platform = posts[0]["platform"]
        where = (" on %s %s" % (platform, lane)).rstrip() if platform else ""
        lo, hi = rules.get(platform, (MIN_PER_DAY, MAX_PER_DAY))

        # A channel set to 0 is not starved, it is retired. Posting to it at
        # all is the finding.
        if hi == 0:
            findings.append({
                "rule": "C07_RETIRED_CHANNEL",
                "day": day,
                "detail": "%d post(s) on %s, which was dropped. Nothing schedules here."
                          % (len(posts), platform),
                "ids": [p["id"] for p in posts],
            })
            continue

        if len(posts) < lo:
            findings.append({
                "rule": "C01_DAY_STARVED",
                "day": day,
                "detail": "%d post(s)%s, target is %d to %d a day"
                          % (len(posts), where, lo, hi),
                "ids": [p["id"] for p in posts],
            })
        if len(posts) > hi:
            findings.append({
                "rule": "C01_DAY_OVER",
                "day": day,
                "detail": "%d posts%s, target is %d to %d a day"
                          % (len(posts), where, lo, hi),
                "ids": [p["id"] for p in posts],
            })


    # 1 post per platform per timestamp. 2 platforms at 15:00 is the cross
    # posting model working, not a collision, so this groups by platform.
    by_platform = defaultdict(list)
    for r in rows:
        by_platform[(r["day"], r["platform"])].append(r)
    for day, platform in sorted(by_platform):
        seen = defaultdict(list)
        for p in by_platform[(day, platform)]:
            seen[p["time"]].append(p["id"])
        for t, ids in sorted(seen.items()):
            if len(ids) > 1:
                findings.append({
                    "rule": "C02_SLOT_COLLISION",
                    "day": day,
                    "detail": "%d posts%s at exactly %s UTC"
                              % (len(ids), " on " + platform if platform else "", t),
                    "ids": ids,
                })

    # 2 posts on 1 account inside 2 hours bury each other. Measured:
    # 2 reels 2 seconds apart took 1818 views and 162. The rule is about
    # 1 account's own feed, so it is checked per account, never across them.
    by_account = defaultdict(list)
    for r in rows:
        by_account[(r["day"], r["account"] or r["platform"])].append(r)
    for key in sorted(by_account):
        day = key[0]
        posts = sorted(by_account[key], key=lambda r: r["time"])
        for a, b in zip(posts, posts[1:]):
            gap = _mins(b["time"]) - _mins(a["time"])
            if gap < MIN_GAP_MIN:
                findings.append({
                    "rule": "C05_TOO_CLOSE",
                    "day": day,
                    "detail": "%s and %s are %d min apart on 1 account, minimum is %d"
                              % (a["time"], b["time"], gap, MIN_GAP_MIN),
                    "ids": [a["id"], b["id"]],
                })

    for r in sorted(rows, key=lambda r: (r["day"], r["time"])):
        if DEAD_START <= _mins(r["time"]) < DEAD_END:
            findings.append({
                "rule": "C06_DEAD_HOUR",
                "day": r["day"],
                "detail": "%s UTC falls in the dead window %s to %s, nobody is awake for it"
                          % (r["time"], DEAD_FROM, DEAD_TO),
                "ids": [r["id"]],
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
    lanes = sorted({r["platform"] for r in rows if r["platform"]})
    print("%d posts across %d days" % (len(rows), days))
    if lanes:
        # Per platform is the number that matters. The total is only ever
        # context, and reading the total as the cadence is the mistake that
        # this gate exists to stop anyone making twice.
        rules = load_channel_rules()
        for lane in lanes:
            n = sum(1 for r in rows if r["platform"] == lane)
            per = n / days if days else 0
            lo, hi = rules.get(lane, (MIN_PER_DAY, MAX_PER_DAY))
            mark = "" if lo <= per <= hi else "   <-- off target"
            print("  %-10s %3d posts, %.1f a day  (target %d to %d)%s"
                  % (lane, n, per, lo, hi, mark))
    else:
        print("  no platform column, checked as a single lane, %.1f a day (target %d to %d)"
              % (len(rows) / days if days else 0, MIN_PER_DAY, MAX_PER_DAY))
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
