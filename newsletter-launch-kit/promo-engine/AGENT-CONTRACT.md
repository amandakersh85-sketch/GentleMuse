# Agent coordination contract

## 0-AWAY. AMANDA BEING AWAY IS NOT A CONTENT PROBLEM. SET 2026-09-11. PERMANENT.

Claude planned around her Nov 5 to 11 cruise as if it were a blackout window. She corrected it:

> *"Don't assume we're automatically going to skip that just because I'm on a cruise. That's the
> entire purpose and point of having Blotato and our refill queue draft situation, so I can
> actually go live my life and have fun and have social media take care of itself."*

**The queue posts without her. That is the whole point of the queue.** She has been scheduling
weeks ahead since August.

**Never frame her travel, her shift, her sleep or her time off as a risk to the content.** Do not
build "blackout windows". Do not propose skipping days. Do not treat a week away as something to
survive. The correct posture is that the machine runs and she lives her life.

**The only thing that genuinely pauses is live human work:** comment replies and in-the-moment
judgment. Even that is recoverable, because public comment replies have no time limit and do not
consume the single private-reply slot. A backlog waiting when she gets back is normal, not damage.

**The one real deadline is approval**, because only she can approve copy. Get batches to her
before she is hard to reach, as a courtesy, not as risk mitigation.

## 0-RATIO. ONE RENDER PER FACT. SET BY AMANDA 2026-09-10. PERMANENT.

Her words: *"fix the ratio ... anything that you see we haven't used, from all of what we have
now, let's keep it fully cohesive and rotated."*

**The rule: 1 media render per IDEA, reused on every platform that idea runs on.**
A second render only when the aspect ratio genuinely differs, which in practice means Pinterest
and nothing else. **Never 1 render per post.**

### Why this exists
**CORRECTED 2026-09-10, same day.** The first measurement counted distinct `mediaUrls` and
reported 146 files at 7.3 per idea. That was wrong. **Blotato mints a fresh storage URL every
time media is attached to a post**, proven by handing 6 identical image URLs to 2 posts and
getting 12 different URLs back. URL count is not file count.

Re-measured by actual byte size across all 146 URLs: **at most 90 distinct files behind 117
posts**, carrying about 20 facts. **Roughly 4.5 files per idea**, not 7.3. The mare and
sleep-paralysis fact has 8 posts running on 4 distinct files, not 8.

90 is an upper bound. A platform re-encode of one source counts as a separate file by size
without being separate creative work, so the true number of renders is 90 or fewer.

At 4.5 the 32 new seasonal nights would cost about 144 renders. At 1 per idea reused, 32. Plus
Pinterest crops, 64. The waste is real and the rule still holds, it is just about half the size
first reported.

**Storage duplication itself is free.** It happens automatically on attach and costs nothing.
Only generation costs.

### What this obligates, every time
1. Before generating anything, check whether a render for that idea already exists. Reuse it.
2. When an idea cross-posts, pass the SAME `mediaUrls` value to every platform.
3. Only regenerate for a real aspect-ratio change, and say which ratio and why.
4. If a batch would produce more files than it has ideas, that batch is wrong. Stop and re-plan.

### Blotato balance
2,974 credits on `amandakersh85@gmail.com`, $6 per 1,000, minimum purchase 1,000. The per-render
credit cost is NOT exposed by the API. Do not quote one. What is certain is that the old ratio
multiplied whatever that cost is by 7.3.

## 0. PLATFORM RULES SET BY AMANDA 2026-09-10. PERMANENT. DO NOT RE-DECIDE THESE.

### LinkedIn gets business posts only. Never holiday, never seasonal.

Her words: *"LinkedIn only gets the business posts not the holiday posts I need that to be a
permanent rule going forward."*

This is not a preference to weigh against reach. It is a standing rule with no expiry.

**Never schedule to LinkedIn (account `20723`):** anything about Halloween, Samhain, the
seasonal nightly run, holiday history, spooky or horror movie facts, ghosts, witches, graves,
trick or treat, jack o lanterns, Christmas, or any other holiday. If the seasonal campaign is
cross-posting to every channel, LinkedIn is carved out of the loop, not included and filtered
later.

**LinkedIn gets:** what she actually learned building the business, AI worth using in plain
language, systems and automation failures with the mistake left in, practical household or
consumer findings that stand on their own as useful, and the free lead magnets.

Verified clean at the time the rule was set: 14 scheduled LinkedIn posts, 09-11 through 09-24,
0 seasonal. Nothing had to be pulled. The rule exists to keep it that way when the 33-night
seasonal run gets built, because that run would otherwise cross-post straight onto LinkedIn.

