# The Cesa video pipeline: resolved

**The blocker was my assumption, not the tooling.** I had been treating "keep the Remotion
pipeline active" as needing a local Remotion render, which needs a `clips/` library and a
`clip-library.csv` that live on Amanda's machine, not here. That path is genuinely closed from
this session.

**It did not need to be that path.** Amanda has 21 real Cesa video assets already sitting in
Blotato from her published post history, every one a public URL that can be scheduled directly
or fed into Blotato's own render templates. No local render required, and no AI-generated dog,
which matters because a synthetic Cesa would break the exact trust the channel is built on.

## The 21 recovered clips

Harvested from her published posts by matching Cesa-related copy and collecting mediaUrls.
Themes available: coming home after a shift, the 17 nicknames, strange sleeping positions,
the office accident, growing old beside you, the Target food ad, scene-stealing supporting
role, the AI-posted-without-checking series.

Full URL list is recoverable any time by running blotato_list_posts over published history and
filtering captions for Cesa terms.

## Blotato templates that replace local Remotion

| Need | Template | Notes |
|---|---|---|
| Stitch clips, add title, captions, music | `/base/v2/combine-clips/c306ae43-...` | Uses her real footage |
| Photo slideshow with text overlays | `/base/v2/image-slideshow/5903b592-...` | Her photos, not AI |
| Carousel with intro, content, CTA slides | `/base/v2/tutorial-carousel/e095104b-...` | The Press Play structure |
| AI voice over scenes | `/base/v2/ai-story-video/5903fe43-...` | Avoid for Cesa. AI images would not be her |

## Standing rule for Cesa video

Never generate a synthetic Cesa. The channel works because she is real and 19. Use her actual
footage, recombined and re-captioned. AI templates are fine for the home and AI content on the
main accounts, never for her.

## Scheduled on her channels

| When (CDT) | Channel | Clip | CTA |
|---|---|---|---|
| Aug 26 6:30p | IG | sleeping positions | CESA |
| Aug 27 6:30p | IG | coming home after a shift | CESA |
| Aug 27 8:00p | TikTok | sleeping positions | link in bio |
| Aug 28 6:30p | IG | the 17 nicknames | CONSIDER |
| Aug 28 8:00p | TikTok | she just wants me back | link in bio |
| Aug 29 6:30p | IG | grow old beside you | CESA |
| Aug 29 8:00p | TikTok | peed in the office | link in bio |
| Aug 30 6:30p | IG | peed in the office | CESA |
| Aug 30 8:00p | TikTok | scene stealing supporting role | link in bio |

IG runs the keyword CTA every time. TikTok cannot fire comment-to-DM, so it stays on link in
bio. CESA to CONSIDER is roughly 2 to 1, per the channel standard.
