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
| `reel-footage.html` | The same composition with a real clip behind the type. |
| `reels-footage.json` | A footage-backed payload. `clip.file`, `clip.start`, `clip.push`. |
| `prep-clips.sh` | Converts source footage to VP9 WebM. Required, see below. |

## Run it

```
npm i ffmpeg-static playwright          # or use an existing chromium
export FFMPEG=./node_modules/ffmpeg-static/ffmpeg
node build.mjs . [FACT_ID]              # omit the id to render every reel
REELS=reels-vo.json node build.mjs .    # render the voiced timing instead

bash prep-clips.sh /path/to/footage ./clips      # once, per batch of footage
COMP=reel-footage.html REELS=reels-footage.json node build.mjs .
```

Voiceover, entirely local, via Kokoro-82M:

```
pip install kokoro-onnx soundfile
npm i hyperframes
python3 vo.py . "$(which hyperframes)"
```

`vo.py` prints a fit table: spoken duration against the room each beat has.
Anything marked TIGHT means the line is longer said than shown.

## Two things that will waste your afternoon if you don't know them

**Playwright's Chromium has no H.264 decoder.** It is the open-source build. A
phone MP4 fails with `DEMUXER_ERROR_NO_SUPPORTED_STREAMS`, the `<video>` never
fires `loadedmetadata`, and every frame renders with an empty plate. There is no
error in the render log, only a silent black background. Run `prep-clips.sh`
first and work in VP9 WebM.

**Chromium will not load `file://` media from a `file://` page.** `build.mjs`
serves the project directory over loopback with byte-range support for exactly
this reason. Do not switch it back to `file://` paths.

Footage renders are slower than typographic ones, roughly 330 seconds against
140 for an 18 second reel, because every frame seeks the video and waits for the
decode.

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

Bind. `reel-footage.html` renders whatever clip a payload points at, and it does
not check that the clip shows what the line says. That is Run 6's job, and the
binding gate still has to pass before a footage-backed payload is built.
