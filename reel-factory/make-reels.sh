#!/usr/bin/env bash
# make-reels.sh — footage folder in, finished reels out.
#
# Run this on the machine that actually holds the footage. The cloud session
# that built this pipeline cannot: Drive's hosts are blocked from it, and the
# Drive connector returns file bytes into the conversation rather than onto a
# disk. Everything else was built and tested there. This is the last mile.
#
#   bash make-reels.sh ~/Footage/cesa
#
# What it does, in order:
#   1. transcodes your clips to VP9 WebM        (Chromium cannot decode H.264)
#   2. probes each one into clip-library.csv    (the gate needs real durations)
#   3. stops if any clip has no Shot line       (Run 6, the substitution ban)
#   4. runs the binding gate                    (Run 6, refuses a mismatch)
#   5. renders every payload that passed
set -euo pipefail

SRC="${1:?usage: bash make-reels.sh <footage-dir> [payloads.json]}"
PAYLOADS="${2:-reels-footage.json}"
HERE="$(cd "$(dirname "$0")" && pwd)"
CLIPS="$HERE/clips"
LIB="$HERE/clip-library.csv"
FFMPEG="${FFMPEG:-ffmpeg}"
FFPROBE="${FFPROBE:-ffprobe}"

command -v node >/dev/null || { echo "node is required"; exit 1; }
command -v "$FFMPEG" >/dev/null || { echo "ffmpeg not found. Set FFMPEG=/path/to/ffmpeg"; exit 1; }

echo "== 1. prepping footage =="
FFMPEG="$FFMPEG" bash "$HERE/prep-clips.sh" "$SRC" "$CLIPS"

echo
echo "== 2. probing into the library =="
python3 - "$CLIPS" "$LIB" "$FFPROBE" <<'PY'
import csv, json, os, subprocess, sys
clips, lib, ffprobe = sys.argv[1], sys.argv[2], sys.argv[3]
COLS = ["ClipID","File","DurationSec","Resolution","Orientation",
        "Shot","Mood","Tags","Described"]
existing = {}
if os.path.exists(lib):
    with open(lib, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            existing[row["ClipID"]] = row          # never clobber a Shot line
rows = []
for name in sorted(os.listdir(clips)):
    if not name.lower().endswith(".webm"):
        continue
    path = os.path.join(clips, name)
    w = h = 0; dur = 0.0
    try:
        out = subprocess.run([ffprobe, "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height:format=duration",
            "-of", "json", path], capture_output=True, text=True)
        meta = json.loads(out.stdout or "{}")
        st = (meta.get("streams") or [{}])[0]
        w, h = st.get("width", 0), st.get("height", 0)
        dur = float((meta.get("format") or {}).get("duration") or 0)
    except (FileNotFoundError, ValueError, json.JSONDecodeError):
        # ffmpeg-static ships no ffprobe. ffmpeg -i tells us the same things.
        import re
        err = subprocess.run([os.environ.get("FFMPEG", "ffmpeg"), "-i", path],
                             capture_output=True, text=True).stderr
        m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
        if m:
            dur = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
        m = re.search(r"Video:.*?, (\d+)x(\d+)", err)
        if m:
            w, h = int(m.group(1)), int(m.group(2))
    if not dur or not w:
        print("  could not read %s, skipping" % name); continue
    cid = os.path.splitext(name)[0]
    prev = existing.get(cid, {})
    rows.append({"ClipID": cid, "File": "clips/" + name,
                 "DurationSec": round(dur, 2),
                 "Resolution": "%dx%d" % (w, h),
                 "Orientation": "Vertical" if h > w else "Horizontal",
                 "Shot": prev.get("Shot", ""), "Mood": prev.get("Mood", ""),
                 "Tags": prev.get("Tags", ""),
                 "Described": prev.get("Described", "no")})
with open(lib, "w", newline="", encoding="utf-8") as fh:
    w_ = csv.DictWriter(fh, fieldnames=COLS); w_.writeheader(); w_.writerows(rows)
described = sum(1 for r in rows if (r["Shot"] or "").strip())
print("  %d clips probed, %d described" % (len(rows), described))
if described < len(rows):
    print()
    print("  STOP. %d clip(s) have no Shot line." % (len(rows) - described))
    print("  Open %s and write one plain sentence per clip describing what is" % lib)
    print("  literally visible. Not the mood. Not the caption it might carry.")
    print("  Then set Described to yes and run this again.")
    print()
    print("  This is the substitution ban. An undescribed clip cannot be checked")
    print("  against a caption, so it does not get bound to one.")
    sys.exit(3)
PY

echo
echo "== 3. binding gate =="
GATE="$HERE/../filing-system/scripts/gm_bind_check.py"
if [ -f "$GATE" ]; then
  python3 "$GATE" --render "$HERE/$PAYLOADS" --library "$LIB" || {
    echo "Gate did not pass. Nothing renders."; exit 1; }
else
  echo "  gm_bind_check.py not found, skipping. Check the bindings by hand."
fi

echo
echo "== 4. rendering =="
FFMPEG="$FFMPEG" COMP=reel-footage.html REELS="$PAYLOADS" node "$HERE/build.mjs" "$HERE"

echo
echo "Done. MP4s are in $HERE."
echo "Nothing has been scheduled or posted. Approval is still the gate."
