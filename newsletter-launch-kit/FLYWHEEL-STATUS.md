# Flywheel status — full snag, delay and leak sweep

**Swept:** 2026-08-27, everything verified live against MailerLite and Blotato, not from notes.
**Goal:** fully operational funnel with no snags, delays or leaks.

---

## Snags found and fixed today

### 1. Every video post to X had been failing for 6 days

11 consecutive failures since Aug 21, all `Could not upload media to Twitter`. Text posts
publish fine (Post 3 proved it on Aug 25). Video does not.

**11 more were queued and would all have failed**, the first at 2026-08-27 19:30 UTC.
All 11 converted to text only. Their copy stands alone, is under 280 characters, and
already used the verified links. They now publish instead of failing.

**Still open for Amanda:** X media upload is broken at the account level, most likely the
API tier or an expired media scope. Reconnecting X in Blotato is the fix if she wants video
back on that channel. Low priority: X has produced 0 impressions.

### 2. TUESDAY was double DMing, live

`447` and `2771` were **both active** on Instagram with the same keyword, same account,
same trigger. Same for `427` and `2772` on Facebook. Anyone commenting TUESDAY got 2 DMs.

Kept `2771` and `2772` because they carry an `emailGate` and actually capture the address.
Retired `447` and `427`, which only handed out a link and captured nothing.

### 3. RESET was completely dead on Facebook

`412`, `413` and `2778` were all inactive, so commenting RESET on the page returned nothing.
The master context lists RESET as live on both channels, so this was a silent regression.
Activated `2778`, which points at the verified `payhip.com/b/9FE2U`.

### 4. Ten Sept 11 cutover drafts would have recreated the double DM

Every `[Sept 11 cutover]` draft duplicates a keyword that is already live. Activating them
without retiring the originals double DMs on every keyword. All 10 renamed to start with
**DO NOT ACTIVATE** and name the live automation they duplicate.

`2781`, `2953` (dup of live `445`), `2782` (dup of `432`), `2773` (dup of `1393`),
`2774` (dup of `1394`), `2775` (dup of `1424`), `2776` (dup of `1422`),
`2777` (dup of `435`), `2779` (dup of `1019`), `2780` (dup of `1020`).

### 5. A signup sat stranded for 4 days

Covered in FLYWHEEL.md. Laura recovered, welcome fired 18:08:42.

### 6. Eleven scheduled posts carried dead links, first firing that night

Purging the deprecated links from this repo did not touch the live Blotato queue. A full
scan of all 147 scheduled posts found 11 still carrying them, the earliest due 2026-08-28
00:20 UTC, which is 7:20 PM Central that evening.

- 7 YouTube shorts, 2 X posts, 2 LinkedIn posts pointed at `gentlemuse.co/reset-guide`,
  a dead Wix page on the DO NOT USE list. Repointed to `https://payhip.com/b/9FE2U`.
- 1 X post and 1 LinkedIn post pointed at a `preview.mailerlite.io` share link, also on the
  DO NOT USE list. Repointed to `https://consider-this.subscribepage.io`.

**Verified after the fix:** all 147 scheduled posts rescanned. 0 DO NOT USE links remain,
and 0 X posts still carry media that would fail.

**Lesson recorded:** fixing a link in the repo is not the same as fixing it in the queue.
Any link correction has to be applied to both, and the queue check is the one that matters
because the queue is what actually publishes.

---

## Two records in this repo were wrong, now corrected

- **The dual popup is not misrouted.** FLYWHEEL.md said it feeds Gentle Muse Subscribers
  instead of the newsletter groups. It actually feeds **both** newsletter groups correctly,
  has content, and is not broken. It is simply **inactive**. Switching it on is a dashboard
  toggle and would put a working signup popup back on the site.
- **The Reset popup is not misrouted either.** It feeds Gentle Muse Subscribers, and the
  Reset nurture triggers on exactly that group. Correct as built.

---

## What is verified healthy

| Piece | State |
|---|---|
| All 3 previously pending automations | **ON** (Consider This welcome, cross-invite, JAT welcome) |
| Newsletter cross-invite | **7 subscribers queued**, all fire 2026-09-08 |
| Cesa Guide Delivery | enabled |
| Reset, AI Guide, Press Play, Bottleneck nurtures | all enabled |
| 11 queued campaigns | all `is_eligible_for_sending`, `needs_repair: false` |
| TikTok | healthy, 30 published across both accounts, the 1 failure was an isolated URL hiccup |
| Keyword coverage | every offer now has exactly 1 active automation per account, no gaps, no duplicates |

---

## Delays now guarded

Both newsletters run dry on a known date. Warnings armed with 3 weeks of lead time.

| Newsletter | Last issue | Goes dry | Warning fires |
|---|---|---|---|
| Just Another Tuesday | #005, 2026-09-22 | after Sept 22 | **2026-09-08** |
| Consider This | #009, 2026-10-15 | after Oct 15 | **2026-09-24** |

---

## What is genuinely left, and why an agent cannot do it

Each of these is a dashboard or Cowork action. Every one has been verified as impossible
from the Claude Code surface, not assumed.

1. **Cesa landing page.** Built from Cowork, where the other 4 came from. Paste kit is ready
   in Drive as `BUILD_0826_cesa-landing-page-paste-kit`, slug `cesa-guide`. Then the URL goes
   in the **@cesasgoldenyears** TikTok bio, and 3 captions get their bio line restored:
   schedule ids `3835340`, `3835351`, `3835358`.
2. **Activate the JAT AI Guide bonus** (`196972920216486983`). API creates automations
   inactive and exposes no activate tool.
3. **Double opt-in on the Consider This form.** `update_form` sets the name only. Mitigated:
   the DM path now creates subscribers active, and the daily sync sweeps anyone stranded.
4. **Activate the dual newsletter popup** (`195832725497709843`). Ready and correct, just off.
5. **Reconnect X in Blotato** if video on that channel matters.
