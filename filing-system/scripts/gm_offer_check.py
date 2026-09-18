#!/usr/bin/env python3
"""Refuse to publish a price Amanda has not shipped, and a ladder with no rungs.

Run 9 doctrine. The pivot to HANDLED arrived as three prose handoffs, each
carrying its own copy of the prices, the keywords and the offer names. Prose
drifts. On 2026-09-17 the handoff that called itself the single source of truth
was wrong about 5 standing facts at the moment it was written, and proposed a
monthly price that was already the price of a different product.

The handoffs answer this with a rule: "when one of us changes a standing fact,
the others update every downstream artifact in the same turn." That is guidance
governing judgment, and judgment is what already failed. Run 6 established what
to do instead. Add the missing table and a check that refuses to ship without
it.

The missing table is data/offer-ladder.csv. The missing field is PriceStatus,
and it is not anybody's memory of whether Amanda approved something. It is
evidenced by where the price actually lives:

  live        a customer can see this price right now, on a published surface
  drafted     written into an automation that is not published
  proposed    exists only in a document
  unverified  named in a document and found nowhere at all

Three modes.

  --ladder    audits the ladder itself: references resolve, a bundle's parts
              exist, a paid rung leads somewhere.
  --queue     reads the post queue. A caption may never carry a price at all.
              A surface that may carry one may only carry a live price.
              Keywords are gm_cta_check.py's job, not this one's.
  --sync      reads a live Blotato automations export and reports every place
              the tables and the platform disagree.

  python3 gm_offer_check.py --ladder
  python3 gm_offer_check.py --queue queue.json
  python3 gm_offer_check.py --sync automations.json

Exit 0 PASS, 1 FAIL, 2 HOLD. No third-party packages. Python 3.8+.
"""
import argparse
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
LADDER = os.path.join(DATA, "offer-ladder.csv")
MAGNETS = os.path.join(DATA, "magnet-map.csv")

PRICE_STATUS = {"live", "drafted", "proposed", "unverified"}
OFFER_STATUS = {"live", "draft", "proposed", "unverified", "orphaned"}

# A price may appear on these. It may never appear on the others.
PRICE_SURFACES = {"page", "dm", "form", "email"}
MUTE_SURFACES = {"caption", "onscreen", "voiceover"}
ALL_SURFACES = PRICE_SURFACES | MUTE_SURFACES

MONEY = re.compile(r"\$\s?([\d,]+(?:\.\d{1,2})?)")
DOLLARS = re.compile(r"\b([\d,]+(?:\.\d{1,2})?)\s*dollars?\b", re.I)

def norm(s):
    return (s or "").strip()


def split_ids(s):
    return [x.strip() for x in norm(s).split("|") if x.strip()]


def as_price(s):
    s = norm(s).replace(",", "")
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def money(text):
    """Every price a piece of text asserts, as floats."""
    out = set()
    for m in list(MONEY.finditer(text or "")) + list(DOLLARS.finditer(text or "")):
        v = as_price(m.group(1))
        if v is not None:
            out.add(v)
    return out


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def load_ladder(path):
    rows = load_csv(path)
    for r in rows:
        r["_id"] = norm(r.get("OfferID"))
        r["_price"] = as_price(r.get("Price"))
        r["_pstatus"] = norm(r.get("PriceStatus")).lower()
        r["_status"] = norm(r.get("Status")).lower()
        r["_bundles"] = split_ids(r.get("Bundles"))
        r["_repack"] = split_ids(r.get("Repackages"))
        r["_credits"] = split_ids(r.get("CreditsToward"))
        r["_accounts"] = set(split_ids(r.get("LiveAccountIds")))
    return rows


def load_magnets(path):
    rows = load_csv(path)
    for r in rows:
        r["_kw"] = norm(r.get("Keyword")).upper()
        r["_accounts"] = set(split_ids(r.get("LiveAccountIds")))
        r["_url"] = norm(r.get("URL")).rstrip("/")
        r["_status"] = norm(r.get("Status")).lower() or "live"
    return rows


# ---------------------------------------------------------------- the ladder

