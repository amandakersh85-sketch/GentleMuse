#!/usr/bin/env python3
"""Assertions for the n8n trivia trigger that are clearer here than in shell.

The node cases run the Code node from the committed daily-trivia-trigger.json
through trivia_trigger_check.js, so they test what Amanda imports, not the
source it was built from.

  python3 trivia_trigger_assert.py <case>
"""
import copy
import csv
import json
import os
import subprocess
import sys
import tempfile
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import gm_keyword_check as K  # noqa: E402
import gm_trivia_bank as B  # noqa: E402
import gm_trivia_trigger as T  # noqa: E402

FIXTURE_BANK = os.path.join(HERE, "trivia-trigger.bank.csv")
HARNESS = os.path.join(HERE, "trivia_trigger_check.js")

# The payload from the design this lane was handed on 09/28, verbatim.
PASTED = {
    "topic": "World History - Forgotten Inventions",
    "target_platform": ["YouTube Shorts", "TikTok"],
    "voice_id": "heygen_voice_123",
    "publish_date": "2026-09-29T08:00:00Z",
}


def sender_payload(fid="TRV-001", day=date(2099, 1, 1)):
    bank = B.load_bank(FIXTURE_BANK)
    lane, _ = T.load_lane_channels()
    cta, problems = T.asks_for(bank[fid], lane, K.load_registry(), K.load_platform_cta())
    if problems:
        raise SystemExit("fixture %s cannot build: %s" % (fid, problems))
    return T.build_payload(fid, bank[fid], day, lane, cta)


def verdict(body):
    fd, path = tempfile.mkstemp(suffix=".json")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(body, fh)
        out = subprocess.run(["node", HARNESS, T.WORKFLOW, path],
                             capture_output=True, text=True, check=True).stdout
    finally:
        os.unlink(path)
    return json.loads(out)


def lane_is_the_board():
    """The 4 channels that carry everything, at the main accounts HANDOFF_0909
    names. If channel-rules.csv reorders its account ids, this says so."""
    lane, other = T.load_lane_channels()
    return (lane == {
        "instagram": {"account": "45886", "cta": "comment-keyword"},
        "facebook": {"account": "30840", "cta": "comment-keyword"},
        "tiktok": {"account": "41488", "cta": "link-in-bio"},
        "youtube": {"account": "36129", "cta": "link-in-description"},
    } and {"linkedin", "twitter", "pinterest"} <= set(other))


def webhook_is_locked():
    """POST, Header Auth on, answered after the check, and no credential in git."""
    with open(T.WORKFLOW, encoding="utf-8") as fh:
        wf = json.load(fh)
    nodes = {n["name"]: n for n in wf["nodes"]}
    hook = nodes["Daily Trivia Webhook"]
    p = hook["parameters"]
    ok = (p["httpMethod"] == "POST" and p["path"] == "daily-trivia-trigger"
          and p["authentication"] == "headerAuth" and p["responseMode"] == "responseNode"
          and bool(hook.get("webhookId")) and "credentials" not in hook
          and nodes["Answer the caller"]["parameters"]["options"]["responseCode"]
          == "={{ $json.status }}")
    chain = ["Daily Trivia Webhook", "Check the payload", "Answer the caller",
             "Accepted facts only", "Next: script from the fact"]
    for a, b in zip(chain, chain[1:]):
        ok = ok and wf["connections"][a]["main"][0][0]["node"] == b
    return ok


