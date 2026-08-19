# GENTLE MUSE — LOCAL EXECUTION HANDOFF
**Paste everything below as your first message in Claude Code on your own machine.**

---

You're picking up a system Amanda Kersh (The Gentle Muse) has been building since
April 2026. It is real, it works, and it has never been run end to end on her own
hardware. Your job is to execute it, not redesign it.

## WHO AND WHAT

Amanda runs 3 LLCs plus 2 personal content lanes:
- **GM** — The Gentle Muse (main brand, content, digital products, funnels)
- **KV** — Kersh Vending Services
- **FS** — Fresh Spin Laundry
- **CGY** — Cesa's Golden Years (personal archive lane, not sales-first)
- **Personal / OF** — private lanes

The bottleneck is production, not strategy. She has raw footage, a finished
automation layer, and 100+ content pieces. She does not have a repeatable way to
turn raw files into shipped video. That's what you're finishing.

## WHAT ALREADY EXISTS — DO NOT REBUILD ANY OF THIS

Built April to June 2026. It works. Read before you touch.

| Thing | What it does |
|---|---|
| `asset_scanner.py` | SHA-256 duplicate detection, propose-only filing engine. Day 8. |
| Downloads Maintenance SOP | 28-run cleanup system with a run counter. Runs 1 and 2 done. |
| Monday Downloads Audit | Scheduled task, runs hands-free |
| Master Asset Index | Google Sheet, the card catalog. THE schema of record. |
| The Hub | 18 destination folders |
| `Upload Batch A.ps1`, `Load Cesa Photo Batch, CGY.ps1` | PowerShell loaders |
| Blotato Queue Refill SOP v2 | 658-post staging library, wave system |

**Master Asset Index columns are the schema everything outputs to:**
`Asset Name | Type | Lane | Category / Use | Lives On | Folder / Location | Direct Link | Status | Needs Filing?`

## WHAT'S NEW — BUILT 08/19/2026, NEVER YET RUN

3 triage modules extending the 28-run system to media. Each has a matching SOP
in Google Drive. All are **syntax-validated but never executed on Windows.**
First run is the real test.

| Run | Script | SOP | Handles |
|---|---|---|---|
| 3 | `GM-Video-Triage.ps1` | SOP_0819_video-triage-run-3 | Footage. Duration, orientation, thumbnails. |
| 4 | `GM-Photo-Triage.ps1` | SOP_0819_photo-triage-run-4 | Stills. Burst grouping, screenshots, Takeout sidecars, GPS privacy gate. |
| 5 | `GM-Doc-Triage.ps1` | SOP_0819_document-triage-run-5 | Paper. Version families, entity routing, sensitive HOLD, dual reports. |

## DO THIS FIRST — THE FIRST 20 MINUTES

Run these in order. Report back after step 5. Don't skip ahead to `-Execute`.

1. **Check the toolchain.**
   ```powershell
   ffmpeg -version
   ffprobe -version
   ```
   Missing? `winget install Gyan.FFmpeg` then reopen PowerShell.

2. **Put the 3 scripts next to `asset_scanner.py`.** Find that file first. Wherever
   it lives is where these belong.

3. **Unblock them.** They came from the internet, so PowerShell will refuse:
   ```powershell
   Get-ChildItem GM-*-Triage.ps1 | Unblock-File
   ```

4. **Run 5 first, propose-only.** Downloads is the smallest, fastest, highest
   signal target. Do NOT start with the Takeout export.
   ```powershell
   .\GM-Doc-Triage.ps1 -Root "$env:USERPROFILE\Downloads"
   ```

5. **Read `SUMMARY.txt`. Report the HOLD count to Amanda before anything else.**
   HOLD is the sensitive pile. If it's large, that's the headline finding.

Then, only after she's seen it:

6. Run 3 against her footage folder, propose-only.
7. Run 4 against the Takeout photos, propose-only. This one is slow. Expect thousands.
8. Bring her the numbers. She decides what gets `-Execute`.

## NON-NEGOTIABLE RULES

These are house rules from her existing system. Breaking one is worse than
doing nothing.

- **Propose-only is the default.** Never pass `-Execute` without her explicit
  approval on that specific run's CUT list.
- **Nothing deletes. Ever.** `-Execute` moves to `_QUARANTINE`. She empties it herself.
- **HOLD is never automated.** Sensitive documents are not moved, renamed,
  archived, sent, or filed by you. She routes those by hand.
- **Never send `doc-triage-LOCAL-ONLY.csv` anywhere.** Not to Claude, not to Drive,
  not to email. Only `doc-triage-SHAREABLE.csv` leaves the machine.
- **GPS-flagged photos never auto-KEEP.** Location data publishes her house.
- **UNSORTED beats a wrong guess.** Never guess an entity on a financial document.
- **Don't push to any repo without asking.**
- **She approves. Always.** Machine verdicts are proposals, not decisions.

## VOICE RULES — for any caption, SOP, or copy you write

From her own Blotato SOP. These are enforced, not suggestions.

- No em dashes. Use commas and periods.
- Digits, not spelled-out numbers. 5, not five.
- Contractions always.
- Warm, grounded, practical. No hype, no boss babe energy.
- Instagram maximum 5 hashtags. Facebook and LinkedIn none.
- Never state a price on affiliate content. Open TikTok Shop violation from 08/04/2026.

## WHAT SUCCESS LOOKS LIKE TODAY

Not a clean hard drive. Answers:

1. **How many sensitive files are loose in Downloads?** (Run 5 HOLD count)
2. **How much real footage of Amanda actually exists?** Google Drive holds only
   about 5 clips. If local is the same, the bottleneck is filming, not sorting,
   and the whole plan changes.
3. **How much usable brand imagery exists?** The index lists roughly 12 content
   photos for GM. If local holds 200 more, the carousel and Pinterest lanes
   unblock without a shoot.

Those 3 numbers are the deliverable. The megabytes are a side effect.

## ALREADY DONE, DON'T REDO

- Google Drive video duplicates: 15 files trashed 08/19/2026, about 151 MB.
  Drive side is finished. These runs are the local side.

## IF SOMETHING THROWS

Paste the full error. The scripts are validated for syntax and confirmed to hold
no delete commands, but they've never touched a real Windows filesystem. Likely
first failures: execution policy, a path with brackets or apostrophes, or an
ffmpeg build without HEIC support. All are quick fixes. Don't work around a
failure by disabling a safety rule.

## ASK BEFORE YOU DO

- Any `-Execute` run
- Anything touching a HOLD file
- Anything that leaves the machine
- Any change to `asset_scanner.py` or the existing SOPs
- Any new tool or paid service. Budget ceiling is 10 USD per month and she
  already pays for several credit-based tools.
