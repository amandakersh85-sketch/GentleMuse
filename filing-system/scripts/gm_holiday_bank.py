#!/usr/bin/env python3
"""
GM-Holiday-Bank — the holiday calendar, the fact bank, and the plan they produce.

Run 7 of the Gentle Muse filing system. Run 6 gave a clip a description so a
caption had something true to bind to. Run 7 does the same job one layer up:
it gives a holiday post a dated, sourced fact to be about, so the writing step
is not inventing history to fill a slot.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A plan is a proposal, not a schedule.
  No substitution. When the bank has nothing for a day, it says so and stops.

Modes
  --audit                 check the calendar and the bank, report what is unusable
  --plan --from --to      the content plan for a date range, one row per post
  --season [DATE]         what is in season on a date, and what is left in the bank

Usage
  python3 gm_holiday_bank.py --audit
  python3 gm_holiday_bank.py --plan --from 2026-10-01 --to 2026-11-01
  python3 gm_holiday_bank.py --plan --from 2026-10-01 --to 2026-11-01 --out plan.csv

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
DEFAULT_CALENDAR = os.path.join(DATA, "holiday-calendar.csv")
DEFAULT_BANK = os.path.join(DATA, "holiday-fact-bank.csv")

# Amanda was born in 1985 and watched from roughly 4 to 14. A nostalgia
# reference outside this window is somebody else's childhood.
ERA_START = 1989
ERA_END = 1999

CALENDAR_COLUMNS = ["HolidayID", "Holiday", "Rule", "LeadDays", "TailDays", "Slot", "Register"]
BANK_COLUMNS = ["FactID", "HolidayID", "Kind", "Fact", "Year", "EraYear",
                "Source", "Backbone", "Verified", "LastUsed"]

KINDS = {"history", "spooky", "origin", "nostalgia", "myth-bust"}

# A fact needs a real source. These are the ways a row says "trust me."
EMPTY_SOURCE = {"", "-", "n/a", "na", "none", "unknown", "common knowledge", "tbd"}


# ---------------------------------------------------------------- date rules

def easter(year):
    """Anonymous Gregorian computus. Returns the date of Easter Sunday."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    el = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * el) // 451
    month, day = divmod(h + el - 7 * m + 114, 31)
    return date(year, month, day + 1)


def resolve(rule, year, calendar=None, _seen=None):
    """Turn a Rule string into a real date in a given year.

    fixed:MM-DD          a fixed calendar date
    nth:MM:WD:N          the Nth weekday of a month. WD is Monday 0 to Sunday 6
    last:MM:WD           the last weekday of a month
    easter               Easter Sunday
    offset:HOLIDAY:N     N days from another holiday in the same calendar
    """
    rule = (rule or "").strip()
    kind, _, rest = rule.partition(":")

    if kind == "fixed":
        month, day = rest.split("-")
        return date(year, int(month), int(day))

    if kind == "nth":
        month, weekday, n = (int(x) for x in rest.split(":"))
        first = date(year, month, 1)
        return first + timedelta(days=(weekday - first.weekday()) % 7 + 7 * (n - 1))

    if kind == "last":
        month, weekday = (int(x) for x in rest.split(":"))
        following = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
        final = following - timedelta(days=1)
        return final - timedelta(days=(final.weekday() - weekday) % 7)

    if kind == "easter":
        return easter(year)

    if kind == "offset":
        other, _, days = rest.rpartition(":")
        seen = _seen or set()
        if other in seen:
            raise ValueError("offset rules loop through %s" % other)
        if not calendar or other not in calendar:
            raise ValueError('offset rule points at unknown holiday "%s"' % other)
        anchor = resolve(calendar[other]["Rule"], year, calendar, seen | {other})
        return anchor + timedelta(days=int(days))

    raise ValueError('unrecognised Rule "%s"' % rule)


def window(row, year, calendar):
    """The date the holiday lands, and the span its content is in season."""
    landed = resolve(row["Rule"], year, calendar)
    lead = int(row.get("LeadDays") or 0)
    tail = int(row.get("TailDays") or 0)
    return landed, landed - timedelta(days=lead), landed + timedelta(days=tail)


def in_season(row, when, calendar):
    """Is `when` inside this holiday's season? Checks the neighbouring years
    too, so a December lead-in still resolves in early January."""
    for year in (when.year - 1, when.year, when.year + 1):
        try:
            landed, opens, closes = window(row, year, calendar)
        except (ValueError, TypeError):
            continue
        if opens <= when <= closes:
            return landed
    return None


