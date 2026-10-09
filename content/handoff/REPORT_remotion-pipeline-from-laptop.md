# Report back from the laptop Remotion session

Written 2 Oct 2026 on Amanda's machine, answering
`content/handoff/HANDOFF_remotion-pipeline.md` section 2.

Everything below was read off this machine today, not remembered.

---

## 1. Where raw footage lands, and how it gets off her phone

**Transport: USB MTP, driven by a PowerShell script. There is no cloud step.**

- `D:\Claude Projects\Gentle Muse\Drafts\Count-NewPhoneFootage.ps1` is a dry run. It
  diffs the phone against the drive **by basename** across 4 local roots, and reports
  the count and bytes so the pull can be estimated before it starts.
- `D:\Claude Projects\Gentle Muse\Drafts\Pull-PhoneFullDiff.ps1` does the copy.
- Phone is a **moto g stylus - 2025**. Source folders: `DCIM\Camera`, `DCIM\HeyGenVideos`,
  `Pictures\Cesa`, `Pictures\Reels Stories`, `Pictures\Gentle Muse Branded Images`.
- Landing zone: `D:\Phone Backup\<YYYY-MM-DD> Phone Import\`.

**Today's run:** 32 new on the phone, 31 copied (1 was a folder), 0.97 GB, about 1 minute,
all 31 verified byte-exact against the phone's reported sizes. Nothing is ever trusted
from the script's own "done" line; the verification is a separate size comparison.

**She must be at the machine with the phone plugged in and set to File transfer.** This
is the step no agent can do alone, which is the real reason footage does not reach you.

Other raw roots worth knowing: `D:\Claude Projects\Gentle Muse\ClubTarget\01_RAW_INSTORE`,
`D:\Claude Projects\Gentle Muse\Footage`, `D:\Takeout-Staging`.

## 2. The composition list

Remotion 4.0.5x, project at `D:\Claude Projects\Gentle Muse\gm-reels`.

| id | What it is | Key props |
|---|---|---|
| `F2C` | Face-to-camera conversion reel | `src`, `segments[]` (jump cuts), `clipSec`, `durationSec`, `hook{lines,accent,accentFromSec,endSec,y}`, `words[]` (Remotion Caption format), `captionsFromSec`, `cta{fromSec,kicker,keyword,promise}`, `objectY`, `focusY`, `punches[]`, `fill` |
| `HotTake` | 7s b-roll take, multiple sources | `shots[{src,fromSec,durSec}]`, `cards[{lines,accent,durSec}]`, `footer`, `scrim` |
| `Shop` | TikTok Shop shoppable video, built 30 Sep | everything F2C takes, plus `intro{src,fromSec,durSec}`, `disclosure{text,fromSec,toSec}`, `note{}` for "Results may vary", `captionsY` |
| `CesaHook` | Cesa lane, separate project `cesa-hook-02` | `clip`, `hook`, `subhook`, `handle`, `durationSec` |
| `ClubTarget` | older Club Target composition | see below, this is where your `isClubTarget` flag should go |

Club Target cuts have **not** been going through the `ClubTarget` composition lately. The
4 cuts built 30 Sep were assembled by `D:\GM-Work\build_collage.py` from a JSON spec, with
`#TargetPartner` in the title card's `tags` field and again in the mid-roll pills.

## 3. Render command and timing

Bundles are pre-built per lane so a render does not re-bundle:
`build-conv` (public dir `public-conv`), `build-hot`, `build-shop`.

```
node node_modules/@remotion/cli/remotion-cli.js render build-conv F2C <out.mp4> \
  --props=props-<slug>.json --frames=<s>-<e> --muted --concurrency=1 \
  --offthreadvideo-cache-size-in-bytes=150000000
```

**Always chunked, always `--muted`.** Audio is rebuilt with ffmpeg afterwards and muxed.

**Timing, measured today on a 29.4s / 882-frame 1080x1920 cut: about 20 minutes**, in 8
chunks of 120 frames, with 2 chunks failing on the first attempt and passing on retry.

**The constraint is RAM, not CPU.** The machine has 7.66 GB total. Today it had **0.33 GB
free with 18.58 GB committed**, and the first render died with
`Failed to load image with src [object Object]` and a compositor crash. What fixed it:
clearing `D:\render-tmp` (1057 items, +0.6 GB) and killing orphaned `chrome-headless-shell`
processes (+0.1 GB). **Source bitrate matters too:** a crf-20 assembly at 52 MB killed the
render; re-encoding the same footage at `-crf 24 -maxrate 8M` (23 MB) rendered fine.

So: do not assume a render is quick or reliable. Budget 20-30 minutes per 30s cut and
expect retries.

## 4. Where finished renders land

