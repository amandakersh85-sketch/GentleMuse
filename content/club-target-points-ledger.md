# Club Target Points Ledger

Started 21 Aug 2026. This is the source of truth for the points reconciliation.
The Drive doc "Club Target Points Ledger, GM" is a stub only. The Drive connector
can create files but cannot append to a Google Doc, so entries live here.

## Why this exists

On 21 Aug 2026 Amanda turned on Instagram distribution for all Club Target content,
before crossing the 500-follower mark, to test whether posts credit anyway.
Every theme is worth 75 points, split three ways:

| Placement | Points | Link goes |
| --- | --- | --- |
| TikTok | 30 | in the caption |
| Instagram Reel | 30 | in the bio |
| Instagram Story | 15 | link sticker |

TikTok alone collects 30 of every 75. The Sunday/Wednesday audit reconciles what
posted against what the portal actually credits, and flags any Instagram gap fast:
a gap there is the answer to the follower-threshold question.

## Baseline

- Portal total 17 Aug 2026 weekly sweep: **304 points** (Insider tier 3, gate to Trendsetter 4 at 500)
- Handle: `amanda.20` · Storefront: `club.target.com/a/amanda.20`

## Entry format

```
=== AUDIT [date] ===
Posts found (platform | date | theme | expected pts)
Stories (not visible to schedulers, ask Amanda)
Expected total added since last audit
Portal total reported by Amanda (or PENDING)
Verdict: CREDITED IN FULL / GAP FLAGGED / PENDING
Notes
```

---

## === AUDIT 23 Aug 2026 (first run) ===

### Published, found via Blotato

**TikTok, 9 posts, 30 points each = 270**

| Date | Theme hashtag | Product |
| --- | --- | --- |
| 20 Aug | #TargetEverydayEssentials | FlavCity variety pack, butter coffee flavor |
| 20 Aug | #HeyDayTechAugust | heyday phone cases, cosmic pink MagSafe |
| 21 Aug | #TargetLunchThrowback | Cinnamon Toast Crunch, soup, cheese |
| 21 Aug | #TargetBudgetFinds | Cat and Jack |
| 21 Aug | #TargetFave | NYX fat oil body line |
| 21 Aug | #TargetFallFirstLooks | Sweaters, skirts, cardigan |
| 21 Aug | #TargetCollegeMVPs | Native, Raw Sugar, dorm apparel |
| 21 Aug | #TargetPetFaves | Freshpet |
| 21 Aug | #TargetGoodandGatherFaves | Good and Gather cookbook |

**Instagram Reels, 4 posts, 30 points each = 120**

| Date | Theme hashtag |
| --- | --- |
| 21 Aug | #TargetFallFirstLooks |
| 21 Aug | #TargetCollegeMVPs |
| 21 Aug | #TargetPetFaves |
| 21 Aug | #TargetGoodandGatherFaves |

**Expected total added since baseline: 390 points.**
If all of it credits: 304 + 390 = 694, which clears the 500 gate to Trendsetter 4.

### GAP FLAGGED, distribution not credit

Five TikToks have no Instagram Reel published **and none scheduled**:

- #TargetEverydayEssentials (FlavCity, butter coffee)
- #HeyDayTechAugust (heyday cases)
- #TargetLunchThrowback
- #TargetBudgetFinds (Cat and Jack)
- #TargetFave (NYX fat oil)

That is **150 points of Instagram Reels sitting unclaimed** against the 21 Aug
decision that everything ships three ways. The fix is a re-post of the same
video with the Reel caption, not new filming.

Only 2 Club Target Reels are queued ahead: Cat and Jack Summer (29 Aug) and the
Adornia necklace (3 Sep). Neither closes the five above.

### Stories

Zero Instagram Stories observed. Stories never pass through Blotato or Metricool,
so this is a question, not a finding: **13 published posts x 15 points = up to 195
more points** available if Stories went up or go up. Amanda to confirm.

### Portal total

**PENDING.** Nothing on the Claude side can log in to club.target.com. Amanda to
report the current total so the 390 can be confirmed as credited, and so any
Instagram shortfall becomes visible.

### Verdict

**PENDING on credit, GAP FLAGGED on distribution.**

### Notes

- No post used a comment keyword CTA, so the unwired HIBISCUS and SOAK traps were not tripped.
- Keyword note carried forward: BUTTER in ManyChat maps to Tree Hut Moroccan Rose body butter, not the FlavCity butter coffee flavor. Do not use "comment BUTTER" on the coffee video.
- Still to verify at Amanda's desk: `Verify-TargetClubSku.ps1 -Sku 89094549` for the HIBISCUS scrub DM link (two-signal rule).

---

## === AUDIT 26 Aug 2026 ===

### Posts found since last audit

**None.** Zero Club Target posts published 23 to 26 Aug on any platform.
Checked Blotato (published, all platforms, 78 posts in window, 0 matching
`#TargetPartner` / `#ClubTarget` / `club.target.com`) and cross-checked
Metricool IG Reels analytics for the same window to catch native phone posts.
Metricool shows 20 Reels published, none of them Club Target product posts.
This is a confirmed zero, not a scheduler blind spot.

