#!/usr/bin/env bash
# Turn landscape footage into a 1080x1920 VP9 master the renderer can use.
#
# Landscape phone footage cannot be full-bleed in a 9:16 reel without losing
# most of the frame, and a fixed centre crop loses the subject as soon as she
# moves. track-vertical.py works out where she is; this applies that path.
#
#   python3 track-vertical.py "$SRC" --out tracks/cesa-grass-1-v.json
#   bash make-vertical.sh "$SRC" tracks/cesa-grass-1-v.json clips/cesa-grass-1-v.webm
#
# VP9 because Playwright's Chromium has no H.264 decoder and fails silently,
# rendering every frame with an empty plate. See prep-clips.sh.
#
# The output is a real clip like any other: probe it into the library with
# MediaState=local and bind it by clip_id. Nothing downstream needs to know it
# was ever landscape.
set -euo pipefail

SRC="${1:?usage: bash make-vertical.sh <source> <track.json> <out.webm>}"
TRACK="${2:?track json from track-vertical.py}"
OUT="${3:?output .webm}"
FFMPEG="${FFMPEG:-ffmpeg}"
HERE="$(cd "$(dirname "$0")" && pwd)"
. "$HERE/../filing-system/scripts/gm_py.sh"   # sets $PY

# A keyframe every half second is plenty for a pan this slow, and it keeps the
# filter expression short enough to pass on a command line.
EXPR="$("$PY" - "$TRACK" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
fps, left = d["fps"], d["left"]
step = int(fps * 0.5)
keys = [(i / fps, left[i]) for i in range(0, len(left), step)]
last = (len(left) - 1) / fps
if keys[-1][0] < last:
    keys.append((last, left[-1]))
terms = ["%.1f" % keys[0][1]]
for (t0, v0), (t1, v1) in zip(keys, keys[1:]):
    if t1 <= t0:
        continue
    terms.append("(%.4f*clip(t-%.3f,0,%.3f))" % ((v1 - v0) / (t1 - t0), t0, t1 - t0))
print("+".join(terms))
PY
)"
WIN="$("$PY" -c "import json,sys; print(json.load(open(sys.argv[1]))['window'])" "$TRACK")"
SRC_H="$("$PY" -c "import json,sys; print(json.load(open(sys.argv[1]))['src'][1])" "$TRACK")"

mkdir -p "$(dirname "$OUT")"
# unsharp is not a look, it is compensation: a 486px window blown up to 1080
# wide is a 2.2x upscale and softens without it.
"$FFMPEG" -y -loglevel error -i "$SRC" \
  -vf "crop=${WIN}:${SRC_H}:'${EXPR}':0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.5:5:5:0.0" \
  -c:v libvpx-vp9 -deadline good -cpu-used 3 -crf 31 -b:v 0 -an \
  "$OUT"
echo "wrote $OUT"
