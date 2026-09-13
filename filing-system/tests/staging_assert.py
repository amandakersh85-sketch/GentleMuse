#!/usr/bin/env python3
"""
A caption's line breaks have to be line breaks.

On 09/13, 84 of 256 rows in staging-library.csv stored their paragraph breaks
as the 2 characters backslash and n. Posting one verbatim would have put
backslash-n into a live caption, which is the visible half of the problem.

The invisible half was worse. gm_keyword_check scans for the ask with a word
boundary, and in "...for children.\\nComment SEASONAL" the n and the C are both
word characters, so no boundary exists and the ask never matched. 10 YouTube
posts carrying a keyword YouTube has no listener for came back clean. The gate
was not wrong about the rule; it never saw the text.

So there are 2 guards, because either alone would have let this through:
the data is checked here, and the gate normalises before it scans.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_keyword_check as K

fails = []

rows = list(csv.DictReader(open(os.path.join(HERE, "..", "data",
                                             "staging-library.csv"),
                                newline="", encoding="utf-8")))
bad = [r["Slug"] for r in rows if "\\n" in (r["Text"] or "")]
if bad:
    fails.append("%d staged row(s) still store a literal backslash-n: %s"
                 % (len(bad), ", ".join(sorted(set(bad))[:6])))

# The gate reads the ask through escaped whitespace rather than past it.
escaped = ("Goosebumps was dismissed.\\n\\nBooks in 1992."
           "\\n\\nComment SEASONAL and I'll send you the weekly note.")
if "SEASONAL" not in K.asks(escaped):
    fails.append("the gate cannot see an ask whose line breaks are escaped, "
                 "so malformed whitespace switches it off")

# And still reads a normal one.
if "SEASONAL" not in K.asks("Books in 1992.\n\nComment SEASONAL and I'll send it."):
    fails.append("the gate stopped reading a normally formatted ask")

# A number glued to a word is still not a keyword.
if K.asks("I wrote it 60 days ago and commented nothing"):
    fails.append("the gate invented an ask out of prose")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  staging: %d rows, 0 escaped; gate reads through escaped whitespace"
      % len(rows))
sys.exit(0)
