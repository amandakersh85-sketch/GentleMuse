#!/usr/bin/env python3
"""Refuse a repost that wears the media it already wore.

Amanda, Sep 3: recycling a caption is the strategy, recycling its exact media
is not. The Hocus Pocus repeat went out wearing the identical picture and
caption, and the schedule held Nightmare and The Nightmare Before Christmas
twice each on Instagram carrying the same file. A repeat viewer reads the
identical image as the account running on empty.

Two findings, both scoped to a single platform:

  R01_WORN_MEDIA_REPOST  a scheduled post repeats a published caption with
                         the exact media that publish already carried
  R02_TWIN_IN_SCHEDULE   the same caption sits in the schedule more than once
                         with identical media; every instance after the first

Carousel campaign posts are exempt where magnet-campaign.csv names their
keyword as an active campaign: the frame set is the approved design and
repeats as built.

  python3 gm_repost_media_check.py --queue scheduled.json --published published.json

Exit 0 clean, 1 a repeat wears its old media, 2 nothing to check.
"""
import argparse, collections, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def norm(text):
    return re.sub(r"[^a-z]", "", (text or "").lower())[:60]


def key(row):
    return (row.get("platform") or "?", norm(row.get("text")))


def media(row):
    m = row.get("mediaUrls")
    if m is None:
        m = row.get("media")
    if isinstance(m, str):
        m = [x for x in m.split("|") if x.strip()]
    return tuple(sorted(str(x) for x in (m or [])))


def when(row):
    return row.get("at") or row.get("postTime") or row.get("scheduledAt") or ""


def load_rows(path):
    if not path:
        return []
    rows = json.load(open(path, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("items") or rows.get("posts") or []
    return rows


def load_campaigns(path):
    """Active campaign keywords; their carousels repeat exactly as designed."""
    if not path or not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [r["Keyword"] for r in csv.DictReader(fh)
                if (r.get("Status") or "").strip() == "active"]


def check(rows, published, campaign_keywords):
    campaign_re = (re.compile(r"\b(" + "|".join(map(re.escape, campaign_keywords)) + r")\b")
                   if campaign_keywords else None)
    worn = collections.defaultdict(set)
    for p in published:
        k = key(p)
        if k[1] and media(p):
            worn[k].add(media(p))

    findings, seen = [], {}
    for r in sorted(rows, key=when):
        k, m = key(r), media(r)
        if not k[1] or not m:
            continue
        if campaign_re and campaign_re.search(r.get("text") or ""):
            continue
        if m in worn.get(k, ()):
            findings.append({
                "code": "R01_WORN_MEDIA_REPOST", "id": r.get("id", "?"),
                "platform": k[0], "at": when(r),
                "msg": "repeats a published caption wearing the exact media it already wore",
            })
        prior = seen.get((k, m))
        if prior is not None:
            findings.append({
                "code": "R02_TWIN_IN_SCHEDULE", "id": r.get("id", "?"),
                "platform": k[0], "at": when(r),
                "msg": "same caption and identical media already scheduled as %s" % prior,
            })
        else:
            seen[(k, m)] = r.get("id", "?")
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True, help="scheduled posts, JSON export")
    ap.add_argument("--published", help="published posts, JSON export")
    ap.add_argument("--campaigns", default=os.path.join(DATA, "magnet-campaign.csv"))
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rows = load_rows(a.queue)
    if not rows:
        print("nothing in the queue file to compare")
        return 2
    findings = check(rows, load_rows(a.published), load_campaigns(a.campaigns))

    if not a.quiet:
        for f in findings:
            print("%-22s %-10s %-10s %-17s %s"
                  % (f["code"], f["id"], f["platform"], f["at"][:16], f["msg"]))
        print("\n%d scheduled checked, %d repeat(s) wearing media already worn"
              % (len(rows), len(findings)))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
