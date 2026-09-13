# LOCAL SESSION HANDOFF: refill the Target queue, then ingest and cut the new footage

Paste everything below the line into a Claude Code session on Amanda's laptop.
Written for a session with zero prior context. Supersedes
`HANDOFF_local-target-ingest.md`, which carries an incorrect pricing rule.

---

You work for Amanda Kersh, The Gentle Muse. Club Target creator, handle
`amanda.20`, storefront `club.target.com/a/amanda.20`. Club Target pays POINTS
per challenge. Every challenge has a hard expiry. Each theme is the same footage
cut 3 ways: IG Story, IG Reel or Post, and TikTok.

You have two jobs and they are independent. Do TRACK A first, it needs nothing
from her. Then do TRACK B.

## THE SITUATION, as of 13 Sep 2026

**The Blotato queue has zero Club Target posts scheduled through 4 Oct.** The last
one published 12 Sep at 00:00 UTC. The queue is dry. Nothing is coming, so no
points are coming, until someone loads it.

Separately, she got back from a Target run on 12 Sep with new footage on her phone
covering the 4 themes that had nothing.

---

# TRACK A: refill the queue from the library she already has

No phone needed. Start here.

## A1. Read the inventory, do not rebuild it

    content/inventory/target-footage-inventory-12sep.md

659 unique assets, 337 video, and **26 carrying a Club Target tag**, each dated
with what it shows. Her library is NOT on the laptop. It lives on the Blotato CDN.
Do not go looking for these files on disk, they are not there.

Bare filenames resolve against:
`https://database.blotato.io/storage/v1/object/public/public_media/5472a21c-0213-4305-8693-b19295e4d67e/`

## A2. Know what is already banked before you produce anything

    content/club-target-claim-ledger.md

15 Club Target posts published 31 Aug to 12 Sep, with live URLs. Read it. The
deadline-bound themes are in better shape than the empty queue suggests:

| Theme | Expires | TikTok 30pt row | Status |
| --- | --- | --- | --- |
| Quick & Easy Meals | 16 Sep | yes | **published 8 Sep** |
| Fall Style Collage | 16 Sep | yes | **published 10 Sep** |
| Make It Yours with Heyday | 16 Sep | none on board | IG only |
| Fresh Activewear | 16 Sep | none on board | IG only, published 6 Sep |
| Fall Home Refresh | 23 Sep | yes | **published 9 Sep** |
| Everyday Target Favorites | 23 Sep | yes | **published 11 Sep** |
| Find Your Denim | 23 Sep | yes | **open**, needs Track B |
| Your Everyday Wellness Reset | 30 Sep | yes | **published 12 Sep** |
| New Ways to Play | 30 Sep | yes | **open**, needs Track B |
| Game Day Line Up | 7 Oct | yes | **open**, needs Track B |

So do not burn the evening re-producing the 16 Sep themes. TikTok is already
banked on both that carry a TikTok row.

## A3. The actual open money in the existing library

**Instagram earns Amanda no Club Target credit until she passes 500 followers.**
That is a hard gate. Any IG-only challenge is worth 0 points today. Keep posting
to IG to grow toward 500, but never count it as points and never prioritize it
over a TikTok row.

That leaves one large untapped vein, and it is repeatable with no deadline:

- **Share a Target Find**, TikTok **30**, IG Story 30, IG Reel 30
- **Budget-friendly finds**, IG Reel 30
- **Post your Target Haul**, IG Story 15
- **Add to your Target Highlight** 10, **Make a Highlight** 10
- **Like and comment on a Target post** 5, **Share your storefront link** 15

**Share a Target Find at 30 TikTok points, repeatable, is the highest yield thing
you can do tonight with footage that already exists.** She has 26 tagged assets
and many more untagged Target-adjacent ones. Each distinct product is one more
Share a Target Find TikTok.

Build a run of these from the library. Good unused or lightly used candidates from
the inventory: `ce491416` Tree Hut scrub, `9c6802ec` Good and Gather salad kits,
`f2c482e8` Molly's Suds, `99a1586f` Tillamook, `232050d5` Adornia necklace,
`aac8732a` Starbucks wall, `2c27e52c` glass pumpkins, `571b6622` heyday cases.

Check each against the live queue before you use it. **No duplicates.** Do not
re-queue an asset already scheduled to the same platform.

## A4. Three defects in the published set, fix what you can

- Facebook `688849`, 1 Sep, #TargetCatandJackSummer: **failed**, never went live.
  "The video could not be processed." Re-cut and re-queue it if the theme is still
  open, otherwise leave it.
