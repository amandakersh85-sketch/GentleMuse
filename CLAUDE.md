# GentleMuse — house rules for any AI working in this repo

This repo is the shared workspace for Amanda's systems: the filing engine, the
SOPs, and the skill packs her AI assistants run against. Anything that is meant
to be repeatable lives here, so every assistant is working from the same copy.

## Everything repeatable ships as a pull request

**A new SOP, a new skill, or a change to an existing one is never committed
straight to `main`.** It goes on a branch and opens a PR.

This is not ceremony. The PR page is the only place the whole change is visible
in one view: what was added, why, and what was verified. It is the record
Amanda reads, and it is what keeps every assistant aligned on one version of
the truth rather than each one carrying its own.

That covers:

- a new SOP, or an edit to one
- a new skill, or a change to how an existing skill behaves
- any script, gate or check that other work depends on
- any change to this file

Small one-off fixes and typos can go straight in. If it will be run more than
once, it is a PR.

## Fixes go at the level the problem lives

When something goes wrong twice, written guidance is not the fix. Guidance
governs judgment, and judgment is what already failed. Find the missing data,
the missing field, or the missing check, and add that instead.

Run 6 is the worked example. Captions kept landing on the wrong clips. The
cause was that the clip inventory recorded no description of what was visible
in a clip, so the pairing step had nothing to pair on. The fix was the missing
column plus a gate that refuses to ship without it, not a reminder to be
careful.

## Verify before claiming

Anything shipped here is run before it is called done. If it could not be run,
say so plainly and say what was checked instead. Tests live next to the thing
they test. `bash filing-system/tests/run-tests.sh`.

## Safety rules that do not bend

1. **Propose-only by default.** Nothing moves without an explicit execute flag.
2. **Nothing deletes.** Execute moves to `_QUARANTINE`. Amanda empties it.
3. **HOLD is never automated.** Sensitive material is held, never auto-routed.
4. **Approval is the gate.** Machine verdicts are proposals. Amanda decides.
5. **No substitution.** When the right input is missing, say so and stop. Do
   not reach for the nearest thing that fits the slot.

## Voice

Anything written for Amanda's audience follows the Gentle Muse voice: calm,
specific, emotionally precise. No hype, no generic motivation, no em dashes, no
spelled-out numbers. When in doubt, run it through `post-grader` and do not
ship below 8 out of 10.
