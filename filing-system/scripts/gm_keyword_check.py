#!/usr/bin/env python3
"""
GM-Keyword-Check — the comment-to-DM keyword gate.

Run 9 of the Gentle Muse filing system. Reads scheduled posts and refuses any
caption that asks for a keyword the account cannot answer.

Why this exists. On 09/11 an assistant was asked whether BROW was a live
keyword. keyword-audit.csv listed 13 automations. Blotato had 57. Every Target
product keyword was missing from the file, so the honest answer read off the
repo was "there is no BROW keyword", and the true answer was that BROW had been
live on 2 accounts since 08/08. The repo held a partial copy and nothing said
so.

Guidance would not have fixed that. The reader was careful and still wrong,
because the data was not there to be careful about. So the fix is the registry
plus this gate, the same shape as the Run 6 fix: the missing column, and a
check that refuses to ship without it.

A dead keyword costs more than a missing one. Someone comments the word, waits
for a DM, and nothing arrives. That is worse than no call to action at all.

House rules, same as every other module:
  Propose-only. This script reads. It never moves, renames or deletes a file.
  Approval is the gate. A PASS is a proposal, not a publish.
  No substitution. An unknown keyword is a finding, not a nearest match.

Rules
  K01_KEYWORD_DEAD        the caption asks for a keyword with no active
                          automation on that account
  K02_KEYWORD_NO_LISTENER a keyword CTA on a platform that has no automation
                          at all. TikTok, YouTube, LinkedIn and Pinterest
                          never carry the keyword. Their CTA is the link.
  K03_KEYWORD_BROKEN      the keyword is live but its destination is marked
                          BROKEN in the registry, so the DM lands on a
                          storefront instead of the product
  K04_NO_DISCLOSURE       a caption whose keyword delivers an affiliate
                          product, with no partner or commission line in the
                          caption itself. The DM carrying it is not enough.
  K05_PRICE_ON_AFFILIATE  a price stated on affiliate content. Open TikTok
                          Shop violation from 08/04/2026.

Exit codes
  0   PASS   every keyword CTA is answerable on the account that carries it
  1   FAIL   at least one blocking finding. Nothing ships.

Usage
  python3 gm_keyword_check.py --posts queue.json
  python3 gm_keyword_check.py --posts board.csv
  python3 gm_keyword_check.py --keyword BROW --platform instagram --account 45886

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
REGISTRY = os.path.join(DATA, "keyword-registry.csv")
PLATFORM_CTA = os.path.join(DATA, "platform-cta.csv")

# "comment BROW", "comment the word BROW", "Comment BROW and I'll send it"
# The keyword is the run of capitals. Lowercase words are prose, not the ask.
ASK = re.compile(
    r"\b[Cc]omment(?:ing)?\s+(?:the\s+word\s+|with\s+|me\s+)?([A-Z][A-Z0-9]{2,15})\b"
)
# "type BROW", "reply BROW", "drop BROW below", "say BROW"
ASK_ALT = re.compile(
    r"\b(?:[Tt]ype|[Rr]eply|[Dd]rop|[Ss]ay|[Ss]end)\s+(?:the\s+word\s+)?([A-Z][A-Z0-9]{2,15})\b"
)

DISCLOSURE = re.compile(
    r"target partner|earn (?:rewards or )?commission|may earn|#ad\b|paid partnership",
    re.I,
)
PRICE = re.compile(r"\$\s?\d")

# Capitalised words that show up mid-caption and are never a keyword ask.
NOT_KEYWORDS = {
    "DM", "PDF", "AI", "USA", "OK", "TV", "CEO", "FAQ", "LOL", "PS",
    "STOP", "FREE", "NEW", "YES", "NO", "AND", "THE", "FOR", "BUT",
}


def load_registry(path=REGISTRY):
    """Every keyword the accounts can actually answer, live and retired."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        raise SystemExit("registry is empty: %s" % path)
    return rows


def load_platform_cta(path=PLATFORM_CTA):
    """Which platforms have a listener at all."""
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def keyword_works(cta_rows, platform):
    """no means the platform has no automation. partial still has listeners."""
    for row in cta_rows:
        if row["Platform"] == platform:
            return row["KeywordWorks"] != "no"
    return False


def asks(text):
    """The keywords a caption tells people to comment."""
    found = []
    for pattern in (ASK, ASK_ALT):
        for m in pattern.finditer(text or ""):
            word = m.group(1)
            if word not in NOT_KEYWORDS and word not in found:
                found.append(word)
    return found


def lookup(registry, keyword, platform, account):
    """Rows for this keyword on this exact account."""
    return [
        r for r in registry
        if r["Keyword"].upper() == keyword.upper()
        and r["Platform"] == platform
        and str(r["AccountId"]) == str(account)
    ]


