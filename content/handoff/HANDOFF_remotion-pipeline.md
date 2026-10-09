# Handoff to the local Remotion project

Written 2 Oct 2026 by the cloud session on branch
`claude/club-target-game-plan-9xs2du`. For the Claude session running against
Amanda's Remotion project on her laptop.

Read this before touching a composition. It is the goals and the contract, not
your code. You know your repo, I do not.

---

# 1. WHAT YOU ARE IN THIS SYSTEM

You are the **ingest and render head**. You are the only part of the system that
can see raw footage.

There are two Claudes working for Amanda and they can't reach each other's files.

| | Cloud session (me) | You, on the laptop |
|---|---|---|
| Runs in | ephemeral cloud container | her actual machine |
| Can see her phone, SD card, Downloads | **no, never** | yes |
| Can see raw unedited footage | **no, never** | yes |
| Can render video | crudely, ffmpeg only, no `drawtext` | **yes, properly, Remotion** |
| Can read and write the Blotato queue | yes | presumably not |
| Holds the compliance canon | yes, in `content/canon/` | read it from git |

**The practical consequence.** Every asset I can work with is something that was
already posted or queued through Blotato, because the Blotato CDN is the only
media library I can reach. I audited this on 12 Sep: 659 unique assets, all of
them already published or scheduled. Her Google Drive has zero video files. The
container filesystem has one media file and it isn't hers.

So **footage that never goes through your pipeline does not exist to me.** That
is the bottleneck this handoff is about.

## Correct an error in the older handoffs

`HANDOFF_trackB-phone-ingest.md` and `HANDOFF_local-target-ingest.md` both say
"use the Remotion pipeline already in the repo." **That is wrong.** There is no
Remotion code in the GentleMuse git repo. I grepped it. The pipeline is yours,
on her laptop, and the cloud side has never seen it. Those lines were written
assuming one machine. Ignore them.

---

# 2. WHAT I NEED BACK FROM YOU

I am asking for a report, not a change. Tell Amanda, or write it into
`content/handoff/` and push, so the cloud side stops guessing:

1. **Where raw footage lands** and how it gets there from her phone.
2. **The composition list.** What renders exist, what props each takes.
3. **The render command**, and roughly how long a 30 second 1080x1920 takes.
4. **Where finished renders land** on disk.
5. **Whether you can upload.** This is the big one, see section 6.
6. **What the pipeline already does automatically** versus what she does by hand
   in the Edits app. She hand-edited a Target haul on 1 Oct, so the two paths
   coexist and I don't know where the line is.

---

# 3. OUTPUT SPEC

Everything that ships is vertical short-form.

- **1080x1920, 30fps, H.264, yuv420p, `+faststart`.** This matches every asset
  on the CDN. I verified today's Amigos master: 1080x1920, 29.9fps, h264 High.
- **Length 20 to 35 seconds.** Her published work sits there.
- **Build every edit so it works silent.** See section 5.
- Deliver the file. Do not burn in a platform watermark.

---

# 4. THE COMPLIANCE RULES. THESE ARE RENDER-TIME, NOT CAPTION-TIME

This section is the real reason you are getting a handoff. **Two of Amanda's
three compliance rules can only be satisfied inside your pipeline.** I can't fix
them after the fact without a lossy re-encode.

## 4.1 The disclosure burn-in. Highest priority thing in this document.

Source: Target's own Scope of Work PDF, pulled 13 Sep. Full text at
`content/reference/club-target-scope-of-work.txt`, analysis at
`content/canon/disclosure-rule.md`.

For any **Club Target** video, Target requires `#TargetPartner`:

- **on screen, early in the video**, not just in the caption
- **near the product or link**
- **repeated** in anything longer than about 15 seconds
- visible without tapping "more"

Explicitly does NOT count, quoted from the document: disclosure only in the bio,
**disclosure hidden at the end of captions**, relying on the platform's "paid
partnership" toggle.

> "Failure to properly disclose may result in removal from the program."

