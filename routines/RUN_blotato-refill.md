# PART B. THE DAILY ROUTINE

> ## STOOD DOWN 2026-09-02. DO NOT AUTO-LOAD.
>
> Amanda gave dominion of the Blotato queue to the Holiday caption strategy and
> voice session. This side is now the **supplier and the safety gate**, not the
> decider: the wave libraries, the load ledgers and `validate-wave.py` stay here,
> but what enters the live queue, and when, is that session's call. One writer to
> the queue.
>
> The `GM Blotato Daily Refill` task is **Disabled**. Do not re-enable it, and do
> not run Step 5 (Load), without Amanda saying so. The two systems hold opposite
> doctrines: this one fills to the 200 cap as far out as the library reaches, and
> that one holds a short live window and pushes the rest to a backlog. Running
> both means each undoes the other every morning.
>
> Steps 0 through 4 and Step 7 are still useful on demand: preflight, validate,
> measure the runway, report. Step 5 is the part that is parked.
>
> Full contract: `content/handoff/HANDOFF_0902_queue-supplier-contract.md`

You are running Amanda's daily Blotato queue top-up for The Gentle Muse. Fresh
session, no prior context. Everything you need is in this file.

---

## LOCAL MACHINE CORRECTIONS (verified 2026-09-02, read this first)

This routine was written for a cloud session. It now runs locally on Amanda's
Windows machine. These five facts differ from the original handoff. They are
verified, not assumed.

1. **The repo is already local.** It lives at `D:\Claude Projects\GentleMuse`
   and is already on branch `claude/club-target-game-plan-9xs2du`. Do NOT
   `git fetch origin` / `git checkout` as the first step. Just `git pull`
   (and continue if the pull fails - the local copy is authoritative for a
   local run).
2. **Use `python`, not `python3`.** On this machine `python3` resolves to a
   Microsoft Store stub and fails. `python` is 3.14.5 and works.
3. **The Blotato tool prefix is `mcp__claude_ai_Blotato__`**, e.g.
   `mcp__claude_ai_Blotato__blotato_list_posts`. Verified working headless.
4. **`validate-wave.py` had a Windows-only crash** (it read files with the
   cp1252 default codec and died on UTF-8 content). Fixed 2026-09-02 to read
   UTF-8 explicitly. If it ever crashes again on encoding, that is the bug.
5. **Pushing to GitHub may fail** - there is no credential helper and no `gh`
   CLI on this machine. The local commit is what protects the next run, so a
   failed push is NOT a duplicate risk the way it was in the cloud. Still
   report it.

**The ledger was repaired on 2026-09-02.** `content/wave1-loaded.log` was
empty while 117 of its 196 rows were already live in Blotato, because the
31 Aug cloud run could not push its log. Those 117 ids are now recorded.
Never blank that file.

---

## Where the libraries live

In this repo, on branch `claude/club-target-game-plan-9xs2du`. Not in Google
Drive. The old Drive library never existed past row GM0045, was built in a
sandbox that did not persist, and has been searched for four times. Do not
search Drive for it.

```
content/wave1-staging-library.txt   196 rows, 21 Sep to 29 Oct 2026
content/wave2-staging-library.txt   200 rows, 30 Oct to 8 Dec 2026
content/wave1-loaded.log            append-only record of what is loaded
scripts/validate-wave.py            run before loading anything
```

Wave 1 holds 196 rows, not 200. Four Club Target rows that duplicated the live
queue were removed on 31 Aug. That is correct, not missing data.

Load Wave 1 first. Only start Wave 2 once every Wave 1 row is in the loaded log.

## Step 0. Preflight

Confirm all of these before touching anything, and stop with a named error if
any fails:

* The branch is checked out and the four paths above exist.
* The Blotato MCP tools are reachable. Call `blotato_list_accounts`. If the
  tools are missing, that is the blocker, say so plainly and stop.
* Reconcile the account IDs below against what `blotato_list_accounts`
  actually returns. Trust the live API over this file and report any
  difference.

## Step 1. Read the SOP

Google Doc `SOP_0826_blotato-queue-refill-v3`, id
`1lwmhffyWjkeCcdNzNxPXCqi2VXSSBKLbJyEsoqX2Wp0`. It supersedes v2, which has a
known scheduling bug. If the Drive MCP is not wired up locally, skip it. Every
rule that matters is repeated in this file on purpose.

One live conflict to know about. The SOP v3 says a row's stored time is a
starting point that must be checked against the slot rules and corrected when
it collides or lands at noon. It explicitly retired the older "use the time
exactly as written" instruction. This file's rule below is the reconciled
version. Follow this file.

## Step 2. Validate

```
python scripts/validate-wave.py content/wave1-staging-library.txt
python scripts/validate-wave.py content/wave2-staging-library.txt
```

If any check FAILS, stop, load nothing, and report exactly which check failed.
A failing library is a bug to fix, never something to load around.

## Step 3. Count the queue and measure runway

`blotato_list_posts` with status `["scheduled"]` over a wide window. The result
is large, roughly 120,000 characters, and will be written to a file rather than
returned inline. Parse it with a script. Blotato Starter caps the queue at 200.

