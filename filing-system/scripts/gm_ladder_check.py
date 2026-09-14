#!/usr/bin/env python3
"""
GM-Ladder-Check — the one thing gate.

Amanda runs 2 companies and has enough ambition for 5 people. The failure this
is built for is not laziness and it is not a bad plan. It is working on station
13 while station 2 is still open, which feels like progress every single day and
produces 7 half finished things in month 7 instead of 1 finished one.

A roadmap does not stop that, because a roadmap is guidance and guidance governs
judgment. Judgment is what already fails here. So the sequence is a data file
with an exit test on every row, and this refuses to let a later station be
called today's work while an earlier one is open.

The rule the whole thing runs on:

  1 work station is open at a time. It closes when its DoneWhen is proven by an
  artifact somebody else could check. Not when it feels done.

Clock stations are the one exception, and they are marked in the file. A clock
station needs a few hours a month and then the calendar. It runs underneath the
open work station because waiting is not attention.

House rules, same as every other module:
  Propose-only. This reads. It never moves, renames or deletes anything.
  Approval is the gate. A PASS is a proposal. Amanda closes a station, not this.
  No substitution. A task that matches no station is reported as unmatched and
  the run stops. It is never filed under the nearest station that fits.

Exit codes
  0   PASS   the ladder is sound, or the task belongs to today
  1   FAIL   at least one blocking finding, or the task belongs to a later station
  2   HOLD   clean, but waiting on something only Amanda can file

Usage
  python3 gm_ladder_check.py --ladder                  audit the sequence
  python3 gm_ladder_check.py --today                   what is the one thing
  python3 gm_ladder_check.py --task "build a due diligence checklist"
  python3 gm_ladder_check.py --deal deals/maple-st.csv run a deal through the gates

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DEFAULT_LADDER = os.path.join(DATA, "mastery-ladder.csv")
DEFAULT_GATES = os.path.join(DATA, "acquisition-gates.csv")

# Avery's weekly hierarchy, in priority order. This is the tiebreak when 2
# things both look urgent, and it is the order the ladder is sequenced in.
LAYERS = ["protect", "sell", "distribute", "improve", "automate", "expand"]
LAYER_MEANING = {
    "protect": "cash, legal standing, deadlines, trust, continuity",
    "sell": "anything that produces revenue or moves somebody closer to buying",
    "distribute": "content, outreach, email growth, partnerships, audience",
    "improve": "funnels, messaging, process, conversion",
    "automate": "removing repeat labour, after the process works",
    "expand": "new products, new platforms, new locations, acquisitions",
}
RANK = {name: i for i, name in enumerate(LAYERS)}
KINDS = ["work", "clock"]
STATUSES = ["done", "open", "locked"]

# An exit test has to be something a second person could check. A number, a
# named file, or a signature. Everything else is an opinion about progress.
_COUNTABLE = re.compile(r"\d|\b\w+\.(?:csv|json|md|txt|pdf)\b|in writing", re.I)

# The way a mastery station fails: the exit test is a feeling. "Understand the
# numbers" has no last day. "6 numbers, 6 sources" has one.
FEELINGS = [
    "understand", "understood", "know about", "knowledge of", "feel ",
    "feels ", "comfortable", "confident", "clear on", "clarity", "be ready",
    "familiar", "grasp", "get a handle", "wrap my head", "get good at",
    "better at", "master ", "mastery", "competent", "competence", "learn about",
]


def norm(text):
    return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def needs_of(row):
    return [n.strip() for n in (row.get("Needs") or "").split("|") if n.strip()]


def companies_of(row, every):
    c = (row.get("Company") or "").strip()
    return set(every) if c == "both" else {c}


# ---------------------------------------------------------------- the audit

def audit(rows):
    """Every finding the sequence itself can be wrong in. Returns (findings, holds)."""
    findings, holds = [], []
    by_id = {r["StationID"]: r for r in rows}
    every = {c for r in rows for c in [(r.get("Company") or "").strip()] if c and c != "both"}

    seen_order = {}
    for r in rows:
        sid = r.get("StationID") or "?"
        for field, allowed in (("Layer", LAYERS), ("Kind", KINDS), ("Status", STATUSES)):
            if (r.get(field) or "").strip() not in allowed:
                findings.append((sid, "L00_BAD_FIELD",
                                 "%s is %r, not one of %s" % (field, r.get(field), "/".join(allowed))))
        try:
            order = int(r["Order"])
        except (KeyError, ValueError):
            findings.append((sid, "L00_BAD_FIELD", "Order is not a number"))
            continue
        if order in seen_order:
            findings.append((sid, "L00_BAD_FIELD",
                             "shares order %d with %s" % (order, seen_order[order])))
        seen_order[order] = sid

    rows = [r for r in rows if (r.get("Order") or "").strip().isdigit()]
    rows.sort(key=lambda r: int(r["Order"]))
    done = {r["StationID"] for r in rows if r["Status"] == "done"}

    # 1. the rule. One work station open, and never none while work remains.
    open_work = [r for r in rows if r["Status"] == "open" and r["Kind"] == "work"]
    if len(open_work) > 1:
        findings.append((", ".join(r["StationID"] for r in open_work), "L01_TWO_OPEN",
                         "%d work stations are open. The ladder allows 1." % len(open_work)))
    if not open_work and len(done) < len(rows):
        findings.append(("-", "L02_NOTHING_OPEN",
                         "%d stations are not done and none is open. Open the next one."
                         % (len(rows) - len(done))))

    for r in rows:
        sid, layer, order = r["StationID"], r["Layer"], int(r["Order"])
        test = r.get("DoneWhen") or ""

        # 2. the exit test has to be checkable by somebody who is not Amanda.
        if not _COUNTABLE.search(test):
            findings.append((sid, "L03_UNCOUNTABLE",
                             "DoneWhen carries no number, no file and no signature: %r" % test[:60]))
        for word in FEELINGS:
            if word in test.lower():
                findings.append((sid, "L10_FEELING_TEST",
                                 "DoneWhen turns on %r, which has no last day" % word.strip()))
                break

        # 3. a closed station has to have left something behind.
        if r["Status"] == "done":
            proof = (r.get("ProofIs") or "").strip()
            if not proof:
                findings.append((sid, "L04_NO_PROOF", "done with no proof recorded"))
            else:
                for token in re.findall(r"[\w./-]+\.(?:csv|json|md|txt)", proof):
                    if not os.path.exists(os.path.join(REPO, token)):
                        holds.append((sid, "H01_PROOF_NOT_FILED",
                                      "proof names %s and it is not in the repo yet" % token))
            for need in needs_of(r):
                if need not in done:
                    findings.append((sid, "L09_DONE_GAP",
                                     "closed, but %s it depends on is not" % need))

        # 4. the flip. Automating and expanding before selling and distributing.
        mine = companies_of(r, every)
        if layer in ("automate", "expand"):
            for other in rows:
                if int(other["Order"]) > order and other["Layer"] in ("sell", "distribute") \
                        and companies_of(other, every) & mine:
                    findings.append((sid, "L05_WORKING_AHEAD",
                                     "%s before %s, which still has to %s"
                                     % (layer, other["StationID"], other["Layer"])))
                    break
        if layer == "expand":
            for other in rows:
                if int(other["Order"]) > order and other["Layer"] == "protect" \
                        and companies_of(other, every) & mine:
                    findings.append((sid, "L06_EXPAND_UNPROTECTED",
                                     "expands before %s protects it" % other["StationID"]))
                    break

        # 5. dependencies that point the wrong way, or open too early.
        for need in needs_of(r):
            if need not in by_id:
                findings.append((sid, "L00_BAD_FIELD", "needs %s, which is not a station" % need))
            elif (by_id[need].get("Order") or "").isdigit() and int(by_id[need]["Order"]) >= order:
                findings.append((sid, "L07_NEEDS_LATER",
                                 "needs %s, which is sequenced after it" % need))
        if r["Status"] == "open":
            missing = [n for n in needs_of(r) if n not in done]
            if missing:
                findings.append((sid, "L08_OPEN_LOCKED",
                                 "open, but %s not done" % ", ".join(missing)))
    return findings, holds


# ---------------------------------------------------------------- the screen

def today(rows):
    """The one thing, and nothing else. Clock stations listed underneath."""
    rows = sorted(rows, key=lambda r: int(r["Order"]))
    done = [r for r in rows if r["Status"] == "done"]
    open_work = [r for r in rows if r["Status"] == "open" and r["Kind"] == "work"]
    clocks = [r for r in rows if r["Status"] == "open" and r["Kind"] == "clock"]

    print("LADDER  %d of %d stations closed" % (len(done), len(rows)))
    if not open_work:
        print("\nnothing is open. Open the next locked station whose needs are met.")
    for r in open_work:
        print("\nTHE ONE THING  %s  %s" % (r["StationID"], r["Station"]))
        print("  company     %s" % r["Company"])
        print("  layer       %s, which is %s" % (r["Layer"], LAYER_MEANING[r["Layer"]]))
        print("  done when   %s" % r["DoneWhen"])
        print("  proved by   %s" % r["ProofIs"])
        print("  est         %s days" % r["EstDays"])
        unblocks = [o["StationID"] for o in rows if r["StationID"] in needs_of(o)]
        if unblocks:
            print("  unblocks    %s" % ", ".join(unblocks))
    for r in clocks:
        print("\n  running underneath  %s  %s" % (r["StationID"], r["Station"]))
        print("      %s, closes when %s" % (r["Kind"], r["DoneWhen"]))

    nxt = [r for r in rows if r["Status"] == "locked"]
    if nxt:
        n = nxt[0]
        print("\nNEXT    %s  %s, locked behind %s"
              % (n["StationID"], n["Station"], ", ".join(needs_of(n)) or "nothing"))
    print("\nWhen 2 things both look urgent, the earlier layer wins:")
    print("  " + " -> ".join(LAYERS))
    return 0


def route(rows, task):
    """Does this belong to today. No substitution: an unmatched task stops."""
    want = " %s " % norm(task)
    scored = []
    for r in rows:
        keys = [norm(k) for k in (r.get("Keywords") or "").split("|") if k.strip()]
        keys.append(norm(r["Station"]))
        hits = [k for k in keys if k and (" %s " % k) in want]
        if hits:
            scored.append((len(hits), -int(r["Order"]), r, hits))
    if not scored:
        print("TASK  %s" % task)
        print("\nNo station on the ladder owns this.")
        print("That is a stop, not a shrug. Either it belongs to a station nobody")
        print("has written down yet, in which case write the station, or it is not")
        print("this quarter's work. It is not filed under the nearest station that fits.")
        return 2

    best = max(s[0] for s in scored)
    matches = [s for s in scored if s[0] == best]
    matches.sort(key=lambda s: -s[1])
    open_work = [r for r in rows if r["Status"] == "open" and r["Kind"] == "work"]
    done = {r["StationID"] for r in rows if r["Status"] == "done"}

    print("TASK  %s" % task)
    worst = 0
    for _, _, r, hits in matches:
        print("\n  %s  %s  [%s]" % (r["StationID"], r["Station"], r["Status"]))
        print("      matched on %s" % ", ".join(hits))
        if r["Status"] == "open":
            print("      This is the one thing. Do it.")
            print("      Done when %s" % r["DoneWhen"])
        elif r["StationID"] in done:
            print("      Closed already. Maintenance on a closed station is fine.")
        else:
            blockers = [n for n in needs_of(r) if n not in done]
            print("      Not yet. Locked behind %s." % (", ".join(blockers) or "the sequence"))
            worst = 1
    if worst and open_work:
        r = open_work[0]
        print("\n  Today is %s, %s." % (r["StationID"], r["Station"]))
        print("  Done when %s" % r["DoneWhen"])
    return worst


def deal(path, template):
    """One real deal against the 8 gates. Unproven holds. Failed blocks."""
    rows = read_csv(path)
    want = [g["GateID"] for g in read_csv(template)]
    have = {r.get("GateID"): r for r in rows}
    findings, holds = [], []

    for gid in want:
        if gid not in have:
            findings.append((gid, "D03_MISSING_GATE", "the deal file does not carry this gate"))
    for gid in want:
        r = have.get(gid)
        if not r:
            continue
        verdict = (r.get("Verdict") or "").strip().lower()
        evidence = (r.get("Evidence") or "").strip()
        if verdict not in ("pass", "fail", "unproven"):
            findings.append((gid, "D04_BAD_VERDICT", "verdict is %r" % r.get("Verdict")))
        elif verdict == "fail":
            findings.append((gid, "D01_GATE_FAILED", r.get("Gate", "")))
        elif verdict == "unproven":
            holds.append((gid, "H02_GATE_UNPROVEN", r.get("Gate", "")))
        elif not evidence:
            findings.append((gid, "D02_NO_EVIDENCE",
                             "passed with nothing written down that says why"))

    print("DEAL  %s" % os.path.basename(path))
    print("  %d of %d gates passed with evidence"
          % (sum(1 for g in want if have.get(g, {}).get("Verdict", "").lower() == "pass"
                 and (have[g].get("Evidence") or "").strip()), len(want)))
    return report(findings, holds, "every gate passed. This is a proposal. Amanda decides.")


# ---------------------------------------------------------------- reporting

def report(findings, holds, clean_line):
    for sid, code, detail in findings:
        print("  %-24s %-12s %s" % (code, sid, detail))
    for sid, code, detail in holds:
        print("  %-24s %-12s %s" % (code, sid, detail))
    if findings:
        print("\nFAIL  %d blocking, %d held" % (len(findings), len(holds)))
        return 1
    if holds:
        print("\nHOLD  %d waiting on Amanda" % len(holds))
        return 2
    print("\nPASS  %s" % clean_line)
    return 0


def main():
    ap = argparse.ArgumentParser(description="the one thing gate")
    ap.add_argument("--ladder", nargs="?", const=DEFAULT_LADDER, default=None,
                    help="audit the sequence (default %s)" % os.path.basename(DEFAULT_LADDER))
    ap.add_argument("--today", action="store_true", help="print the one thing and stop")
    ap.add_argument("--task", help="does this task belong to today")
    ap.add_argument("--deal", help="run a filled gate sheet for one deal")
    ap.add_argument("--gates", default=DEFAULT_GATES, help="the gate template")
    a = ap.parse_args()

    path = a.ladder or DEFAULT_LADDER
    if a.deal:
        try:
            return deal(a.deal, a.gates)
        except OSError as e:
            print("cannot read the deal file: %s" % e)
            return 2
    try:
        rows = read_csv(path)
    except OSError as e:
        print("cannot read the ladder: %s" % e)
        return 2
    if not rows:
        print("the ladder is empty. Nothing to sequence.")
        return 2

    if a.today or a.task:
        # Both screens sort on Order. A hand-edited file with a typo in it gets
        # sent to the audit, which names the row, rather than to a traceback.
        bad = [r.get("StationID", "?") for r in rows
               if not (r.get("Order") or "").strip().isdigit()]
        if bad:
            print("%s has no usable Order: %s" % (", ".join(bad), path))
            print("Run --ladder for the full finding list.")
            return 2
        return today(rows) if a.today else route(rows, a.task)

    print("LADDER  %s, %d stations" % (os.path.basename(path), len(rows)))
    findings, holds = audit(rows)
    return report(findings, holds, "1 station open, the sequence holds.")


if __name__ == "__main__":
    sys.exit(main())
