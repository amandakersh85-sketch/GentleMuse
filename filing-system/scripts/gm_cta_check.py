#!/usr/bin/env python3
"""Refuse to ship a post whose call to action cannot work where it is going.

Run 6 doctrine. Captions kept naming a keyword on platforms that have no
listener, and kept carrying a link to a magnet the caption never mentions.
Guidance did not fix it twice. The missing data was a map of which keyword is
actually live on which account, and which platforms take a keyword at all.
This is the check that reads that map and refuses.

  python3 gm_cta_check.py --queue queue.json
  python3 gm_cta_check.py --queue queue.json --magnets M.csv --platforms P.csv
  python3 gm_cta_check.py --queue queue.json --paid-window 120

Each queue row needs: id, platform, accountId, text. Optional: at, magnet.
Exit 0 PASS, 1 FAIL, 2 HOLD.
"""
import argparse, csv, json, os, re, sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

ACTION = re.compile(r"\b(follow|share|save|like|subscribe|repost)\b", re.I)
URL = re.compile(r"https?://[^\s<>\")]+")
BIO = re.compile(r"\bin (?:my|the) bio\b|\blink in bio\b", re.I)

# "comment WAITLIST" — a word handed to the reader as if it were a keyword.
# The map only knew the keywords that exist, so a word that was never a keyword
# was invisible to every check here.
#
# The word "comment" is matched in any case. It was case-sensitive when this
# went in, which meant the capitalised form that starts most sentences, and
# therefore most captions, walked straight past. Fixing that was only safe once
# the map covered every live keyword rather than the lead magnets alone: the 23
# affiliate keywords and the 13 PR screening phrases are real working capture
# paths, and refusing them as invented would have blocked every brand deal.
KEYWORD_CTA = re.compile(r"\b(?i:comment)(?:\s+the\s+word)?\s+([A-Z][A-Z0-9]{2,})\b")

# Allcaps words that follow "comment" without being offered as keywords.
NOT_A_KEYWORD = {"BELOW", "YES", "NO", "OK", "HERE", "THIS", "IT", "AND", "ME"}

# queue-zones.csv defines the PAID zone as anything carrying one of these.
PAID = re.compile(r"#ad\b|#TargetPartner\b", re.I)


