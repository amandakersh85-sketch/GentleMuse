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
