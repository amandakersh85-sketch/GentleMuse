# GM 500-campaign daily data scrub

- id: trig_01UqWPUhURmnHcfGvsC6jJP4
- cron (UTC): 30 2 * * *
- enabled: False
- bound session: session_0137iXCxybaJY38HpNTYV5QB
- connectors: none
- model: default

## Prompt

Daily data scrub for the 500-follower campaign (runs 9:30 PM Central). Pull Blotato top posts for the last 48h (blotato_list_top_posts, sortBy views_count) and Metricool IG evolution metrics (brandId 6066935). Compare against content/data-scrub-log.md in the repo, append today's numbers with format-level analysis (Cesa vs build-in-public vs experiment vs promo, views + avg watch time + follows), commit and push to branch claude/instagram-500-follower-text-6oku92. Flag which formats to double down on and which to cut. If Amanda has posted a fresh follower count in chat, log it; otherwise note the count is pending. Campaign ends Sunday night Aug 23; after the Monday morning firing delivers the final full-campaign scrub, disable this trigger via update_trigger.
