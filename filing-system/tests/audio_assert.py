#!/usr/bin/env python3
"""A video post that carries no sound.

Amanda, 10/04: "it's going out with no sound again." 6 posts from 3 assets
were queued with no audio track, every existing gate passed them, and the
nights that had published were all fine. These are the rules that read the
file instead of a column.

Synthetic containers, built byte by byte here, so the suite needs no network,
no ffmpeg and no media checked into the repo.
"""
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_audio_check as A

fails = []


def want(got, expect, label):
    if got != expect:
        fails.append("%s: got %r, wanted %r" % (label, got, expect))


def box(typ, payload=b""):
    return struct.pack(">I", 8 + len(payload)) + typ.encode("latin-1") + payload


def hdlr(kind):
    # 4 bytes version/flags, 4 pre_defined, then the 4 character handler
    return box("hdlr", b"\0" * 8 + kind.encode("latin-1") + b"\0" * 12)


def trak(kind):
    return box("trak", box("mdia", hdlr(kind) + box("minf", box("stbl", b""))))


def mvhd(scale, length, version=0):
    if version == 1:
        # version 1: 8 byte times, then a 4 byte scale and an 8 byte duration
        body = b"\x01\0\0\0" + b"\0" * 16 + struct.pack(">I", scale) + struct.pack(">Q", length)
    else:
        body = b"\0" * 4 + b"\0" * 8 + struct.pack(">I", scale) + struct.pack(">I", length)
    return box("mvhd", body + b"\0" * 80)


def mp4(kinds, faststart=True, mdat=b"\0" * 2048, scale=None, length=None, version=0):
    head = mvhd(scale, length, version) if scale is not None else b""
    moov = box("moov", head + b"".join(trak(k) for k in kinds))
    ftyp = box("ftyp", b"isom")
    return ftyp + moov + box("mdat", mdat) if faststart else ftyp + box("mdat", mdat) + moov


# The parser reads the handlers out of a container, both layouts, because the
# live files come both ways: the silent halloweentown asset is faststart with
# moov at byte 32 and the campaign nights carry moov at 99.6 percent.
want(A.handlers(mp4(["vide", "soun"])), ["vide", "soun"], "a sound file reports both tracks")
want(A.handlers(mp4(["vide"])), ["vide"], "a silent file reports only video")
want(A.has_moov(mp4(["vide", "soun"])), True, "moov is found at the front")
want(A.has_moov(mp4(["vide", "soun"], faststart=False)), True, "and at the back")
want(A.has_moov(box("ftyp", b"isom") + box("mdat", b"\0" * 64)), False,
     "a file with no moov is not claimed to have one")

# 64 bit sizes, which a long mdat uses, must not derail the walk.
big = box("ftyp", b"isom") + struct.pack(">I", 1) + b"mdat" + struct.pack(">Q", 16 + 32) + b"\0" * 32
big += box("moov", trak("vide") + trak("soun"))
want(A.handlers(big), ["vide", "soun"], "a 64 bit mdat does not stop the walk")

# A truncated container is not called clean. No substitution: say so and stop.
want(A.has_moov(box("ftyp", b"isom")[:6]), False, "a truncated file reports no moov")

# Duration comes out of the same bytes the handlers do. On 10/07 it was the
# only way to tell a mis-tagged food review from one that was genuinely
# rendered short, and the answer changed the finding.
want(A.seconds(mp4(["vide", "soun"], scale=600, length=18600)), 31.0,
     "a 31 second movie measures 31 seconds")
want(A.seconds(mp4(["vide", "soun"], scale=1000, length=122600)), 122.6,
     "and a 123 second one measures 123")
back = mp4(["vide"], faststart=False, scale=600, length=6960)
at = back.find(b"moov")
want(A.seconds(back[at - 4:]), 11.6,
     "duration reads out of the mid atom tail slice probe hands it")
want(A.handlers(back[at - 4:]), ["vide"],
     "and the handlers come out of that same slice")
want(A.seconds(mp4(["vide", "soun"], scale=90000, length=2790000, version=1)), 31.0,
     "a version 1 mvhd carries 64 bit times")
want(A.seconds(mp4(["vide", "soun"])), None,
     "a file with no mvhd reports no duration rather than 0")
want(A.seconds(mp4(["vide", "soun"], scale=0, length=100)), None,
     "a 0 timescale is not divided by")

