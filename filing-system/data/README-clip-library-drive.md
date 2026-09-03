# clip-library-drive.csv

The real footage inventory, pulled from Amanda's Google Drive on 08/31/2026.
34 clips, 0.7 GB. This is Run 6 step 2 done against actual files rather than a
hypothetical library.

## Why it stops here

The footage exists and is fully identified, but it cannot reach the render
environment. Both transports are closed:

- `drive.google.com` and `www.googleapis.com` are blocked by the egress proxy
  (000 and 403 respectively).
- The Drive connector returns file content as base64. The smallest Cesa clip is
  17 MB, which is 22.6 million characters, about 5.7 million tokens. Not viable
  for a single file, let alone 34.

So the binding gate still correctly reports HOLD on every beat. Nothing here is
a workaround for that, and nothing should be.

## What unblocks it

Two columns, in this order:

1. `DurationSec`, `Resolution`, `Orientation` — run `ffprobe` over the local
   copies on the Windows machine, or re-run Run 3's `GM-Video-Triage.ps1` and
   merge. The gate needs duration to reject a beat longer than its clip.
2. `Shot` — one plain sentence per clip describing what is literally visible.
   This is the one step nobody else can do. Send the thumbnails and a draft
   comes back for correction, same shape as the Run 3 visual pass.

Set `Described` to `yes` per row as each is written, then:

```
python3 ../scripts/gm_clip_library.py --audit clip-library-drive.csv
python3 ../scripts/gm_bind_check.py --render reels/ --library clip-library-drive.csv
```

## Lanes

26 GM, 5 UNSORTED (raw phone footage, filenames only), 3 CGY (Cesa).

One file in the OF lane was found and deliberately **not** catalogued. House
rule 3: sensitive material is held, never auto-routed. It is excluded from this
CSV entirely and should be filed by hand.

## The three that matter first

`cesa-intro-1080p`, `cesavideo-91320` and `spotlight-on-princesa` are the CGY
lane. Cesa is 27% of all reel views across 75 days, so these are the highest
value rows in the file. Describe them first.
