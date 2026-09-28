#!/usr/bin/env python3
"""
GM-Trivia-Pick — the day's trivia fact, and everything its video and posts need.

Added 09/28/2026 to Run 8, the trivia pipeline.

The daily trivia job (daily-trivia/make.py) asks this module 1 question: what
goes out next, and what does each platform say. The answer is built only from
data that already governs it, so nothing is invented on the way:

  the fact          trivia-fact-bank.csv, only when usable_problems() is empty
  the platforms     channel-rules.csv, the channels that carry everything
  the ask           trivia-cta.csv, and only when keyword-registry.csv says the
                    keyword is live on that account
  the words         the Fact and the Backbone, exactly as banked. No model
                    writes the script, so no number can appear that the bank
                    does not carry. T03 still checks every caption.
  the face          her own twin, 1 of the 2 podcast looks, rotated by day

The design first proposed on 09/28 had OpenAI write a script from a free
topic, "World History - Forgotten Inventions". That is the one input this lane
is built to refuse: a topic handed to a model asks the model to supply the
facts. SOP_0909 section 8.

House rules, same as every other module:
  Propose-only. This script reads. It never renders, uploads or posts.
  No substitution. A held fact is refused, not swapped for the nearest one.
  Reuse before generating. A fact already approved has a video. It is not
    picked again.

Usage
  python3 gm_trivia_pick.py --next            what goes out next
  python3 gm_trivia_pick.py --fact TRV-001    this fact

Exit codes
  0   a package, every caption through the trivia and keyword gates
  1   refused. The fact cannot go, or a caption failed a gate
  2   nothing usable left to send

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import glob
import json
import os
import re
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gm_keyword_check as K  # noqa: E402
import gm_trivia_bank as B  # noqa: E402
import gm_trivia_check as T  # noqa: E402

ROOT = os.path.dirname(HERE)
CHANNEL_RULES = os.path.join(ROOT, "data", "channel-rules.csv")
TRIVIA_CTA = os.path.join(ROOT, "data", "trivia-cta.csv")
APPROVED = os.path.join(os.path.dirname(ROOT), "daily-trivia", "approved")

# The route this job renders. A motion-text fact goes through the reel factory
# instead. HANDOFF_0909 section 6.
DELIVERY = ("talking-head",)

# Her own twin, never Avery or Cesa. HANDOFF_0909 section 6: the 2 podcast
# looks, because the lane is somebody telling you a thing they know. Rotated by
# day, the same way plates rotate on the reels. A look id is what HeyGen takes
# as avatar_id.
VOICE_ID = "05f19352e8f74b0392a8f411eba40de1"
VOICE_SPEED = 0.92
AVATARS = (
    ("3243536278874919a784ed66c135a473", "Amanda with a podcast microphone"),
    ("96af09cd10804111a290ecb70f39500f", "Amanda hosting a live podcast"),
)

# The Gentle Muse page on Facebook account 30840. refill.py and HANDOFF_0909.
FB_PAGE = "1086399221215093"

# 1 topic tag, added after the fixed tags on platforms that carry hashtags.
TOPIC_TAGS = {"ai": "#ai", "automation": "#automation", "creator": "#creatoreconomy"}

TITLE_MAX = 100


# ---------- the rules, read from the data that already holds them ----------

def load_lane_channels(path=CHANNEL_RULES):
    """The channels this lane posts to: the ones the board sends everything.

    On 09/28 that is Instagram, Facebook, TikTok and YouTube. LinkedIn is
    business only, Pinterest is evergreen pins, X is dropped. The first account
    listed is the main one. Cesa's accounts never carry this lane.
    """
    lane = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            ch = (r.get("Channel") or "").strip().lower()
            try:
                most = int(r.get("MaxPerDay") or 0)
            except ValueError:
                most = 0
            if ch and (r.get("Content") or "").strip().lower() == "everything" and most > 0:
                lane[ch] = (r.get("AccountIds") or "").split("|")[0].strip()
    return lane


def load_trivia_cta(path=TRIVIA_CTA):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return {((r.get("Platform") or "").strip(), (r.get("AccountId") or "").strip()): r
                for r in csv.DictReader(fh)}


def approved_ids(folder=APPROVED):
    """Every fact that already has an approved video. Its package is the record."""
    out = set()
    for path in glob.glob(os.path.join(folder, "*.json")):
        try:
            with open(path, encoding="utf-8") as fh:
                out.add(json.load(fh).get("factId", ""))
        except (OSError, ValueError):
            continue
    return out - {""}


def avatar_for(day):
    return AVATARS[day.toordinal() % len(AVATARS)]


def delivery_of(fact):
    return (fact.get("Delivery") or "").strip().lower()


# ---------- which fact ----------

def pick_next(bank, day, sources, skip):
    """The first fact in the bank's pull order that this job can render and
    that is not in skip. Anything passed over is named, not hidden."""
    passed = []
    for fid, fact in B.available(bank, 0, today=day, sources=sources):
        if fid in skip:
            passed.append((fid, "already approved or declined"))
        elif delivery_of(fact) not in DELIVERY:
            passed.append((fid, "%s, which renders in the reel factory" % delivery_of(fact)))
        else:
            return fid, fact, passed
    return None, None, passed


def refusals(fid, fact, day, approved, skip):
    # Staleness is judged on the day it goes out, which is the day the claim
    # is said out loud.
    problems = list(B.usable_problems(fact, day, approved))
    if delivery_of(fact) not in DELIVERY:
        problems.append('Delivery is "%s". That renders in the reel factory, not through '
                        "HeyGen, so it does not go to this job." % delivery_of(fact))
    if fid in skip:
        problems.append("already approved or declined. An approved fact has its video. "
                        "Reuse that one.")
    return problems


def asks(fact, lane, cta_rows, registry):
    """Each platform's call to action row, and every reason one cannot be used.

    A keyword has to be live on the account that carries it: a dead keyword is
    worse than none, because somebody comments the word and waits. A link has
    to go where the fact's keyword sends people, or the 2 asks disagree.
    """
    keyword = (fact.get("Keyword") or "").strip().upper()
    live = [r for r in registry if r["Keyword"].upper() == keyword and r["Active"] == "yes"]
    destinations = {(r.get("Destination") or "").strip() for r in live} - {""}
    rows, problems = {}, []
    for ch, acct in lane.items():
        row = cta_rows.get((ch, acct))
        if row is None:
            problems.append("no trivia call to action for %s %s in trivia-cta.csv" % (ch, acct))
            continue
        ask = (row.get("Keyword") or "").strip().upper()
        if ask:
            if ask != keyword:
                problems.append("%s asks for %s and this fact routes to %s"
                                % (ch, ask, keyword or "no keyword"))
                continue
            here = [r for r in K.lookup(registry, ask, ch, acct) if r["Active"] == "yes"]
            if not here:
                problems.append("%s is not live on %s %s in keyword-registry.csv. Somebody "
                                "would comment it and nothing would answer." % (ask, ch, acct))
                continue
            if (here[0].get("Note") or "").startswith("BROKEN"):
                problems.append("%s on %s is marked BROKEN in keyword-registry.csv: %s"
                                % (ask, ch, here[0]["Note"]))
                continue
        link = (row.get("Link") or "").strip()
        if link and link not in destinations:
            problems.append("the %s link in trivia-cta.csv, %s, is not where %s sends people"
                            % (ch, link, keyword or "the fact's keyword"))
            continue
        rows[ch] = row
    return rows, problems


# ---------- the words, all of them from the bank row ----------

def script_of(fact):
    """What she says on camera: the fact, then the turn. Nothing added."""
    return "%s %s" % ((fact.get("Fact") or "").strip(), (fact.get("Backbone") or "").strip())


def title_of(fact):
    """The first sentence of the fact. Too long, and it ends at the last comma
    that still leaves a real phrase, or failing that at a word."""
    first = re.split(r"(?<=[.?!])\s", (fact.get("Fact") or "").strip(), maxsplit=1)[0]
    if len(first) <= TITLE_MAX:
        return first.rstrip(".")
    clause = first[:TITLE_MAX].rsplit(",", 1)[0]
    if len(clause) >= 40:
        return clause
    return first[:TITLE_MAX].rsplit(" ", 1)[0].rstrip(",;: ")


def caption(fact, row):
    """Fact, turn, the platform's own ask, its link, its tags."""
    parts = [(fact.get("Fact") or "").strip(), (fact.get("Backbone") or "").strip()]
    line = (row.get("Line") or "").strip()
    link = (row.get("Link") or "").strip()
    if line and link and line.endswith(":"):
        parts.append("%s\n%s" % (line, link))
    else:
        parts.extend(x for x in (line, link) if x)
    tags = (row.get("Hashtags") or "").strip()
    if tags:
        topic = TOPIC_TAGS.get((fact.get("Topic") or "").strip().lower())
        parts.append(" ".join(x for x in (tags, topic) if x))
    return "\n\n".join(p for p in parts if p)


