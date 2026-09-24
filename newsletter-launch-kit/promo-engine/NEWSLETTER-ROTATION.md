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

**Consider This: 6 finished carousel sets, 6 slides each, 36 PNGs** in `carousels/`.

| Set | Hook | Issue it promotes |
|---|---|---|
| `carousel-towels-01` to `-06` | Your towels aren't old, they're coated | sent |
| `carousel-sponge-01` to `-06` | Your sponge isn't sanitized after microwaving | sent |
| `carousel-duct-01` to `-06` | Your lint screen is clean, the duct behind it isn't | sent |
| `carousel-gasket-01` to `-06` | The seal nobody wipes | sent |
| `carousel-filter-01` to `-06` | Your highest-rated furnace filter may be wrong for your house | sent |
| `carousel-pillow-01` to `-06` | Your pillow has an expiration date | 10/08 |

**Just Another Tuesday: 0 carousel sets.** It has `promo-tuesday.png`, `promo-tuesday-1x.png`
and `JAT_promo_visual_pairings.jpg`, all single images, all retired by rule 2. **JAT cannot
enter the rotation until 6 carousel sets are built for it.** The copy to build them from is
already written and approved in `../DRAFT_0909_jat-send-day-promo-posts.txt` and
`../DRAFT_0909_just-another-tuesday-issues-6-10-v1.txt`.

So today the rotation is Consider This only, on a 6 set cycle. It becomes a 12 set cycle,
alternating CT and JAT, the day the JAT sets exist.

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

**Recommendation: B now, A for the sets that earn it.** B gets the rotation running this week.
A is worth the 6 renders once she sees which hooks pull.

### 2. The queue is at 184 of 200

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
