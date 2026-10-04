#!/usr/bin/env python3
"""Refuse a video post that carries no sound.

Amanda, 10/04: "it's going out with no sound again. There's ones going out
with no voiceover or no music, and that's not okay."

She was right that silent reels are queued and wrong about which ones, and
nothing in this repo could have told either of us. 133 videos were on the
10/04 board and 6 posts, from 3 distinct assets, had no audio stream at all:
halloweentown-v2 on 10/13 and 10/17 across all 4 accounts, and the Samhain
countdown trailers on 10/27. All 6 are from the 4459xxx batch. The 20 nights
that had actually published all carried the approved bed at -17.4 dB.

Every gate passed those 6. C01 counts posts, C05 counts minutes, C13 counts
nights, C15 counts slots. Not 1 of them opens the file. A silent reel is not
starved, not early, not a repeat and not a collision, so the board read clean
while 6 soundless posts sat in it waiting their turn.

This is the missing check, and it reads the file rather than a column,
because the queue payload says nothing about audio and never will.

  A01_NO_AUDIO_TRACK    the mp4 has no audio track
  A02_AUDIO_UNREADABLE  the container could not be read, so it is not being
                        called clean. No substitution: say so and stop.

Nothing is decoded and nothing is downloaded whole. The audio question is
answered by the moov atom, so the probe asks for the first 64 KB, and only
when moov is not in there, the last 512 KB. These files come both ways: the
silent halloweentown asset is faststart with moov at byte 32, the campaign
nights carry moov at 99.6 percent.

  python3 gm_audio_check.py --queue queue.json [--cache DIR] [--local DIR]

Exit 0 clean, 1 a post has no sound, 2 nothing to check.
"""
import argparse, json, os, struct, sys, urllib.error, urllib.request

HEAD_BYTES = 64 * 1024
TAIL_BYTES = 512 * 1024
TIMEOUT = 30


def boxes(buf, start, end, depth=0):
    """Walk an MP4 atom tree, descending only the containers that matter."""
    i = start
    while i + 8 <= end:
        try:
            size = struct.unpack(">I", buf[i:i + 4])[0]
            typ = buf[i + 4:i + 8].decode("latin-1")
        except Exception:
            return
        hdr = 8
        if size == 1:
            if i + 16 > end:
                return
            size = struct.unpack(">Q", buf[i + 8:i + 16])[0]
            hdr = 16
        elif size == 0:
            size = end - i
        if size < hdr or i + size > end:
            return
        yield typ, i + hdr, i + size, depth
        if typ in ("moov", "trak", "mdia", "minf", "stbl"):
            yield from boxes(buf, i + hdr, i + size, depth + 1)
        i += size


def handlers(buf):
    """The 4 character handler of every track in this buffer.

    'soun' is an audio track, 'vide' a video one. A file with a vide and no
    soun is the thing this gate exists to refuse.
    """
    found = []
    for typ, s, e, _d in boxes(buf, 0, len(buf)):
        if typ == "hdlr" and s + 12 <= e:
            found.append(buf[s + 8:s + 12].decode("latin-1", "replace"))
    return found


def has_moov(buf):
    return any(t == "moov" for t, _s, _e, d in boxes(buf, 0, len(buf)) if d == 0)


def fetch(url, start=None, length=None):
    req = urllib.request.Request(url)
    if start is not None:
        end = "" if length is None else str(start + length - 1)
        req.add_header("Range", "bytes=%d-%s" % (start, end))
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read(), r.headers.get("Content-Range"), r.status


def probe(url, cache=None, local=None):
    """(handlers, note). handlers is None when the container was unreadable."""
    name = url.rsplit("/", 1)[-1]
    if local:
        p = os.path.join(local, name)
        if os.path.exists(p):
            buf = open(p, "rb").read()
            return (handlers(buf), "local") if has_moov(buf) else (None, "no moov in local file")
        return None, "not in --local dir"
    if cache:
        os.makedirs(cache, exist_ok=True)
        p = os.path.join(cache, name + ".json")
        if os.path.exists(p):
            try:
                c = json.load(open(p))
                return c["handlers"], "cached"
            except Exception:
                pass
    try:
        head, _cr, _st = fetch(url, 0, HEAD_BYTES)
    except (urllib.error.URLError, OSError) as e:
        return None, "head fetch failed: %s" % e
    res, note = None, None
    if has_moov(head):
        res, note = handlers(head), "moov in head"
    else:
        # moov sits at the end on a file that was not written faststart, and
        # these come both ways, so a suffix range is the second and last ask
        try:
            req = urllib.request.Request(url)
            req.add_header("Range", "bytes=-%d" % TAIL_BYTES)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                tail = r.read()
        except (urllib.error.URLError, OSError) as e:
            return None, "tail fetch failed: %s" % e
        # the tail starts mid atom, so scan forward for a moov header
        at = tail.find(b"moov")
        if at >= 4:
            res, note = handlers(tail[at - 4:]), "moov in tail"
        else:
            return None, "moov not found in first %dKB or last %dKB" % (
                HEAD_BYTES // 1024, TAIL_BYTES // 1024)
    if cache and res is not None:
        try:
            json.dump({"handlers": res}, open(os.path.join(cache, name + ".json"), "w"))
        except Exception:
            pass
    return res, note


def load_queue(path):
    d = json.load(open(path))
    return rows_from(d["items"] if isinstance(d, dict) else d)


def rows_from(items):
    """The mp4 posts in a queue dump. A still has no audio question to answer."""
    rows = []
    for it in items:
        draft = it.get("draft") or {}
        content = draft.get("content") or {}
        for u in (content.get("mediaUrls") or []):
            if not str(u).lower().endswith(".mp4"):
                continue
            rows.append({
                "id": str(it.get("id")),
                "when": (it.get("scheduledAt") or "")[:16],
                "platform": content.get("platform") or (draft.get("target") or {}).get("targetType"),
                "account": str(draft.get("accountId")),
                "url": u,
            })
    return rows


def check(rows, cache=None, local=None):
    findings = []
    seen = {}
    for r in rows:
        if r["url"] not in seen:
            seen[r["url"]] = probe(r["url"], cache=cache, local=local)
        hs, note = seen[r["url"]]
        if hs is None:
            findings.append({
                "rule": "A02_AUDIO_UNREADABLE", "id": r["id"], "when": r["when"],
                "detail": "%s on %s %s: could not read the container (%s)" % (
                    r["id"], r["platform"], r["account"], note),
            })
        elif "soun" not in hs:
            findings.append({
                "rule": "A01_NO_AUDIO_TRACK", "id": r["id"], "when": r["when"],
                "detail": "%s at %s on %s %s has no audio track (tracks: %s)" % (
                    r["id"], r["when"], r["platform"], r["account"],
                    ", ".join(hs) or "none"),
            })
    findings.sort(key=lambda f: (f["when"], f["id"]))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--cache")
    ap.add_argument("--local", help="read files from here instead of the network")
    a = ap.parse_args()
    rows = load_queue(a.queue)
    if not rows:
        print("no mp4 posts to check")
        return 2
    findings = check(rows, cache=a.cache, local=a.local)
    print("%d mp4 posts, %d distinct files" % (len(rows), len({r["url"] for r in rows})))
    for f in findings:
        print("%-22s %s" % (f["rule"], f["detail"]))
    if not findings:
        print("audio clean: every video carries a sound track")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
