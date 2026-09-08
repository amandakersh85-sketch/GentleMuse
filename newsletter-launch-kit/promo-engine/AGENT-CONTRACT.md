# Agent coordination contract

## 0b. THIS ENVIRONMENT CANNOT FACT-CHECK THE JAT SOURCE DOMAINS

`sabrina.dev`, `substack.com` and `reletter.com` are **blocked by the network egress proxy** in
Claude Code sessions. Confirmed 2026-09-07: `WebFetch` on all three returns `EGRESS_BLOCKED`.

The Just Another Tuesday pre-send check asks whether sabrina.dev is live and what its subscriber
count is. **From here that can only be answered by `WebSearch` summaries, which are not a source
read.** Two searches returning the same figure is one page summarized twice, not corroboration.

So: report the search figure with that caveat attached, recommend wording that stays true across a
range of values, and leave the number itself for Amanda to confirm in a browser. **Never write
"verified" about a JAT source claim from this surface.**

## 0a. IF YOU TOUCH THE BLOTATO QUEUE, READ THE HANDOFF FIRST

**[`HANDOFF-0902-SCHEDULE-ALIGNMENT.md`](HANDOFF-0902-SCHEDULE-ALIGNMENT.md)**

**`claude/holiday-caption-strategy-m5abq8` is lead on the posting project** as of 2026-09-02,
by Amanda's decision. It fills the open slots. Other sessions do not schedule, move or delete
without her asking.

That file carries the ladder times, the 200-post cap, the paging rule, the delete-error trap,
and the reach findings the draft bank refills toward. Queue is at **137 of 200**.

**`RECOVERABLE-OCT-1-6.md` is a copy bank, not a restore list.** 19 finished posts the lead
can pull from. Do not restore them as a queue.

**Never move a post carrying `#ad` or `#TargetPartner` to a different date.** Same day is fine;
across days is Amanda's call, because brand deals carry delivery windows.

**Sessions cannot message each other.** Tried on 2026-09-02, both by session id and by title;
neither resolves across environments. This repo and Amanda are the only channels.

## 0. READ THIS BEFORE ANYTHING ELSE, EVERY SESSION

**Amanda's Google Drive holds the master context. This repo does not.** Open it first:

1. `START_HERE_0818_gentle-muse-master-context` (Drive, root folder). It is titled "read
   this FIRST, before doing anything" and it carries the verified links, account ids,
   group ids, live automations, and the file index for every project doc.
2. The `SOP_*` doc matching your task. The current queue SOP is
   `SOP_0826_blotato-queue-refill-v3`.
3. If your surface has `memory_list` / `memory_read` (Cowork does, Claude Code does not),
   read her memory too.

**This was skipped on 2026-08-27 and it cost real money and real time.** Consequences of
that one omission, all found in a single Drive read:

- The Just Another Tuesday landing page was recorded as "URL unknown" in 4 files here and
  2 rotation slots sat blocked on it. The URL had been documented in Drive since 08/18.
- 6 files pushed `preview.mailerlite.io/...` share links as the canonical signup link.
  That pattern is on Amanda's explicit DO NOT USE list.
- 3 files pointed the Reset Guide at `gentlemuse.co/reset-guide`, a dead Wix page that is
  also on the DO NOT USE list. Amanda is leaving Wix.
- 4 Blotato automations queued for the Sept 11 cutover carried those same dead links.
- A whole session was spent concluding "MailerLite cannot make landing pages," which is
  only true of the Claude Code surface. Cowork has done it repeatedly.

**Surface limits are not product limits.** Before telling Amanda something is impossible,
say which surface you are on and check whether another one already did it. She has had
landing pages built for Consider This, Just Another Tuesday, AI Guide and Press Play, and
she did not build a single one by hand.

### Verified links, from Drive. Use only these.

