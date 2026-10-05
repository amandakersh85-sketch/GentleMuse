#!/usr/bin/env python3
"""
A fact nobody checked reads exactly like a fact somebody checked.

On 10/04 Amanda asked for 3 Thanksgiving facts to be rewritten and the rest
fact checked. 4 of the 26 were wrong. Night 8 said Sarah Hale campaigned 17
years when it was 36. Night 20 dated the name Pilgrims to the 1840s when
Daniel Webster said it in 1820. Night 24 described a study that used 5 items
as one that used 3, and invented a comparison it never made. Night 26 was not
a fact at all. Every row said confidence: high, because confidence is a
session's opinion of its own memory, and every row would have rendered.

What was missing is the record of the check: verified, checked, and a sources
cell that points at something. These are the rules that read them.

The gate cannot tell a true fact from a false one, and this file does not
pretend it can. It refuses a night nobody read against a source, which is the
condition all 4 errors shipped under.
"""
import datetime
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_fact_check as F

TODAY = "2026-11-10"
DAY = datetime.date.fromisoformat(TODAY)
FRESH = (DAY - datetime.timedelta(days=F.DECAY_DAYS - 10)).isoformat()
STALE = (DAY - datetime.timedelta(days=F.DECAY_DAYS + 10)).isoformat()

fails = []


def row(night, **kw):
    """A night that passes everything, before kw spoils one thing about it."""
    base = {"night": night, "date": "2026-11-20", "slug": "n%d" % night,
            "hook": "hook %d" % night, "fact": "fact %d" % night,
            "sources": "a source that points at something", "verified": "yes",
            "checked": FRESH}
    base.update(kw)
    return base


def run(items, today=TODAY):
    """The gate against a throwaway plan. Returns (codes, declared nights)."""
    tmp = tempfile.mkdtemp()
    try:
        plan = os.path.join(tmp, "plan.json")
        json.dump(items, open(plan, "w"))
        csv = os.path.join(tmp, "plans.csv")
        open(csv, "w").write(
            "Campaign,Plan,DateField,SlugField,HookField,SlotFields,Why\n"
            "fixture,%s,date,slug,hook,ig=instagram:1,a throwaway plan\n" % plan)
        plans = F.load_plans(csv)
        codes, declared = [], []
        for p in plans:
            f, d, _, err = F.check_plan(p, today)
            assert not err, err
            codes += [x["rule"] for x in f]
            declared += [(i.get("night"), st) for _, i, st in d]
        return codes, declared
    finally:
        shutil.rmtree(tmp)


def want(label, items, code=None, absent=(), declared=None, today=TODAY):
    codes, dec = run(items, today)
    if code and code not in codes:
        fails.append("%s: expected %s, got %s" % (label, code, codes or "nothing"))
    if not code and codes:
        fails.append("%s: expected a clean read, got %s" % (label, codes))
    for a in absent:
        if a in codes:
            fails.append("%s: %s fired as well, so 1 problem reads as several"
                         % (label, a))
    if declared is not None and sorted(dec) != sorted(declared):
        fails.append("%s: declared %s, expected %s" % (label, dec, declared))


# A night that was checked, says what against, and says when.
want("a verified night", [row(1)], declared=[])

# The 4 ways a night ships unchecked. "no" is the state every Thanksgiving row
# was in when it was drafted, and the one the Halloween plan has never left.
for label, bad in (("no verified cell", {}),
                   ("an empty verified cell", {"verified": ""}),
                   ("verified: no", {"verified": "no"}),
                   ("verified: soon", {"verified": "soon"})):
    item = row(1)
    item.pop("verified", None)
    item.update(bad)
    # F01 is the only finding: doing the check is what produces a source and a
    # date, so reporting all 3 would be 3 findings for 1 fix. The row is broken
    # all 3 ways on purpose, because a row broken only 1 way cannot tell
    # whether the other 2 rules were skipped or just had nothing to say.
    item.update(sources="", checked="")
    want(label, [item], "F01_FACT_UNVERIFIED",
         absent=("F02_FACT_NO_SOURCE", "F03_FACT_STALE"))

# A declared exception is still held to the rest of it. partly means checked,
# so it has a source and a date like anything else.
want("verified: partly with no sources",
     [row(1, verified="partly", sources="")], "F02_FACT_NO_SOURCE")
want("verified: partly never checked",
     [row(1, verified="partly", checked="")], "F03_FACT_STALE")

# Checked and partly confirmed, with the limit named. Passes, and is listed,
# because an exception nobody sees is an exception that spreads.
want("verified: partly", [row(1, verified="partly")], declared=[(1, "partly")])
want("verified: n/a with a reason",
     [row(1, verified="n/a, this is a framing and not a claim",
          sources="none. This is a closing thought and not a factual claim")],
     declared=[(1, "n/a")])

# A check with nothing behind it cannot be checked.
want("no sources", [row(1, sources="")], "F02_FACT_NO_SOURCE")
for empty in F.EMPTY_SOURCE:
    if empty:
        want("sources: %s" % empty, [row(1, sources=empty)], "F02_FACT_NO_SOURCE")

# The 2 shapes a sources cell comes in. The Thanksgiving plan writes prose and
# the Halloween plan writes a list of {name, url}. str([]) is "[]", which is not
# in EMPTY_SOURCE, so the first version of this gate passed an empty list.
want("sources as a list of citations",
     [row(1, sources=[{"name": "Etymonline, haunt",
                       "url": "https://www.etymonline.com/word/haunt"}])])
want("sources as an empty list", [row(1, sources=[])], "F02_FACT_NO_SOURCE")
want("sources as a list of empty citations",
     [row(1, sources=[{"name": "", "url": ""}])], "F02_FACT_NO_SOURCE")