**This is very likely why every challenge on her board read 0% while her captions
looked correct.** I sampled three published Club Target TikToks across their full
duration. `6966604` and `6919291` carried the disclosure on the **final frame
only**. `6933972` had **none anywhere**. Captions were clean on all 42 posts. The
failure was entirely in the render.

**So: build `#TargetPartner` into the Club Target composition as a first-class
element, not something a human remembers to add.** The house treatment, already
used and matching her existing look, is a red chip:

- `#CC0000` rounded rectangle, white bold text, about 52px, 24x16 padding
- positioned clear of her face and clear of any caption rail
- shown roughly **0.5s to 6.5s**, and again **15.0s to 21.0s** on a 30s cut

A prop flag like `isClubTarget: true` that drives this automatically would end
this entire class of failure. That is the single highest-value change you can
make to the pipeline.

## 4.2 The reverse rule, learned the hard way on 24 Sep

**Never put `#TargetPartner` on a video that is not a Target partnership.** I did
exactly that, to a TikTok piece that had nothing to do with Target, and had to
reverse it the same day. Amanda: "it wasn't made for target, it was originally
just a piece for tiktok."

A false disclosure declares a paid relationship that does not exist. That is
worse than a missing one.

A post is genuinely Club Target only if it names a Target product **and** carries
the `club.target.com` link **and** carries the partner disclosure sentence. Tags
alone mean nothing.

## 4.3 The pricing rule, and what it is NOT

Full text: `content/canon/pricing-rule.md`. Amanda corrected this personally on
13 Sep after it was misapplied several times, including once by me.

```
TikTok Shop items + linked on TikTok = no price.
Everything else = no restriction.
```

**It is not a Target rule.** Target has no pricing penalty and the Scope of Work
says nothing whatsoever about prices. Club Target posts may name prices freely. A
shelf tag with a price visible in frame is fine. **Do not strip price cards from
a Target render.** Three captions were edited on 7 Sep on a wrong reading of this
and she was not happy about it.

---

# 5. AUDIO. NEW RULE AS OF TODAY, 2 OCT

Amanda, today: *"I'm really tired of having some weird music or store
background."*

I measured the Amigos food review master to check what was actually on the track.
Per-half-second RMS across 29 windows: min -27.9 dB, max -14.7 dB, **spread 13.3
dB with no silence gaps anywhere.** That is a continuous music or ambient bed.
Speech drops to about -45 dB in the gaps between phrases. There is no voice on
that track. All the meaning is carried by on-screen text cards.

**So the rule for the pipeline:**

1. **Default to rendering silent**, or with a clean removable bed on its own
   track. Do not bake store ambience into the master.
2. She adds music **natively in-app**, from the TikTok and Instagram Commercial
   Music Library. Licensed tracks cannot be fetched and composited from outside;
   they have to be attached in the app. A silent render is what lets her do that.
3. **If she hands you a voice memo, drop it into the render natively.**
4. **Never generate a synthetic voice.** Hard rule, no exceptions.

This is the same call we made for the Kuromi video and for today's Amigos recut,
and she has accepted it both times.

---

# 6. THE UPLOAD PROBLEM, AND HOW TO SOLVE IT

Right now a finished render on her laptop cannot reach the queue unless she
uploads it by hand.

Blotato has `blotato_create_presigned_upload_url`. If you have Blotato MCP access
on the laptop, **you can close this loop end to end**: render, upload, get a
public CDN URL, and either queue it yourself or hand me the URL to queue.

If you don't have Blotato access, say so, and the fallback is that I generate a
presigned URL from this side and she pushes the file to it. That works but needs
her in the loop for every asset.

**Closing this loop is the second highest-value change after the disclosure
flag.** It is the difference between a pipeline and a pile of exported files.

## Two things that will bite you on upload

- **Blotato re-hosts on update.** `blotato_update_schedule` does not keep the URL
  you give it. It copies the file into its own store and rewrites `mediaUrls`.
  **Always verify by re-reading the row after writing, never trust the URL you
  sent.** Confirm by md5 if it matters.