Two 23 Aug Reels carry `#TargetPartner` but are follower-campaign posts with no
challenge theme hashtag, so they are **not counted** toward any theme.

**Expected points added this run: 0.**

### Distribution cross-check

The five TikToks from the 23 Aug audit remain **unmatched** — no Reel published,
none scheduled. Still 150 points unclaimed:

- #TargetEverydayEssentials · #HeyDayTechAugust · #TargetLunchThrowback
- #TargetBudgetFinds · #TargetFave

Only two Club Target Reels are queued: Cat and Jack (31 Aug) and Adornia
necklace (3 Sep). Neither closes any of the five. Unchanged from last week.

### Portal total — partial reading, and why it does not settle it

Amanda reported on 25 Aug: **Trendsetter tier 4, 656 points to tier 5.**
That confirms the total is at or above 500, but it does **not** isolate whether
Instagram credited, because the TikToks alone clear the gate:

| Scenario | Arithmetic | Total |
| --- | --- | --- |
| TikToks credit, Reels do **not** | 304 + 270 | **574** |
| Both credit | 304 + 390 | **694** |

Both present as tier 4 externally. The exact number is the discriminator and the
gap is 120 points. **574 means Instagram does not credit below 500 followers.
694 means it does.**

Context that makes this a live test: Amanda is at roughly 162 followers as of
24 Aug (62 → 139 → 162), did not reach 500 by the original deadline, and moved
the deadline to 13 Sep. The 4 Reels published 21 Aug were therefore posted well
under the supposed threshold.

### Stories

Unchanged and still unanswered. Up to 195 points (13 posts x 15) if any went up.
Invisible to both schedulers.

### Verdict

**PENDING on credit** — needs the exact portal number, not the tier.
**GAP FLAGGED on distribution** — 150 points, carried over, unchanged.

### Notes

- **CORRECTION, same day.** The note first filed here said new posts were landing
  at 22:50, 23:30 and 13:20 and called those the weakest hours on the chart.
  That was wrong. Those are UTC values straight off the Blotato API, and Central
  is UTC minus 5 during CDT, so they are 5:50 PM, 6:30 PM and 8:20 AM Central.
  All three are reasonable slots. No action was needed and none was taken.
- The real scheduling defect, found while checking the above: the staging library
  hardcodes `T17:00` for every Instagram row, which is **noon Central**, and stacks
  4 and 5 rows on the identical timestamp (GM0002 to GM0005 all at
  `2026-08-28T17:00`, GM0006 to GM0009 all at `2026-08-29T17:00`). That is the
  source of the five-at-noon pileup cleaned up on 24 Aug, and SOP v2's slot table
  said `instagram 17:00`, so the next wave load would have recreated it.
  Fixed at source on 26 Aug: SOP v3 published with corrected slots (Instagram
  15:00 UTC primary, 23:00 UTC secondary, one post per platform per timestamp),
  and the daily top-up routine repointed at v3 with the slot rules inlined.
- Carried forward, still open: BUTTER maps to Tree Hut body butter in ManyChat,
  not the FlavCity coffee flavor. And `Verify-TargetClubSku.ps1 -Sku 89094549`
  still needs a run at Amanda's desk for the HIBISCUS DM link.

---

## === AUDIT 30 Aug 2026 (deadline-day check) ===

Triggered by a deadline reminder naming three themes as unexecuted:
Everyday Pet Favorites, Fresh Home Finds, Game Day Throwback.

### The reminder is wrong on one of the three

**Everyday Pet Favorites is NOT unexecuted.** `#TargetPetFaves` (Freshpet)
published 21 Aug on both placements:

| Placement | Status | Proof |
| --- | --- | --- |
| TikTok | published | `tiktok.com/@thegentlemuse2026/video/7676615071606344973` |
| Instagram Reel | published | `instagram.com/reel/DcUd68_DkyR/` |
| Instagram Story | **not found** | invisible to schedulers, phone only |

60 of 75 already banked. Only the Story (15) is open. Do not reshoot this.

**Fresh Home Finds: confirmed zero.** No post carrying a Fresh Home Finds
hashtag exists, published or scheduled, on any platform.

**Game Day Throwback: confirmed zero.** `#TargetLunchThrowback` (Cinnamon Toast
Crunch, 21 Aug, TikTok only) is the back-to-school lunch theme, not Game Day.
It does not count toward it.

### Larger unclaimed balance found in the same sweep

Five TikToks still have no Instagram Reel. **150 points, zero filming required**
— the video files are already hosted and the captions already exist:

| Theme | Product | Media asset |
| --- | --- | --- |
| #TargetFave | NYX fat oil body line | `a484faa6-3a3e-4338-9ac1-9bfbd0fd3d45.mp4` |
| #TargetBudgetFinds | Cat and Jack | `19d97015-9c59-438d-9572-a9f82d5f53ed.mp4` |
| #TargetLunchThrowback | Cinnamon Toast Crunch | `95acfd10-7bef-4fd9-b12d-e423d95d9d0a.mp4` |
| #HeyDayTechAugust | heyday phone cases | `571b6622-af72-4588-ab35-fecde3c2bbc3.mp4` |
| #TargetEverydayEssentials | FlavCity variety pack | `0d080199-8ee2-47c3-b740-4ac026c86486.mp4` |

