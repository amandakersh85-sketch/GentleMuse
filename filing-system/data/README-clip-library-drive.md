# clip-library-drive.csv

The real footage inventory, pulled from Amanda's Google Drive on 08/31/2026.
34 clips, 0.7 GB. This is Run 6 step 2 done against actual files rather than a
hypothetical library.

## Why it stops here

The footage exists and is fully identified, but the actual video cannot reach
the render environment:

- The Drive connector returns file content as base64. The smallest Cesa clip is
  17 MB, which is 22.6 million characters, about 5.7 million tokens. Not viable
  for a single file, let alone 34. This is arithmetic, not a permissions
  question, and no connector fixes it.

So the binding gate still correctly reports HOLD on every beat. Nothing here is
a workaround for that, and nothing should be.

What changed 2026-09-03: a `mcp__Google_Drive__search_files` /
`get_file_metadata` connector works in-session and was used to run a full
`owner = 'me'` sweep of every video file in the account, cross-checked against
this CSV row by row. Nothing turned up that wasn't already here. So metadata
(filenames, sizes, dates, folder ids) is reachable now, and re-running that
sweep is the right move before assuming a clip is missing rather than just
unsynced. Content is a different question from metadata and the size math
above still holds regardless of transport — do not read that as "Drive is
open" for the actual video bytes. Earlier notes here said the connector
itself was blocked; that was true when written and is not the current state,
so don't take a stale "egress-blocked" claim on faith without checking again.

## Real footage or the AI twin — the SourceKind column

Amanda, Sep 3: a lot of the descriptive-titled clips are HeyGen generations of
her AI twin, not footage she shot, and the two are not easy to tell apart by
eye — the twin looks like her. Her own inbox pins the timeline (Gmail, HeyGen
notices, read 2026-09-03):

- HeyGen account opened 2026-05-07, first video finished the same day.
- The Instant Avatar (the twin) was built around 2026-06-12.
- "Your Video is Ready" waves: May 7, Jun 12-13, Jun 22, Jun 26-28, Jul 5,
  Jul 11-12, Jul 24, Jul 31, Aug 20. The Jun 12-22 waves match the 21-clip
  descriptive-titled batch that landed in Drive on Jun 23, and the Jul 11-12
  wave lands hours before the three `*_1080p` intro files hit Drive Jul 12.

So the `SourceKind` column: `real` only where arithmetic proves it — captured
before 2026-05-07, when the account did not exist to generate anything.
Everything else is `real?`, `heygen?` or `unknown`, where a trailing `?` is a
machine proposal built from naming and timing evidence. House rule 4 applies:
these are proposals, Amanda confirms, and the CSV records her answer with the
`?` dropped.

What each HeyGen clip actually says is not in the video file — it is the
script she typed, and it lives in her HeyGen library. This environment cannot
reach it: `api.heygen.com` is egress-blocked here and the CLI's OAuth login
needs her browser. Fastest path is the heygen CLI on her own machine
(`heygen auth login --oauth`, then the listing side of `heygen --help` to
export video titles and scripts), dropped into the repo. For the real clips,
transcription runs where the files are — the hyperframes CLI carries a
whisper.cpp transcribe fallback (see
`.claude/skills/media-use/references/setup-providers.md`).

## What unblocks it

After every new Drive sync (phone dumped to laptop, then uploaded), re-run the
sweep above and re-derive dates before doing anything else — new rows land
with only Drive's upload time, which is not when the footage was actually
shot:

```
python3 ../scripts/gm_clip_library.py --derive-dates clip-library-drive.csv
```

Then two columns, in this order:

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

`--audit` sorts the undescribed list by `Captured` (the derived date) oldest
first, so it doubles as the work order: start at the top.

## Lanes

26 GM, 5 UNSORTED (raw phone footage, filenames only), 3 CGY (Cesa).

One file in the OF lane was found and deliberately **not** catalogued. House
rule 3: sensitive material is held, never auto-routed. It is excluded from this
CSV entirely and should be filed by hand.

## The three that matter first

`cesa-intro-1080p`, `cesavideo-91320` and `spotlight-on-princesa` are the CGY
lane. Cesa is 27% of all reel views across 75 days, so these are the highest
value rows in the file. Describe them first.
