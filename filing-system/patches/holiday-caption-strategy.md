# Patch — holiday caption strategy across the content chain

Applies Run 7 to the three skills that produce holiday content. Without this
patch the gate still catches invented history, but only after it is written.
With it, the chain cannot express an unsourced claim in the first place.

**To apply:** three edits, one per skill. Each is marked below.

---

## 1. `gentle-muse-video-factory` — new section

Add this after **"Weekly content rotation"**.

### Holiday content

When a post falls inside a holiday season, the holiday register runs on top of
the weekly rotation slot. It does not replace it. Monday in the last week of
October is still Mindset, told in spooky-warm.

**The register.** Nostalgic. A touch of Disney and whimsy. A millennial born in
1985 who watched the Disney Channel and Nickelodeon from about 1989 into the
late 1990s. That window is `1989` to `1999` and it is enforced, not suggested.
A reference to 2008 is a different generation's childhood and the gate rejects
it.

**Whimsy is allowed here because the backbone is mandatory.** The standing rule
against whimsy without weight is not suspended, it is satisfied: every holiday
post carries a fact, and every fact in the bank carries a `Backbone`, the line
that says why it matters. Fact, then turn. A post that reports the fact and
stops is a trivia account, and the gate fails it as `E09_NO_TURN`.

**The fact is data, not recall.** Holiday posts make claims about the past.
Amanda loves history and her audience will come to trust her on it, which means
a plausible invented date costs more than a weak hook. So:

- Every holiday post binds to a `FactID` from
  `filing-system/data/holiday-fact-bank.csv`, or to the string `"HOLD"`.
- **Never write a historical fact from memory, however confident.** That is the
  exact failure this run exists to stop. A fact that sounds right and a fact
  that is sourced are the same object to a writing step, which is why the check
  is mechanical.
- Every year the caption names must be in that bank row, or inside the era
  window. Decades may paraphrase: "the 1690s" is a fair way to say 1692.
- Say the fact in the post. A `FactID` that does not appear in the writing is
  decoration, and the gate fails it as `E08_FACT_NOT_TOLD`.
- Rewrite the backbone in her words. Do not paste it.

**Get the plan first, do not guess the calendar:**

```
python3 filing-system/scripts/gm_holiday_bank.py --season
python3 filing-system/scripts/gm_holiday_bank.py --plan \
    --from 2026-10-01 --to 2026-10-31 --per-holiday 5
```

Each planned row comes back with the holiday, the slot, the register, the
`FactID`, the fact, the source and the backbone. That is the whole brief.

### Holiday caption JSON

Ships alongside the render JSON, one object per post:

```json
{
  "title": "Frankenstein at 18",
  "holiday_id": "halloween",
  "post_date": "2026-10-23",
  "platform": "instagram",
  "fact_id": "HAL-004",
  "hook": "The scariest book ever written was started by an 18 year old stuck inside in bad weather.",
  "caption": "1816 was the year without a summer...",
  "cta": "Follow for more Gentle Muse resets",
  "hashtags": ["#gentlemuse", "#spookyseason", "#halloween", "#maryshelley", "#frankenstein"]
}
```

### The substitution ban

When the bank has no fact for a beat, the only legal move is:

```json
{"holiday_id": "easter", "post_date": "2026-03-30", "fact_id": "HOLD", "hook": "..."}
```

**Never borrow a fact from a neighbouring holiday, and never write one from
memory to fill the slot.** A missing fact is a research task, not a writing
decision. Say it out loud in the delivery: list the HOLD posts as facts that
still need writing and sourcing.

If a whole season would be HOLD, do not ship the batch. Ship the research list.

### No bank in context

If `holiday-fact-bank.csv` is not in context, **do not invent FactIDs and do
not write history from memory.** Write every post as `"fact_id": "HOLD"` with
the angle filled in, and open the delivery with one line: *"No fact bank in
context, so every holiday post is HOLD. Point me at
filing-system/data/holiday-fact-bank.csv and I'll bind these."*

### The gate is mandatory

```
python3 filing-system/scripts/gm_holiday_check.py --post posts/
```

`FAIL` fix and re-run. `HOLD` report the facts that need writing. Nothing goes
to Buffer, Blotato or Metricool on a FAIL. A holiday reel needs this gate and
Run 6's binding gate, both. When the tool cannot be run in the current
environment, do the same checks by hand against the bank, post by post, and say
in the delivery that the check was manual.

---

## 2. `content-coach` — rotation table

Add below the weekly rotation table:

> **Check the holiday calendar before pitching.** Run
> `python3 filing-system/scripts/gm_holiday_bank.py --season`. When a holiday
> is in season, at least 2 of the 5 ideas should be holiday ideas in that
> holiday's register, anchored to an unused `FactID` from the bank. Name the
> FactID in the idea block so the draft step inherits it. When the bank has
> nothing left for that holiday, say so and pitch the research instead of
> inventing the fact.

And add one line to the idea block format:

```
Fact anchor: [FactID from the bank, or HOLD with what needs sourcing]
```

---

## 3. `post-grader` — auto-fail checks

Add to the numbered auto-fail list:

> 7. **An unsourced historical claim.** Any date, origin story or "did you
>    know" in a holiday post that is not traceable to a row in
>    `filing-system/data/holiday-fact-bank.csv`. This is an automatic 0 on the
>    body score, not a cap at 6. A wrong fact in her voice costs more than a
>    weak hook, because the audience cannot tell and she is the one who wears
>    it.
> 8. **A nostalgia reference outside 1989 to 1999.** Wrong childhood, wrong
>    field.
> 9. **A fact with no turn.** The post reports the trivia and stops. Fact then
>    turn, every time.

And add to **Platform rules to check**:

> - Holiday posts: run `gm_holiday_check.py` before grading. It catches the
>   mechanical failures (em dashes, spelled-out numbers, hashtag count, hype,
>   unsourced years) so the read is spent on the parts a script cannot see:
>   whether the caption contradicts the fact it cites, and whether the turn
>   actually lands.

---

## What "good" looks like

Add to the video factory's closing list:

- Every holiday claim bound to a `FactID` that exists in the bank, with the
  fact actually said in the writing
- Every year in the copy sourced by that row, or inside 1989 to 1999
- The backbone rewritten in her words, never pasted, never omitted
- Missing facts shipped as `HOLD` and listed as research, never invented and
  never borrowed from another holiday
- The holiday gate run, and passing, before the batch is called done
