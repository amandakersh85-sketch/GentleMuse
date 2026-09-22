#!/usr/bin/env python3
"""
A promise nobody wrote down is a promise no gate can keep.

On 09/19/2026 Amanda announced the nightly run on Instagram: 1 true thing
about the season every night, 43 nights, no dark days. The board then went
dark on 26 of those 43 nights and every existing rule passed it, because a
night holding 4 Club Target posts and no Halloween fact is not starved, not
silent, not a collision and not a repeat. Nothing in the data said the
campaign owed that night anything.

Two columns fixed that. campaign-targets.csv now carries the start date, the
accounts and the 1 a night. staging-library.csv now says which campaign a
slug belongs to. These are the rules that read them.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_cadence_check as C

LIVE_CAMPAIGNS, LIVE_STAGING = C.CAMPAIGNS, C.STAGING

# Point the real loaders at fixtures. The live campaign ends, and a test that
# ends with it is not a test.
C.CAMPAIGNS = os.path.join(HERE, "promise.campaign.csv")
C.STAGING = os.path.join(HERE, "promise.library.csv")

fails = []


def rules_on(board):
    rows = C.load(os.path.join(HERE, board))
    return [f for f in C.check(rows)
            if f["rule"] in ("C13_PROMISE_DARK", "C14_PROMISE_FLOOD")]


def want(got, expect, label):
    if got != expect:
        fails.append("%s: got %r, wanted %r" % (label, got, expect))


# The loaders read what was actually added, not a stub of it.
camp = C.load_target()
want(camp is not None and camp["Campaign"], "test-nightly", "the campaign loads")
want(camp["PerNight"], "1", "the promise carries its own per night number")
want(C.campaign_accounts("instagram:45886|facebook:30840"),
     [("instagram", "45886"), ("facebook", "30840")], "accounts parse")

slugs = C.load_campaign_slugs("test-nightly")
want("alpha" in slugs, True, "a campaign slug is in the set")
want("outsider" in slugs, False, "another campaign's slug is not")
# Plates fold. The library holds nbc-crt; the board writes nbc.
want("nbc" in slugs, True, "a plate folds to its fact before the join")

# 1 a night, every night, is the promise kept. Neither rule fires.
want(rules_on("promise.clean.csv"), [], "a night a night is clean")

# 03/03 carries a post, so no existing rule sees anything wrong with it. It
# is a post from a different campaign, which is exactly the case the whole
# board was full of.
dark = rules_on("promise.dark.csv")
want([f["rule"] for f in dark], ["C13_PROMISE_DARK"], "a covered but campaign-less night")
if dark:
    want("2026-03-03" in dark[0]["detail"], True, "the dark night is named")
    want("where the promise was published" in dark[0]["detail"], True,
         "the account the words went out on is called out")

# 3 in 1 night is not generosity. It is 2 nights taken off the end, which is
# what 09/24 did to the real run.
flood = rules_on("promise.flood.csv")
want([f["rule"] for f in flood], ["C14_PROMISE_FLOOD"], "3 on 1 night")
if flood:
    want(flood[0]["day"], "2026-03-01", "the flooded night is named")
    want(sorted(flood[0]["ids"]), ["1", "2", "3"], "every post in the pile is named")

# The queue's own first day is a partial night. Its early slots have already
# published and left the queue, so judging it reports a dark night every time
# the gate runs. promise.today.csv opens on 03/02, mid campaign, with nothing
# from the campaign on 03/02 or on 03/03.
today = rules_on("promise.today.csv")
want([f["rule"] for f in today], ["C13_PROMISE_DARK"], "only the real dark night")
if today:
    want("2026-03-01" in today[0]["detail"], False, "a night before the queue is not judged")
    want("2026-03-02" in today[0]["detail"], False, "the night the queue opens on is not judged")
    want("2026-03-03" in today[0]["detail"], True, "the first whole night in the queue is")

# Scope. The 2 rules answer for a board that carries this campaign and reaches
# into its run. Everything else is a different board, and reading it as 5 dark
# nights would bury the real finding under noise on every fixture in the suite.
want(rules_on("promise.elsewhere.csv"), [],
     "a board that ends before the campaign starts is not dark nights")
want(rules_on("promise.nofacts.csv"), [],
     "a board with no fact column is C10's finding, not this one's")

# And the live data still carries what the rules need. A promise recorded and
# then quietly emptied is the state the board was already in.
live = C.load_target(LIVE_CAMPAIGNS)
if live is None:
    fails.append("no live campaign in campaign-targets.csv")
else:
    for col in ("StartDate", "TargetDate", "PerNight", "Accounts", "PromisedOn"):
        if not (live.get(col) or "").strip():
            fails.append("the live campaign has no %s, so the promise rules skip it" % col)
    if not C.load_campaign_slugs(live["Campaign"], LIVE_STAGING):
        fails.append("no row in staging-library.csv is marked %s, so the join finds nothing"
                     % live["Campaign"])

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  promise rules: a dark night found under a full day, a flooded night found under the cap")
sys.exit(0)
