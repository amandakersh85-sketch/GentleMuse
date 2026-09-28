#!/usr/bin/env python3
"""
GM-Trivia-Trigger — hands 1 checked fact to the n8n daily trivia workflow.

Added 09/28/2026 to Run 8, the trivia pipeline.

The n8n workflow for this lane starts at a webhook, daily-trivia-trigger, and
goes on to write the script with OpenAI, render it with HeyGen and schedule it
through Blotato. The design it arrived with had the webhook take a free topic,
"World History - Forgotten Inventions", and hand it to a model to write about.
That is the one input this lane is built to refuse, twice over. The topic is
outside the lane, and a model asked to write 40 seconds about a topic will
supply the numbers itself. T03 exists because those numbers are the whole risk.

So the unit of work is a fact, not a topic. This script takes 1 row from
trivia-fact-bank.csv that the bank says can carry a post, adds what the render
and the schedule need from the data that already governs them, and posts it to
the webhook. The workflow's first node runs the same checks again, because the
webhook answers anything that holds the key.

Where each part of the payload comes from
  the fact          trivia-fact-bank.csv, only when usable_problems() is empty
  platforms, asks   channel-rules.csv, the channels that carry everything
  keyword, link     keyword-registry.csv, only when live on that account
  voice, avatar     her own twin, the 2 podcast looks, rotated by day

House rules, same as every other module:
  Propose-only. Without --send nothing leaves this machine.
  Approval is the gate. Sending starts a render, not a post. Every node after
    the workflow's check has to end at HOLD for Amanda. SOP_0909 section 8.
  No substitution. A held fact is refused, not swapped for the nearest one.
  Reuse before generating. A fact already sent has a render. It is not sent
    again without --resend.

The key is read from N8N_TRIVIA_KEY and is never printed. The address is read
from N8N_TRIVIA_URL, the production URL that ends /webhook/daily-trivia-trigger.

Usage
  python3 gm_trivia_trigger.py --next                  propose the next fact
  python3 gm_trivia_trigger.py --fact TRV-001          propose this fact
  python3 gm_trivia_trigger.py --next --send           send it
  python3 gm_trivia_trigger.py --workflow --write      rebuild the n8n workflow
  python3 gm_trivia_trigger.py --workflow --check      has it drifted from the rules?

Exit codes
  0   proposed, or sent and accepted by the workflow's check
  1   refused. The fact cannot go, or the workflow's check turned it away
  2   nothing sent, or nothing confirmed. Nothing usable, no key, wrong key,
      nothing listening, or an answer that is not the check's

No third-party packages. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import sys
import urllib.error
import urllib.request
import uuid
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gm_trivia_bank as B  # noqa: E402
import gm_keyword_check as K  # noqa: E402

ROOT = os.path.dirname(HERE)
CHANNEL_RULES = os.path.join(ROOT, "data", "channel-rules.csv")
DEFAULT_LOG = os.path.join(ROOT, "data", "trivia-trigger-log.csv")
CHECK_JS = os.path.join(ROOT, "n8n", "trivia-payload-check.js")
WORKFLOW = os.path.join(ROOT, "n8n", "daily-trivia-trigger.json")

WEBHOOK_PATH = "daily-trivia-trigger"
KEY_HEADER = "X-Trivia-Key"
FACT_ID = r"^TRV-\d{3,}$"
TIMEZONE = "America/Chicago"
LOG_COLUMNS = ["SentOn", "FactID", "PublishDate", "Execution"]

# The route this workflow renders. A motion-text fact goes through the reel
# factory instead. HANDOFF_0909 section 6.
DELIVERY = ("talking-head",)

# Her own twin, never Avery or Cesa. HANDOFF_0909 section 6: the 2 podcast
# looks, because the lane is somebody telling you a thing they know. Rotated
# by day, the same way plates rotate on the reels.
VOICE_ID = "05f19352e8f74b0392a8f411eba40de1"
VOICE_SPEED = 0.92
AVATARS = (
    ("3243536278874919a784ed66c135a473", "Amanda with a podcast microphone"),
    ("96af09cd10804111a290ecb70f39500f", "Amanda hosting a live podcast"),
)


# ---------- the rules, read from the data that already holds them ----------

def load_lane_channels(path=CHANNEL_RULES):
    """The channels this lane posts to, and how the rest are described.

    Trivia goes where the board sends everything: on 09/28 that is Instagram,
    Facebook, TikTok and YouTube. LinkedIn is business only, Pinterest is
    evergreen pins, X is dropped. The first account listed is the main one.
    Cesa's accounts never carry this lane.
    """
    lane, other = {}, {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            ch = (r.get("Channel") or "").strip().lower()
            if not ch:
                continue
            content = (r.get("Content") or "").strip()
            try:
                most = int(r.get("MaxPerDay") or 0)
            except ValueError:
                most = 0
            if content.lower() == "everything" and most > 0:
                lane[ch] = {"account": (r.get("AccountIds") or "").split("|")[0].strip(),
                            "cta": (r.get("CTA") or "").strip()}
            else:
                other[ch] = content or "none"
    return lane, other


def rules(channels=CHANNEL_RULES):
    """What the workflow's check holds a payload to. Built, never typed."""
    lane, other = load_lane_channels(channels)
    return {
        "factIdPattern": FACT_ID,
        "topics": list(B.TOPICS),
        "minFact": B.MIN_FACT,
        "minBackbone": B.MIN_BACKBONE,
        "delivery": list(DELIVERY),
        "platforms": lane,
        "notInLane": other,
        "voiceId": VOICE_ID,
        "avatarIds": [a for a, _ in AVATARS],
        "timezone": TIMEZONE,
    }