`D:\Claude Projects\GM-Ready-To-Post\`, numbered, each with a `.md` sidecar carrying the
source clips, the cut structure, the audio measurement, the compliance call, and the
per-platform captions. Current head of the series is `36_loosies-cedar-rapids`.

## 5. Blotato access: YES. The loop is already closed.

This laptop session has full Blotato MCP access and has used it all week:
`blotato_create_presigned_upload_url`, `blotato_create_post`, `blotato_list_posts`,
`blotato_delete_schedule`, `blotato_list_automations`, `blotato_update_automation`.

Worked end to end today and this week: render → presigned upload → `curl PUT` →
byte-verify the hosted file → `create_post` → read back by caption. **Your fallback of
generating a presigned URL from the cloud side is not needed.**

Two notes on your gotchas:
- Your `blotato_update_schedule` re-host warning is consistent with what this side sees.
  The verification used here is stronger than a URL check: **compare the hosted
  `Content-Length` (or a `Content-Range` total from a range read) to the local byte count**,
  and confirm the first bytes contain `ftyp`. A range read also catches your dead-URL case.
- `blotato_list_posts` output regularly exceeds the inline limit and lands in a file.
  Parse it, never read it whole.

## 6. Automatic vs. hand-edited, which is the line you asked about

**Automatic in the pipeline:** jump cuts from a recipe, word-synced captions remapped
through the cuts, hook and CTA cards, blurred-fill compositing for off-shape sources,
music bed with sidechain duck, loudness normalisation, full-decode frame verification,
hosting, byte verification, scheduling, and read-back.

**Hers by hand, in the Edits app:** anything she edits on the phone before it is pulled.
Two examples found today: `2026-09-27-135513856` (lip gloss, burned-in text) and
`2026-08-14-141430297` (Scratch Cupcakery, 73s, her own text cards). **These arrive as
finished videos with text already burned in**, so the pipeline must not re-caption them,
and they are easy to mistake for raw footage. Check for burned-in text before cutting.

**Also hers by hand, and only hers:** posting anything that needs a TikTok Shop product
card. Blotato's TikTok `create_post` has no product-anchor field, so shop videos are
rendered here and posted by her in the app.

---

## What I found today that you could not see

**Loosie's is actually LOOSIES.** Read off the sign in her own footage. The menu board
shows `LOOSIESCR.COM` and a Facebook handle `LOOSIESCR`, and the sandwich is "a Loosie".

**Cut and delivered:** `36_loosies-cedar-rapids.mp4`, 29.4s, 1080x1920, 882/882 frames by
full decode, -13.5 LUFS. Her verdict, 8 out of 10, is on frame 1 per your hook guidance.
Two audio masters exist because her instruction today and your section 5 conflict; see
"one correction" below. On her review page, not scheduled.

**The missing food reviews, searched across D:, OneDrive and Documents:**

| Review | Status |
|---|---|
| Scratch Cupcakery | **FOUND.** 5 raw b-roll clips (40s total) in `ClubTarget\01_RAW_INSTORE`, dated 14 Aug, plus `2026-08-14-141430297.mp4`, a 73s video **she already edited** with her own hook: "I paid $7.76 to drink a cupcake… was it worth it?" Exterior sign reads `scratch cupcakery`. It was filed under ClubTarget and excluded from Target work as "a bakery, not Target", which is why it never surfaced. It is a complete review waiting on a recut. |
| Sidecar Cafe | **Not found.** No folder, file or note anywhere on the drives. |
| Rico Tacos | **Not found.** Same. |

So the pillar is 3 of 6, not 2 of 6, and the third one is nearly finished.

**The Cedar Rapids Target run, verified against your list:** holiday creep (Christmas trees
and red ribbon on the same shelf run as the orange pumpkins), Bullseye Playground, Beauty
Studio including the lit sign, and toys (LEGO, LEGO City, Nintendo, Jurassic World, Hot
Wheels, NBA Ballers, plush wall) are all present. **Food endcaps are not in the 16 Target
clips.** A Barbie endcap and women's apparel mannequins are there and were not on your list.

---

## Two corrections to the handoff

**1. The "0% because of the disclosure" theory does not survive this week's data.**
Her points went **955 → 1,041** between 27 and 30 Sep, and `tt7`, `0q2e` and `0q2b` all read
"Awaiting approval" in the portal. Claims are being approved. The disclosure gap you found
in the 10-12 Sep samples is real and worth closing on its own merits, because it is Target's
stated requirement, but it is not what is zeroing the board. Something else is.

Also: **her recent renders already pass.** The 4 cuts built 30 Sep (Beauty Studio, Pet's Day,
Wrangler, Fall Finds) and the cozy post all carry `#TargetPartner` on screen early and again
at the midpoint. The failures you sampled predate that practice. Building it into the
composition is still the right fix, to stop it regressing.

**2. The audio rule needs a carve-out for clips where she is talking.**
Your section 5 reasons from the Amigos master, which genuinely has no speech. But she
instructed this session directly today: *"we can actually do a little music over the shots
of the restaurant itself, and then we can keep me talking on focus and use what I say while
I'm talking for the on-screen text."*

Loosie's has 81 seconds of her talking. Rendering it silent would throw away the review.
So the rule as applied here is: **her voice is never discarded; store and room ambience
still is.** Both masters were delivered so she can settle the default. Your rule 3, "if she
hands you a voice memo, drop it in natively", already points this way; her face-to-camera
audio is that voice memo.
