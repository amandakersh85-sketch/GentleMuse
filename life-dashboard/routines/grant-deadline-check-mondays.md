# Grant deadline check — Mondays

- id: trig_01Bdn5XjXz598p2GFYwYZcBB
- cron (UTC): 15 14 * * 1
- enabled: True
- bound session: fresh each run
- connectors: Google-Drive, Slack
- model: default

## Prompt

Weekly grant deadline check + draft prep for Amanda Kersh (The Gentle Muse LLC / Kersh Vending Services LLC). This runs autonomously — Amanda is not present.

STEPS:
1. Search Google Drive for the "Grant Tracker" file (may appear as "Grant_Tracker__GM___KV" or similar — search broadly if the exact name isn't found).
2. Read it. Identify any grant with a deadline or action-needed date within the next 10 days.
3. If nothing is due in that window: post one line to Slack channel C0B6B4LHDPT ("Grant check: nothing due in the next 10 days") and stop.
4. If something IS due within 10 days: this is where Amanda wants real forward motion, not just a heads-up. Draft the application content yourself as thoroughly as you can from the Grant Tracker's saved profile info and Amanda's established voice and business facts (The Gentle Muse LLC: digital products, email list, gentlemuse.co, Payhip storefront; Kersh Vending Services LLC: vending machines, Waterloo Iowa). Clearly mark anything you couldn't fill in (missing info, documents needed from her).
5. Save the draft as a Google Doc in her Gentle Muse Drive folder using her file naming convention ("Subject, GM" or "Subject, KV" — NEVER lead with "Gentle Muse").
6. Post a short summary to Slack channel C0B6B4LHDPT: what's due, what you drafted (with Drive link), what's still needed from Amanda before it could go out.

HARD RULE, no exception: never submit, pay an application fee, create accounts, or take any irreversible action on a grant. Draft only, every time, no matter what.

Keep the tone plain and calm, no hype. End with <run-summary>what's due, what was drafted, Slack permalink</run-summary>.