- **Verify the URL resolves before queueing.** On 23 Sep I built a media URL from
  a truncated prefix and invented the rest. It scheduled fine and pointed at
  nothing. It would have failed silently four days later and I'd have reported it
  as queued. A `curl -r 0-1023` expecting HTTP 206 catches this in one second.

---

# 7. HOW SHE FILMS, SO YOU CUT WHAT IS ACTUALLY THERE

Full detail: `content/canon/filming-method.md`. This file exists because a stale
rule nearly caused a session to reject her own good footage.

**Her mode varies and you cannot assume it.**

- Through 12 Sep: talking head, on camera, speaking
- 14 Sep denim TikTok: silent b-roll, no face
- 15 Sep fall fits: on camera, in a fitting room
- 1 Oct Target haul: hand-edited by her in the Edits app

On 12 Sep she said flatly she would not do on-camera or fitting room work. On
15 Sep she published a fitting room video. That is her call to make and she
changed it.

**So: look at the frames before you write anything. Never write a caption or a
text card that claims a shot the footage does not contain.** If you are planning
a shoot rather than cutting existing footage, ask her. Product and aisle footage
is always safe: shelf, rack, endcap, item picked up and turned, item in cart.

**The hook.** With possibly no face and possibly no voice, the first 2 seconds
are carried by the on-screen text line and the strongest frame. Lead with the
frame, not a talking setup. A verdict or a claim beats a windup. I recut Amigos
today for exactly this: the original opened on an abstract line over a sign and
buried "7.5 out of 10" at the 25 second mark. The recut opens on the verdict.

---

# 8. HER VOICE, FOR ANY TEXT YOU RENDER

- No em dashes. Ever.
- Digits, not spelled-out numbers. "7.5 out of 10", not "seven point five".
- Contractions.
- No hype, no guru voice, no overnight-success framing.
- Instagram max 5 hashtags. Facebook and LinkedIn none.
- **Nothing ships without her approval.**

---

# 9. WHAT THE QUEUE NEEDS FROM YOU RIGHT NOW

Current state as of 2 Oct, from a full fresh pull.

**The queue is starving in the back half of October.** 11 to 18 posts a day
through 8 Oct, then 1 to 3 a day after the 20th. 22 Oct is completely empty.
New renders should target **21 Oct onward**.

## 9.1 Four food reviews have no footage anywhere I can reach

Amanda wants six local food reviews back in rotation: Scooter's Coffee, Sidecar
Cafe, Amigos, Rico Tacos, Scratch Cupcakery, Lucy's.

I paginated her **entire** Blotato record to its floor at 7 May 2026. 1910 unique
posts, all platforms. Result: **only Scooter's and Amigos exist as reusable
assets.** Sidecar Cafe, Rico Tacos and Scratch Cupcakery have never been through
Blotato at all. She may have posted them natively, which would mean the files
exist on her machine and not on the CDN.

**Check her local drives for these three.** If the footage is there, it is
invisible to me and recoverable only by you. That is a concrete win available
today.

- **Lucy's**, a loose meat sandwich shop in Cedar Rapids, filmed 2 Oct, raw and
  unedited on her phone. Needs a cut. This is the most immediate job.
- Full detail in `content/food-review-rotation.md`.

## 9.2 Target footage shot 2 Oct at Cedar Rapids, not yet cut

From her messages while in store. All raw on the phone:

- **Holiday creep**: Christmas next to Halloween in Bullseye Playground
- **Bullseye Playground** shots
- **Beauty Studio**, the aisle is literally signed "beauty studio"
- **Food endcaps**, plus endcaps from the other Target
- **Toys**, including a Lego display she called out as good
- **Two Hyde & EEK Halloween decor items**, DPCI `240-43-3184` and `240-43-5023`,
  bought for an at-home decorate-with-me for challenge `0q0x`

**Note on DPCI.** Shelf tags print a DPCI like `240-43-3184`. Storefront links use
an 8-digit SKU like `/_/sku/94895169`. **They are not derivable from each other.**
She has to pull the real SKU from inside her Club Target storefront. Do not try to
construct one.

Every one of these needs the disclosure burn-in from section 4.1.

---

