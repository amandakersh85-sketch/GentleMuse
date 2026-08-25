# The Daily Promo Rotation Test

**Started:** 2026-08-25
**Premise (Amanda's):** post 3 times a day, and make 1 of those 3 a promo for a newsletter
or lead magnet. Recycle the promos across every channel, staggered times. Run it as a test,
find out which platform feeds which offer, then buckle down on the winners.

---

## The rotation: 1 offer per day, every channel

Running 1 offer per day across all channels is what makes this measurable. Because only 1
offer is promoted on a given day, that day's signups belong to that offer. Mixing 3 offers
a day would produce noise and no answer.

| Day | Offer | Audience | Destination |
|---|---|---|---|
| Mon | Consider This | Home / household | MailerLite signup form |
| Tue | Just Another Tuesday | Builders / AI | LANDING PAGE URL NEEDED |
| Wed | AI Beginner's Guide | Builders / AI | ai-guide.subscribepage.io |
| Thu | Consider This (send day) | Home / household | MailerLite signup form |
| Fri | Reset Guide | Calm / reset | gentlemuse.co/reset-guide |
| Sat | Press Play | Books / audio | comment PLAY |
| Sun | Just Another Tuesday | Builders / AI | LANDING PAGE URL NEEDED |

Both newsletters get 2 slots a week. The guides get 1 each. Tuesday and Thursday promos land
on the days those newsletters actually send, so a new signup gets an issue almost immediately
instead of waiting 6 days.

## Staggered posting times (America/Chicago)

Deliberately spread across the day, and deliberately OUTSIDE Amanda's existing content block
(her current posts run roughly 8:30 to 10:00 AM). Times are odd-numbered on purpose so the
feed does not look automated.

| Channel | Time | UTC |
|---|---|---|
| X | 6:45 AM | 11:45 |
| LinkedIn | 7:40 AM | 12:40 |
| Pinterest | 11:20 AM | 16:20 |
| Facebook | 12:35 PM | 17:35 |
| Instagram | 5:50 PM | 22:50 |
| TikTok | 7:15 PM | 00:15 (+1) |
| YouTube | 8:05 PM | 01:05 (+1) |

This also spreads the same offer across 7 different hours, so a follower who is on 2 platforms
does not see the identical promo twice in 10 minutes.

---

## How the test produces an actual answer

Two data sources, cross-referenced weekly:

1. **Offer performance** comes from MailerLite. Because only 1 offer runs per day, that day's
   new subscribers and form conversions belong to that offer. Pull group counts and form
   `conversions_count` weekly.
2. **Platform performance** comes from Blotato per-post analytics (impressions, clicks,
   engagement per post). That says which channel carried the offer, not which one produced
   the signup.

Cross-referencing the two gives the channel-by-offer matrix. Log it weekly in the table below.

### The honest limitation, and the cheap fix

The above gives strong signal but not perfect attribution: it cannot say "this exact signup
came from LinkedIn." Every channel currently points at the same URL per offer. 2 ways to
close that gap when Amanda wants exact numbers:

- **Cheap (about 20 minutes, recommended):** a free link shortener with per-link click stats.
  Make 1 short link per channel per offer. Click counts then attribute exactly, and the
  shortener does the counting.
- **Thorough:** 1 MailerLite signup form per channel, each feeding the same group. Form
  `conversions_count` is then exact per channel. Note: forms created through the API come out
  as empty inactive shells, so each one needs a few minutes of design in the MailerLite
  dashboard before it works. That is why it is not already done here.

Until one of those is in place, read the weekly log as directional, not exact.

---

## Weekly log

| Week | Offer | Best channel by clicks | New signups | Notes |
|---|---|---|---|---|
| Aug 25 to 31 | | | | first week of the test |

**Decision rule:** after 3 weeks, any channel-and-offer pair that is clearly ahead gets more
slots. Any pair that produced nothing gets dropped and its slot reassigned. Do not act on
1 week of data.

---

## Week 1 — actually scheduled (all times America/Chicago)

| Date | Offer | Channels | Status |
|---|---|---|---|
| Wed Aug 26 | AI Beginner's Guide | X 6:45a, LinkedIn 7:40a, Facebook 12:35p | SCHEDULED |
| Thu Aug 27 | Day 60 handoff (promotes JAT) | Amanda's series slot | DRAFT, needs JAT URL |
| Fri Aug 28 | Reset Guide | X 6:45a, LinkedIn 7:40a, Facebook 12:35p | SCHEDULED |
| Sat Aug 29 | Press Play | Facebook 12:35p only | SCHEDULED |
| Sun Aug 30 | Just Another Tuesday | none | BLOCKED, no URL |
| Mon Aug 31 | Consider This | X 6:45a, LinkedIn 7:40a, Facebook 12:35p | SCHEDULED |

10 posts scheduled. Thursday Aug 27 deliberately carries no rotation promo: the Day 60
handoff is that day's promo, and doubling up would muddy which offer earned the day.

Week 1 review fires Tue Sep 1 to fill in the log.

## What is scheduled vs blocked

- **X, LinkedIn, Facebook:** text plus link. Fully schedulable now.
- **Instagram, Pinterest:** need an image. Promo graphics generated in the launch design system.
- **TikTok, YouTube:** need video. These come from Amanda's Video Factory, not from here.
- **Tuesday and Sunday (Just Another Tuesday):** blocked on the signup URL. The newsletter has
  a live landing page (Christine used it on Aug 19) but MailerLite's API does not expose
  landing pages, so the address is unknown in this workspace. Amanda pastes it once and both
  days unblock.
