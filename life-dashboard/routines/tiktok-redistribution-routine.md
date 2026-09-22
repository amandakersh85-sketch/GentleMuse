# TikTok redistribution routine

- id: trig_01SWbuAk7CGGned8thLYHtSe
- cron (UTC): 0 9 * * 2,5
- enabled: False
- bound session: fresh each run
- connectors: Blotato, Canva, Gmail, Google-Calendar, Google-Drive, Meta-Ads, Metricool, Slack, Wix
- model: default

## Prompt

Before proceeding, review the SOP at C:\Users\amand\OneDrive\Gentle Muse\Drafts\SOP - Cloud TikTok Redistribution (2x weekly).md and the existing method at C:\Users\amand\OneDrive\Documents\Claude\Scheduled\weekly-tiktok-redistribution-friday\SKILL.md.

Decision required: Confirm how clean video files will be ingested into Blotato without manual PowerShell execution each time. Review the options in the SOP and specify the chosen method (e.g., watched folder, API integration, scheduled script) before this routine can run autonomously.

Once confirmed, the routine will:

1. Access TikTok Studio, Blotato, and ManyChat via Claude-in-Chrome.
2. Identify the newest finished TikToks ready for redistribution.
3. Prepare and post each video to Instagram, Facebook, and YouTube using the platform-specific tools.
4. Never repost to TikTok.
5. Log completion and any errors.

This routine requires your computer and Chrome to be running. If the browser is unavailable or no new videos are ready, report the status briefly.