Report total scheduled, free slots, and the date and time the queue runs dry,
in Central, labelled. If there are fewer than 10 free slots, load nothing and
report the count in one line.

Baseline measured 09/02/2026 so you can sanity check your own parse: 182
scheduled, 18 free, continuous content through 15 October 2026 at 10:00 AM
Central, then nothing until a single Christmas post on 1 December 2026 at
10:00 AM Central. Empty days inside the run: 12 September, 26 September,
27 September.

## Step 4. Never load a HOLD row

NEVER LOAD A ROW WHOSE ID STARTS WITH "HOLD-". Those are the seasonal campaign
rows: Halloween, Black Friday, Thanksgiving, Small Business Saturday, Cyber
Monday, last call. Unlike every other row they are newly written commercial
copy rather than something Amanda has already published, so she reads them
before they go out.

Skip them silently. But once per run, if any HOLD row falls inside the next 14
days, say so in the report and name the date, so a beat does not slip past
unreviewed. Amanda releases one by dropping the HOLD- prefix herself.

Wave 1 contains 0 HOLD rows. They are all in Wave 2.

## Step 5. Load

Load the remaining rows in ID order, skipping any ID already in
`content/wave1-loaded.log`.

Use each row's scheduledTime as written UNLESS it breaks a slot rule or
collides with something already in the live queue. On a collision, MOVE the
post to the next free slot for that platform. Keep the written time whenever it
is a legal slot and free - do not shuffle a row that did not need moving. Never
skip on a timestamp match, that silently drops real content. Decide "already
loaded?" on the row ID, or failing that on post text, never on platform plus
timestamp.

**Duplicate guard.** Before loading, also check the row's (platform + exact
post text) against the live queue. If that same text is already scheduled on
that same platform, it is a duplicate in the feed even if the id is not in the
log. Skip it and add it to the log. This is the check that caught 117 rows on
2026-09-02.

Slots and daylight saving. Central drops to CST on 1 November 2026, so the UTC
slot changes to hold local time constant.

```
before 1 Nov (UTC-5)   instagram 15:00 and 23:00, tiktok 15:00,
                       facebook 17:10, youtube 17:20, x and linkedin 13:30
from 1 Nov (UTC-6)     instagram 16:00 and 23:00, tiktok 16:00,
                       facebook 18:10, youtube 18:20, x and linkedin 14:30
```

* One post per platform per timestamp, always.
* Instagram max 2 a weekday, 1 at the weekend. A third moves to the next open day.
* Nothing on Instagram between 02:00 and 13:00 UTC.
* Noon Central is retired as a slot. That is 17:00 UTC before 1 Nov, 18:00 UTC after.
* When a slot is contested, Cesa rows win. Cesa is the only format on the
  account that gets shared, 49 shares on one post against 0 to 2 on everything else.

Clock discipline. The libraries and the Blotato API both use UTC. Amanda reads
Central. Always label which clock you mean. A report on 26 August got this
backwards and called 22:50 UTC a late-night slot when it is 5:50 PM Central.

For each row call `blotato_create_post` with the row's platform, text and
mediaUrl. Prepend this to the media filename:

```
https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/
```

Account IDs, VERIFIED LIVE 2026-09-02 against `blotato_list_accounts`:

```
facebook   30840  (pageId 1086399221215093)   The Gentle Muse
instagram  45886  thegentlemuse2026           (mediaType story|reel required)
youtube    36129  (row's title, privacyStatus public, shouldNotifySubscribers false)
tiktok     41488  thegentlemuse2026           (privacyLevel PUBLIC_TO_EVERYONE)
twitter    21430  GentleMuse2026
linkedin   20723  AMANDA KERSH
pinterest   6328  TheGentleMuse2026           <- in the live API, omitted from the handoff
```

Cesa's own connected accounts, VERIFIED LIVE 2026-09-02: TikTok 55761 and
Instagram 65540, both @cesasgoldenyears. If a row targets Cesa's own channel
rather than the main brand, it needs those IDs.

A forward slash in a row's post text means a line break.

Post the text exactly as written. Do not rewrite, do not strip hashtags, do not
remove `#TargetPartner` or `#ad`, never state a price or a discount percentage.
There is an open TikTok Shop violation from 08/04/2026 over misleading pricing,
so this one is not cosmetic.

Two platform bugs that will bite you, both verified 09/01/2026:

* X is not Premium. Anything over 280 characters is rejected outright. Check
  the length before you send it, do not let it fail at the API. Count the text
  AFTER converting each `/` to a line break.
* X video is unreliable. Of 24 X posts attempted since June, 11 failed with
  "Could not upload media to Twitter" and every single failure carried an .mp4.
  Text-only X posts publish clean. Do not silently accept an X video failure,
  count it and name it.

Stop on "maximum number of scheduled posts (200)". Expected, means full, not broken.

## Step 6. Log and commit

Append every loaded row ID to `content/wave1-loaded.log`, one per line with the
date, then commit and push to `claude/club-target-game-plan-9xs2du`:

```
git -c user.email=noreply@anthropic.com -c user.name=Claude
```