- `6776722` (IG, 5 Sep) and `6837551` (TikTok, 7 Sep) carry `#ClubTarget` and
  `#TargetPartner` but **no challenge theme hashtag**, so there is nothing to claim
  them against. Only Amanda can edit a published caption. Put both on her list.

---

# TRACK B: ingest the phone and cut the new footage

## B1. Find the footage. Do not ask her for a path.

- macOS: `~/Pictures/Photos Library.photoslibrary`, Image Capture staging,
  `~/Downloads`, `/Volumes/*`
- Windows: `This PC\<phone>\Internal storage\DCIM\Camera`, `~/Downloads`, `~/Videos`
- Also any Photos or iCloud sync folder, AirDrop, and Downloads

Filter to files created **12 Sep 2026 or later**. Copy into a working folder in the
repo. Do not move or delete anything off the phone.

Inventory each: filename, path, duration, created timestamp, best guess at product
or aisle. For video you cannot identify from the filename, sample a frame with
ffmpeg and look at it.

**If the phone has nothing dated 12 Sep or later, say so in one line and stop.**
Do not go hunting through older footage. Do not backfill from the existing library
and call it the new run. Go finish Track A instead.

## B2. What she says she shot, 12 Sep. Verify against the files.

All 4 gap themes. Everything is b-roll, no narration, she is not in frame.

| Theme | Got it | Note |
| --- | --- | --- |
| Find Your Denim | yes | product and rack footage, no try-on |
| Make It Yours with Heyday | yes | current, replaces the 20 Aug footage |
| New Ways to Play | yes | the entire gaming wall, framed as family game night |
| Game Day Line Up | **partial** | she shot **sportswear**, not snacks |

**SKUs captured:** the dress and the sweater she bought. Both also feed Fall Style
Collage. Use one to repair automation `2277` FALLFIT if the Universal Thread piece
is among them.

**Not captured:** the medicube Kojic Acid Turmeric Jelly Gel Mask shelf tag.
Automation `453` stays broken until someone gets it.

### Game Day, unresolved read

Board copy: "What makes your game day lineup? Round up the Target finds you
actually reach for on game day." That supports either reading, food or apparel. She
shot apparel. Snacks is the more common interpretation and she offered to go back.
It expires 7 Oct, 24 days out, so there is no rush. If both exist later, cut the
snack version as primary and hold sportswear as the second attempt or as Share a
Target Find filler. If only sportswear exists, ship sportswear, it satisfies the
copy.

## B3. Priority order for cutting the new footage

1. **Find Your Denim**, TikTok. Expires 23 Sep, 10 days. 30 points, nothing exists.
2. **New Ways to Play**, TikTok. Expires 30 Sep, 17 days. 30 points, nothing exists.
3. **Game Day Line Up**, TikTok. Expires 7 Oct, 24 days. 30 points.
4. **Make It Yours with Heyday**. Expires 16 Sep, 3 days, but it is **IG only on the
   board**, so it is worth 0 points until she passes 500 followers. Cut it for reach,
   not for points, and only after 1 to 3 are queued.
5. Everything left over becomes Share a Target Find TikToks.

## B4. Two broken automations, both need a SKU

Both currently dump people on the bare storefront instead of a product page.

- **`2277` IG FALLFIT.** Universal Thread Open Stitch Cozy Cardigan. Old SKU
  `94430282` is dead. If she photographed a shelf tag in denim or apparel, read the
  SKU off it and fix the button with `blotato_update_automation`.
- **`453` FB MASK.** medicube Kojic Acid Turmeric Jelly Gel Mask. Broken since
  8 Aug. Same fix, needs the tag she did not get.

---

# HOW SHE FILMS. Fixed. Do not plan around anything else.

- **She is not on camera. Ever.** No face, no body, no fitting room, no try-on, no
  hands-in-frame talking piece. Never write a shot, a script beat, or a caption that
  implies she appeared in the video.
- **Product and aisle footage only.** Shelf, rack, endcap, the item picked up and
  turned, the item in the cart. That is the whole vocabulary.
- **She may not record a voiceover.** Build every edit to work silent, carried by
  on-screen text and the caption. If she hands you a voice memo, drop it into the
  Remotion render natively and treat it as a bonus, never a dependency. **Never
  generate a synthetic voice.**
- **Denim: no fitting room.** The challenge asks her to show Target denim, not model
  it. Rack pan, folded stack, one pair held to the light, close on wash and
  stitching. That satisfies it.

With no face and possibly no voice, the first 2 seconds are carried by the
on-screen text line and the strongest frame in the clip. Lead with the frame, not a
talking setup.

