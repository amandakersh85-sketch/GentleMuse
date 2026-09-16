#!/usr/bin/env python3
"""
A caption that states a countdown is not fill material.

On 09/16 gm_fill_plan proposed the Samhain trailer, which says "Samhain is 5
nights out", for 09/24, 09/28 and 10/02. It is true on 10/26 and nowhere else,
so all 3 would have published a countdown wrong by a month. The plan was not
wrong about spacing or about the call to action; it simply had no idea the
caption pinned itself to a date.

C04 would have caught it on the next nightly, after it was already scheduled.
This catches it before it is proposed, which is the cheaper place.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_fill_plan as F

fails = []


def want(cond, msg):
    if not cond:
        fails.append(msg)


SAMHAIN = ("Samhain is 5 nights out.\n\nThe night the year turns.\n\n"
           "Comment SEASONAL and I'll send you the weekly note.")
NIGHTS = "43 nights. No dark days.\n\nComment SEASONAL and I'll send it."
PLAIN = ("Jack o lanterns were turnips.\n\nThe ritual mattered.\n\n"
         "Comment SEASONAL and I'll send you the weekly note.")

# 5 nights out from Halloween is 10/26, exclusive, and nothing else.
want(F.true_on(SAMHAIN, "2026-10-26"), "the Samhain trailer was refused on its own date")
for d in ("2026-09-24", "2026-09-28", "2026-10-02", "2026-10-25", "2026-10-27"):
    want(not F.true_on(SAMHAIN, d),
         "the Samhain trailer was allowed on %s, where it is false" % d)

# 43 nights counts tonight, so it is true on 09/19 and not on 09/20.
want(F.true_on(NIGHTS, "2026-09-19"), "a nights trailer was refused on its own date")
want(not F.true_on(NIGHTS, "2026-09-20"), "a nights trailer was allowed a day late")

# A caption with no countdown is true whenever.
for d in ("2026-09-24", "2026-10-26", "2026-10-31"):
    want(F.true_on(PLAIN, d), "a caption with no countdown was held on %s" % d)

# The inventory itself must drop them rather than leaving it to the caller.
inv = F.load_inventory("2026-09-24")
for slug in ("countdown-ig", "countdown-tt"):
    want(slug not in inv, "%s reached the inventory for a day it is false on" % slug)
inv26 = F.load_inventory("2026-10-26")
want(any(s in inv26 for s in ("countdown-ig", "countdown-tt")),
     "the countdown reels were held on 10/26, the 1 day they are true")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  fill plan: date-locked captions held on 5 wrong days, allowed on 2 right ones")
sys.exit(0)
