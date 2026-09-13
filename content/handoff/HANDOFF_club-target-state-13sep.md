# CLUB TARGET STATE HANDOFF, 13 Sep 2026

For a session that already has Amanda's rules loaded. This is state and findings,
not a rulebook. Where a rule matters it points at the canon file instead of
restating it.

---

You are picking up Club Target for Amanda Kersh, The Gentle Muse. Handle
`amanda.20`, storefront `club.target.com/a/amanda.20`.

Read these three first. They are short and two of them were written today.

- `content/canon/disclosure-rule.md` **new today, most important**
- `content/canon/pricing-rule.md`
- `content/club-target-claim-ledger.md` **new today**

Source document, saved because it had never been readable before:
`content/reference/club-target-scope-of-work.txt`

Everything below is the state you are inheriting.

## THE HEADLINE FINDING, 13 Sep

**Her board reads 0% on every challenge and the likely cause is now known.**

`obs.duel.me` started resolving after Amanda opened the network policy. That let
me pull Target's official Scope of Work PDF, linked in every Monday email from
`target@duel.technology` and never readable before today.

It requires, quoting:
- On Stories and videos, place the disclosure **on screen and near the link or
  product**
- The disclosure must appear **early in the video** or Story frame
- For multi-frame Stories or longer videos, **repeat the disclosure**
- **What doesn't count:** disclosure hidden at the end

I pulled three published Club Target TikToks off the Blotato CDN and sampled
frames across their full duration:

| Post | Date | Theme | On-screen `#TargetPartner` |
| --- | --- | --- | --- |
| `6966604` | 12 Sep | Wellness Reset | **final frame only** |
| `6919291` | 10 Sep | Fall Collage | **final frame only** |
| `6933972` | 11 Sep | Everyday Favorites | **none anywhere** |

Meanwhile **all 42** Club Target captions carry `#TargetPartner` inside the first
2 lines. Zero caption failures.

Correct captions plus zero credit plus a video rule she is failing is a coherent
story. Treat the on-screen disclosure as the working explanation.

**So: every Club Target video from now on opens with `#TargetPartner` burned into
the first frames, near the product, repeated around the midpoint on anything over
roughly 15 seconds.** End card as well is fine. End card alone is a fail.

It is not proven, only strongly indicated. The remaining alternative is a submit
or link-your-post step in the portal she has not done. Ask her to open one
challenge card and look. Two minutes and it settles it.

### How to check a video yourself

There is no ffmpeg or poppler in this container and `apt-get` fails. Working
route:

    pip install imageio-ffmpeg
    FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
    curl -sS -o v.mp4 "<mediaUrls entry>"
    "$FF" -v error -ss 0.3 -i v.mp4 -frames:v 1 -vf scale=400:-1 f.png -y

Then read `f.png`. Tile several with `-vf "tile=4x2"` for a contact sheet.

PDF text extraction also works, but only after `pip install --force-reinstall
cffi cryptography`, because the Debian `cryptography` is broken and takes pypdf
and pdfminer down with it. The Read tool cannot do PDFs here, it needs poppler.

## WHERE THE QUEUE ACTUALLY STANDS

**Zero Club Target posts are scheduled anywhere through 4 Oct.** Last one
published 12 Sep 00:00 UTC.

**The general queue is fine.** Full through 20 Sep, then it thins. That is not a
fault: Wave 1 (`content/wave1-staging-library.txt`, 196 rows covering 21 Sep to
29 Oct) has not loaded yet because the daily top-up routine holds a rolling
window under Blotato's 200-post cap. Leave it alone.

## WHY THE TARGET QUEUE COULD NOT BE REFILLED TODAY

Two independent reasons. Both are real, neither is a tooling failure.

**1. The library is tapped.** 26 Target-tagged assets exist
(`content/inventory/target-footage-inventory-12sep.md`). 21 are already on TikTok.
Of the 5 that are not, 4 belong to themes already banked on TikTok, so re-posting
them earns nothing. **Exactly one asset is genuinely reusable:** `f2c482e8`,
Molly's Suds, published to Instagram only on 5 Sep, never on TikTok.

There is no unqueued Target media in the repo either. Wave 1 and Wave 2 carry no
Target rows; four were removed on 11 Sep because they were regenerating posts that
had been deleted.