# 10. ACCOUNTS AND SLOTS, IF YOU QUEUE DIRECTLY

| Account | Platform | ID |
|---|---|---|
| @thegentlemuse2026 | Instagram | `45886` |
| @thegentlemuse2026 | TikTok | `41488` |
| Amanda Kersh | Facebook | `30840`, pageId `1086399221215093` |
| The Gentle Muse | YouTube | `36129` |
| **cesasgoldenyears** | Instagram | `65540` |
| **cesasgoldenyears** | TikTok | `55761` |

**Cesa's accounts are a separate brand. Never put Target or Gentle Muse content
there.** Cesa content must never give veterinary advice.

Slots in use, UTC. Central is UTC-5 until 1 Nov.

- Instagram 15:00, 18:30, 20:15, 21:00, 22:30, 23:00, 23:30
- TikTok 15:00, 21:00, 23:00, 23:45
- Facebook 15:30, 17:10, 22:15, 23:30
- YouTube 17:20, 19:45, 22:45, 23:30

**TikTok post creation requires all of these or it 400s:** `privacyLevel`,
`disabledComments`, `disabledDuet`, `disabledStitch`, `isYourBrand`,
`isAiGenerated`. **YouTube requires** `title`, `privacyStatus`,
`shouldNotifySubscribers`.

---

# 11. THE OBJECTIVE, SO YOU OPTIMIZE FOR THE RIGHT THING

Amanda, in her own words, recorded in `content/canon/positioning.md`:

> "Basically, I'm an accountability coach. That does food reviews and affiliate
> marketing. And still works full time at Walmart."

Food reviews are a **standing pillar**, not filler. Her reason: *"I like for my
food reviews to get cycled through, so that way people are used to seeing me as a
food critic and food reviewer... I don't want people to just think I'm one note."*

She is also studying vending and laundromat businesses. **That is explicitly
phase 2.** *"We're not going to focus on that part right now. We're doing it in
phases."* Do not pull it forward.

**The objective is audience growth, not the Club Target scoreboard.** I got this
wrong on 22 Sep and she corrected me:

> "The fucking principle is we're trying to get more followers... as long as we do
> post the target stuff to Instagram we're conditioning our followers and
> non-followers alike to enjoy and engage with that type of content... We're in a
> growth phase."

So **do not deprioritize an Instagram cut because Instagram earns no Club Target
points.** Points are a scoreboard. Followers are the goal.

---

# 12. THINGS THAT WILL WASTE YOUR TIME

- **`club.target.com` cannot be read by any agent.** It is a JS single-page app
  behind her login and returns an identical empty shell. Retested 22 Sep and
  2 Oct. **I cannot and must not claim her points.** Only she can, logged in.
- **`redsky.target.com` returns 435.** `www.target.com` is a JS SPA with no
  product data. There is no programmatic route to Target product info.
- **Gmail authorization has been down since about 21 Sep.** Three Monday Club
  Target challenge drops were missed: 21 Sep, 28 Sep, and 5 Oct is coming.
  **She needs to re-authorize Gmail.** Challenge names come from tile PNGs in
  those emails and we are flying blind without them.
- **Never write into her existing DM conversations.** Off limits.
- **Do not upload or screenshot her filled Paycheck Planner.** It has account
  numbers, rent, her landlord, utilities and a roommate's full name.
- **Payhip hazard:** stored `sale_price` reads $5.00. Ticking the sale box
  without typing a price puts a $37 product on sale for $5.

---

# 13. IF YOU ONLY DO THREE THINGS

1. **Make `#TargetPartner` an automatic, early, repeated on-screen element of the
   Club Target composition.** Driven by a prop, not by memory. This is the
   compliance failure that most likely zeroed her board, and it is fixable only
   at render time.
2. **Close the upload loop** so a finished render reaches the queue without her
   hand-carrying it.
3. **Cut Lucy's, and search her drives for Sidecar, Rico Tacos and Scratch
   Cupcakery.** Four of her six food reviews are missing and three of them may
   already exist on that machine.

Then report back what section 2 asks for, so the cloud side stops guessing about
your half of the system.