| Offer | Link |
|---|---|
| Consider This | https://consider-this.subscribepage.io |
| Just Another Tuesday | https://just-another-tuesday-gm.subscribepage.io |
| AI Guide (free) | https://ai-guide.subscribepage.io |
| Press Play | https://press-play.subscribepage.io |
| Reset Guide (free) | https://payhip.com/b/9FE2U |
| Essentials | https://www.gentlemuse.co/tiktok |
| Cesa | instagram.com/cesasgoldenyears (landing page not built yet) |

### TUESDAY keyword destination, corrected 2026-08-27

All 4 TUESDAY automations now point at `https://just-another-tuesday-gm.subscribepage.io`.
Previously 447 and 427 sent people to `ai-guide.subscribepage.io`, which was deliberate
back when JAT had no page of its own. It has one, so that workaround is retired.

| id | Account | Was | Now |
|---|---|---|---|
| 447 | Amanda IG 45886 | ai-guide.subscribepage.io | JAT page |
| 427 | Amanda FB 30840 | ai-guide.subscribepage.io | JAT page |
| 2771 | Amanda IG 45886 | no button, email gate only | JAT page added |
| 2772 | Amanda FB 30840 | no button, email gate only | JAT page added |

Two stale claims were removed from the 447/427 DM copy at the same time, both verified
live against MailerLite:

- "starting September 1" was wrong. JAT #001 sent 2026-08-25. Next issue is #002 on Sep 1.
- "The link below also hands you the 59 page beginner guide" was only true while the
  button pointed at the AI guide page. It no longer does.

### DO NOT USE

- `reset-guide.subscribepage.io` belongs to a different creator, not Amanda
- `preview.mailerlite.io/...` form share links, old and replaced
- `gentlemuse.co/reset-guide`, dead Wix page

---


**For: Claude and Avery/Codex, both working Gentle Muse promo content.**
Amanda's ask: stop duplicating, stop asking her the same questions, check each other's work.

We cannot message each other directly. This repo is the shared workspace. Read this file
before starting work, write to the claim board before building anything, and the duplication
problem goes away.

---

## 1. Claim board — write here BEFORE you build

Add a row before you start. Do not build anything that already has a row.

| Asset | Owner | Status | Date |
|---|---|---|---|
| promo-ai-guide.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-reset-guide.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-tuesday.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| promo-press-play.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| consider-this-launch.png (single card) | Claude | DONE, scheduled | 2026-08-25 |
| 6-slide carousels | Avery/Codex | claimed by Amanda's direction | 2026-08-25 |

**Claude is NOT building carousels** while Avery holds that claim. Claude owns single promo
cards, captions, scheduling, keyword automations, and the newsletter side.

## 2. Naming convention

- Single promo card: `promo-<offer>.png` at 2x, `promo-<offer>-1x.png` at 1x
- Carousel slide: `carousel-<offer>-<nn>.png`, zero padded, `01` is the hook slide
- Everything lives in `newsletter-launch-kit/promo-engine/`
- Commit the HTML source next to the PNG so the other agent can restyle without guessing

## 3. Design system, so both our work looks like 1 brand

Rendered 1080x1350 via headless Chromium from HTML. Fonts are in
`/root/.claude/skills/synced/canvas-design/canvas-fonts/`: Lora (body and headline),
Gloock (numerals and accent figures), Jura (letterspaced labels).

Two palettes, split by audience. Do not mix them on 1 asset.

| Role | Warm (home audience: Consider This, Reset, Press Play) | Cool (builder audience: Just Another Tuesday, AI Guide) |
|---|---|---|
| bg gradient | #F6F1E6 to #F1E9D8 | #F4F4F2 to #EAEAE6 |
| ink | #2B2620 | #262626 |
| muted | #7C7061 | #6E6E6E |
| accent | #B0674C terracotta | #3F5E52 green |
| rule | #D9CFBD | #D5D5CE |

Working generator: `promo-engine/gen.py`. Reuse it rather than rebuilding the template.

## 4. Non-negotiable content rules

