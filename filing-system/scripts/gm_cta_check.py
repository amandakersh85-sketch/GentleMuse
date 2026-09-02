#!/usr/bin/env python3
"""Refuse to ship a post whose call to action cannot work where it is going.

Run 6 doctrine. Captions kept naming a keyword on platforms that have no
listener, and kept carrying a link to a magnet the caption never mentions.
Guidance did not fix it twice. The missing data was a map of which keyword is
actually live on which account, and which platforms take a keyword at all.
This is the check that reads that map and refuses.

  python3 gm_cta_check.py --queue queue.json
  python3 gm_cta_check.py --queue queue.json --magnets M.csv --platforms P.csv

Each queue row needs: id, platform, accountId, text. Optional: at, magnet.
Exit 0 PASS, 1 FAIL, 2 HOLD.
"""
import argparse, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")

ACTION = re.compile(r"\b(follow|share|save|like|subscribe|repost)\b", re.I)
URL = re.compile(r"https?://[^\s<>\")]+")
BIO = re.compile(r"\bin (?:my|the) bio\b|\blink in bio\b", re.I)


def load_magnets(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            kw = (r.get("Keyword") or "").strip().upper()
            if not kw:
                continue
            r["_accounts"] = {a.strip() for a in (r.get("LiveAccountIds") or "").split("|") if a.strip()}
            r["_url"] = (r.get("URL") or "").strip().rstrip("/")
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

        # P02 keyword named, magnet link present, and they disagree
        for kw in named:
            want = magnets[kw]["_url"]
            others = [u for u in urls if any(
                m["_url"] and m["_url"] in u and m["_url"] != want for m in magnets.values())]
            if others and not any(want and want in u for u in urls):
                add("P02_WRONG_LINK", row,
                    "says %s but links %s, which is a different magnet" % (kw, others[0]))

        # P03 magnet link with no mention of that magnet anywhere in the caption
        for m in magnets.values():
            u = m["_url"]
            if not u or not any(u in x for x in urls):
                continue
            kw = (m["Keyword"] or "").upper()
            title = (m["Magnet"] or "").lower()
            words = [w for w in re.split(r"[^a-z]+", title) if len(w) > 3]
            mentioned = (kw in named) or any(w in text.lower() for w in words)
            if not mentioned:
                add("P03_LINK_WITHOUT_MENTION", row,
                    "carries the %s link but the caption never mentions %s" % (kw, m["Magnet"]))

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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True)
    ap.add_argument("--magnets", default=os.path.join(DATA, "magnet-map.csv"))
    ap.add_argument("--platforms", default=os.path.join(DATA, "platform-cta.csv"))
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    rows = json.load(open(a.queue, encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("items") or rows.get("posts") or []
    findings = check(rows, load_magnets(a.magnets), load_platforms(a.platforms))

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
