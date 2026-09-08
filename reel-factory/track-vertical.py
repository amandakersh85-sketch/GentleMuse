#!/usr/bin/env python3
"""Track the subject in landscape footage and emit a 9:16 crop path.

Why this exists
---------------
Phone footage that was shot landscape cannot be full-bleed in a 9:16 reel
without throwing away most of the frame. cesa-grass-1 is 1920x864, so the
tallest 9:16 window inside it is 486 wide: 25 percent of the picture. A fixed
centre crop loses the subject the moment she walks, and a reel that cuts the
dog's head off is not shippable.

This finds her per frame and writes a slow pan that keeps her head in shot.
Pair it with make-vertical.sh, which turns the track into a real 1080x1920
master the renderer can use like any other clip.

What it cannot do
-----------------
It cannot make the subject fit. On cesa-grass-1 she is a median 488px wide
against a 486px window, so for most of the clip some of her is outside the
frame no matter where the window sits. The honest fix for that is to reshoot
vertically. This gets the head in frame about 95 percent of the time, which is
enough for a backup cut, not a substitute for shooting it right.

Detection is deliberately dumb and dependency-light: the subject is much darker
than concrete and is not green, and her ear tips are the top of the silhouette,
which is a far more reliable head anchor than the centre of her mass.

  python3 track-vertical.py <source.mp4> --out tracks/<slug>.json
"""
import argparse
import json
import os
import subprocess
import sys

import numpy as np

SMALL_W, SMALL_H, FPS = 240, 108, 10


def sample(path, ffmpeg):
    """Decode the clip once, small and in RGB, for analysis only."""
    out = subprocess.run(
        [ffmpeg, "-v", "error", "-i", path,
         "-vf", f"fps={FPS},scale={SMALL_W}:{SMALL_H}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True)
    raw = np.frombuffer(out.stdout, dtype=np.uint8)
    n = raw.size // (SMALL_W * SMALL_H * 3)
    if n == 0:
        sys.exit("track-vertical: decoded no frames from %s" % path)
    return raw[:n * SMALL_W * SMALL_H * 3].reshape(n, SMALL_H, SMALL_W, 3).astype(np.float32)


def locate(frames):
    """Per frame: the subject's horizontal extent, and where her head is."""
    n = len(frames)
    lum = frames.mean(axis=3)
    green = frames[..., 1] - (frames[..., 0] + frames[..., 2]) / 2
    head = np.zeros(n)
    left = np.zeros(n)
    right = np.zeros(n)
    for i in range(n):
        dark = lum[i] < np.percentile(lum[i], 20)
        mask = dark & (green[i] < 8)          # dark, and not grass
        mask[:int(SMALL_H * 0.08)] = False    # the top strip is shaded lawn
        col = np.convolve(mask.sum(axis=0).astype(np.float32),
                          np.ones(3) / 3, mode="same")
        if col.max() < 2:                     # lost her; hold the last reading
            head[i] = head[i - 1] if i else SMALL_W / 2
            left[i] = left[i - 1] if i else 0
            right[i] = right[i - 1] if i else SMALL_W
            continue
        idx = np.flatnonzero(col > max(2.0, col.max() * 0.30))
        run = max(np.split(idx, np.flatnonzero(np.diff(idx) > 2) + 1), key=len)
        lo, hi = run[0], run[-1]
        left[i], right[i] = lo, hi
        body = mask[:, lo:hi + 1]
        tops = np.where(body.any(axis=0), body.argmax(axis=0), SMALL_H + 1)
        if (tops <= SMALL_H).sum() == 0:
            head[i] = (lo + hi) / 2
            continue
        ears = np.flatnonzero(tops <= tops.min() + 2)   # the silhouette apex
        head[i] = lo + ears.mean()
    return head, left, right


def smooth(a, frames):
    win = int(frames) | 1
    pad = win // 2
    return np.convolve(np.pad(a, pad, mode="edge"), np.ones(win) / win, mode="valid")


def build(head, left, right, src_w, win, lead, head_smooth, path_smooth, max_px_s):
    body = (left + right) / 2
    h = smooth(head, FPS * head_smooth)
    side = np.sign(smooth(h - body, FPS * 2))
    side[side == 0] = 1                        # keep looking room ahead of her
    target = smooth(smooth(h - side * (win * lead), FPS * path_smooth), FPS * 1.5)
    want = np.clip(target - win / 2, 0, src_w - win)
    step = max_px_s / FPS
    out = np.empty(len(want))
    out[0] = want[0]
    for i in range(1, len(want)):              # a pan that cannot lurch
        out[i] = out[i - 1] + np.clip(want[i] - out[i - 1], -step, step)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--out", required=True)
    ap.add_argument("--ffmpeg", default=os.environ.get("FFMPEG", "ffmpeg"))
    ap.add_argument("--ffprobe", default=os.environ.get("FFPROBE", "ffprobe"))
    ap.add_argument("--lead", type=float, default=0.06)
    ap.add_argument("--head-smooth", type=float, default=1.0)
    ap.add_argument("--path-smooth", type=float, default=1.5)
    ap.add_argument("--max-pan", type=float, default=140.0, help="source px per second")
    a = ap.parse_args()

    meta = json.loads(subprocess.run(
        [a.ffprobe, "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "json", a.source],
        capture_output=True, text=True).stdout or "{}")
    st = (meta.get("streams") or [{}])[0]
    src_w, src_h = st.get("width"), st.get("height")
    if not src_w or src_h >= src_w:
        sys.exit("track-vertical: %s is %sx%s, which is not landscape. Nothing to do."
                 % (a.source, src_w, src_h))
    win = int(round(src_h * 9 / 16))
    if win > src_w:
        sys.exit("track-vertical: %s is not wide enough for a 9:16 window." % a.source)

    frames = sample(a.source, a.ffmpeg)
    head, left, right = locate(frames)
    scale = src_w / SMALL_W
    head, left, right = head * scale, left * scale, right * scale
    pan = build(head, left, right, src_w, win,
                a.lead, a.head_smooth, a.path_smooth, a.max_pan)

    edge = 40
    held = ((head >= pan + edge) & (head <= pan + win - edge)).mean()
    width = right - left
    covered = np.clip(np.minimum(right, pan + win) - np.maximum(left, pan), 0, None)
    visible = covered / np.maximum(width, 1)

    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump({
        "source": os.path.basename(a.source),
        "src": [src_w, src_h],
        "window": win,
        "fps": FPS,
        "left": [round(float(v), 1) for v in pan],
        "measured": {
            "head_in_frame": round(float(held), 4),
            "median_subject_visible": round(float(np.median(visible)), 4),
            "subject_wider_than_window": round(float((width > win).mean()), 4),
        },
    }, open(a.out, "w"), indent=1)

    print("source            %dx%d, 9:16 window is %d px of %d" % (src_w, src_h, win, src_w))
    print("head in frame     %.1f%%" % (held * 100))
    print("subject visible   %.1f%% (median)" % (np.median(visible) * 100))
    print("wider than window %.1f%% of frames" % ((width > win).mean() * 100))
    print("pan travel        %.0f px" % np.abs(np.diff(pan)).sum())
    print("wrote             %s" % a.out)


if __name__ == "__main__":
    main()
