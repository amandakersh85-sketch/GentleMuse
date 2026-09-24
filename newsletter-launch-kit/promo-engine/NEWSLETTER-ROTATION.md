# The newsletter carousel rotation

**Set by Amanda 2026-09-24, by voice, and it supersedes the send-day-only version of this rule.**

Her words: *"make sure we're getting at least one newsletter thing pushed out every other day or
so"*, *"I want to cut any one page, we only want the carousels"*, *"we're cycling through on a
recycle of all of the just another Tuesday and consider this, those are the two most important
things, getting people to sign up for the newsletters, just keep rotating them"*, and *"make
sure we have music to the carousels."*

## The rule in 4 lines

1. **A newsletter promo goes out at least every other day.** Not only on send days. That was
   the old rule and it was too thin.
2. **Carousels only.** Single-image newsletter promos are retired. Do not schedule another one.
3. **Recycle what exists.** The assets are already built and already approved. The job is
   rotation, not generation. Nothing new gets rendered to fill a slot a finished carousel can
   fill.
4. **Carousels carry music.** See the blocker below, which is real and is not solved yet.

This sits alongside her other lanes and does not compete with them: seasonal runs every
evening, 1 post of her own every day, the club targets keep their slots. The newsletter
rotation is the 4th lane and it is the one that was missing.

## What exists to rotate, counted 2026-09-24

**Consider This: 6 finished carousel sets, 6 slides each** in `carousels/`.

| Set | Hook |
|---|---|
| `carousel-towels-*` | Your towels aren't old, they're coated |
| `carousel-sponge-*` | Microwaving your sponge isn't sanitizing it |
| `carousel-duct-*` | Your lint screen is clean, the duct behind it isn't |
| `carousel-gasket-*` | The part of your washer that never gets clean |
| `carousel-filter-*` | The highest-rated filter might be the wrong one |
| `carousel-pillow-*` | Your pillow has an expiration date |

**Just Another Tuesday: 6 finished carousel sets, built 2026-09-24** by
`../promo-engine/gen_jat_carousels.py`, to Amanda's instruction that JAT had to be as good
as the Consider This sets. Same 6 slide structure, same type system, same 1080x1350. The one
deliberate difference is palette: Consider This runs WARM, JAT runs COOL, which is the split
the retired single-page promos already used.

| Set | Hook | Source |
|---|---|---|
| `carousel-jat-enabled-*` | 6 automations had stopped, all 6 still said enabled | promo-tuesday copy |
| `carousel-jat-number-*` | I found my number 1 problem, then ignored it 3 weeks | JAT #006 |
| `carousel-jat-doors-*` | I had 4 front doors, they were all the same door | JAT #007 |
| `carousel-jat-obedient-*` | The algorithm was not broken, it was obedient | JAT #008 |
| `carousel-jat-923-*` | I chased down $9.23, it found the real problem | JAT #009 |
| `carousel-jat-permission-*` | My first robot asked permission before it moved | JAT #010 |

Every beat traces to approved copy in `../DRAFT_0909_just-another-tuesday-issues-6-10-v1.txt`
or the promo page it replaces. Nothing invented.

**The single-image promos are retired.** `promo-tuesday.png`, `promo-tuesday-1x.png` and
`JAT_promo_visual_pairings.jpg` stay in the repo as history. Do not schedule them.

## Live in the queue as of 2026-09-24

Amanda picked option B: **TikTok carries the music via `autoAddMusic`, Instagram runs silent.**
8 posts scheduled, 4 drops, alternating the 2 newsletters.

| Date | Set | Instagram 13:00 UTC | TikTok 17:00 UTC |
|---|---|---|---|
| 09/26 | jat-enabled | silent carousel, TUESDAY CTA | autoAddMusic on |
| 09/28 | towels | silent carousel, CONSIDER CTA | autoAddMusic on |
| 09/30 | jat-number | silent carousel, TUESDAY CTA | autoAddMusic on |
| 10/02 | sponge | silent carousel, CONSIDER CTA | autoAddMusic on |

