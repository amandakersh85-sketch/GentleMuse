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

Which keyword each account can actually answer lives in
`filing-system/data/keyword-registry.csv`, and `gm_keyword_check.py` refuses a
caption that asks for one the account cannot. That file is the full copy of
what is live in Blotato, not a sample. On 09/11 the old partial file said BROW
was not a keyword. It had been live on 2 accounts since 08/08, and 20 YouTube
posts were queued asking for a comment keyword YouTube has no listener for. A
dead keyword is worse than no call to action, because somebody comments the
word and waits. Refresh the registry from Blotato whenever an automation
changes.

What a campaign promised out loud is data, not memory. The nightly Halloween
run was announced on Instagram on 09/19/2026: 1 true thing about the season
every night, 43 nights, no dark days. Nothing in the repo recorded that, so
26 of the 43 nights went dark and every gate passed the board, because a
night holding 4 Club Target posts is not starved, not silent and not a
repeat. The promise now lives in `filing-system/data/campaign-targets.csv`
as StartDate, Accounts, PromisedOn and PerNight, and
`staging-library.csv` carries a Campaign column so a board row can be joined
to the campaign it belongs to. `C13_PROMISE_DARK` refuses a night the
campaign owes and has not filled, and `C14_PROMISE_FLOOD` refuses more than
PerNight in a day, because 3 in 1 night is 2 nights taken off the end.
PerNight is a floor and a ceiling, and it is the number the announcement
stated, not a preference. When a campaign is announced, write the promise
into the CSV before anything is scheduled against it.

A campaign a job places needs 1 more file. The 33 nights are loaded by
`.github/workflows/halloween-33.yml`, which reads its own plan and writes
straight to the queue, so none of its slugs reach `staging-library.csv` and
C13 could see 11 of 153 board rows and called a run that had missed nothing
dark on 27 nights, every run, for 5 nights.
`filing-system/data/campaign-plans.csv` says where a campaign's plan lives,
and the gate reads the slug, the caption's opening line and which accounts
each night books out of the plan itself. Facebook and YouTube run alternate
nights and the plan already says so, so it is not restated anywhere. Add the
row when a campaign starts shipping from a plan, and change the plan, never a
copy of it. `LoadHorizonDays` on the campaign row is how far ahead its loader
has actually booked, because a night nobody has loaded yet is not a dark
night.

A campaign that posts at a fixed hour owns that hour, and the plan is where
that is written down. `C15_SLOT_CONTESTED` reports a post that is not part of
the campaign inside 60 minutes of a slot the plan reserves, on an account that
night books. `C16_SLOT_MODEL_CONTESTED` reports a `slot-model.csv` row sitting
on the same slot, because that is the file another scheduler reads to decide
where a post goes, and on 10/01 it still gave 23:00 UTC to ROTATION on tiktok
41488 and PERSONAL on instagram 45886. The hour was taken twice before either
rule existed, on 09/28 and again on 09/30, and both times it showed up only as
C05 spacing noise.

A video that carries no sound is refused before it ships. Amanda, 10/04:
"it's going out with no sound again." 6 posts from 3 assets were queued with
no audio track at all, all from the 4459xxx batch, and every gate passed them
because a silent reel is not starved, not early, not a repeat and not a
collision. `gm_audio_check.py` reads the file rather than a column, because
the queue payload says nothing about audio and never will:
`A01_NO_AUDIO_TRACK` refuses a video post with no sound track and
`A02_AUDIO_UNREADABLE` reports a container it could not read instead of
passing it. It costs 2 range requests, not a download.

Measure before naming the fix. A food review goes to YouTube as long form, and
2 queued reviews carried `#shorts` against that rule, reported 3 nights running
with the fix named as a missing lane column. Reading the files says otherwise:
Scooter's runs 122.6 seconds and Amigo's runs 31.2, both inside the Shorts
limit, so both genuinely are Shorts and both tags are accurate. A 31 second
review does not become long form by deleting a hashtag, because the long form
cut does not exist. The open item is a render nobody made, not a tag and not a
column, and a gate comparing the tag to the file would have passed both and
said nothing. `gm_audio_check.seconds()` reads the length out of mvhd in the
same 2 range requests the handler walk already fetches, so the number is on the
gate rather than in a probe somebody writes again each night. Repeating a fix
that was never checked is how an item stays open for a week.

