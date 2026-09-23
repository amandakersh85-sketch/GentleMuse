# MailerLite weekly health — Mondays

- id: trig_01Fp2vySvszCDu2kyFHvmsqb
- cron (UTC): 25 14 * * 1
- enabled: True
- bound session: fresh each run
- connectors: MailerLite, Slack
- model: default

## Prompt

Weekly MailerLite check for The Gentle Muse. Use the MailerLite connector. This runs autonomously — Amanda is not present. Read-only status check — do not create, import, activate, or send anything.

STEPS:
1. Get the account's total subscriber count.
2. List groups — find "Gentle Muse Subscribers", report its active count.
3. List automations — find "Reset Guide Welcome + Nurture Sequence, GM" (or similarly named welcome automation). Report whether it's enabled, and if automation activity shows send/open data, summarize it briefly.
4. If the account still shows any sender/domain verification issue when you try a light check (e.g. automations list works but no send data exists yet), just note "sender still needs verification" or "no data yet" — don't treat that as a problem to solve, just report it.
5. Post a short, plain-English summary to Slack channel C0B6B4LHDPT: subscriber count, group size, automation status, and one sentence on whether things look like they're moving (growing, flat, or too early to tell). No jargon, no padding — if there's nothing meaningful yet because the list is brand new, just say that plainly.

End with <run-summary>subscriber count + one-word trend + Slack permalink</run-summary>.
