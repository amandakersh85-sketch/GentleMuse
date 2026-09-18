# The avatar pipeline, and the line it must not cross

Drafted 09/18/2026 during an away session. **A plan, not a build.** Nothing is
wired, no key was used, no video was made, nothing was spent.

Amanda, 09/18: *"I'm not replacing myself, I'm being protective of my time and
energy."*

That sentence is the whole design. It is also in tension with POS-010, which
says her face is the default and the asset. Both can be true, but only if the
avatar is confined to one tier and locked out of another. That boundary is the
plan. Everything else is plumbing.

---

## 1. The thing your own data says first

Sabrina Ramonov self-reports 250 posts a week. That is the model people point at
when they talk about this, and it is the wrong lesson to take.

`posting-cadence.csv` records the opposite result, measured on Amanda's own
account: **15 reels in one day produced 1,330 views. A single good one produced
7,726.** The same file already sets the rule at 1 reel a day, "Not 2."

So the avatar's job is not more posts. It is the same number of posts costing
fewer of her hours. If the pipeline ends with 250 posts a week, it has been
built wrong and her own numbers predicted it.

**Volume is not the win. The win is Friday and Saturday stop being consumed.**

---

## 2. Where the avatar is allowed, and where it is banned

The formats already split cleanly by whether the words are a personal claim.

| Format | Slot | Avatar? | Why |
|---|---|---|---|
| `F-OPERATOR` | Mon, Wed, Thu, Fri | **No** | This is the authority tier. THE MOVE is the value, and the value is that a real person who runs real coverage is telling you the order of operations. An avatar delivering it keeps the words and loses the reason to believe them. |
| `F-RECEIPT` | Tue, Sat, Sun | **Never** | These are first-person claims about her own week. "I turned off one of my own offers this week." An avatar saying that is a claim Amanda did not make, about events only she witnessed. That is the unverifiable-claims stop, and it is the one line that cannot be unlocked. |
| `F-SEASONAL` | the daily 10:00 FACT slot | **Yes** | A sourced fact from the Run 7 bank, already checked, already turned, already carrying its source. Nobody is testifying. The fact is true whoever says it. |
| Echo and repurpose | TikTok and Facebook reposts | **Yes** | The asset already exists and already passed its gates. This is distribution, not authorship. |

The short version: **the avatar may state what is verifiable. It may never
testify.**

That rule is not a style preference. It falls straight out of the mandatory
stops and out of POS-005, where the proof is that Amanda personally runs
coverage across multiple areas every week. Proof delivered by a synthetic
double is not proof.

---

## 3. Disclosure is already mechanical, so use it

`queue-backlog.csv` shows every TikTok payload Blotato sends already carries:

```
"isAiGenerated": false
```

The switch exists. It is set false on all 178 posts in the backlog, correctly,
because none of them were synthetic.

So disclosure does not need a policy anybody remembers. It needs a field and a
check, which is the pattern this repo has used since Run 6:

- `Delivery` gains a value: `avatar`
- Any queue row with `delivery: avatar` **must** set `isAiGenerated: true`
- A gate refuses the mismatch in either direction, the same way `Q01_LANE_LEAK`
  refuses a keyword on the wrong account

This is the smallest piece of the build and it should be written first, before a
single video exists. Building it after the first batch means the first batch is
the one that ships undisclosed.

---

## 4. The face floor does not move

`--face-floor 4` counts posts where Amanda actually filmed. An avatar post
**does not count toward it.**

If avatar posts counted, the floor would quietly change meaning from "Amanda
filmed 4 times this week" to "4 things looked like Amanda this week," and the
whole point of the floor was that filler with nothing counting it becomes the
plan. Same failure, new costume.

Concretely: a week of 4 filmed + 3 avatar passes. A week of 0 filmed + 7 avatar
fails, loudly, which is correct.

---

## 5. The pipeline, once those 3 rules exist

The feedstock already exists and this is the part worth noticing. Run 7's fact
bank produces rows that are already sourced, already turned, already tagged with
a `Delivery`, and already refused by a gate if the history is not in the bank.
That is a script queue nobody has to write.

```
holiday-fact-bank.csv / daily-fact-bank.csv
        |
        |  gm_holiday_bank.py --plan        (already built, already tested)
        v
   script rows, sourced and turned
        |
        |  gm_holiday_check.py              (already refuses an invented fact)
        v
   HeyGen API: script -> avatar video
        |
        |  NEW: gm_avatar_check.py          (disclosure + face floor + ban list)
        v
   Blotato upload, isAiGenerated true
        |
        v
   scheduled into the FACT slot only
```

Weekly cadence, batched the way filming is batched: one sitting, 7 scripts out,
7 videos back, checked, queued. It should cost her an hour of review, not a day
of production.

---

## 6. What is actually true about the tooling right now

Checked in this environment, 09/18:

- **A HeyGen key is present** in the environment. It was not used and not
  tested, because testing it is a live API call against her account.
- **The HyperFrames CLI is not installed here.** The skill pack references
  HeyGen-hosted cloud rendering, so there is a second possible route, but
  nothing is installed to run it today.
- **Blotato upload already works** and is already in daily use, so the last
  mile is not new work.

## 7. What has to happen before anything renders, in order

1. **Amanda records the avatar likeness in HeyGen.** Consent and training
   footage are hers to give and cannot be delegated. Nothing downstream matters
   until this exists.
2. **Confirm the key works and find the per-video cost.** Spending is a hard
   stop in away mode and every other mode. A cost per video and a monthly
   ceiling get agreed before the first render, not after the first invoice.
3. **Write `gm_avatar_check.py` first.** Disclosure, the format ban list, and
   the face-floor exclusion. Before any video exists.
4. **One video, reviewed by her, in the FACT slot.** Not a batch. If the first
   one does not sound like her, the fix is cheap. If the first 30 do not, it is
   not.
5. **Then batch weekly**, with the Friday review number unchanged: followers
   gained, per `posting-cadence.csv`.

---

## 8. The honest risk

The avatar will sound like her before it sounds like her. The gap shows up
worst in exactly the register that makes this brand work, which is the warm,
specific, slightly uneven way a real person says a true thing.

Mitigation is the format split above. The seasonal fact slot is the most
tolerant of a flat read, because the fact carries it. THE MOVE is the least
tolerant, because the whole claim is that a specific woman with a specific job
knows this. That is why F-OPERATOR stays hers.

**If only one rule survives this document, make it that one.**
