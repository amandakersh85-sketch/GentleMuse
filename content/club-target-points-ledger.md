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
