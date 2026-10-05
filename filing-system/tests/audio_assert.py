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


def mp4(kinds, faststart=True, mdat=b"\0" * 2048):
    moov = box("moov", b"".join(trak(k) for k in kinds))
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

# The 2 rules, over a queue in the shape blotato_list_schedules returns.
TMP = os.path.join(HERE, "_audio_fixtures")
os.makedirs(TMP, exist_ok=True)
open(os.path.join(TMP, "sound.mp4"), "wb").write(mp4(["vide", "soun"]))
open(os.path.join(TMP, "silent.mp4"), "wb").write(mp4(["vide"]))


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

for n in ("sound.mp4", "silent.mp4"):
    os.remove(os.path.join(TMP, n))
os.rmdir(TMP)

if fails:
    for f in fails:
        print("  " + f)
    sys.exit(1)
print("  audio rules: a silent reel is refused, a still is skipped, an unreadable file is reported")
sys.exit(0)