All on `database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/`.

**Caveat, not yet resolved:** these themes ran 20 to 21 Aug. Whether they are
still open on 30 Aug cannot be checked from here, `club.target.com` is blocked
by the egress proxy. Amanda has to read the portal. If they are closed, posting
them now credits 0 and burns 5 Instagram slots.

### Defect found, live on both platforms

The Freshpet caption reads **"Cesa is 13 and she has opinions."** She is 19.
Live on the 21 Aug TikTok and Instagram Reel, and it contradicts every other
post in the account and the guide. Fixable by editing the caption in-app.

### Verdict

**GAP CONFIRMED** on Fresh Home Finds (75) and Game Day Throwback (60).
**PARTIAL** on Everyday Pet Favorites, 60 of 75, Story outstanding.
**PENDING PORTAL** on the 5 unmatched Reels, 150 points, blocked on theme
windows only Amanda can see.

---

## === RESOLVED 30 Aug 2026: the Instagram credit question ===

Amanda confirmed: **no credit on Instagram until 500 followers.**

That settles the test that has been PENDING since 23 Aug. Of the two scenarios:

| Scenario | Arithmetic | Total |
| --- | --- | --- |
| **TikToks credit, Reels do not** | 304 + 270 | **574** ← confirmed |
| Both credit | 304 + 390 | 694 |

**Portal total is 574.** The 21 Aug experiment is concluded and the answer is no.

### What this changes

The 75-point theme split is not available to her. Until she crosses 500 followers,
every theme is worth **30 points, not 75**:

| Placement | Points | Status below 500 followers |
| --- | --- | --- |
| TikTok | 30 | **the only one that pays** |
| Instagram Reel | 30 | 0 |
| Instagram Story | 15 | 0 |

Consequences to carry into every future audit and game plan:

- The "150 points unclaimed on 5 unmatched Reels" figure logged on 23 Aug,
  26 Aug and earlier today is **void**. Those Reels were never worth anything.
  Do not chase them.
- The Instagram Story line item is worth 0. Stop putting it on the task list.
- Today's three themes are worth **30 each, 90 total**, not 210.
- Everyday Pet Favorites is **fully complete at 30 of 30**, not 60 of 75.
  The TikTok published 21 Aug is the entire available value of that theme.
- Instagram distribution of Club Target content still has value for follower
  growth, which is the actual gate. It just has no points value yet.

### TikTok execution status, 30 Aug

Amanda asked for the TikTok uploads to be executed. Checked every Club Target
asset in the account:

| Theme | TikTok | Note |
| --- | --- | --- |
| #TargetEverydayEssentials | published 20 Aug | done |
| #HeyDayTechAugust | published 20 Aug | done |
| #TargetLunchThrowback | published 21 Aug | done |
| #TargetBudgetFinds | published 21 Aug | done |
| #TargetFave | published 21 Aug | done |
| #TargetFallFirstLooks | published 21 Aug | done |
| #TargetCollegeMVPs | published 21 Aug | done |
| #TargetPetFaves | published 21 Aug | done |
| #TargetGoodandGatherFaves | published 21 Aug | done |
| #TargetCatandJackSummer | scheduled 2 Sep | footage exists |
| #TargetLittleFinds | Adornia, in Wave 1 for 1 Oct | footage exists |
| **Fresh Home Finds** | **none** | **no footage exists** |
| **Game Day Throwback** | **none** | **no footage exists** |

**Nothing was uploaded, because there is nothing to upload.** Every Club Target
video asset in the library is already published or already scheduled. Fresh Home
Finds and Game Day Throwback were never filmed. They cannot be posted without a
store run.

### Defect flagged, not actioned

The Cat and Jack TikTok is scheduled **twice** with identical media and caption:
post `3630587` on 2 Sep and post `3939647` on 24 Sep. Same asset
`600306c6-0606-4d93-a38b-690b4320de1f.mp4`. The second is a Wave 1 row that
duplicated a pre-existing queue entry. Only one can credit the theme, and TikTok
may suppress the repeat. Deletion in Blotato is permanent, so this is flagged for
Amanda's call rather than actioned.

---

## === AUDIT 31 Aug 2026, 00:08 UTC (Sun/Wed routine) ===

Window checked: 25 Aug to 25 Sep, published and scheduled, all platforms, 250 rows
plus a second page to 31 Oct. The queue holds nothing after 25 Sep, so the window
is complete in practice.

### 1. TikTok coverage: NO GAPS

| Theme | TikTok | Also on |
| --- | --- | --- |
| #TargetCatandJackSummer | scheduled 2 Sep, post `3630587` | facebook, instagram |
| #TargetLittleFinds | scheduled 3 Sep, post `3952005` | facebook, instagram |

The Adornia TikTok scheduled earlier today is confirmed live in the queue. The
gap found on 30 Aug is closed.

### 2. Points added since last audit: 0

No Club Target post published in the window. 18 posts published since 30 Aug
00:00 UTC, all Cesa, newsletter and evergreen. **Running total unchanged at 574.**

