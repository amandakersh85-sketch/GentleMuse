# GentleMuse — house rules for any AI working in this repo

This repo is the shared workspace for Amanda's systems: the filing engine, the
SOPs, and the skill packs her AI assistants run against. Anything that is meant
to be repeatable lives here, so every assistant is working from the same copy.

## Everything repeatable ships as a pull request

**A new SOP, a new skill, or a change to an existing one is never committed
straight to `main`.** It goes on a branch and opens a PR.

This is not ceremony. The PR page is the only place the whole change is visible
in one view: what was added, why, and what was verified. It is the record
Amanda reads, and it is what keeps every assistant aligned on one version of
the truth rather than each one carrying its own.

That covers:

- a new SOP, or an edit to one
- a new skill, or a change to how an existing skill behaves
- any script, gate or check that other work depends on
- any change to this file

Small one-off fixes and typos can go straight in. If it will be run more than
once, it is a PR.

## Fixes go at the level the problem lives

When something goes wrong twice, written guidance is not the fix. Guidance
governs judgment, and judgment is what already failed. Find the missing data,
the missing field, or the missing check, and add that instead.

Run 6 is the worked example. Captions kept landing on the wrong clips. The
cause was that the clip inventory recorded no description of what was visible
in a clip, so the pairing step had nothing to pair on. The fix was the missing
column plus a gate that refuses to ship without it, not a reminder to be
careful.

## Verify before claiming

Anything shipped here is run before it is called done. If it could not be run,
say so plainly and say what was checked instead. Tests live next to the thing
they test. `bash filing-system/tests/run-tests.sh`.

## Safety rules that do not bend

1. **Propose-only by default.** Nothing moves without an explicit execute flag.
2. **Nothing deletes.** Execute moves to `_QUARANTINE`. Amanda empties it.
3. **HOLD is never automated.** Sensitive material is held, never auto-routed.
4. **Approval is the gate.** Machine verdicts are proposals. Amanda decides.
5. **No substitution.** When the right input is missing, say so and stop. Do
   not reach for the nearest thing that fits the slot.

## The posting board, which does not get re-litigated

Set 09/08/2026. This is the whole cadence in one place, because it has been
explained more times than it should have been.

| Channel | Per day | What goes there | Call to action |
|---|---|---|---|
| Instagram | 3 to 5 | everything | comment keyword to DM |
| Facebook | 3 to 5 | everything, same cadence as Instagram | comment keyword to DM |
| TikTok | 3 to 5 | everything | link in bio, never the keyword |
| YouTube | 3 to 5 | everything. Shorts for reels, long form for food reviews | link in description |
| LinkedIn | 1 | business only. Just Another Tuesday, or the free AI guide | link |
| X | 0 | dropped 09/08, it was not serving | none |

The 3 to 5 is per account per day, not per platform: the 2 Instagram
accounts are 2 audiences. Instagram and Facebook are a pair and move
together because both carry the keyword comment to DM. TikTok never gets
the comment keyword, its call to action is the bio link. A food review goes
to YouTube as long form, not as a Short.

LinkedIn runs on a rotation: 2 days of promo links, then 1 editorial
business post. The editorial is written from Amanda's newsletters, made
cohesive and on brand, and it has to read like business advice she would
actually give someone. Recycling promo there is fine and she has said so.
`press-play`, `consider-this` and `just-another-tuesday` are all valid
LinkedIn links. Pinterest is parked on purpose, not forgotten.

Prefer a HyperFrames motion text video over a still wherever there is a
choice. One video covers every platform; a still does not.

**Reuse before generating.** The budget does not stretch to regenerating
what already exists and works. Every free lead magnet carousel is evergreen
and reusable, and there is enough variation in them to keep running until
the volume target is met or the data says otherwise. New sets lead because
they are the best quality; an older one goes in now and then to keep the
mix fresh.

Pinterest runs 1 recycled pin a day off that same evergreen pool, to keep
the account warm rather than dry. A pin is a bookmark, so repinning the
same image is how the platform works and does not count as re-wearing
media. Everywhere else the no re-wear rule stands.

The rule lives in `filing-system/data/channel-rules.csv` and
`gm_cadence_check.py` enforces it. Change the CSV, not the gate, and never
a prose note instead of either.

Variety is the point of the volume. A day should not be 5 of the same lane.
The lanes are: holiday fact, Cesa, Club Target, food review, lead magnet
carousel, Amanda on camera, trivia.

The trivia lane is scoped to AI, automation and the creator economy. Set
09/08/2026. General trivia fills the same slot at the same cost while
diluting the positioning the account is there to carry, so the scope lives
in the Topic column of `filing-system/data/trivia-fact-bank.csv` and the
bank refuses anything else. A newsletter is where a fact was found, never
what makes it true: FoundIn and Source are 2 columns and the gate refuses a
row where they are the same. Facts that move get re-checked every 90 days.
`SOP_0909_trivia-pipeline.txt` is the whole procedure.

## Voice

Anything written for Amanda's audience follows the Gentle Muse voice: calm,
specific, emotionally precise. No hype, no generic motivation, no em dashes, no
spelled-out numbers. When in doubt, run it through `post-grader` and do not
ship below 8 out of 10.
