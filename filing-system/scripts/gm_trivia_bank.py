#!/usr/bin/env python3
"""
GM-Trivia-Bank — the AI, automation and creator-economy fact bank.

Run 8 of the Gentle Muse filing system.

Run 6 gave a clip a description so a caption had something true to bind to.
Run 7 gave a holiday post a dated, sourced fact so the writing step was not
inventing history to fill a slot. Run 8 is the same job for the trivia lane,
with one failure the holiday lane does not have.

Holiday facts are settled. Nobody is going to change what year Goosebumps
started. AI and creator-economy facts move: a price, a model name, a user
count, a policy. A fact that was true in March and is repeated in September
is not a fact any more, it is a mistake in her voice.

So this bank carries 2 things the holiday bank does not.

  FoundIn vs Source   The newsletter is where a fact was FOUND. It is never
                      what makes it true. Source and SourceUrl must point at
                      the thing itself: the company's own post, the paper,
                      the filing, the documentation. A row whose Source is
                      just the newsletter again is refused, because that is
                      how a summary of a summary ends up on camera.

  Decays + VerifiedOn A fact that can go out of date has to be re-checked
                      before it is used again. Past the window it is held,
                      not published.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A plan is a proposal, not a schedule.
  No substitution. When the bank has nothing usable, it says so and stops.

Modes
  --audit             check the bank and report every row that cannot carry a post
  --available [N]     the N usable facts least recently used, the pull order
  --topics            what is in the bank, by topic and by state

Usage
  python3 gm_trivia_bank.py --audit
  python3 gm_trivia_bank.py --available 5

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import os
import sys
from collections import Counter, defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
DEFAULT_BANK = os.path.join(DATA, "trivia-fact-bank.csv")

BANK_COLUMNS = [
    "FactID", "Topic", "Fact", "Backbone", "FoundIn", "Source", "SourceUrl",
    "AsOf", "Decays", "Verified", "VerifiedOn", "Delivery", "Keyword", "LastUsed",
]

# Amanda's positioning, 09/09/2026. Generic trivia fills the same slot while
# diluting the thing she is actually selling, so the lane is scoped in data
# rather than in somebody's judgment at 1am.
TOPICS = ("ai", "automation", "creator")

# How long a moving fact stays good before it has to be checked again.
DECAY_DAYS = 90

# Words that mean a Source cell was filled in without pointing at anything.
EMPTY_SOURCE = ("", "-", "n/a", "na", "none", "tbd", "unknown", "?")

# A Source that is really just the newsletter again. The newsletter is
# provenance, never authority.
SECONDARY_MARKERS = (
    "newsletter", "digest", "roundup", "substack", "beehiiv", "mailing list",
    "daily brief", "morning brew", "the rundown", "tldr", "issue #",
)


def _read(path, required, label):
    if not os.path.exists(path):
        raise SystemExit("%s not found: %s" % (label, path))
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit("%s is missing required column(s): %s"
                             % (label, ", ".join(missing)))
        return [r for r in reader if any((v or "").strip() for v in r.values())]


def load_bank(path=DEFAULT_BANK):
    rows = _read(path, BANK_COLUMNS, "trivia-fact-bank.csv")
    return {(r["FactID"] or "").strip(): r for r in rows if (r["FactID"] or "").strip()}


def _clean(fact, key):
    return (fact.get(key) or "").strip()


def looks_secondary(value):
    low = value.lower()
    return any(m in low for m in SECONDARY_MARKERS)


def parse_date(value):
    try:
        return date(*(int(p) for p in value.split("-")))
    except (ValueError, TypeError, AttributeError):
        return None


def is_stale(fact, today=None):
    """A moving fact whose last check is older than the decay window."""
    if _clean(fact, "Decays").lower() not in ("yes", "true", "1"):
        return False
    checked = parse_date(_clean(fact, "VerifiedOn"))
    if checked is None:
        return True
    return (today or date.today()) - checked > timedelta(days=DECAY_DAYS)


def usable_problems(fact, today=None):
    """Every reason this row cannot carry a post yet. Empty list means usable."""
    problems = []

    if len(_clean(fact, "Fact")) < 20:
        problems.append("no Fact line")

    if len(_clean(fact, "Backbone")) < 15:
        problems.append("no Backbone, so it is trivia with no turn")

    topic = _clean(fact, "Topic").lower()
    if topic not in TOPICS:
        problems.append('Topic "%s" is outside the lane, which is %s'
                        % (topic or "(blank)", ", ".join(TOPICS)))

    source = _clean(fact, "Source")
    found = _clean(fact, "FoundIn")
    if source.lower() in EMPTY_SOURCE:
        problems.append("no Source")
    elif looks_secondary(source):
        problems.append('Source "%s" is a newsletter. That is where it was '
                        "found, not what makes it true. Point Source at the "
                        "thing itself." % source)
    elif found and source.strip().lower() == found.strip().lower():
        problems.append("Source is the same as FoundIn, so nothing was checked")

    if not _clean(fact, "SourceUrl").lower().startswith("http"):
        problems.append("no SourceUrl, so nobody can check it in 1 click")

    if _clean(fact, "Verified").lower() not in ("yes", "true", "1"):
        problems.append("not Verified")

    if is_stale(fact, today):
        checked = _clean(fact, "VerifiedOn") or "never"
        problems.append("Decays and was last checked %s, past the %d day window"
                        % (checked, DECAY_DAYS))

    return problems


def is_usable(fact, today=None):
    return not usable_problems(fact, today)


def audit(bank, today=None):
    usable, held = [], []
    for fid, fact in sorted(bank.items()):
        problems = usable_problems(fact, today)
        (held if problems else usable).append((fid, fact, problems))

    print("%d fact(s) in the bank" % len(bank))
    by_topic = Counter(_clean(f, "Topic").lower() for f in bank.values())
    for topic in TOPICS:
        print("  %-11s %d" % (topic, by_topic.get(topic, 0)))
    print()
    print("%d usable, %d held" % (len(usable), len(held)))

    if usable:
        print("\nusable:")
        for fid, fact, _ in usable:
            print("  %-9s %-11s %s" % (fid, _clean(fact, "Topic"),
                                       _clean(fact, "Fact")[:58]))
    if held:
        print("\nheld, and why:")
        for fid, fact, problems in held:
            print("  %-9s %s" % (fid, _clean(fact, "Fact")[:58] or "(no fact line)"))
            for p in problems:
                print("            %s" % p)
    return 1 if held else 0


def available(bank, limit, today=None):
    """Usable facts, least recently used first. That is the pull order."""
    rows = [(fid, f) for fid, f in bank.items() if is_usable(f, today)]
    rows.sort(key=lambda r: (_clean(r[1], "LastUsed") or "0000-00-00", r[0]))
    return rows[:limit] if limit else rows


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--bank", default=DEFAULT_BANK)
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--available", nargs="?", type=int, const=5, default=None)
    ap.add_argument("--topics", action="store_true")
    args = ap.parse_args()

    bank = load_bank(args.bank)

    if args.available is not None:
        rows = available(bank, args.available)
        if not rows:
            print("nothing usable in the bank. Run --audit to see what each row "
                  "is waiting on. Do not reach for the nearest fact that fits.")
            return 2
        for fid, fact in rows:
            print("%-9s %-11s last used %-11s %s"
                  % (fid, _clean(fact, "Topic"),
                     _clean(fact, "LastUsed") or "never",
                     _clean(fact, "Fact")[:52]))
        return 0

    if args.topics:
        state = defaultdict(Counter)
        for fact in bank.values():
            state[_clean(fact, "Topic").lower()]["usable" if is_usable(fact) else "held"] += 1
        for topic in TOPICS:
            c = state.get(topic, Counter())
            print("%-11s usable %-3d held %d" % (topic, c["usable"], c["held"]))
        return 0

    return audit(bank)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