def package(fid, fact, day, lane, rows):
    """Everything the render and the 4 posts need, and nothing they do not."""
    avatar_id, avatar_name = avatar_for(day)
    posts = []
    for ch, acct in lane.items():
        post = {"platform": ch, "accountId": acct, "text": caption(fact, rows[ch])}
        if ch == "instagram":
            post.update(mediaType="reel", shareToFeed=True)
        elif ch == "facebook":
            post.update(pageId=FB_PAGE, mediaType="reel")
        elif ch in ("youtube", "tiktok"):
            post["title"] = title_of(fact)
        posts.append(post)
    return {
        "factId": fid,
        "topic": (fact.get("Topic") or "").strip().lower(),
        "fact": (fact.get("Fact") or "").strip(),
        "backbone": (fact.get("Backbone") or "").strip(),
        "source": (fact.get("Source") or "").strip(),
        "sourceUrl": (fact.get("SourceUrl") or "").strip(),
        "verifiedOn": (fact.get("VerifiedOn") or "").strip(),
        "madeOn": day.isoformat(),
        "script": script_of(fact),
        "heygen": {"avatarId": avatar_id, "avatarName": avatar_name, "voiceId": VOICE_ID,
                   "voiceSpeed": VOICE_SPEED, "aspectRatio": "9:16"},
        "posts": posts,
    }