# ---------------------------------------------------------------- loading

def _read(path, required, label):
    if not os.path.exists(path):
        raise SystemExit("%s not found: %s" % (label, path))
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in required if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit("%s is missing required column(s): %s"
                             % (label, ", ".join(missing)))
        return [row for row in reader if any((v or "").strip() for v in row.values())]


def load_calendar(path):
    rows = _read(path, CALENDAR_COLUMNS, "holiday-calendar.csv")
    return {(r["HolidayID"] or "").strip(): r for r in rows if (r["HolidayID"] or "").strip()}


def load_bank(path):
    rows = _read(path, BANK_COLUMNS, "holiday-fact-bank.csv")
    return {(r["FactID"] or "").strip(): r for r in rows if (r["FactID"] or "").strip()}


def is_usable(fact):
    """A fact that can carry a post. Anything less is not available."""
    return not usable_problems(fact)


def usable_problems(fact):
    """Every reason this row cannot carry a post yet. Empty list means usable."""
    problems = []
    if len((fact.get("Fact") or "").strip()) < 20:
        problems.append("no Fact line")
    if (fact.get("Source") or "").strip().lower() in EMPTY_SOURCE:
        problems.append("no Source")
    if len((fact.get("Backbone") or "").strip()) < 15:
        problems.append("no Backbone, so it is trivia with no turn")
    if (fact.get("Verified") or "").strip().lower() not in ("yes", "true", "1"):
        problems.append("not Verified")
    return problems


def parse_years(value):
    """Year holds one year, or several for a fact that spans a period."""
    out = []
    for part in re.split(r"[,;/]", value or ""):
        part = part.strip()
        if part.isdigit():
            out.append(int(part))
    return out


def parse_year(value):
    """The first year on the row, for messages that need to name just one."""
    years = parse_years(value)
    return years[0] if years else None


def parse_date(value, label):
    try:
        return date(*(int(p) for p in value.split("-")))
    except (ValueError, TypeError):
        raise SystemExit('%s must look like YYYY-MM-DD, got "%s"' % (label, value))


# ---------------------------------------------------------------- audit

def audit(calendar, bank, era):
    problems, notes = [], []

    if not calendar:
        problems.append("the calendar is empty.")
    if not bank:
        problems.append("the fact bank is empty.")

    year = date.today().year
    for holiday_id, row in sorted(calendar.items()):
        try:
            landed, opens, closes = window(row, year, calendar)
            notes.append("  %-18s %s   in season %s to %s"
                         % (holiday_id, landed, opens, closes))
        except (ValueError, TypeError) as error:
            problems.append('%s has a Rule that will not resolve: %s' % (holiday_id, error))

    by_holiday = defaultdict(list)
    for fact in bank.values():
        by_holiday[(fact.get("HolidayID") or "").strip()].append(fact)

    for holiday_id in sorted(by_holiday):
        if holiday_id not in calendar:
            problems.append('fact bank references holiday "%s", which is not in the calendar.'
                            % holiday_id)

    seen_text = {}
    unusable = []
    for fact_id in sorted(bank):
        fact = bank[fact_id]
        kind = (fact.get("Kind") or "").strip()
        if kind not in KINDS:
            problems.append('%s has Kind "%s". Use one of: %s'
                            % (fact_id, kind, ", ".join(sorted(KINDS))))

        reasons = usable_problems(fact)
        if reasons:
            unusable.append((fact_id, reasons))
            problems.append("%s cannot carry a post: %s. A row goes in the bank when it "
                            "has a source, not before." % (fact_id, "; ".join(reasons)))

        era_year = parse_year(fact.get("EraYear"))
        if kind == "nostalgia" and era_year is None:
            problems.append("%s is a nostalgia row with no EraYear. Without the year "
                            "there is nothing to check the era window against." % fact_id)
        if era_year is not None and not (era[0] <= era_year <= era[1]):
            problems.append("%s references %d, outside the %d to %d window. That is "
                            "somebody else's childhood." % (fact_id, era_year, era[0], era[1]))

        key = " ".join((fact.get("Fact") or "").lower().split())[:90]
        if key and key in seen_text:
            problems.append("%s repeats %s almost word for word." % (fact_id, seen_text[key]))
        elif key:
            seen_text[key] = fact_id

    print("GM-Holiday-Bank audit")
    print("  calendar : %d holidays" % len(calendar))
    print("  bank     : %d facts, %d usable, %d nostalgia rows"
          % (len(bank),
             sum(1 for f in bank.values() if is_usable(f)),
             sum(1 for f in bank.values() if (f.get("Kind") or "").strip() == "nostalgia")))
    print("  era      : %d to %d" % era)
    print("")

    print("Coverage")
    for holiday_id in sorted(calendar):
        usable = [f for f in by_holiday.get(holiday_id, []) if is_usable(f)]
        total = len(by_holiday.get(holiday_id, []))
        flag = "  " if usable else "!!"
        print("%s %-18s %2d usable of %2d" % (flag, holiday_id, len(usable), total))
        if not usable:
            problems.append('"%s" has no usable fact. Every post for it will HOLD until '
                            "one is written. Do that before the season opens." % holiday_id)
    print("")

    if notes:
        print("Dates this year")
        for line in notes:
            print(line)
        print("")

    if unusable:
        print("Not yet usable (%d)" % len(unusable))
        for fact_id, reasons in unusable:
            print("  %-10s %s" % (fact_id, "; ".join(reasons)))
        print("")

    if problems:
        print("FINDINGS (%d)" % len(problems))
        for problem in problems:
            print("  %s" % problem)
        print("")
        print("VERDICT: FAIL. Fix the findings before planning against this bank.")
        return 1

    print("VERDICT: PASS. Calendar resolves, every fact carries a source and a backbone.")
    return 0


