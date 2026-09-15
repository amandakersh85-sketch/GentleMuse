# Watchers: the reminders that fire when the numbers align

Set up 2026-09-01. Every one of these stays **silent by default**. They speak only when a
threshold is crossed, because at this stage low numbers are the normal result and reporting
them daily would train Amanda to ignore the reports.

## The 4 live watchers

| Watcher | Fires | Trigger id | Speaks when |
|---|---|---|---|
| Daily DM sync + keyword failure sweep | daily 13:00 UTC | `trig_0123dXXH4Gn978bHSD6gehCZ` | an email was captured, a run failed, someone is stranded, or a followGate reappeared |
| Breakout watcher | Tue + Fri 09:00 CT | `trig_01Cv1x3tz6yEpcRySrPSSowR` | an Instagram post clears 2,500 views **or** 15 shares |
| Monday scoreboard | Mondays 10:00 CT | `trig_01R5JH3vQkByMWcgf7rKwPPt` | a follower milestone, a real new subscriber, or a real keyword lead |
| Re-permission deadline | once, 2026-09-06 | `trig_01JSSTESKSSnnMjD8vwxRSP7` | always, it is a one-shot decision point |

## The thresholds, and why each one

### Breakout: 2,500 views or 15 shares

Anchored to real numbers, not round ones. The single post that broke out, `6250675` on Aug 18,
did **7,726 views on 54 shares**. Everything else she has ever posted sits between 150 and
1,900 views and none cleared 9 shares. Ordinary recent posts do 150 to 800 in the first 24
hours. So 2,500 is comfortably outside normal and well under the winner.

**Shares are the real trigger.** The winner kept climbing for 7 days; nothing without shares
grew past day 1. A post with 15 shares and modest views is more interesting than one with
3,000 views and none.

When it fires, the instruction is to cross-post that exact video to Cesa's channels and
Facebook, requeue it 2 to 3 weeks out, and name what the caption has in common with the
winner. The pattern is the asset, not the post.

### Followers: 177 today, milestones at 200 through 500

Verified via Metricool `IGEV01` on 2026-09-01, not estimated.

| Date | Followers | Net |
|---|---|---|
| Aug 25 | 173 | |
| Aug 27 | 171 | -2 |
| Aug 29 | 173 | +1 |
| Aug 30 | 176 | **+3** |
| Aug 31 | 177 | +1 |

**Up 4 in a week. At that pace 500 is roughly 18 months away.** At the Aug 30 rate it is about
3 months. That gap is the whole problem, and 500 is the number that unlocks Club Target.

The watcher speaks at each 50-follower milestone, on any **negative** week, and on any week of
**+15 or better** so a working pattern gets noticed while it is still running.

### First real conversion: any contact that is not Amanda

Every automation run in the system belongs to contactId `1048429878116670` or `955627417560872`,
both hers. Every subscriber except Mary, Melissa, Nadia, christine and Laura is one of her own
addresses. So the condition is simply: **anyone new who is not on that list.**

That would be the first lead the funnel has ever produced. It gets reported as a headline.

## One limitation worth knowing

These triggers wake **this** session rather than starting a fresh one, which is what gives them
access to Blotato, MailerLite and Metricool. The trigger records themselves carry no connector
grants of their own, so if this session is ever reclaimed the watchers lose their tools and
will need recreating from a live session. Nothing silently half-works: a firing without tools
will say so.