def gate(pkg, bank, registry, platform_cta):
    """Every caption through the trivia gate and the keyword gate. Any FAIL or
    HOLD stops the day: nothing renders until the words are right."""
    findings = []
    for p in pkg["posts"]:
        post = {"id": "%s-%s" % (pkg["factId"], p["platform"]), "factId": pkg["factId"],
                "platform": p["platform"], "accountId": p["accountId"], "text": p["text"]}
        findings.extend(T.check_post(post, bank))
        findings.extend(K.check_post(post, registry, platform_cta))
    return findings


def build(bank, day, *, fact_id=None, skip=(), sources=B.DEFAULT_SOURCES,
          channels=CHANNEL_RULES, cta=TRIVIA_CTA, registry=K.REGISTRY,
          platform_cta=K.PLATFORM_CTA):
    """Pick and package 1 fact. Returns (package or None, exit code, lines)."""
    lines = []
    skip = set(skip)
    approved = B.load_sources(sources)
    if fact_id is None:
        fid, fact, passed = pick_next(bank, day, sources, skip)
        lines.extend("passed over %s, %s" % (s, why) for s, why in passed)
        if fid is None:
            lines += ["Nothing to send. No verified talking-head fact is left that has not",
                      "already been approved or declined. Add verified rows to",
                      "trivia-fact-bank.csv. Do not reach for the nearest fact that fits."]
            return None, 2, lines
    else:
        fid = fact_id.strip().upper()
        fact = bank.get(fid)
        if fact is None:
            return None, 1, ["%s is not in the bank. A fact that is not written down was not "
                             "checked." % fid]

    reg = K.load_registry(registry)
    rows, cta_problems = asks(fact, load_lane_channels(channels), load_trivia_cta(cta), reg)
    problems = refusals(fid, fact, day, approved, skip) + cta_problems
    if problems:
        return None, 1, ["REFUSED. %s cannot go out." % fid] + ["  " + p for p in problems]

    pkg = package(fid, fact, day, load_lane_channels(channels), rows)
    findings = gate(pkg, bank, reg, K.load_platform_cta(platform_cta))
    if findings:
        return None, 1, (["REFUSED. A caption for %s failed a gate." % fid] +
                         ["  %s %s %s" % (f["rule"], f["id"], f["detail"]) for f in findings])
    return pkg, 0, lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="The day's trivia fact and its posts.")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--next", action="store_true", help="the next fact in the pull order")
    which.add_argument("--fact", metavar="TRV-NNN", help="this fact")
    ap.add_argument("--date", help="the day it goes out, YYYY-MM-DD. Default today")
    ap.add_argument("--skip", default="", help="fact ids to pass over, comma separated")
    ap.add_argument("--bank", default=B.DEFAULT_BANK)
    ap.add_argument("--sources", default=B.DEFAULT_SOURCES)
    ap.add_argument("--approved", default=APPROVED)
    ap.add_argument("--registry", default=K.REGISTRY)
    a = ap.parse_args(argv)

    day = date.today()
    if a.date:
        day = B.parse_date(a.date) if re.match(r"^\d{4}-\d{2}-\d{2}$", a.date) else None
        if day is None:
            print("--date %s is not a day. Give YYYY-MM-DD." % a.date)
            return 2
    skip = approved_ids(a.approved) | {s.strip().upper() for s in a.skip.split(",") if s.strip()}
    pkg, code, lines = build(B.load_bank(a.bank), day, fact_id=a.fact, skip=skip,
                             sources=a.sources, registry=a.registry)
    for line in lines:
        print(line)
    if pkg:
        print(json.dumps(pkg, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
