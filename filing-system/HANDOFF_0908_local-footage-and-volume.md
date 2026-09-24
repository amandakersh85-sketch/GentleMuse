# GENTLE MUSE — LOCAL FOOTAGE AND VOLUME HANDOFF
**Paste everything below as your first message in Claude Code on Amanda's own machine.**

---

You are continuing a build that has been running in a cloud session. Read
`CLAUDE.md` at the repo root first and follow it exactly. The short version
of the house rules: anything repeatable ships as a PR, a fix goes at the
level the problem lives (missing data or a missing gate, never a reminder
to be careful), nothing ships unverified, and the 5 safety rules do not
bend.

Branch: `claude/holiday-caption-strategy-m5abq8`. Everything below is
already committed and pushed there. Pull it before you start.

You own **footage**. The Carousel Build project owns the carousels and the
schedule, see `HANDOFF_0908_carousel-build-and-scheduling.md`. Do not
duplicate its work. When you finish a cut, host it, stage it in
`staging-library.csv`, and let that session place it.

## THE BOARD

| Channel | Per day | What goes there | Call to action |
|---|---|---|---|
| Instagram | 3 to 5 | everything | comment keyword to DM |
| Facebook | 3 to 5 | everything, same cadence as IG, they move as a pair | comment keyword to DM |
| TikTok | 3 to 5 | everything | **link in bio, never the keyword** |
| YouTube | 3 to 5 | Shorts for reels, **long form for food reviews** | link in description |
| LinkedIn | **1** | **business only.** Just Another Tuesday or the free AI guide | link |
| X | **0** | dropped 09/08 | none |

In `filing-system/data/channel-rules.csv`, enforced by `gm_cadence_check.py`.
Change the CSV, never the gate.

The lanes a day gets filled from, never 5 of one: holiday fact, Cesa, Club
Target, food review, lead magnet carousel, Amanda on camera, trivia.

## WHY YOU EXIST AND THE CLOUD SESSION DOES NOT

You can open the D: drive. That is the whole difference and it is the
reason this handoff exists.

22 clips filmed 09/04 and 09/05 live at
`D:\Phone Backup\2026-09-05 Phone Import\Camera`. They never reached Google
Drive. The cloud session checked Drive on 5 separate occasions across 4
days; the newest video there is from July. So 13 Club Target store clips
and the Cesa grass clip are described in the library, sourced, and
completely unusable from the cloud.

That is now a gate, not a note. `clip-library-drive.csv` carries a
`MediaState` column (local, drive, offline) and `gm_bind_check.py` refuses
any payload bound to an offline clip with `E11_MEDIA_UNREACHABLE`. When you
work locally with the D: drive mounted, those clips are reachable. Flip
their MediaState to `local` **only after you have actually opened the file**,
and set `GM_MEDIA_ROOT` to wherever the footage really is.

## DO THIS FIRST — THE FIRST 20 MINUTES

Run in order. Report after step 4 before doing anything that writes.

1. **Prove the toolchain.**
   ```
   ffmpeg -version
   node --version
   python3 --version
   ```
   `reel-factory/node_modules` may not exist locally. `npm install` in
   `reel-factory/` if Playwright and ffmpeg-static are missing.

2. **Prove the tests pass before you change anything.**
   ```
   bash filing-system/tests/run-tests.sh
   ```
   Expect **92 passed, 0 failed**. If it is not 92/0 on a clean checkout,
   stop and say so. Do not start work on a red suite.

3. **Prove you can see the footage.**
   ```
   dir "D:\Phone Backup\2026-09-05 Phone Import\Camera"
   ```
   You are looking for 22 files, `VID_20260904_19*.mp4` and
   `VID_20260905_11*.mp4`. If the drive is not there, say so and stop.
   Do not substitute. Rule 5.

4. **Report:** tests result, whether the footage is visible, how many files.

## THE WORK, IN PRIORITY ORDER

### 1. Club Target, the thing only you can do

Read `filing-system/briefs/2026-09-08-club-target-labor-day.md`. It has a
finished 3 clip edit and a caption ready to paste. The Labor Day Deals
challenge (0p1g, 30 points, would take her from 610 to 640 and past the 630
Tier 5 needs) closes around 09/08, so **check whether it is still open before
building anything.** If it closed, the same 13 clips still serve the next
posting challenge and the edit sheet still applies.

Hard constraints on anything Club Target:
- `#TargetPartner` is the FIRST thing in the caption. The program requires it.
- Branded content toggle ON.
- **Never state a price** in caption, on-screen text, or voiceover. Shelf tags
  visible on camera are fine, that is the store's own signage. Stating one is
  the open TikTok Shop violation from 08/04/2026.
- Post direct to TikTok, not through Blotato, so the 200 slot cap cannot
  touch it. TikTok is the only viable lane: every Club Target posting
  challenge rejects accounts under 500 followers, TikTok has 1,654 and
  Instagram has about 131.