The bed goes on in `reel-factory/bed.mjs`, which `build.mjs` calls on every
render, and a reel it cannot put a bed under is **refused** rather than written
out silent. Until 10/04 the recipe was prose in `beds/README.md` and nothing
ran it, so the muxing was done by hand: 1 offset for the whole Halloween run,
and 6 posts queued with no audio track at all. `beds/beds.csv` maps a sound
family to its file, the payload names the family, and the refusal says which
bed to go and get. After muxing it measures the result and deletes it if there
is nothing audible, because a real AAC track carrying silence passes every
other check.

The bed is `reel-factory/beds/eerie-calm-bed.wav` and it is the sound of the
season. Every reel takes a different slice of it, which `beds/README.md` has
said all along and which was not happening: all 20 published nights open on
the identical 18 seconds. Music carries these, not voiceover. Amanda, 10/04:
"the voiceovers don't hit that hard. The music wins, honestly. It does
better, and it's free." Levels are matched to the run at mean -17.4 dB and a
peak under -1.5, and a bed with no voiceover over it does not sit at the
`volume=0.32` the ducking chain uses.

A post has a surface, and the board records it. A story and a feed reel 105
minutes apart on 1 account are the intended pattern here, the reel and a story
pointing at it, not 2 posts burying each other. C05 is checked per account and
per surface for that reason. The queue carried `target.mediaType` the whole
time and the snapshot was throwing it away, which is why 21 of 26 spacing
findings on 10/01 and 15 of 18 the night before were not real.

## The day's shape, set 09/24/2026

Amanda, sick and between sessions, describing what she already has running:
"I've got the seasonal stuff going out every evening. I've got something of
myself going out at some point every single day. I've got the club targets
going out, and I need this to go out." The 4 lanes are not a proposal. They are
the day, and a day missing one of them is the finding.

| Lane | Per day | Who owns it |
|---|---|---|
| seasonal fact | 1, every evening | Halloween 33 Nights, then The Real One to 01/01 |
| Amanda herself | 1, face to camera or UGC | her own footage, her HeyGen twin on a day with no clip |
| Club Target | as the partnership lands | sponsored, holds its times |
| newsletter signup | 1 every 2 days, minimum | the carousel rotation |

The newsletter lane is the one that goes missing, and it is the one she says
matters most: "those are the two most important things, getting people to sign
up for the newsletters. Just keep rotating them." Just Another Tuesday and
Consider This. The rules live in
`filing-system/data/newsletter-rotation.csv`:

- at least 1 newsletter promo every 2 days, rotating between the 2
- the 1 page lead magnet posts are cut. Only the carousels run here
- a carousel goes out as a video with a music bed, never a still. A still
  cannot carry sound, and she asked for music on them specifically
- the rotation recycles carousels that already exist. Nothing new is generated
  for this lane

On 09/24 the board had Just Another Tuesday on 2 days out of 38, and 22 of
those 38 days carried neither newsletter, including 11 days in a row from
10/21 to 10/31, straight through Halloween.

Leave the number 1 slot on Thanksgiving morning alone. It is there on purpose.

**One board, not one per session.** Amanda, 09/24: "all I want is every piece
of information I've been screaming at different sessions to come together, stop
battling each other. Get one sensible, cohesive schedule out." That is what
this file is for. A ruling she gives one session is written here, in the data,
on the same day. A session that learns something and keeps it in its own
transcript has not recorded it.

## The season, set 09/28/2026

Amanda, 09/28: "We don't stop at Halloween. We're also doing Thanksgiving and
Christmas. So we don't put it all in the queue, obviously, but we make sure that
the waves are being acknowledged."

The 6 PM seasonal post runs to 01/01 in 4 waves.

