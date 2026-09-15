# TRACK B HANDOFF: ingest the phone and cut the 12 Sep footage

Paste everything below the horizontal rule into a Claude Code session on Amanda's
laptop, after she connects her phone. Written for a session with zero prior
context.

Track A (refilling the queue from footage already on the Blotato CDN) is being run
separately in the cloud session. **Do not do Track A here.** Your job is the new
footage only.

---

You work for Amanda Kersh, The Gentle Muse. Club Target creator, handle
`amanda.20`, storefront `club.target.com/a/amanda.20`. Club Target pays POINTS per
challenge, every challenge has a hard expiry, and each theme is the same footage
cut 3 ways: IG Story, IG Reel or Post, and TikTok.

She got back from a Target run on 12 Sep 2026 with new footage on her phone. Your
only job is to get that footage off the phone, verify what is actually there, cut
it, and queue it.

Another session is separately refilling the queue from her existing library. Do not
touch the existing library, do not produce from it, do not reschedule anything you
did not create. If you find yourself planning content from footage older than
12 Sep, stop, you are in the wrong lane.

## STEP 1. Find the footage. Do not ask her for a path.

- macOS: `~/Pictures/Photos Library.photoslibrary`, Image Capture staging,
  `~/Downloads`, `/Volumes/*`
- Windows: `This PC\<phone>\Internal storage\DCIM\Camera`, `~/Downloads`, `~/Videos`
- Also any Photos or iCloud sync folder, AirDrop, and Downloads

Filter to files created **12 Sep 2026 or later**. Copy them into a working folder
inside the repo. **Do not move or delete anything off the phone.**

Inventory every file: filename, path, duration, created timestamp, and your best
guess at the product or aisle. For any video you cannot identify from the filename,
sample a frame with ffmpeg and actually look at it. Do not guess from the filename
alone.

**If the phone has nothing dated 12 Sep or later, say so in one line and stop.** Do
not go hunting through older footage. Do not backfill from her existing library and
present it as the new run. Just tell her the phone did not have it.

## STEP 2. Verify against what she says she shot

She reported this on 12 Sep. Treat it as a claim to check, not as fact. All of it
is b-roll, no narration, she is not in frame.

| Theme | She says | Note |
| --- | --- | --- |
| Find Your Denim | got it | product and rack footage, no try-on |
| Make It Yours with Heyday | got it | current, replaces the 20 Aug footage |
| New Ways to Play | got it | filmed the entire gaming wall, family game night framing |
| Game Day Line Up | **partial** | she shot **sportswear**, not snacks |

**SKUs she captured:** the dress and the sweater she bought. Both also feed Fall
Style Collage.

**Not captured:** the medicube Kojic Acid Turmeric Jelly Gel Mask shelf tag.

Report any gap between this table and the actual files plainly. If a theme she
thinks she got is not really on the phone, that is the single most important thing
you can tell her, and it is better said tonight than on the deadline.

## STEP 3. Cut in this priority order

Deadlines are from 13 Sep 2026.

1. **Find Your Denim**, TikTok. Expires **23 Sep, 10 days**. 30 points. Nothing
   exists for it. This is the only new-footage theme with real time pressure.
2. **New Ways to Play**, TikTok. Expires 30 Sep, 17 days. 30 points.
3. **Game Day Line Up**, TikTok. Expires 7 Oct, 24 days. 30 points.
4. **Make It Yours with Heyday.** Expires 16 Sep, but it is **Instagram only on the
   board**, and Instagram earns Amanda no Club Target credit until she passes 500
   followers. So it is worth **0 points today**. Cut it for reach if there is time,
   never before 1 through 3 are queued.
5. Anything left over becomes filler for the repeatable challenges.

**Instagram earns no Club Target credit below 500 followers.** That gate decides
priority throughout. Keep posting to IG to grow the account, but never count it as
points and never let an IG cut delay a TikTok cut.

### Game Day, unresolved read

Board copy: "What makes your game day lineup? Round up the Target finds you
actually reach for on game day." That supports either reading, food or apparel. She
shot apparel. Snacks is the more common interpretation and she offered to go back
for chips, dips and drinks. It expires 7 Oct, so there is no rush. If only
sportswear exists, ship sportswear, it satisfies the copy. If she later gets snacks,
cut that as primary and keep sportswear as a second attempt.

### Denim, specifically

**No fitting room, no try-on.** The challenge asks her to show Target denim, not
model it. Rack pan, folded stack, one pair held up to the light, close on the wash
and the stitching. That satisfies it completely.

## STEP 4. Fix automation 2277 if the SKU is in her photos

**`2277` IG FALLFIT** points at the bare storefront instead of a product page.
Universal Thread Open Stitch Cozy Cardigan, old SKU `94430282` is dead. The
automation is literally named "NEEDS SKU, cardigan 94430282 is dead". Anyone who
comments FALLFIT currently lands on a storefront.

She photographed shelf tags for the dress and the sweater she bought. If the
Universal Thread piece is among them, read the SKU off the tag and repair the
button with `blotato_update_automation`.

**`453` FB MASK** has the same failure, broken since 8 Aug, and needs the medicube
Turmeric Jelly Gel Mask tag she did not get. Leave it broken and note it.

# HOW SHE FILMS. Fixed. Do not plan around anything else.

- **Whether she is on camera VARIES. Do not assume either way.** She said on
  12 Sep she would stay off camera, then published an on-camera fitting room post
  on 15 Sep. Her older work is talking head. **Cut what the footage actually
  contains**, look at the frames before writing a caption, and never claim a shot
  the footage does not have. See `content/canon/filming-method.md`.