**Times were chosen against the ladder, not on top of it.** 13:00 UTC is 8:00 AM Central, a
clear 2 hours before the 15:00 seasonal slot, so Instagram's 10:00 AM Central primary stays
reserved. 17:00 UTC is TikTok's stated second slot, 12:00 PM Central, and is 2 hours clear of
everything already on that account. Nothing was moved and nothing was displaced.

**Queue went from 184 to 192 of the 200 cap. 8 slots left on purpose.** The rest of the
rotation loads on refill as October publishes and frees room. November is wide open.

**Note on media URLs.** Blotato mints a fresh storage URL every time media is attached, so the
URLs on these 8 posts do not match each other or the upload response. That is expected and is
already recorded in `AGENT-CONTRACT.md` under the render ratio rule. URL count is not file
count. The 12 slides behind these 8 posts are 12 files, not 48.

## The cycle

Rotate in the order above, oldest hook first, then start over. A set may repeat every 12 days
on the CT-only cycle and every 24 once JAT joins. Repeats are the point: 4 real subscribers
have ever converted and none of them saw a hook twice.

Do not retire a set because it has run before. Retire it only when the fact in it stops being
true.

## 2 blockers Amanda needs to decide on. Neither is fixable from here.

### 1. Instagram carousels cannot be given music through the API

Checked against the Blotato `create_post` schema on 2026-09-24, not assumed:

- Instagram accepts `audioName`, and it is **reels only**. It labels audio that is already
  inside the video file. It does not attach a track to an image carousel.
- **TikTok accepts `autoAddMusic`**, and TikTok photo carousels do take music that way.
- Facebook, LinkedIn and Pinterest have no audio field at all.

Music on an Instagram image carousel is added in the Instagram app at post time. There is no
API path to it, so no scheduling tool can do it, including this one.

**3 ways forward, her pick:**

- **A. Render the carousels as video.** Burn the slides into a 6 to 8 second slideshow with the
  music baked into the file, post as a Reel. This is the only option that puts music on
  Instagram and it costs a render per set, 6 renders total, which is within the 1-render-per-
  fact rule because it replaces the still set rather than adding to it.
- **B. TikTok carries the music, Instagram runs silent.** Post the same slides as a TikTok
  photo carousel with `autoAddMusic` on, and as a silent IG carousel. Costs nothing, ships
  tonight, and Instagram is the channel that actually converts.
- **C. Amanda posts the IG carousels by hand** and picks the audio herself. Best sound, worst
  use of her time, and it breaks the point of the queue.

**RESOLVED 2026-09-24. Amanda chose B, and it is live.** TikTok carries the music, Instagram
runs silent. A stays on the table for whichever sets earn it once she sees which hooks pull.

### 2. The queue is at 192 of 200 (was 184 before this rotation loaded)

37 days scheduled, 09/24 through 10/31, and the plan cap is 200. **16 slots free right now.**
An every-other-day rotation from 09/26 to 11/26 needs about 31 posts, so it cannot all be
loaded at once.

It works as a rolling refill instead: load 16 now, and top up as October publishes and frees
room. November is wide open, the current queue ends 10/31, so the second half loads itself
with no pressure.

## Standing limits this rule does not touch

- `claude/holiday-caption-strategy-m5abq8` is lead on the posting project. It schedules.
- The ladder in `../SCHEDULING-LADDER.md`. Instagram @thegentlemuse2026 owns 10:00 AM Central
  and a newsletter carousel does not jump that queue. 2 hours minimum between posts on the same
  account.
- LinkedIn gets business posts only, never seasonal.
- X stays off.
- 1 render per fact. The rotation reuses `mediaUrls`, it does not re-upload per post.
- Verified links only: `https://consider-this.subscribepage.io` and
  `https://just-another-tuesday-gm.subscribepage.io`.

---

# The LinkedIn lane

**Set by Amanda 2026-09-24, by voice, same session.** Her words: make sure we are blowing
LinkedIn up with Just Another Tuesday and the AI Guide, those are the huge thing, smack the
hell out of LinkedIn with it.

