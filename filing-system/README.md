# Gentle Muse Filing System — Media Triage Modules

Runs 3 through 7 of the 28-run Downloads Maintenance system.

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
| `scripts/gm_holiday_bank.py` | Run 7. Resolves the holiday calendar, audits the fact bank, and builds the content plan. |
| `scripts/gm_holiday_check.py` | Run 7. The gate. Refuses any holiday caption whose history isn't in the bank. |
| `data/holiday-calendar.csv` | Run 7. 14 holidays, their date rules, slots and season windows. |
| `data/holiday-fact-bank.csv` | Run 7. 50 sourced facts, each with the turn that makes it hers and what it needs on screen. |
| `scripts/gm_teardown_check.py` | Run 8. The gate. Refuses a competitor nobody read, and a reel that asks without promising. |
| `data/competitor-teardowns.csv` | Run 8. 8 accounts torn down from their own content, plus 3 leads held as unusable. |
| `sops/SOP_0819_video-triage-run-3.txt` | Run 3 SOP |
| `sops/SOP_0819_photo-triage-run-4.txt` | Run 4 SOP |
| `sops/SOP_0819_document-triage-run-5.txt` | Run 5 SOP |
| `sops/SOP_0828_reel-caption-clip-binding.txt` | Run 6 SOP |
| `sops/SOP_0829_holiday-caption-strategy.txt` | Run 7 SOP |
| `sops/SOP_0901_competitor-teardowns.txt` | Run 8 SOP |
| `patches/video-factory-clip-binding.md` | Paste-in patch for the `gentle-muse-video-factory` skill |
| `patches/holiday-caption-strategy.md` | Paste-in patch for the video factory, `content-coach` and `post-grader` |
| `tests/run-tests.sh` | Regression suite for Runs 6 and 7, 29 cases |

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

## Run 7 — holiday caption strategy

Same shape as Run 6, one layer up. A holiday post makes claims about the past,
and nothing in the chain could tell a checked fact from a confident invention.
Ask any assistant for a creepy historical Halloween fact and it produces one,
dated and specific, whether or not it happened. Amanda loves history and her
audience will come to trust her on it, so a plausible wrong date costs more
than a weak hook.

Run 7 adds the two missing tables and enforces them. A **fact bank**, where
every row carries a source and a `Backbone`, the line that says why the fact
matters. A **holiday calendar**, so season windows and floating dates are
computed rather than remembered. And an **era window**, 1989 to 1999, because
Amanda described the holiday register as a millennial born in 1985 watching the
Disney Channel and Nickelodeon, which is a date range and therefore checkable.

```
python3 scripts/gm_holiday_bank.py --season
python3 scripts/gm_holiday_bank.py --audit
python3 scripts/gm_holiday_bank.py --plan --from 2026-10-01 --to 2026-10-31 --per-holiday 5
python3 scripts/gm_holiday_check.py --post posts/
```

The plan comes back with the fact, the source and the backbone already attached
to each date, which is the part that lets a batch get written without Amanda in
the room. Each row also carries a `Delivery` value (`text`, `broll`, `cesa` or
`face`), so the plan closes with what the batch needs filmed and how many posts
can be finished with no footage at all. 11 of the 50 seeded facts are `text`. The gate refuses anything whose history is not in the bank, whose
nostalgia lands outside the window, or which reports a fact without turning it.
No fact means `HOLD`, never the nearest fact that fits. See the Run 7 SOP.

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

Run 7 written 08/29/2026, before the failure rather than after it. Executed here:
`bash tests/run-tests.sh` now runs 29 cases across Runs 6 and 7, all passing,
including a reproduction of the invented-fact failure. Both scripts are
read-only and hold no delete command. The 50 seeded facts were written from
standard reference works and each row names its source, but they have not been
re-checked against those sources by a second reader. The sources are named so
that pass is possible, and the Run 7 SOP says to do it before the Halloween
batch ships.

## Run 8 — competitor teardowns and the contract

30,671 views produced 13 email subscribers. Views to followers works. Followers
to email does not, and the writing was never the problem.

Eight accounts were torn down from their own transcripts and captions rather
than from anybody's opinion of them. None of them ask for the follow. Every one
states a promise with a frequency or a stance behind it. So a reel payload now
carries a `contract`, and the gate refuses a reel that carries a call to action
without one, or a contract that is a request in disguise.

    python3 scripts/gm_teardown_check.py --bank data/competitor-teardowns.csv
    python3 scripts/gm_teardown_check.py --render ../reel-factory/

Exit `0` pass, `1` fail, `2` hold. The bank separates an account somebody read
from a name in somebody else's roundup, and will not let the second be cited as
the first. Run 8 also taught the Run 6 binding gate to read the reel factory's
payload shape, which it could not do before, so the ten built reels are checked
for the first time.
