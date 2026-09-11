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
  C08_FACT_TWICE      the same fact twice on 1 channel on 1 day, except on a
                      channel marked RepeatExempt, where repeating is the
                      mechanism rather than the mistake
  C09_FACT_OVERPLAYED the same fact more than 2 times on 1 channel across
                      the window, or 2 airings closer together than 3 days
  C10_FACT_UNLABELLED a row with no fact, which the 2 rules above cannot
                      be run against
  C11_CHANNEL_SILENT  a channel that is supposed to post and has nothing at
                      all on a day in the window. Read off the roster column,
                      not off the rows, because a channel with no rows makes
                      no group and every other rule skips it in silence.
  C12_RUNWAY_END      slots held on the far side of a hole 5 days or longer,
                      while the near days are the empty ones

Fill the fact column from what the caption *opens* with, not from the whole
caption. The CTA, the link and the hashtags are identical across a lane and
drown the 1 part that says what the post is about: matching whole captions
scored a correct pair at 0.21 and split Hocus Pocus into 2 facts, which let a
real repeat through. And 4 plates of 1 fact are 1 fact here. A different
plate is a different reel and the same thing said twice.

Exit code 1 when anything is flagged, so it can gate a scheduling run.

Usage:
  gm_cadence_check.py <snapshot.csv> [--anchor 15:00] [--target 2026-10-31]

Snapshot columns: id, postTimeUTC, label, platform, accountId, fact
postTimeUTC is UTC.

The fact column is the one added on 09/08/2026, after a refill put the same
Disney reel on YouTube 6 times in 11 days and the same TikTok fact twice in
1 day. Nothing in the board recorded what a post was *about*, so no gate
could see it. Volume is not variety, and a queue that only counts posts
cannot tell the difference. A row with no fact fails rather than passes,
because a check that silently skips is worse than no check. The anchor default 15:00 UTC is 10:00 America/Chicago
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

# How often 1 fact may run on 1 channel.
#
# Amanda, 09/10/2026: "re-air is fine after 4+ days". That replaces the count
# cap with a spacing rule. The 2 airing cap was mine, set on 09/08 when 1 fact
# had run 6 times in 11 days, and the real complaint then was 6 airings inside
# a fortnight and twice in a day, not the number itself. Spacing fixes both.
#
# MAX_AIRINGS = 0 means no cap on the count. Twice in 1 day is still refused
# by C08, which is the rule she actually stated and never softened.
MAX_AIRINGS = 0
MIN_FACT_GAP_DAYS = 4

# A hole this long with posts stranded on the far side of it. A day or 2
# of sparseness is ordinary; 5 is a week of silence with slots already
# spent on the other side, which is what the cap punishes.
MIN_RUNWAY_HOLE_DAYS = 5

# Per channel overrides, because 3 to 5 is not the rule everywhere.
# LinkedIn is 1 a day and always business. X is 0, dropped 09/08 because it
# was not serving. Keeping these in a CSV rather than in this file means the
# rule can be read by anything, and changed without touching the gate.
CHANNEL_RULES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "channel-rules.csv")


def load_repeat_exempt(path=CHANNEL_RULES):
    """Channels where repeating a fact is the mechanism, not a mistake.

    Pinterest is the only one. A pin is a bookmark, so repinning the same
    image is how the platform works, and C08 and C09 flagging it is the gate
    enforcing a rule the house policy already exempts. Read from the CSV so
    the exemption is a fact about the channel, not a name buried in here.
    """
    out = set()
    try:
        with open(path, newline="") as fh:
            for r in csv.DictReader(fh):
                if (r.get("RepeatExempt") or "").strip().lower() in ("yes", "true", "1"):
                    ch = (r.get("Channel") or "").strip().lower()
                    if ch:
                        out.add(ch)
    except OSError:
        pass
    return out