def avatar_for(day):
    return AVATARS[day.toordinal() % len(AVATARS)]


def link_clickable(cta_rows, platform, account):
    for r in cta_rows:
        if r.get("Platform") == platform and str(r.get("AccountId")) == str(account):
            return (r.get("LinkClickable") or "").strip().lower() == "yes"
    return False


def asks_for(fact, lane, registry, cta_rows):
    """Each platform's call to action, and every reason one cannot be built.

    The keyword has to be live on every account that is asked to carry it.
    A dead keyword is worse than none: somebody comments the word and waits.
    """
    keyword = (fact.get("Keyword") or "").strip().upper()
    problems, live = [], {}
    for ch, rule in lane.items():
        if rule["cta"] != "comment-keyword":
            continue
        if not keyword:
            problems.append("the row has no Keyword, so %s would have no ask" % ch)
            continue
        rows = [r for r in K.lookup(registry, keyword, ch, rule["account"])
                if (r.get("Active") or "").strip().lower() == "yes"]
        if not rows:
            problems.append("%s is not live on %s %s in keyword-registry.csv. Somebody "
                            "would comment it and nothing would answer."
                            % (keyword, ch, rule["account"]))
        elif "BROKEN" in (rows[0].get("Note") or ""):
            problems.append("%s on %s is marked BROKEN in keyword-registry.csv: %s"
                            % (keyword, ch, rows[0].get("Note")))
        else:
            live[ch] = (rows[0].get("Destination") or "").strip()

    link = next((d for d in live.values() if d), "")
    cta = {}
    for ch, rule in lane.items():
        entry = {"shape": rule["cta"]}
        if rule["cta"] == "comment-keyword":
            entry["keyword"] = keyword
        if link and link_clickable(cta_rows, ch, rule["account"]):
            entry["link"] = link
        cta[ch] = entry
    if not problems and not link and any(r["cta"] == "link-in-description"
                                         for r in lane.values()):
        problems.append("no destination link for %s in keyword-registry.csv, so YouTube's "
                        "description would have nowhere to send anyone" % (keyword or "the row"))
    return cta, problems


# ---------- which fact ----------