Fresh Home Finds and Game Day Throwback expired unfilmed. Amanda decided on
30 Aug not to make a store run. 60 points forgone, recorded as a deliberate call.

### 3. Duplicates: 4 pairs, 3 of them urgent

Identical caption and media, scheduled twice:

| Platform | Post | When | Paired with |
| --- | --- | --- | --- |
| instagram | Cesa, "Coming home to her after a long shift" | 1 Sep 15:00 | 1 Sep 16:30 |
| instagram | Cesa, "She's 19. Every strange sleeping position" | 4 Sep 18:30 | 4 Sep 18:50 |
| instagram | Cesa, "10 of her years have been mine" | 4 Sep 19:45 | 4 Sep 20:05 |
| instagram | Adornia #TargetLittleFinds | 3 Sep 17:00 | 24 Sep 15:00 |

The three Cesa pairs post the same words **20 to 25 minutes apart**. Blotato
deletion is permanent, so nothing was deleted. Needs Amanda's call.

The Adornia pair is not a points issue, Instagram pays 0, but it repeats a paid
partnership post 3 weeks apart.

### 4. NEW DEFECT: the retired noon slot is still in the live queue

The 17:00 UTC slot is noon Central. It was retired at source on 26 Aug when SOP v3
shipped, but **only for new waves**. Every pre-existing queue row from 31 Aug to
20 Sep still carries it, so noon Central fires every single day for 3 weeks.

Instagram is over its own cap on 8 consecutive days:

| Date | IG posts | Cap | Times, UTC |
| --- | --- | --- | --- |
| 31 Aug Mon | 4 | 2 | 15:00, 17:00, 17:30, 23:00 |
| 1 Sep Tue | **7** | 2 | 00:00, 15:00, 16:30, 17:30, 18:50, 20:00, 22:50 |
| 2 Sep Wed | 4 | 2 | 15:00, 17:00, 20:00, 22:50 |
| 3 Sep Thu | 3 | 2 | 17:00, 22:50, 23:00 |
| 4 Sep Fri | **7** | 2 | 17:00, 17:00, 18:30, 18:50, 19:45, 20:05, 22:50 |
| 5 Sep Sat | 2 | 1 | 17:00, 17:00 |
| 6 Sep Sun | 3 | 1 | 17:00, 22:50, 23:00 |
| 7 Sep Mon | 3 | 2 | 17:00, 22:50, 23:00 |

Two exact-minute collisions: instagram 4 Sep 17:00 x2 and 5 Sep 17:00 x2.

From 8 Sep the queue settles to 1 or 2 a day, and from 21 Sep the Wave 1 rows use
the corrected 15:00 and 23:00 slots. So the damage is bounded to the next 8 days.

Flagged, not actioned. Spreading these and removing the duplicates is one job and
it needs Amanda's yes on the deletions.

### 5. Queue runs dry after 25 Sep

Nothing scheduled beyond 25 Sep 23:00. Wave 1 covers 21 Sep to 29 Oct in the
staging file but was only loaded through 25 Sep, and Wave 2 is not loaded at all.
**This is the same partial load that ate the Adornia TikTok.** 34 days of written,
validated content is sitting in the repo unloaded.

### 6. Theme board: still empty

`content/club-target-theme-board.md` has never been filled from the portal. Two
themes expired this week because nothing was written down. The ask stands:

> Open the Club Target portal and paste the theme list. For each one:
> theme name, exact hashtag, closing date.

### Verdict

**CLEAN** on TikTok coverage, the 30 Aug gap is closed.
**NO CHANGE** on points, 574.
**ACTION NEEDED** on 3 duplicate Instagram pairs and 8 days of noon-slot overload.
**BLOCKED** on the theme board, which is the root cause of the 60 points forgone.

### Queue repair executed 31 Aug, on Amanda's go

- **Deleted 6 duplicate scheduled posts.** 3 Cesa Instagram pairs firing 20 to 25
  minutes apart (`3926378`, `3926388`, `3927279`), the Adornia Instagram repeat
  (`3939642`), and 2 rows the daily top-up regenerated mid-repair: another Adornia
  Instagram on 30 Sep (`3970796`) and a Cat and Jack Instagram on 7 Oct
  (`3970869`).
- **Rescheduled 37 Instagram posts** onto the corrected slots, 15:00 and 23:00 UTC
  (10 AM and 6 PM Central), 2 a weekday and 1 at the weekend. The 17:00 UTC noon
  Central slot is now cleared from 31 Aug through 7 Sep. Overflow runs through
  12 Oct, which also extends the Instagram queue past the 25 Sep dry date.
- **Removed 4 Club Target rows from wave 1** (GW0019, GW0021, GW0055, GW0057).
  Every one repeated content already scheduled. Leaving them in the library made
  the daily top-up rebuild them after deletion, which is why 2 came back during
  this repair. Removing them at source stops the loop.

**Process note for future runs.** The first pass of this repair moved 9 posts onto
26 Sep to 1 Oct using a queue snapshot taken the previous afternoon. The daily
top-up had run at 06:40 UTC that morning and already filled those days, so the
moves collided and had to be redone against a fresh read. **Re-read the live queue
immediately before writing to it, never from a snapshot taken earlier in the
session.**

