# Gentle Muse Filing System — Media Triage Modules

Runs 3, 4, 5 and 6 of the 28-run Downloads Maintenance system.

These extend the existing filing engine (`asset_scanner.py`) to media.
They do not replace it. `asset_scanner.py` already handles SHA-256 duplicate
detection and propose-only filing. These modules add what it can't do: read a
video's duration, group a photo burst, or spot a sensitive document.

## What's here

| Path | What it is |
|---|---|
| `HANDOFF_0819_local-execution.md` | Paste this into Claude Code on the local machine to run the system |
| `scripts/GM-Video-Triage.ps1` | Run 3. Footage. Duration, orientation, thumbnails. |
| `scripts/GM-Photo-Triage.ps1` | Run 4. Stills. Burst grouping, screenshots, Takeout sidecars, GPS gate. |
| `scripts/GM-Doc-Triage.ps1` | Run 5. Paper. Version families, entity routing, sensitive HOLD. |
| `scripts/gm_clip_library.py` | Run 6. Builds and audits `clip-library.csv` — what is actually *in* each clip. |
| `scripts/gm_bind_check.py` | Run 6. The gate. Refuses any caption bound to a clip that doesn't show it. |
| `sops/SOP_0819_video-triage-run-3.txt` | Run 3 SOP |
| `sops/SOP_0819_photo-triage-run-4.txt` | Run 4 SOP |
| `sops/SOP_0819_document-triage-run-5.txt` | Run 5 SOP |
| `sops/SOP_0828_reel-caption-clip-binding.txt` | Run 6 SOP |
| `patches/video-factory-clip-binding.md` | Paste-in patch for the `gentle-muse-video-factory` skill |
| `tests/run-tests.sh` | Run 6 regression suite, 10 cases |

SOPs are `.txt` on purpose. GitHub renders plain text preformatted, which keeps
the column alignment the house format uses.

## House rules, enforced by every script

1. **Propose-only by default.** Nothing moves without `-Execute`.
2. **Nothing deletes.** `-Execute` moves to `_QUARANTINE`. Amanda empties it.
3. **HOLD is never automated.** Sensitive documents aren't moved, renamed,
   archived, or sent.
4. **Approval is the gate.** Machine verdicts are proposals.
5. **No substitution.** When no clip matches a caption, the beat is `HOLD` and
   the footage gets filmed. Reaching for the nearest clip is what ships a
   mismatch.

## Output schema

Every module writes CSV columns matching the Master Asset Index, so approved
rows paste straight into the card catalog:

```
Asset Name | Type | Lane | Category / Use | Lives On | Folder / Location | Direct Link | Status | Needs Filing?
```

Lanes: GM, KV, FS, CGY, OF, Personal, UNSORTED.

## Run 6 — caption-to-clip binding

Run 3 records a clip's duration, resolution and hash. It records nothing about
what is *visible* in it, so pairing a caption to a clip had nothing to pair on
and produced mismatches at random. Run 6 adds the missing field and enforces it.

```
python3 scripts/gm_clip_library.py --from-triage out/video-triage.csv --out clip-library.csv
# write one plain sentence per clip in the Shot column, then:
python3 scripts/gm_clip_library.py --audit clip-library.csv
python3 scripts/gm_bind_check.py --render reels/ --library clip-library.csv
```

Exit `0` pass, `1` fail, `2` hold. See the Run 6 SOP for the full check list.
Run 6 is Python, not PowerShell, so it runs and is tested anywhere:
`bash tests/run-tests.sh`.

## Requirements

- Windows PowerShell 5.1 or PowerShell 7 (Runs 3–5)
- Python 3.8+ (Run 6, no third-party packages)
- ffmpeg and ffprobe for durations, dimensions and thumbnails
  (`winget install Gyan.FFmpeg`). Without them the size and duplicate rules
  still run and the scripts say so.

## Status

Runs 3–5 written 08/19/2026. Syntax-validated, and confirmed to hold no delete
command against user files. **Not yet executed on a Windows machine.** The first
run is the real test. See each SOP's LIMITS section.

Run 6 written 08/28/2026 after a caption/clip mismatch shipped twice. Python, so
it was actually executed here: `bash tests/run-tests.sh`, 10 cases including a
reproduction of the reported mismatch, all passing. It reads footage metadata and
writes one CSV; it holds no delete command either. What it has *not* seen is
Amanda's real library — the Shot descriptions don't exist yet, and writing them
is step 3 of the Run 6 SOP.
