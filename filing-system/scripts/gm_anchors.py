#!/usr/bin/env python3
"""Turn the holiday calendar's rules into the dates content actually has to land on.

Every holiday in holiday-calendar.csv carries a Rule, a LeadDays and a TailDays.
Nothing was reading them, so holiday content was scheduled by hand and by memory,
which is how a fall campaign ends up starting on a date nobody chose.

  python3 gm_anchors.py --year 2026
  python3 gm_anchors.py --from 2026-09-02 --days 120

Prints, per holiday: the date itself, and the window content has to sit inside.
"""
import argparse, csv, os, sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
# Python weekday(): Monday is 0, Sunday is 6. The calendar's rules use the same.
WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def easter(year):
    """Anonymous Gregorian algorithm."""
    a = year % 19
    b, c = divmod(year, 100)
    d, e = divmod(b, 4)
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = divmod(c, 4)
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month, day = divmod(h + l - 7 * m + 114, 31)
    return date(year, month, day + 1)


def nth_weekday(year, month, weekday, n):
    d = date(year, month, 1)
    d += timedelta(days=(weekday - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def last_weekday(year, month, weekday):
    d = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, 12, 31)
    return d - timedelta(days=(d.weekday() - weekday) % 7)


def resolve(rule, year, solved):
    """Resolve one Rule string to a date. `solved` maps HolidayID -> date."""
    kind, _, rest = rule.partition(":")
    if kind == "fixed":
        m, d = rest.split("-")
        return date(year, int(m), int(d))
    if kind == "easter" or rule == "easter":
        return easter(year)
    if kind == "nth":
        month, weekday, n = (int(x) for x in rest.split(":"))
        return nth_weekday(year, month, weekday, n)
    if kind == "last":
        month, weekday = (int(x) for x in rest.split(":"))
        return last_weekday(year, month, weekday)
    if kind == "offset":
        base, days = rest.split(":")
        if base not in solved:
            return None
        return solved[base] + timedelta(days=int(days))
    raise ValueError("unknown rule: %r" % rule)


def anchors(year, calendar_path):
    rows = list(csv.DictReader(open(calendar_path, newline="", encoding="utf-8")))
    solved, out = {}, []
    # 2 passes so offset rules can see the holiday they hang off
    for _ in range(2):
        for r in rows:
            hid = r["HolidayID"]
            if hid in solved:
                continue
            d = resolve(r["Rule"].strip(), year, solved)
            if d:
                solved[hid] = d
    for r in rows:
        hid = r["HolidayID"]
        if hid not in solved:
            continue
        d = solved[hid]
        out.append({
            "id": hid, "name": r["Holiday"], "date": d,
            "opens": d - timedelta(days=int(r["LeadDays"])),
            "closes": d + timedelta(days=int(r["TailDays"])),
            "slot": r["Slot"], "register": r.get("Register", ""),
        })
    return sorted(out, key=lambda a: a["opens"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int)
    ap.add_argument("--from", dest="frm")
    ap.add_argument("--days", type=int, default=120)
    ap.add_argument("--calendar", default=os.path.join(DATA, "holiday-calendar.csv"))
    a = ap.parse_args()

    if a.frm:
        start = date.fromisoformat(a.frm)
        end = start + timedelta(days=a.days)
        rows = anchors(start.year, a.calendar) + anchors(start.year + 1, a.calendar)
        rows = [r for r in rows if r["opens"] <= end and r["closes"] >= start]
        rows.sort(key=lambda r: r["opens"])
        head = "windows open between %s and %s" % (start, end)
    else:
        year = a.year or date.today().year
        rows = anchors(year, a.calendar)
        head = "%d" % year

    print(head)
    print("%-17s %-11s %-11s %-11s %s" % ("holiday", "date", "opens", "closes", "slot"))
    for r in rows:
        print("%-17s %-11s %-11s %-11s %s"
              % (r["id"], r["date"], r["opens"], r["closes"], r["slot"]))
    print("\n%d anchors" % len(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