**This does not conflict with the LinkedIn rule, it is the LinkedIn rule.** `AGENT-CONTRACT.md`
says LinkedIn gets what she learned building the business, AI in plain language, systems and
automation failures with the mistake left in, and the free lead magnets. Just Another Tuesday
and the AI Guide are all 4 of those things. Seasonal stays carved out, as always.

## What LinkedIn looked like before this, counted 2026-09-24

**8 scheduled posts across 26 days, 09/25 through 10/20.** For the account she calls her huge
thing, Just Another Tuesday had exactly 1 post on it and the AI Guide had none.

## 2 defects found in the existing LinkedIn queue. NOT fixed, because they are not mine to rewrite.

1. **Posts `4716080` (10/15) and `4716102` (10/20) carry the wrong link.** The copy is the
   Consider This towels piece, the CTA says comment CONSIDER, and the link at the bottom is
   `https://ai-guide.subscribepage.io`. Towels copy pointing at the AI Guide page. Both are
   duplicates of each other, 5 days apart.
2. **Those same 2 posts use a comment-to-DM CTA on a platform that has no comment-to-DM
   automation.** Blotato runs keywords on Instagram and Facebook only. On LinkedIn, "comment
   CONSIDER and I'll send it" promises something nothing is listening for. LinkedIn posts have
   to carry the link itself.

Also worth a look: `4726815` (10/16) links to `https://thegentlemuse.subscribepage.io`, which
is not on the verified link table in `AGENT-CONTRACT.md`. It may be fine, it is just unverified.

## AI Guide carousels, built 2026-09-24

The AI Guide had no carousel either, only the retired single-page `promo-ai-guide.png`, so it
could not be posted under the carousels-only rule. 4 sets built by `gen_aiguide_carousels.py`,
same structure and type system as Consider This and JAT, COOL palette, which is what the
retired AI Guide single-pager already used.

| Set | Hook |
|---|---|
| `carousel-guide-needed-*` | I wrote the AI guide I needed 60 days ago |
| `carousel-guide-hours-*` | You do not need to be 10 years ahead on AI |
| `carousel-guide-behind-*` | Most AI advice starts 3 steps past you |
| `carousel-guide-explorer-*` | I stopped calling myself an AI expert |

The CTA slide carries no keyword on purpose, because LinkedIn has no automation. The caption
carries the link there, and the keyword CTA gets added in the caption on IG and FB.

## Live on LinkedIn as of 2026-09-24

4 posts, alternating the 2 offers, 13:30 UTC to match the existing LinkedIn pattern:

| Date | Set | Offer |
|---|---|---|
| 09/29 | jat-enabled | Just Another Tuesday |
| 10/01 | guide-needed | AI Guide |
| 10/03 | jat-number | Just Another Tuesday |
| 10/05 | guide-hours | AI Guide |

Long-form business register, link in the post, no keyword CTA, no hashtags, matching what
already performs on that account.

## THE CAP IS NOW THE BINDING CONSTRAINT. This is the thing to fix.

**The queue is at 200 of 200 and Blotato is refusing new posts.** Confirmed, not predicted:
2 further LinkedIn posts were rejected with

> `You have reached the maximum number of scheduled posts (200) for your plan.` code `20010`

The 2 that did not land are 10/07 `jat-doors` and 10/09 `guide-behind`. Both sets are built
and already uploaded, so they are a 2 minute job the moment there is room.

**3 ways to get room, all Amanda's call:**

- **Prune.** There are cheap posts in the queue that could go. The `Full reel on my page.`
  Instagram one-liners are the obvious candidates. Nobody should delete another session's
  scheduled posts without her say-so, which is why this is written down instead of done.
- **Let it drain.** October publishes several posts a day, so room appears daily on its own.
  The rotation then refills as slots open, which is what the standing rule already says.
- **Upgrade the plan.** The cap is a plan limit, not a platform limit.

Until then, **every new post is a trade against an existing one.** Anyone filling slots should
say what they are displacing.
