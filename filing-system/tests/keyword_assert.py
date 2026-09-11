#!/usr/bin/env python3
"""
The registry has to stay a complete copy, not a partial one.

The failure this guards is not a wrong row. It is a missing row that reads
exactly like a correct "no". On 09/11 keyword-audit.csv held 13 of 57
automations, so every Target product keyword answered "not live" off the repo.
A partial file is worse than no file, because it looks like an answer.

These assertions are about shape, not about any one keyword: pairs, kinds,
destinations, and the invariant that nothing in the registry points at an
account that has no listener.
"""
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

rows = list(csv.DictReader(open(os.path.join(DATA, "keyword-registry.csv"),
                                newline="", encoding="utf-8")))
cta = list(csv.DictReader(open(os.path.join(DATA, "platform-cta.csv"),
                               newline="", encoding="utf-8")))

fails = []


def want(cond, msg):
    if not cond:
        fails.append(msg)


live = [r for r in rows if r["Active"] == "yes"]

want(len(rows) >= 55,
     "the registry has %d rows. Blotato had 57 automations on 09/11, so a "
     "much smaller file means it went stale again." % len(rows))

# Every row has to name an account that actually listens. A keyword row on
# TikTok would be the same class of wrong as the stale file: a plausible
# answer nobody can act on.
listens = {r["Platform"] for r in cta if r["KeywordWorks"] != "no"}
for r in live:
    want(r["Platform"] in listens,
         "%s is registered on %s, which has no automation at all"
         % (r["Keyword"], r["Platform"]))

# A product keyword with no destination cannot deliver anything.
for r in live:
    if r["Kind"] in ("product", "own-product", "magnet"):
        want(r["Destination"].startswith("http"),
             "%s on %s has no destination URL" % (r["Keyword"], r["AccountId"]))

# BROW is the worked example. If it ever falls out of the file, the question
# that produced this gate gets the wrong answer again.
brow = [r for r in live if r["Keyword"] == "BROW"]
want(len(brow) == 2,
     "BROW should be live on 2 accounts, found %d" % len(brow))
want({r["Platform"] for r in brow} == {"instagram", "facebook"},
     "BROW should be live on instagram and facebook")
want(all("83347380" in r["Destination"] for r in brow),
     "BROW should point at the NYX brow gel SKU 83347380")

# The 2 automations whose links are known dead have to stay marked. An
# unmarked broken link is a DM that lands on a storefront and looks fine.
broken = {r["Keyword"] for r in live if r["Note"].startswith("BROKEN")}
want("FALLFIT" in broken, "FALLFIT has a dead SKU and must stay marked BROKEN")
want("MASK" in broken, "MASK has no SKU and must stay marked BROKEN")

# The Cesa account answers 3 keywords and nothing else. Registering a 4th
# there without adding the automation is how a dead CTA ships.
cesa = {r["Keyword"] for r in live if r["AccountId"] == "65540"}
want(cesa == {"CONSIDER", "CESA", "SEASONAL"},
     "cesasgoldenyears should answer exactly CONSIDER CESA SEASONAL, found %s"
     % sorted(cesa))

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  registry: %d rows, %d live" % (len(rows), len(live)))
sys.exit(0)