### 2. The Cesa Oct 24 reel, blocked on one file

`reel-factory/WAITING-reels-final-cesa-blackgirl.json` is written and
waiting on `VID_20260905_110554470.mp4`, which is on D: and nowhere else.
The `WAITING-` prefix means the directory sweep skips it, so it does not
fail the suite. When you can open that file:
- ingest it, describe it in `clip-library-drive.csv`, set MediaState
- rename the payload back to `reels-final-cesa-blackgirl.json`
- render, mix, QC by frame, host, stage

### 3. Volume, which is the actual constraint

Read `filing-system/briefs/2026-09-08-why-the-queue-cannot-run-16-a-day-yet.md`
and `filing-system/sops/SOP_0908_posting-cadence-3-to-5.txt` before touching
the queue.

The binding constraint is **content, not the cap and not the slots**. 12 days
at 16 posts a day needs 48 unique reels. There are 28. The other 93 reservoir
rows are next year's holidays (Christmas 15, Thanksgiving 8, Valentine's 8,
St Patrick's 7 and so on), each needing a plate at about 50 credits against
2,974 held, so roughly 59 of the 93 are affordable.

**The Halloween bank is exhausted.** All 20 facts in it now have a reel
payload; the 5 built on 09/08 were the last of them. So more Halloween
volume needs new FACTS, not new renders. Do not go looking for unrendered
Halloween facts, there are none.

What is actually free and unclaimed, in order:

1. **3 reels are built and need only hosting.** `countdown-ig`,
   `countdown-tt` and `halloweentown-v2` are rendered in `reel-factory/out/`
   and appear in `staging-library.csv` as NEEDS_RENDER with Waiting
   "hosting". Upload them, put the URLs in `blitz-media-map.csv`, flip the
   12 rows to STAGED. That is 12 more loadable rows for zero credits and
   about 20 minutes. Do this first.
2. **New Halloween facts into the bank**, if the season needs more. Every
   claim needs a real source and a Year, or `gm_holiday_check.py` refuses
   it with `E07_UNSOURCED_YEAR`. Sourcing is the slow part, not rendering.
3. **Thanksgiving, which is next on the calendar** (Nov 26). 8 facts are
   banked and need plates. At about 50 credits a plate against 2,974 held,
   this is affordable now and it is the work that stops November looking
   like September did.

For anything using existing plates, the bind gate polices the pairing, so a
forced match will be refused rather than shipped. That is working as
intended, not an obstacle to route around.

### 4. Food reviews, which have never been redistributed

They exist on TikTok and are doing nothing anywhere else. Raw first, TikTok
as the fallback.

1. **Inventory the raw.** Search the phone and D: drive for restaurant
   footage. Amanda specifically cannot find **Amigos, from August** — look
   for it. Anything you find, ingest into `clip-library-drive.csv` with a
   real Shot description and MediaState.
2. **Fall back to TikTok** for reviews with no raw. Pull her posted copies
   down and strip the watermark before reusing them.
3. **Cut each one 2 ways:**
   - **YouTube long form.** The full review, as a normal video, NOT a Short.
     This is explicit: a food review is not a Short.
   - **Short cut** for Instagram, Facebook and TikTok.
4. Caption per channel. Keyword to DM on Instagram and Facebook, bio link on
   TikTok, description link on YouTube.

Food reviews are a **recycle lane**, not a one-off. The Tuesday magnet is
"Consider This", the newsletter that promises to say when something is
overpriced. `rotation-magnet.csv` calls that a review contract, so a food
review is the natural Tuesday post.

### 5. The trivia series

Amanda wants a random trivia facts series, and the standing rule is the same
one the holiday bank already runs on: **fact verified, source verified,
cited, and true.** That is the whole point of it, so nothing goes out that
`gm_holiday_check.py` would refuse.

The series currently lives in a ChatGPT project called Avery. **Ask Amanda
for that handoff prompt before you build anything** — the format and voice
are already decided there and reinventing them wastes the work.

Then, per fact: a bank row with a real Source and a Year, a beat script, a
plate or an existing clip with a `match_reason`, and Marcia reading it. The
same pipeline as the Halloween run. Do not invent a second one.

**On the avatar twin, the honest answer:** the HeyGen account behind this
API key has 20 avatar groups and every one is a HeyGen stock avatar (Dante,
Brody, Aya, Elodie and so on). **There is no twin of Amanda on it.** The CLI
does have `heygen avatar create` and `heygen avatar consent create`, so one
can be made, but it needs her consent recording and her sitting down to do
it. Until then the trivia series runs as typography plus Marcia, exactly
like the Halloween reels, which already works.

Do not tell her the twin is ready. Tell her what it takes.

### 6. Amanda on camera