# ---------------------------------------------------------------- plan

def plan(calendar, bank, start, end, era, per_holiday):
    if end < start:
        raise SystemExit("--to is before --from.")

    by_holiday = defaultdict(list)
    for fact in bank.values():
        if is_usable(fact):
            by_holiday[(fact.get("HolidayID") or "").strip()].append(fact)

    def sort_key(fact):
        return ((fact.get("LastUsed") or "").strip() or "0000-00-00", fact["FactID"])

    seasons = []
    for holiday_id, row in calendar.items():
        landed = in_season(row, start, calendar) or in_season(row, end, calendar)
        if landed is None:
            probe = start
            while probe <= end and landed is None:
                landed = in_season(row, probe, calendar)
                probe += timedelta(days=1)
        if landed is not None:
            seasons.append((landed, holiday_id, row))
    seasons.sort()

    rows, holds = [], []
    for landed, holiday_id, row in seasons:
        pool = sorted(by_holiday.get(holiday_id, []), key=sort_key)
        opens = max(start, landed - timedelta(days=int(row.get("LeadDays") or 0)))
        closes = min(end, landed + timedelta(days=int(row.get("TailDays") or 0)))
        span = (closes - opens).days + 1
        wanted = min(per_holiday, max(1, span))

        if not pool:
            holds.append((holiday_id, row["Holiday"], landed,
                          "no usable fact in the bank"))
            continue

        for index in range(wanted):
            if index >= len(pool):
                holds.append((holiday_id, row["Holiday"], landed,
                              "bank has %d usable fact%s, plan asked for %d"
                              % (len(pool), "" if len(pool) == 1 else "s", wanted)))
                break
            fact = pool[index]
            offset = 0 if wanted == 1 else round(index * (span - 1) / (wanted - 1))
            rows.append({
                "PostDate": (opens + timedelta(days=offset)).isoformat(),
                "HolidayID": holiday_id,
                "Holiday": row["Holiday"],
                "HolidayDate": landed.isoformat(),
                "Slot": row.get("Slot", ""),
                "Register": row.get("Register", ""),
                "FactID": fact["FactID"],
                "Kind": fact.get("Kind", ""),
                "Fact": fact.get("Fact", ""),
                "Backbone": fact.get("Backbone", ""),
                "Source": fact.get("Source", ""),
                "EraYear": fact.get("EraYear", ""),
            })

    rows.sort(key=lambda r: (r["PostDate"], r["FactID"]))
    return rows, holds


def print_plan(rows, holds, start, end, era):
    print("GM-Holiday-Bank plan")
    print("  range : %s to %s" % (start, end))
    print("  era   : %d to %d" % era)
    print("  posts : %d" % len(rows))
    print("")
    if rows:
        for row in rows:
            print("%s  %-16s %-20s %-10s %s"
                  % (row["PostDate"], row["HolidayID"], row["Slot"],
                     row["Kind"], row["FactID"]))
            print("    fact     : %s" % row["Fact"])
            print("    backbone : %s" % row["Backbone"])
            print("    source   : %s" % row["Source"])
            print("")
    if holds:
        print("HOLD (%d)" % len(holds))
        for holiday_id, name, landed, why in holds:
            print("  %-18s %s  %s" % (holiday_id, landed, why))
        print("  Write the missing facts. Do not reach for a fact from another holiday.")
        print("")


