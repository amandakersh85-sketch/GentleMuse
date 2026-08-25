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
