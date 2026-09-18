#!/usr/bin/env python3
"""Refuse content that does not carry Amanda's message, and refuse a lane leak.

Run 10 doctrine. Two failures, both measured, both the same shape.

The first is the lane. 30,671 views produced 13 email subscribers. Run 8 read
that as a missing contract and added one. The contract was not the whole
problem. The reach was in the senior dog lane and the offer was in the business
lane, and a person who arrived for a 19 year old dog does not buy a $750
systems engagement. The weekday rotation gave 2 of 7 slots to a free dog guide
and 0 slots to the 2 products that actually take money. The Decision Map at $47
and Done Reacting to Money at $37 were both live, both selling, and both absent
from the week.

The second is the message. Amanda's own words, 09/18: "the gentle muse is not a
clear enough purpose and call to action channel to hold its own." The brand
thesis lived in her head and in 3 prose handoffs that each carried a different
version of it. Run 9 already showed what happens to a standing fact kept in
prose.

So the message becomes a table and the lane becomes a field, and this refuses
anything that ignores either.

  --position   audits brand-position.csv. Every claim needs a source.
  --rotation   audits the weekday rotation. Every slot names a live keyword, a
               format that exists, and the positioning row it serves.
  --queue      reads the post queue and refuses a lane leak in either
               direction.
  --week       counts a week by delivery and refuses one that fell below the
               face floor, then reports where the calls to action actually went.

  python3 gm_position_check.py --position
  python3 gm_position_check.py --rotation
  python3 gm_position_check.py --queue queue.json
  python3 gm_position_check.py --week week.json --face-floor 4

The floor exists because "film more" is guidance. Amanda, 09/18: film face to
camera as much as she can, and use the other content as filler when she is
pressed for time. Filler is a fallback, and a fallback with nothing counting it
quietly becomes the plan. 4 of 7 is a majority and it is deliberately
reachable against a Sunday to Thursday shift and a Friday and Saturday filming
window. Raise it when a week clears it comfortably.

Exit 0 PASS, 1 FAIL, 2 HOLD. No third-party packages. Python 3.8+.
"""
import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
POSITION = os.path.join(DATA, "brand-position.csv")
ROTATION = os.path.join(DATA, "rotation-magnet.csv")
FORMATS = os.path.join(DATA, "content-format.csv")
MAGNETS = os.path.join(DATA, "magnet-map.csv")

FIELDS = {"reader", "promise", "absolution", "guarantee", "proof", "enemy",
          "math", "never", "lane", "face", "sells", "transformation", "generosity"}

# The split, as account ids. Amanda's channels convert on Amanda.
AMANDA = {"45886", "30840", "41488", "36129", "20723", "21430", "6328"}
CESA = {"65540", "55761"}

# magnet-map carries a Lane per keyword. These 2 may never cross.
CESA_LANE = "cesa"
BUSINESS_LANES = {"build"}

KEYWORD_CTA = re.compile(r"\b(?i:comment)(?:\s+the\s+word)?\s+([A-Z][A-Z0-9]{2,})\b")


def norm(s):
    return (s or "").strip()


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def report(findings, quiet, header):
    fails = [f for f in findings if not f["code"].startswith("H")]
    holds = [f for f in findings if f["code"].startswith("H")]
    if not quiet:
        for f in sorted(findings, key=lambda f: (f["code"], f["id"])):
            print("%-22s %-10s %s" % (f["code"], f["id"], f["msg"]))
        print("\n%s: %d findings (%d fail, %d hold)"
              % (header, len(findings), len(fails), len(holds)))
    return 1 if fails else (2 if holds else 0)


# --------------------------------------------------------------- the message