def load_magnets(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            kw = (r.get("Keyword") or "").strip().upper()
            if not kw:
                continue
            r["_accounts"] = {a.strip() for a in (r.get("LiveAccountIds") or "").split("|") if a.strip()}
            r["_url"] = (r.get("URL") or "").strip().rstrip("/")
            r["_status"] = (r.get("Status") or "live").strip().lower() or "live"
            out[kw] = r
    return out


def load_platforms(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            aid = (r.get("AccountId") or "").strip()
            if not aid:
                continue
            r["_actions"] = {a.strip().lower() for a in (r.get("RequiredActions") or "").split("|") if a.strip()}
            out[aid] = r
    return out


def page_claim(text):
    """Return page counts a caption asserts, e.g. '15 pages' or '13 page guide'."""
    return {m.group(1) for m in re.finditer(r"\b(\d{1,3})\s+page", text, re.I)}


def check(rows, magnets, platforms):
    findings = []

    def add(code, row, msg):
        findings.append({"code": code, "id": row.get("id", "?"),
                         "platform": row.get("platform", "?"),
                         "at": row.get("at", ""), "msg": msg})

    for row in rows:
        text = row.get("text") or ""
        aid = str(row.get("accountId") or "").strip()
        plat = platforms.get(aid)
        urls = [u.rstrip("/.,)") for u in URL.findall(text)]
        named = [kw for kw in magnets if re.search(r"\b" + kw + r"\b", text)]

        if not plat:
            add("P00_UNKNOWN_ACCOUNT", row,
                "account %s is not in platform-cta.csv, so nothing can be checked" % (aid or "(blank)"))
            continue

        # P01 keyword named where no automation listens on that account
        for kw in named:
            if aid not in magnets[kw]["_accounts"]:
                add("P01_DEAD_KEYWORD", row,
                    "says %s but no %s automation is live on %s (%s)"
                    % (kw, kw, plat["Handle"], plat["Platform"]))

        # P09 the automation behind the keyword is not published, so the
        # comment arrives and nothing answers it.
        for kw in named:
            if magnets[kw]["_status"] != "live":
                add("P09_DRAFT_KEYWORD", row,
                    "says %s, whose automation is %s and will not answer"
                    % (kw, magnets[kw]["_status"]))

        # P10 a word handed to the reader as a keyword that is not one. Every
        # other check here reads the map, so a word absent from the map was
        # never looked at. WAITLIST shipped in the launch pack this way.
        for word in KEYWORD_CTA.findall(text):
            if word in magnets or word in NOT_A_KEYWORD:
                continue
            add("P10_INVENTED_KEYWORD", row,
                "tells the reader to comment %s, and %s is in no automation" % (word, word))

        # P02 keyword named, magnet link present, and they disagree
        for kw in named:
            want = magnets[kw]["_url"]
            others = [u for u in urls if any(
                m["_url"] and m["_url"] in u and m["_url"] != want for m in magnets.values())]
            if others and not any(want and want in u for u in urls):
                add("P02_WRONG_LINK", row,
                    "says %s but links %s, which is a different magnet" % (kw, others[0]))

        # P03 magnet link with no mention of that magnet anywhere in the caption.
        # Asked per link, not per keyword. CESA and PRINCESS both deliver the
        # senior dog guide, so naming either one accounts for that one URL.
        # Per keyword, a caption that correctly says CESA was failed for not
        # also saying PRINCESS.
        by_url = {}
        for m in magnets.values():
            if m["_url"]:
                by_url.setdefault(m["_url"], []).append(m)
        for u, sharing in by_url.items():
            if not any(u in x for x in urls):
                continue
            mentioned = False
            for m in sharing:
                kw = (m["Keyword"] or "").upper()
                words = [w for w in re.split(r"[^a-z]+", (m["Magnet"] or "").lower())
                         if len(w) > 3]
                if kw in named or any(w in text.lower() for w in words):
                    mentioned = True
                    break
            if not mentioned:
                add("P03_LINK_WITHOUT_MENTION", row,
                    "carries the %s link but the caption never mentions %s"
                    % ("/".join(sorted((m["Keyword"] or "").upper() for m in sharing)),
                       sharing[0]["Magnet"]))

        # P04/P05 action platforms need an action ask and a reachable destination.
        # LinkClickable: yes = a caption URL works, bio = the link lives in the bio
        # so the caption must point there, field = the destination is a post field.
        clickable = (plat.get("LinkClickable") or "").strip().lower()
        if plat["_actions"]:
            if not ACTION.search(text):
                add("P04_NO_ACTION", row,
                    "%s takes no keyword, so it needs an ask: %s"
                    % (plat["Platform"], " / ".join(sorted(plat["_actions"]))))
            if clickable == "yes" and not urls:
                add("P05_NO_LINK", row,
                    "%s captions are clickable and this one carries no link, so there is no path off the post"
                    % plat["Platform"])
            if clickable == "bio" and not BIO.search(text) and not row.get("link"):
                add("P05_NO_LINK", row,
                    "a %s caption URL is not tappable, so the post has to send people to the bio"
                    % plat["Platform"])
            if clickable == "field" and not row.get("link"):
                add("P05_NO_LINK", row,
                    "%s carries its destination in a field and this post has none" % plat["Platform"])

        # P06 the same link pasted twice
        for u in set(urls):
            if urls.count(u) > 1:
                add("P06_DUPLICATE_LINK", row, "pastes %s %d times" % (u, urls.count(u)))

        # P07 caption promises a page count the magnet does not deliver
        claims = page_claim(text)
        for kw in named:
            want = page_claim(magnets[kw].get("Claim") or "")
            if want and claims and not (claims & want):
                add("P07_PROMISE_MISMATCH", row,
                    "promises %s pages, %s delivers %s"
                    % ("/".join(sorted(claims)), kw, "/".join(sorted(want))))

        # H01 nothing to capture with. An action ask on an action platform counts,
        # a follow is a real return even when no link is in the caption.
        acted = bool(plat["_actions"]) and bool(ACTION.search(text))
        if not named and not urls and not row.get("link") and not acted:
            add("H01_NO_CAPTURE_PATH", row,
                "no keyword, no link and no action ask, so the post cannot return anything")

    return findings


def when(row):
    """Parse a row's run time, or None when it has none to parse."""
    at = (row.get("at") or "").strip()
    if not at:
        return None
    try:
        return datetime.fromisoformat(at.replace("Z", "+00:00"))
    except ValueError:
        return None


def paid_stacking(rows, window_min):
    """Two paid posts too close on one account is a delivery failure.

    On 2026-08-21 four paid and promotional posts published to Instagram at
    22:59, 23:00, 23:01 and 23:01. They took 2, 0, 0 and 0 likes. A brand deal
    carries a delivery window and the whole point of the window is reach, so
    stacking them buries the one thing on the queue that was actually sold.
    The spacing rule in posting-cadence.csv already said 2 hours. Nothing read
    it at ship time, which is why this is a check and not a line in a file.

    Paid against paid only. Paid against organic buries the ad too, but at 7
    to 13 posts a day a paid post is almost always within 2 hours of
    something, so that rule would fire on nearly every ad and be ignored
    inside a week. Volume has to come down before that one is worth writing.
    """
    findings = []
    byacct = {}
    for row in rows:
        if not PAID.search(row.get("text") or ""):
            continue
        aid = str(row.get("accountId") or "").strip()
        t = when(row)
        if t is None:
            findings.append({"code": "H02_PAID_NO_TIME", "id": row.get("id", "?"),
                             "platform": row.get("platform", "?"), "at": "",
                             "msg": "carries #ad or #TargetPartner and has no run time, "
                                    "so its spacing cannot be checked"})
            continue
        byacct.setdefault(aid, []).append((t, row))

    for aid, items in byacct.items():
        items.sort(key=lambda x: x[0])
        for (t1, r1), (t2, r2) in zip(items, items[1:]):
            gap = (t2 - t1).total_seconds() / 60
            if gap < window_min:
                findings.append({
                    "code": "P08_PAID_STACKED", "id": r2.get("id", "?"),
                    "platform": r2.get("platform", "?"),
                    "at": r2.get("at", ""),
                    "msg": "lands %d min after paid post %s on the same account, "
                           "under the %d min minimum"
                           % (round(gap), r1.get("id", "?"), window_min)})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--magnets", default=os.path.join(DATA, "magnet-map.csv"))
    ap.add_argument("--platforms", default=os.path.join(DATA, "platform-cta.csv"))
    ap.add_argument("--paid-window", type=int, default=120, metavar="MIN",
                    help="minutes of clear air a paid post needs, default 120")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rows = json.load(open(a.queue, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("items") or rows.get("posts") or []
    findings = check(rows, load_magnets(a.magnets), load_platforms(a.platforms))
    findings += paid_stacking(rows, a.paid_window)

    fails = [f for f in findings if not f["code"].startswith("H")]
    holds = [f for f in findings if f["code"].startswith("H")]

    if not a.quiet:
        for f in sorted(findings, key=lambda f: (f["code"], f["at"])):
            print("%-24s %-10s %-9s %s" % (f["code"], f["id"], f["platform"], f["msg"]))
        print("\n%d posts checked, %d findings (%d fail, %d hold)"
              % (len(rows), len(findings), len(fails), len(holds)))

    return 1 if fails else (2 if holds else 0)


if __name__ == "__main__":
    sys.exit(main())
