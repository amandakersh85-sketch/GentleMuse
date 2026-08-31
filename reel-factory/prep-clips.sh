#!/usr/bin/env bash
# Transcode source footage to VP9 WebM so the renderer can actually decode it.
#
# The Chromium that ships with Playwright is the open-source build. It has no
# H.264 decoder, so a phone MP4 fails with:
#   DEMUXER_ERROR_NO_SUPPORTED_STREAMS: FFmpegDemuxer: no supported streams
# and every frame renders with an empty plate and no error anywhere obvious.
# VP9 in WebM is supported, so everything gets converted once up front.
#
# Usage:  bash prep-clips.sh <src-dir> <out-dir>
set -euo pipefail
SRC="${1:?source directory}"; OUT="${2:?output directory}"
FFMPEG="${FFMPEG:-ffmpeg}"
mkdir -p "$OUT"
shopt -s nullglob nocaseglob
for f in "$SRC"/*.mp4 "$SRC"/*.mov "$SRC"/*.m4v; do
  base="$(basename "${f%.*}")"
  dest="$OUT/$base.webm"
  [ -f "$dest" ] && { echo "skip  $base (already prepped)"; continue; }
  echo "prep  $base"
  "$FFMPEG" -y -loglevel error -i "$f" \
    -c:v libvpx-vp9 -deadline realtime -cpu-used 8 -crf 34 -b:v 0 -an "$dest"
done
echo
echo "Now probe them into the library so the gate can check beat lengths:"
echo "  for f in $OUT/*.webm; do"
echo "    ffprobe -v error -select_streams v:0 \\"
echo "      -show_entries stream=width,height:format=duration \\"
echo "      -of default=nw=1 \"\$f\"; done"
