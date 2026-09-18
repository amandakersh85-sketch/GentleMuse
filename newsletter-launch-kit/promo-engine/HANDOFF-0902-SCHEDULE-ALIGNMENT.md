# Handoff: schedule alignment across sessions, 2026-09-02

**From:** `claude/newsletter-signup-strategy-2fpuoq` (funnel, Cesa reach tests, keyword automations)
**To:** `claude/holiday-caption-strategy-m5abq8` (holiday/history series, 3-slot model, draft bank)
**Also for:** any future session that writes to the Blotato queue.

We collided today. Both sessions were scheduling into one 200-post queue with no shared
contract, and it cost a week of October. This file is the contract. Read it before you
schedule, delete, or refill anything.

Direct session-to-session messaging does not work between these environments — it was tried
today, both by session id and by title, and neither resolves. **This repo and Amanda are the
only channels.** Write here; do not assume the other session will hear you any other way.

---

## 1. Immediate, if you are the holiday-caption session

You are blocked on a permission prompt for `blotato_delete_schedule` id `3970845`.
**That post no longer exists.** All 19 X/Twitter posts were deleted on Amanda's instruction
at ~16:10 UTC today, `3970845` among them. Deny the prompt.

**A Blotato delete can return an error and still have worked.** `blotato_delete_schedule`
returned `Blotato API error. Try again in a moment.` three times on one id; a follow-up
`blotato_get_schedule` returned `Not found`. The first delete had succeeded and only the
response failed. **Confirm with `get_schedule` before retrying or concluding a delete failed.**
Two earlier deletes this session were abandoned on this same error and were probably fine.

---

## 2. The open question: who cleared Oct 1-6, and does it get restored

Between roughly 16:05 and 16:25 UTC today, **19 future-dated posts across Oct 1-6 vanished.**
None were X posts.

| Date | Posts before | Survived |
|---|---|---|
| Oct 1 | 4 | **0** |
| Oct 2 | 5 | **0** |
| Oct 3 | 2 | **0** |
| Oct 4 | 3 | **0** |
| Oct 5 | 5 | **0** |
| Oct 6 | 5 | **0** |
| Oct 7 | 6 | 5 |
| Oct 8 | 4 | 3 |

The Oct 1-6 window went to **zero survivors** while Oct 7 and 8 lost only the X posts this
session deleted. That sharp boundary is a deliberate bulk clear, not cascade damage: the X
deletions were spread across Sept 3 - Oct 10, so collateral would have been spread the same
way instead of landing inside one contiguous block.

The holiday-caption session's own task summary reads *"3-slot model building: 200 posts
captured, planner working, rate-limited deletions in progress."* That is the most likely
explanation — October cleared to be rebuilt on a 3-slot model, probably forced by the 200-post
cap.

**All 19 are recoverable in full** — text, media URLs, account ids, original times — in
[`RECOVERABLE-OCT-1-6.md`](RECOVERABLE-OCT-1-6.md). Six Facebook, five Instagram, three TikTok,
two LinkedIn, one YouTube, one Cesa.

**Answer needed before anything is restored:**
- **(a) Cleared on purpose, refill in progress** -> they stay deleted. Restoring would fight
  the rebuild and re-create the collisions.
- **(b) Not you, or unintended** -> all 19 go back to their original slots.

Nothing gets restored without that answer. Write it into this file.

---

## 3. The scheduling ladder — build the 3-slot model on these times

Full derivation in [`../SCHEDULING-LADDER.md`](../SCHEDULING-LADDER.md). Source:
`getBestTimeToPostByNetwork`, brandId `6066935`, `America/Chicago`, pulled 2026-09-02.

| Account | Primary | Secondary | UTC |
|---|---|---|---|
| Instagram @thegentlemuse2026 | 10:00 AM CT | 3:00 PM | 15:00 / 20:00 |
| Instagram @cesasgoldenyears | 11:30 AM CT | — | 16:30 |
| Facebook, The Gentle Muse | 12:00 PM CT | 5:00 PM | 17:00 / 22:00 |
| TikTok, both accounts | 6:00 PM CT | 12:00 PM | 23:00 / 17:00 |

**Minimum 2 hours between posts on the same account.**

Why not everyone at 10 AM, which is what both sessions were doing:

| Platform | 10 AM | Its assigned slot | Cost of moving |
|---|---|---|---|
| Instagram, Wed | 6,506 | 6 PM = 4,869 | **-25%. Too expensive. It keeps 10 AM.** |
| Facebook, Wed | 15,528 | 12 PM = **15,834** | **better than the peak** |
| TikTok, Mon | 1,089 | 6 PM = **1,096** | **better than the peak** |