---

## === AUDIT 3 Sep 2026, 00:09 UTC (Sun/Wed routine) ===

Window 30 Aug to 2 Nov, published and scheduled, all platforms, 218 rows, no
pagination cursor, so the window is complete.

### Points added: +30. Running total 604.

**#TargetCatandJackSummer TikTok published 2 Sep, 10 AM Central.** That is the
first Club Target point earned since 21 Aug.

| | |
| --- | --- |
| Baseline 17 Aug | 304 |
| 9 TikToks, 20 to 21 Aug | 270 |
| Cat and Jack TikTok, 2 Sep | 30 |
| **Total** | **604** |

`#TargetLittleFinds` (Adornia) TikTok is scheduled 3 Sep at 6 PM Central,
post `3952005`. Something moved it off the 10 AM slot it was created on. It is
still inside 3 Sep so the theme is not at risk. Worth 30 when it lands, taking
her to 634.

### 1. TikTok coverage: NO GAPS

Both live themes carry a TikTok. Nothing is one-sided.

### 2. A Club Target post FAILED

Facebook, 1 Sep 00:59 UTC, the Cat and Jack `#ad` video:

> Could not upload video to Facebook: the video could not be processed

**Cost 0 points**, Facebook earns nothing in this program, and the TikTok and
Instagram versions of the same theme both went out fine. Logged because the same
failure on a TikTok row would cost the full 30 and must never pass unnoticed.
The daily top-up now checks the failed queue every run.

### 3. Duplicates: 3 new pairs, all Facebook, all regenerated

| Text | Scheduled | And again |
| --- | --- | --- |
| Every weird sleeping position gets a 3 second stare | 11 Sep | 28 Sep |
| Your sponge isn't sanitized after microwaving | 22 Sep | 27 Sep |
| 5 books that are free forever | 21 Sep | 26 Sep |

Same regeneration fault that produced the Adornia and Cat and Jack Instagram
duplicates on 31 Aug, now on Facebook. Deletion is permanent so these are flagged
for Amanda, not removed.

### 4. REGRESSION: Instagram is over cap on 15 straight days again

The 31 Aug respread put Instagram on 2 a weekday and 1 at the weekend. **Two daily
top-up runs have undone it.** 68 Instagram rows are scheduled and 15 consecutive
days from 3 Sep to 16 Sep exceed the cap, peaking at 5 on 3 Sep.

Worse, the new rows are on times that are not slots at all: **16:30, 20:00, 22:00
and 22:30 UTC**, alongside the retired 17:00 noon Central. The SOP allows only
15:00 and 23:00.

Hand-fixing this a second time is pointless while the generator keeps re-breaking
it, so the fix went in at source instead. The daily top-up prompt now carries:

- **Hard daily caps counted across the WHOLE DAY** as it will stand after its
  writes, not just its own additions, for every platform.
- **Only 15:00 and 23:00 UTC for Instagram.** Inventing a slot to fit an extra
  post in is now explicitly banned, with 16:30, 20:00 and 22:30 named.
- **Dedupe before creating**, on media filename or the first 120 characters of
  text, anywhere in the queue, not just at the same timestamp.
- **Re-read the live queue immediately before writing**, never from an earlier
  snapshot.
- **Check the failed queue every run** and report each failure with its error.

The respread itself still needs doing once, after the next top-up runs clean.
Holding for Amanda rather than fixing it a third time into the same fault.

### 5. Queue health

165 posts scheduled, running through 14 Oct. No longer at risk of running dry.

### Verdict

**+30 BANKED**, total 604, 634 once Adornia lands 3 Sep.
**CLEAN** on TikTok coverage.
**ACTION NEEDED** on 3 Facebook duplicates and the Instagram cap regression.
**ROOT CAUSE FIXED** in the top-up routine, pending its next run.

### Facebook duplicates removed 3 Sep, on Amanda's go

Deleted `4056369`, `4056322`, `4056285`. Re-read the Facebook queue afterwards
and confirmed all 3 pairs are gone, one copy of each survives:

| Kept | Fires |
| --- | --- |
| Every weird sleeping position, `3732505` | 11 Sep |
| Your sponge isn't sanitized, `3939608` | 22 Sep |
| 5 books that are free forever, `3939602` | 21 Sep |

### Correction to log against myself

The 3 Sep audit wrote a hard cap of **1 Facebook post a day** into the daily
top-up routine. That number was inferred, not measured. Reading the live Facebook
queue afterwards shows it has been running **2 a day for weeks**, at 17:10 and
22:00 UTC, and the 22:00 posts are a deliberate series: the SEASONAL holiday run
(`4055xxx`) and the Cesa guide run (`4059xxx`). Both are real campaigns, not
duplicates.

So the cap is wrong and 22:00 UTC is a legitimate second Facebook slot, 5 PM
Central. Left as-is for one cycle rather than pushing a third prompt rewrite in
an hour. The top-up only places NEW rows, it never moves existing posts, so the
worst this can do is defer a newly loaded Facebook row by a day. Checking the
06:00 UTC run on the Sunday audit and correcting the number then.