Both agents follow these. They come from Amanda directly.

1. **9/10 or it does not ship.** Under 9 is an auto-fail. Rebuild the hook per platform until
   that platform's hook grades 9. One hook reused across platforms is how you land at 8.5.
2. **Keyword CTA every time on Instagram and Facebook.** See KEYWORD-RULE.md. Link goes in
   `firstComment`, never instead of the keyword.
3. Voice: digits not words, no em dashes, no hype, no generic motivation, name the specific
   real detail. Max 5 hashtags on Instagram.
4. Add a share prompt where it fits. Shares are what carried the Press Play carousels to
   roughly 100 views.
5. Nothing publishes without Amanda's approval on new formats. Recycling approved promos on
   the standing rotation is pre-approved.
6. **NEVER GUESS WHEN AMANDA GIVES DIRECTION. CHECK THE SOURCE.** (Her rule, 2026-08-26,
   verbatim emphasis hers.) If she says a thing exists, was set up, or was decided, go read
   the actual source before acting or before telling her it isn't there: this repo's notes
   first, then the live tool (MailerLite, Blotato, Wix, Drive). Do not infer, do not
   reconstruct from memory, do not substitute a plausible alternative for the thing she
   named. If the source says something different from what she remembers, quote the source
   back to her in one line and stop. Guessing has cost her real time more than once.

## 5. What each of us should NOT touch

- **Claude owns:** MailerLite entirely (campaigns, automations, groups), Blotato scheduling
  and DM keyword automations, single promo cards, captions.
- **Avery owns:** the 6-slide carousels currently claimed.
- If you need to change something the other owns, write it in section 6 instead of doing it.

## 6. Cross-checks and open questions

Anything you want the other agent to verify or answer goes here.

- **From Claude, 2026-08-25:** X measured 0 impressions on 2 consecutive promo posts and
  Facebook returned 3 views. Instagram and Pinterest are where the reach is. Carousels should
  be built Instagram-first at 1080x1350, not repurposed from a landscape source.
- **From Claude, 2026-08-25:** the GentleMuse repo is PUBLIC. Scheduled posts reference the
  graphics by raw.githubusercontent.com URL pinned to a commit SHA, which is what makes the
  images render. Do not rewrite history on this branch or the scheduled posts lose their media.
- **From Claude, 2026-08-25:** TUESDAY keyword is live in Blotato on Instagram and Facebook
  with an email gate. Just Another Tuesday no longer needs a public signup URL on those 2
  platforms. It still needs one for X, LinkedIn and Pinterest.
- ~~**Open for Amanda:** the Just Another Tuesday landing page URL~~ RESOLVED 2026-08-27,
  it is https://just-another-tuesday-gm.subscribepage.io, documented in Drive since 08/18.
  Superseded text: the JAT landing page URL, previously believed unknown in this
  workspace.

## 6b. THE SCHEDULING LADDER, non-negotiable

**Instagram @thegentlemuse2026 owns 10:00 AM Central. Nothing else is scheduled there.**
Facebook takes 12:00 PM, TikTok takes 6:00 PM, Cesa's Instagram takes 11:30 AM. Minimum 2
hours between posts on the same account.

Every platform peaks at 10 AM, so every session reaching for "the best time" collides. Two
Reels 2 seconds apart on 08-23 got 1,818 views and 162. Facebook and TikTok give up 0 to 4
percent by moving; Instagram would give up 25 percent, so it keeps the slot.

Before scheduling a batch, page `blotato_list_schedules` to the END using the cursor, and say
how many posts you examined. Full reasoning and the Metricool numbers are in
newsletter-launch-kit/SCHEDULING-LADDER.md.

## 7. Current state, so nobody re-derives it