def load_channel_rules(path=CHANNEL_RULES):
    """Channel -> (min, max). Falls back to 3 to 5 for anything unlisted.

    This is the roster as well as the rule. C01 can only flag a channel that
    is already in the file being checked, so a channel with nothing scheduled
    produces no group and no finding: Pinterest sat at 0 posts for 11 days
    and every check passed. C11 walks this roster instead, which is the only
    place that knows a channel is meant to be posting at all.
    """
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
                # What the caption claims about how far out the campaign is.
                # C04 read "label" and the snapshot had stopped writing one,
                # so the rule ran against an always-empty cell and passed
                # everything. A rule reading a column nobody fills is not a
                # rule, it is a line in a docstring.
                "countdown": (r.get("countdown") or "").strip(),
                # Every rule here is per platform or per account. Without these
                # 2 columns the checks collapse into 1 stream and start
                # contradicting the doctrine they exist to enforce: 4 platforms
                # posting 4 times each reads as 16 posts in a day, and
                # Instagram at 15:00 alongside TikTok at 15:00 reads as a
                # collision. A file without them is checked as a single lane,
                # which is right for 1 account and wrong for a board.
                "platform": (r.get("platform") or "").strip().lower(),
                "account": (r.get("accountId") or r.get("account") or "").strip(),
                # What the post is about, not what file it plays. 2 renders
                # of 1 fact on 2 plates are still 1 fact to the person
                # scrolling, so the plate is not the thing to count.
                "fact": (r.get("fact") or "").strip().lower(),
                "has_fact_column": "fact" in r,
                # The channels this board is supposed to cover, carried on
                # every row by gm_board_snapshot.py. Without it, absence is
                # invisible: Pinterest held 0 posts for 11 days and the board
                # reported clean, because there were no Pinterest rows to
                # group. A file with no roster is a single lane, not a board,
                # and is not checked for silence.
                "roster": [c for c in (r.get("roster") or "").split("|") if c],
            })
    return rows


def countdown_days(cell):
    """The countdown a row states, as (number, inclusive).

    The snapshot writes 43n for "43 nights", which counts tonight, and 43d for
    "43 days out", which does not. Both phrasings are hers and both are right;
    they just do not mean the same arithmetic, so the gate has to be told
    which one it is looking at rather than guessing. The older countdown12
    label form still reads, so a board written by an earlier snapshot checks
    instead of silently passing.
    """
    cell = (cell or "").strip()
    m = re.search(r"countdown(\d+)", cell, re.I)
    if m:
        return int(m.group(1)), True
    m = re.match(r"^(\d{1,3})([nd])$", cell, re.I)
    if m:
        return int(m.group(1)), m.group(2).lower() == "n"
    return (int(cell), True) if cell.isdigit() else None


CAMPAIGNS = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "campaign-targets.csv")


def load_target(path=CAMPAIGNS):
    """The date the live countdown campaign is counting down to.

    C04 used to need --target on the command line, which meant it ran only
    when somebody remembered to pass it, which was never. The date belongs in
    the data next to everything else the gate reads.
    """
    if not os.path.exists(path):
        return None
    with open(path, newline="", encoding="utf-8") as fh:
        live = [r for r in csv.DictReader(fh) if r["Live"] == "yes"]
    return live[0] if live else None