The Instagram rules from the same edit stand. Those were measured, not inferred:
15 consecutive days over cap on times that are not slots at all.

---

## === AUDIT 7 Sep 2026, 00:09 UTC (Sun/Wed routine) ===

Window 2 Sep to 6 Nov, 249 rows, no pagination cursor. Complete.

### The store run worked. +60. Running total 694.

Amanda filmed on 5 and 6 Sep and 2 new themes are published on TikTok:

| Theme | Published | Link |
| --- | --- | --- |
| #TargetLaborDayFind | 5 Sep 2:24 PM Central | `7682133897622179086` |
| #TargetActiveStyle | 6 Sep 10:18 AM Central | `7682441762052377869` |

**304 baseline + 390 from 13 themes = 694.** That crosses the number the 30 Aug
test predicted for the both-credit scenario, by TikTok alone.

Three more Target TikToks are queued, worth up to 90:

| Theme | Fires | Product |
| --- | --- | --- |
| #TargetQuickMeals | 8 Sep, 7 PM Central | Good and Gather chopped salad kits |
| #TargetFave | 9 Sep, 7 PM Central | Tree Hut pink hibiscus scrub |
| #TargetHomeForFall | 10 Sep, 7 PM Central | glass pumpkins, Threshold candle |

### URGENT: 4 posts state prices. This is the standing hard rule.

Amanda has an open TikTok Shop violation from 4 Aug 2026 over misleading pricing.
The rule is never state a price. Four Club Target posts break it:

| Post | Status | The text |
| --- | --- | --- |
| `6776742` #TargetLaborDayFind | **ALREADY PUBLISHED** 5 Sep | "buy 1 get 1 25% off" |
| `4059738` no theme tag | fires 7 Sep 6 PM Central | "50% clearance", "$2.99" |
| `4158113` #TargetQuickMeals | fires 8 Sep 7 PM Central | "dinner for $3.89" |
| `4158117` #TargetHomeForFall | fires 10 Sep 7 PM Central | "glass pumpkins at $15" |

`scripts/validate-wave.py` fails on exactly these two patterns, a dollar figure and
a percent off. These posts did not come through the wave library so they never hit
the validator.

### Second problem: #ad is missing

Every new post carries `#TargetPartner` but **not `#ad`**. Every earlier Club Target
post carried both. That is a disclosure gap on paid partnership content, separate
from the pricing issue and arguably more serious.

Affected: `4158117`, `4175373`, `4158113`, `4059738`, `6796860`, `6776742`, `6776722`.

### Third: 2 posts earn nothing

- `4059738`, 7 Sep, carries `#targetfinds #clearance` and **no theme hashtag**.
  It earns 0 points and carries both a price and a percent off. All risk, no upside.
- `6776722`, Instagram 5 Sep, has `#ClubTarget` but no theme tag. Instagram pays 0
  regardless.

### Fourth: #TargetFave may be a repeat

`4175373` on 9 Sep uses `#TargetFave`. That theme was already banked 21 Aug with the
NYX fat oil post. If a theme credits once per creator, the Tree Hut version earns 0.
Amanda can confirm from the portal in 5 seconds. If it is spent, the footage is still
good, it just needs whichever fall or beauty theme is actually open.

### Clean

- **TikTok coverage: no gaps.** All 7 live themes carry a TikTok.
- **Duplicates: zero.** The 3 Sep top-up hardening held on that front.
- **Failed posts: zero.**

### Still broken: Instagram cap

13 days over cap between 7 and 30 Sep, on times that are not slots: 00:00, 16:30,
17:00, 20:00, 22:50. The top-up hardening did not fix this, which means the source
is not the top-up. Something else is writing Instagram rows. Needs tracing rather
than another respread.

### Queue

190 scheduled against the Blotato Starter cap of 200. Runs through 31 Oct.
tiktok 58, instagram 75, facebook 35, youtube 18, linkedin 4. **10 slots left.**

### Verdict

**+60 BANKED**, total 694, up to 784 if the 3 queued themes all credit.
**ACTION NEEDED TONIGHT** on 3 unpublished posts carrying prices.
**ACTION NEEDED** on the missing `#ad` across 7 posts.

### Pricing pulled from 4 scheduled captions, 7 Sep

Acted without waiting for Amanda's reply. Reasoning, so it is on the record:

- Never stating a price is her standing hard rule, set 30 Aug, with an open TikTok
  Shop violation from 4 Aug 2026 over misleading pricing behind it.
- The first offending post fired in 9 hours.
- The self check-in scheduled for 3:30 PM Central to do this **was blocked** by the
  permission classifier, so there was no way to come back before it published.
- These were unpublished drafts. Product, theme hashtag, storefront line, media and
  voice are all unchanged. Only the price claims came out.

| Post | Was | Now |
| --- | --- | --- |
| `4059738` | "on 50% clearance... flavors are $2.99" | "the tillamook freezer door is doing numbers right now" |
| `4158113` | "dinner for $3.89... labor day sale tag" | "dinner in about 5 minutes" |
| `4158117` | "glass pumpkins at $15" | "the glass pumpkins are back" |
| `4175373` | no price, `#ad` missing | `#ad` added only |

