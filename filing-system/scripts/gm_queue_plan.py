#!/usr/bin/env python3
"""Compare the live queue against the slot model over a rolling window.

The queue kept drifting 2 ways at once: overfull in the first week, empty in
the second, and scheduled 3 months out so the plan cap blocked new work. The
missing data was a written model of what a day is supposed to contain. That is
slot-model.csv. This reads it and reports the difference.

  python3 gm_queue_plan.py --queue fresh.json --start 2026-09-02 --days 14
  python3 gm_queue_plan.py --queue fresh.json --start 2026-09-02 --days 14 --json

Exit 0 the window matches the model, 1 it does not, 2 nothing to compare.
"""
import argparse, csv, json, os, sys, collections
from datetime import datetime, timedelta, timezone, date

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CT = timezone(timedelta(hours=-5))          # America/Chicago, CDT
WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
NAMES = {"45886": "IG gm", "65540": "IG cesa", "41488": "TT gm", "55761": "TT cesa",
         "30840": "FB", "36129": "YT", "20723": "LI", "21430": "X", "6328": "PIN"}


def load_model(path):
    slots = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            r["_accounts"] = [a.strip() for a in (r.get("AccountIds") or "").split("|") if a.strip()]
            r["_per_day"] = int(r.get("PerDay") or 1)
            slots.append(r)
    return slots


def load_rotation(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return {r["Weekday"]: r for r in csv.DictReader(fh)}


def wanted_per_day(slots):
    """account id -> how many posts a day the model asks for."""
    want = collections.Counter()
    for s in slots:
        for a in s["_accounts"]:
            want[a] += s["_per_day"]
    return want


def local_date(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(CT)


def plan(rows, slots, start, days):
    want = wanted_per_day(slots)
    window = [start + timedelta(days=n) for n in range(days)]
    last = window[-1]

    have = collections.defaultdict(collections.Counter)
    beyond, offmodel = [], []
    for r in rows:
        d = local_date(r["at"])
        aid = str(r.get("accountId") or "")
        if d.date() > last:
            beyond.append(r)
        elif d.date() >= start:
            have[d.date()][aid] += 1
            if aid not in want:
                offmodel.append(r)

    over, under = [], []
    for day in window:
        for aid, n in want.items():
            got = have[day][aid]
            if got > n:
                over.append((day, aid, got, n))
            elif got < n:
                under.append((day, aid, got, n))
    return {"window": window, "have": have, "want": want, "over": over,
            "under": under, "beyond": beyond, "offmodel": offmodel}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--start", required=True, help="YYYY-MM-DD, local")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--model", default=os.path.join(DATA, "slot-model.csv"))
    ap.add_argument("--rotation", default=os.path.join(DATA, "rotation-magnet.csv"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = json.load(open(a.queue, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("items") or rows.get("posts") or []
    if not rows:
        print("nothing in the queue file to compare")
        return 2

    slots = load_model(a.model)
    rot = load_rotation(a.rotation)
    start = date.fromisoformat(a.start)
    p = plan(rows, slots, start, a.days)

    if a.json:
        print(json.dumps({
            "over": [[str(d), aid, g, w] for d, aid, g, w in p["over"]],
            "under": [[str(d), aid, g, w] for d, aid, g, w in p["under"]],
            "beyond": [r["id"] for r in p["beyond"]],
            "offmodel": [r["id"] for r in p["offmodel"]],
        }, indent=1))
    else:
        cols = sorted(p["want"])
        print("day".ljust(16) + "  ".join(NAMES.get(c, c).ljust(8) for c in cols) + "  rotation")
        for day in p["window"]:
            wd = WEEKDAY[day.weekday()]
            cells = []
            for c in cols:
                got, w = p["have"][day][c], p["want"][c]
                cells.append(("%d/%d" % (got, w) + ("!" if got != w else " ")).ljust(8))
            kw = (rot.get(wd) or {}).get("Keyword", "?")
            print(("%s %s" % (day, wd[:3])).ljust(16) + "  ".join(cells) + "  " + kw)
        print("\n%d slots over, %d slots under, %d posts beyond the %d day window, "
              "%d on channels the model does not run daily"
              % (len(p["over"]), len(p["under"]), len(p["beyond"]), a.days, len(p["offmodel"])))

    return 0 if not (p["over"] or p["under"] or p["beyond"]) else 1


if __name__ == "__main__":
    sys.exit(main())
