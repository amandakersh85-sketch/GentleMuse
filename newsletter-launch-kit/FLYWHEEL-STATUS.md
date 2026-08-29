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

## What is genuinely left, after actually trying

An earlier version of this file listed 5 items as impossible from this session. That was
wrong on 2 of them. The dedicated MCP tools cannot do those things, but
`mcp__MailerLite__batch_requests` executes **arbitrary MailerLite API calls**, and it was
never tried. Two items were closed with it.

### Closed 2026-08-27 via the raw API

| Item | How |
|---|---|
| **JAT AI Guide bonus is now ENABLED** (`196972920216486983`) | `POST api/automations/{id}/enable`. Confirmed `enabled: true` on a follow-up read. |
| **Dual newsletter popup is now ACTIVE** (`195832725497709843`) | `POST api/forms/{id}/activate`. Confirmed `active: true`. Feeds both newsletter groups. |

**Method note worth keeping:** `PUT api/automations/{id}` and `PUT api/forms/{id}` both
return **200 while silently ignoring** the field you tried to change. A 200 from this API is
not proof of anything. Always read the returned body and confirm the value actually moved.
The working pattern is action-style endpoints (`/enable`, `/activate`), and a 405 response
is useful: `POST api/forms/{id}/settings` answered "Supported methods: PUT", which is how
that route was found at all.

### Genuinely not possible from here, each verified by probe

1. **Cesa landing page.** There is no landing page API. `api/sites`, `api/pages`,
   `api/landing-pages` and `api/websites` all return 404. Built from Cowork, paste kit ready
   in Drive as `BUILD_0826_cesa-landing-page-paste-kit`, slug `cesa-guide`. Then the URL goes
   in the **@cesasgoldenyears** TikTok bio and 3 captions get their bio line restored:
   `3835340`, `3835351`, `3835358`.
2. **Double opt-in on form `195835257531925894`.** 5 attempts: flat field, nested settings,
   full settings replacement, the dedicated `/settings` endpoint, and 3 action-endpoint
   shapes. Every write was accepted and ignored, or 404. **Mitigated and low impact:**
   account-level double opt-in is already `false`, the DM path creates subscribers active,
   and the daily sync sweeps anyone stranded within 24 hours.
3. **X media upload.** Needs an OAuth reconnect in the Blotato dashboard, not an API call.
   Low priority, X has produced 0 impressions.

### One thing Amanda should know about the popup

It is now live on gentlemuse.co and visitors will see it. It carries `double_optin: true`,
so signups there land unconfirmed and are picked up by the daily sweep within 24 hours
rather than instantly. Switching it back off is one call if she does not want it:
`POST api/forms/195832725497709843/activate` is what turned it on.

---

## Update 2026-08-29: first live keyword traffic, and a delivery bug it exposed

### The Cesa landing page is LIVE

`https://cesa-guide.subscribepage.io` exists, built outside this session on 2026-08-28,
using exactly the `cesa-guide` slug from the Drive paste kit. **That closes the item this
file listed as impossible from here.** It was always a Cowork job and Cowork did it.

The CESA automations were rewired the same day: `2952` (Cesa IG) and `445` (Amanda IG) had
their **emailGate removed** and now send a button straight to the landing page, which
captures the email itself and feeds the Cesa group. Delivery copy also updated from 13 to
15 pages.

**Consequence for the daily sync:** CESA no longer needs syncing, because the landing page
feeds MailerLite directly. The sync list dropped from 6 automations to 3: `2954` CONSIDER
on Cesa's IG, `2771` and `2772` TUESDAY. The routine was rewritten to rebuild that list
from `blotato_list_automations` every run rather than trusting a hardcoded list, because
this is the second time the set has changed underneath it.

### The keyword fired for real, and 2 of 3 attempts failed

First live traffic through the funnel. Contact `1048429878116670` commented **CESA** on 3
different posts on 2026-08-28:

| Time UTC | Post | Result |
|---|---|---|
| 16:33:03 | `6536249` | **FAILED** error 20102 |
| 18:58:16 | `6533423` | **FAILED** error 20102 |
| 19:32:26 | `6503252` | Sent |

Error 20102: *"The comment you are trying to reply to, already has a reply."*

**Instagram allows exactly one private reply per comment.** If anyone replies to a keyword
comment before the automation does, that slot is spent and the DM never sends. The lead is
lost with no visible sign on the post itself.

**Operating rule, now in the daily sync as step 3:** do not reply to a keyword comment
before the automation has. Let the DM go out first, then reply publicly if you want to.
Every automation run gets checked for failures each day, not just for captures.

### What has not happened yet

No real subscriber. The Cesa group holds 3 records and all 3 are Amanda's:
`amanda@gentlemuse.co` plus `+cesatest` and `+cesatest2`. The person who commented did not
complete the landing page.

**The delivery chain itself is proven though.** `+cesatest` shows 1 sent, **1 open, 1 click,
100% on both**. Comment to DM to landing page to group to guide works end to end. What is
missing is volume, not plumbing.

### Still open

- The 3 Cesa TikTok captions still end on "Follow along for more of her" with no bio line,
  because the bio-link rule says do not write it until the destination is confirmed live in
  the bio. The page now exists, so the moment Amanda confirms it is in the
  **@cesasgoldenyears** TikTok bio, the line goes back. Only `3835358` is still unpublished;
  `3835340` and `3835351` already went out.
