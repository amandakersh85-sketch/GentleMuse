# Monday scoreboard: followers, list, first conversions

- id: trig_01R5JH3vQkByMWcgf7rKwPPt
- cron (UTC): 0 15 * * 1
- enabled: True
- bound session: session_01Lj4AttK199DuE1QnxDMi2g
- connectors: none
- model: default

## Prompt

Weekly scoreboard for The Gentle Muse. Report only what crossed a line. Skip anything that just moved a little.

FOLLOWERS. mcp__Metricool__getAnalyticsDataByMetrics, brandId 6066935, metrics ["IGEV01","IGEV03"], from 8 days ago to today, timezone America/Chicago. IGEV01 is the current follower count on @thegentlemuse2026, IGEV03 is the daily net.
Baseline: 177 on 2026-08-31, up 4 that week, having dipped to 171 on Aug 27.
Say something only if one of these is true:
- The count crossed 200, 250, 300, 350, 400, 450 or 500 for the first time. At 500 tell her plainly: the Club Target threshold is met, apply now, that was the whole reason for the goal.
- Net growth for the week was negative. That is worth knowing early.
- Net growth for the week was 15 or more. Something worked; say which posts ran that week and tell her to do more of that shape.
Otherwise say nothing about followers.

THE LIST. mcp__MailerLite__list_subscribers, and mcp__MailerLite__list_resources with resource_type group.
As of 2026-09-01 there are 5 real subscribers: Mary, Melissa, Nadia, christine, Laura. Everything else on the account is Amanda's own addresses and tests: amandakersh85@gmail.com, amanda@gentlemuse.co, the +cesatest / +cesatest2 / +cesaloop / +lptest aliases, and princesamaryelizabeth@gmail.com which shares her IP. Melissa and Nadia may have been unsubscribed by the Sept 6 re-permission run.
Say something only if a NEW subscriber appears who is not on that list of hers. That is the first real signup the funnel has ever produced and it is the headline, not a footnote. Report where they came from, which group they landed in, and confirm the delivery automation fired for them.
Do not report a subscriber count that has not changed.

KEYWORDS. blotato_list_automation_runs across the live automations.
As of 2026-09-01 no real audience member has ever used a keyword. Every run in the system is Amanda testing from her second account, contactId 1048429878116670 or 955627417560872.
Say something only if a run exists from a contactId that is neither of those. That is the first real keyword lead ever and she should hear it loudly, with what they commented, which offer, and whether the DM sent.

If none of the above fired, say nothing at all and stay quiet. A quiet week is the current normal and does not need a report.
