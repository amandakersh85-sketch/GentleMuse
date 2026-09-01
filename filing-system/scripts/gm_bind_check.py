#!/usr/bin/env python3
"""
GM-Bind-Check — the caption-to-clip binding gate.

Run 6 of the Gentle Muse filing system. Reads a reel render JSON and the clip
library, and refuses to pass any video whose on-screen text is bound to a clip
that does not show what the text is talking about.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A PASS is a proposal, not a publish.

Exit codes
  0   PASS      every clip binding verified against the library
  1   FAIL      at least one blocking finding. Nothing ships.
  2   HOLD      no failures, but one or more beats have no clip and are
                waiting on Amanda to film. Nothing ships for those beats.

Usage
  python3 gm_bind_check.py --render reel.json --library clip-library.csv
  python3 gm_bind_check.py --render batch/ --library clip-library.csv --report out.csv

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys

# ---------------------------------------------------------------- text tools

STOPWORDS = {
    "a", "about", "after", "all", "am", "an", "and", "any", "are", "around",
    "as", "at", "back", "be", "been", "before", "being", "but", "by", "can",
    "did", "do", "does", "doing", "done", "dont", "down", "each", "even",
    "ever", "every", "first", "for", "from", "get", "gets", "getting", "go",
    "goes", "going", "got", "had", "has", "have", "her", "here", "hers",
    "herself", "him", "his", "how", "i", "if", "im", "in", "into", "is", "it",
    "its", "just", "keep", "know", "last", "let", "like", "little", "look",
    "made", "make", "makes", "many", "me", "more", "most", "much", "my",
    "never", "new", "no", "not", "now", "of", "off", "on", "once", "one",
    "only", "or", "other", "our", "out", "over", "own", "put", "really",
    "right", "said", "same", "say", "see", "she", "should", "so", "some",
    "still", "such", "take", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "thing", "things", "this", "those", "through",
    "time", "to", "too", "two", "up", "us", "use", "very", "want", "was",
    "way", "we", "well", "were", "what", "when", "where", "which", "while",
    "who", "why", "will", "with", "would", "you", "your", "youre", "yours",
}

# Brand filler. True of half the library, so it proves nothing about a binding.
GENERIC = {
    "aesthetic", "calm", "cozy", "feminine", "gentle", "girl", "muse", "quiet",
    "shot", "slow", "soft", "vertical", "video", "vibe", "warm", "woman",
    "clip", "footage", "b-roll", "broll", "pretty", "nice", "good",
}

_WORD = re.compile(r"[a-z0-9]+")


def stem(word):
    """Crude suffix trim. 'sleeping' -> 'sleep', 'princesses' -> 'princess'."""
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def tokens(text, drop_generic=True):
    """Content words only, stemmed. Punctuation, stopwords and filler removed."""
    raw = _WORD.findall((text or "").lower().replace("-", " ").replace("_", " "))
    out = set()
    for word in raw:
        if word in STOPWORDS or len(word) < 3:
            continue
        if drop_generic and word in GENERIC:
            continue
        out.add(stem(word))
    return out


# ---------------------------------------------------------------- library

REQUIRED_COLUMNS = ["ClipID", "File", "Shot", "DurationSec"]


def load_library(path):
    """Read clip-library.csv into {clip_id: row}. Raises on a broken schema."""
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise SystemExit(
                "clip-library.csv is missing required column(s): %s\n"
                "Build it with gm_clip_library.py before running the gate."
                % ", ".join(missing)
            )
        library = {}
        for row in reader:
            clip_id = (row.get("ClipID") or "").strip()
            if not clip_id:
                continue
            library[clip_id] = row
    return library


def clip_vocabulary(row):
    """Every content word the library knows about this clip."""
    return tokens(
        " ".join(
            [
                row.get("Shot", ""),
                row.get("Tags", ""),
                row.get("ClipID", ""),
                row.get("Mood", ""),
            ]
        )
    )


def duration_of(row):
    try:
        return float(row.get("DurationSec") or 0)
    except (TypeError, ValueError):
        return 0.0


def is_described(row):
    shot = (row.get("Shot") or "").strip()
    flag = (row.get("Described") or "").strip().lower()
    if flag in ("no", "false", "0"):
        return False
    return len(shot) >= 12


# ------------------------------------------------- the reel-factory dialect

TAGS = re.compile(r"<[^>]+>")


def _plain(html):
    """Beat HTML down to the words a reader actually sees."""
    return " ".join(TAGS.sub(" ", html or "").split())


def adapt_reel_factory(reel):
    """Translate a reel-factory payload into the shape this gate checks.

    The factory writes one plate under a whole reel: a single still or clip,
    with the captions arriving as timed beats over the top. That is a different
    document from the beat-per-clip renders this gate was written for, and
    until now it slipped past unchecked, which is precisely the hole Run 6 was
    built to close. So it gets translated rather than exempted.

    One plate carrying one caption stream becomes one binding: the clip, and
    every word laid over it. A reel that declares no footage at all is a
    typography cut and has nothing to bind, so it passes with nothing to say.
    """
    beats = reel.get("beats") or []
    title = reel.get("id") or reel.get("slug") or reel.get("title")
    out = {"title": title, "duration": reel.get("duration")}

    clip = reel.get("clip")
    if not clip:
        # No plate. Legal only when the reel says so, matching the fact bank's
        # text delivery lane. Silence is not a declaration.
        if (reel.get("delivery") or "").strip().lower() == "text":
            out["clips"] = []
            out["_no_footage"] = True
        else:
            out["clips"] = []
        return out

    file_path = (clip.get("file") or "").strip()
    clip_id = (clip.get("clip_id") or "").strip()
    if not clip_id and file_path:
        # make-reels.sh writes ClipID as the basename and File as clips/<name>,
        # so the basename is the identity, not a guess at one.
        clip_id = os.path.splitext(os.path.basename(file_path))[0]

    out["clips"] = [{
        "text": " ".join(_plain(b.get("html")) for b in beats if isinstance(b, dict)),
        "clip_id": clip_id,
        "match_reason": (clip.get("match_reason") or "").strip(),
        "override": clip.get("override"),
        "duration": reel.get("duration"),
    }]
    return out


def is_reel_factory(doc):
    return isinstance(doc, dict) and "beats" in doc and "clips" not in doc


# ---------------------------------------------------------------- findings

class Finding:
    def __init__(self, code, level, video, beat, message):
        self.code = code
        self.level = level          # FAIL | HOLD | NOTE
        self.video = video
        self.beat = beat
        self.message = message

    def line(self):
        where = self.video if self.beat is None else "%s beat %s" % (self.video, self.beat)
        return "  [%s] %-18s %s\n      %s" % (self.level, self.code, where, self.message)


# ---------------------------------------------------------------- the checks

def check_video(video, library, index):
    """Return a list of Findings for one render JSON object."""
    found = []
    title = video.get("title") or "video %d" % index
    add = lambda c, l, b, m: found.append(Finding(c, l, title, b, m))

    clips = video.get("clips")
    if video.get("_no_footage") and not clips:
        return found
    if not isinstance(clips, list) or not clips:
        add("E00_NO_CLIPS", "FAIL", None, "render JSON has no clips array.")
        return found

    declared = video.get("duration")
    running = 0.0
    seen = {}

    for position, clip in enumerate(clips, start=1):
        if not isinstance(clip, dict):
            add("E00_BAD_CLIP", "FAIL", position, "clip entry is not an object.")
            continue

        text = (clip.get("text") or "").strip()
        clip_id = (clip.get("clip_id") or "").strip()
        reason = (clip.get("match_reason") or "").strip()
        try:
            beat_len = float(clip.get("duration") or 0)
        except (TypeError, ValueError):
            beat_len = 0.0
        running += beat_len

        # ---- the HOLD lane. The only legal way to ship a beat with no clip.
        if clip_id.upper() == "HOLD":
            if not text:
                add("E10_EMPTY_TEXT", "FAIL", position,
                    "HOLD beat with no on-screen text. Write the line or drop the beat.")
            else:
                add("H01_NEEDS_FOOTAGE", "HOLD", position,
                    'no clip bound. Text is "%s". This beat needs filming. '
                    "Do not substitute a near-miss clip." % text)
            continue

        # ---- identity
        if not clip_id:
            add("E01_NO_CLIP_ID", "FAIL", position,
                'no clip_id. File paths are not identity — bind by ClipID or use "HOLD".')
            continue

        row = library.get(clip_id)
        if row is None:
            add("E01_UNKNOWN_CLIP", "FAIL", position,
                'clip_id "%s" is not in the clip library. Invented clips break the render.'
                % clip_id)
            continue

        if not text:
            add("E10_EMPTY_TEXT", "FAIL", position, "clip is bound but carries no on-screen text.")
            continue

        # ---- the clip must be describable before it can be verified
        if not is_described(row):
            add("E02_UNDESCRIBED", "FAIL", position,
                'clip "%s" has no usable Shot description. An undescribed clip cannot be '
                "verified against a caption, so it cannot be bound. Describe it first."
                % clip_id)
            continue

        # ---- declared file must agree with the library
        json_file = (clip.get("file") or "").strip()
        lib_file = (row.get("File") or "").strip()
        if json_file and lib_file and json_file != lib_file:
            add("E03_FILE_MISMATCH", "FAIL", position,
                'clip_id "%s" points at "%s" in the library but the JSON says "%s".'
                % (clip_id, lib_file, json_file))

        # ---- the real length of the real file
        real = duration_of(row)
        try:
            start = float(clip.get("start") or 0)
        except (TypeError, ValueError):
            start = 0.0
        if real and (start + beat_len) - real > 0.05:
            add("E04_OVERRUN", "FAIL", position,
                'beat asks for %.4gs starting at %.4gs, but "%s" is only %.4gs long. '
                "The text will outlast the footage." % (beat_len, start, clip_id, real))

        # ---- vertical only
        orientation = (row.get("Orientation") or "").strip().lower()
        wants_vertical = str(video.get("format") or "9:16").strip() in ("9:16", "4:5")
        if wants_vertical and orientation and orientation not in ("vertical", "portrait"):
            add("E06_ORIENTATION", "FAIL", position,
                'clip "%s" is %s. A %s reel needs vertical footage.'
                % (clip_id, orientation, video.get("format")))

        # ---- the binding itself
        if len(reason) < 10:
            add("E08_NO_MATCH_REASON", "FAIL", position,
                'no match_reason. State in plain words what in this clip shows "%s".' % text)

        caption_words = tokens(text)
        clip_words = clip_vocabulary(row)
        shared = caption_words & clip_words
        overridden = str(clip.get("override") or "").strip().lower() in ("true", "yes", "1")

        if caption_words and not shared:
            if overridden:
                add("N01_OVERRIDE", "NOTE", position,
                    'no shared content word between text and clip. Overridden: "%s"' % reason)
            else:
                add("E07_TOPIC_MISMATCH", "FAIL", position,
                    'on-screen text "%s" shares no content word with clip "%s" (%s). '
                    'This is the mismatch. Rebind, or set "override": true with a '
                    "match_reason that explains the visual metaphor."
                    % (text, clip_id, row.get("Shot", "").strip()))

        # ---- did a better clip exist? the "you already had the right one" check
        better = []
        for other_id, other in library.items():
            if other_id == clip_id or not is_described(other):
                continue
            overlap = caption_words & clip_vocabulary(other)
            if len(overlap) > len(shared):
                better.append((len(overlap), other_id, other.get("Shot", "").strip(), overlap))
        if better:
            better.sort(key=lambda b: (-b[0], b[1]))
            top = better[0]
            level = "FAIL" if (not shared and not overridden) else "NOTE"
            code = ("E11_BETTER_CLIP_EXISTS" if (not shared and not overridden)
                    else "N02_CLOSER_CLIP")
            add(code, level, position,
                'text "%s" matches "%s" (%s) on %s — a better fit than the bound clip "%s".'
                % (text, top[1], top[2], sorted(top[3]), clip_id))

        # ---- same clip, two different stories
        if clip_id in seen:
            prior_text, prior_pos = seen[clip_id]
            if tokens(prior_text) and tokens(prior_text) != caption_words and not (
                tokens(prior_text) & caption_words
            ):
                add("E09_REUSE_CONFLICT", "FAIL", position,
                    'clip "%s" already carries "%s" at beat %d. One clip cannot illustrate '
                    "two unrelated lines in the same reel."
                    % (clip_id, prior_text, prior_pos))
        else:
            seen[clip_id] = (text, position)

    # ---- arithmetic
    if declared is not None:
        try:
            if abs(float(declared) - running) > 0.05:
                add("E05_SUM_MISMATCH", "FAIL", None,
                    "clips sum to %.4gs but duration says %.4gs." % (running, float(declared)))
        except (TypeError, ValueError):
            add("E05_SUM_MISMATCH", "FAIL", None, 'duration "%s" is not a number.' % declared)

    return found


# ---------------------------------------------------------------- io

def load_renders(path):
    """Accept one JSON file, or a directory of them. Always returns a list."""
    paths = []
    if os.path.isdir(path):
        paths = sorted(
            os.path.join(path, name)
            for name in os.listdir(path)
            if name.lower().endswith(".json")
        )
    else:
        paths = [path]

    videos = []
    for file_path in paths:
        with open(file_path, encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            batch = data
        elif isinstance(data, dict) and isinstance(data.get("videos"), list):
            batch = data["videos"]
        else:
            batch = [data]
        videos.extend(adapt_reel_factory(v) if is_reel_factory(v) else v
                      for v in batch)
    return videos, paths


def main():
    parser = argparse.ArgumentParser(
        description="Verify every caption-to-clip binding in a reel render JSON."
    )
    parser.add_argument("--render", required=True,
                        help="render JSON file, or a folder of them")
    parser.add_argument("--library", required=True, help="clip-library.csv")
    parser.add_argument("--report", help="optional CSV of every finding")
    parser.add_argument("--quiet", action="store_true",
                        help="print the verdict line only")
    args = parser.parse_args()

    library = load_library(args.library)
    videos, sources = load_renders(args.render)

    findings = []
    for index, video in enumerate(videos, start=1):
        findings.extend(check_video(video, library, index))

    fails = [f for f in findings if f.level == "FAIL"]
    holds = [f for f in findings if f.level == "HOLD"]
    notes = [f for f in findings if f.level == "NOTE"]

    if not args.quiet:
        print("GM-Bind-Check")
        print("  library : %s  (%d clips, %d described)"
              % (args.library, len(library),
                 sum(1 for r in library.values() if is_described(r))))
        print("  render  : %s  (%d video%s)"
              % (args.render, len(videos), "" if len(videos) == 1 else "s"))
        print("")
        for level in ("FAIL", "HOLD", "NOTE"):
            group = [f for f in findings if f.level == level]
            if group:
                print("%s (%d)" % (level, len(group)))
                for finding in group:
                    print(finding.line())
                print("")

    if args.report:
        with open(args.report, "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["Level", "Code", "Video", "Beat", "Finding"])
            for f in findings:
                writer.writerow([f.level, f.code, f.video, f.beat or "", f.message])
        if not args.quiet:
            print("report written: %s" % args.report)

    if fails:
        print("VERDICT: FAIL — %d blocking finding%s. Nothing ships."
              % (len(fails), "" if len(fails) == 1 else "s"))
        return 1
    if holds:
        print("VERDICT: HOLD — %d beat%s waiting on footage. "
              "The rest is clean. Do not substitute."
              % (len(holds), "" if len(holds) == 1 else "s"))
        return 2
    print("VERDICT: PASS — %d video%s, every binding verified.%s"
          % (len(videos), "" if len(videos) == 1 else "s",
             " %d note(s)." % len(notes) if notes else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
