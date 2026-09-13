#!/usr/bin/env python3
"""
The countdown reader has to tell a countdown from a number.

On 09/11 a reschedule turned a correct "43 nights" into a wrong one and the
gate could not see it, because C04 read a column nothing filled and needed a
flag nobody passed. Fixing that surfaced the opposite failure straight away:
a reader loose enough to catch "43 nights" also catches "60 days ago" and
"free for 30 days", and a gate that cries drift on prose gets ignored.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "scripts"))
import gm_board_snapshot as S
import gm_cadence_check as C

fails = []


def want(got, expect, label):
    if got != expect:
        fails.append("%s: got %r, wanted %r" % (label, got, expect))


# The 2 real shapes, which count differently.
want(S.countdown_in("43 nights. No dark days."), "43n", "nights trailer")
want(S.countdown_in("Halloween is 43 days out."), "43d", "days out")
want(S.countdown_in("Halloween is 7 days out."), "7d", "single digit days out")
want(S.countdown_in("12 days to go."), "12d", "days to go")

# "5 nights out" is the exclusive phrasing wearing the word nights. Read as
# inclusive it counts tonight twice, which on the Samhain trailer turned a
# correct 5 into a drift finding against 6. Order in the reader decides this.
want(S.countdown_in("Samhain is 5 nights out."), "5d", "nights out is exclusive")
want(S.countdown_in("3 nights away."), "3d", "nights away is exclusive")
want(S.countdown_in("43 nights. No dark days."), "43n",
     "a bare nights count still reads as inclusive")

# Prose that states a number and a unit and is not a countdown. Every one of
# these is a real caption the first version flagged.
for prose in ("I wrote the AI guide I needed 60 days ago.",
              "5 books free forever. Not free for 30 days.",
              "written by someone who was 60 days in, not 10 years.",
              "that is 53 days of capacity spent on nothing",
              "Hold about 12 days at a time and keep everything else open."):
    want(S.countdown_in(prose), "", "prose: " + prose[:34])

# The reader hands the gate the counting convention, not just the number.
want(C.countdown_days("43n"), (43, True), "43n is inclusive")
want(C.countdown_days("43d"), (43, False), "43d is exclusive")
want(C.countdown_days("countdown12"), (12, True), "the old label form still reads")
want(C.countdown_days(""), None, "an empty cell is not a countdown")

# The campaign date lives in data, so C04 runs without anyone passing a flag.
t = C.load_target()
if t is None:
    fails.append("no live campaign in campaign-targets.csv, so C04 never runs")
else:
    want(t["TargetDate"], "2026-10-31", "the live campaign counts down to Halloween")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  countdown reader: 2 shapes read, 5 prose cases refused")
sys.exit(0)
