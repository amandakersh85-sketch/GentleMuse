# The Club Target disclosure rule, from the official Scope of Work

Source: `1gy7-target-scope-of-work.pdf`, linked in every weekly Club Target email
from `target@duel.technology`. Pulled 13 Sep 2026 from
`https://obs.duel.me/media/684be12737bd76dbd7a6adf3/2604/1gy7-target-scope-of-work.pdf`.
Full text saved at `content/reference/club-target-scope-of-work.txt`.

This is Target's own document. It supersedes anything inferred.

## What it requires

For Instagram and TikTok, `#TargetPartner` must appear **at the very beginning of
the caption OR in on-screen text**.

**Placement rules, quoted:**
- Must appear within the first 2 lines of captions
- On Stories and videos, place it on screen and near the link or product
- The disclosure must be visible without tapping "more" or scrolling

**Videos and Stories, quoted:**
- The disclosure must appear **early in the video** or Story frame
- For multi-frame Stories or longer videos, **repeat the disclosure**
- Each Story frame with a Target link or product must include a disclosure

**What does not count, quoted:**
- Disclosure only in your bio
- **Disclosure hidden at the end of captions**
- Relying solely on platform "paid partnership" tools

"Failure to properly disclose may result in removal from the program."

## Where Amanda actually stands, measured 13 Sep 2026

**Captions: clean.** All 42 Club Target posts carry `#TargetPartner` within the
first 2 lines. Zero failures.

**Video frames: failing.** Three published Club Target TikToks were pulled from the
CDN and sampled across their full duration:

| Post | Date | Theme | On-screen disclosure |
| --- | --- | --- | --- |
| `6966604` | 12 Sep | Wellness Reset | **final frame only** |
| `6919291` | 10 Sep | Fall Collage | **final frame only** |
| `6933972` | 11 Sep | Everyday Favorites | **none anywhere** |

The Scope of Work says the disclosure must appear EARLY in the video. Hers appears
last, or not at all. That is the most likely reason every challenge on her board
reads 0% while her captions look correct.

## The rule going forward

Every Club Target video must carry `#TargetPartner` **on screen in the opening
frames**, near the product, and repeat it later in anything longer than about 15
seconds. Keeping it in the final frame as well is fine, but the final frame alone
does not satisfy the requirement.

## Unresolved: the other-brands clause

The Scope of Work also says a post "cannot include references to products/services
from any other brands."

The plain reading would forbid naming NYX, FlavCity, Dr Teals, Tree Hut, Molly's
Suds and similar, all of which Amanda has named in Club Target posts and all of
which Target sells. The sensible reading is that the clause means competitors and
other retailers, not vendors stocked by Target, since most challenges are
impossible to complete otherwise.

**Do not act on this either way.** It is ambiguous and the downside of guessing
wrong is large. Amanda has a live email thread with `clubtarget@target.com` that
has answered two policy questions already. Ask there.

## What this is NOT

This is not the pricing rule. The Scope of Work says **nothing whatsoever about
prices.** That confirms `content/canon/pricing-rule.md`: the price restriction is a
TikTok Shop rule, not a Target rule, and it does not touch Club Target content.

## 24 Sep 2026: first overlay added after the fact, the 6 Oct pair

Amanda asked for a `#TargetPartner` overlay on the 6 Oct rows before they publish.
Done and verified live in Blotato.

| Row | Platform | Time UTC |
| --- | --- | --- |
| `4726792` | Instagram Reel | 06 Oct 18:30 |
| `4726804` | TikTok | 06 Oct 21:30 |

Both rows carried the **same** file, `75caa1aa-5c29-4235-a8e5-6d0578e65c33.mp4`
and `a0fe13f0-f271-4585-8e5e-1ba40e20489c.mp4`, byte identical (md5
`d9c231f442b98f50156af17325d34b6f`). 1080x1920, 30.3 seconds, talking head at
home doing her makeup, burned title cards at the top and a verbatim caption rail
low. No disclosure anywhere in the original.

### What was added

A red chip, `#CC0000` with white DejaVu Sans Bold at 52px, 24 by 16 padding,
placed at x 56, y 440. That sits just under her title card, clear of her face and
clear of the caption rail, and it matches the red chip she already uses on the
fall layers cut.

Shown **0.5 to 6.5 seconds** and again **15.0 to 21.0 seconds**. Early, and
repeated, which is what a 30 second video needs.

### How to redo it

`drawtext` is NOT in this container's ffmpeg build, even though libfreetype shows
in the config. `drawbox`, `overlay`, `ass` and `subtitles` are. So build the chip
as a PNG with Pillow (`pip install pillow`) and composite it:

```
-filter_complex "[0:v][1:v]overlay=56:440:enable='between(t,0.5,6.5)+between(t,15,21)'[v]"
-map "[v]" -map 0:a -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a copy
```

### Blotato re-hosts on update

`blotato_update_schedule` does not keep the URL you hand it. It copies the file
into its own store and rewrites `mediaUrls`. The upload went to
`552af97f-e702-46c0-888a-78380f32d081.mp4` and the rows came back pointing at
`408a5925-ea90-4d9c-86ed-05ec0983822e.mp4` (TikTok) and
`5b9b6ac5-db80-4d91-9a23-55b29cc2f878.mp4` (Instagram).

**So verify after updating, do not trust the URL you sent.** All 3 re-hosted
copies pull down md5 `46d684eec3a5d86503238c74745fda80`, identical to the local
render, so both rows are confirmed carrying the overlay.

### To roll back

The originals are untouched at their own URLs. Point `mediaUrls` back at
`a0fe13f0-f271-4585-8e5e-1ba40e20489c.mp4` for either row.

### Still open on these 2 rows

The captions carry `#TargetPartner` in the **closing** hashtag block, not the
first 2 lines. The Scope of Work names "disclosure hidden at the end of captions"
as something that does not count. The overlay now covers the on-screen half of
the rule, but the caption half is still failing on both. Not changed, she only
asked for the overlay.