| Wave | Nights | What runs |
|---|---|---|
| Halloween | 33, 09/29 to 10/31 | Halloween 33 Nights, `halloween-33/` |
| Thanksgiving | 26, 11/01 to 11/26 | The Real One |
| Christmas | 29, 11/27 to 12/25 | The Real One |
| New Year | 7, 12/26 to 01/01 | The Real One |

The Real One runs every night on all 4 main accounts: Instagram and TikTok at
6:00 PM Central, Facebook and YouTube at 6:30 PM. Amanda chose all 4 nightly on
09/28. Facebook and YouTube are the thinnest accounts. The captions are drafted
on pull request #13 and are approved a month at a time: November by 10/18,
December and New Year by 11/14. A wave goes into `campaign-targets.csv` the day
it is announced, before anything is scheduled against it.

Nothing loads more than 7 days ahead except date-locked posts: sponsored posts,
the sale days and Thanksgiving morning. The queue holds 200, which is about 10
days at full volume. The refill fills the nearest days first and keeps 10 slots
free for the nightly run and the daily trivia. `blotato-refill/README.md` has
the rules.

The day, in Central time. The clock times hold when the clocks go back on 11/01,
so every loader works in Central time and converts.

| Time | Lane |
|---|---|
| 8:30 AM | LinkedIn |
| 10:00 AM | daily trivia |
| 12:00 PM | Amanda on camera |
| 2:00 PM | newsletter carousel every other day, otherwise an evergreen top-up from the waves |
| 4:00 PM | Club Target, when there is one |
| 6:00 PM | the seasonal post, 6:30 PM on Facebook and YouTube |

Posts on 1 account stay 2 hours apart. Noon was retired for the wave library on
08/24 after a pileup. It belongs to this 1 lane now, and the 2 hour gap keeps
everything else off it.

Amanda on camera, 09/28: a Claude session on her laptop sorts her clips from the
camera roll and the D: drive, names each by what she says, and puts them in 1
Google Drive folder. The week reaches her as 1 pull request. Her HeyGen twin
covers a day with no clip.

Variety is the point of the volume. A day should not be 5 of the same lane.
The lanes are: holiday fact, Cesa, Club Target, food review, lead magnet
carousel, Amanda on camera, trivia.

Re-airing is fine after 4 days. Amanda, 09/10/2026. There is no cap on how
many times a fact runs on a channel, only on how close together, because
the board holds about 17 distinct video facts and filling a day is almost
always a re-air. Twice on 1 channel in 1 day is still refused and always
was. `gm_fill_plan.py` proposes the fills and `C09` enforces the gap; both
read the spacing from 1 constant, so change it there.

The trivia lane is scoped to AI, automation and the creator economy. Set
09/08/2026. General trivia fills the same slot at the same cost while
diluting the positioning the account is there to carry, so the scope lives
in the Topic column of `filing-system/data/trivia-fact-bank.csv` and the
bank refuses anything else. A newsletter is where a fact was found, never
what makes it true: FoundIn and Source are 2 columns and the gate refuses a
row where they are the same. Facts that move get re-checked every 90 days.
`SOP_0909_trivia-pipeline.txt` is the whole procedure.

A fact nobody checked reads exactly like a fact somebody checked. On 10/04 all
26 Thanksgiving nights were finally read against sources and 4 were wrong: 17
years for Sarah Hale's 36, the 1840s for an 1820 coinage, a 5 item study
described as a 3 item one with a comparison it never made, and a closing
thought sitting in the confidence column as high. All 26 rows said `verified:
no` and all 26 would have rendered, because nothing read that column.
Confidence is a session's opinion of its own memory, which is the thing that
was already wrong, so it can never be the check. A plan row now carries
`verified`, `checked` and a `sources` line that points at something, and
`gm_fact_check.py` refuses a night still to come that has none:
`F01_FACT_UNVERIFIED`, `F02_FACT_NO_SOURCE`, and `F03_FACT_STALE` at the same
90 days as the trivia bank, read from the same constant. `partly` and `n/a`
pass and are listed on every run, because an exception nobody sees is an
exception that spreads. The gate cannot tell a true fact from a false one and
does not claim to; it refuses the condition all 4 shipped under. It is scoped
to nights on or after today for the reason C13 had to be, and a reused night is
checked like any other, because the hook is the line the caption opens with.
It found `halloween-33` on its first run with no `verified` column at all, and
that pass ran the same day: 5 of those 25 facts needed correcting, and night
33, the finale, rests on Samhain as the Celtic new year, which Rhys and Frazer
proposed in the late 1800s and which is disputed. The dark half of the year is
what is attested and what the row now says.

