#!/usr/bin/env python3
"""
A correction that does not reach the queue is a 2nd version of the truth.

On 10/04 the fact check corrected night 10 of the Halloween run from "candy
corn was invented in the 1880s by George Renninger" to "is credited to",
because the attribution is oral history and the sources say so. The loader had
written the old sentence into the queue the day before. 4 posts were going out
on 10/08 still stating it as record, and no gate noticed: every rule in this
repo reads the board's shape and not its words.

These are the rules that read the words.
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_caption_check as C

fails = []


def want(got, exp, label):
    if got != exp:
        fails.append("%s: got %r, expected %r" % (label, got, exp))


# The apostrophes are load bearing. The plan writes a straight quote, the queue
# often comes back with a curly one, and without normalising that every caption
# in the run reads as drift.
NIGHT = {"night": 10, "date": "2026-10-08", "slug": "candy-corn",
         "hook": "Candy corn began in the 1880s.",
         "fact": "It is credited to Renninger on oral history, not the maker's "
                 "own record.",
         "backbone": "Nobody's sure, and the sources say so."}

CTA = "\n\nNight 10 of 33.\n\nComment SEASONAL and I'll send you the note."


def post(pid, text):
    return {"id": pid, "scheduledAt": "2026-10-08T23:00:00.000Z",
            "draft": {"accountId": "45886",
                      "target": {"targetType": "instagram"},
                      "content": {"platform": "instagram", "text": text}}}


def run(nights, items):
    tmp = tempfile.mkdtemp()
    plan = os.path.join(tmp, "plan.json")
    json.dump(nights, open(plan, "w"))
    csv = os.path.join(tmp, "plans.csv")
    open(csv, "w").write(
        "Campaign,Plan,DateField,SlugField,HookField,SlotFields,Why\n"
        "fixture,%s,date,slug,hook,ig=instagram:1,a throwaway plan\n" % plan)
    return C.check(C.rows_from(items), plans=csv)


def caption(n):
    return "%s\n\n%s\n\n%s" % (n["hook"], n["fact"], n["backbone"])


# The caption the loader would write from this plan row, plus the call to
# action that every platform appends and that this rule ignores.
fresh, matched = run([NIGHT], [post("p1", caption(NIGHT) + CTA)])
want([f["rule"] for f in fresh], [], "a caption matching its plan row is clean")
want(matched, 1, "and it joined to the night by its opening line")

# The 10/04 case: the plan was corrected after the caption was written.
old = dict(NIGHT, fact="It was invented by George Renninger.")
stale, _ = run([NIGHT], [post("p2", caption(old) + CTA)])
want([f["rule"] for f in stale], ["C17_CAPTION_STALE"],
     "a caption built before a correction is reported")
want(stale[0]["night"], 10, "and the finding names the night")

# Each field on its own, because a redraft can touch any 1 of the 3.
for field, label in (("fact", "a reworded fact"),
                     ("backbone", "a reworded closing line")):
    drifted = dict(NIGHT)
    drifted[field] = "something else entirely."
    found, _ = run([NIGHT], [post("p3", caption(drifted) + CTA)])
    want([f["rule"] for f in found], ["C17_CAPTION_STALE"], "%s is reported" % label)

# A different hook is a different night, not a stale caption. The rule must not
# claim a post it cannot identify.
other, matched2 = run([NIGHT], [post("p4", "An unrelated post about a dog.\n\nBody.")])
want([f["rule"] for f in other], [], "a post that is not this campaign's is skipped")
want(matched2, 0, "and is not counted as matched")

# The call to action differs per platform and changes often. It is not the
# rule's business, or every platform variant reads as a drift.
for cta in ("\n\nNight 10 of 33.\n\nFollow for the real one. Link in bio.",
            "\n\nNight 10 of 33.\n\nSubscribe. #gentlemuse #shorts",
            "\n\nNight 10 of 33."):
    ok, _ = run([NIGHT], [post("p5", caption(NIGHT) + cta)])
    want([f["rule"] for f in ok], [], "the call to action is ignored")

# Curly quotes and rewrapped lines are not drift either. The loader and the
# plan disagree about whitespace constantly.
loose = caption(NIGHT).replace("'", "’").replace(". ", ".  ") + CTA
assert "\u2019" in loose, "the fixture must carry a curly quote or this proves nothing"
ok, _ = run([NIGHT], [post("p6", loose)])
want([f["rule"] for f in ok], [], "quote style and spacing are not drift")

# ------------------------------------------------------- and the live board
plans = [p for p in C.load_plans() if p["Campaign"] == "halloween-nightly"]
if not plans:
    fails.append("halloween-nightly is not in campaign-plans.csv, so no gate "
                 "compares its captions to its plan")
else:
    nights = json.load(open(plans[0]["_path"], encoding="utf-8"))
    hooks = [n["hook"] for n in nights if n.get("hook")]
    if len(set(hooks)) != len(hooks):
        fails.append("2 Halloween nights share an opening line, so the queue "
                     "cannot be joined to the plan by hook")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  caption rules: a corrected plan that never reached the queue is found, "
      "and a per-platform call to action is not mistaken for drift")
sys.exit(0)