def audit_position(rows):
    findings = []

    def add(code, pid, msg):
        findings.append({"code": code, "id": pid, "msg": msg})

    seen = set()
    for r in rows:
        pid = norm(r.get("PosID")) or "(blank)"
        field = norm(r.get("Field")).lower()
        if pid in seen:
            add("M04_DUPLICATE_ID", pid, "this PosID is already used")
        seen.add(pid)
        if not norm(r.get("Value")):
            add("M01_NO_VALUE", pid, "a positioning row with no value says nothing")
        if not norm(r.get("Source")):
            add("M02_NO_SOURCE", pid,
                "no source. A brand thesis nobody can trace is how the last 3 handoffs drifted.")
        if field not in FIELDS:
            add("M03_BAD_FIELD", pid, "Field '%s' is not one of %s"
                % (field, ", ".join(sorted(FIELDS))))

    have = {norm(r.get("Field")).lower() for r in rows}
    for must in ("reader", "promise", "guarantee", "proof", "never"):
        if must not in have:
            add("M05_MISSING_FIELD", "-",
                "the table names no %s. Without it the message is not decidable." % must)
    return findings


# -------------------------------------------------------------- the rotation

def audit_rotation(rot, formats, magnets, position):
    findings = []

    def add(code, day, msg):
        findings.append({"code": code, "id": day, "msg": msg})

    known_formats = {norm(f.get("FormatID")) for f in formats}
    known_pos = {norm(p.get("PosID")) for p in position}
    live = {norm(m.get("Keyword")).upper(): m for m in magnets}

    for r in rot:
        day = norm(r.get("Weekday")) or "(blank)"
        kw = norm(r.get("Keyword")).upper()
        fmt = norm(r.get("Format"))
        serves = norm(r.get("Serves"))

        m = live.get(kw)
        if not kw:
            add("R04_DEAD_KEYWORD", day, "the slot names no keyword, so it captures nothing")
        elif m is None:
            add("R04_DEAD_KEYWORD", day, "%s is in no automation" % kw)
        elif norm(m.get("Status")).lower() not in ("", "live"):
            add("R04_DEAD_KEYWORD", day,
                "%s is %s and will not answer" % (kw, norm(m.get("Status"))))
        elif norm(m.get("Lane")).lower() == CESA_LANE:
            add("R01_LANE_LEAK", day,
                "%s is a Cesa lane keyword and this is Amanda's rotation. "
                "Cesa converts on Cesa's channel." % kw)

        if not fmt:
            add("R02_UNKNOWN_FORMAT", day,
                "no format. Freestyle with no rails is the thing that was not clicking.")
        elif fmt not in known_formats:
            add("R02_UNKNOWN_FORMAT", day, "format %s is not in content-format.csv" % fmt)

        if not serves:
            add("R03_NO_MESSAGE", day,
                "this slot serves no line of the positioning, so it is content for its own sake")
        elif serves not in known_pos:
            add("R03_NO_MESSAGE", day, "Serves names %s, which is not in brand-position.csv" % serves)

    return findings


# ----------------------------------------------------------------- the queue

def check_queue(rows, magnets):
    findings = []

    def add(code, row, msg):
        findings.append({"code": code, "id": row.get("id", "?"), "msg": msg})

    lane_of = {norm(m.get("Keyword")).upper(): norm(m.get("Lane")).lower() for m in magnets}

    for row in rows:
        text = row.get("text") or ""
        aid = str(row.get("accountId") or "").strip()
        named = [kw for kw in lane_of if re.search(r"\b" + kw + r"\b", text)]
        named += [w for w in KEYWORD_CTA.findall(text) if w in lane_of and w not in named]

        for kw in named:
            lane = lane_of[kw]
            if lane == CESA_LANE and aid in AMANDA:
                add("Q01_LANE_LEAK", row,
                    "routes %s, a Cesa lane keyword, on one of Amanda's accounts (%s). "
                    "Cesa may appear. She may not carry the call to action here." % (kw, aid))
            elif lane in BUSINESS_LANES and aid in CESA:
                add("Q01_LANE_LEAK", row,
                    "routes %s, a business keyword, on Cesa's account (%s). Her audience "
                    "came for the dog and does not buy the ladder." % (kw, aid))
    return findings


# ------------------------------------------------------------------ the week