Note the LinkedIn queue ends 09-24 and has its own cliff after that.

### X / Twitter is OFF. It stays off unless Amanda says otherwise.

All 19 scheduled X posts were deleted 2026-09-02 under the 200-post plan cap. Copy preserved in
full in `DELETED-X-QUEUE.md`. Confirmed live 2026-09-10: querying X from 08-01 to 12-31 returns
**0 scheduled**. Every X record is `published` (last 2026-09-02 13:30) or `failed`.

Do not refill the X queue as a side effect of building anything else.

**Why it failed, which matters if it is ever revived.** Two separate problems, not one:
1. `blotato_list_top_posts` for twitter since 06-01 returns no rows at all. Not low numbers, no
   rows, across 3 months, on a platform Blotato does instrument.
2. **Every X post carrying video failed**, 11 of them, all with `Could not upload media to
   Twitter`. Only text-only posts ever published successfully.

So the one configuration that has ever technically worked on X is **text-only posts with a
lead-magnet link**. That is her open question, not a decision: she said *"unless you blast x
with my carousels ... it needs to be nothing but free lead magnets ... and see if anything
happens but I don't know I feel like it's not worth the time."* Carousels are images, and image
uploads are in the same media path that failed on video, so a carousel revival is the version
least likely to work. Do not act on any of this without her explicit go-ahead.

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
| 32 seasonal plates (`BRIEF-AVERY-SEASONAL-32-PLATES.md`) | Avery/Codex | **HANDED OFF, awaiting Avery** | 2026-09-10 |
| HeyGen background kit (`BRIEF-AVERY-HEYGEN-BACKGROUND-KIT.md`) | Avery/Codex | **HANDED OFF, awaiting Avery** | 2026-09-10 |
| The Real One, 9 pilot plates (`BRIEF-AVERY-REAL-ONE-PILOT-9.md`) | Avery/Codex | **HANDED OFF, awaiting Avery** | 2026-09-11 |

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

## 0f. CORRECTION: you cannot see Amanda's side of a DM. Never treat her inbox as a queue.

**Found 2026-09-09 04:18, and it overturns a claim this file made six hours earlier.**

`0e` said the DM inbox "was never being watched" and that real messages sat in it unanswered.
**That was wrong.** Blotato records DMs sent *through Blotato* and DMs *received*, but NOT the
replies Amanda sends from the Instagram app.

The proof is in the threads themselves. Conversations `229724` and `219329` contain ONLY
`direction: incoming` messages — and in both, the other person quotes her replies straight back:

> "I like the way you think"
> "You're right about Cesa; you need to take care of her"
> "You're not chasing shiny objects, you're letting the data tell you where to double down"

She has been answering all along. The record is incomplete, and an incomplete record was read as
an empty one. **A missing outgoing message is not evidence of silence.**

### What this breaks

The funnel watch had been instructed to reply to any DM that "looked unanswered". That
instruction was live for six hours and is now revoked. Had it fired on a real thread it could
have:

- replied into a conversation she is actively holding,
- contradicted something she already said and the record does not show,
- and imitated a register that is hers — one thread contains "Yes honey".

### The rule now

**Her DM inbox is correspondence, not a work queue. Read it, report it, do not answer it.** The
single exception is an email address typed in-thread: that address is genuinely stranded because
nothing syncs a hand-sent thread, so add it to the Cesa group and say so.

Public comment replies are the opposite case and remain fully automatic. A comment is public, its
whole reply history is visible in `blotato_list_comments`, and there is no hidden side. That
routine (`trig_01HK4yKpqXoMKYjpiX6LQUj2`) is unaffected and correct.

### `229724` — read this before judging it

Contact `1725097938924220` sells **food trailers** and is proposing a commission arrangement with
her in Iowa. The register is personal and affectionate. On the surface it has the shape of a
romance-plus-business approach.

**It is almost certainly none of those things.** *House of Trailers* is one of her real website
clients, named in her own `wix-site-builder` skill. This is a live business relationship with a
client, in a warm register, about money.

Calling that a scam would have been a fabrication about her life dressed up as a security finding
— the exact failure her hard rule exists to prevent: **NEVER GUESS, ALWAYS CHECK SOURCE.** Two
sources disagreed and the repo held the answer. Never characterise a person in her inbox without
checking whether they already appear in her own files.

### The general lesson, third time in two days

