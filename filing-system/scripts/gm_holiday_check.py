#!/usr/bin/env python3
"""
GM-Holiday-Check — the holiday caption gate.

Run 7 of the Gentle Muse filing system. Reads a holiday caption JSON and the
fact bank, and refuses to pass any post whose history is not in the bank, whose
nostalgia lands outside Amanda's era, or which reports a fact without ever
turning it into something.

Run 6 stopped a caption from being bound to a clip that did not show it. This
stops a caption from being bound to a fact that nobody checked. The failure it
is built for is the one a language model produces by default: a confident,
plausible, invented historical detail, delivered in her voice, to an audience
that follows her partly because she gets history right.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A PASS is a proposal, not a publish.
  No substitution. No fact in the bank means HOLD, not the nearest fact that fits.

Exit codes
  0   PASS   every claim traced to a sourced fact
  1   FAIL   at least one blocking finding. Nothing ships.
  2   HOLD   clean, but a post is waiting on a fact that has not been written.

Usage
  python3 gm_holiday_check.py --post caption.json
  python3 gm_holiday_check.py --post batch/ --report out.csv

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from gm_holiday_bank import (  # noqa: E402
    DEFAULT_BANK, DEFAULT_CALENDAR, ERA_END, ERA_START,
    in_season, load_bank, load_calendar, parse_year, parse_years, usable_problems,
)

# ---------------------------------------------------------------- text tools

STOPWORDS = {
    "a", "about", "after", "all", "also", "am", "an", "and", "any", "are",
    "around", "as", "at", "back", "be", "became", "because", "been", "before",
    "being", "both", "but", "by", "came", "can", "come", "could", "did", "do",
    "does", "doing", "done", "dont", "down", "each", "even", "ever", "every",
    "first", "for", "from", "get", "gets", "getting", "go", "goes", "going",
    "got", "had", "has", "have", "her", "here", "hers", "herself", "him",
    "his", "how", "i", "if", "im", "in", "into", "is", "it", "its", "just",
    "keep", "know", "last", "let", "like", "little", "long", "made", "make",
    "makes", "many", "me", "more", "most", "much", "my", "never", "new", "no",
    "nobody", "not", "now", "of", "off", "on", "once", "one", "only", "or",
    "other", "our", "out", "over", "own", "put", "really", "right", "said",
    "same", "say", "see", "she", "should", "so", "some", "still", "such",
    "take", "than", "that", "the", "their", "them", "then", "there", "these",
    "they", "thing", "things", "this", "those", "through", "time", "to", "too",
    "two", "up", "us", "use", "very", "want", "was", "way", "we", "well",
    "were", "what", "when", "where", "which", "while", "who", "why", "will",
    "with", "would", "you", "your", "youre", "yours",
}

_WORD = re.compile(r"[a-z0-9']+")
# Years, and decade forms like "1690s". The bank reaches back to 325, so a
# window starting at 1800 would have let every pre-modern date through unchecked.
_YEAR = re.compile(r"\b(\d{3,4})(s?)\b")
YEAR_FLOOR, YEAR_CEILING = 300, 2099
_HASHTAG = re.compile(r"#\w+")
_SENTENCE = re.compile(r"[.!?\n]+")

# Every one of these caps a post at 6 in post-grader. The gate catches the
# mechanical ones so the human read is spent on the parts a script cannot see.
HYPE = [
    "boss babe", "bossbabe", "girlboss", "girl boss", "hustle", "grind",
    "slay", "queen", "let's go", "lets go", "letsgo", "you got this",
    "no excuses", "run don't walk", "run dont walk", "life changing",
    "life-changing", "change your life", "changed my life", "game changer",
    "game-changer", "the ultimate", "must have", "must-have", "obsessed",
    "crushing it", "level up", "dream life", "trust the process",
]

# "one" and "once" are left out. They are pronouns as often as counts, and a
# human still reads every post. Everything here is a count almost every time.
SPELLED = [
    "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty",
    "fifty", "sixty", "seventy", "eighty", "ninety", "hundred", "thousand",
]


def stem(word):
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def tokens(text):
    """Content words only, stemmed. Digits are kept, they carry the history."""
    raw = _WORD.findall((text or "").lower().replace("-", " ").replace("_", " "))
    return {stem(w) for w in raw if w not in STOPWORDS and len(w) >= 3}


def sentences(text):
    return [s.strip() for s in _SENTENCE.split(text or "") if s.strip()]


def claimed_years(text):
    """Every year a post asserts. Returns (year, is_decade) pairs.

    A bare 3 or 4 digit number in a Gentle Muse caption is a date almost every
    time. When it is not, the override exists and the SOP says to use it.
    """
    out = []
    for match in _YEAR.finditer(text or ""):
        if match.start() and (text[match.start() - 1] in "$#" or text[match.start() - 1].isdigit()):
            continue
        year = int(match.group(1))
        if YEAR_FLOOR <= year <= YEAR_CEILING:
            out.append((year, bool(match.group(2))))
    return out


def body_of(post):
    """Everything a reader sees. Hook, caption and on-screen text all count."""
    parts = [post.get("hook"), post.get("caption"), post.get("cta")]
    screen = post.get("on_screen")
    if isinstance(screen, list):
        parts.extend(str(s) for s in screen)
    elif screen:
        parts.append(str(screen))
    return "\n".join(p for p in parts if p)


# ---------------------------------------------------------------- findings

class Finding:
    def __init__(self, code, level, post, message):
        self.code = code
        self.level = level          # FAIL | HOLD | NOTE
        self.post = post
        self.message = message

    def line(self):
        return "  [%s] %-22s %s\n      %s" % (self.level, self.code, self.post, self.message)


# ---------------------------------------------------------------- the checks

def check_post(post, bank, calendar, era, reuse_days, batch_seen, index):
    found = []
    title = post.get("title") or post.get("fact_id") or "post %d" % index
    add = lambda code, level, message: found.append(Finding(code, level, title, message))

    body = body_of(post)
    overridden = str(post.get("override") or "").strip().lower() in ("true", "yes", "1")
    reason = (post.get("override_reason") or post.get("match_reason") or "").strip()

    fact_id = (post.get("fact_id") or "").strip()
    holiday_id = (post.get("holiday_id") or "").strip()
    platform = (post.get("platform") or "").strip().lower()

    post_date = None
    if post.get("post_date"):
        try:
            post_date = date(*(int(p) for p in str(post["post_date"]).split("-")))
        except (ValueError, TypeError):
            add("E05_BAD_DATE", "FAIL",
                'post_date "%s" is not a date. Use YYYY-MM-DD.' % post["post_date"])

    # ---- the HOLD lane. The only legal way to ship a holiday post with no fact.
    if fact_id.upper() == "HOLD":
        if not body.strip():
            add("E00_EMPTY", "FAIL", "HOLD post with no text at all. Write the angle or drop it.")
        else:
            add("H01_NEEDS_FACT", "HOLD",
                'no fact bound. The bank has nothing sourced for this beat yet. '
                "Write the fact into the bank, with where it came from. "
                "Do not reach for a fact from another holiday.")
        return found

    if not body.strip():
        add("E00_EMPTY", "FAIL", "post has no hook, caption or on-screen text.")
        return found

    # ---- the fact must exist, and be usable
    if not fact_id:
        add("E01_NO_FACT_ID", "FAIL",
            'no fact_id. A holiday post makes a claim about the past, so it binds to a '
            'bank row or it says "HOLD". There is no third option.')
        return found

    fact = bank.get(fact_id)
    if fact is None:
        add("E01_UNKNOWN_FACT", "FAIL",
            'fact_id "%s" is not in the fact bank. This is the invented-history failure. '
            "Add the fact with a source, or HOLD the post." % fact_id)
        return found

    problems = usable_problems(fact)
    if problems:
        add("E02_UNUSABLE_FACT", "FAIL",
            '"%s" cannot carry a post: %s. Fix the bank row first.'
            % (fact_id, "; ".join(problems)))
        return found

    fact_text = fact.get("Fact", "")
    backbone = fact.get("Backbone", "")
    fact_holiday = (fact.get("HolidayID") or "").strip()
    fact_years = parse_years(fact.get("Year"))
    fact_year = fact_years[0] if fact_years else None
    era_year = parse_year(fact.get("EraYear"))

    # ---- the holiday must exist, and must be the fact's own holiday
    row = calendar.get(holiday_id)
    if not holiday_id:
        add("E03_NO_HOLIDAY", "FAIL", "no holiday_id. Name the holiday this post belongs to.")
    elif row is None:
        add("E03_UNKNOWN_HOLIDAY", "FAIL",
            'holiday_id "%s" is not in the calendar.' % holiday_id)
    elif fact_holiday and fact_holiday != holiday_id:
        add("E04_WRONG_HOLIDAY", "FAIL",
            '"%s" belongs to "%s" in the bank, but this post is filed under "%s". '
            "This is substitution: a fact borrowed from a holiday it does not belong to."
            % (fact_id, fact_holiday, holiday_id))

    # ---- season
    if row is not None and post_date is not None:
        landed = in_season(row, post_date, calendar)
        if landed is None:
            add("E05_OUT_OF_SEASON", "FAIL",
                "%s is outside the %s season (%s days lead, %s tail). Move the date or "
                "widen LeadDays in the calendar."
                % (post_date, holiday_id, row.get("LeadDays"), row.get("TailDays")))

    # ---- the era window. This is the emotional field, and it is checkable.
    if era_year is not None and not (era[0] <= era_year <= era[1]):
        add("E06_ERA_BREAK", "FAIL",
            '"%s" references %d. The window is %d to %d, which is what Amanda actually '
            "watched. Outside it, the nostalgia is somebody else's."
            % (fact_id, era_year, era[0], era[1]))

    supported = set(fact_years) | ({era_year} if era_year is not None else set())
    for year, decade in sorted(set(claimed_years(body))):
        if decade:
            # "the 1690s" is a fair paraphrase of 1692. A decade is covered when
            # something the bank sources falls inside it.
            covered = any(year <= y <= year + 9 for y in supported)
            if covered or (year <= era[1] and year + 9 >= era[0]):
                continue
        elif year in supported or era[0] <= year <= era[1]:
            continue
        if overridden and len(reason) >= 10:
            add("N01_OVERRIDE", "NOTE",
                'caption names %s, which "%s" does not source. Overridden: %s'
                % ("the %ds" % year if decade else str(year), fact_id, reason))
            continue
        add("E07_UNSOURCED_YEAR", "FAIL",
            'caption names %s. "%s" sources %s and the era window is %d to %d. '
            "A date in a history post either comes from the bank or it does not go out. "
            'Add a bank row for it, or set "override": true with an override_reason '
            "naming the source."
            % ("the %ds" % year if decade else "the year %d" % year, fact_id,
               ", ".join(str(y) for y in sorted(supported)) or "no year",
               era[0], era[1]))

    # ---- did the post actually tell the fact it cites?
    fact_words = tokens(fact_text)
    body_words = tokens(body)
    shared = fact_words & body_words
    if len(shared) < 2:
        if overridden and len(reason) >= 10:
            add("N02_OVERRIDE", "NOTE",
                'post shares little with "%s". Overridden: %s' % (fact_id, reason))
        else:
            add("E08_FACT_NOT_TOLD", "FAIL",
                'the post cites "%s" but never says it. Shared wording: %s. A fact_id that '
                "does not appear in the writing is decoration, and the claim it is standing "
                "behind is unverified."
                % (fact_id, sorted(shared) or "none"))

    # ---- the backbone. A fact with no turn is a trivia account, not Gentle Muse.
    backbone_words = tokens(backbone)
    carries_backbone = len(backbone_words & body_words) >= 2
    turn_sentences = [
        s for s in sentences(body)
        if len(tokens(s)) >= 4
        and (not fact_words or len(tokens(s) & fact_words) / max(1, len(tokens(s))) < 0.4)
    ]
    if not carries_backbone and not turn_sentences:
        add("E09_NO_TURN", "FAIL",
            "the post reports the fact and stops. There is no line that says why it matters. "
            'The bank has the turn for this one: "%s". Say it in her words, do not paste it.'
            % backbone.strip())

    # ---- voice. The mechanical half of post-grader's auto-fails.
    if "\u2014" in body or "\u2013" in body:
        add("E10_EM_DASH", "FAIL",
            "em dash or en dash in the copy. Use a period or a comma. This one is strict.")
    elif re.search(r"\s-\s", body):
        add("N04_SPACED_HYPHEN", "NOTE",
            "a spaced hyphen is standing in for an em dash. Same job, same rule.")

    spelled = sorted({w for w in _WORD.findall(body.lower()) if w in SPELLED})
    if spelled:
        add("E11_SPELLED_NUMBER", "FAIL",
            "spelled-out number(s): %s. Use digits." % ", ".join(spelled))

    hits = sorted({p for p in HYPE if p in body.lower()})
    if hits:
        add("E13_HYPE", "FAIL",
            "hype or generic motivation: %s. This caps the post at 6 in post-grader."
            % ", ".join('"%s"' % h for h in hits))

    tags = post.get("hashtags")
    if isinstance(tags, list):
        tag_list = [str(t) for t in tags]
    else:
        tag_list = _HASHTAG.findall(body)
    if len(tag_list) > 5:
        add("E12_HASHTAG_COUNT", "FAIL",
            "%d hashtags. The limit is 5." % len(tag_list))

    # ---- platform
    # "Comment RESET" in any casing of the verb, but the keyword itself is shouted.
    if platform == "tiktok" and re.search(r"(?i:\bcomment)\s+[A-Z]{3,}\b", body):
        add("E14_PLATFORM", "FAIL",
            'TikTok cannot fire comment-to-DM. Use "link in bio" instead of a keyword CTA.')
    if platform in ("youtube", "shorts", "youtube shorts") and not (post.get("title") or "").strip():
        add("E14_PLATFORM", "FAIL", "YouTube Shorts needs a real searchable title.")

    # ---- reuse
    if fact_id in batch_seen:
        add("E15_REUSE", "FAIL",
            '"%s" is already used by "%s" in this batch. One fact, one post.'
            % (fact_id, batch_seen[fact_id]))
    else:
        batch_seen[fact_id] = title

    last_used = (fact.get("LastUsed") or "").strip()
    if last_used and post_date:
        try:
            used_on = date(*(int(p) for p in last_used.split("-")))
            if abs((post_date - used_on).days) < reuse_days:
                add("E15_REUSE", "FAIL",
                    '"%s" was last used %s, %d days from this post. The reuse window is %d days.'
                    % (fact_id, used_on, abs((post_date - used_on).days), reuse_days))
        except (ValueError, TypeError):
            add("E15_REUSE", "FAIL",
                'bank row "%s" has LastUsed "%s", which is not a date.' % (fact_id, last_used))

    if fact_year and str(fact_year) not in body:
        add("N03_YEAR_ABSENT", "NOTE",
            'the fact is dated %d and the post never says so. A date is usually the most '
            "interesting word in the sentence." % fact_year)

    return found


# ---------------------------------------------------------------- io

def load_posts(path):
    if os.path.isdir(path):
        paths = sorted(os.path.join(path, n) for n in os.listdir(path)
                       if n.lower().endswith(".json"))
    else:
        paths = [path]
    posts = []
    for file_path in paths:
        with open(file_path, encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            posts.extend(data)
        elif isinstance(data, dict) and isinstance(data.get("posts"), list):
            posts.extend(data["posts"])
        else:
            posts.append(data)
    return posts, paths


def main():
    parser = argparse.ArgumentParser(
        description="Verify every historical claim in a holiday caption against the fact bank.")
    parser.add_argument("--post", required=True, help="caption JSON file, or a folder of them")
    parser.add_argument("--bank", default=DEFAULT_BANK)
    parser.add_argument("--calendar", default=DEFAULT_CALENDAR)
    parser.add_argument("--era", default="%d-%d" % (ERA_START, ERA_END),
                        help="nostalgia window, default %d-%d" % (ERA_START, ERA_END))
    parser.add_argument("--reuse-days", type=int, default=365,
                        help="how long a fact rests before reuse, default 365")
    parser.add_argument("--report", help="optional CSV of every finding")
    parser.add_argument("--quiet", action="store_true", help="print the verdict line only")
    args = parser.parse_args()

    try:
        era = tuple(int(p) for p in args.era.split("-"))
        if len(era) != 2 or era[0] > era[1]:
            raise ValueError
    except ValueError:
        raise SystemExit('--era must look like 1989-1999, got "%s"' % args.era)

    bank = load_bank(args.bank)
    calendar = load_calendar(args.calendar)
    posts, sources = load_posts(args.post)

    findings, batch_seen = [], {}
    for index, post in enumerate(posts, start=1):
        if not isinstance(post, dict):
            findings.append(Finding("E00_BAD_POST", "FAIL", "post %d" % index,
                                    "entry is not an object."))
            continue
        findings.extend(check_post(post, bank, calendar, era,
                                   args.reuse_days, batch_seen, index))

    fails = [f for f in findings if f.level == "FAIL"]
    holds = [f for f in findings if f.level == "HOLD"]
    notes = [f for f in findings if f.level == "NOTE"]

    if not args.quiet:
        print("GM-Holiday-Check")
        print("  bank  : %s  (%d facts, %d usable)"
              % (args.bank, len(bank), sum(1 for f in bank.values() if not usable_problems(f))))
        print("  posts : %s  (%d post%s)"
              % (args.post, len(posts), "" if len(posts) == 1 else "s"))
        print("  era   : %d to %d" % era)
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
            writer.writerow(["Level", "Code", "Post", "Finding"])
            for f in findings:
                writer.writerow([f.level, f.code, f.post, f.message])
        if not args.quiet:
            print("report written: %s" % args.report)

    if fails:
        print("VERDICT: FAIL — %d blocking finding%s. Nothing ships."
              % (len(fails), "" if len(fails) == 1 else "s"))
        return 1
    if holds:
        print("VERDICT: HOLD — %d post%s waiting on a fact. The rest is clean. "
              "Do not substitute." % (len(holds), "" if len(holds) == 1 else "s"))
        return 2
    print("VERDICT: PASS — %d post%s, every claim traced to a sourced fact.%s"
          % (len(posts), "" if len(posts) == 1 else "s",
             " %d note(s)." % len(notes) if notes else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