def check_week(rows, magnets, floor):
    """Did the week actually get filmed, and where did the asks go."""
    findings, counts = [], {}
    kind_of = {norm(m.get("Keyword")).upper(): norm(m.get("Kind")).lower() for m in magnets}

    undeclared = []
    for r in rows:
        d = norm(r.get("delivery")).lower()
        if not d:
            undeclared.append(r.get("id", "?"))
            continue
        counts[d] = counts.get(d, 0) + 1

    face = counts.get("face", 0)
    # A week that declares nothing is a hold, not a failure. You cannot miss a
    # floor you have no measurement for.
    if counts and face < floor:
        findings.append({"code": "W01_FACE_FLOOR", "id": "week",
                         "msg": "%d of %d posts are face to camera, under the floor of %d. "
                                "Filler is the fallback, not the plan."
                                % (face, len(rows), floor)})
    if undeclared:
        findings.append({"code": "H03_NO_DELIVERY", "id": "week",
                         "msg": "%d posts declare no delivery, so they cannot be counted: %s"
                                % (len(undeclared), ", ".join(undeclared[:6]))})

    routed = {}
    for r in rows:
        text = r.get("text") or ""
        for kw, kind in kind_of.items():
            if re.search(r"\b" + re.escape(kw) + r"\b", text):
                routed[kind] = routed.get(kind, 0) + 1
                break
    return findings, counts, routed


# ----------------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--position", action="store_true", help="audit the positioning table")
    ap.add_argument("--rotation", action="store_true", help="audit the weekday rotation")
    ap.add_argument("--queue", metavar="JSON", help="check a post queue for lane leaks")
    ap.add_argument("--week", metavar="JSON", help="count a week by delivery")
    ap.add_argument("--face-floor", type=int, default=4, metavar="N",
                    help="how many of the week's posts must be face to camera, default 4")
    ap.add_argument("--position-file", default=POSITION)
    ap.add_argument("--rotation-file", default=ROTATION)
    ap.add_argument("--formats", default=FORMATS)
    ap.add_argument("--magnets", default=MAGNETS)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if not (a.position or a.rotation or a.queue or a.week):
        ap.error("nothing to check. Pass --position, --rotation, --queue or --week.")

    try:
        position = load(a.position_file)
        magnets = load(a.magnets)
    except FileNotFoundError as e:
        print("cannot read %s. Nothing is checked and nothing is assumed." % e.filename)
        return 2

    worst = 0

    if a.position:
        worst = max(worst, report(audit_position(position), a.quiet,
                                  "%d positioning rows audited" % len(position)))

    if a.rotation:
        try:
            rot, formats = load(a.rotation_file), load(a.formats)
        except FileNotFoundError as e:
            print("cannot read %s." % e.filename)
            return 2
        if not a.quiet and a.position:
            print()
        worst = max(worst, report(audit_rotation(rot, formats, magnets, position),
                                  a.quiet, "%d rotation slots audited" % len(rot)))

    if a.queue:
        try:
            rows = json.load(open(a.queue, encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("cannot read the queue: %s" % e)
            return 2
        if isinstance(rows, dict):
            rows = rows.get("items") or rows.get("posts") or []
        if not a.quiet and (a.position or a.rotation):
            print()
        worst = max(worst, report(check_queue(rows, magnets), a.quiet,
                                  "%d posts checked" % len(rows)))

    if a.week:
        try:
            rows = json.load(open(a.week, encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("cannot read the week: %s" % e)
            return 2
        if isinstance(rows, dict):
            rows = rows.get("items") or rows.get("posts") or []
        findings, counts, routed = check_week(rows, magnets, a.face_floor)
        if not a.quiet and (a.position or a.rotation or a.queue):
            print()
        worst = max(worst, report(findings, a.quiet, "%d posts in the week" % len(rows)))
        if not a.quiet:
            print("\ndelivery: %s" % (", ".join("%s %d" % (k, v)
                  for k, v in sorted(counts.items())) or "nothing declared"))
            print("the asks went to: %s" % (", ".join("%s %d" % (k, v)
                  for k, v in sorted(routed.items())) or "nothing"))

    return worst


if __name__ == "__main__":
    sys.exit(main())