def posting_window(rows):
    """The run of days the board is actually posting across.

    Not every day between the first and the last: a single post held for
    Halloween would make every channel look silent for 6 weeks. The window
    ends at the first gap of 2 days or more with nothing scheduled anywhere.
    """
    days = sorted({r["day"] for r in rows})
    if not days:
        return []
    window = [days[0]]
    for prev, nxt in zip(days, days[1:]):
        if (date.fromisoformat(nxt) - date.fromisoformat(prev)).days >= 2:
            break
        window.append(nxt)
    return window


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


    # A channel with nothing scheduled has no rows, so every rule above skips
    # it in silence. On 09/08 that hid Pinterest at 0 posts for 11 days while
    # the board reported clean. This walks the roster in channel-rules.csv
    # rather than the file, so absence is a finding rather than a blank.
    # Where the board actually runs out, and what is being held past it.
    #
    # The 200 post cap is a fixed number of slots, so a post held for
    # Halloween owns its slot for 7 weeks. On 09/08 that filled the queue
    # while the next 11 days starved, and on 09/09 the nightly backfill
    # tried it again: every row left in the backlog was dated Oct 12 or
    # later, and the board was about to run dry on Sep 19. Scheduling
    # oldest first is what does it, because the oldest waiting row is the
    # furthest from useful.
    if rows:
        window = posting_window(rows)
        allday = sorted({r["day"] for r in rows})
        beyond = [d for d in allday if d > window[-1]]
        # Running dry is not itself a finding, it is just where the runway
        # ends, and the summary prints it. The defect is holding slots on
        # the far side of a hole while the near days are the empty ones.
        if beyond:
            gap = (date.fromisoformat(beyond[0])
                   - date.fromisoformat(window[-1])).days - 1
            if gap >= MIN_RUNWAY_HOLE_DAYS:
                held = sum(1 for r in rows if r["day"] > window[-1])
                findings.append({
                    "rule": "C12_RUNWAY_END",
                    "day": window[-1],
                    "detail": "the board runs dry after %s, then %d empty day(s) "
                              "before the next post on %s. %d slot(s) are held "
                              "past the hole. Fill the near days first, they are "
                              "the ones an audience is waiting through."
                              % (window[-1], gap, beyond[0], held),
                    "ids": [],
                })

    roster = sorted({c for r in rows for c in r["roster"]})
    if rows and roster:
        window = posting_window(rows)
        present = defaultdict(set)
        for r in rows:
            if r["platform"]:
                present[r["platform"]].add(r["day"])
        for channel in roster:
            lo, _hi = rules.get(channel, (MIN_PER_DAY, MAX_PER_DAY))
            if lo <= 0:
                continue
            silent = [d for d in window if d not in present.get(channel, set())]
            if not silent:
                continue
            findings.append({
                "rule": "C11_CHANNEL_SILENT",
                "day": silent[0],
                "detail": "%s has nothing at all on %d of the %d days in the window "
                          "(%s). It is set to %d a day."
                          % (channel, len(silent), len(window),
                             ", ".join(silent[:6]) + (" ..." if len(silent) > 6 else ""),
                             lo),
                "ids": [],
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

    # What the board is about, per channel. Counting posts told us the queue
    # was healthy while 1 fact carried 6 of the 11 YouTube days. These 3 rules
    # are the difference between volume and variety.
    if any(r.get("has_fact_column") for r in rows):
        unlabelled = [r["id"] for r in rows if not r["fact"]]
        if unlabelled:
            findings.append({
                "rule": "C10_FACT_UNLABELLED",
                "day": "-",
                "detail": "%d row(s) carry no fact. The repeat rules cannot be run "
                          "against them, so the board is not checked. Fill the column."
                          % len(unlabelled),
                "ids": unlabelled[:20],
            })

        exempt = load_repeat_exempt()
        by_fact = defaultdict(list)
        for r in rows:
            if r["fact"] and r["platform"] not in exempt:
                by_fact[(r["account"] or r["platform"], r["fact"])].append(r)

        for key in sorted(by_fact):
            lane, fact = key
            posts = sorted(by_fact[key], key=lambda r: (r["day"], r["time"]))

            per_day = defaultdict(list)
            for p in posts:
                per_day[p["day"]].append(p)
            for day in sorted(per_day):
                if len(per_day[day]) > 1:
                    findings.append({
                        "rule": "C08_FACT_TWICE",
                        "day": day,
                        "detail": "\"%s\" runs %d times on %s in 1 day. Once a day is the rule."
                                  % (fact, len(per_day[day]), lane),
                        "ids": [p["id"] for p in per_day[day]],
                    })

            if MAX_AIRINGS and len(posts) > MAX_AIRINGS:
                findings.append({
                    "rule": "C09_FACT_OVERPLAYED",
                    "day": posts[0]["day"],
                    "detail": "\"%s\" runs %d times on %s (%s). The cap is %d."
                              % (fact, len(posts), lane,
                                 ", ".join(p["day"] for p in posts), MAX_AIRINGS),
                    "ids": [p["id"] for p in posts],
                })

            for a, b in zip(posts, posts[1:]):
                if a["day"] == b["day"]:
                    continue
                gap = (date.fromisoformat(b["day"]) - date.fromisoformat(a["day"])).days
                if gap < MIN_FACT_GAP_DAYS:
                    findings.append({
                        "rule": "C09_FACT_OVERPLAYED",
                        "day": b["day"],
                        "detail": "\"%s\" runs on %s and again %d day(s) later on %s. "
                                  "Minimum is %d days."
                                  % (fact, a["day"], gap, lane, MIN_FACT_GAP_DAYS),
                        "ids": [a["id"], b["id"]],
                    })

    campaign = load_target()
    if target or campaign:
        tgt = date.fromisoformat(target or campaign["TargetDate"])
        name = campaign["Campaign"] if campaign and not target else "the target"
        for r in rows:
            got = countdown_days(r.get("countdown") or r.get("label") or "")
            if got is None:
                continue
            n, inclusive = got
            out = (tgt - date.fromisoformat(r["day"])).days
            actual = out + 1 if inclusive else out
            if actual != n:
                findings.append({
                    "rule": "C04_COUNTDOWN_DRIFT",
                    "day": r["day"],
                    "detail": "caption says %d %s, but %s is %d %s from %s"
                              % (n, "nights" if inclusive else "days out", name,
                                 actual, "nights" if inclusive else "days out",
                                 r["day"]),
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
    if rows:
        window = posting_window(rows)
        if window:
            print("  runway ends %s" % window[-1])
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
