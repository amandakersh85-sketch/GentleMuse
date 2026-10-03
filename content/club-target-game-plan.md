# Club Target Game Plan

Updated 30 Aug 2026. Supersedes every earlier plan. Handle `amanda.20`.
Storefront `club.target.com/a/amanda.20`.

## The one number that changed everything

Amanda confirmed on 30 Aug that **Instagram does not credit below 500 followers.**
Portal total is **574**.

| Placement | Nominal | Actual, today |
| --- | --- | --- |
| TikTok | 30 | **30** |
| Instagram Reel | 30 | 0 |
| Instagram Story | 15 | 0 |
| **Theme total** | 75 | **30** |

**A theme is a TikTok. Everything else is follower growth, not points.**
Keep posting to Instagram, it feeds the 500-follower gate that unlocks the other
45. It just does not pay yet. Re-open this file the day she crosses 500.

## How points actually got missed

Three distinct failures, all found 30 Aug. The plan below closes each one.

1. **The TikTok never got loaded.** `#TargetLittleFinds` (Adornia) had 2 Instagram
   rows and 1 Facebook row scheduled, and **zero TikTok**. The staging library was
   correct, the row existed as GW0057 for 1 Oct. The live queue only ran through
   25 Sep, so the wave was partially loaded and the only row that pays fell off
   the end. Silent. Nothing errored.
2. **A theme got double-booked.** Cat and Jack was scheduled twice from the same
   asset, 2 Sep and 24 Sep. Only one can credit and TikTok may suppress the repeat.
3. **A theme was never filmed.** Fresh Home Finds and Game Day Throwback had no
   footage at all, because there was no written list of open themes to shoot
   against. They were only discovered on deadline day.

## The four standing rules

**Rule 1. TikTok first, always.**
No Club Target asset is scheduled to any platform until its TikTok row exists in
the **live Blotato queue**. Not in the staging file. In the queue. The file
passing validation means nothing if the wave was only half loaded.

**Rule 2. Verify against the live queue, not the library.**
`scripts/validate-wave.py` now fails any wave where a Club Target theme appears
without a TikTok row. Both waves pass today. That is not sufficient on its own,
because the 30 Aug leak happened after the file was correct. The Sunday and
Wednesday audit re-runs the same check against Blotato itself.

**Rule 3. The theme board is the shot list.**
`club.target.com` is blocked from Claude's network. Amanda is the only one who can
read open themes and their closing dates. Nothing else in this plan works without
that list. See below.

**Rule 4. One store run per theme batch, filmed against the board.**
Themes are filmed in batches. Any theme announced after a store run has no footage
and will be missed. That is exactly what happened to Fresh Home Finds. Film against
the board, not against memory.

## What Amanda does, and it is one thing

Open the Club Target portal. For every open theme, paste back three fields:

```
theme name | exact hashtag | closing date
```

That is the whole job. Everything downstream is automated. The audit asks for this
every Sunday and Wednesday, and it goes into `content/club-target-theme-board.md`
with days-remaining computed per theme.

Without it, the plan degrades to reacting to deadline-day reminders, which is how
75 points were lost this week.

## Current state, 30 Aug 2026

### Banked, TikTok published

Everyday Essentials, HeyDay Tech, Lunch Throwback, Budget Finds, TargetFave,
Fall First Looks, College MVPs, Pet Faves, Good and Gather.
9 themes x 30 = **270 points**, on top of the 304 baseline. Total **574**.

### Queued and safe

| Theme | TikTok | Status |
| --- | --- | --- |
| #TargetCatandJackSummer | 2 Sep, 15:00 UTC | live, duplicate removed |
| #TargetLittleFinds | 3 Sep, 15:00 UTC | **scheduled 30 Aug to close the gap** |

### Open, blocked on filming

| Theme | Points | Blocker |
| --- | --- | --- |
| Fresh Home Finds | 30 | no footage, needs a store run |
| Game Day Throwback | 30 | no footage, needs a store run |

### Known defect, not yet fixed

The Freshpet caption reads "Cesa is 13". She is 19. Live on the 21 Aug TikTok and
Instagram Reel. Fixable by editing the caption in-app.

## Store run checklist

Before leaving the house:

1. Pull up `content/club-target-theme-board.md`. Film against it, in order of
   closing date, soonest first.
2. One clip per theme. The clip has to actually show the product, the caption
   carries `#TargetPartner #ad`, `@target`, `#ClubTarget`, the theme hashtag, and
   the storefront or SKU link.
3. **Never state a price.** Open TikTok Shop violation from 4 Aug 2026 over
   misleading pricing. No dollar figures, no "under $30", no discount percentages.
   The validator fails on all three.
4. Capture the SKU for each product. A SKU link credits more reliably than the
   bare storefront link.

## Cadence

| When | What | Who |
| --- | --- | --- |
| Sun and Wed, 00:00 UTC | Audit: TikTok coverage, duplicates, new posts, theme board request | automated |
| Daily | Blotato queue top-up, SOP v3 slots | automated |
| Per store run | Film against the board, soonest closing date first | Amanda |
| On crossing 500 IG followers | Re-open this file, Instagram starts paying | Amanda flags it |