She said it plainly and it keeps getting dropped: she is on camera. She has
HyperFrames and a 3 motion machine. Her 5 to camera scripts are in
`filing-system/data/halloween-track-a-scripts.csv` for Oct 19, 21, 23, 27
and 29. Two of the 5 backup reels have been spent on near term volume; the
Mary Shelley and War of the Worlds cuts are held so those days cannot go
dark. When she films, her footage replaces the backup and the backup goes
back to the reservoir.

## TWO DECISIONS AMANDA HAS ALREADY MADE

**Track A reels: split.** 5 were built 09/08 as backup for her Oct 19-29 to
camera days. Salem (HAL-003) went to Instagram and the poisoned candy one
(HAL-020) to TikTok for 09/08. Load **one more** when a slot frees — the
witch trials cut (HAL-006) was cap-blocked off Facebook 09/08 19:30 and is
first in line. **Hold the other 2** (HAL-004 Mary Shelley, HAL-007 War of the
Worlds) staged as October backup so those days cannot go dark.

**The October tail: build the list, show her, then act.** 101 posts sit on
Sep 20 to Oct 31 at 2.4 a day, holding half the cap. 95 are not locked to
their date; 6 are (Samhain Oct 31, trick or treat Sep 30 and Oct 4). Pulling
the 95 frees 95 slots and lets the near 12 days run full.

**Approved 09/08.** The Carousel Build session owns executing it, but if
that has not happened by the time you are working, the order is the same and
it does not change:
1. Write every one of the 95 into `staging-library.csv` as a STAGED row with
   its caption, hosted media URL, account and intended slot.
2. Verify each row reads back complete. A row missing its media URL is not
   a row.
3. Show her the list in session and get her word.
4. Only then remove the schedules, and only for rows you have verified.

Nothing is lost if this is done in that order, which is the only reason it
is allowed at all. Rules 2 and 4 are why the list comes first.

## HOW TO BUILD A REEL, EXACTLY

Four things have gone wrong here and all four are now gates. Do not work
around a refusal; the refusal is the point.

```
cd reel-factory
export FFMPEG=./node_modules/ffmpeg-static/ffmpeg
export COMP=reel-footage.html          # NOT optional
REELS=reels-final-<slug>.json node build.mjs .
```

- **`COMP` is not optional.** Unset, it defaults to `reel.html`, which draws
  embers and no footage and hardcodes "plate loaded". 5 reels rendered that
  way on 09/08 with the plates entirely absent and the build reported
  success. Compositions now declare `window.__consumes_plate` and the build
  refuses a payload that binds a clip to one that ignores clips.
- **Line breaks.** Keep each `<br>` separated segment at **30 characters or
  fewer**. Past about 31 the browser breaks the line again wherever it likes
  and you get an orphan: "A fear that changed how a / country / parents has
  nothing behind / it." 11 of 26 beats shipped that way on 09/08. The
  composition now counts drawn lines against asked lines and the build
  refuses the difference.
- **Every clip binding needs a `clip_id` and a real `match_reason`** saying
  what in that clip shows the line. This is the Run 6 rule and
  `gm_bind_check.py` enforces it.
- **QC by frame, always.** Pull a frame from every beat and look at it. A
  silent remux once replaced a good master with an old one and only the file
  timestamp caught it. Trust the frame, not the log line.

Voice: HeyGen `heygen voice speech create --voice-id
05f19352e8f74b0392a8f411eba40de1 --speed 0.92 --text "..."`. That is Marcia.
No `--json` flag, the output is already JSON, and it serves MP3 at `.wav`
URLs. Take durations from the API response, not the container.

Bed: `reel-factory/beds/eerie-calm-bed.wav`, committed 09/08 because it had
been living only in a scratch directory and a signed URL that expires around
09/11. Every reel in the season carries this exact track. The ducking recipe
is in `reel-factory/beds/README.md`. Give each reel a different 27 second
window of it so a run of them does not open identically.

## ACCOUNTS

```
instagram  45886  thegentlemuse2026      instagram 65540  cesasgoldenyears
tiktok     41488  thegentlemuse2026      tiktok    55761  cesasgoldenyears
facebook   30840  pageId 1086399221215093
youtube    36129   linkedin 20723   pinterest 6328
twitter    dropped 09/08, nothing schedules there
```

## THINGS THAT DO NOT BEND

1. Propose only by default. Nothing moves without an explicit execute flag.
2. Nothing deletes. Execute moves to `_QUARANTINE`. Amanda empties it.
3. HOLD is never automated. Sensitive material is held, never auto routed.
   The OF lane stays excluded and hand filed.
4. Approval is the gate. Machine verdicts are proposals.
5. No substitution. When the right input is missing, say so and stop.

Also: never propose a Blotato plan upgrade, she has ruled twice. API keys
never touch git. The HeyGen key was echoed into a session log once and
should be rotated at HeyGen when convenient.

## VOICE

Calm, specific, emotionally precise. No hype, no generic motivation, no em
dashes, no spelled out numbers. Run anything for her audience through
`post-grader` and do not ship below 8 out of 10.
