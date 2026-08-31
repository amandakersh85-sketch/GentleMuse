# Gentle Muse Reel Factory

Renders a finished 9:16 MP4 from a fact in the Run 7 bank. No footage required,
no cloud renderer, no API key. Chromium draws every frame, ffmpeg encodes them.

This exists because the `Delivery` column says 11 of the 50 seeded facts are
`text`, meaning they need nothing filmed. Those are the posts that can ship on a
week when there is no time to film, and this is what ships them.

## What's here

| Path | What it is |
|---|---|
| `reel.html` | The composition. Reads `window.PAYLOAD`, exposes `seek(t)`. |
| `build.mjs` | Renders frames at a fixed fps and encodes to MP4. |
| `vo.py` | Generates a voiceover per beat and reports whether it fits. |
| `reels.json` | The 4 October `text` scripts, 18s each. |
| `reels-vo.json` | One script retimed to measured speech instead of reading pace. |

## Run it

```
npm i ffmpeg-static playwright          # or use an existing chromium
export FFMPEG=./node_modules/ffmpeg-static/ffmpeg
node build.mjs . [FACT_ID]              # omit the id to render every reel
REELS=reels-vo.json node build.mjs .    # render the voiced timing instead
```

Voiceover, entirely local, via Kokoro-82M:

```
pip install kokoro-onnx soundfile
npm i hyperframes
python3 vo.py . "$(which hyperframes)"
```

`vo.py` prints a fit table: spoken duration against the room each beat has.
Anything marked TIGHT means the line is longer said than shown.

## The determinism rule

Everything in the composition is a pure function of `t`. The ember and fog
systems are seeded once and evaluated per frame, never with `Math.random` at
draw time and never with `requestAnimationFrame`. Frame N is identical on every
run, which is what makes the render reproducible and the seek-based pipeline
work at all. Do not add a time-based animation that reads the wall clock.

## Why the atmosphere is drawn rather than downloaded

Every external image host is blocked from the render environment, so a stock
plate cannot be fetched. Drawing it has turned out better anyway: it is unique
to the brand rather than the same library image everyone else is using, it
carries no licence question, and it costs nothing per reel.

## What it does not do

Footage. A reel with Cesa or Amanda in it needs the clip library and Run 6's
binding gate. This handles the `text` lane only.
