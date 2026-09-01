#!/usr/bin/env python3
"""
GM-Teardown-Check — the competitor teardown gate.

Run 8 of the Gentle Muse filing system. Two jobs.

  --bank    audits the teardown bank and refuses to let a name that was only
            mentioned in somebody's listicle be cited as a finding. A handle
            nobody pulled an artifact from is a lead, not a competitor.

  --render  audits a reel payload. A reel that carries a call to action must
            also declare the Contract it is asking the viewer to enter. Follow,
            comment, share is a request. A contract is a promise with a
            frequency or a stance behind it.

Why the Contract field exists at all. Run 6 established the pattern: when the
same failure happens twice, add the missing column and a check that refuses to
ship without it, rather than writing guidance about being careful. The failure
here is measured. 30,671 views produced 13 email subscribers. Views to
followers works. Followers to email does not. Every account in the teardown
bank that converts states a promise the viewer can subscribe to. None of them
ask. So the missing thing is not a better CTA, it is a declared contract, and
this gate is where it gets enforced.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A PASS is a proposal, not a publish.
  No substitution. A missing input is reported, never filled with the nearest
  thing that fits the slot.

Exit codes
  0   PASS      everything checked holds
  1   FAIL      at least one blocking finding. Nothing ships.
  2   HOLD      no failures, but rows are leads only and nothing is usable yet.

Usage
  python3 gm_teardown_check.py --bank filing-system/data/competitor-teardowns.csv
  python3 gm_teardown_check.py --render reel-factory/reels-footage.json
  python3 gm_teardown_check.py --bank BANK --render DIR --report out.csv

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys

# Confidence levels, weakest first. Anything below PULLED means nobody has
# actually looked at the thing being described.
LISTED = "listed"            # a name in somebody else's roundup
PULLED = {"transcript", "reported", "adlibrary"}
ALL_CONFIDENCE = PULLED | {LISTED}

PLACEHOLDER_HANDLES = {"", "unconfirmed", "unknown", "tbd", "n/a", "na", "-"}

# A contract has to promise something. These are requests wearing a promise's
# clothes, and every one of them is what Amanda is currently shipping.
GENERIC_CONTRACT = [
    "follow for more", "follow me", "like and subscribe", "subscribe for",
    "more content", "stay tuned", "don't forget to", "dont forget to",
    "hit follow", "smash that", "link in bio", "check out my",
    "comment below", "share this",
]

# A closing beat that opens on one of these is giving the viewer an instruction.
# Authority delivers. It does not ask permission first.
REQUEST_OPENERS = {
    "send", "share", "tag", "follow", "comment", "save", "drop", "like",
    "subscribe", "click", "dm", "type", "hit", "smash", "repost", "duet",
    "stitch", "join", "sign", "grab", "download", "check", "watch", "swipe",
    "don't", "dont", "make", "let", "go", "tell", "reply", "leave",
}

SENTENCE = re.compile(r"[^.!?]+")
WORD = re.compile(r"[A-Za-z']+")
STRIP_TAGS = re.compile(r"<[^>]+>")


def opening_word(text):
    m = WORD.search(text or "")
    return m.group(0).lower() if m else ""


def request_openers(label, line):
    """Every place this beat opens by telling the viewer what to do."""
    hits = []
    if opening_word(label) in REQUEST_OPENERS:
        hits.append(norm(label))
    plain = " ".join(STRIP_TAGS.sub(" ", line or "").split())
    for sentence in SENTENCE.findall(plain):
        if opening_word(sentence) in REQUEST_OPENERS:
            hits.append(sentence.strip())
    return hits


BANK_COLS = ["TeardownID", "Handle", "Platform", "Lane", "Followers",
             "ArtifactURL", "Views", "Likes", "EngRate", "Hook", "Structure",
             "Contract", "MoneyPath", "StealThis", "Evidence", "Confidence",
             "Verified"]


def norm(s):
    return (s or "").strip()


def lower(s):
    return norm(s).lower()


def as_num(s):
    try:
        return float(norm(s).replace(",", ""))
    except ValueError:
        return None


# ------------------------------------------------------------------ the bank

def check_bank(path):
    """Returns (findings, notes, usable_count, total)."""
    findings, notes = [], []
    if not os.path.exists(path):
        return ([("T00_NO_BANK", path, "teardown bank not found")], [], 0, 0)

    with open(path, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))

    if rows:
        missing = [c for c in BANK_COLS if c not in rows[0]]
        if missing:
            findings.append(("T09_SCHEMA", path,
                             "bank is missing columns: " + ", ".join(missing)))

    seen = {}
    usable = 0
    for i, r in enumerate(rows, start=2):
        tid = norm(r.get("TeardownID")) or ("row %d" % i)
        handle = norm(r.get("Handle"))
        conf = lower(r.get("Confidence"))
        verified = lower(r.get("Verified")) == "yes"

        if tid in seen:
            findings.append(("T07_DUPLICATE_ID", tid,
                             "already used on row %d" % seen[tid]))
        seen[tid] = i

        if conf and conf not in ALL_CONFIDENCE:
            findings.append(("T08_BAD_CONFIDENCE", tid,
                             "confidence '%s' is not one of: %s"
                             % (conf, ", ".join(sorted(ALL_CONFIDENCE)))))

        # The substitution ban, made mechanical. A roundup mention is a lead.
        if verified and conf == LISTED:
            findings.append(("T02_UNVERIFIED_CLAIM", tid,
                             "marked verified on a listicle mention. Somebody "
                             "else's roundup is not evidence. Pull the artifact "
                             "or leave Verified as no."))

        if verified and lower(handle) in PLACEHOLDER_HANDLES:
            findings.append(("T06_PLACEHOLDER_HANDLE", tid,
                             "marked verified with no real handle. A name "
                             "without a handle cannot be checked, and inventing "
                             "the handle is the thing this gate exists to stop."))

        if verified and not norm(r.get("Evidence")):
            findings.append(("T01_NO_EVIDENCE", tid,
                             "marked verified with no Evidence URL"))

        if verified and not norm(r.get("Hook")) and not norm(r.get("ArtifactURL")):
            findings.append(("T03_NO_ARTIFACT", tid,
                             "marked verified but carries neither a quoted hook "
                             "nor an artifact URL. Nothing was actually read."))

        if verified and not norm(r.get("Contract")):
            findings.append(("T04_NO_CONTRACT", tid,
                             "marked verified with no Contract. The whole point "
                             "of the teardown is naming the promise that earns "
                             "the follow."))

        views, likes = as_num(r.get("Views")), as_num(r.get("Likes"))
        rate = as_num(r.get("EngRate"))
        if views and likes and rate is not None:
            actual = likes / views
            if abs(actual - rate) > 0.005:
                findings.append(("T05_ENGRATE", tid,
                                 "EngRate says %.3f, likes over views is %.3f"
                                 % (rate, actual)))

        if verified:
            usable += 1
        else:
            notes.append(("N02_LEAD_ONLY", tid,
                          "lead only%s. Not usable as a model until an artifact "
                          "is pulled." % (" (" + handle + ")" if handle and
                                          lower(handle) not in PLACEHOLDER_HANDLES
                                          else "")))

    return findings, notes, usable, len(rows)


# ---------------------------------------------------------------- the render

def payload_files(path):
    if os.path.isdir(path):
        return sorted(os.path.join(path, f) for f in os.listdir(path)
                      if f.endswith(".json"))
    return [path]


def check_render(path):
    findings, notes, holds = [], [], []
    for f in payload_files(path):
        if not os.path.exists(f):
            findings.append(("C00_NO_RENDER", f, "render payload not found"))
            continue
        try:
            with open(f, encoding="utf-8") as fh:
                doc = json.load(fh)
        except (ValueError, OSError) as e:
            findings.append(("C00_NO_RENDER", f, "could not read: %s" % e))
            continue

        reels = doc if isinstance(doc, list) else [doc]
        for reel in reels:
            if not isinstance(reel, dict):
                continue
            name = norm(reel.get("id")) or norm(reel.get("title")) \
                or os.path.basename(f)
            beats = reel.get("beats") or []
            cta_beats = [b for b in beats
                         if isinstance(b, dict) and norm(b.get("cta"))]
            has_cta = bool(cta_beats)

            for b in cta_beats:
                for hit in request_openers(b.get("cta"), b.get("html")):
                    findings.append(("C04_REQUEST_NOT_DELIVERY", name,
                                     "the closing beat instructs the viewer: "
                                     "\"%s\". State who it is for and what they "
                                     "now have. Do not ask." % hit))
            contract = norm(reel.get("contract"))

            if has_cta and not contract:
                findings.append(("C01_CTA_WITHOUT_CONTRACT", name,
                                 "carries a call to action and declares no "
                                 "contract. The ask is the mechanism. The "
                                 "promise is what gets subscribed to."))
            elif contract:
                low = contract.lower()
                hit = next((g for g in GENERIC_CONTRACT if g in low), None)
                if hit:
                    findings.append(("C03_GENERIC_CONTRACT", name,
                                     "contract reads as a request, not a "
                                     "promise: '%s'" % hit))
                elif len(contract.split()) < 4:
                    findings.append(("C02_THIN_CONTRACT", name,
                                     "contract is too short to promise "
                                     "anything: '%s'" % contract))
            # A reel that asks for nothing still has to say where the viewer
            # goes next. Amanda runs live comment-to-DM keywords; a reel that
            # names none of them is spending reach with no way to catch it.
            # Silence is not allowed. Either name the keyword, or say in the
            # file why no live one fits.
            if has_cta:
                kw = norm(reel.get("keyword"))
                gap = norm(reel.get("keyword_gap"))
                if not kw and not gap:
                    findings.append(("C05_NO_CAPTURE_PATH", name,
                                     "no keyword and no stated gap. Name the "
                                     "live comment-to-DM keyword this reel "
                                     "feeds, or record why none of them fits."))
                elif not kw and len(gap) < 20:
                    findings.append(("C05_THIN_GAP", name,
                                     "keyword_gap does not say anything: '%s'" % gap))
                elif not kw:
                    notes.append(("N04_NO_KEYWORD", name,
                                  "reach with no capture path. %s" % gap))

            for h in (reel.get("holds") or []):
                holds.append(("H01_UNVERIFIED_CLAIM", name, norm(h)))

            if not has_cta and not contract:
                notes.append(("N03_NO_CTA", name,
                              "no call to action and no contract. Fine for a "
                              "pure atmosphere cut, worth a look otherwise."))
    return findings, notes, holds


# -------------------------------------------------------------------- report

def emit(findings, notes, report, holds=()):
    for code, subject, detail in findings:
        print("FAIL  %-24s %s" % (code, subject))
        print("      %s" % detail)
    for code, subject, detail in holds:
        print("HOLD  %-24s %s" % (code, subject))
        print("      %s" % detail)
    for code, subject, detail in notes:
        print("note  %-24s %s" % (code, subject))
        print("      %s" % detail)
    if report:
        with open(report, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["Level", "Code", "Subject", "Detail"])
            for code, subject, detail in findings:
                w.writerow(["FAIL", code, subject, detail])
            for code, subject, detail in holds:
                w.writerow(["HOLD", code, subject, detail])
            for code, subject, detail in notes:
                w.writerow(["note", code, subject, detail])


def main():
    ap = argparse.ArgumentParser(description="Gentle Muse teardown gate.")
    ap.add_argument("--bank", help="competitor-teardowns.csv")
    ap.add_argument("--render", help="a reel payload JSON, or a directory")
    ap.add_argument("--report", help="write findings to this CSV")
    args = ap.parse_args()

    if not args.bank and not args.render:
        ap.error("give --bank, --render, or both")

    findings, notes, holds = [], [], []
    usable = total = 0
    if args.bank:
        f, n, usable, total = check_bank(args.bank)
        findings += f
        notes += n
    if args.render:
        f, n, h = check_render(args.render)
        findings += f
        notes += n
        holds += h

    emit(findings, notes, args.report, holds)
    print()

    if findings:
        print("FAIL. %d finding(s). Nothing ships." % len(findings))
        return 1
    if holds:
        print("HOLD. %d reel(s) assert something nobody confirmed. Those do not "
              "ship until Amanda says the claim is true." % len(holds))
        return 2
    if args.bank and usable == 0 and total:
        print("HOLD. %d row(s), none verified. Every one is a lead. Pull an "
              "artifact before citing any of them." % total)
        return 2
    if args.bank:
        print("PASS. %d of %d rows are backed by an artifact somebody read."
              % (usable, total))
    else:
        print("PASS.")
    print("This is a proposal, not a publish. Approval is still the gate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
