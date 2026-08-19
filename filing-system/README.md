# Gentle Muse Filing System — Media Triage Modules

Runs 3, 4 and 5 of the 28-run Downloads Maintenance system.

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
| `sops/SOP_0819_video-triage-run-3.txt` | Run 3 SOP |
| `sops/SOP_0819_photo-triage-run-4.txt` | Run 4 SOP |
| `sops/SOP_0819_document-triage-run-5.txt` | Run 5 SOP |

SOPs are `.txt` on purpose. GitHub renders plain text preformatted, which keeps
the column alignment the house format uses.

## House rules, enforced by every script

1. **Propose-only by default.** Nothing moves without `-Execute`.
2. **Nothing deletes.** `-Execute` moves to `_QUARANTINE`. Amanda empties it.
3. **HOLD is never automated.** Sensitive documents aren't moved, renamed,
   archived, or sent.
4. **Approval is the gate.** Machine verdicts are proposals.

## Output schema

Every module writes CSV columns matching the Master Asset Index, so approved
rows paste straight into the card catalog:

```
Asset Name | Type | Lane | Category / Use | Lives On | Folder / Location | Direct Link | Status | Needs Filing?
```

Lanes: GM, KV, FS, CGY, OF, Personal, UNSORTED.

## Requirements

- Windows PowerShell 5.1 or PowerShell 7
- ffmpeg and ffprobe for durations, dimensions and thumbnails
  (`winget install Gyan.FFmpeg`). Without them the size and duplicate rules
  still run and the scripts say so.

## Status

Written 08/19/2026. Syntax-validated, and confirmed to hold no delete command
against user files. **Not yet executed on a Windows machine.** The first run is
the real test. See each SOP's LIMITS section.