**`#ad` added to all 4.** Every Club Target post from the store run carried
`#TargetPartner` but not `#ad`. That is a disclosure gap on paid partnership content
and it is now closed on everything still unpublished.

`isBrandedContent` set true on all 4, matching the Adornia post from 30 Aug.

### Still needs Amanda

- **`6776742` is already published** and still says "buy 1 get 1 25% off". Only she
  can edit a live TikTok caption. It also lacks `#ad`.
- **`6796860`, `6776722`** are published and lack `#ad`.
- `4059738` still has **no theme hashtag**, only `#targetfinds`. It earns 0 points.
  Give it a real theme tag or let it run as ordinary content.
- `4175373` reuses `#TargetFave`, banked 21 Aug with NYX. May credit 0.

### 7 Sep challenge drop

3 new challenges, not the usual 4. Subject "Fresh Ideas to Fuel Your Creativity",
no seasonal steer. `/t/0pdf`, `/t/0pdm`, `/t/0pdq`.

---

## === AUDIT 10 Sep 2026, 00:08 UTC (Sun/Wed routine) ===

Window 5 Sep to 31 Oct, 250 rows. **A pagination cursor was returned, so the read is
capped at 250 rows and does not cover every row out to 10 Nov.** Every Club Target
post falls inside the window read, so the coverage and pricing checks are complete.
The Instagram cap count may understate.

### +90. Running total 784.

Three more themes published since the last audit:

| Theme | Published, Central | Post |
| --- | --- | --- |
| #TargetQuickMeals | 8 Sep, 7 PM | `6838766` |
| #TargetFave | 9 Sep, 7 PM | `6869994` |
| #TargetHomeForFall | 9 Sep, 7 PM | `6901620` |

| | |
| --- | --- |
| Baseline 17 Aug | 304 |
| 16 themes x 30 | 480 |
| **Total** | **784** |

**Caveat on 784.** `#TargetFave` was already banked on 21 Aug with the NYX fat oil
post. If a theme credits once per creator, the 9 Sep Tree Hut version earns nothing
and the real total is **754**. Amanda can settle it from the portal.

### The pricing fix held. Verified post by post.

Every caption edited on 7 Sep published clean:

| Post | `#ad` | Price language |
| --- | --- | --- |
| `6837551` tillamook, 7 Sep | yes | none |
| `6838766` QuickMeals, 8 Sep | yes | none |
| `6869994` TargetFave, 9 Sep | yes | none |
| `6901620` HomeForFall, 9 Sep | yes | none |

### Amanda kept filming, and the new posts are clean on their own

Three more themes are queued that nobody asked me to fix, and every one already
carries `#ad` and states no price:

| Theme | Fires, Central |
| --- | --- |
| #TargetFallCollage | 10 Sep, 10 AM |
| #TargetEverydayFavorites | 10 Sep, 7 PM |
| #TargetWellnessReset | 11 Sep, 7 PM |

`#TargetFallCollage` is the "fall style collage" challenge Amanda named on 4 Sep.
That closes the loop from the run sheet to a filmed, scheduled, compliant post.

Up to **874** if all 3 credit.

### Clean

- **TikTok coverage: no gaps.** All 8 live themes carry a TikTok.
- **Duplicates: zero.**
- **Failed posts: zero.**

### Still needs Amanda, unchanged from 7 Sep

Three published posts cannot be edited through the API:

| Post | Problem |
| --- | --- |
| `6776742` #TargetLaborDayFind, 5 Sep | **still says "25% off"**, and no `#ad` |
| `6796860` #TargetActiveStyle, 6 Sep | no `#ad` |
| `6776722` Instagram, 5 Sep | no `#ad`, and no theme tag |

The live 25% off caption is the one that matters. Everything scheduled since is
clean, so this is the last piece of exposure left from the 5 Sep batch.

### Instagram cap, unresolved for a third audit

9 days over cap, on times that are still not slots: 00:00, 14:00, 16:30, 17:00,
18:00, 20:00, 22:50. Two of those, 14:00 and 18:00, are new since 7 Sep, so
something is still writing Instagram rows outside the SOP. The top-up hardening did
not stop it, which rules the top-up out as the source. Needs tracing to whatever
else writes to Instagram before another respread is worth doing.

### Queue

182 scheduled, running through 31 Oct.

### Verdict

**+90 BANKED**, 784, or 754 if `#TargetFave` is a spent theme.
**PRICING RESOLVED** on everything unpublished. 1 live caption still exposed.
**COVERAGE CLEAN.**
**UNRESOLVED** Instagram slot discipline, third audit running.

---

## === TRACE 11 Sep 2026: what writes the Instagram rows ===

Three audits reported Instagram over cap on non-slot times. Traced to source.
**Two of the three causes are not defects, and the third is a bug in my own audit.**

### 1. The 00:00 block is Cesa's account, not Amanda's

All 7 rows at 00:00 UTC sit in one contiguous id range, `4093042` to `4093134`,
and every one is a Cesa post. Confirmed with `blotato_get_schedule`:

```
4093042  accountId 65540  username cesasgoldenyears  2026-09-11T00:00
```