**2. The hashtags for the open challenges are unknown.** This is the hard blocker.

12 challenge links have arrived in the last 3 weeks. The weekly email carries
**links only**. The challenge names and hashtags are baked into tile images on
`d3k81ch9hvuctc.cloudfront.net`, which still 403s. Verified again today by reading
the 7 Sep email in plain text: nothing but URLs.

Every hashtag that IS confirmed belongs to a theme already banked on TikTok. So
there is nothing to post against. A post carrying the wrong theme tag scores 0,
which is worse than not posting.

**What unblocks it.** Amanda taps a challenge link and screenshots the name and
hashtag. The three newest, from 7 Sep:

    https://club.target.com/t/0pdf
    https://club.target.com/t/0pdm
    https://club.target.com/t/0pdq

Older, may still be open: `0p19` `0p1f` `0p1c` `txd` (31 Aug),
`0n9n` `0n97` `0nas` `0n9f` (24 Aug), `0kvn` `0kyp` `0kyt` `0kyz` (17 Aug).

Do not try to fetch these. `club.target.com` returns an identical empty shell to
any non-browser client. Verified five ways on 31 Aug and again today. Do not
re-test, it wastes her time and yours.

## THE BOARD, deadlines from 13 Sep

| Theme | Expires | Days | TikTok row | Status |
| --- | --- | --- | --- | --- |
| Quick & Easy Meals | 16 Sep | 3 | yes | published 8 Sep |
| Fall Style Collage | 16 Sep | 3 | yes | published 10 Sep |
| Make It Yours with Heyday | 16 Sep | 3 | **none** | IG only, 0 points |
| Fresh Activewear | 16 Sep | 3 | **none** | IG only, published 6 Sep |
| Find Your Denim | 23 Sep | 10 | yes | **open**, footage shot 12 Sep |
| Fall Home Refresh | 23 Sep | 10 | yes | published 9 Sep |
| Everyday Target Favorites | 23 Sep | 10 | yes | published 11 Sep |
| Your Everyday Wellness Reset | 30 Sep | 17 | yes | published 12 Sep |
| New Ways to Play | 30 Sep | 17 | yes | **open**, footage shot 12 Sep |
| Game Day Line Up | 7 Oct | 24 | yes | **open**, footage shot 12 Sep, apparel only |

**The 16 Sep deadline is not an emergency.** Both themes that carry a TikTok row
are already published. The other two are Instagram only.

**Instagram earns her no Club Target credit until she passes 500 followers.** That
gate decides priority everywhere. Keep posting to IG to grow the account, never
count it as points, never let an IG cut delay a TikTok cut.

Repeatable, no deadline: Share a Target Find (IG Story 30, IG Reel 30, TikTok 30),
Post your Target Haul (IG Story 15), Budget-friendly finds (IG Reel 30), Add to
your Target Highlight 10, Make a Highlight 10, Like and comment on a Target post 5,
Share your storefront link 15. **Hashtags for these are also unknown.**

## DEFECTS OPEN

- Facebook `688849`, 1 Sep, #TargetCatandJackSummer: **failed**, never went live.
  "Could not upload video to Facebook: the video could not be processed."
- `6776722` (IG, 5 Sep) and `6837551` (TikTok, 7 Sep) carry `#ClubTarget` and
  `#TargetPartner` but **no challenge theme hashtag**. Nothing to claim them
  against. Published, so only Amanda can edit them.
- **`2277` IG FALLFIT** points at the bare storefront. Universal Thread Open Stitch
  Cozy Cardigan, SKU `94430282` is dead. Amanda photographed shelf tags on 12 Sep;
  if the Universal Thread piece is among them, fix with
  `blotato_update_automation`.
- **`453` FB MASK** same failure, broken since 8 Aug. Needs the medicube Kojic Acid
  Turmeric Jelly Gel Mask tag, which she did not get.
- `scripts/validate-wave.py` still carries a blanket no-prices check that predates
  the 13 Sep pricing correction. It is over-broad. If it fails only on a price in a
  Club Target row, that is a false alarm.

## THE OTHER-BRANDS CLAUSE, unresolved and worth a look

