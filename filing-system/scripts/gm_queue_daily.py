#!/usr/bin/env python3
"""The daily queue pass. One command, one screen, no thinking required.

Reads the live queue export and answers, in order:
  1. how much room is left against the plan cap
  2. which holiday windows open soon and whether anything is scheduled in them
  3. what the 3 slot model is short of, in the MODEL zone only
  4. which posts carry a call to action that cannot work
  5. whether the running sprint is actually present in the SPRINT zone

  python3 gm_queue_daily.py --queue live.json --today 2026-09-02

Exit 0 nothing to do, 1 there is work, 2 the queue file is unreadable.
"""
import argparse, csv, json, os, subprocess, sys, collections
from datetime import date, datetime, timedelta, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
CT = timezone(timedelta(hours=-5))
CAP = 200
NAMES = {"45886": "IG gm", "65540": "IG cesa", "41488": "TT gm",
         "55761": "TT cesa", "30840": "FB"}


def rows_from(path):
    r = json.load(open(path, encoding="utf-8"))
    return r.get("items") or r.get("posts") or [] if isinstance(r, dict) else r


def local(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(CT).date()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--today", default=str(date.today()))
    a = ap.parse_args()

    try:
        rows = rows_from(a.queue)
    except Exception as e:
        print("cannot read the queue file: %s" % e)
        return 2
    today = date.fromisoformat(a.today)

    zones = list(csv.DictReader(open(os.path.join(DATA, "queue-zones.csv"), encoding="utf-8")))
    sprints = list(csv.DictReader(open(os.path.join(DATA, "campaign-sprints.csv"), encoding="utf-8")))
    work = 0

    # 1 cap
    n = len(rows)
    print("QUEUE  %d of %d scheduled, %d slots free" % (n, CAP, CAP - n))
    if CAP - n < 20:
        print("       under 20 free. Clear the far end before scheduling more.")
        work += 1

    # 2 anchors
    print("\nANCHORS opening in the next 45 days")
    out = subprocess.run([sys.executable, os.path.join(HERE, "gm_anchors.py"),
                          "--from", str(today), "--days", "45"],
                         capture_output=True, text=True).stdout.splitlines()
    have = collections.Counter(local(r["at"]) for r in rows)
    for line in out[2:]:
        p = line.split()
        if len(p) < 4 or not p[1][:4].isdigit():
            continue
        hid, when, opens, closes = p[0], p[1], p[2], p[3]
        o, c = date.fromisoformat(opens), date.fromisoformat(closes)
        inside = sum(v for k, v in have.items() if o <= k <= c)
        flag = "" if inside else "   <- nothing scheduled in this window"
        print("  %-17s %s  window %s to %s, %d posts inside%s"
              % (hid, when, opens, closes, inside, flag))
        if not inside and o <= today + timedelta(days=45):
            work += 1

    # 3 model shortfall, MODEL zone only
    lo, hi = today + timedelta(days=8), today + timedelta(days=14)
    want = {"45886": 3, "41488": 2, "30840": 2}
    print("\nMODEL zone, %s to %s" % (lo, hi))
    short = 0
    d = lo
    while d <= hi:
        got = collections.Counter(r.get("accountId") for r in rows if local(r["at"]) == d)
        gaps = ["%s +%d" % (NAMES.get(k, k), v - got[k]) for k, v in want.items() if got[k] < v]
        print("  %s %s  %s" % (d, d.strftime("%a"), " ".join(gaps) if gaps else "on model"))
        short += sum(v - got[k] for k, v in want.items() if got[k] < v)
        d += timedelta(days=1)
    if short:
        print("  refill %d posts from the draft bank" % short)
        work += 1

    # 4 calls to action
    gate = subprocess.run([sys.executable, os.path.join(HERE, "gm_cta_check.py"),
                           "--queue", a.queue], capture_output=True, text=True)
    bad = [l for l in gate.stdout.splitlines() if l.startswith("P0")]
    print("\nCALLS TO ACTION  %d that cannot work" % len(bad))
    for l in bad[:6]:
        print("  " + l)
    if len(bad) > 6:
        print("  and %d more, run gm_cta_check.py" % (len(bad) - 6))
    if bad:
        work += 1

    # 5 sprint presence
    print("\nSPRINT")
    live = [s for s in sprints
            if date.fromisoformat(s["Start"]) <= today <= date.fromisoformat(s["End"])]
    if not live:
        print("  none running today")
    for s in live:
        front = sum(1 for r in rows if today <= local(r["at"]) <= today + timedelta(days=7))
        print("  %s  %s to %s, owns the %s slot, magnet %s"
              % (s["Name"], s["Start"], s["End"], s["OwnsSlot"], s["Magnet"]))
        print("  %d posts in the next 7 days" % front)

    print("\n%s" % ("nothing to do" if not work else "%d things need a hand" % work))
    return 0 if not work else 1


if __name__ == "__main__":
    sys.exit(main())
