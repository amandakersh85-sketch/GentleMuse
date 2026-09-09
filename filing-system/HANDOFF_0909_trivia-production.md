# Handoff: run the trivia production pipeline locally

For a local Claude Code session in `GentleMuse/`. Written 09/09/2026.
Read `filing-system/sops/SOP_0909_trivia-pipeline.txt` first. This file is
how to run it; that file is why it is shaped this way.

## What you are producing

One AI, automation or creator-economy trivia cut per day, distributed to
YouTube, TikTok, Facebook and Instagram. Gentle Muse account, not a
separate brand. Amanda's positioning call, 09/08/2026.

This lane exists because the board is short on distinct facts, not because
it is short on posts. If you find yourself re-airing a fact to fill a slot,
you have rebuilt the problem this was meant to solve.

## Before you touch anything

```bash
bash filing-system/tests/run-tests.sh          # 126 passing as of 09/09
python3 filing-system/scripts/gm_trivia_bank.py --audit
```

The audit will say `0 usable, 3 held`. That is correct. The bank ships
unverified on purpose. Your first job is section 1.

## 1. Verify the 3 seeded facts

TRV-001, TRV-002, TRV-003. For each one: open `SourceUrl`, read enough to
confirm the claim in `Fact` exactly as written, then set `Verified=yes`
and `VerifiedOn=` today in `filing-system/data/trivia-fact-bank.csv`.

If a source does not say what the row says, fix the row or delete it. Do
not soften the wording to make it survive. A row that needs softening to
pass was not a fact.

Re-run `--audit`. You want usable rows before anything else happens.

## 2. Hunt (the daily loop)

Amanda's newsletters are the hunting ground. She gets marketing, creator
and AI mail daily. **Ask her which senders or which Gmail label to read
before you start** — see Open Questions.

Rules for this stage:

- The newsletter goes in `FoundIn`. Never in `Source`.
- A candidate is a lead, not a fact. Nothing leaves this stage as truth.
- Prefer facts with a stable primary source. A vendor blog post that will
  be edited is weaker than a paper, a filing, or dated documentation.
- Mark `Decays=yes` for anything that is a price, a count, a rate, a model
  name or a policy. When in doubt it decays.

## 3. Verify, then bank

Open the primary source. Not the newsletter's paraphrase of it.

```
FactID     TRV-0NN, next free number
Topic      ai | automation | creator, nothing else
Fact       the claim, 20+ chars, written the way it will be said
Backbone   the turn, 15+ chars. What it means for her audience.
FoundIn    the newsletter it surfaced in
Source     the thing that makes it true
SourceUrl  a link that opens to that thing
AsOf       the date or year the fact is true as of
Decays     yes | no
Verified   yes, only after a human read the source
VerifiedOn the date that happened
Delivery   talking-head | motion-text
Keyword    TUESDAY (this lane routes to Just Another Tuesday)
```

## 4. Write

One script, then 4 captions. Voice rules from CLAUDE.md: calm, specific,
no hype, no generic motivation, no em dashes, digits not words.

Per-platform call to action, from `channel-rules.csv`:

| platform | call to action |
|---|---|
| Instagram, Facebook | comment keyword to DM |
| TikTok | link in bio, never the keyword |
| YouTube | link in description, `#shorts` on a vertical cut |

The Backbone must survive into every caption. `T04_NO_TURN` fails a post
that reports the fact and stops.

**Do not add numbers.** Any figure not in the bank row fails `T03`. If the
fact needs a number the row does not carry, go back and check that number
against the source, then add it to the row. That order, never the reverse.

## 5. Check

```bash
python3 filing-system/scripts/gm_trivia_check.py --post draft.json
# exit 0 PASS, 1 FAIL nothing ships, 2 HOLD waiting on a fact
```

Post JSON: `{"id", "factId", "platform", "text"}`. A directory works too.

Then `post-grader`. Nothing ships below 8 out of 10.

## 6. Render

Two routes. Pick per `Delivery` on the bank row.

**motion-text** — works today, zero external cost, covers all 4 platforms.
The existing reel factory:

```bash
cd reel-factory
COMP=reel-footage.html REELS=<payload>.json \
  FFMPEG=./node_modules/ffmpeg-static/ffmpeg node build.mjs .
```

`COMP` is not optional. Unset, it silently falls back to `reel.html`,
which draws no plate, and you get 5 reels with no imagery and no error.
That has already happened once. Line segments must be 30 characters or
under or the browser rewraps and orphans a word; the build refuses this
now, but write to it rather than fighting it.

**talking-head** — HeyGen. Voice `05f19352e8f74b0392a8f411eba40de1`,
speed 0.92, roughly $0.02 per line. Wallet was $13.37 on 09/08, check it
with `heygen user me get` before a batch.

```bash
heygen voice speech create --voice-id 05f19352e8f74b0392a8f411eba40de1 \
  --speed 0.92 --text "..."
```

There is no `--json` flag. Mix against `reel-factory/beds/eerie-calm-bed.wav`
with the ducking recipe in the reel-factory README.

**Blocker on the talking head:** there is no HeyGen avatar twin of Amanda.
All 20 avatar groups on the account are stock. `avatar create` and
`avatar consent create` exist but need a consent recording from her that
does not exist yet. Until then a talking head is either a stock face that
is not her, or footage she shoots. See Open Questions.

## 7. Schedule

Never straight to publish. Into the HOLD queue, Amanda releases.

When she has approved, schedule through Blotato respecting every gate:

```bash
python3 filing-system/scripts/gm_board_snapshot.py <queue.json> board.csv
python3 filing-system/scripts/gm_cadence_check.py board.csv
```

- `C08` / `C09` — a fact runs at most twice per channel, 3 days apart,
  never twice in a day
- `C11` — no channel silent on a day it owes a post
- `C12` — fill the nearest empty days first. Never oldest row first. A row
  dated weeks out holds one of the 200 slots the near window needs.

Account ids: YouTube 36129, TikTok 41488, Facebook 30840 (pageId
1086399221215093), Instagram 45886. Pinterest 6328, LinkedIn 20723.

## What this session must not do

- Publish without Amanda's approval. House rule 4.
- Mark a row Verified without opening the source. That is the one thing
  that makes the whole run pointless.
- Substitute a nearby fact when the right one is missing. House rule 5.
  A held row stays held.
- Propose a Blotato plan upgrade. She has ruled twice.
- Put any API key in git.

## Open questions for Amanda

1. **Which newsletters.** Name the senders or a Gmail label. Without it
   the hunt stage has no defined input and I will be guessing at her inbox.
2. **The talking head.** No avatar twin exists. Options: she records a
   HeyGen consent clip once and gets an unlimited twin, she shoots the
   cuts herself as she did for the existing Daily Random Trivia Fact
   clips, or the lane runs as motion text until she has time.
3. **Cadence.** 1 fact a day across 4 platforms is 4 more of the 200
   slots per day, which shortens the runway. Confirm 1 a day, or set it
   to 3 a week.

## State on handoff

- Branch `claude/holiday-caption-strategy-m5abq8`, pushed.
- `run-tests.sh` 126 passing, 0 failing.
- Bank: 3 rows, 0 usable, all awaiting verification.
- Board: 199 of 200 scheduled, runs dry after Sep 18 except a thin tail.
- Cesa lane still 42 posts short, blocked on footage not in Drive.