def audit_ladder(rows):
    findings = []

    def add(code, oid, msg):
        findings.append({"code": code, "id": oid, "msg": msg})

    known = {r["_id"] for r in rows if r["_id"]}
    by_kw = {}
    top = max((int(r.get("Rung") or 0) for r in rows), default=0)

    for r in rows:
        oid = r["_id"] or "(blank)"
        name = norm(r.get("Offer")) or oid

        if not r["_id"]:
            add("L02_BAD_FIELD", oid, "a rung with no OfferID cannot be referenced by anything")
        if not norm(r.get("Evidence")):
            add("L01_NO_EVIDENCE", oid,
                "%s names a price and a status with nothing behind them" % name)
        if r["_pstatus"] not in PRICE_STATUS:
            add("L02_BAD_FIELD", oid, "PriceStatus '%s' is not one of %s"
                % (r.get("PriceStatus"), ", ".join(sorted(PRICE_STATUS))))
        if r["_status"] not in OFFER_STATUS:
            add("L02_BAD_FIELD", oid, "Status '%s' is not one of %s"
                % (r.get("Status"), ", ".join(sorted(OFFER_STATUS))))

        kw = norm(r.get("Keyword")).upper()
        if kw:
            by_kw.setdefault(kw, []).append(oid)

        # every reference has to resolve, or the ladder is describing a rung
        # that does not exist
        for field, refs in (("Bundles", r["_bundles"]),
                            ("Repackages", r["_repack"]),
                            ("CreditsToward", r["_credits"])):
            for ref in refs:
                if ref not in known:
                    add("L07_UNKNOWN_REF", oid,
                        "%s names %s, which is not a rung on this ladder" % (field, ref))

        # a bundle cannot be priced while nobody has found its parts
        for ref in r["_bundles"]:
            part = next((x for x in rows if x["_id"] == ref), None)
            if part is not None and part["_pstatus"] == "unverified":
                add("L04_UNVERIFIED_COMPONENT", oid,
                    "%s bundles %s (%s), which is named in a document and found nowhere"
                    % (name, ref, norm(part.get("Offer"))))

        # a live rung nobody can reach is not live
        if r["_status"] == "live" and not kw and not norm(r.get("URL")):
            add("L08_NO_PATH", oid, "%s is live with no keyword and no URL, so there is no way in" % name)

        # the Codie mechanic: every tier lowers the risk of buying the next.
        # A paid rung that credits toward nothing is where the ladder stops.
        if (r["_price"] or 0) > 0 and not r["_credits"] \
                and int(r.get("Rung") or 0) < top and r["_status"] in ("live", "draft"):
            add("L05_NO_BRIDGE", oid,
                "%s takes money and credits toward nothing, so a buyer here has no next step"
                % name)

    for kw, ids in by_kw.items():
        if len(ids) > 1:
            add("L03_KEYWORD_COLLISION", ids[1],
                "%s is claimed by %s, so a comment cannot route to one of them"
                % (kw, " and ".join(ids)))

    # two rungs at the same price is how $750 became both the Chaos Cleanup
    # Plan and the proposed monthly retainer
    seen = {}
    for r in rows:
        if r["_price"] is None or r["_price"] <= 0:
            continue
        key = (r["_price"], norm(r.get("Unit")).lower())
        if key in seen and norm(r.get("Rung")) != norm(seen[key].get("Rung")):
            findings.append({
                "code": "L06_PRICE_COLLISION", "id": r["_id"],
                "msg": "%s and %s are both $%s %s on different rungs"
                       % (norm(seen[key].get("Offer")), norm(r.get("Offer")),
                          norm(r.get("Price")), norm(r.get("Unit")))})
        else:
            seen[key] = r

    # a proposed rung that reprices a real one is a decision, not a defect
    for r in rows:
        for ref in r["_repack"]:
            was = next((x for x in rows if x["_id"] == ref), None)
            if was is None or was["_price"] is None or r["_price"] is None:
                continue
            if was["_price"] != r["_price"]:
                findings.append({
                    "code": "H01_REPRICE_PENDING", "id": r["_id"],
                    "msg": "%s is proposed at $%s where %s is %s at $%s. Amanda decides."
                           % (norm(r.get("Offer")), norm(r.get("Price")),
                              norm(was.get("Offer")), was["_pstatus"], norm(was.get("Price")))})

    return findings