def check_post(post, registry, cta_rows):
    findings = []
    pid = str(post.get("id", "?"))
    platform = (post.get("platform") or "").strip()
    account = str(post.get("accountId") or post.get("account") or "").strip()
    text = post.get("text") or post.get("caption") or ""

    wanted = asks(text)
    if not wanted:
        return findings

    listens = keyword_works(cta_rows, platform)

    for keyword in wanted:
        if not listens:
            findings.append({
                "rule": "K02_KEYWORD_NO_LISTENER", "level": "FAIL", "id": pid,
                "detail": "%s asks for %s and has no automation. The CTA on "
                          "%s is the link, never the keyword."
                          % (platform, keyword, platform),
            })
            continue

        rows = lookup(registry, keyword, platform, account)
        live = [r for r in rows if r["Active"] == "yes"]
        if not live:
            elsewhere = [
                "%s %s" % (r["Platform"], r["AccountId"])
                for r in registry
                if r["Keyword"].upper() == keyword.upper() and r["Active"] == "yes"
            ]
            where = (" It is live on " + ", ".join(elsewhere) + ".") if elsewhere \
                else " It is not live anywhere."
            findings.append({
                "rule": "K01_KEYWORD_DEAD", "level": "FAIL", "id": pid,
                "detail": "%s has no active automation for %s.%s"
                          % (account or platform, keyword, where),
            })
            continue

        row = live[0]
        if row["Note"].startswith("BROKEN"):
            findings.append({
                "rule": "K03_KEYWORD_BROKEN", "level": "FAIL", "id": pid,
                "detail": "%s fires on %s but its link is broken: %s"
                          % (keyword, account, row["Note"]),
            })

        if row["Kind"] == "product":
            if not DISCLOSURE.search(text):
                findings.append({
                    "rule": "K04_NO_DISCLOSURE", "level": "FAIL", "id": pid,
                    "detail": "%s delivers an affiliate product and the caption "
                              "carries no partner line. The DM is not enough, "
                              "the disclosure sits on the post." % keyword,
                })
            if PRICE.search(text):
                findings.append({
                    "rule": "K05_PRICE_ON_AFFILIATE", "level": "FAIL", "id": pid,
                    "detail": "a price is stated on affiliate content. Open "
                              "TikTok Shop violation from 08/04/2026.",
                })

    return findings


def load_posts(path):
    if os.path.isdir(path):
        posts = []
        for name in sorted(os.listdir(path)):
            if name.endswith(".json"):
                posts.extend(load_posts(os.path.join(path, name)))
        return posts
    if path.endswith(".csv"):
        with open(path, newline="", encoding="utf-8") as fh:
            return [
                {"id": r.get("id") or r.get("PostId"),
                 "platform": r.get("platform") or r.get("Platform"),
                 "accountId": r.get("accountId") or r.get("AccountId"),
                 "text": r.get("text") or r.get("caption") or r.get("Caption")}
                for r in csv.DictReader(fh)
            ]
    with open(path, encoding="utf-8") as fh:
        blob = json.load(fh)
    if isinstance(blob, dict):
        blob = blob.get("posts") or blob.get("items") or blob.get("schedules") or []
    return blob


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts")
    ap.add_argument("--keyword")
    ap.add_argument("--platform")
    ap.add_argument("--account")
    ap.add_argument("--registry", default=REGISTRY)
    ap.add_argument("--platform-cta", default=PLATFORM_CTA)
    args = ap.parse_args()

    registry = load_registry(args.registry)
    cta_rows = load_platform_cta(args.platform_cta)

    # The one-question mode. "Is BROW live on Instagram 45886?"
    if args.keyword:
        rows = [r for r in registry
                if r["Keyword"].upper() == args.keyword.upper()
                and r["Active"] == "yes"]
        if args.platform:
            rows = [r for r in rows if r["Platform"] == args.platform]
        if args.account:
            rows = [r for r in rows if str(r["AccountId"]) == str(args.account)]
        if not rows:
            print("%s is not live on that account" % args.keyword.upper())
            return 1
        for r in rows:
            print("%-12s %-10s %-7s automation %-6s %s"
                  % (r["Keyword"], r["Platform"], r["AccountId"],
                     r["AutomationID"], r["Delivers"]))
            print("%-12s %s" % ("", r["Destination"]))
            if r["Note"]:
                print("%-12s note: %s" % ("", r["Note"]))
        return 0

    if not args.posts:
        ap.error("give --posts or --keyword")

    posts = load_posts(args.posts)
    findings = []
    for post in posts:
        findings.extend(check_post(post, registry, cta_rows))

    live = sum(1 for r in registry if r["Active"] == "yes")
    print("%d post(s) checked against %d live keyword(s)" % (len(posts), live))
    if not findings:
        print("keywords clean")
        return 0

    print()
    for f in findings:
        print("%-24s %-5s %s" % (f["rule"], f["level"], f["id"]))
        print("%-24s   %s" % ("", f["detail"]))

    fails = [f for f in findings if f["level"] == "FAIL"]
    print()
    print("%d finding(s), %d blocking" % (len(findings), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
