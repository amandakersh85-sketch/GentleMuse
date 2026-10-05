#!/usr/bin/env python3
"""Refuse a campaign night whose fact nobody checked.

Amanda, 10/04: "rewrite 13, 22 and 23 and don't forget to fact check the
other ones."

She was right to ask, and the asking is the problem. 4 of the 26 Thanksgiving
rows were wrong when they were read against sources on 10/04:

  night 8   said Sarah Hale campaigned for 17 years. It was 36, from 1827.
            17 is the letter campaign alone, from 1846.
  night 24  said writing down 3 things beats thinking them. The study used 5
            things and never compared writing against thinking. The real
            finding is that once a week beats 3 times a week.
  night 20  dated the name Pilgrims to the 1840s. Daniel Webster said it at
            the 1820 bicentennial.
  night 26  was not a fact at all. It is a closing thought, and it was
            sitting in the confidence column as high.

Every one of those would have rendered and published. plan.json carried a
confidence column, which is a session's opinion of its own memory, and
halloween-33/approval/plan.json has no record of checking at all: 20 nights
published off it and nothing anywhere says what was read.

Guidance is not the fix here. A session that believes 17 is right will not be
saved by being told to check, because it already thinks it did. The fix is
the missing field and the gate that refuses without it.

  F01_FACT_UNVERIFIED  a night still to come whose verified cell is not yes,
                       not partly, and not an n/a that says why
  F02_FACT_NO_SOURCE   nothing in the sources cell, so there is no way to
                       check the check
  F03_FACT_STALE       checked longer ago than DECAY_DAYS, or never

A reused night is checked like any other. Its body text lives in an already
rendered reel, but campaign-plans.csv says the hook is the line the caption
opens with, so the hook is a published claim and gets read against a source
like everything else. "Reused" is not an exemption, or it becomes the way an
unchecked fact ships.

A row that fails F01 is not also reported under F02 or F03. Doing the check
is what produces a source and a date, so 1 fix closes all 3 and 3 findings
would be noise.

What this cannot do: tell a true fact from a false one. Nothing in a file can.
It refuses a night nobody read against a source, which is the condition all 4
errors above shipped under, and it leaves the reading to whoever does it.

Scoped to nights on or after today, for the reason C13 had to be: a night
already published cannot be fixed by refusing it, and 28 findings about
history is how a gate gets switched off. Past nights are counted on 1 line
instead.

verified: partly and verified: n/a both pass and are both listed, because an
exception that nobody sees is an exception that spreads. partly means checked
and partly confirmed, with the limit written into sources. n/a means not a
factual claim.

  python3 gm_fact_check.py [--plans FILE] [--campaign NAME] [--today YYYY-MM-DD]

Exit 0 clean, 1 a night is unverified, 2 no plan to check.
"""
import argparse, datetime, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gm_board_snapshot import load_plans, PLANS          # noqa: E402
from gm_trivia_bank import DECAY_DAYS, EMPTY_SOURCE      # noqa: E402

# yes is checked and confirmed. partly is checked and partly confirmed, with
# the limit named in sources. n/a is not a factual claim. Anything else,
# including a blank and including "no", is a night that cannot ship.
CLEARED = ("yes",)
DECLARED = ("partly", "n/a")


def state(row):
    """yes, partly, n/a or empty. n/a may carry its reason after a comma."""
    v = str(row.get("verified") or "").strip().lower()
    if v in CLEARED:
        return "yes"
    for d in DECLARED:
        if v == d or v.startswith(d + ","):
            return d
    return ""


def source_text(row):
    """The sources cell flattened, whatever shape it is in.

    The Thanksgiving plan writes prose and the Halloween plan writes a list of
    {name, url}. str() on an empty list gives "[]", which is not in
    EMPTY_SOURCE, so the first version of this gate passed a row whose sources
    list was empty. Both shapes normalise here instead.
    """
    src = row.get("sources")
    if isinstance(src, (list, tuple)):
        parts = []
        for s in src:
            if isinstance(s, dict):
                parts += [str(v) for v in s.values()]
            else:
                parts.append(str(s))
        src = " ".join(parts)
    return str(src or "").strip()


def rows_from(plan, items, today):
    """Plan rows split into the nights still to come and the ones gone by."""
    field = (plan.get("DateField") or "date").strip()
    ahead, past = [], []
    for it in items:
        day = str(it.get(field) or "").strip()
        (ahead if day >= today else past).append(it)
    return ahead, past


def nights(items, field="night"):
    return ", ".join(str(i.get(field) or "?") for i in items)


def check_plan(plan, today):
    """Findings for 1 campaign plan, plus what passed by declaration."""
    path = plan["_path"]
    if not os.path.exists(path):
        return [], [], 0, "plan file is missing: %s" % plan.get("Plan")
    items = json.load(open(path, encoding="utf-8"))
    if isinstance(items, dict) and "nights" in items:
        items = items["nights"]
    ahead, past = rows_from(plan, items, today)
    name = plan.get("Campaign") or os.path.basename(path)

    unverified, unsourced, stale, declared = [], [], [], []
    for it in ahead:
        st = state(it)
        if not st:
            unverified.append(it)
        else:
            if st != "yes":
                declared.append((name, it, st))
            src = source_text(it)
            if src.lower() in EMPTY_SOURCE:
                unsourced.append(it)
            when = str(it.get("checked") or "").strip()
            try:
                age = (datetime.date.fromisoformat(today)
                       - datetime.date.fromisoformat(when)).days
            except ValueError:
                age = None
            if age is None or age > DECAY_DAYS:
                stale.append(it)

    findings = []
    for rule, bad, detail in (
        ("F01_FACT_UNVERIFIED", unverified,
         "%s: %d of %d nights still to come have no verified cell, so nothing "
         "says the fact was read against a source. Nights %s"),
        ("F02_FACT_NO_SOURCE", unsourced,
         "%s: %d of %d nights still to come name no source, so the check "
         "cannot be checked. Nights %s"),
        ("F03_FACT_STALE", stale,
         "%s: %d of %d nights still to come were last checked more than "
         + str(DECAY_DAYS) + " days ago or never. Nights %s"),
    ):
        if bad:
            findings.append({
                "rule": rule, "campaign": name,
                "detail": detail % (name, len(bad), len(ahead), nights(bad)),
            })
    return findings, declared, len(past), None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", default=PLANS)
    ap.add_argument("--campaign", help="check only this campaign")
    ap.add_argument("--today", default=datetime.date.today().isoformat())
    a = ap.parse_args()

    plans = load_plans(a.plans)
    if a.campaign:
        plans = [p for p in plans if (p.get("Campaign") or "") == a.campaign]
    if not plans:
        print("no campaign plan to check")
        return 2

    findings, declared, past, notes = [], [], 0, []
    for p in plans:
        f, d, n, err = check_plan(p, a.today)
        if err:
            notes.append(err)
            continue
        findings += f
        declared += d
        past += n

    print("%d plan%s, %d night%s already gone by" % (
        len(plans), "" if len(plans) == 1 else "s",
        past, "" if past == 1 else "s"))
    for n in notes:
        print("plan missing: %s" % n)
    for d in declared:
        name, it, st = d
        print("declared %-7s %s night %s: %s" % (
            st, name, it.get("night"), it.get("hook") or it.get("slug")))
    for f in findings:
        print("%-20s %s" % (f["rule"], f["detail"]))
    if notes:
        return 1
    if not findings:
        print("facts clean: every night still to come was read against a source")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