# ----------------------------------------------------------------- the queue

def check_queue(rows, ladder, magnets):
    findings = []

    def add(code, row, msg):
        findings.append({"code": code, "id": row.get("id", "?"), "msg": msg})

    live_prices = {r["_price"] for r in ladder if r["_pstatus"] == "live" and r["_price"] is not None}
    by_price = {}
    for r in ladder:
        if r["_price"] is not None:
            by_price.setdefault(r["_price"], []).append(r)

    for row in rows:
        text = row.get("text") or ""
        surface = norm(row.get("surface")).lower() or "caption"

        if surface not in ALL_SURFACES:
            add("Q04_BAD_SURFACE", row,
                "surface '%s' is not one of %s" % (surface, ", ".join(sorted(ALL_SURFACES))))
            continue

        found = money(text)

        if surface in MUTE_SURFACES:
            for v in sorted(found):
                add("Q01_PRICE_IN_CAPTION", row,
                    "a %s may never carry a price and this one says $%s"
                    % (surface, ("%g" % v)))
        else:
            for v in sorted(found):
                rungs = by_price.get(v, [])
                if not rungs:
                    add("Q03_UNKNOWN_PRICE", row,
                        "says $%s, which is not a price on the ladder" % ("%g" % v))
                elif v not in live_prices:
                    r = rungs[0]
                    add("Q02_UNAPPROVED_PRICE", row,
                        "says $%s for %s, which is %s and has never shipped"
                        % ("%g" % v, norm(r.get("Offer")), r["_pstatus"]))

    return findings


# ------------------------------------------------------------------ the sync

def price_in(text):
    return money(text)


def load_export(path):
    doc = json.load(open(path, encoding="utf-8"))
    if isinstance(doc, dict):
        doc = doc.get("automations") or doc.get("items") or []
    out = []
    for a in doc:
        kws = set()
        for t in a.get("triggers") or []:
            for k in t.get("keywords") or []:
                kws.add(str(k).strip().upper())
        urls = [str(b.get("url") or "").rstrip("/") for b in (a.get("buttons") or []) if b.get("url")]
        out.append({
            "id": str(a.get("id") or ""),
            "account": str(a.get("accountId") or ""),
            "platform": str(a.get("platform") or ""),
            "name": str(a.get("name") or ""),
            "keywords": kws,
            "urls": urls,
            "dm": str(a.get("dmMessage") or ""),
            "live": bool(a.get("isActive")) and bool(a.get("publishedVersionId")),
        })
    return out


def sync(export, ladder, magnets, scope=None):
    """scope limits the comparison to named keywords, for checking one change."""
    if scope:
        magnets = [m for m in magnets if m["_kw"] in scope]
        ladder = [r for r in ladder if norm(r.get("Keyword")).upper() in scope]
    findings, notes = [], []

    def add(code, who, msg):
        findings.append({"code": code, "id": who, "msg": msg})

    live = [a for a in export if a["live"]]

    for m in magnets:
        kw = m["_kw"]
        serving = [a for a in live if kw in a["keywords"]]
        if m["_status"] == "live" and not serving:
            add("S01_NOT_LIVE", kw,
                "the map calls %s live and no published automation answers it" % kw)
            continue
        if m["_status"] != "live" and serving:
            add("S01_NOT_LIVE", kw,
                "the map calls %s %s and automation %s is published and answering it"
                % (kw, m["_status"], serving[0]["id"]))
            continue
        if not serving:
            continue

        have = {a["account"] for a in serving}
        if have != m["_accounts"]:
            add("S03_ACCOUNT_DRIFT", kw,
                "%s answers on %s, the map says %s"
                % (kw, "|".join(sorted(have)) or "nothing", "|".join(sorted(m["_accounts"])) or "nothing"))

        urls = {u for a in serving for u in a["urls"]}
        if m["_url"] and urls and m["_url"] not in urls:
            add("S05_URL_DRIFT", kw,
                "%s sends people to %s, the map says %s"
                % (kw, sorted(urls)[0], m["_url"]))

    mapped = {m["_kw"] for m in magnets}
    for r in ladder:
        kw = norm(r.get("Keyword")).upper()
        if not kw or r["_price"] is None:
            continue
        serving = [a for a in export if kw in a["keywords"]]
        said = set()
        for a in serving:
            said |= price_in(a["dm"])
        if said and r["_price"] not in said:
            add("S04_PRICE_DRIFT", r["_id"],
                "the ladder prices %s at $%s, the %s DM says $%s"
                % (norm(r.get("Offer")), norm(r.get("Price")), kw,
                   ", $".join("%g" % v for v in sorted(said))))

    for a in live:
        unmapped = {k for k in a["keywords"] if k not in mapped}
        if unmapped and not (a["keywords"] & mapped):
            notes.append("%-12s %-8s %s" % (sorted(unmapped)[0], a["account"], a["name"][:48]))

    return findings, notes


