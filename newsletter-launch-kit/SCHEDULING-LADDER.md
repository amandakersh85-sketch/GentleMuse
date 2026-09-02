# The scheduling ladder

**Set 2026-09-02. This governs every session that schedules for The Gentle Muse.**

Read this before scheduling anything. It exists because 3 sessions were all reaching for the
same hour and burying each other's posts.

## The one-line rule

**Instagram @thegentlemuse2026 owns 10:00 AM Central. Nothing else goes there.**

## The ladder

| Platform / account | Primary slot (CT) | Second post that day | UTC |
|---|---|---|---|
| **Instagram @thegentlemuse2026** | **10:00 AM** | 3:00 PM | 15:00 / 20:00 |
| Instagram @cesasgoldenyears | 11:30 AM | — | 16:30 |
| Facebook, The Gentle Muse | 12:00 PM | 5:00 PM | 17:00 / 22:00 |
| TikTok, both accounts | 6:00 PM | 12:00 PM | 23:00 / 17:00 |
| YouTube, X, LinkedIn, Pinterest | anywhere | — | low stakes |

**Minimum 2 hours between any 2 posts on the same account and platform.** Not 30 minutes.
2 hours.

## Why this split, from the Metricool data

Every platform peaks at 10 AM Central. **That is the whole problem.** 3 sessions all
scheduling "at the best time" means 3 posts in the same minute, and Instagram splits the
initial test audience between them.

The evidence: on 2026-08-23 two Reels published 2 seconds apart and got **1,818 views and
162**. Same account, same day.

The fix works because the *second*-best hour is different on each platform, and giving up
that second place costs almost nothing except on Instagram:

| Platform | 10 AM | Its assigned slot | Cost of moving |
|---|---|---|---|
| Instagram, Wed | 6,506 | 6 PM would be 4,869 | **-25%, too expensive. It keeps 10 AM.** |
| Facebook, Wed | 15,528 | 12 PM is **15,834** | **better than the peak** |
| Facebook, Mon | 15,247 | 12 PM 14,786 | -3% |
| TikTok, Mon | 1,089 | 6 PM is **1,096** | **better than the peak** |
| TikTok, Wed | 1,432 | 6 PM 1,386 | -3% |

So Facebook and TikTok give up 0 to 4 percent, and Instagram, the account chasing 500
followers for Club Target, keeps the hour it cannot afford to lose.

Source: `mcp__Metricool__getBestTimeToPostByNetwork`, brandId 6066935, America/Chicago,
pulled 2026-09-02 for instagram, facebook and tiktok.

## Before scheduling a batch

1. **Page to the END of the queue.** `blotato_list_schedules` returns 50 at a time and the
   queue is 182. Follow the cursor until it stops coming back. Checking page 1 and calling it
   done produced a wrong "zero collisions" answer on 08-30.
2. **Say how many posts you examined** when you report a sweep. If the number does not match
   the `count` the API returns, the sweep is not finished.
3. **Re-verify after moving anything.** On 09-02 a fix moved a post directly on top of another
   one. Only the re-check caught it.
4. **The plan caps at 200 scheduled posts.** Near the cap, new posts fail outright with a cap
   error until something is deleted. X is the cheapest thing to delete: it returns an empty
   analytics set entirely.

## Sessions currently scheduling

| Session | What it schedules |
|---|---|
| `claude/newsletter-signup-strategy-2fpuoq` | funnel, Cesa reach tests, keyword automations |
| `claude/holiday-caption-strategy-m5abq8` | holiday and history series, CTA rewrites |
| Cesa daily render / queue topup sessions | Cesa clips to both accounts |

**These do not share a machine and cannot message each other.** Coordination goes through
Amanda and through this file. If you change the ladder, change it here and tell her, so the
next session reads the same thing.

---

## Execution record, 2026-09-02

The Facebook and TikTok backlog was migrated onto the ladder. **34 posts moved.**

**Verified against source after the moves.** Paged `blotato_list_schedules` with the cursor
until it returned an empty page:

```
POSTS EXAMINED: 200   API count: 200   -> COMPLETE
2-hour rule violations: NONE
Non-Instagram posts still at 15:00Z (10 AM CT): NONE
Facebook off-ladder: NONE
TikTok off-ladder: NONE
```

### Where the queue landed

| Account | n | Slots |
|---|---|---|
| IG @thegentlemuse2026 (45886) | 73 | 15:00Z x29, 23:00Z x22, 17:00Z x10, 20:00Z x7, other x5 |
| Facebook (30840) | 41 | 17:10Z x32, 17:00Z x3, 22:00Z x6 |
| TikTok main (41488) | 30 | 23:00Z x21, 17:00Z x8, 20:00Z x1 |
| X (21430) | 19 | 13:30Z x19 |
| LinkedIn (20723) | 12 | 13:30Z x11, 17:00Z x1 |
| YouTube (36129) | 12 | 17:20Z x12 |
| IG @cesasgoldenyears (65540) | 7 | 00:00Z x4, 23:00Z x3 |
| TikTok Cesa (55761) | 4 | 00:10Z x4 |
| Pinterest (6328) | 2 | 16:20Z x2 |

### Three judgment calls, recorded so nobody re-litigates them

1. **The 4 Cesa TikToks at `00:10Z` were left alone.** 00:10Z is 7:10 PM CT the *previous*
   day, which is already inside the evening band the ladder is aiming at. Moving them to
   23:00Z would have shifted each one a full day earlier. Not worth it.

2. **`4056495` was caught after the sweep had already started.** It was added by another
   session at `2026-10-10T15:00Z`, the Instagram 10 AM slot, on the TikTok account. Moved to
   `2026-10-10T23:00Z`. Nothing else was on 41488 that day.

3. **Sept 3 had three TikToks on 41488 and only two ladder slots.** The one in the leftover
   3 PM slot was the paid `#TargetPartner #ad` Adornia post. Rather than move a paid post to
   a different date, which is Amanda's call and not a scheduling decision, the two posts were
   **swapped within the day**:
   - `3952005` (#ad) 20:00Z -> **23:00Z**, the 6 PM primary slot
   - `3630599` (unhinged gratitude, organic) 23:00Z -> **20:00Z**

   Gaps on 41488 that day are now 17:00 -> 20:00 -> 23:00, three hours each.

### Open, out of scope, needs a decision

- **IG @cesasgoldenyears (65540) is not on the ladder.** Its 7 posts sit at 00:00Z and 23:00Z,
  not the 16:30Z (11:30 AM CT) the ladder assigns it. Amanda asked for Facebook and TikTok, so
  Cesa's IG was not touched. Worth doing next, but it is a separate call.
- **The queue grew 182 -> 200 while this work was in flight.** Another session is still
  scheduling and has not adopted the ladder. One of its new posts took the 10 AM TikTok slot
  (item 2 above). The queue is now **at the 200 plan cap** — the next new post will fail.
