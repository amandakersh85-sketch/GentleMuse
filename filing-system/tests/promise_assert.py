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

LIVE_CAMPAIGNS, LIVE_STAGING, LIVE_PLANS = C.CAMPAIGNS, C.STAGING, C.PLANS

# Point the real loaders at fixtures. The live campaign ends, and a test that
# ends with it is not a test.
C.CAMPAIGNS = os.path.join(HERE, "promise.campaign.csv")
C.STAGING = os.path.join(HERE, "promise.library.csv")

fails = []


def rules_on(board):
    rows = C.load(os.path.join(HERE, board))
    return [f for f in C.check(rows)
            if f["rule"] in ("C13_PROMISE_DARK", "C14_PROMISE_FLOOD")]


def nights_in(finding):
    """The nights a C13 finding names, and not the horizon edge in its text.

    The detail says which window it judged, so the edge date appears in the
    sentence as well as in the list. Substring matching on it reads the edge as
    a dark night, which is how this helper came to exist.
    """
    return finding["detail"].rsplit(": ", 1)[1].split()


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

# A campaign that ships from a plan file. The 33 Nights loader places its own
# posts off its own plan, so none of its slugs are in the staging library and
# the library join found 11 of the campaign's rows on the 09/30 board and
# missed the rest. C13 read a run that had not skipped a night as 27 dark
# ones, on all 4 accounts, and it did it on every run for 5 nights.
C.CAMPAIGNS = os.path.join(HERE, "promise.plan.campaign.csv")
C.STAGING = os.path.join(HERE, "promise.library.csv")
C.PLANS = os.path.join(HERE, "promise.plans.csv")

pslugs, powes = C.load_campaign_plan("plan-nightly")
want("p01" in pslugs and "p10" in pslugs, True, "the plan's slugs join to the board")
want(len(pslugs), 10, "every night in the plan is in the set")
want(("facebook", "200") in powes["2026-03-01"], True,
     "an alternating account owes the night its plan books")
want(("facebook", "200") in powes.get("2026-03-02", set()), False,
     "and owes nothing on the night its plan skips")
want(("instagram", "100") in powes["2026-03-02"], True,
     "the nightly account owes every night")

# 1 a night on instagram, alternate nights on facebook, loaded 6 nights out.
# That is the promise kept, and it is what the live board looked like on 09/30
# while the gate was calling it 27 dark nights.
want(rules_on("promise.plan.clean.csv"), [],
     "a plan kept to the letter is clean")

# The horizon is not an off switch. A night inside it with nothing on it is
# still the finding it always was.
gap = rules_on("promise.plan.gap.csv")
want([f["rule"] for f in gap], ["C13_PROMISE_DARK"], "a dark night inside the horizon still fires")
want(nights_in(gap[0]), ["2026-03-04"], "and it is named, on its own")
want("instagram 100" in gap[0]["detail"], True, "on the account that owed it")

# The alternating account is charged for the nights its plan books, and only
# those. 03/05 is one of them.
alt = rules_on("promise.plan.altgap.csv")
want([f["rule"] for f in alt], ["C13_PROMISE_DARK"], "a missed alternating night fires")
want("facebook 200" in alt[0]["detail"], True, "on facebook")
want("2026-03-05" in alt[0]["detail"], True, "naming the night the plan booked")
want(nights_in(alt[0]), ["2026-03-05"], "and only that night")
for off in ("2026-03-02", "2026-03-04", "2026-03-06"):
    want(off in nights_in(alt[0]), False, "%s is a night facebook never owed" % off)

# Past the horizon nobody has loaded yet, so there is nothing to find. 03/07
# to 03/10 are empty on all 3 boards above and named on none of them.
for f in gap + alt:
    for beyond in ("2026-03-07", "2026-03-08", "2026-03-09", "2026-03-10"):
        want(beyond in nights_in(f), False, "%s is not loaded yet, so it is not dark" % beyond)

C.CAMPAIGNS = os.path.join(HERE, "promise.campaign.csv")
C.PLANS = os.path.join(HERE, "promise.plans.csv")

# And the live data still carries what the rules need. A promise recorded and
# then quietly emptied is the state the board was already in.
live = C.load_target(LIVE_CAMPAIGNS)
if live is None:
    fails.append("no live campaign in campaign-targets.csv")
else:
    for col in ("StartDate", "TargetDate", "PerNight", "Accounts", "PromisedOn"):
        if not (live.get(col) or "").strip():
            fails.append("the live campaign has no %s, so the promise rules skip it" % col)
    C.PLANS = LIVE_PLANS
    staged = C.load_campaign_slugs(live["Campaign"], LIVE_STAGING)
    planned, owed = C.load_campaign_plan(live["Campaign"])
    if not (staged or planned):
        fails.append("the live campaign %s has no slugs in staging-library.csv and no plan "
                     "in campaign-plans.csv, so the join finds nothing" % live["Campaign"])
    if planned and not owed:
        fails.append("the live plan lists no accounts per night, so C13 cannot tell a night "
                     "an account owes from 1 it does not")
    if not (live.get("LoadHorizonDays") or "").strip():
        fails.append("the live campaign has no LoadHorizonDays, so every night its loader "
                     "has not reached yet reads as a dark night")

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  promise rules: a dark night found under a full day, a flooded night found under the cap")
sys.exit(0)