# ----------------------------------------------------------------------- cli

def report(findings, quiet, header):
    fails = [f for f in findings if not f["code"].startswith("H")]
    holds = [f for f in findings if f["code"].startswith("H")]
    if not quiet:
        for f in sorted(findings, key=lambda f: (f["code"], f["id"])):
            print("%-25s %-8s %s" % (f["code"], f["id"], f["msg"]))
        print("\n%s: %d findings (%d fail, %d hold)"
              % (header, len(findings), len(fails), len(holds)))
    return 1 if fails else (2 if holds else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ladder", nargs="?", const=LADDER, metavar="CSV",
                    help="audit the offer ladder")
    ap.add_argument("--queue", metavar="JSON", help="check a post queue for prices and keywords")
    ap.add_argument("--sync", metavar="JSON", help="a live Blotato automations export")
    ap.add_argument("--scope", metavar="KW,KW", default="",
                    help="limit --sync to these keywords, for checking one change")
    ap.add_argument("--ladder-file", default=LADDER)
    ap.add_argument("--magnets", default=MAGNETS)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if not (a.ladder or a.queue or a.sync):
        ap.error("nothing to check. Pass --ladder, --queue or --sync.")

    ladder_path = a.ladder if isinstance(a.ladder, str) else a.ladder_file
    try:
        ladder = load_ladder(ladder_path)
        magnets = load_magnets(a.magnets)
    except FileNotFoundError as e:
        print("cannot read %s. Nothing is checked and nothing is assumed." % e.filename)
        return 2

    worst = 0

    if a.ladder:
        worst = max(worst, report(audit_ladder(ladder), a.quiet,
                                  "%d rungs audited" % len(ladder)))

    if a.queue:
        try:
            rows = json.load(open(a.queue, encoding="utf-8"))
        except (OSError, ValueError) as e:
            print("cannot read the queue: %s" % e)
            return 2
        if isinstance(rows, dict):
            rows = rows.get("items") or rows.get("posts") or []
        if not a.quiet and a.ladder:
            print()
        worst = max(worst, report(check_queue(rows, ladder, magnets), a.quiet,
                                  "%d posts checked" % len(rows)))

    if a.sync:
        try:
            export = load_export(a.sync)
        except (OSError, ValueError) as e:
            print("cannot read the export: %s" % e)
            return 2
        scope = {w.strip().upper() for w in a.scope.split(",") if w.strip()}
        findings, notes = sync(export, ladder, magnets, scope)
        if not a.quiet and (a.ladder or a.queue):
            print()
        worst = max(worst, report(findings, a.quiet,
                                  "%d automations read" % len(export)))
        if notes and not a.quiet:
            print("\nLive and not in the magnet map (%d). Affiliate and PR "
                  "automations live outside it on purpose:" % len(notes))
            for n in sorted(notes):
                print("  " + n)

    return worst


if __name__ == "__main__":
    sys.exit(main())