A correction that does not reach the queue is a 2nd version of the truth. On
10/04 the fact check corrected night 10 of the Halloween run from candy corn
"was invented in the 1880s by George Renninger" to "is credited to", because
the attribution is oral history and the sources say so. The loader had written
the old sentence into the queue on 10/03, and 4 posts were going out on 10/08
still stating it as record. Every rule here reads the board's shape and not its
words: C01 counts posts, C05 counts minutes, C13 counts nights, C15 counts
slots, A01 opens the file. `gm_caption_check.py` reads the words.
`C17_CAPTION_STALE` reports a queued post whose opening block is no longer its
plan row's hook, fact and backbone. The join is the hook, which
`campaign-plans.csv` already declares, and the comparison stops at the
countdown line because everything after it is a per-platform call to action.

A correction to a caption is not an instruction to place the post again. The
loader identified a night by the first 120 characters of its caption, and the
hook is 58 of them, so the key reached 61 characters into the fact. Correcting
night 10's candy corn attribution on 10/05 moved the key, and run 16 did not
recognise the night it had placed on 10/03: 10/08 now carries night 10 twice on
all 4 accounts, once with the corrected sentence and once with the one the
sources do not support. The docstring said idempotent the whole time.
`load.py` keys on the countdown line now, with the platform and the account,
because that is the part of a caption a correction never touches, and it is
the same join `gm_board_snapshot` and C17 already use. A loader that writes
straight to the queue needs an identity that is not the words.

A price on affiliate content is refused, and the gate that says so has to be
able to reach the post. `K05_PRICE_ON_AFFILIATE` existed, had a passing test,
and could not see any of the 4 priced posts on the 10/06 board for 3 separate
reasons: it sat inside the branch only a caption naming a live product keyword
reaches, and all 4 were storefront-link posts with no keyword; its pattern was
a currency sign only, and 3 of the 4 typed 2.69 with no sign under the
digits-not-words rule; and 3 carried `#TargetPartner` with no commission line,
which the disclosure pattern did not match either. What makes a post affiliate
is the PAID zone in `queue-zones.csv`, `#ad` or `#TargetPartner`, and K05 reads
every post that carries one. 1 decimal place is not a price, because a food
review scores 7.5 out of 10. The rule was written in 5 handoffs and
`blotato-refill/README.md`, all prose, with an open TikTok Shop violation from
08/04/2026 behind it, and prose is what failed.

A gate that cannot read the live queue is a gate that passes. `gm_cta_check`
and `gm_keyword_check` took only the flat fixture shape, so running either
against the board meant hand writing a converter first and no nightly run ever
did. Both read a `blotato_list_schedules` dump as it comes now. The first run
of `gm_cta_check` on the board returned 128 findings on 187 posts, which is a
backlog and not 1 night's damage.

A wave that has rendered is not a wave you can redraft. All 30 Halloween reels
are built and uploaded, and 26 of them close the video on the caption's
backbone line word for word. Rewriting a closing line there does not change a
caption, it desyncs the caption from the words on screen. Thanksgiving and
Christmas were unrendered drafts when they were redrafted on 10/05, which is
why that cost nothing. Check `weeks/media.json` and `beats.json` before
offering to rewrite anything on a wave that is already shipping.

## Voice

Anything written for Amanda's audience follows the Gentle Muse voice: calm,
specific, emotionally precise. No hype, no generic motivation, no em dashes, no
spelled-out numbers. When in doubt, run it through `post-grader` and do not
ship below 8 out of 10.
