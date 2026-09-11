#!/usr/bin/env python3
"""
gm_board_snapshot.py - turn a Blotato queue dump into a board the gate can read.

gm_cadence_check.py needs a fact column, and the queue does not carry one. It
carries a caption. This is the step in between: it reads a queue dump, finds
the fact each post is about, and writes the snapshot CSV.

Two things it will not do.

It matches on what the caption *opens* with, not the whole caption. The CTA,
the link and the hashtags are identical across every post in a lane and drown
the 1 part that says what the post is about. Matching whole captions scored a
correct pair at 0.21 on the 09/08 board, low enough to look like no match at
all, and it split Hocus Pocus into 2 facts, which let a real repeat through.

And when nothing in the register covers a row, it leaves the fact empty rather
than guessing. C10_FACT_UNLABELLED then reports the row. A guess that looks
like an answer is worse than a blank, because the blank gets filled and the
guess gets trusted.

4 plates of 1 fact are 1 fact. A different plate is a different reel and the
same thing said twice, and the person scrolling sees the fact.

Usage:
  gm_board_snapshot.py <queue-dump.json> <out.csv> [--register staging-library.csv]

The queue dump is the items array from blotato_list_schedules, or an object
with one.
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(HERE), "data")
REGISTER = os.path.join(DATA, "staging-library.csv")

# Below this, the opening lines do not agree well enough to call it the same
# fact. Measured on the 09/08 board: real matches sat at 0.69 and up, the
# nearest wrong one at 0.50.
THRESHOLD = 0.65

# Plates of one fact. nbc-crt and nbc-oak are 2 reels and 1 fact.
FAMILY = {
    "nbc-cemetery": "nbc", "nbc-crt": "nbc", "nbc-oak": "nbc", "nbc-theater": "nbc",
    "gb-bike": "gb", "gb-fort": "gb", "gb-rack": "gb", "gb-paperbacks": "gb",
    "mare-bedroom": "mare", "mare-nightstand": "mare",
    "mare-rocking": "mare", "mare-weighted": "mare",
}

STOP = set("""a an the and or but if then so of to in on at for with from by as is are was were be been
being it its this that these those you your yours i me my mine we our ours they them their he she his her
not no yes do does did what when where who whom how why all any each more most other some such only own
same than too very can will just dont don t s re ve ll m about after before because into over under again
once here there out up down off then them one two three four five six seven eight nine ten first still
never always got get make made""".split())


def toks(text):
    t = (text or "").lower()
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"#\w+", " ", t)
    t = re.sub(r"[^a-z0-9]+", " ", t)
    return [w for w in t.split() if w not in STOP and len(w) > 2]


# A campaign trailer states how far out it is, and that number stops being
# true the moment the post is moved. On 09/11 a reschedule to fix a slot
# collision silently turned a correct "43 nights" into a wrong one, and C04
# could not see it because the rule read a column the snapshot left empty.
#
# The board uses 2 phrasings and they count differently, which is why a bare
# "\d+ days" is not enough to go on:
#   "43 nights. No dark days."   tonight is night 1, so inclusive
#   "Halloween is 43 days out."  days remaining, so exclusive
# Everything else that says a number and a day is prose, not a countdown:
# "60 days ago", "free for 30 days", "hold about 12 days at a time".
NIGHTS   = re.compile(r"\b(\d{1,3})\s+nights?\b", re.I)
DAYS_OUT = re.compile(r"\b(?:is\s+)?(\d{1,3})\s+days?\s+(?:out|to go|left)\b", re.I)


def countdown_in(text):
    """The countdown a caption states, as <number><n for nights, d for days>."""
    text = text or ""
    m = NIGHTS.search(text)
    if m:
        return m.group(1) + "n"
    m = DAYS_OUT.search(text)
    if m:
        return m.group(1) + "d"
    return ""


def opening(text):
    """The first 3 lines. That is where the fact is stated."""
    return set(toks(" ".join((text or "").strip().split("\n")[:3])))


def containment(a, b):
    return len(a & b) / max(1, min(len(a), len(b)))


def load_roster(path=None):
    """The channels this board is supposed to cover, from channel-rules.csv.

    Written onto every row so the gate can check for a channel that is
    missing entirely. Nothing else can: every other rule groups the rows it
    was handed, and a silent channel has none.
    """
    out = []
    try:
        with open(path or os.path.join(DATA, "channel-rules.csv"), newline="") as fh:
            for r in csv.DictReader(fh):
                ch = (r.get("Channel") or "").strip().lower()
                try:
                    if ch and int(r["MinPerDay"]) > 0:
                        out.append(ch)
                except (KeyError, ValueError):
                    continue
    except OSError:
        pass
    return "|".join(sorted(out))


def load_register(path=REGISTER):
    """Slug -> the openings of every caption written for it."""
    reg = defaultdict(list)
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if not (r.get("MediaUrl") or "").strip().endswith(".mp4"):
                continue
            reg[r["Slug"].strip()].append(opening(r["Text"].replace("\\n", "\n")))
    return reg


def load_queue(path):
    d = json.load(open(path))
    items = d["items"] if isinstance(d, dict) else d
    rows = []
    for it in items:
        draft = it["draft"]
        content = draft["content"]
        rows.append({
            "id": it["id"],
            "when": it["scheduledAt"][:16],
            "platform": content.get("platform") or draft["target"].get("targetType"),
            "account": str(draft.get("accountId")),
            "text": content.get("text") or "",
        })
    return rows


def resolve(rows, register):
    out = []
    unresolved = 0
    for r in rows:
        head = opening(r["text"])
        best = (0.0, "")
        for slug, openings in register.items():
            score = max(containment(head, o) for o in openings)
            if score > best[0]:
                best = (score, slug)
        if best[0] >= THRESHOLD:
            fact, guess = FAMILY.get(best[1], best[1]), ""
        else:
            unresolved += 1
            fact = ""
            first = " ".join(r["text"].strip().split("\n")[0].split()[:7]).lower()
            guess = re.sub(r"[^a-z0-9]+", "-", first).strip("-") or ("row-" + r["id"])
        out.append([r["id"], r["when"], countdown_in(r["text"]), r["platform"],
                    r["account"], fact, guess])
    out.sort(key=lambda x: x[1])
    return out, unresolved


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    register = REGISTER
    for i, a in enumerate(argv):
        if a == "--register" and i + 1 < len(argv):
            register = argv[i + 1]

    rows = load_queue(args[0])
    out, unresolved = resolve(rows, load_register(register))

    tmp = args[1] + ".tmp"
    with open(tmp, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "postTimeUTC", "countdown", "platform", "accountId",
                    "fact", "factGuess", "roster"])
        roster = load_roster()
        w.writerows([row + [roster] for row in out])
    os.replace(tmp, args[1])

    print("%d posts: %d carry a fact from the register, %d have none"
          % (len(out), len(out) - unresolved, unresolved))
    if unresolved:
        print("The %d without one are not checked for repeats. C10 will say so."
              % unresolved)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