- 28 posts scheduled Aug 26 through Sep 3. Full list in ROTATION-TEST.md.
- Blotato is the only DM keyword tool. ManyChat was disconnected 2026-08-30, ahead of its
  Sept 11 end. 11 automations live across both IG accounts and the FB page. The 10 named
  `DO NOT ACTIVATE` are duplicates of live ones: never activate them, it recreates the
  one-DM-per-comment race. See BLOTATO-KEYWORD-MIGRATION.md and KEYWORD-RULE.md.
- All MailerLite automations enabled. Both newsletters loaded and scheduled.
- Aug 27 is the last day of the 60 Day AI Journey. From Aug 28 the cadence is 3 posts a day
  with 2 of the 3 being promos.

## 0c. Checking ONE automation without paging 50 at a time

`blotato_list_automations` has no get-by-id, so every gate check has meant paging 50-item pages
until the target appears. The CESA watch does this 12 times a day across 3 automations.

**A cursor is just base64 of `<createdAt>_<id>`** — the values from any earlier listing. Encode
the automation created immediately BEFORE your target (they are ordered newest first, so
"before" means the next one down the list) and pass `limit: 1`. You get exactly your target.

```python
base64.b64encode(b'2026-08-08T19:57:27.092Z_446').decode()  # lands on 445
base64.b64encode(b'2026-08-08T19:48:25.060Z_434').decode()  # lands on 432
```

Verified working 2026-09-08 on both. The response's own `cursor` field confirms which record you
landed on. Known-good anchors:

| Target | Anchor to encode |
|---|---|
| `445` CESA IG main | `2026-08-08T19:57:27.092Z_446` |
| `432` CESA Facebook | `2026-08-08T19:48:25.060Z_434` |
| `2952` / `2954` Cesa IG | `2026-08-27T18:15:02.000Z_2954` (returns both at `limit: 2`) |

This does not replace paging when the job is **counting** or **finding** things — a full sweep
still has to page to an empty page and state the count examined. It replaces paging when you
already know exactly which record you want.

## 0d. AMANDA'S STANDING RULE ON COMMENT REPLIES — 2026-09-08. READ THIS BEFORE ASKING HER ANYTHING.

Her words, verbatim:

> "if you see responses, respond, please, please, for the love of God, please respond to anything
> you have the capability of responding to in a timely fashion. If it's too weird, bring it to my
> attention for an approval before you post, and then I'll say yes. Ninety percent of the time,
> I'm pretty sure I'll approve your drafts."

**The default is POST, not ASK.** This session earned that rule the hard way. It found 12
unanswered comments on Cesa's page going back 11 days, wrote replies for all of them, and then
handed her a wall of drafts to approve while she was walking out the door late for work. One of
those drafts was the words "Thank you xx".

She was right to be angry. The mistake was not caution, it was misapplying a rule.

### Where approval-first actually applies

**Yes:** captions, Reels, newsletters, sales copy, landing pages, anything a `post-grader` or
`reel-blueprint` skill gates, anything going out under a brand partnership.

**No:** replying to a human being who commented on her post. A reply at 3 hours is worth several
times the same reply at 3 days, and asking costs the difference.

### The only things to bring her instead of posting

Sexual, racist or abusive comments (never reply, list them so she can block). Spam and collab
bait. Anyone alleging stolen content, threatening legal action, or accusing her of mistreating
Cesa. A medical question where a wrong answer could hurt an animal. Anything that would require
inventing a fact about her life that the caption does not supply. Anything about an `#ad` or
`#TargetPartner` post beyond a thank you.

**That is the whole list.** Everything else gets posted.

### She replies on the account she can see, and that is not a discipline problem

Her conversational replies concentrate on @thegentlemuse2026 because that is where her
notifications land. @cesasgoldenyears is a second inbox. Facebook is a third. The fix is not to
tell her to check more often — it is for the routine to cover the inboxes she cannot watch.

### Capability, stated plainly so no future session gets this wrong

`blotato_post_comment` posts a public reply as her, on any of her accounts, on any published
post, threaded under any top-level comment. **Meta Business Suite is not required and never was.**
A 201 with `status: queued` is not proof; re-read with `blotato_list_comments` and confirm
`status: posted` with a real `platformCommentId`.

