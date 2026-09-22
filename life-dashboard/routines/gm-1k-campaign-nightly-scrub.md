# GM 1K-campaign nightly scrub

- id: trig_013atCTphGYzThaKstBMEBAT
- cron (UTC): 30 2 * * *
- enabled: True
- bound session: session_0137iXCxybaJY38HpNTYV5QB
- connectors: none
- model: default

## Prompt

Nightly data scrub for the 1K campaign (Sept 8 to Oct 8, start 190 followers). Read content/1k-campaign-plan.md and CLAUDE.md on branch claude/instagram-500-follower-text-6oku92 first.

METHODOLOGY RULE: pull the FULL campaign corpus (since 2026-09-08), not a 48 hour window. Two format rankings were reported wrong in August from short windows. Use blotato_list_top_posts for instagram AND facebook separately, sortBy views_count, limit 60, since 2026-09-08. If the result is too large, save to file and parse with python.

Append to content/data-scrub-log.md: follower count (ask Amanda, do NOT trust Metricool, it lags 3 to 5 days), per-post table with views and avg watch time, and format-level analysis across Cesa organic, Amanda face-to-camera, trivia, humor, Club Target product, and Remotion talking head. Commit and push to the same branch.

Specifically track each night: (1) trivia views on Instagram against the 37 baseline and the Facebook 230-577 band, this is the live test of the clean-export fix, (2) whether any Cesa post breaks 10,000 views, which is the single number that makes 1,000 followers reachable, (3) daily post volume against the 3-4 per platform target across IG, TikTok, Facebook, YouTube Shorts.

Flag any published post carrying a platform watermark or AI badge, that is now a hard rule violation. Flag any product post missing its SKU link.

Campaign ends Oct 8. After the Oct 9 morning firing delivers the final wrap, disable this trigger via update_trigger.