# Facts move. CLAUDE.md sets 90 days for the trivia bank and this reads the
# same constant, so moving it moves both.
want("never checked", [row(1, checked="")], "F03_FACT_STALE")
want("checked %d days ago" % (F.DECAY_DAYS + 10),
     [row(1, checked=STALE)], "F03_FACT_STALE")
want("checked %d days ago" % (F.DECAY_DAYS - 10), [row(1, checked=FRESH)])
want("a checked cell that is not a date",
     [row(1, checked="last week")], "F03_FACT_STALE")

# Scoped to nights still to come, for the reason C13 had to be: refusing a
# night that already published fixes nothing, and 28 findings about history is
# how a gate gets switched off.
want("an unchecked night that already published",
     [row(1, date="2026-11-01", verified="no")], today="2026-11-10")
want("an unchecked night today",
     [row(1, date="2026-11-10", verified="no")], "F01_FACT_UNVERIFIED",
     today="2026-11-10")

# 1 finding per code per plan, naming the nights, rather than 1 per row.
codes, _ = run([row(n, verified="no") for n in (3, 1, 2)])
if codes.count("F01_FACT_UNVERIFIED") != 1:
    fails.append("3 unverified nights gave %d findings, expected 1 naming all 3"
                 % codes.count("F01_FACT_UNVERIFIED"))

# ------------------------------------------------- and now the live campaign
root = os.path.dirname(os.path.dirname(HERE))
for p in F.load_plans():
    name = p.get("Campaign")
    if name != "thanksgiving-nightly":
        continue
    items = json.load(open(p["_path"], encoding="utf-8"))
    if len(items) != 26:
        fails.append("the Thanksgiving plan holds %d nights, not 26" % len(items))
    for it in items:
        if not F.state(it):
            fails.append("night %s of the live Thanksgiving plan is unverified, "
                         "so a fact nobody read would render" % it.get("night"))
        if str(it.get("sources") or "").strip().lower() in F.EMPTY_SOURCE:
            fails.append("night %s of the live Thanksgiving plan names no source"
                         % it.get("night"))
    # The 4 rows that were wrong on 10/04. Their corrections are the test: a
    # plan that drifts back to any of them is a plan that fails here.
    by = {i["night"]: i for i in items}
    for night, gone, now in (
            (8, "17 years", "36"),
            (20, "1840s", "1820"),
            (24, "3 things", "once a week"),
    ):
        blob = " ".join(str(by[night].get(k) or "")
                        for k in ("hook", "fact", "backbone"))
        if gone in blob:
            fails.append("night %d is back to %r, which was checked and is wrong"
                         % (night, gone))
        if now not in blob:
            fails.append("night %d no longer carries %r, the checked figure"
                         % (night, now))
    if by[26]["confidence"] != "editorial":
        fails.append("night 26 is a closing thought, not a fact, and its "
                     "confidence column says %r" % by[26]["confidence"])
    break
else:
    fails.append("thanksgiving-nightly is not in campaign-plans.csv, so no gate "
                 "reads its facts")

# ------------------------------------- the 2 waves that run in standard time
# Central is UTC-6 from 11/01, so 6:00 PM Central is 00:00 UTC the NEXT day.
# The Thanksgiving plan was drafted with 23:00Z copied off the Halloween plan,
# where it is right because September and October are daylight time. In
# standard time that is 5:00 PM: an hour early on all 26 nights. The invariant
# is cheap to state and it was not obvious enough to get right by reading.
for campaign, count in (("thanksgiving-nightly", 26), ("christmas-nightly", 29)):
    for p in F.load_plans():
        if (p.get("Campaign") or "") != campaign:
            continue
        items = json.load(open(p["_path"], encoding="utf-8"))
        if len(items) != count:
            fails.append("%s holds %d nights, not %d" % (campaign, len(items), count))
        for it in items:
            ev = it.get("evening")
            if not ev:
                fails.append("%s night %s has no evening, so nothing says which "
                             "Central day the audience sees it"
                             % (campaign, it.get("night")))
                continue
            want_utc = (datetime.date.fromisoformat(ev)
                        + datetime.timedelta(days=1)).isoformat()
            if it["date"] != want_utc:
                fails.append("%s night %s: evening %s should land on UTC %s, "
                             "not %s" % (campaign, it.get("night"), ev,
                                         want_utc, it["date"]))
            for field, when in (("ig_tt", "00:00Z"), ("fb_yt", "00:30Z")):
                if it.get(field) != when:
                    fails.append("%s night %s %s is %r. 6:00 PM Central in "
                                 "standard time is 00:00Z the next day, so "
                                 "23:00Z would be an hour early"
                                 % (campaign, it.get("night"), field,
                                    it.get(field)))
        break
    else:
        fails.append("%s is not in campaign-plans.csv" % campaign)

# A different carol every night, which is what Amanda asked for and what the old
# 1-file-per-family schema could not express. 3 families over 29 nights is the
# Halloween failure again: 1 track under the whole run.
for p in F.load_plans():
    if (p.get("Campaign") or "") != "christmas-nightly":
        continue
    items = json.load(open(p["_path"], encoding="utf-8"))
    beds = [i.get("bed") or "" for i in items]
    if len(set(beds)) != len(items):
        fails.append("the Christmas wave has %d nights and %d distinct beds, so "
                     "some nights share a song" % (len(items), len(set(beds))))
    if not all(beds):
        fails.append("a Christmas night names no bed, so bed.mjs refuses it")
    if len({i.get("treatment") for i in items}) != 3:
        fails.append("Amanda asked for a rotation of 3 kinds of Christmas sound "
                     "and the plan uses %d"
                     % len({i.get("treatment") for i in items}))
    break

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  fact rules: an unchecked night is refused, a declared exception is listed, "
      "a published night is left alone")
sys.exit(0)