def sent_ids(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as fh:
            return {(r.get("FactID") or "").strip() for r in csv.DictReader(fh)} - {""}
    except OSError:
        return set()


def delivery_of(fact):
    return (fact.get("Delivery") or "").strip().lower()


def pick_next(bank, day, sources, sent):
    """The first fact in the bank's pull order that this workflow can render
    and nobody has sent. Anything passed over is named, not hidden."""
    skipped = []
    for fid, fact in B.available(bank, 0, today=day, sources=sources):
        if fid in sent:
            skipped.append((fid, "already sent"))
        elif delivery_of(fact) not in DELIVERY:
            skipped.append((fid, "%s, which renders in the reel factory" % delivery_of(fact)))
        else:
            return fid, fact, skipped
    return None, None, skipped


def refusals(fid, fact, day, approved, sent, resend):
    # Staleness is judged on the day it airs, not the day it is sent. That is
    # the day the claim is said out loud.
    problems = list(B.usable_problems(fact, day, approved))
    if delivery_of(fact) not in DELIVERY:
        problems.append('Delivery is "%s". That renders in the reel factory, not through '
                        "HeyGen, so it does not go to this workflow." % delivery_of(fact))
    if fid in sent and not resend:
        problems.append("already sent, so it already has a render. Reuse that one. Pass "
                        "--resend only if the run that rendered it failed.")
    return problems


def build_payload(fid, fact, day, lane, cta):
    avatar_id, _ = avatar_for(day)
    return {
        "fact_id": fid,
        "topic": (fact.get("Topic") or "").strip().lower(),
        "fact": (fact.get("Fact") or "").strip(),
        "backbone": (fact.get("Backbone") or "").strip(),
        "source": (fact.get("Source") or "").strip(),
        "source_url": (fact.get("SourceUrl") or "").strip(),
        "as_of": (fact.get("AsOf") or "").strip(),
        "verified_on": (fact.get("VerifiedOn") or "").strip(),
        "delivery": delivery_of(fact),
        "publish_date": day.isoformat(),
        "target_platform": list(lane),
        "accounts": {ch: rule["account"] for ch, rule in lane.items()},
        "cta": cta,
        "voice_id": VOICE_ID,
        "voice_speed": VOICE_SPEED,
        "avatar_id": avatar_id,
    }


# ---------- sending ----------

def scrub(text, key):
    """Never let the key reach the terminal, however it got into the text."""
    return text.replace(key, "[REDACTED]") if key else text


def post(url, key, payload, timeout):
    req = urllib.request.Request(
        url, data=json.dumps(payload).encode("utf-8"), method="POST",
        headers={"Content-Type": "application/json", KEY_HEADER: key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def record(path, fid, day, execution):
    fresh = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        if fresh:
            w.writerow(LOG_COLUMNS)
        w.writerow([date.today().isoformat(), fid, day.isoformat(), execution])


def answer(status, raw, key, fid, day, log):
    """Read n8n's reply. Returns the exit code."""
    raw = scrub(raw or "", key)
    try:
        body = json.loads(raw) if raw.strip() else {}
    except ValueError:
        body = {}
    if not isinstance(body, dict):
        body = {}

    if status == 202 and body.get("ok") is True:
        execution = str(body.get("execution") or "")
        record(log, fid, day, execution)
        print("ACCEPTED. The workflow's check passed %s%s." % (
            fid, ", execution %s" % execution if execution else ""))
        print("Logged in %s. Commit that line. It is what stops this fact rendering twice." % log)
        print("Every node after the check has to end at HOLD for Amanda. SOP_0909 section 8.")
        return 0

    if status == 422:
        print("REFUSED by the workflow's check. Nothing goes on from it.")
        for reason in body.get("reasons") or ["(it gave no reasons)"]:
            print("  %s" % reason)
        return 1

    if status in (401, 403):
        print("n8n rejected the key, HTTP %d. Nothing went on." % status)
        print("The webhook's Header Auth credential must be named %s and hold the same" % KEY_HEADER)
        print("value as N8N_TRIVIA_KEY.")
        return 2

    if status == 404:
        print("n8n has nothing listening there, HTTP 404. Nothing went on.")
        print("Either the workflow is not published, or this is the /webhook-test/ URL")
        print("and the editor is not waiting for a test call.")
        return 2

    if 200 <= status < 300:
        # The shape of the webhook as it was first pasted: it answers on its
        # own before any check runs, so a 200 here means work has started
        # that nothing has looked at.
        record(log, fid, day, "unchecked")
        print("n8n started the workflow without running the check, HTTP %d." % status)
        print("The webhook answered on its own, so nothing refused this payload and")
        print("whatever comes after it is already running. Its Respond setting must be")
        print("'Using Respond to Webhook Node'. Import daily-trivia-trigger.json again.")
        print("Logged as unchecked in %s so the fact is not sent twice." % log)
        return 2

    message = body.get("message") or raw.strip() or "(empty)"
    print("n8n answered HTTP %d: %s" % (status, message[:300]))
    if "authentication data" in message.lower():
        print("The webhook has Header Auth on and no credential chosen. Pick the %s" % KEY_HEADER)
        print("credential on the webhook node and publish again.")
    print("Nothing is confirmed. Look at the executions in n8n before sending again.")
    return 2


def show(fid, payload, url):
    avatar = dict(AVATARS)[payload["avatar_id"]]
    asks = []
    for ch in payload["target_platform"]:
        c = payload["cta"][ch]
        if c["shape"] == "comment-keyword":
            ask = "%s comment %s" % (ch, c["keyword"])
            asks.append(ask + (" and the link" if c.get("link") else ""))
        else:
            asks.append("%s %s" % (ch, c["shape"].replace("-", " ")))
    print("  fact     %s, %s, verified %s" % (fid, payload["topic"], payload["verified_on"]))
    print("           %s" % payload["fact"])
    print("  for      %s on %s" % (payload["publish_date"], ", ".join(payload["target_platform"])))
    print("  asks     %s" % "; ".join(asks))
    print("  avatar   %s, voice at %s" % (avatar, payload["voice_speed"]))
    print("  to       %s" % (url or "N8N_TRIVIA_URL is not set"))
    if "/webhook-test/" in url:
        print("           That is the test URL. It only listens while the editor waits for a")
        print("           test call. The daily run uses the production URL, /webhook/.")
    print()
    print(json.dumps(payload, indent=2, ensure_ascii=False))


# ---------- the n8n workflow, built from the same rules ----------

GLUE = """
// n8n: 1 call in, 1 verdict out. The next node answers the caller with it,
// and only an accepted fact goes on past the node after that.
const call = $input.first().json;
const result = checkPayload(call.body, RULES, todayIn(RULES.timezone));
return [{json: Object.assign(result, {payload: result.ok ? call.body : null})}];
"""

GATE = """// A refused call has had its answer and stops here. Only an accepted fact
// goes on to the script.
return $input.all().filter((item) => item.json.ok === true);
"""

RESPONSE = ("={{ { ok: $json.ok, fact_id: $json.fact_id, reasons: $json.reasons, "
            "execution: $execution.id } }}")

NOTE = """## Daily trivia trigger

Built by GentleMuse `filing-system/scripts/gm_trivia_trigger.py --workflow --write`. Change the rules there and import again. Do not edit this copy.

**The body is 1 fact from trivia-fact-bank.csv, never a topic.** Anything else gets a 422 with its reasons.

**Before it is live**
1. Webhook node, Credential for Header Auth, create new. Name `X-Trivia-Key`. Value a long random string, the same one that goes in `N8N_TRIVIA_KEY`.
2. Publish the workflow (Active, in older n8n). The sender uses the production URL, the one ending `/webhook/daily-trivia-trigger`.

**Building on from Accepted facts only**
- Script: from `$json.payload.fact` and `$json.payload.backbone` only. No number the fact does not carry.
- HeyGen: `voice_id` at `voice_speed`, with `avatar_id`.
- Then HOLD. Amanda approves before anything reaches Blotato.
- Blotato: `accounts` and `cta` per platform. TikTok never gets the keyword.

SOP_0909 section 8."""

NEXT_NOTE = ("Connect the script step here. Write from $json.payload.fact and "
             "backbone only. HeyGen, then HOLD for Amanda, then Blotato.")


def node_id(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "gentlemuse/daily-trivia-trigger/" + name))


def workflow(channels=CHANNEL_RULES):
    with open(CHECK_JS, encoding="utf-8") as fh:
        check = fh.read().strip()
    code = "const RULES = %s;\n\n%s\n%s" % (json.dumps(rules(channels), indent=2), check, GLUE)

    hook, checker, reply, gate, nxt, note = (
        "Daily Trivia Webhook", "Check the payload", "Answer the caller",
        "Accepted facts only", "Next: script from the fact", "About this workflow")
    nodes = [
        {"parameters": {"content": NOTE, "height": 600, "width": 480, "color": 5},
         "id": node_id(note), "name": note, "type": "n8n-nodes-base.stickyNote",
         "typeVersion": 1, "position": [-560, -200]},
        {"parameters": {"httpMethod": "POST", "path": WEBHOOK_PATH,
                        "authentication": "headerAuth", "responseMode": "responseNode",
                        "options": {}},
         "id": node_id(hook), "name": hook, "type": "n8n-nodes-base.webhook",
         "typeVersion": 2, "position": [0, 0], "webhookId": node_id("webhook")},
        {"parameters": {"jsCode": code},
         "id": node_id(checker), "name": checker, "type": "n8n-nodes-base.code",
         "typeVersion": 2, "position": [240, 0]},
        {"parameters": {"respondWith": "json", "responseBody": RESPONSE,
                        "options": {"responseCode": "={{ $json.status }}"}},
         "id": node_id(reply), "name": reply, "type": "n8n-nodes-base.respondToWebhook",
         "typeVersion": 1.1, "position": [480, 0]},
        {"parameters": {"jsCode": GATE},
         "id": node_id(gate), "name": gate, "type": "n8n-nodes-base.code",
         "typeVersion": 2, "position": [720, 0]},
        {"parameters": {}, "id": node_id(nxt), "name": nxt, "type": "n8n-nodes-base.noOp",
         "typeVersion": 1, "position": [960, 0], "notes": NEXT_NOTE, "notesInFlow": True},
    ]
    chain = [hook, checker, reply, gate, nxt]
    connections = {a: {"main": [[{"node": b, "type": "main", "index": 0}]]}
                   for a, b in zip(chain, chain[1:])}
    return {"name": "Daily Trivia Trigger", "nodes": nodes, "connections": connections,
            "settings": {"executionOrder": "v1", "timezone": TIMEZONE}}


def dump(wf):
    return json.dumps(wf, indent=2, ensure_ascii=False) + "\n"


def workflow_mode(a):
    text = dump(workflow(a.channels))
    if a.check:
        try:
            with open(WORKFLOW, encoding="utf-8") as fh:
                current = fh.read()
        except OSError:
            current = ""
        if current == text:
            print("daily-trivia-trigger.json matches the rules it is built from")
            return 0
        print("daily-trivia-trigger.json is out of date with the rules it is built from.")
        print("Run gm_trivia_trigger.py --workflow --write, then import the new file into")
        print("n8n. Until then the live check holds payloads to the old rules.")
        return 1
    if a.write:
        with open(WORKFLOW, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        print("wrote %s. Import it into n8n to replace the live copy." % WORKFLOW)
        return 0
    sys.stdout.write(text)
    return 0


# ---------- main ----------

def main(argv=None):
    ap = argparse.ArgumentParser(description="Hand 1 checked trivia fact to the n8n workflow.")
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--next", action="store_true",
                       help="the next usable fact nobody has sent")
    which.add_argument("--fact", metavar="TRV-NNN", help="this fact")
    which.add_argument("--workflow", action="store_true",
                       help="build the n8n workflow JSON from the rules")
    ap.add_argument("--write", action="store_true",
                    help="with --workflow, write it to filing-system/n8n")
    ap.add_argument("--check", action="store_true",
                    help="with --workflow, exit 1 if the committed copy is out of date")
    ap.add_argument("--date", help="the day it is for, YYYY-MM-DD. Default tomorrow")
    ap.add_argument("--send", action="store_true",
                    help="actually send. Without it nothing leaves this machine")
    ap.add_argument("--resend", action="store_true",
                    help="send a fact that was sent before, because that run failed")
    ap.add_argument("--bank", default=B.DEFAULT_BANK)
    ap.add_argument("--sources", default=B.DEFAULT_SOURCES)
    ap.add_argument("--registry", default=K.REGISTRY)
    ap.add_argument("--platform-cta", default=K.PLATFORM_CTA)
    ap.add_argument("--channels", default=CHANNEL_RULES)
    ap.add_argument("--log", default=DEFAULT_LOG)
    ap.add_argument("--timeout", type=int, default=30)
    a = ap.parse_args(argv)

    if a.workflow:
        return workflow_mode(a)
    if a.write or a.check:
        ap.error("--write and --check go with --workflow")

    today = date.today()
    if a.date:
        day = B.parse_date(a.date) if re.match(r"^\d{4}-\d{2}-\d{2}$", a.date) else None
        if day is None:
            print("--date %s is not a day. Give YYYY-MM-DD. Each platform's time comes from"
                  % a.date)
            print("its slot when it is scheduled, after Amanda approves. Nothing was sent.")
            return 2
        if day < today:
            print("--date %s is already past. Nothing was sent." % a.date)
            return 2
    else:
        day = today + timedelta(days=1)

    bank = B.load_bank(a.bank)
    approved = B.load_sources(a.sources)
    sent = sent_ids(a.log)
    lane, _ = load_lane_channels(a.channels)

    if a.next:
        fid, fact, skipped = pick_next(bank, day, a.sources, sent)
        for sid, why in skipped:
            print("passed over %s, %s" % (sid, why))
        if fid is None:
            print("Nothing to send. No usable talking-head fact in the bank that has not")
            print("already been sent. Run gm_trivia_bank.py --audit to see what each row is")
            print("waiting on. Do not reach for the nearest fact that fits.")
            return 2
    else:
        fid = a.fact.strip().upper()
        fact = bank.get(fid)
        if fact is None:
            print("%s is not in the bank. A fact that is not written down was not checked."
                  % fid)
            print("Nothing was sent.")
            return 1

    cta, cta_problems = asks_for(fact, lane, K.load_registry(a.registry),
                                 K.load_platform_cta(a.platform_cta))
    problems = refusals(fid, fact, day, approved, sent, a.resend) + cta_problems
    if problems:
        print("REFUSED. %s cannot go to the trivia workflow. Nothing was sent." % fid)
        for p in problems:
            print("  %s" % p)
        return 1

    payload = build_payload(fid, fact, day, lane, cta)
    url = os.environ.get("N8N_TRIVIA_URL", "").strip()
    key = os.environ.get("N8N_TRIVIA_KEY", "").strip()

    if not a.send:
        print("PROPOSED. Nothing was sent. Add --send to transmit.\n")
        show(fid, payload, scrub(url, key))
        print("\nSending hands this fact to n8n, which renders it in Amanda's voice. Read it")
        print("once more before --send.")
        return 0

    if not url:
        print("N8N_TRIVIA_URL is not set, so there is nowhere to send it. Set it to the")
        print("workflow's production URL and run again. Nothing was sent.")
        return 2
    if not key:
        print("N8N_TRIVIA_KEY is not set, so there is nothing to answer the webhook's")
        print("Header Auth with. Set it and run again. Nothing was sent.")
        return 2

    print("SENDING\n")
    show(fid, payload, scrub(url, key))
    print()
    try:
        status, raw = post(url, key, payload, a.timeout)
    except Exception as e:  # noqa: BLE001 - any failure here means not confirmed
        print("could not reach n8n: %s" % scrub(str(e), key))
        print("Nothing is confirmed. Look at the executions in n8n before sending again.")
        return 2
    return answer(status, raw, key, fid, day, a.log)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