This log is the only record of what is loaded. A run that loads posts without
committing the log will cause duplicates next time. Commit locally FIRST, then
attempt the push. If the push fails, say so at the top of the report, but note
that the local commit already protects the next local run.

## Step 7. Report

Write the report to `routines/reports/RPT_MMDD_blotato-refill.md`, and also
save a copy to Google Drive under the same name if the Drive MCP is available
locally.

**If that file already exists, do NOT overwrite it.** Write to
`RPT_MMDD_blotato-refill-HHMM.md` instead, using the local 24 hour time, and
say in the new report which file holds the earlier run. Two runs landed on the
same date on 2026-09-02 and the second one nearly erased the first, which was
the one carrying the action item. Same rule for the Drive copy. Amanda's standing rule is that nothing load-bearing lives only in a
session. Drive is the only layer shared across Claude, Claude Code and Codex.

In her voice: warm, grounded, plain. No em dashes. Digits, not spelled out
numbers. Contractions. No sign-off pleasantries and do not tell her to go get
to work.

Say:

* how many were queued before, and how many free slots
* how many loaded, and the last row ID reached
* the date the queue now runs through, in Central
* any row whose time you moved, and where you moved it to
* any row that failed for a reason other than the 200 cap, with the exact error
* any HOLD row due within 14 days, with its date
* whether the log commit and push actually landed

When both libraries are nearly exhausted, roughly 30 rows left unloaded across
the two, say so and tell Amanda Wave 3 needs building. Never invent or improvise
post content to fill a gap. Never claim something was scheduled that was not.

## Club Target compliance gate (added 09/02/2026)

Verified this day against the live Club Target portal, the Program Terms PDF and
Blotato's automation list. The first two are now HARD GATES in
`scripts/validate-wave.py`. The rest is judgement you have to carry.

* **Never put a Club Target link or tag on the Cesa channel.** Program Terms 2.4:
  "All domains used to post Links must be listed in your 'approved creator'
  profile." `@cesasgoldenyears` is **not** listed, and the portal offers no way to
  add it - Settings carries only profile picture, display name, email and
  password. ENFORCED: the validator fails any row that combines a Cesa marker
  (`cesasgoldenyears`, `cesa-guide.subscribepage.io`, `Comment CESA`) with a Club
  Target marker (`club.target.com`, `#ClubTarget`, `#TargetPartner`).
* **Every "Comment WORD" CTA must name a keyword that has a live automation.**
  A CTA is a promise made in public; if nothing answers the word, the commenter
  gets silence on the best-performing content there is. ENFORCED: the validator
  holds the list of live keywords verified 09/02/2026 and fails the file on any
  other word. The disabled ones - SESSION, PROMO, BUDGET, AI, HIBISCUS, NECKLACE,
  BRACELET - are deliberately absent, because they are the trap.
* **Cesa's keywords are CESA, CONSIDER and SEASONAL**, all on Blotato Instagram
  account `65540`. SOOTHE is a Target body wash keyword on `45886` and is **not**
  a Cesa keyword. Cesa's TikTok (`55761`) has **no automations at all**, so a
  comment-keyword CTA there promises something nothing answers.
* **Both Instagram accounts are under the 500-follower minimum.**
  `@thegentlemuse2026` 184, `@cesasgoldenyears` 48, read from the profiles on
  09/02/2026. Every challenge's rejection list reads verbatim: "Post from accounts
  with less than 500 followers." **TikTok is the only account that clears it** -
  that is why the TikTok-orphan check exists and why it is not negotiable. Of the
  40 challenges open on 09/02, roughly 21 are IG Story or IG Reel/Post and are not
  submittable today at all.
* **A written ruling was requested from `clubtarget@target.com` on 09/02/2026**,
  the channel Program Terms 15.9 prescribes. Three questions: may a second owned
  account be added to the approved creator profile, is the 500 minimum applied
  per-account or per-creator, and may distinct content from a second approved
  account be entered into different challenges. **Do not relax the Cesa gate until
  that reply lands and says yes.** If it says the minimum is per-creator, the whole
  Instagram lane reopens and this section needs rewriting.

---

## Standing rules that outrank convenience

* Never declare something impossible or manual-only off one failed method. Try
  the API, the MCP, and browser control before reporting a blocker, and when
  you do report one, name exactly which methods you tried and what each one
  failed with.
* Never hand over a link, ID or account detail that has not been verified this
  run. If it is not confirmed, label it MUST VERIFY and name where it gets
  confirmed.
* Verified links, use only these: Consider This
  `https://consider-this.subscribepage.io`, AI Guide
  `https://ai-guide.subscribepage.io`, Press Play
  `https://press-play.subscribepage.io`, Reset Guide
  `https://payhip.com/b/9FE2U`, Essentials
  `https://www.gentlemuse.co/tiktok`, Cesa `instagram.com/cesasgoldenyears`.
* Dead, do not use: `reset-guide.subscribepage.io` is a different creator,
  `preview.mailerlite.io/...` was replaced 08/18/2026,
  `gentlemuse.co/reset-guide` 503s and Wix is being left.
