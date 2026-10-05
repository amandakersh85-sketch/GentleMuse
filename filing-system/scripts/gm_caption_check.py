#!/usr/bin/env python3
"""Refuse a queued caption that no longer matches the plan it was built from.

Amanda, 10/05: "do the same for the halloween 28."

It cannot be done the way it was done for Thanksgiving and Christmas, and
finding out why turned up something worse. On 10/04 the fact check corrected
night 10, the candy corn row, from "was invented in the 1880s by George
Renninger" to "is credited to", because History.com and National Geographic
both say the attribution is oral history and nobody knows for certain.

The loader had already written the old sentence into the queue on 10/03. 4
posts go out on 10/08 at 23:00 and 23:30 still stating it as record. The
correction reached the plan and stopped there, and no gate noticed, because
every rule in this repo reads the board's shape and not the board's words:
C01 counts posts, C05 counts minutes, C13 counts nights, C15 counts slots,
A01 opens the file. Not 1 of them compares what a post says against what it
was supposed to say.

  C17_CAPTION_STALE  a queued campaign post whose caption's opening block is
                     not the plan row's hook, fact and backbone any more

The join is the hook, which campaign-plans.csv already declares as the field a
caption opens with, so this works for any wave shipping from a plan. The
comparison is the opening block only: everything after the countdown line is a
per-platform call to action and is none of this rule's business.

A correction that does not reach the queue is not a correction. It is a 2nd
version of the truth, and the audience gets the older one.

  python3 gm_caption_check.py --queue queue.json [--campaign NAME]

Exit 0 clean, 1 a caption is stale, 2 nothing to check.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gm_board_snapshot import load_plans          # noqa: E402

# "Night 7 of 33.", "5 nights out.", anything the wave puts between the
# backbone and the call to action. The block before it is what this compares.
COUNTDOWN = re.compile(r"\n\n(?:Night \d+ of \d+\.|[^\n]{0,60}\bnights? (?:out|left)\b[^\n]{0,20})",
                       re.I)


def squash(t):
    """Whitespace and curly quotes differ between the plan and the queue."""
    t = (t or "").replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    return " ".join(t.split())


def opening(text):
    """The caption down to the countdown line, or the first 3 blocks."""
    m = COUNTDOWN.search(text or "")
    if m:
        return (text or "")[:m.start()]
    return "\n\n".join((text or "").split("\n\n")[:3])


def rows_from(items):
    out = []
    for it in items:
        d = it.get("draft") or {}
        c = d.get("content") or {}
        out.append({
            "id": str(it.get("id")),
            "when": (it.get("scheduledAt") or "")[:16],
            "platform": c.get("platform") or (d.get("target") or {}).get("targetType"),
            "account": str(d.get("accountId")),
            "text": c.get("text") or "",
        })
    return out


def check(rows, campaign=None, plans=None):
    findings, matched = [], 0
    for plan in load_plans(plans):
        name = (plan.get("Campaign") or "").strip()
        if campaign and name != campaign:
            continue
        if not os.path.exists(plan["_path"]):
            continue
        nights = json.load(open(plan["_path"], encoding="utf-8"))
        if isinstance(nights, dict):
            nights = nights.get("nights") or []
        hf = (plan.get("HookField") or "hook").strip()
        byhook = {squash(n.get(hf)): n for n in nights if n.get(hf)}
        for r in rows:
            head = squash(r["text"]).split(". ")[0] + "."
            night = None
            for hook, n in byhook.items():
                if squash(r["text"]).startswith(hook):
                    night = n
                    break
            if not night:
                continue
            matched += 1
            want = squash("%s\n\n%s\n\n%s" % (night.get(hf, ""),
                                              night.get("fact", ""),
                                              night.get("backbone", "")))
            got = squash(opening(r["text"]))
            if got != want:
                findings.append({
                    "rule": "C17_CAPTION_STALE", "id": r["id"], "when": r["when"],
                    "campaign": name, "night": night.get("night"),
                    "detail": "%s at %s on %s %s carries night %s's older text. "
                              "The plan was changed after the loader wrote this "
                              "caption, so the correction is in the plan and not "
                              "in the post." % (
                                  r["id"], r["when"], r["platform"], r["account"],
                                  night.get("night")),
                })
    findings.sort(key=lambda f: (f["when"], f["id"]))
    return findings, matched


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--campaign")
    a = ap.parse_args()
    items = json.load(open(a.queue))
    items = items["items"] if isinstance(items, dict) else items
    rows = rows_from(items)
    findings, matched = check(rows, campaign=a.campaign)
    if not matched:
        print("no queued post matches a plan hook, so nothing to compare")
        return 2
    print("%d of %d queued posts join a plan night by their opening line"
          % (matched, len(rows)))
    for f in findings:
        print("%-19s %s" % (f["rule"], f["detail"]))
    if not findings:
        print("captions clean: every queued post still says what its plan row says")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
