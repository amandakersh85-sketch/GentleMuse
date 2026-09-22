# Blotato refill (Sonnet, every 2 days)

- id: trig_01CiLyBpQXyJfk242UsTec7g
- cron (UTC): 0 11 */2 * *  (6:00 AM Central, every 2 days)
- enabled: True
- bound session: fresh each run
- connectors: 13 stored on the routine (Blotato is the only one used). Connectors cannot be changed from a session, so trimming them needs the routine's own settings page.
- model: claude-sonnet-5
- changed 2026-09-22: was Opus, daily, a 9,700 character prompt that did every placement decision by hand and re-read the SOP from Drive. Placement now lives in `blotato-refill/refill.py`, with its rules in `blotato-refill/README.md`.

## Prompt

Blotato queue refill for The Gentle Muse. Fresh session. A script makes every placement decision; your job is to feed it the queue, send exactly what it plans, and save the log. Keep this run small: use only the Blotato tools, do not read files you do not need, do not reason about individual posts.

1. Get the code and the libraries, in the GentleMuse repo:
   git fetch origin main claude/routine-audit-dashboard-2mf256 claude/club-target-game-plan-9xs2du
   git show origin/main:blotato-refill/refill.py > /tmp/refill.py 2>/dev/null || git show origin/claude/routine-audit-dashboard-2mf256:blotato-refill/refill.py > /tmp/refill.py
   git worktree add -B claude/club-target-game-plan-9xs2du /tmp/ct origin/claude/club-target-game-plan-9xs2du
   If the repo or the branch cannot be reached, stop and report exactly which command failed. Load nothing.

2. Read the live queue: call blotato_list_schedules with limit 50, then again with each returned cursor until there is none. Write /tmp/q.json as a JSON list with 1 object per item, and nothing else:
   {"id": item.id, "accountId": item.draft.accountId, "platform": item.draft.content.platform, "scheduledAt": item.scheduledAt, "text": first 150 characters of item.draft.content.text, "media": last path segment of item.draft.content.mediaUrls[0], or ""}
   Check the object count matches the "count" the tool reported.

3. python3 /tmp/refill.py plan --lib /tmp/ct --queue-file /tmp/q.json --out /tmp/plan.json --report /tmp/report.md
   If the report begins with a stop reason, skip to step 6.

4. For every entry in /tmp/plan.json whose "args" is not null, call blotato_create_post with exactly those args, in file order. Change nothing. If one fails with "maximum number of scheduled posts (200)", stop creating: that means full, not broken. Note any other error with its exact text and carry on. Keep the list of entry ids that succeeded.

5. python3 /tmp/refill.py log --lib /tmp/ct --plan /tmp/plan.json --ids <succeeded ids, comma separated>
   Copy /tmp/report.md to /tmp/ct/content/refill-reports/<today UTC, YYYY-MM-DD>.md and to latest.md in the same folder, edited only to change "Would load (propose only, nothing sent)" to "Loaded" with the real count. Then in /tmp/ct:
   git add content && git -c user.email=noreply@anthropic.com -c user.name=Claude commit -m "Blotato refill <date>" && git push origin HEAD:claude/club-target-game-plan-9xs2du
   Retry the push up to 3 times with git pull --rebase between. If it still fails, say so at the very top of your reply: the next run would load those rows twice.

6. Call blotato_list_posts with status ["failed"] and since 3 days ago. Name each with platform, time and exact error. A failed TikTok costs points: say so first.

7. Reply with the report and any errors, in Amanda's voice: warm, plain, short. No em dashes, digits not words, times in Central. Never claim something was scheduled that was not.

If this run's extra message says DRY RUN: do steps 1 to 3 and 6 only, create nothing, commit nothing, push nothing, and reply with the plan report.
