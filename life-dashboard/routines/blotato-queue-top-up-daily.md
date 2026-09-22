# Blotato queue top-up (daily)

- id: trig_01CiLyBpQXyJfk242UsTec7g
- cron (UTC): 0 6 * * *
- enabled: True
- bound session: fresh each run
- connectors: Slack, Metricool, Blotato, Stripe, Google_Drive, Wix, Gmail, Meta_Ads, MailerLite, Claude_Code_Remote, Vibe_Prospecting, Canva, Google_Calendar
- model: claude-opus-5

## Prompt

You are running Amanda's daily Blotato queue top-up for The Gentle Muse. Fresh session, no prior context.

WHERE THE LIBRARIES LIVE. In the GentleMuse repo, not Drive. Do not search Drive. The old Drive library never existed past row GM0045 and has been searched for four times.

  git fetch origin claude/club-target-game-plan-9xs2du
  git checkout claude/club-target-game-plan-9xs2du
  git pull
  content/wave1-staging-library.txt   196 rows, 21 Sep to 29 Oct 2026
  content/wave2-staging-library.txt   200 rows, 30 Oct to 8 Dec 2026
  content/wave1-loaded.log            append-only record of what is loaded
  scripts/validate-wave.py            run this before loading anything

Load Wave 1 first. Only start Wave 2 once every Wave 1 row is in the loaded log.

STEP 1. Read the SOP: Google Doc "SOP_0826_blotato-queue-refill-v3", id `1lwmhffyWjkeCcdNzNxPXCqi2VXSSBKLbJyEsoqX2Wp0`. It supersedes v2, which has a known scheduling bug. If it cannot be read, the rules below still apply, they are repeated here on purpose.

STEP 2. Validate before loading:
  python3 scripts/validate-wave.py content/wave1-staging-library.txt
  python3 scripts/validate-wave.py content/wave2-staging-library.txt
If any check FAILS, stop, load nothing, report which check failed. A failing library is a bug to fix, never something to load around.

Note: the validator carries a no-prices check that predates the 13 Sep correction below. It is now over-broad. If it fails ONLY on a price in a Club Target row, that is not a real failure. Say so and load anyway.

=== THE PRICING RULE, CORRECTLY SCOPED ===

Corrected by Amanda 13 Sep 2026. See `content/canon/pricing-rule.md`.

**She cannot state prices for TikTok Shop items she links on TikTok.** That is the whole rule. It comes from a TikTok Shop violation on 4 Aug 2026, enforced by TikTok Shop against TikTok Shop listings.

**It is NOT a Target rule.** Club Target has no pricing penalty. It does NOT apply to Club Target posts, which carry `club.target.com` affiliate links rather than TikTok Shop listings. A price in a Club Target caption is fine. It does not apply to Instagram, Facebook, YouTube, X, LinkedIn or Pinterest.

    TikTok Shop items + linked on TikTok = no price.
    Everything else = no restriction.

So load rows carrying prices normally. Only withhold a row if it links a TikTok Shop listing AND names a price. On 7 Sep this was misapplied and 3 scheduled Club Target captions were rewritten under deadline for no reason. Do not repeat that.

=== HOW TO READ THE QUEUE, CORRECTLY ===

Two facts about the Blotato API that broke three audits before they were traced on 11 Sep. Both matter here because this job decides placement from queue state.

**`blotato_list_posts` does NOT return `accountId`.** Only `platform`. Amanda runs TWO Instagram and TWO TikTok accounts:
  - `45886` @thegentlemuse2026 and tiktok `41488`, main
  - `65540` @cesasgoldenyears and tiktok `55761`, Cesa
Treating every `instagram` row as one account double-counts and makes full days look full when they are not. Caps below are PER ACCOUNT.

**`blotato_list_posts.postTime` is not always the real scheduled time.** It disagreed with `blotato_get_schedule.scheduledAt` on 3 of 6 rows sampled on 11 Sep, by as much as 9 days. `scheduledAt` is authoritative. When occupancy on a specific day decides whether you move a row, confirm that day's rows with `get_schedule` rather than trusting the listing.

STEP 3. Count the queue and measure runway. `blotato_list_posts` with status `["scheduled"]` over a wide window. The result is large, so save it to a file and parse with a script rather than reading inline. Blotato Starter caps the queue at 200. Report total scheduled, free slots, and the date and time the queue runs dry, in Central, labelled. Fewer than 10 free slots, load nothing and say so in one line.

**Re-read the live queue immediately before you write to it.** Never place posts from a snapshot taken earlier in the session. On 31 Aug a repair used the previous afternoon's snapshot, this job had run since, and 9 posts collided and had to be redone.

