# LOCAL SESSION HANDOFF: ingest the Target run and collect every open point

Paste this into a Claude Code session on Amanda's laptop, after she connects her
phone. It is written for a session with no prior context.

---

You are working for Amanda Kersh, The Gentle Muse. She is a Club Target creator,
handle `amanda.20`, storefront `club.target.com/a/amanda.20`. Club Target pays
POINTS per challenge, every challenge has a hard expiry, and each theme is the same
footage cut 3 ways: IG Story, IG Reel or Post, and TikTok.

She just got back from a Target run on 12 Sep 2026 and connected her phone. Your job
is to ingest that new footage, combine it with the assets she already has, and
convert all of it into posted content before the deadlines.

## STEP 1. Ingest the phone

Find and copy the new footage. Do not ask her for a path, go find it.

- macOS: `~/Pictures/Photos Library.photoslibrary`, Image Capture staging, `~/Downloads`, `/Volumes/*`
- Windows: `This PC\<phone>\Internal storage\DCIM\Camera`, `~/Downloads`, `~/Videos`
- Also check any Photos or iCloud sync folder, and AirDrop and Downloads

Filter to files created 12 Sep 2026 or later. Copy them into a working folder in the
repo, do not move or delete anything off the phone.

Build an inventory: filename, path, duration, created timestamp, and your best guess
at the product or aisle. For video you cannot identify from the filename, sample a
frame with ffmpeg and look at it.

## STEP 2. Merge with the assets she already has

Her existing library is NOT on the laptop. It lives on the Blotato CDN, referenced by
every post she has made. A full inventory was built on 12 Sep and committed to:

    content/inventory/target-footage-inventory-12sep.md

That file lists 659 unique assets, 337 of them video, and the 26 that carry a Club
Target tag, each with a date and what it shows. Read it before you plan anything.
Do not re-derive it, and do not go looking for these files on disk. They are not
there.

To pull the live list yourself: `blotato_list_posts` across published and scheduled,
then collect `mediaUrls`. Prefix for any bare filename is
`https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/`

## STEP 3. The board, with real deadlines

Read from her portal 12 Sep. Days remaining are from 12 Sep.

**4 days left, expires 16 Sep**
| Theme | IG Story | IG Reel/Post | TikTok |
| --- | --- | --- | --- |
| Quick & Easy Meals | 15 | 30 | 30 |
| Fall Style Collage | 15 | 30 | 30 |
| Make It Yours with Heyday | 15 | 30 | none on board |
| Fresh Activewear | 15 | 30 | none on board |

**11 days, expires 23 Sep**
| Theme | IG Story | IG Reel/Post | TikTok |
| --- | --- | --- | --- |
| Find Your Denim | 15 | 30 | 30 |
| Fall Home Refresh | 15 | 30 | 30 |
| Everyday Target Favorites | 15 | 30 | 30 |

**18 days, expires 30 Sep**: Your Everyday Wellness Reset and New Ways to Play,
15 / 30 / 30 each.

**25 days, expires 7 Oct**: Game Day Line Up, 15 / 30 / 30.

**Repeatable, no deadline**: Share a Target Find (IG Story 30, IG Reel 30, TikTok 30),
Post your Target Haul (IG Story 15), Budget-friendly finds (IG Reel 30), Add to your
Target Highlight (10), Make a Highlight (10), Like and comment on a Target post (5),
Share your storefront link (15).

## STEP 4. What was still missing before the run

Six themes were already covered by footage shot 6 to 12 Sep. Four were empty:

| Needed filming | Also grab |
| --- | --- |
| Find Your Denim | the Universal Thread SKU off the shelf tag |
| Make It Yours with Heyday | August footage does not count, needs current |
| Game Day Line Up | nothing existed |
| New Ways to Play | toy and game aisles, nothing existed |

Check the new phone footage against these four first. Anything she did not get is
the only thing that still needs a store trip.

## STEP 5. Two broken automations, both need a SKU

Both currently dump people on the bare storefront instead of a product page.

- **`2277` IG FALLFIT.** Universal Thread Open Stitch Cozy Cardigan. Old SKU
  `94430282` is dead. If she photographed a shelf tag in the denim or apparel
  section, read the SKU off it and fix the button with `blotato_update_automation`.
- **`453` FB MASK.** medicube Kojic Acid Turmeric Jelly Gel Mask. Broken since
  8 Aug, nobody had noticed. Same fix.

## HOW SHE FILMS. This is fixed, do not plan around anything else.

Amanda confirmed 12 Sep:

