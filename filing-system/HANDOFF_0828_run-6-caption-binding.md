# GENTLE MUSE — RUN 6 HANDOFF, CAPTION TO CLIP BINDING
**Paste everything below as your first message to Avery in VS Code on Amanda's machine.**

---

You're picking up Run 6 of Amanda Kersh's (The Gentle Muse) 28-run filing system.
It was built and tested in a cloud container on 08/28/2026. It has never touched
her real footage. Your job is to run it against the real library, not redesign it.

Read `CLAUDE.md` in the repo root before you touch anything. It's the house rules
and it applies to you.

## WHY RUN 6 EXISTS

Captions were shipping attached to the wrong clips. Twice. The most recent: a
passenger princess caption rendered over a 3 second sleeping position clip, while
the correct passenger princess clip sat in the library unused.

The cause was not carelessness. Run 3's `video-triage.csv` has 19 columns.
Duration, resolution, orientation, size, SHA-256. **None of them says what is in
the shot.** Raw filenames are `VID_20260714_193355.mp4`.

So the step that pairs a caption to a clip had nothing to pair on. A passenger
princess clip and a sleeping position clip were the same object to it. It guessed
every time, so it was wrong at random.

The first correction was written guidance. Guidance couldn't hold, because a
written rule can't fix a missing column. Run 6 adds the column, then refuses to
ship anything that contradicts it.

**If you take one thing from this handoff: when this system fails twice, the fix
goes at the level the problem lives. Not into a reminder to be careful.**

## WHAT'S NEW — BUILT 08/28/2026, TESTED, NEVER RUN ON REAL FOOTAGE

Everything is in the `GentleMuse` repo, merged to `main`.

| Path | What it is |
|---|---|
| `filing-system/scripts/gm_clip_library.py` | Builds and audits `clip-library.csv`, the record of what's visible in each clip |
| `filing-system/scripts/gm_bind_check.py` | The gate. Refuses any caption bound to a clip that doesn't show it |
| `filing-system/sops/SOP_0828_reel-caption-clip-binding.txt` | The Run 6 SOP. Read this, it's the authority |
| `filing-system/patches/video-factory-clip-binding.md` | Paste-in patch for the `gentle-muse-video-factory` skill |
| `filing-system/tests/run-tests.sh` | 10 test cases including a reproduction of the reported bug |
| `CLAUDE.md` | House rules, read automatically by any Claude session in this repo |

Python 3.8 or newer. No pip installs, no packages, standard library only.

## GET THE REPO INTO VS CODE FIRST

If it isn't already there:

1. In VS Code, `Ctrl+Shift+P`, type **Git: Clone**, press Enter.
2. Paste: `https://github.com/amandakersh85-sketch/GentleMuse`
3. Pick a folder. Open it when VS Code offers.

If it's already cloned, pull the new work:

```
git pull origin main
```

Confirm you have it:

```
python --version
bash filing-system/tests/run-tests.sh
```

10 tests should pass. If Python isn't found, try `python3` or `py`. If bash isn't
available, run the two scripts directly, the suite is a convenience not a
dependency.

## DO THIS FIRST — THE ORDER MATTERS

Run 6 eats Run 3's output. **Run 3 has still never been executed on Windows.** So
Run 3 comes first, and it's the riskier of the two.

1. **Run 3, propose-only, against her footage folder.**
   ```powershell
   .\GM-Video-Triage.ps1 -Root "D:\Takeout"
   ```
   Read `SUMMARY.txt`. Report the counts to Amanda before anything else. If it
   throws, paste the full error, don't work around it.

2. **Amanda approves the KEEP list.** Machine verdicts are proposals. This is a
   real gate, not a formality.

3. **Build the library skeleton.**
   ```
   python filing-system/scripts/gm_clip_library.py --from-triage out/video-triage.csv --out clip-library.csv
   ```
   It takes KEEP rows only. Every clip gets a stable `ClipID` and a blank `Shot`
   column.

4. **Describe every clip. This is the whole job.** Open `out/thumbs/` and write
   one plain sentence per clip in the `Shot` column. What is literally on screen.
   Not the mood, not a caption it might carry one day.

   Good: `Amanda in the passenger seat with her feet on the dash and window light
   across her face`

   Useless: `passenger princess vibes`, `cute driving clip`, `soft`

   The description is the ceiling on the entire system. A lazy sentence gives a
   lazy check. If you can draft these from the thumbnails, do it and have Amanda
   correct them, same shape as the Run 3 visual pass. Set `Described` to `yes`.