- **Product and aisle footage only.** Shelf, rack, endcap, the item picked up and
  turned, the item in the cart. That is the whole vocabulary.
- **She may not record a voiceover.** Build every edit so it works silent, carried
  by on-screen text and the caption. If she hands you a voice memo, drop it into the
  Remotion render natively and treat it as a bonus, never a dependency. **Never
  generate a synthetic voice.**

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
caused collisions before. Another session may be writing to the same queue tonight,
so this matters more than usual: check for a collision at every slot you intend to
use, and if a slot is taken, move yours rather than overwriting.

**`blotato_list_posts.postTime` is not reliable.** It has disagreed with
`blotato_get_schedule.scheduledAt` by up to 9 days. Confirm a scheduled time with
`blotato_get_schedule` before trusting it.

**`blotato_list_posts` returns no `accountId`, only `platform`.** Her two Instagram
accounts get summed into one number. Do not conclude a cap is breached from that
count alone.

# HARD RULES. Violating any one of these kills the points.

1. **`#TargetPartner` at the START of the caption**, plus **`#ClubTarget`**. Both
   are required on every single challenge post. No post counts without both.
2. **THE PRICING RULE, CORRECTLY SCOPED.** She cannot state prices for **TikTok
   Shop items she links on TikTok**. That is the entire rule. It comes from a TikTok
   Shop violation on 4 Aug 2026 and is enforced by TikTok Shop against TikTok Shop
   listings.
   - It is **not** a Target rule. Club Target has no pricing penalty.
   - Club Target posts carry `club.target.com` affiliate links, not TikTok Shop
     listings, so **a price in a Club Target caption is fine**.
   - A price visible on a shelf tag in frame is fine. **Do not cut the frame.**
   - **Do not flag a price on a Club Target post. Ever.**
   - Full text: `content/canon/pricing-rule.md`.
   - `scripts/validate-wave.py` still carries an over-broad no-prices check that
     predates this correction. If it fails only on a price in a Club Target row,
     that is a false alarm. Say so and proceed.
3. **ON-SCREEN DISCLOSURE. This is the one most likely to be costing her points
   right now.** Target's official Scope of Work requires that on videos,
   `#TargetPartner` appears **on screen, early in the video, near the product**,
   and is **repeated** in anything longer than roughly 15 seconds. A disclosure
   that appears only at the end does **not** count.
   - Measured 13 Sep: her captions all pass, but of 3 published Club Target
     TikToks sampled, 2 carry the disclosure only in the final frame and 1 carries
     none at all. Every challenge on her board reads 0%. These are probably the
     same fact.
   - So **every video you cut must open with `#TargetPartner` burned into the
     first frames.** Put it near the product, not floating in a corner. Repeat it
     around the midpoint on anything over 15 seconds. Keep it in the end card too
     if you like, but the end card alone is a fail.
   - Full rule and the source document: `content/canon/disclosure-rule.md` and
     `content/reference/club-target-scope-of-work.txt`.
4. Disclosure line in the caption, verbatim: "I'm a Target partner, so I may earn
   rewards or commission when you shop my link, at no extra cost to you."
5. Every Instagram and Facebook post names a LIVE keyword. Never ship a post
   pointing at nothing. Check with `blotato_list_automations` first.
6. No duplicates. Do not re-queue an asset already scheduled to the same platform.
7. Voice: warm, grounded, practical. No hype. **No em dashes.** Digits, not
   spelled-out numbers. Contractions always. Product copy reads as lived experience,
   not ad copy. Max 5 hashtags on Instagram, none on Facebook or LinkedIn.
8. Platform lanes: Instagram and Facebook share a lane, TikTok is separate because
   TikTok Shop is a separate business. Do not blanket cross-post.
9. **Nothing publishes without Amanda's approval.** Queue it, show her the list,
   wait.

# THE CLAIM STEP, and what you cannot do

Posting does not earn the points. Amanda has to claim each one on
`club.target.com`. **You cannot claim for her.** The board is a JavaScript app
behind a login and returns an identical empty shell to any non-browser client.
Verified five ways on 31 Aug: direct curl, `www.target.com`, headless Chromium, the
tile image CDN `d3k81ch9hvuctc.cloudfront.net`, and `obs.duel.me`. Do not re-test
and do not burn time on it. Never say you claimed or submitted anything.

A routine already runs daily at 16:00 UTC that catches each publish and appends it
to `content/club-target-claim-ledger.md`. Keep that file accurate for anything you
queue.

# THE 0% MYSTERY, likely solved 13 Sep

Every challenge on her board reads **0%**, including ones she has published for.
Her captions are not the problem: all 42 Club Target posts carry `#TargetPartner`
within the first 2 lines.

**The video frames are.** Target's Scope of Work requires the disclosure on screen
EARLY in the video. Of 3 published Club Target TikToks sampled, 2 carry it only in
the final frame and 1 carries none. See `content/canon/disclosure-rule.md`.

So cut every new video with the disclosure in the opening frames and this should
stop recurring. It does not fix the already-published ones, which only Amanda can
edit, and it does not rule out a second cause: there may also be a submit or
link-your-post step in the portal she has not done. **Have her open one challenge
card and look for a submit action.** Two minutes, and it either confirms or
eliminates the remaining possibility.


# WHAT TO HAND BACK

1. The new footage inventory: what was actually on the phone.
2. Which of the 4 themes are genuinely covered by real files, and which are not.
   Be blunt about any gap between this and what she thinks she shot.
3. Whether the FALLFIT SKU was recoverable from her shelf tag photos.
4. What you queued, where, and at what times.
5. The shortest possible list of anything only she can still do.

Commit to branch `claude/club-target-game-plan-9xs2du`.
End commit messages with:
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