Public replies have **no time window** and do **not** consume the one-per-comment private reply
slot, so an old comment is still worth answering and a public reply never blocks a later DM.

### Executed 2026-09-08

23 replies posted and individually verified: 12 on @cesasgoldenyears clearing a backlog to
Aug 20, 11 on @thegentlemuse2026. Both accounts went to zero unanswered. The oldest was a
commenter who answered a caption's direct question about dog nicknames and had waited 11 days.

Routine `trig_01HK4yKpqXoMKYjpiX6LQUj2` now runs every 3 hours across all three accounts and
posts without asking.

## 0e. THE DM INBOX WAS NEVER BEING WATCHED — found 2026-09-08 20:18

The funnel watch was expanded to discover DM conversations dynamically instead of carrying a
hardcoded list. On its first run with that change it found three threads with activity that day,
and only ONE of them was a thread this session created.

**The instruction had a bug of its own.** It said "every conversation created on or after
2026-09-08". Two of the three were created days earlier and *bumped* that morning, so
`createdAt`-only would have hidden them. Fixed to **`createdAt` OR `updatedAt` in the last 24
hours**. Cheap shortcut worth knowing: when `updatedAt == createdAt`, nothing has happened in that
thread since it was opened, so there is no need to fetch its messages.

### What was in there

| Thread | Contact | What it is |
|---|---|---|
| `504372` | `1061893740060282` | "We love this!!🩷🩷" — a real person, unanswered since 16:47. **Replied.** |
| `490500` | `965890496530269` | Pay-to-collab scheme. **No reply.** |
| `219329` | `1701463360911952` | MLM recruiter, running since Aug 20. **No reply.** |

**`490500` is the one that matters.** @emmamilesx / ratherpeach.com, four messages Sept 7-8, and
the mechanism is: get a discount code, **place an order yourself**, reply DONE, then get
"onboarded" and a personal code to push to followers. As of 16:08 today it added "we have limited
spots" urgency.

Amanda's own screening message, live on automation `415`, says: *"I do not pay shipping,
processing, membership, starter kit, or ambassador fees."* This offer requires her to buy the
product to become an affiliate for it. It is exactly what that sentence exists to refuse.

**`219329`** has been running since Aug 20 with periodic bumps — "freedom-based online business",
"my team", a "high-ticket affiliate" Roadmap. Standard MLM recruitment.

### `415` PR screening is missing these, and it is the same bug as the keywords

`415`'s keywords are multi-word phrases: `like to collab`, `gifted collab`, `pr package`,
`brand ambassador`, `partnership opportunity`. The pitch that got through said **`Tap "collab"
below 💌`**. It contains "collab" but not "like to collab", so nothing fired.

This is the **third** instance today of the same failure: a multi-word keyword assuming word
adjacency while a real human puts other words in between.

| Keyword | Real text | Fired |
|---|---|---|
| `my chi` | "my **healthy** chi that's about to turn 9" | no |
| `like to collab` | 'Tap "collab" below' | no |
| `my dog` | "my old dog" (predicted, same shape) | no |

**Proposed, not applied:** add the standalone token `collab` to `415`. Keyword changes are config
and Amanda approves those. Worth noting `415` is `message-received`, so a false positive there
costs almost nothing — it just sends her screening boilerplate to someone who said "collab".

### Standing rule that follows from this

Her DM inbox holds real people and real solicitations, and nothing was reading it. The watch now
does, every 2 hours, and it REPLIES to real people rather than reporting them — per her rule of
2026-09-08. Solicitations are never answered on her behalf: they get quoted to her and left alone.

Note the constraint difference. A plain DM reply only works within **24 hours** of the person's
last message, and once that window closes it is gone — unlike a comment, where a public reply
works forever. So an unread DM decays in a way an unread comment does not.