# The 2 rules, over a queue in the shape blotato_list_schedules returns.
TMP = os.path.join(HERE, "_audio_fixtures")
os.makedirs(TMP, exist_ok=True)
open(os.path.join(TMP, "sound.mp4"), "wb").write(mp4(["vide", "soun"]))
open(os.path.join(TMP, "silent.mp4"), "wb").write(mp4(["vide"], scale=600, length=6960))


def post(pid, name, when="2026-10-13T15:00"):
    return {"id": pid, "scheduledAt": when + ":00.000Z",
            "draft": {"target": {"targetType": "instagram"},
                      "content": {"platform": "instagram", "mediaUrls": ["https://x/" + name]},
                      "accountId": "45886"}}


rows = A.rows_from([post("p1", "sound.mp4"), post("p2", "silent.mp4")])
want(len(rows), 2, "both mp4 posts load")
found = A.check(rows, local=TMP)
want([f["rule"] for f in found], ["A01_NO_AUDIO_TRACK"], "only the silent post is refused")
want("p2" in found[0]["detail"], True, "and it is named")
want("instagram 45886" in found[0]["detail"], True, "with the account it lands on")
want("11.6s long" in found[0]["detail"], True,
     "and with how long it runs, so the next session does not have to go and measure it")

# A still is not a video and is not this rule's business.
still = {"id": "p3", "scheduledAt": "2026-10-13T15:00:00.000Z",
         "draft": {"target": {"targetType": "instagram"},
                   "content": {"platform": "instagram", "mediaUrls": ["https://x/card.png"]},
                   "accountId": "45886"}}
want(A.rows_from([still]), [], "a still is not checked for audio")

# A file the probe cannot reach is reported, never passed.
unreadable = A.check(A.rows_from([post("p4", "missing.mp4")]), local=TMP)
want([f["rule"] for f in unreadable], ["A02_AUDIO_UNREADABLE"],
     "an unreachable file is reported, not called clean")

# A post whose media went missing on the way in is not a still and is not
# clean. It is a hole in the input, and the only thing that makes it visible is
# counting what did NOT reach the gate. On the 10/05 nightly 26 posts lost
# their mediaUrls while the queue was assembled from 2 Blotato endpoints, the
# gate read 135 mp4 posts and said clean, and the run's 1 silent post was in
# the 26 it never saw.
stripped = {"id": "p5", "scheduledAt": "2026-10-13T15:00:00.000Z",
            "draft": {"target": {"targetType": "tiktok"},
                      "content": {"platform": "tiktok"},
                      "accountId": "41488"}}
want(A.rows_from([stripped]), [], "a post with no mediaUrls yields no row")
queue = [post("p6", "sound.mp4"), stripped, still]
reached = len({r["id"] for r in A.rows_from(queue)})
nomedia = sum(1 for i in queue
              if not ((i.get("draft") or {}).get("content") or {}).get("mediaUrls"))
want((reached, len(queue), nomedia), (1, 3, 1),
     "the gate can say how many queue rows it never saw")

# probe over a fake range server. The window is a guess, and on 10/08 it was
# wrong 3 times: 5246409, 5246417 and 5288026 were faststart with moov at byte
# 32, their moov ran 78 to 84 KB against a 64 KB head read, and all 3 were
# reported unreadable. The tail path had the same bug in a worse form, where a
# truncated moov reads as 0 tracks and A01 calls a file with sound silent.
# Nothing offline reached probe before this, which is why neither showed up.
import re as _re
import urllib.request as _ur


class Served:
    """One blob over HTTP range semantics, counting what was asked for."""

    def __init__(self, blob):
        self.blob, self.asks = blob, []

    def open(self, req, timeout=0):
        rng = req.get_header("Range") or ""
        m = _re.match(r"bytes=(\d*)-(\d*)$", rng)
        n = len(self.blob)
        if m and m.group(1) == "":                      # suffix, bytes=-N
            start, end = max(0, n - int(m.group(2))), n - 1
        elif m:
            start = int(m.group(1))
            end = int(m.group(2)) if m.group(2) else n - 1
        else:
            start, end = 0, n - 1
        end = min(end, n - 1)
        self.asks.append((start, end - start + 1))
        body, served = self.blob[start:end + 1], self
        class R:
            headers = {"Content-Range": "bytes %d-%d/%d" % (start, end, n)}
            status = 206
            def __enter__(s): return s
            def __exit__(s, *x): pass
            def read(s, *a): return body
            def getheader(s, k, d=None): return s.headers.get(k, d)
        R.headers = type("H", (dict,), {"get": dict.get})(R.headers)
        return R()


def probe_served(blob):
    srv = Served(blob)
    with mock_urlopen(srv):
        return A.probe("https://x/served.mp4"), srv


