#!/usr/bin/env python3
"""Refuse a post whose media count is lower than a better version of the same
caption has ever carried.

The swipe-check in gm_cta_check.py only catches a caption that literally says
"swipe." A live post read "Your towels aren't old. They're coated." with 1
image the same week a 6-image version of the identical caption was archived
in queue-backlog.csv. No keyword would have caught that. What catches it is
comparing media counts across every place that caption has ever appeared and
refusing a regression, regardless of what the words say.

  python3 gm_carousel_check.py --queue live.json
  python3 gm_carousel_check.py --queue live.json --archive other.csv

Exit 0 no regression, 1 a regression was found, 2 nothing to check.
"""
import argparse, csv, json, os, re, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")


def norm(text):
    return re.sub(r"[^a-z]", "", (text or "").lower())[:60]


def key(row):
    """Compare within a platform only. LinkedIn and Instagram legitimately
    carry different image counts for the same caption; only a regression
    within the same platform is a real bug."""
    return (row.get("platform") or "?", norm(row.get("text")))


def media_count(row):
    m = row.get("media")
    if m is None:
        m = row.get("mediaUrls")
    if isinstance(m, str):
        return len([x for x in m.split("|") if x.strip()])
    return len(m or [])


def load_queue(path):
    rows = json.load(open(path, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("items") or rows.get("posts") or []
    return rows


def load_archive(path):
    if not path or not os.path.exists(path):
        return []
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out.append({"id": r.get("BlotatoID"), "text": r.get("Text"),
                        "media": r.get("MediaUrls"), "platform": r.get("Platform")})
    return out


def best_counts(rows):
    """(platform, normalized caption) -> (best media count seen, its id)"""
    best = {}
    for r in rows:
        k = key(r)
        if not k[1]:
            continue
        n = media_count(r)
        if n > best.get(k, (0, None))[0]:
            best[k] = (n, r.get("id"))
    return best


def check(rows, archive_rows):
    best = best_counts(list(rows) + list(archive_rows))
    findings = []
    for r in rows:
        k = key(r)
        if not k[1]:
            continue
        want, source_id = best.get(k, (0, None))
        have = media_count(r)
        if want > have and source_id != r.get("id"):
            findings.append({
                "code": "C01_MEDIA_REGRESSION", "id": r.get("id", "?"),
                "platform": r.get("platform", "?"), "at": r.get("at", ""),
                "msg": "carries %d image(s), but %s carried %d for the same caption"
                       % (have, source_id or "an earlier version", want),
            })
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--archive", default=os.path.join(DATA, "queue-backlog.csv"))
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rows = load_queue(a.queue)
    if not rows:
        print("nothing in the queue file to compare")
        return 2
    archive_rows = load_archive(a.archive)
    findings = check(rows, archive_rows)

    if not a.quiet:
        for f in findings:
            print("%-22s %-10s %-9s %s" % (f["code"], f["id"], f["platform"], f["msg"]))
        print("\n%d posts checked against %d archived, %d regression(s) found"
              % (len(rows), len(archive_rows), len(findings)))

    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