# PRODUCTION AND QUEUEING

Use the Remotion pipeline already in the repo.

**Instagram Stories ARE supported by Blotato.** Verified 12 Sep:
`blotato_create_post` takes `mediaType: "story"` for Instagram and Facebook. Queue
Stories like any other post. Catch: `firstComment` does not work on stories, so a
Story keyword must be on-screen text or a link sticker, never a comment.

Account IDs: instagram `45886` @thegentlemuse2026, tiktok `41488`, facebook `30840`
with pageId `1086399221215093`. Cesa's separate accounts are instagram `65540` and
tiktok `55761`. **Do not put Target content there.**

Slots, UTC: instagram 15:00 and 23:00, tiktok 15:00, facebook 17:10 and 22:00.
Central is UTC-5 until 1 Nov. Challenge posts go ON TOP of her running queue, not
instead of it. 5 to 7 Instagram posts a day is fine, volume is not a concern, reach
is. The only hard limit is no duplicates.

**Re-read the live queue immediately before you write to it.** A stale snapshot has
caused collisions before.

**`blotato_list_posts.postTime` is not reliable.** It has disagreed with
`blotato_get_schedule.scheduledAt` by up to 9 days. For anything already published,
trust `state.postUrl` existing over the timestamp. Before trusting a scheduled time,
confirm it with `blotato_get_schedule`.

**`blotato_list_posts` returns no `accountId`, only `platform`.** Her two Instagram
accounts get summed into one number. Do not conclude a cap is breached from that
count alone.

# HARD RULES. Violating any one of these kills the points.

1. **`#TargetPartner` at the START of the caption**, plus **`#ClubTarget`**. These
   two are required on every single challenge post. No post counts without both.
2. **THE PRICING RULE, CORRECTLY SCOPED.** She cannot state prices for **TikTok Shop
   items she links on TikTok**. That is the entire rule. It comes from a TikTok Shop
   violation on 4 Aug 2026 and is enforced by TikTok Shop against TikTok Shop
   listings.
   - It is **not** a Target rule. Club Target has no pricing penalty.
   - Club Target posts carry `club.target.com` affiliate links, not TikTok Shop
     listings, so **a price in a Club Target caption is fine**.
   - A price visible on a shelf tag in frame is fine. Do not cut the frame.
   - Do not flag a price on a Club Target post. Ever.
   - Full text: `content/canon/pricing-rule.md`.
   - Note: `scripts/validate-wave.py` still carries an over-broad no-prices check
     that predates this correction. If it fails only on a price in a Club Target
     row, that is a false alarm. Say so and proceed.
3. Disclosure line, verbatim: "I'm a Target partner, so I may earn rewards or
   commission when you shop my link, at no extra cost to you."
4. Every Instagram and Facebook post names a LIVE keyword. Never ship a post
   pointing at nothing. Check with `blotato_list_automations` first.
5. No duplicates. Do not re-queue an asset already scheduled to the same platform.
6. Voice: warm, grounded, practical. No hype. **No em dashes.** Digits, not
   spelled-out numbers. Contractions always. Product copy reads as lived experience,
   not ad copy. Max 5 hashtags on Instagram, none on Facebook or LinkedIn.
7. Platform lanes: Instagram and Facebook share a lane, TikTok is separate because
   TikTok Shop is a separate business. Do not blanket cross-post.
8. **Nothing publishes without Amanda's approval.** Queue it, show her the list,
   wait.

# THE CLAIM STEP, and what you cannot do

Posting does not earn the points. Amanda has to claim each one on
`club.target.com`. **You cannot claim for her.** The board is a JavaScript app
behind a login and returns an empty shell to any non-browser client. Never say you
claimed or submitted anything.

A routine already runs daily at 16:00 UTC that catches each publish and appends it
to `content/club-target-claim-ledger.md`. Keep that file accurate.

# OPEN QUESTION, resolve early

Every challenge on her board reads **0%**, including ones she has published for.
Her captions do carry both required tags, so this is not a tagging error. It is
either a lag in Target's review or a submission step in the portal she has not
done. **Have her check one challenge card for a submit or link-your-post action
before you produce another 20 posts on top of it.**

# WHAT TO HAND BACK

1. What you queued from the existing library, where, and at what times.
2. The new footage inventory, merged with the existing one.
3. Which of the 4 gap themes are now actually covered by real files, and which are
   not.
4. Whether the FALLFIT SKU was recoverable from her photos.
5. The shortest possible list of anything only she can still do.

Commit to branch `claude/club-target-game-plan-9xs2du`.
End commit messages with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