Facebook and TikTok give up 0-4%. Instagram — the account chasing 500 followers — keeps the
hour it cannot afford to lose. Both sessions stacking into 10 AM produced **10 same-minute
collisions**, since fixed.

**Timezone trap that will bite you.** Four Cesa posts sat at `00:00Z`, which is **7 PM CT the
previous day**. Mapping those to their UTC date would have pushed each post a full day late.
Map by **Central-time day**. September is CDT (UTC-5), so 11:30 AM CT = 16:30Z on the local date.

---

## 4. The cap, and how to read the queue without being wrong

**The plan caps at 200 scheduled posts.** At the cap, new posts fail outright. We hit it
today, which is very likely why a week got cleared to make room.

**The queue is now at 161.** 19 slots were freed by deleting X entirely.

X is dead and should not be re-queued. Justified from source, re-confirmed live immediately
before deleting rather than trusted from notes: `blotato_list_top_posts` for `twitter`,
`since` 2026-06-01, sorted by views, returns `{"items":[]}` — **no rows across three months**,
on a platform Blotato *does* instrument. X had also failed every video upload for six straight
days. All 19 captions archived in [`DELETED-X-QUEUE.md`](DELETED-X-QUEUE.md).

**Paging discipline.** `blotato_list_schedules` returns max 50 per page. **Follow the cursor
until you get an empty page**, and state how many posts you examined against the API `count`
when you report a sweep. Reading page 1 and stopping produced a wrong "zero collisions" answer
here on 08-30.

**Never bulk-delete a date window without pulling the content out first.** That is what
`RECOVERABLE-OCT-1-6.md` is; do the same before clearing anything the other session may have
filled.

---

## 5. The mission, so the draft bank refills toward it

**Goal: 500 Instagram followers.** The binding constraint is **reach, not volume.**

One post did essentially all the work:

| Post | Views | Reach | Shares | Likes |
|---|---|---|---|---|
| `6250675`, Aug 18 | **7,726** | **7,109** | **54** | 731 |
| next best of 25 | 1,865 | 1,289 | 4 | 58 |

Followers went **42 -> 173 in the seven days after it.** In the six days after that: **+4.**

**One Reel produced +131. Everything published since produced +4.** More posts is not the
lever. Shares are.

### What the numbers say a winning post looks like

- **~280 characters. Three sentences and a CTA.** The winner was 280. Posts after Aug 26 ran
  480-640 characters and pitched the guide inside the caption body; 24-hour reach fell about
  **7x** (1,250-3,226 down to 159-790) across every content type, not just the dog posts.
- **Shares are the distribution mechanism.** 54 against 9 for the next highest in the set. The
  winner was still climbing at day 7 (3,226 views at 24h -> 7,726 by day 7). **Nothing without
  shares grew past day one.**
- **Write one sendable sentence.** What gets shared is a line someone wants to send to a
  specific person. *"She just wants me back"* is sendable. Funny is not the same as sendable.
- **Do not ask for the share.** One post literally said *"Send this to someone whose dog helped
  raise her"* and got **1 share, 192 views.** The ask does not produce shares. The feeling does.
- **Reels over carousels, pending a verdict.** One carousel got a **reach of 4** the same day a
  Reel got 331. That is n=1, so two more carousels are running as a deliberate test with a
  **verdict due Sept 4**. Do not mass-produce carousels before then.
- **Keep the guide pitch out of the caption body.** Short CTA, at the end.

### It is not an engagement problem

Recent posts run 9-13% engagement on the reach they get, which is healthy. Reach of 126-195
against ~100 followers means Instagram is serving her own followers and almost nobody new.
The content lands on whoever sees it. The problem is who sees it.

---

## 6. The intake problem, and what NOT to do about it

**Across all 14 live Blotato DM automations, real keyword usage since Aug 8 is ZERO.** Not low.
Zero. Every RESET / CESA / TUESDAY / CONSIDER CTA sitting in the queue has never once been
fired by a real person.

Blotato keyword matching is **case-sensitive and substring-based** — a comment reading
"Keep playing" did not fire `PLAY`.

The conclusion is *not* "write more CTAs" or "add keyword variants." It is that reach is the
bottleneck and **a CTA must not eat the characters that should carry the sendable sentence.**

Also live and worth not breaking: Instagram allows **one DM per comment** (error 20102).
Public comment replies do not consume that slot.

### Verified links only

| Offer | Link |
|---|---|
| Consider This | https://consider-this.subscribepage.io |
| Just Another Tuesday | https://just-another-tuesday-gm.subscribepage.io |
| AI Guide (free) | https://ai-guide.subscribepage.io |
| Press Play | https://press-play.subscribepage.io |
| Reset Guide (free) | https://payhip.com/b/9FE2U |
| Essentials | https://www.gentlemuse.co/tiktok |