def print_season(calendar, bank, when, era):
    print("GM-Holiday-Bank season")
    print("  date : %s" % when)
    print("")
    live = []
    for holiday_id, row in calendar.items():
        landed = in_season(row, when, calendar)
        if landed is not None:
            live.append((landed, holiday_id, row))
    live.sort()
    if not live:
        upcoming = []
        for holiday_id, row in calendar.items():
            for year in (when.year, when.year + 1):
                try:
                    landed = resolve(row["Rule"], year, calendar)
                except (ValueError, TypeError):
                    continue
                if landed >= when:
                    upcoming.append((landed, holiday_id, row))
                    break
        upcoming.sort()
        print("  Nothing in season. Next up:")
        for landed, holiday_id, row in upcoming[:3]:
            opens = landed - timedelta(days=int(row.get("LeadDays") or 0))
            print("    %-18s lands %s, season opens %s (%d days)"
                  % (holiday_id, landed, opens, (opens - when).days))
        return 0

    for landed, holiday_id, row in live:
        pool = [f for f in bank.values()
                if (f.get("HolidayID") or "").strip() == holiday_id and is_usable(f)]
        fresh = [f for f in pool if not (f.get("LastUsed") or "").strip()]
        print("  %-18s lands %s   slot %s   register %s"
              % (holiday_id, landed, row.get("Slot", ""), row.get("Register", "")))
        print("    %d usable fact%s, %d never used"
              % (len(pool), "" if len(pool) == 1 else "s", len(fresh)))
        if not pool:
            print("    HOLD. Nothing to post from. Write a fact before writing a caption.")
    return 0


# ---------------------------------------------------------------- cli

def main():
    parser = argparse.ArgumentParser(
        description="Resolve the holiday calendar, audit the fact bank, and plan from them.")
    parser.add_argument("--calendar", default=DEFAULT_CALENDAR)
    parser.add_argument("--bank", default=DEFAULT_BANK)
    parser.add_argument("--audit", action="store_true", help="check the calendar and the bank")
    parser.add_argument("--plan", action="store_true", help="build a plan for a date range")
    parser.add_argument("--season", nargs="?", const="today", metavar="DATE",
                        help="what is in season on a date, default today")
    parser.add_argument("--from", dest="start", help="plan start, YYYY-MM-DD")
    parser.add_argument("--to", dest="end", help="plan end, YYYY-MM-DD")
    parser.add_argument("--per-holiday", type=int, default=3,
                        help="posts to plan per holiday in range, default 3")
    parser.add_argument("--era", default="%d-%d" % (ERA_START, ERA_END),
                        help="nostalgia window, default %d-%d" % (ERA_START, ERA_END))
    parser.add_argument("--out", help="optional CSV of the plan")
    args = parser.parse_args()

    try:
        era = tuple(int(p) for p in args.era.split("-"))
        if len(era) != 2 or era[0] > era[1]:
            raise ValueError
    except ValueError:
        raise SystemExit('--era must look like 1989-1999, got "%s"' % args.era)

    calendar = load_calendar(args.calendar)
    bank = load_bank(args.bank)

    if args.audit:
        return audit(calendar, bank, era)

    if args.season is not None:
        when = date.today() if args.season == "today" else parse_date(args.season, "--season")
        return print_season(calendar, bank, when, era)

    if args.plan:
        if not args.start or not args.end:
            raise SystemExit("--plan needs --from and --to.")
        start = parse_date(args.start, "--from")
        end = parse_date(args.end, "--to")
        rows, holds = plan(calendar, bank, start, end, era, args.per_holiday)
        print_plan(rows, holds, start, end, era)
        if args.out:
            with open(args.out, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()) if rows else
                                        ["PostDate", "HolidayID", "FactID"])
                writer.writeheader()
                writer.writerows(rows)
            print("plan written: %s" % args.out)
        if holds and not rows:
            print("VERDICT: HOLD. Nothing plannable in this range.")
            return 2
        if holds:
            print("VERDICT: HOLD. %d post%s planned, %d gap%s a fact written."
                  % (len(rows), "" if len(rows) == 1 else "s",
                     len(holds), " needs" if len(holds) == 1 else "s need"))
            return 2
        print("VERDICT: PASS. %d post%s planned, every one bound to a sourced fact."
              % (len(rows), "" if len(rows) == 1 else "s"))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