class mock_urlopen:
    def __init__(self, srv): self.srv = srv
    def __enter__(self):
        self.real = _ur.urlopen
        _ur.urlopen = self.srv.open
        return self
    def __exit__(self, *x):
        _ur.urlopen = self.real


def padded_trak(kind, pad):
    """A trak carrying pad bytes of filler, so moov can be made any size."""
    return box("trak", box("mdia", hdlr(kind) + box("minf", box("stbl", box("free", b"\0" * pad)))))


def big_mp4(kinds, pad, faststart=True, mdat=b"\0" * 4096, scale=600, length=18600):
    moov = box("moov", mvhd(scale, length) + b"".join(padded_trak(k, pad) for k in kinds))
    ftyp = box("ftyp", b"isom")
    return (ftyp + moov + box("mdat", mdat)) if faststart else (ftyp + box("mdat", mdat) + moov)


# a moov header whose body is not all there still reports where and how long
cut = big_mp4(["vide", "soun"], 40000)[:A.HEAD_BYTES]
found = [b for b in A.top_boxes(cut) if b[0] == "moov"]
want(len(found), 1, "top_boxes finds a moov header the window truncated")
want(A.has_moov(cut), False, "while the walk itself will not yield it")

# faststart, moov bigger than the head read: read exactly, do not guess wider
blob = big_mp4(["vide", "soun"], 40000)
want(len(blob) > A.HEAD_BYTES, True, "the fixture moov really does overrun the head read")
(hs, secs, note), srv = probe_served(blob)
want(hs, ["vide", "soun"], "a faststart moov over the head read is read, not refused")
want(secs, 31.0, "and its duration comes with it")
want("fetched whole" in (note or ""), True, "and the note says the moov was fetched by its own size")
want(len(srv.asks), 2, "which costs 1 request more than the head read, not a download")
_t, _at, _size = [b for b in A.top_boxes(blob[:A.HEAD_BYTES]) if b[0] == "moov"][0]
want(srv.asks[1], (_at, _size), "and that request is exactly the moov range, not the file")

# the tail path: find() matches 4 bytes that also occur in payload, so the
# first hit need not be a header. A bogus size read off one gives 0 tracks and
# A01 then calls a file with sound silent, which is the worst outcome the gate
# has. The scan keeps going until a hit is a real moov.
decoy = b"\x7f\xff\xff\xffmoov" + b"\0" * 512          # a size nothing can satisfy
blob = big_mp4(["vide", "soun"], 0, faststart=False,
               mdat=b"\0" * 4096 + decoy + b"\0" * (A.TAIL_BYTES // 2))
want(blob.count(b"moov"), 2, "the fixture really does carry a decoy before the real moov")
(hs, secs, note), srv = probe_served(blob)
want(hs, ["vide", "soun"], "a decoy moov in payload does not stop the real one being found")
want(secs, 31.0, "and the duration still comes off the real moov")

# the same shape with no audio is still refused, so the scan did not go soft
blob = big_mp4(["vide"], 0, faststart=False,
               mdat=b"\0" * 4096 + decoy + b"\0" * (A.TAIL_BYTES // 2))
srv = Served(blob)
with mock_urlopen(srv):
    found = A.check(A.rows_from([post("p-decoy", "served.mp4")]))
want([f["rule"] for f in found], ["A01_NO_AUDIO_TRACK"],
     "and a silent file behind a decoy is still refused")

# a tail with nothing moov shaped in it is reported, not guessed at
blob = box("ftyp", b"isom") + box("mdat", b"\0" * (A.HEAD_BYTES + A.TAIL_BYTES))
(hs, secs, note), srv = probe_served(blob)
want(hs, None, "a file with no moov anywhere is reported unreadable")
want("not found" in (note or ""), True, "and the note says where it looked")

# a declared size past MOOV_MAX is reported, never fetched
blob = big_mp4(["vide", "soun"], 40000)
at = blob.find(b"moov") - 4
huge = blob[:at] + struct.pack(">I", A.MOOV_MAX + 1) + blob[at + 4:]
(hs, secs, note), srv = probe_served(huge)
want(hs, None, "a moov claiming more than MOOV_MAX is not fetched")
want("over the" in (note or ""), True, "and the note says why")
want(len(srv.asks), 1, "and nothing beyond the head read was asked for")

for n in ("sound.mp4", "silent.mp4"):
    os.remove(os.path.join(TMP, n))
os.rmdir(TMP)

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  audio rules: a silent reel is refused, a still is skipped, an unreadable file is reported")
sys.exit(0)
