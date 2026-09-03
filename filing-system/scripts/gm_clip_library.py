#!/usr/bin/env python3
"""
GM-Clip-Library — build and audit the clip library the binding gate reads.

Companion to gm_bind_check.py. Turns the KEEP rows of a Run 3 video-triage.csv
into clip-library.csv, the one file that records what is actually visible in
each clip. Without a Shot description a clip cannot be bound to a caption,
because there is nothing to verify the caption against.

Re-running is safe. --merge keeps every description already written, matched on
SHA-256 first and file path second, so a re-triage never wipes the descriptions.

House rules, same as every other module:
  Propose-only. This script reads footage metadata and writes one CSV.
  It never moves, renames, re-encodes or deletes a video.

Usage
  Build the skeleton from a triage run:
    python3 gm_clip_library.py --from-triage out/video-triage.csv --out clip-library.csv

  Rebuild after new footage, keeping existing descriptions:
    python3 gm_clip_library.py --from-triage out/video-triage.csv --out clip-library.csv --merge

  See what still needs describing:
    python3 gm_clip_library.py --audit clip-library.csv

  Fix dates on a Drive pull before auditing it (a phone names files with the
  date it captured them; Drive's own createdTime is only when it got uploaded,
  which can lag the recording by weeks and bury how far back the backlog goes):
    python3 gm_clip_library.py --derive-dates clip-library-drive.csv

Exit codes
  0  done, or audit clean
  1  audit found undescribed clips, duplicate IDs, or a broken schema

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import datetime
import os
import re
import sys

COLUMNS = [
    "ClipID",        # stable identity. The only thing a render JSON may bind to.
    "File",          # path as the renderer sees it, e.g. driving/passenger-princess-01.mp4
    "Shot",          # REQUIRED. One plain sentence of what is literally on screen.
    "Tags",          # semicolon-separated nouns the caption might use
    "Mood",          # calm | focused | soft | playful | tired | tender
    "DurationSec",
    "Orientation",
    "Lane",
    "Described",     # yes | no. The gate refuses anything that is not yes.
    "SourcePath",
    "SHA256",
    "Thumb",
]

_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(text):
    return _SLUG.sub("-", (text or "").lower()).strip("-")


def category_of(row):
    """Best guess at the renderer-facing folder, from the source path."""
    folder = row.get("Folder / Location") or row.get("FullPath") or ""
    leaf = os.path.basename(folder.replace("\\", "/").rstrip("/"))
    return slugify(leaf) or "unsorted"


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


_VID_PREFIX = re.compile(r"VID_(\d{4})(\d{2})(\d{2})_")
_LEADING_DATE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})[-_]")
_TRAILING_STAMP = re.compile(r"(\d{4})(\d{2})(\d{2})\d{6}(?:\.\w+)?$")


def derive_captured(clip_id, file_name):
    """A phone names its own files with the date it captured them
    (VID_20260409_..., 2026-04-08-..., ..._20260509132226.mp4). Pull that date
    back out where the filename encodes one, rather than trusting Drive's own
    createdTime, which is only when the file reached Drive and can lag the
    actual recording by weeks."""
    for text in (clip_id or "", file_name or ""):
        for pattern in (_VID_PREFIX, _LEADING_DATE, _TRAILING_STAMP):
            m = pattern.search(text)
            if not m:
                continue
            year, month, day = (int(g) for g in m.groups())
            try:
                return datetime.date(year, month, day).isoformat()
            except ValueError:
                continue
    return None


def derive_dates(path, out_path):
    rows = read_csv(path)
    with open(path, newline="", encoding="utf-8-sig") as handle:
        fieldnames = list(csv.DictReader(handle).fieldnames or [])
    for column in ("Captured", "DateSource"):
        if column not in fieldnames:
            fieldnames.append(column)

    from_filename = from_upload = 0
    for row in rows:
        if (row.get("Captured") or "").strip():
            continue
        found = derive_captured(row.get("ClipID"), row.get("File"))
        if found:
            row["Captured"], row["DateSource"] = found, "filename"
            from_filename += 1
        else:
            row["Captured"] = (row.get("Created") or "").strip()
            row["DateSource"] = "drive-upload" if row["Captured"] else ""
            from_upload += 1

    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("GM-Clip-Library dates")
    print("  file      : %s" % out_path)
    print("  rows      : %d" % len(rows))
    print("  captured date read from the filename itself : %d" % from_filename)
    print("  no date in the filename, kept Drive's upload time : %d" % from_upload)
    return 0


def build(triage_path, out_path, merge):
    rows = read_csv(triage_path)
    keep = [r for r in rows if (r.get("Verdict") or "").strip().upper() == "KEEP"]

    prior_by_hash, prior_by_file = {}, {}
    if merge and os.path.exists(out_path):
        for row in read_csv(out_path):
            if row.get("SHA256"):
                prior_by_hash[row["SHA256"]] = row
            if row.get("SourcePath"):
                prior_by_file[row["SourcePath"]] = row

    used_ids = set()
    out_rows = []
    kept_descriptions = 0

    for row in keep:
        name = row.get("Asset Name") or ""
        category = category_of(row)
        base = slugify(os.path.splitext(name)[0]) or "clip"
        clip_id = "%s-%s" % (category, base)
        n = 2
        while clip_id in used_ids:
            clip_id = "%s-%s-%02d" % (category, base, n)
            n += 1
        used_ids.add(clip_id)

        source = row.get("FullPath") or ""
        prior = prior_by_hash.get(row.get("SHA256") or "") or prior_by_file.get(source)

        shot = (prior or {}).get("Shot", "").strip()
        if prior and shot:
            kept_descriptions += 1

        out_rows.append({
            "ClipID": (prior or {}).get("ClipID") or clip_id,
            "File": (prior or {}).get("File") or "%s/%s" % (category, name),
            "Shot": shot,
            "Tags": (prior or {}).get("Tags", ""),
            "Mood": (prior or {}).get("Mood", ""),
            "DurationSec": row.get("DurationSec", ""),
            "Orientation": row.get("Orientation", ""),
            "Lane": row.get("Lane", ""),
            "Described": "yes" if len(shot) >= 12 else "no",
            "SourcePath": source,
            "SHA256": row.get("SHA256", ""),
            "Thumb": row.get("Thumb", ""),
        })

    with open(out_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(out_rows)

    described = sum(1 for r in out_rows if r["Described"] == "yes")
    print("GM-Clip-Library")
    print("  triage rows : %d  (%d KEEP)" % (len(rows), len(keep)))
    print("  written     : %s  (%d clips)" % (out_path, len(out_rows)))
    if merge:
        print("  descriptions carried forward: %d" % kept_descriptions)
    print("  described   : %d of %d" % (described, len(out_rows)))
    if described < len(out_rows):
        print("")
        print("  %d clip(s) still need a Shot line. Until a clip is described the gate"
              % (len(out_rows) - described))
        print("  will not let a caption bind to it. Open the thumbs folder, write one")
        print("  plain sentence per clip in the Shot column, set Described to yes.")
    return 0


def audit(path):
    rows = read_csv(path)
    problems = []

    with open(path, newline="", encoding="utf-8-sig") as handle:
        header = csv.DictReader(handle).fieldnames or []
    for column in ("ClipID", "File", "Shot", "DurationSec"):
        if column not in header:
            problems.append(("SCHEMA", "required column missing: %s" % column))

    seen = {}
    undescribed = []
    for i, row in enumerate(rows, start=2):
        clip_id = (row.get("ClipID") or "").strip()
        if not clip_id:
            problems.append(("NO_ID", "row %d has no ClipID" % i))
            continue
        if clip_id in seen:
            problems.append(("DUPLICATE_ID",
                             'ClipID "%s" appears at rows %d and %d' % (clip_id, seen[clip_id], i)))
        seen[clip_id] = i

        shot = (row.get("Shot") or "").strip()
        flag = (row.get("Described") or "").strip().lower()
        if len(shot) < 12 or flag in ("no", "false", "0"):
            undescribed.append({
                "id": clip_id,
                "when": (row.get("Captured") or row.get("Created") or "").strip(),
                "lane": (row.get("Lane") or "").strip(),
                "file": (row.get("File") or "").strip(),
            })
        try:
            if float(row.get("DurationSec") or 0) <= 0:
                problems.append(("NO_DURATION", 'clip "%s" has no duration' % clip_id))
        except ValueError:
            problems.append(("BAD_DURATION",
                             'clip "%s" duration is not a number' % clip_id))

    # Oldest first: a human works through these by hand, and the ones sitting
    # longest unsorted are the ones most likely to get lost entirely.
    undescribed.sort(key=lambda r: (r["when"], r["id"]))

    print("GM-Clip-Library audit")
    print("  file      : %s" % path)
    print("  clips     : %d" % len(rows))
    print("  described : %d" % (len(rows) - len(undescribed)))
    print("")
    if undescribed:
        print("UNDESCRIBED — unusable until a Shot line is written (%d), oldest first"
              % len(undescribed))
        for u in undescribed[:40]:
            print("  %-34s %-11s %-9s %s"
                  % (u["id"], u["when"] or "?", u["lane"] or "?", u["file"]))
        if len(undescribed) > 40:
            print("  ... and %d more" % (len(undescribed) - 40))
        print("")
    if problems:
        print("PROBLEMS (%d)" % len(problems))
        for code, message in problems:
            print("  [%s] %s" % (code, message))
        print("")

    if problems or undescribed:
        print("VERDICT: NOT READY — the gate will reject bindings to these clips.")
        return 1
    print("VERDICT: READY — every clip is described and uniquely identified.")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Build or audit clip-library.csv.")
    parser.add_argument("--from-triage", help="video-triage.csv from Run 3")
    parser.add_argument("--out", help="output CSV (default: overwrite the input)")
    parser.add_argument("--merge", action="store_true",
                        help="keep Shot descriptions already written")
    parser.add_argument("--audit", help="audit an existing clip-library.csv")
    parser.add_argument("--derive-dates",
                        help="fill in Captured/DateSource on a Drive-pull CSV "
                             "from filename patterns, in place unless --out is given")
    args = parser.parse_args()

    if args.audit:
        return audit(args.audit)
    if args.derive_dates:
        return derive_dates(args.derive_dates, args.out or args.derive_dates)
    if args.from_triage:
        return build(args.from_triage, args.out or "clip-library.csv", args.merge)
    parser.error("pass --from-triage, --derive-dates, or --audit")


if __name__ == "__main__":
    sys.exit(main())
