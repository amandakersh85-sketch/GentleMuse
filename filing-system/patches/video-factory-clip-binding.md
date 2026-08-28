# Patch — gentle-muse-video-factory, caption-to-clip binding

Applies Run 6 to the skill that generates the reels. Without this patch the
gate still catches mismatches, but only after they are written. With it, the
generator cannot express a mismatch in the first place.

**To apply:** open the `gentle-muse-video-factory` skill and replace the
section titled **"Render JSON conventions"** with everything between the rules
below. Then replace the render JSON block in **"Output format — for every
video"** with the example at the end.

---

## Render JSON conventions

The render JSON is downstream-friendly structured data. Fill it like this:

- **title** — human-readable, e.g. `"Quiet Progress Reel 01"`. If it's a
  numbered batch, use the same prefix across the batch.
- **format** — always `"9:16"` for short-form unless the user requests
  otherwise.
- **duration** — integer seconds; **must equal** the sum of
  `clips[].duration`. Validate before delivering.
- **end_text** — the CTA line shown at the very end.
- **clips** — array of clip objects. Every clip carries five required fields:
  - `clip_id` — **the binding. This is the only identity that counts.** It must
    be a `ClipID` that literally appears in `clip-library.csv`, or the string
    `"HOLD"`. Never bind by file path, category or vibe. A path is not an
    identity, and inventing one breaks the render.
  - `file` — copy the `File` value from that library row, verbatim. Do not
    compose it yourself.
  - `start` — `0` unless trimming into the source clip.
  - `duration` — integer seconds. `start + duration` **must not exceed** that
    row's `DurationSec`. A three second clip cannot carry a nine second line.
  - `text` — the on-screen line for that clip. Sentence case, no end
    punctuation on short statements.
  - `match_reason` — one plain sentence naming what **in that clip's `Shot`
    line** shows what the text says. Not "felt right." Not "matches the vibe."
    If the pairing can't be said in words, it hasn't been made.

### The binding rule

Read the clip's `Shot` description. Read the on-screen text. **They must share
a real content word.** "Passenger princess era" binds to *"Amanda in the
passenger seat with her feet on the dash"* — `passenger` is shared. It does not
bind to *"tangled sheets and a pillow at a strange angle"*, which shares
nothing. That is the whole check, and it is the failure that has shipped twice.

Before binding, scan the **entire library** for the best match, not the first
plausible one. If a clip with more overlap exists, use it. The gate names the
better clip when one is passed over, so passing one over is not survivable.

### The substitution ban

When no clip in the library shows what a line says, the only legal move is:

```json
{"clip_id": "HOLD", "start": 0, "duration": 3, "text": "Candles lit at four in the afternoon"}
```

**Never reach for the nearest available clip.** Substituting a near-miss is how
every mismatch has been produced. A missing clip is a filming task, not a
rendering decision — `HOLD` surfaces it as one. Say it out loud in the delivery
too: list the HOLD beats as shots Amanda still needs to film.

If a whole reel would be HOLD beats, don't ship the reel. Ship the shot list.

### Override, used sparingly

A line can be visually true without sharing a word — discipline over a slow
coffee pour. Add `"override": true` and a `match_reason` that states the
metaphor. If most beats need an override, the library is underdescribed; say so
rather than overriding through it.

### Undescribed clips are not available

A library row with an empty `Shot`, or `Described` set to `no`, cannot be
bound. There is nothing to verify a caption against. Treat those clips as if
they aren't in the library, and say which ones need describing.

### No library in context

If `clip-library.csv` is not in context, **do not invent clip IDs.** Write every
beat as `"clip_id": "HOLD"` with the text filled in, and open the delivery with
one line: *"No clip library in context — every beat is HOLD. Send
clip-library.csv and I'll bind these."* Guessing at file paths is what produces
the mismatch.

### The gate is mandatory

Every batch is verified before it is called done:

```
python3 filing-system/scripts/gm_bind_check.py --render reels/ --library clip-library.csv
```

`FAIL` — fix and re-run. `HOLD` — report the beats that need filming. Nothing
goes to Remotion or Buffer on a FAIL. When the tool can't be run in the current
environment, do the same checks by hand against the library, beat by beat, and
say in the delivery that the check was manual.

---

## Output format — render JSON block

````
**Render JSON:**

```json
{
  "title": "Passenger Princess Reel 01",
  "format": "9:16",
  "duration": 11,
  "clips": [
    {
      "clip_id": "driving-passenger-princess-01",
      "file": "driving/passenger-princess-01.mp4",
      "start": 0,
      "duration": 4,
      "text": "Passenger princess era and completely unbothered",
      "match_reason": "clip shows her in the passenger seat, feet up, window light on her face"
    },
    {
      "clip_id": "HOLD",
      "start": 0,
      "duration": 3,
      "text": "Candles lit at four in the afternoon for no reason"
    }
  ],
  "end_text": "Follow for more Gentle Muse resets"
}
```
````

---

## What "good" looks like

Replace the "Reference only clips/categories that exist..." line with:

- Reference only ClipIDs that exist in Amanda's library — never invent files,
  never fall back to a category guess when no library is in context

Then add:

- Every clip bound by a `ClipID` that exists in the library, with a
  `match_reason` naming what in the shot shows the line
- No beat longer than the clip carrying it
- Missing footage shipped as `HOLD` and listed as shots to film — never
  substituted with a near-miss clip
- The binding gate run, and passing, before the batch is called done
