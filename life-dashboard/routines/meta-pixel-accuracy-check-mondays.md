# Meta Pixel accuracy check — Mondays

- id: trig_012SoNHjpYsZFnLsnA7yrmzv
- cron (UTC): 30 14 * * 1
- enabled: True
- bound session: fresh each run
- connectors: Meta-Ads, Slack, Wix
- model: default

## Prompt

Weekly Meta Pixel accuracy check for The Gentle Muse (gentlemuse.co). This is a narrow, standalone check — separate from the analytics pipeline. This runs autonomously — Amanda is not present. Read-only: report and let Amanda approve any fix. Do not make any write/fix changes yourself.

Context: on July 6, 2026, the Wix marketing tag (tag ID 1dbebc44-3325-43e4-8a7f-d4ef807fb00b, site ID 69c70274-e4c5-4e90-8c9e-bac496b142b0) was fixed to point at the correct, active Meta Pixel (1646221669832923, under active ad account 1646561496770076 which has a payment method), after being wrongly wired to an orphaned pixel (1503306501428814, under closed ad account 1613101019948594).

Each run:
1. Use the Meta Ads connector (dataset stats/details) to confirm pixel 1646221669832923 has fired events in the past 7 days.
2. Use the Wix connector to GET the marketing tags for site 69c70274-e4c5-4e90-8c9e-bac496b142b0 and confirm the Facebook Pixel tag's trackingId is still 1646221669832923 (hasn't reverted or been overwritten by an editor change/republish).
3. Post the result to Slack channel C0B6B4LHDPT, concisely: firing status (yes/no + rough event count) and Wix tag status (correct or drifted). If anything is wrong, flag exactly what and what fix is needed — but do NOT fix it yourself.
4. Track consecutive clean weeks in your report (state the count based on prior run history if visible). Once 4 consecutive clean weeks are reached (expected around Aug 3, 2026), tell Amanda in the Slack report that the pixel has been stable for a month and ask if she wants to drop this check to monthly cadence.

Keep the report short — a few lines, not a long writeup. End with <run-summary>pixel firing yes/no, tag correct/drifted, Slack permalink</run-summary>.