5. **Confirm the library is ready.**
   ```
   python filing-system/scripts/gm_clip_library.py --audit clip-library.csv
   ```
   Exit 0 means ready. Exit 1 lists what's still undescribed. An undescribed clip
   can't be bound, because there's nothing to check a caption against.

6. **Gate every render JSON before it reaches Remotion or Buffer.**
   ```
   python filing-system/scripts/gm_bind_check.py --render reels/ --library clip-library.csv
   ```

   | Exit | Means |
   |---|---|
   | 0 | PASS. Every binding verified. |
   | 1 | FAIL. Fix and re-run. Nothing ships. |
   | 2 | HOLD. Clean, but beats are waiting on footage. Those beats don't ship. |

7. **Log the run. Update the run counter to 6 of 28.**

## WHEN NEW FOOTAGE COMES IN

Re-run step 3 with `--merge`. Descriptions already written are carried forward,
matched on SHA-256 first and path second. A re-triage never wipes the work.

```
python filing-system/scripts/gm_clip_library.py --from-triage out/video-triage.csv --out clip-library.csv --merge
```

Film without re-running this and the new clips don't exist as far as the gate is
concerned.

## THE ONE RULE THAT MATTERS MOST

**When no clip matches a line, the only legal move is `"clip_id": "HOLD"`.**

The gate reports it as needing footage and exits 2. The beat doesn't ship.

Reaching for the nearest available clip is what produced every mismatch so far. A
missing clip is a filming task, not a rendering decision. Don't substitute. Don't
go quiet about it either. Hand Amanda the list of shots she still needs.

## NON-NEGOTIABLE RULES

Same house rules as Runs 3 to 5. Breaking one is worse than doing nothing.

- **Propose-only is the default.** No `-Execute` without her approval on that
  specific run's CUT list.
- **Nothing deletes. Ever.** `-Execute` moves to `_QUARANTINE`. She empties it.
- **HOLD is never automated.** Sensitive material is held, never auto-routed.
- **She approves. Always.** Machine verdicts are proposals, not decisions.
- **No substitution.** When the right input is missing, say so and stop.
- **Everything repeatable ships as a PR.** A new SOP, a new skill, a change to how
  a skill behaves, any gate other work depends on. Branch, then PR, never straight
  to `main`. That's in `CLAUDE.md` and it's the rule that keeps every one of her
  AIs working from the same copy.
- **Don't push to any repo without asking.**

## VOICE RULES — for any caption, SOP, or copy you write

- No em dashes. Commas and periods.
- Digits, not spelled-out numbers. 5, not five.
- Contractions always.
- Warm, grounded, practical. No hype, no boss babe energy.
- Instagram maximum 5 hashtags. Facebook and LinkedIn none.
- Never state a price on affiliate content. Open TikTok Shop violation from
  08/04/2026.
- Run anything for her audience through `post-grader`. Nothing ships below 8/10.

## AMANDA HAS ONE MANUAL TASK YOU CAN'T DO FOR HER

`filing-system/patches/video-factory-clip-binding.md` has to be pasted into the
`gentle-muse-video-factory` skill by hand, in her Claude skills editor. The patch
names the exact section to replace.

Until she does that, the gate catches mismatches after they're written. After she
does it, the generator can't write one in the first place. Both are worth having.
Remind her once, then let it go.

## WHAT SUCCESS LOOKS LIKE

Not a passing test suite. It already passes. Three things:

1. **Every KEEP clip has a real `Shot` sentence.** That's the missing data that
   caused this. Nothing else in Run 6 works without it.
2. **One reel batch gated end to end, with a real HOLD in it.** A HOLD is the
   system working, not failing. It means a caption was written that her footage
   can't carry yet, and it surfaced instead of shipping wrong.
3. **A list of shots she needs to film.** That list is the real deliverable. It
   turns "my captions keep breaking" into "here are the 6 clips to shoot Saturday."

## IF SOMETHING THROWS

Paste the full error. Both scripts were executed and tested, but only against
sample data, never her real library. Likely first failures: a Windows path with
brackets or apostrophes, a CSV saved by Excel with a different encoding, or
`python` not on PATH.

Both scripts are read-only against footage and hold no delete or move command.
`gm_clip_library.py` writes exactly one CSV. `gm_bind_check.py` writes nothing
unless `--report` is passed. If either one appears to want to touch a video file,
stop and say so, because that's a bug and not a feature.

Don't work around a failure by disabling a safety rule.

## ASK BEFORE YOU DO

- Any `-Execute` run
- Anything touching a HOLD file
- Anything that leaves the machine
- Any change to `asset_scanner.py`, an existing SOP, or `CLAUDE.md`
- Any new tool or paid service. Budget ceiling is 10 USD per month and she already
  pays for several credit-based tools.