| Read | Mistake |
|---|---|
| Partial Blotato queue | claimed "zero collisions" |
| Analytics not yet fetched | claimed no breakout post |
| DM list missing her outgoing | claimed nobody reads her inbox |

Every one is the same error: **treating the absence of a record as the absence of the thing.**
Before reporting that something has not happened, establish that the source would show it if it
had.

## 0g. TWO ROUTINES, NOT THREE. Comment replies and the lead sweep merged 2026-09-09.

Amanda's call. Three routines were polling the same comment list on overlapping schedules — funnel
watch every 2h, comment replies every 3h, lead sweep every 6h — against a real arrival rate of
about **one audience comment every 2.5 days**. Nearly every pass found nothing, and each one still
produced a report in her terminal.

`trig_012kjdGhjy2pJoLjMn6h5x2G` (lead sweep) is **DELETED**. Do not recreate it.

| Routine | Trigger | Cadence | What it does |
|---|---|---|---|
| Comments | `trig_01HK4yKpqXoMKYjpiX6LQUj2` | every 3h at :50 | Replies publicly to everyone AND sends the guide to anyone who qualified. Acts without asking. |
| Funnel watch | `trig_01ErT42pMQ87cEbk1Y3NXppt` | every 2h at :18 | Runs, gates, DM inbox. **Reports only, never writes.** |

### Why merging was right, not just cheaper

Both old routines read the same `blotato_list_comments` page and both had to decide the same thing
about the same comment: does this person get a reply, and do they get the guide. Splitting that
across two prompts on different clocks meant the answers could disagree, and it meant the lead
sweep might reply to a comment the reply routine had already handled three hours earlier, or leave
one for a routine that would not run for another three.

One pass over one list, one decision per comment, one report.

### The split that DOES matter, and must not be collapsed

The remaining boundary is **write vs read**, not comments vs leads:

- **Comments are public.** The whole reply history is visible in `blotato_list_comments`, there is
  no hidden side, so acting automatically is safe. That routine writes.
- **DMs are her correspondence.** Blotato does not record the replies she sends from the Instagram
  app, so you cannot tell whether a thread has been answered (see `0f`). That routine only reads.

The one exception is a `commentId`-scoped private reply to someone who has just commented. That is
funnel machinery, not correspondence, and it lives in the comments routine where it belongs.

### Cadence reasoning, in case it comes up again

3 hours is chosen for staleness, not for volume. At one comment every 2.5 days almost any cadence
covers the load; what 3 hours buys is that nobody waits half a day for an answer. The funnel watch
stays at 2 hours because a reappearing gate is silent and costs leads for as long as it stands.

## 0-MEASURE. "I CANNOT MEASURE THAT" IS ALMOST ALWAYS FALSE. 2026-09-11. PERMANENT.

Amanda, after I reported Are You Afraid of the Dark as unmeasurable:

> "you're supposed to be able to go find this shit. If I ask you for something, you're
> supposed to find any means necessary."

She was right and the number was sitting one URL away. AYAOTD had **2,115 plays, 75
likes, 23 comments, 10 saves** — the best-responding post on the account — while I was
calling it unavailable.

**The rule: a missing number is a claim, and claims get verified before they get
reported.** Before saying any metric cannot be obtained, exhaust in this order:

1. The platform's own public page HTML. Server-rendered state blobs
   (`__UNIVERSAL_DATA_FOR_REHYDRATION__`, `ytInitialData`) carry exact counts.
2. A different URL shape for the same object. TikTok photo posts are bare at
   `/photo/<id>` and complete at `/video/<id>`. Same id.
3. The account-level page, when per-post fails.
4. Only then say it is unavailable — and say exactly what was tried.

**Never present a third-party dashboard's silence as the platform's number.** Metricool
reports 1–4 views/day on YouTube; the channel itself reports 51,824 lifetime views and
Shorts up to 1,286. Metricool receives 4 of her videos with null metrics and cannot see
the main TikTok at all. A tool that cannot see the account is not evidence about the
account. When a dashboard and the platform disagree, the platform wins and the dashboard
gets named as broken.

**Never blame the environment before checking it.** `ERR_CONNECTION_RESET` from headless
Chromium was the session relay dropping its parallel startup connections, not TikTok
blocking. `curl -sS "$HTTPS_PROXY/__agentproxy/status"` names the real failure. One
sequential curl succeeded 76 times out of 76 where the browser failed every time.

Working method and re-run commands: `REACH-ANALYSIS.md`, section
"MEASURED FROM SOURCE 2026-09-11". Raw data: `promo-engine/data/`.