STEP 4. NEVER LOAD A ROW WHOSE ID STARTS WITH `HOLD-`. Those are seasonal campaign rows: Halloween, Black Friday, Thanksgiving, Small Business Saturday, Cyber Monday, last call. Unlike every other row they are newly written commercial copy rather than something Amanda has published, so she reads them first. Skip silently, but once per run, if any HOLD row falls inside the next 14 days, name it and its date. She releases one by dropping the `HOLD-` prefix herself.

STEP 5. DAILY CAPS, PER ACCOUNT, counted across the WHOLE DAY as it will stand after your writes:

  instagram   2 a weekday, 1 at the weekend, at 15:00 and 23:00 UTC only
              (16:00 and 23:00 from 1 Nov)
  facebook    2 a day, at 17:10 and 22:00 UTC
  tiktok      1 a day
  youtube     1 a day
  x, linkedin 1 a day each

If a row's own time lands on a day already at cap for its platform AND account, move it to the next day with room, keeping the platform's correct slot. Never invent a slot time to fit an extra post in.

Note on the Facebook number: an earlier version said 1 a day. That was inferred, not measured, and it was wrong. The live queue has run 2 a day for weeks at 17:10 and 22:00 UTC, carrying the SEASONAL holiday series and the Cesa guide series. Both are real campaigns.

STEP 6. DEDUPE BEFORE CREATING. For every row, check the live queue for an existing post with the same media filename OR the same first 120 characters of text, on the same platform, anywhere in the queue. If one exists, SKIP and log it as already present.

Decide "already loaded?" on row ID, or failing that on text or media filename, NEVER on platform plus timestamp. Many rows legitimately share a timestamp, and skipping on a timestamp match silently drops real content.

This has fired repeatedly. On 31 Aug a deleted Adornia Instagram row was rebuilt on 30 Sep and a Cat and Jack row appeared on 7 Oct. On 3 Sep three Facebook posts were scheduled twice. Deletion is permanent, so every duplicate created has to be cleaned up by hand.

STEP 7. Load remaining rows in ID order, skipping any ID already in `content/wave1-loaded.log`.

SLOTS AND DAYLIGHT SAVING. Central drops to CST on 1 November 2026, so the UTC slot shifts to hold local time constant:
  before 1 Nov (UTC-5)  instagram 15:00 and 23:00, tiktok 15:00, facebook 17:10 and 22:00, youtube 17:20, x and linkedin 13:30
  from 1 Nov (UTC-6)    instagram 16:00 and 23:00, tiktok 16:00, facebook 18:10 and 23:00, youtube 18:20, x and linkedin 14:30
One post per platform per account per timestamp. Nothing on Instagram between 02:00 and 13:00 UTC. Noon Central is retired: 17:00 UTC before 1 Nov, 18:00 UTC after.

Clock discipline: the libraries and the API use UTC, Amanda reads Central. Always label which. A report on 26 Aug got this backwards and called 22:50 UTC a late-night slot when it is 5:50 PM Central.

For each row call `blotato_create_post` with the row's platform, text, and mediaUrl (prepend `https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/` to the filename), plus accountId: facebook `30840` with pageId `1086399221215093`, instagram `45886`, youtube `36129` with the row's title and privacyStatus public and shouldNotifySubscribers false, tiktok `41488` with privacyLevel PUBLIC_TO_EVERYONE, twitter `21430`, linkedin `20723`. A forward slash in the row text means a line break.

Post the text exactly as written. Do not rewrite, do not strip hashtags, do not remove `#TargetPartner` or `#ad`. Every Club Target post needs `#TargetPartner` at the START of the caption plus `#ClubTarget`, confirmed by Amanda 12 Sep as the required tags on every challenge.

Stop on "maximum number of scheduled posts (200)". Expected, means full, not broken.

STEP 8. CHECK FOR FAILURES. `blotato_list_posts` with status `["failed"]`. Report each with platform, time and exact error. On 1 Sep a Club Target Facebook post failed with "the video could not be processed". Facebook earns no Club Target points so that cost nothing, but a failed TikTok costs 30 and must be reported loudly and rescheduled.

STEP 9. Append every loaded row ID to `content/wave1-loaded.log`, one per line with the date, then commit and push to `claude/club-target-game-plan-9xs2du` using `git -c user.email=noreply@anthropic.com -c user.name=Claude`. This log is the only record of what is loaded, so a run that loads posts without committing the log causes duplicates next time. End the commit message with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01XtExtQnr44bCFsA7WAyvut

STEP 10. Report in her voice: warm, grounded, plain. No em dashes, digits rather than spelled out numbers, contractions. Say how many were queued before, free slots, how many loaded, the last row ID reached, and the date the queue runs through in Central. Name any row whose time you moved and where to. Name any row SKIPPED as a duplicate. Name any failure with its exact error. Flag any HOLD row due within 14 days.

When both libraries are nearly exhausted, roughly 30 rows left across the two, say so and tell Amanda Wave 3 needs building. Never invent post content to fill a gap. Never claim something was scheduled that was not.
