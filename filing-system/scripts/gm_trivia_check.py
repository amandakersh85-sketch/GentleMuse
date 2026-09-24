#!/usr/bin/env python3
"""
GM-Trivia-Check — the trivia caption gate.

Run 8 of the Gentle Muse filing system. Reads a trivia post JSON and the fact
bank, and refuses any post whose claim is not traceable to a checked fact.

Run 7 stopped a caption being bound to a holiday fact nobody checked. This is
the same guard on a lane where the failure is likelier and lands harder. The
audience for AI and creator-economy trivia is an audience that will know when
a number is wrong, and the account exists to be the one that gets it right.

The rule that does the most work here is T03. Every number in the caption has
to appear in the bank row. A language model asked to write 40 seconds about a
2017 paper will happily add a parameter count, a funding round or a market
size that nobody asked for and nobody checked. Those extra numbers are the
whole risk, and they are mechanically findable.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A PASS is a proposal, not a publish.
  No substitution. No usable fact means HOLD, not the nearest fact that fits.

Exit codes
  0   PASS   every claim traced to a checked fact
  1   FAIL   at least one blocking finding. Nothing ships.
  2   HOLD   clean, but waiting on a fact that has not been checked yet.

Usage
  python3 gm_trivia_check.py --post caption.json
  python3 gm_trivia_check.py --post batch/

Post JSON: {"id", "factId", "platform", "text"}

No third-party packages. Python 3.8+.
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gm_trivia_bank import (  # noqa: E402
    DEFAULT_BANK, TOPICS, load_bank, usable_problems,
)

# Numbers that are not claims: hashtags, list counts in a call to action, and
# the ordinary small numbers any sentence carries.
NOISE_NUMBERS = {"1", "2", "3", "4", "5", "10"}


def numbers_in(text):
    """Every number a reader would take as a fact, normalised."""
    out = set()
    for raw in re.findall(r"\d[\d,]*(?:\.\d+)?", text or ""):
        n = raw.replace(",", "").rstrip(".")
        if n and n not in NOISE_NUMBERS:
            out.add(n)
    return out


def strip_cta(text):
    """The claim half of the caption, without the call to action and tags."""
    lines = []
    for line in (text or "").split("\n"):
        low = line.lower()
        if low.startswith("#") or "subscribepage" in low or "http" in low:
            continue
        if low.startswith(("comment ", "follow for", "follow along", "subscribe")):
            continue
        lines.append(line)
    return "\n".join(lines)


def check_post(post, bank):
    findings = []
    pid = post.get("id") or "(unnamed)"
    fid = (post.get("factId") or "").strip()
    text = post.get("text") or ""

    if not fid:
        return [{"rule": "T00_NO_FACT_ID", "level": "HOLD", "id": pid,
                 "detail": "the post names no FactID, so there is nothing to "
                           "check it against. Write the fact into the bank "
                           "first."}]

    fact = bank.get(fid)
    if fact is None:
        return [{"rule": "T01_UNKNOWN_FACT", "level": "FAIL", "id": pid,
                 "detail": '"%s" is not in the bank. A fact that is not written '
                           "down was not checked." % fid}]

    problems = usable_problems(fact)
    if problems:
        findings.append({
            "rule": "T02_FACT_NOT_USABLE", "level": "FAIL", "id": pid,
            "detail": "%s is in the bank but cannot carry a post yet: %s"
                      % (fid, "; ".join(problems)),
        })

    topic = (fact.get("Topic") or "").strip().lower()
    if topic not in TOPICS:
        findings.append({
            "rule": "T05_OFF_LANE", "level": "FAIL", "id": pid,
            "detail": 'topic "%s" is outside the lane. Generic trivia fills the '
                      "slot and dilutes the positioning it is meant to carry."
                      % (topic or "(blank)"),
        })

    # The hallucination catcher. Anything numeric the caption asserts has to
    # be a number the bank row actually holds.
    banked = numbers_in(" ".join([
        fact.get("Fact") or "", fact.get("AsOf") or "", fact.get("Backbone") or "",
    ]))
    claimed = numbers_in(strip_cta(text))
    invented = sorted(claimed - banked, key=lambda n: (len(n), n))
    if invented:
        findings.append({
            "rule": "T03_NUMBER_NOT_IN_BANK", "level": "FAIL", "id": pid,
            "detail": "the caption states %s, which %s does not carry. Either it "
                      "came from somewhere nobody checked, or the bank row is "
                      "short. Fix the row or cut the number."
                      % (", ".join(invented), fid),
        })

    # A caption can echo 1 word of the backbone by accident, so 1 word is not
    # evidence the turn survived. Longer words, and at least 2 of them.
    backbone = (fact.get("Backbone") or "").strip()
    if backbone:
        words = {w for w in re.findall(r"[a-z]{6,}", backbone.lower())}
        shared = words & set(re.findall(r"[a-z]{6,}", text.lower()))
        if words and len(shared) < 2:
            findings.append({
                "rule": "T04_NO_TURN", "level": "FAIL", "id": pid,
                "detail": "the caption reports the fact and never turns it. The "
                          "bank row has a Backbone and none of it survived into "
                          "the post.",
            })

    if "—" in text or "–" in text:
        findings.append({"rule": "T06_VOICE", "level": "FAIL", "id": pid,
                         "detail": "em dash. Not her voice."})

    return findings


def load_posts(path):
    if os.path.isdir(path):
        out = []
        for name in sorted(os.listdir(path)):
            if name.endswith(".json"):
                out.extend(load_posts(os.path.join(path, name)))
        return out
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    return data if isinstance(data, list) else [data]


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--post", required=True)
    ap.add_argument("--bank", default=DEFAULT_BANK)
    args = ap.parse_args()

    bank = load_bank(args.bank)
    posts = load_posts(args.post)

    findings = []
    for post in posts:
        findings.extend(check_post(post, bank))

    print("%d post(s) checked against %d fact(s)" % (len(posts), len(bank)))
    if not findings:
        print("trivia clean")
        return 0

    print()
    for f in findings:
        print("%-24s %-5s %s" % (f["rule"], f["level"], f["id"]))
        print("%-24s   %s" % ("", f["detail"]))

    fails = [f for f in findings if f["level"] == "FAIL"]
    print()
    print("%d finding(s), %d blocking" % (len(findings), len(fails)))
    return 1 if fails else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