def drift_is_caught():
    """A rule changed in the CSV and not rebuilt must fail the check."""
    with tempfile.TemporaryDirectory() as tmp:
        changed = os.path.join(tmp, "channel-rules.csv")
        with open(T.CHANNEL_RULES, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
            fields = list(rows[0].keys())
        for r in rows:
            if r["Channel"] == "twitter":
                r.update(Content="everything", MaxPerDay="3", CTA="link")
        with open(changed, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)
        r = subprocess.run([sys.executable, os.path.join(HERE, "..", "scripts",
                                                         "gm_trivia_trigger.py"),
                            "--workflow", "--check", "--channels", changed],
                           capture_output=True, text=True)
        return r.returncode == 1 and "out of date" in r.stdout


def avatar_rotates():
    d = date(2026, 9, 29)
    a, b = T.avatar_for(d)[0], T.avatar_for(d + timedelta(days=1))[0]
    return a != b and {a, b} == {x for x, _ in T.AVATARS}


def accepts_what_the_sender_builds():
    v = verdict(sender_payload())
    return v["ok"] is True and v["status"] == 202 and v["payload"]["fact_id"] == "TRV-001"


def refuses_the_pasted_design():
    v = verdict(PASTED)
    said = " | ".join(v["reasons"])
    want = ["no fact_id from trivia-fact-bank.csv", 'topic "World History - Forgotten Inventions" is '
            "outside the lane", '"YouTube Shorts" does not carry this lane',
            '"TikTok" is written tiktok here', "voice_id is not Amanda's voice",
            "publish_date must be the day"]
    missing = [w for w in want if w not in said]
    for w in missing:
        print("  missing: %s" % w)
    return v["ok"] is False and v["status"] == 422 and not missing


# Each is 1 thing the board rules out, applied to a payload that otherwise passes.
CASES = [
    ("a general trivia topic", lambda p: p.update(topic="history"), "outside the lane"),
    ("X, dropped 09/08", lambda p: p["target_platform"].append("twitter"),
     '"twitter" does not carry this lane. channel-rules.csv has it as: none'),
    ("LinkedIn, business only", lambda p: p["target_platform"].append("linkedin"),
     '"linkedin" does not carry this lane'),
    ("the keyword on TikTok", lambda p: p["cta"]["tiktok"].update(keyword="TUESDAY"),
     "tiktok never carries the comment keyword"),
    ("Instagram with no keyword", lambda p: p["cta"]["instagram"].pop("keyword"),
     "instagram asks for a comment keyword and names none"),
    ("Cesa's Instagram", lambda p: p["accounts"].update(instagram="65540"),
     "instagram goes to account 45886"),
    ("another person's voice", lambda p: p.update(voice_id="avery-voice"),
     "voice_id is not Amanda's voice"),
    ("a stock avatar", lambda p: p.update(avatar_id="stock-avatar"),
     "avatar_id is not 1 of her 2 podcast looks"),
    ("a day already past", lambda p: p.update(publish_date="2000-01-01"), "is already past"),
    ("a time instead of a day", lambda p: p.update(publish_date="2099-01-01T08:00:00Z"),
     "publish_date must be the day"),
    ("motion-text", lambda p: p.update(delivery="motion-text"),
     'delivery "motion-text" is not rendered here'),
    ("no source to check", lambda p: p.update(source_url=""), "no source_url"),
    ("never verified", lambda p: p.pop("verified_on"), "no verified_on"),
    ("YouTube with no link", lambda p: p["cta"]["youtube"].pop("link"),
     "youtube needs the link"),
]


def refuses_each_thing_ruled_out():
    base = sender_payload()
    ok = True
    for name, change, expect in CASES:
        p = copy.deepcopy(base)
        change(p)
        v = verdict(p)
        if v["ok"] or v["status"] != 422 or not any(expect in r for r in v["reasons"]):
            print("  not refused as expected: %s, got %s" % (name, v["reasons"]))
            ok = False
    v = verdict([base])
    if v["ok"] or "not a JSON object" not in v["reasons"][0]:
        print("  a list was not refused")
        ok = False
    return ok


if __name__ == "__main__":
    fn = {"lane": lane_is_the_board,
          "shape": webhook_is_locked,
          "drift-caught": drift_is_caught,
          "rotates": avatar_rotates,
          "accepts": accepts_what_the_sender_builds,
          "refuses-paste": refuses_the_pasted_design,
          "refuses-each": refuses_each_thing_ruled_out}[sys.argv[1]]
    sys.exit(0 if fn() else 1)