- **She is not on camera. Ever.** No face, no body, no fitting room, no try-on, no
  hands-in-frame talking piece. Do not write a shot, a script beat, or a caption
  that implies she appeared in the video.
- **Product and aisle footage only.** Shelf, rack, endcap, the item picked up and
  turned, the item in the cart. That is the whole vocabulary.
- **She may not record a voiceover.** Build every edit so it works silent, with the
  story carried by on-screen text and the caption. If she does hand you a voice
  memo, drop it into the Remotion render natively and treat it as a bonus, not a
  dependency. Never generate a synthetic voice.
- **Denim specifically: no fitting room.** The challenge asks her to show the Target
  denim, not to model it. Rack pan, folded stack, one pair held up to the light,
  close on the wash and the stitching. That satisfies it.

This constrains the hook. With no face and possibly no voice, the first 2 seconds
have to be carried by the on-screen text line and the strongest frame in the clip.
Lead with the frame, not a talking setup.

## WHEN THE FOOTAGE ARRIVES

She said she may upload tonight or tomorrow. Do not assume same-day. If the phone
has nothing dated 12 Sep or later, say so in one line and stop, do not go hunting
through older footage or start producing from the existing library to fill the gap.

## STEP 6. Produce and queue

Use the Remotion pipeline already in the repo. If she supplies a voice memo, drop it
into the Remotion render natively, frame by frame. Do not build a separate voiceover
step and never spend credits on synthetic voice. Assume silent-with-text as the
default and treat her voice as optional.

**Instagram Stories ARE supported by Blotato.** Verified 12 Sep:
`blotato_create_post` takes `mediaType: "story"` for Instagram and Facebook. Queue
Stories like any other post. One catch: `firstComment` does not work on stories, so
a Story keyword has to be on-screen text or a link sticker, not a comment.

Account IDs: instagram `45886` @thegentlemuse2026, tiktok `41488`, facebook `30840`
with pageId `1086399221215093`. Cesa's separate accounts are instagram `65540` and
tiktok `55761`, do not put Target content there.

Slots, UTC: instagram 15:00 and 23:00, tiktok 15:00, facebook 17:10 and 22:00.
Central is UTC-5 until 1 Nov. Challenge posts go ON TOP of her running queue, not
instead of it. 5 to 7 Instagram posts a day is fine, volume is not a concern, reach
is. The only hard limit is no duplicates.

## HARD RULES. Violating any one of these kills the points.

1. **`#TargetPartner` at the START of the caption**, plus **`#ClubTarget`**. Amanda
   confirmed 12 Sep that these two are the required tags on every single challenge.
   No post counts without both.
2. **NO PRICES.** Not in the caption, not on screen, not in voiceover, not on a shelf
   tag visible in frame. If a price is visible in a frame, cut the frame. She took a
   TikTok Shop penalty on 4 Aug 2026 for a price mismatch, and on 7 Sep four posts
   had to be rewritten under deadline for the same reason.
3. Disclosure line, verbatim: "I'm a Target partner, so I may earn rewards or
   commission when you shop my link, at no extra cost to you."
4. Every Instagram and Facebook post names a LIVE keyword. Never ship a post pointing
   at nothing. Check with `blotato_list_automations` first.
5. No duplicates. Do not re-queue an asset already scheduled to the same platform.
6. Voice: warm, grounded, practical. No hype. No em dashes. Digits not spelled-out
   numbers. Contractions always. Product copy reads as lived experience, not ad copy.
   Max 5 hashtags on Instagram, none on Facebook.
7. Platform lanes: Instagram and Facebook share a lane, TikTok is separate because
   TikTok Shop is a separate business. Do not blanket cross-post.
8. Nothing publishes without Amanda's approval.

## OPEN QUESTION, worth resolving early

Every challenge on her board reads **0%**, including ones she has already published
for: Quick & Easy Meals posted 8 Sep, Fall Home Refresh 9 Sep, Fresh Activewear
6 Sep. Her captions DO carry both required tags, so this is not a tagging error.
It is either a lag in Target's review, or there is a submission step in the portal
she has not done. Have her check one challenge card in the portal for a submit or
link-your-post action before you produce another 20 posts on top of it.

## WHAT TO HAND BACK

1. The new footage inventory, merged with the existing one.
2. Which of the 4 gap themes are now covered and which still are not.
3. Whether the FALLFIT and MASK SKUs were recoverable from her photos.
4. What you queued, where, and at what times.
5. The shortest possible list of anything only she can still do.

Commit everything to branch `claude/club-target-game-plan-9xs2du`.
End commit messages with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
