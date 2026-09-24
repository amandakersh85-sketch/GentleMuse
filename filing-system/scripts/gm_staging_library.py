#!/usr/bin/env python3
"""
gm_staging_library.py - build the refill reservoir.

The SOP points the refill loop at CAL_0818_staging-library-v3.xlsx, 658
rows, 4 waves of 200. That file is not in Drive. It was flagged missing on
2026-08-26 and it was still missing on 2026-09-08, which is why the queue
has been hand fed 6 posts a night and sits at 1.8 Instagram posts a day
against a target of 3 to 5 per platform per day.

This rebuilds the reservoir from what the repo actually knows: the fact
bank, the rendered payloads, the hosted media map and the written caption
sets. Every row says exactly what it is waiting on, so nothing is invented
to fill a slot.

  STAGED         rendered, hosted and captioned. Loadable right now.
  NEEDS_CAPTION  rendered and hosted, no caption written yet.
  NEEDS_RENDER   a sourced fact with no reel behind it.

Slots come from the SOP and Amanda's Metricool hours, 2 hours apart, none
in the dead window:

  instagram / tiktok  15:00 17:00 19:00 21:00 23:00 UTC  (10am to 6pm Central)
  facebook            17:10 UTC   youtube  17:20 UTC

Usage:
  gm_staging_library.py --out filing-system/data/staging-library.csv
  gm_staging_library.py --report
"""
import csv
import glob
import json
import os
import sys
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "filing-system", "data")

CLUB_SLOTS = ["15:00", "17:00", "19:00", "21:00", "23:00"]
ACCOUNTS = {"instagram": "45886", "tiktok": "41488",
            "facebook": "30840", "youtube": "36129"}
ECHO_SLOT = {"facebook": "17:10", "youtube": "17:20"}


def read(name):
    with open(os.path.join(D, name), newline="") as fh:
        return list(csv.DictReader(fh))


def build():
    media = {r["Slug"]: r["HostedUrl"] for r in read("blitz-media-map.csv")}
    caps = {r["FactID"]: r for r in read("halloween-track-b-captions.csv")}
    facts = {r["FactID"]: r for r in read("holiday-fact-bank.csv")}

    payloads = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "reel-factory", "reels-final-*.json"))):
        try:
            reel = json.load(open(f))[0]
        except Exception:
            continue
        slug = reel.get("slug") or os.path.splitext(os.path.basename(f))[0]
        payloads[slug] = reel.get("id", "")

    rows = []
    for slug in sorted(payloads):
        fid = payloads[slug]
        url = media.get(slug, "")
        cap = caps.get(fid)
        if url and cap:
            status = "STAGED"
        elif url:
            status = "NEEDS_CAPTION"
        else:
            status = "NEEDS_RENDER"
        for plat in ("instagram", "tiktok", "facebook", "youtube"):
            text = ""
            if cap:
                text = cap.get({"instagram": "IG", "tiktok": "TT"}.get(plat, "FB"), "")
            rows.append({
                "Slug": slug, "FactID": fid, "Platform": plat,
                "AccountId": ACCOUNTS[plat],
                "SlotUTC": ECHO_SLOT.get(plat, ""),
                "Status": status, "MediaUrl": url,
                "Text": text.replace("\n", "\\n"),
                "Waiting": {"STAGED": "", "NEEDS_CAPTION": "a caption in her voice",
                            "NEEDS_RENDER": "hosting"}[status],
            })

    # sourced facts with no reel behind them at all
    have_fids = set(payloads.values())
    for fid, f in sorted(facts.items()):
        if fid in have_fids or not f.get("Fact"):
            continue
        rows.append({
            "Slug": "", "FactID": fid, "Platform": "", "AccountId": "",
            "SlotUTC": "", "Status": "NEEDS_RENDER", "MediaUrl": "", "Text": "",
            "Waiting": "a plate and a render",
        })
    return rows


def main(argv):
    rows = build()
    counts = {}
    for r in rows:
        counts[r["Status"]] = counts.get(r["Status"], 0) + 1

    loadable = counts.get("STAGED", 0)
    print("staging library: %d rows" % len(rows))
    for k in ("STAGED", "NEEDS_CAPTION", "NEEDS_RENDER"):
        print("  %-14s %d" % (k, counts.get(k, 0)))
    print()
    print("loadable now: %d rows" % loadable)
    print("at 4 posts per platform per day that is %.1f days of queue" % (loadable / 16.0))

    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
        fields = ["Slug", "FactID", "Platform", "AccountId", "SlotUTC",
                  "Status", "MediaUrl", "Text", "Waiting"]
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv))
    except BrokenPipeError:
        sys.exit(0)
