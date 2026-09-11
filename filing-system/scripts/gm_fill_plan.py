#!/usr/bin/env python3
"""
gm_fill_plan.py - propose posts for an empty day, without repeating too soon.

The nightly backfill needs to answer 1 question: this day is empty, what goes
on it. The board holds about 17 distinct video facts, so the answer is almost
always something that has run before, and the only thing that makes that fine
is how long ago.

Amanda, 09/10/2026: "re-air is fine after 4+ days". That is the whole rule.
There is no cap on how many times a fact runs, only on how close together.

The guard that matters most is on the history, not the plan
-----------------------------------------------------------
This picker is only as good as the history it checks against. The first run
of it on 09/10 was fed a queue dump whose rows had lost their caption text,
so every fact looked like it had never aired, and it cheerfully proposed
putting The Nightmare Before Christmas on YouTube 1 day after YouTube runs
it. Nothing in the output looked wrong. Every row said "last ran never".

So this refuses to plan against a history whose rows carry no text. A blind
history is worse than no history, because it produces a confident answer.

House rules, same as every other module:
  Propose-only. This script reads and prints a plan. It schedules nothing.
  Approval is the gate. A plan is a proposal.
  No substitution. When nothing clears the gap, it says so and leaves the
  slot empty rather than reaching for the nearest fact that fits.

Usage
  gm_fill_plan.py --day 2026-09-19 --history recent.json --queue queue.json

history: the items array from blotato_list_posts, which carries text.
queue:   the items array from blotato_list_schedules, for what is already
         on the day being filled.

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gm_board_snapshot as S  # noqa: E402

DATA = os.path.join(os.path.dirname(HERE), "data")
MIN_GAP_DAYS = 4          # Amanda, 09/10/2026
MIN_MINUTES_APART = 120
FLOOR = 3

SLOTS = {
    "36129": ["14:30", "17:20", "20:20", "23:20"],
    "41488": ["15:00", "17:00", "20:00", "23:00"],
    "30840": ["14:00", "17:00", "19:30", "22:00"],
    "45886": ["15:00", "18:00", "20:00", "23:00"],
}
PLATFORM = {"36129": "youtube", "41488": "tiktok",
            "30840": "facebook", "45886": "instagram"}


def fact_of(text, register):
    head = S.opening(text or "")
    best = (0.0, "")
    for slug, openings in register.items():
        score = max(S.containment(head, o) for o in openings)
        if score > best[0]:
            best = (score, slug)
    return S.FAMILY.get(best[1], best[1]) if best[0] >= S.THRESHOLD else ""


def load_history(path, day=None):
    """Recent posts with their captions. Refuses a history it cannot read.

    2 ways a history lies, and both produce a confident wrong answer rather
    than an error, which is why they are checked here rather than trusted:

      rows with no caption   every fact reads as never aired
      a history that stops   short of the day being filled, so whatever was
                             scheduled in between is invisible
    """
    items = json.load(open(path))
    if isinstance(items, dict):
        items = items.get("items", [])

    blind = [i for i in items if not (i.get("text") or "").strip()]
    if blind:
        raise SystemExit(
            "%d of %d history rows carry no text, so their facts cannot be "
            "read and every one of them would look like it never aired. "
            "Pull the history from blotato_list_posts, which returns the "
            "caption, rather than from a dump that dropped it."
            % (len(blind), len(items)))

    if day and items:
        newest = max(i["postTime"][:10] for i in items)
        need = (date.fromisoformat(day) - timedelta(days=1)).isoformat()
        if newest < need:
            raise SystemExit(
                "the history stops at %s and the day being filled is %s, so "
                "anything scheduled in between is invisible and would be "
                "proposed again too soon. Re-pull the history through %s."
                % (newest, day, need))
    return items


def load_inventory():
    inv = defaultdict(dict)
    with open(os.path.join(DATA, "staging-library.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            url = (r.get("MediaUrl") or "").strip()
            if not url.endswith(".mp4"):
                continue
            if (r.get("Status") or "").strip() != "STAGED":
                continue
            if not (r.get("Text") or "").strip():
                continue
            inv[r["Slug"].strip()][r["Platform"].strip()] = (
                url, r["Text"].replace("\\n", "\n"))
    return inv


def minutes(hhmm):
    return int(hhmm[:2]) * 60 + int(hhmm[3:])


def plan_day(day, history, queue, register, inv, cta):
    # Last airing per platform. Per platform rather than per account is the
    # stricter reading, and stricter is the safe direction here.
    last = defaultdict(dict)
    for item in history:
        f = fact_of(item.get("text"), register)
        if not f:
            continue
        d = item["postTime"][:10]
        p = item["platform"]
        if f not in last[p] or d > last[p][f]:
            last[p][f] = d

    taken = defaultdict(list)
    onday = defaultdict(set)
    for r in queue:
        if r["scheduledAt"][:10] != day:
            continue
        taken[str(r["draft"].get("accountId"))].append(r["scheduledAt"][11:16])
    for item in history:
        if item["postTime"][:10] != day:
            continue
        f = fact_of(item.get("text"), register)
        if f:
            onday[item["platform"]].add(f)

    out = []
    for acct, slots in SLOTS.items():
        platform = PLATFORM[acct]
        for _ in range(max(0, FLOOR - len(taken[acct]))):
            options = []
            for slug, per_platform in inv.items():
                if platform not in per_platform:
                    continue
                f = S.FAMILY.get(slug, slug)
                if f in onday[platform]:
                    continue
                ran = last[platform].get(f)
                if ran and (date.fromisoformat(day) - date.fromisoformat(ran)).days < MIN_GAP_DAYS:
                    continue
                options.append((ran or "0000-00-00", slug, f, ran))
            slot = next((s for s in slots
                         if all(abs(minutes(s) - minutes(t)) >= MIN_MINUTES_APART
                                for t in taken[acct])), None)
            if not options or slot is None:
                out.append({"account": acct, "platform": platform, "slug": None,
                            "why": "nothing clears the %d day gap" % MIN_GAP_DAYS
                                   if not options else "no slot %d min clear"
                                   % MIN_MINUTES_APART})
                continue
            options.sort()
            _, slug, f, ran = options[0]
            taken[acct].append(slot)
            onday[platform].add(f)
            url, text = inv[slug][platform]
            written = recaption(text, platform, acct, cta)
            if written is None:
                out.append({"platform": platform, "slug": None,
                            "why": "no call to action recorded for %s %s in "
                                   "cta-lines.csv" % (platform, acct)})
                continue
            out.append({"account": acct, "platform": platform, "day": day,
                        "time": slot, "slug": slug, "fact": f, "url": url,
                        "text": written,
                        "lastRan": ran or "not in this history"})
    return out


CTA_LINES = os.path.join(DATA, "cta-lines.csv")


def load_cta_lines(path=CTA_LINES):
    """The call to action each account actually carries, keyed by account."""
    with open(path, newline="", encoding="utf-8") as fh:
        return {(r["Platform"], r["AccountId"]): r for r in csv.DictReader(fh)}


# A caption reused on another channel arrives carrying the old channel's ask.
# On 09/11 that put "Comment SEASONAL" on 20 YouTube posts, where nothing
# listens for it. The body travels. The ask does not, and neither do the
# hashtags, because both are properties of where the post lands.
CTA_MARKERS = (
    "comment ", "subscribe for", "follow for", "link in bio",
    "the note is in my bio", "1 true thing about the season",
)


def body_of(text):
    """The caption with its old ask, link and hashtags taken off."""
    kept = []
    for para in (text or "").split("\n\n"):
        stripped = para.strip()
        if not stripped:
            continue
        low = stripped.lower()
        if any(m in low for m in CTA_MARKERS):
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith("http"):
            continue
        kept.append(stripped)
    return "\n\n".join(kept)


def recaption(text, platform, account, cta):
    """Put the target account's own ask on a body borrowed from elsewhere."""
    row = cta.get((platform, str(account)))
    if row is None:
        # No substitution. A channel with no recorded ask does not get one
        # invented for it, and it does not get another channel's either.
        return None
    parts = [body_of(text)]
    line, link = row["Line"], row["Link"]
    if link and line.rstrip().endswith(":"):
        parts.append(line + "\n" + link)   # the link reads as the colon's object
    elif link:
        parts.append(line)
        parts.append(link)
    else:
        parts.append(line)
    if row["Hashtags"]:
        parts.append(row["Hashtags"])
    return "\n\n".join(p for p in parts if p)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--day", required=True)
    ap.add_argument("--history", required=True)
    ap.add_argument("--queue", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    history = load_history(args.history, args.day)
    queue = json.load(open(args.queue))
    if isinstance(queue, dict):
        queue = queue.get("items", [])
    rows = plan_day(args.day, history, queue, S.load_register(),
                    load_inventory(), load_cta_lines())

    if args.json:
        print(json.dumps(rows, indent=1))
        return 0

    print("%s: %d post(s) proposed, %d day gap" % (args.day, len(rows), MIN_GAP_DAYS))
    for r in rows:
        if not r["slug"]:
            print("  %-9s HELD, %s" % (r["platform"], r["why"]))
            continue
        print("  %-9s %s  %-16s last ran %s"
              % (r["platform"], r["time"], r["slug"], r["lastRan"]))
    held = sum(1 for r in rows if not r["slug"])
    return 2 if held else 0


if __name__ == "__main__":
    sys.exit(main())