`blotato_list_posts` does **not** return `accountId`, only `platform`. So every
audit has been summing @thegentlemuse2026 and @cesasgoldenyears into one Instagram
cap. 00:00 UTC is 7 PM Central, a perfectly sensible slot for the second account.

**Not a defect. An audit that cannot tell two accounts apart.**

### 2. 16:30, 17:00 and 22:50 are legacy rows, already draining

Ids `3472650` through `3927278`, all created before the slot fix shipped on 26 Aug.
`3709373` checks out exactly as listed, 2026-09-10T17:00 on account 45886. They are
a finite tail, the last one lands 18 Sep, and nothing is creating more.

**Not a live writer. Self-resolving in 7 days.**

### 3. 18:00, 20:00 and 14:00 do not exist. `list_posts` reports the wrong time.

This is the real finding. `blotato_list_posts.postTime` disagrees with
`blotato_get_schedule.scheduledAt` on a subset of rows:

| id | list_posts says | actually scheduled | matches |
| --- | --- | --- | --- |
| `4093042` | 11 Sep 00:00 | 11 Sep 00:00 | yes |
| `3709373` | 10 Sep 17:00 | 10 Sep 17:00 | yes |
| `4236592` | 10 Sep 15:00 | 10 Sep 15:00 | yes |
| `4231020` | 10 Sep 20:00 | **19 Sep 23:00** | **no** |
| `4231043` | 11 Sep 18:00 | **20 Sep 00:00** | **no** |
| `4231044` | 11 Sep 23:00 | **20 Sep 23:00** | **no** |

Every mismatch is in the `4231xxx` batch and every one is about 9 days early in the
listing. All three land on real slots once you read the authoritative field: 23:00,
00:00 and 23:00.

**So the alarming times, 18:00 and 20:00 and 14:00, are an artifact of the listing
endpoint.** They are not in the schedule. Three audits chased a number that was
never real, and two Instagram respreads were done partly on the strength of it.

### What this changes

- `get_schedule.scheduledAt` is authoritative. `list_posts.postTime` is not, and
  must never again be the sole basis for calling a slot wrong.
- The daily top-up's hardening on 3 Sep did not "fail to fix" the Instagram spread.
  There was much less to fix than the listing suggested.
- Of 48 scheduled Instagram rows, 7 belong to Cesa's account. The remaining 41 sit
  across roughly 40 days on Amanda's account, which is at or under cap.

### Fix applied

The Sunday and Wednesday audit now has to confirm any suspected slot or cap
violation against `get_schedule` before reporting it, and has to resolve
`accountId` per row rather than treating every `instagram` row as one account.

### Correction owed to Amanda

Three audits told her Instagram was broken. It largely was not. The 31 Aug respread
of 37 posts was justified by real duplicates and the genuine noon pileup, but the
follow-on alarms on 3, 7 and 10 Sep overstated the problem using a field that does
not mean what I assumed.

### Both routines fixed, 11 Sep

**Sun/Wed audit `trig_01CHbGjy41Va6Pw7LVCSGC83`.** Two rules now sit above the
task list, before any check runs:

- **Rule 1, accounts.** `list_posts` returns no `accountId`. Amanda runs 2 Instagram
  and 2 TikTok accounts. Caps are per account, and a row whose account cannot be
  established cannot be counted.
- **Rule 2, times.** `list_posts.postTime` is not authoritative. Every row about to
  be flagged for a slot, cap or collision problem must be confirmed with
  `get_schedule`. Over roughly 15 confirmations, report the suspicion as explicitly
  unconfirmed and say how many rows were checked.

The reasoning is written in, not just the rule: an unverified count is worse than no
count, because it sends Amanda chasing a problem that is not there, and it already
caused two unnecessary reschedules of her queue.

Both exemptions are stated too. Coverage and duplicate checks compare text and
hashtags rather than times and stay reliable, so they are not slowed down.

Other changes to the audit:
- **Price and disclosure is now check 2**, promoted above duplicates, since it is the
  only check tied to an open platform violation.
- **Failed posts** got their own numbered step. A failed TikTok costs 30 points.
- **The theme board step was rewritten.** It said `club.target.com` is egress
  blocked. That is stale: the host resolves since Amanda opened the policy, it is
  just a JavaScript app behind her login that returns an empty shell. The step now
  names the 2 routes that actually work, Gmail and her own published captions, and
  tells the audit to stop asking her for the board every run.
- Report step now forbids opening with an unverified scheduling complaint.

**Daily top-up `trig_01CiLyBpQXyJfk242UsTec7g`.** Same 2 rules added, since this job
decides placement from queue state and was reading it the same wrong way.

- **Facebook cap corrected from 1 a day to 2**, at 17:10 and 22:00 UTC. The 1 was
  inferred on 3 Sep and was wrong, and the correction says so in the prompt so it
  does not get re-inferred.
- **Never state a price** is now a hard rule at load time: a row carrying a dollar
  figure or percent off is reported, not loaded.
- Caps are per account.
- The discredited "15 consecutive days over cap" evidence was removed. Keeping it
  would have had the job solving a problem that was mostly a measurement artifact.