The Scope of Work also says a post "cannot include references to products/services
from any other brands."

Read plainly that would forbid naming NYX, FlavCity, Dr Teals, Tree Hut and
Molly's Suds, all of which she has named in Club Target posts and all of which
Target sells. The sensible reading is that it means competitors and other
retailers, not vendors stocked by Target, since most challenges are impossible
otherwise.

**Do not act on this either way.** Ambiguous, and guessing wrong is expensive. She
has a live thread with `clubtarget@target.com` that has already answered two policy
questions. Ask there.

## A STYLE CHANGE YOU NEED TO KNOW ABOUT

Her published Club Target videos are **talking head**: she is on camera, speaking,
holding products. That is the existing body of work.

**Going forward she is not on camera and may not record voiceover.** She confirmed
this on 12 Sep. The new footage is silent b-roll: shelf, rack, endcap, item picked
up and turned. No face, no fitting room, no try-on.

That changes the hook. With no face and no voice, the first 2 seconds are carried
by the on-screen text line and the strongest frame. Lead with the frame. And note
this now doubles up nicely with the disclosure fix, since the opening frames need
`#TargetPartner` on them anyway.

Never generate a synthetic voice.

## AUTOMATION IN PLACE

- `trig_01LikHf7zVVJZAxZMe5mLNsj` **Club Target claim watch**, daily 16:00 UTC,
  fires into session `session_01XtExtQnr44bCFsA7WAyvut`. Sweeps the last 36 hours
  for published Club Target posts, appends them to the claim ledger, hands Amanda
  one line per claim. Knows the disclosure rule.
- `trig_01CHbGjy41Va6Pw7LVCSGC83` Club Target audit, Sun and Wed 00:00 UTC.
- `trig_018yBeoQES7zGTiZJnztqJJp` Monday challenge drop from Gmail, 13:40 UTC.
- `trig_01CiLyBpQXyJfk242UsTec7g` Blotato queue top-up, daily 06:00 UTC.

**Nobody can claim points for her.** `club.target.com` is a login-gated JavaScript
app. The routines detect and hand off. She presses the button.

## OPERATIONAL GOTCHAS

- `blotato_list_posts` returns **no `accountId`**, only `platform`. Her two
  Instagram accounts get summed into one number. Do not conclude a cap is breached
  from that count.
- `blotato_list_posts.postTime` is **not authoritative**. It has disagreed with
  `blotato_get_schedule.scheduledAt` by up to 9 days. For published rows trust
  `state.postUrl` existing. For scheduled rows confirm with
  `blotato_get_schedule`.
- Re-read the live queue immediately before writing to it. A stale snapshot caused
  a 9-post collision on 31 Aug.
- `blotato_list_posts` output usually exceeds the inline limit and gets saved to a
  file with one enormous line. Parse it with python3, do not Read it.
- Instagram Stories work: `blotato_create_post` takes `mediaType: "story"` for
  Instagram and Facebook. `firstComment` does not work on stories, so a Story
  keyword must be on-screen text or a link sticker.
- Account IDs: instagram `45886`, tiktok `41488`, facebook `30840`
  (pageId `1086399221215093`). Cesa's are instagram `65540`, tiktok `55761`,
  **no Target content there**.
- Slots UTC: instagram 15:00 and 23:00, tiktok 15:00, facebook 17:10 and 22:00.
  Central is UTC-5 until 1 Nov.

## WHAT TO DO, IN ORDER

1. **Ask Amanda for the challenge hashtags.** Nothing new can be queued without
   them. Give her the three 7 Sep links and ask for a screenshot of the name and
   tag. This is the single blocking item.
2. **Ask her to check one challenge card for a submit action.** Settles whether the
   disclosure fix is the whole story.
3. Once you have a hashtag for an open theme, queue `f2c482e8` (Molly's Suds) to
   TikTok if it fits. It is the only genuinely fresh Target asset left.
4. Cut the 12 Sep footage when the laptop session hands it over. Priority: Denim,
   then New Ways to Play, then Game Day. See
   `content/handoff/HANDOFF_trackB-phone-ingest.md`.
5. Every new video: `#TargetPartner` on screen in the opening frames.

Commit to branch `claude/club-target-game-plan-9xs2du`.
End commit messages with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