**NEVER use:** `reset-guide.subscribepage.io` (belongs to a different creator),
`preview.mailerlite.io/...` share links, `gentlemuse.co/reset-guide` (dead Wix page).

---

## 7. Ownership split, proposed

| Session | Owns |
|---|---|
| `claude/holiday-caption-strategy-m5abq8` | **October forward** — holiday/history series, the 3-slot model, draft bank refill |
| `claude/newsletter-signup-strategy-2fpuoq` | **Now through Sept 30** — funnel, Cesa reach tests, keyword automations, this ladder |

### Rules of engagement, either session

1. Schedule on the **ladder times**. 2-hour minimum between same-account posts.
2. **Page to an empty page** before claiming a clean sweep; report the count you examined.
3. **Never bulk-delete a date window** without archiving its content to a file first.
4. **Confirm deletes with `get_schedule`** — the error response lies.
5. Watch the **200 cap**. At 161 now; roughly 39 slots of headroom.
6. Changing the ladder means changing `SCHEDULING-LADDER.md` and telling Amanda, because the
   other session will not hear it any other way.

---

## 8. Reply here

Append your answers to this file and push:

- [ ] **Oct 1-6:** deliberate clear (leave deleted), or unintended (restore all 19)?
- [ ] **Ladder:** adopting these times for the 3-slot model? If it conflicts with something in
      your model not visible from here, say what and this side will adjust rather than fight it.
- [ ] **Draft bank:** confirm the refill targets the winning shape in section 5 — Reels,
      ~280 characters, one sendable sentence, short CTA at the end.

---

# RESOLVED, 2026-09-02: holiday-caption session is lead

**Amanda's decision.** `claude/holiday-caption-strategy-m5abq8` is **lead on the posting
project** and will fill the open slots. The question in section 2 is closed:

- **Oct 1-6 stays deleted.** The clear was deliberate. Nothing is restored.
- **`RECOVERABLE-OCT-1-6.md` is now a copy bank, not a restore list.** It holds **19 finished
  posts** — text, media URLs, account ids. The lead is filling roughly that many slots, so
  that copy is there to pull from rather than write from scratch. Reuse it or ignore it; just
  do not treat it as a queue to be restored.
- **This session stands down on the queue.** No further scheduling, moving, or deleting from
  `claude/newsletter-signup-strategy-2fpuoq` without Amanda asking.

## Queue state at handover

| Checkpoint | Count |
|---|---|
| Before any of today's work | 200 (**at cap**) |
| After X deleted (19) | 161 |
| After the lead's clearing | **137** |

**63 slots of headroom.** Verified by paging to the end: 137 examined against an API count of
137.

## Two things left on the lead's desk

This session found these and **did not touch them**, because the lead owns the queue now.
Both were created by moves made after the 161-post verification, and both are on Instagram —
the account chasing 500 followers.

### 1. Two 1-hour collisions on IG main

The ladder minimum is 2 hours on the same account.

| Moved post | From | To | Collides with | Gap |
|---|---|---|---|---|
| `3691551` | Sep 5, 20:00Z | Sep 14, 22:00Z | `3472650` @ 23:00Z | **1.00h** |
| `3630603` | Sep 3, 22:30Z | Sep 15, 22:00Z | `3691541` @ 23:00Z | **1.00h** |

Two Instagram posts an hour apart split the same audience window. Suggested fix: move the
22:00Z post of each pair to 20:00Z, the Instagram secondary slot, which restores a 3-hour gap.

### 2. A paid partnership post moved 12 days — needs Amanda, not an agent

**`3630603` is the `#TargetPartner #ad` Adornia necklace post on Instagram.** It was moved
from **Sept 3 to Sept 15**.

Earlier today this session deliberately declined to move the *TikTok* version of this same ad
to a different date, on the grounds that **the date a paid post runs is Amanda's call and a
brand deal may carry a delivery window.** That reasoning applies identically here. The
Instagram version has now moved 12 days regardless.

**Flag for Amanda:** confirm the Target partnership has no delivery deadline that Sept 15
misses. If it does, this needs moving back, and that is a business decision rather than a
scheduling one.

## Standing rules, unchanged and still binding on whoever schedules

1. Ladder times. 2-hour minimum on the same account.
2. Page the cursor to an empty page; report the count examined against the API count.
3. Archive a date window's content to a file before bulk-deleting it.
4. Confirm deletes with `get_schedule` — the error response lies.
5. Watch the 200 cap.
6. **Do not move a post carrying `#ad` or `#TargetPartner` to a different date.** Within the
   same day is fine. Across days is Amanda's call.
