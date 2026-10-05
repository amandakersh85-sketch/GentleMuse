#!/usr/bin/env python3
"""Write a wave's captions out in the shape a person can read and approve.

plan.json is what the gates and the loader read. It is not what anybody wants
to read 29 facts out of. Amanda, 10/04: "would you ever give me the list of
Christmas texts to check?" That should have shipped with the draft.

This generates the sheet from the plan, so the 2 cannot drift. It was inline
python twice before, once per wave, which is how a third copy gets written with
1 field spelled differently.

  python3 gm_caption_sheet.py <campaign> [--out FILE]

Default output is <plan's directory>/captions-to-check.md.
"""
import argparse
import datetime
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gm_board_snapshot import load_plans          # noqa: E402

PREAMBLE = """Redrafted 10/05 on Amanda's notes: tighten it, name the detail rather than
gesturing at it, and make the closing line the ribbon on the gift. The facts
themselves are unchanged. She approved those.

Every fact was read against the sources below before it was written. Check them
anyway: the gate records that a check happened, it cannot tell a true fact from
a false one.

The `hook` is the line the caption opens with. The `fact` is the body. The
`backbone` is the closing line. Approve, change or cut per night."""


def sheet(title, nights):
    out = ["# %s" % title, "", PREAMBLE, ""]
    for n in nights:
        day = n.get("evening") or n.get("date")
        when = datetime.date.fromisoformat(day).strftime("%a %m/%d")
        era = n.get("era") or ""
        out += ["---", "",
                "## %s. %s, %s" % (n.get("night"), when,
                                   era if era and era != "none" else "no date"),
                "", "**%s**" % n.get("hook", ""), "",
                n.get("fact", ""), "",
                "*%s*" % n.get("backbone", ""), ""]
        if n.get("bed_desc"):
            out += ["Sound: %s" % n["bed_desc"], ""]
        src = n.get("sources")
        if isinstance(src, (list, tuple)):
            for s in src:
                if isinstance(s, dict):
                    out.append("- [%s](%s)" % (s.get("name", ""), s.get("url", "")))
                else:
                    out.append("- %s" % s)
        elif src:
            out.append("- %s" % src)
        out.append("")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("campaign")
    ap.add_argument("--out")
    ap.add_argument("--title")
    a = ap.parse_args()

    for row in load_plans():
        if (row.get("Campaign") or "").strip() != a.campaign:
            continue
        import json
        nights = json.load(open(row["_path"], encoding="utf-8"))
        if isinstance(nights, dict):
            nights = nights.get("nights") or []
        title = a.title or "%s, the captions to check" % a.campaign
        out = a.out or os.path.join(os.path.dirname(row["_path"]),
                                    "captions-to-check.md")
        open(out, "w", encoding="utf-8").write(sheet(title, nights))
        print("%s: %d nights -> %s" % (a.campaign, len(nights), out))
        return 0
    print("no campaign called %r in campaign-plans.csv" % a.campaign)
    return 2


if __name__ == "__main__":
    sys.exit(main())
