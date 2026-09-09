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

The hunting ground is `filing-system/data/trivia-sources.csv`. Amanda
answered on 09/09: **tier 1 and tier 3 approved, tier 2 parked.** 10 senders
to read, 5 marked `later`.

You do not have to remember that. `gm_trivia_bank.py` reads the list and
holds any fact whose `FoundIn` names a sender she has not approved. A blank
`FoundIn` is fine, it just means the fact did not come off the sweep.

Tier 2 is parked, not rejected. If she opens it later, set `Approved` to
`yes` on those rows and the bank starts accepting them. Change the CSV,
never the gate.

Tier 3 is worth understanding: TikTok Shop, Amazon Associates and Blotato
announcing their own policy changes ARE primary sources. A fact from one of
those needs no second hop, which makes them the cheapest verified material
in the lane.

There is also an exclusion that matters more than the inclusions. Her inbox
carries 5 high-volume stock-tip newsletters on beehiiv: alphasignals,
stocknewsletter, amn, dividends, stockmarketnews. Headlines like "Jon
Najarian's #1 Energy Trade" and "BlackRock is hoarding it. Do you own it?"
They are off-lane, they are hype shaped, and several read as promotional
rather than reported. They are the worst possible input for a lane whose
entire value is being right. Do not read them, and do not let their volume
make them look like signal.

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

**Her avatar twins already exist.** There is no blocker here. An earlier
version of this handoff said there was, because `heygen avatar list` was
run with no filter and a default limit of 20, which returns the stock
groups and stops. The filter is the whole trick:

```bash
heygen avatar list --ownership private --limit 50
heygen avatar looks list --group-id <id> --limit 50
```

Five private groups: 2 Amanda, plus Avery, Cesa and Claude. The look id is
the `avatar_id` you pass when creating a video, not the group id.

Group `e81779635cbc4a7982cfd571a194e0dd` is the production one, 16 looks,
8 of them deliberately named:

| look id | name |
|---|---|
| `3243536278874919a784ed66c135a473` | Amanda with a podcast microphone |
| `96af09cd10804111a290ecb70f39500f` | Amanda hosting a live podcast |
| `f47aa68f16a945c380f47c5045b797ff` | Warmly Lit Radiance |
| `da3d97c8c1164a90a7dad04dfd61ab43` | Authority Red Casual |
| `583b7249de074a2db80fd8b8dc35bf86` | UGC Ad Video |
| `d33d6e3265a14daa8263858d836b4a7f` | Chic Urban Fashionista |

The other group is `8b9584ee0f3b42ff9561f4a32b622de7`, 13 looks, 4 named,
including a plain "Amanda" at `f3105abaf466488e960c54bf89449d47`.

For trivia use one of the 2 podcast looks. It reads as somebody telling
you a thing they know, which is the posture the lane wants. Rotate rather
than using one look every day, the same way plates rotate on the reels.

Avery is a separate person and a separate voice. Do not use the Avery or
Cesa twins on Gentle Muse trivia without asking.

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

## Decisions, answered 09/09

1. **Newsletters.** Scanned 09/09, and she approved tier 1 and tier 3 and
   parked tier 2. 10 senders live in `trivia-sources.csv`, enforced by the
   bank. Tier 3 is the cheap half: TikTok Shop, Amazon Associates and
   Blotato announcing their own changes are primary sources already.
2. **Delivery.** HeyGen talking head, using her existing twin. See the
   render section for look ids. No consent recording needed.
3. **Cadence.** 1 fact a day, all 4 platforms. That is 28 of the 200
   slots a week, so watch `C12_RUNWAY_END` and fill the nearest empty
   days first.

## State on handoff

- Branch `claude/holiday-caption-strategy-m5abq8`, pushed.
- `run-tests.sh` 126 passing, 0 failing.
- Bank: 3 rows, 0 usable, all awaiting verification.
- Avatar: her own twin, group `e81779635cbc4a7982cfd571a194e0dd`.
- Board: 199 of 200 scheduled, runs dry after Sep 18 except a thin tail.
- Cesa lane still 42 posts short, blocked on footage not in Drive.
