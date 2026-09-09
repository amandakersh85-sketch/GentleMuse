#!/usr/bin/env python3
"""The Symphony relay. Sends one message to Amanda's Symphony agents and waits
for the answer.

Symphony acts as Amanda. A message sent here carries her authority to schedule,
to email her contacts and to act on her business, so the relay proposes by
default and only transmits under --send.

  python3 gm_symphony.py --message "..."            # prints what would be sent
  python3 gm_symphony.py --message "..." --send     # sends and waits
  python3 gm_symphony.py --resume <conversationId>  # collects a late answer
  python3 gm_symphony.py --message "..." --send --expect-data

--expect-data says the message asked for facts, so a reply that describes what
Symphony could do rather than reporting anything is failed the same way a
credit wall is. Leave it off for questions that genuinely want prose.

The token is read from SYMPHONY_TOKEN and is never written to the terminal, to
a file or to a commit. Without it the relay stops rather than sending unsigned.

Exit 0 Symphony answered, 1 Symphony replied but the reply is a wall rather
than an answer, 2 the exchange could not be completed.
"""
import argparse, json, os, re, sys, time
import urllib.error, urllib.request

BASE = os.environ.get("SYMPHONY_BASE",
                      "https://symphony.wix.com/individuals-chat/poc/agent")

# A reply can come back with status "answered" and still not be an answer.
# On 09/08 the relay was verified against the live endpoint and what came back
# was the daily credit wall. The transport reported success. Nothing in the
# envelope said the agents had never run. These markers are how a wall is told
# apart from work, so that a caller cannot read one as the other.
WALLS = [
    ("symphony.wix.com/packages", "upgrade link in place of an answer"),
    ("daily credit limit",        "daily credit limit reached"),
    ("credit limit",              "credit limit reached"),
    ("credits reset",             "agents waiting on a credit reset"),
    ("out of credits",            "credits exhausted"),
    ("ran out of credits",        "credits exhausted"),
    ("agents paused",             "agents paused mid run"),
    ("paused midway",             "agents paused mid run"),
    ("pick up where they left off", "agents paused mid run"),
    ("upgrade to a premium plan", "upgrade prompt in place of an answer"),
]


def wall_reason(reply):
    """Return why this reply is a wall, or None if it reads as a real answer."""
    low = (reply or "").lower()
    for marker, reason in WALLS:
        if marker in low:
            return reason
    return None


# A reply can also come back fluent, on topic and empty. Asked what is on the
# calendar, an agent that cannot reach the calendar will describe what it could
# do for you, and that reads like an answer to everything except a person
# checking it against their own accounts. It is the wall again in a politer
# register, so it is caught the same way.
#
# Two signals have to agree before the relay calls it. HEDGES are the phrasings
# of a capability description rather than a report. EVIDENCE counts the
# particulars that make a claim checkable: digits, weekdays, months. A blurb
# carries hedges and almost no particulars. A real answer that happens to close
# with an offer of help carries both, and passes.
HEDGES = [
    "i can help", "i can assist", "i'd be able to", "i would be able to",
    "i'll be able to", "i am able to", "i'm able to", "i can also",
    "once you connect", "once connected", "you can ask me", "you can tell me",
    "just let me know", "let me know if you", "would you like me to",
    "here's what i can do", "here is what i can do", "i don't have access",
    "i do not have access", "i can't access", "i cannot access",
    "i don't currently have", "i do not currently have",
    # Added 09/09 from Symphony's own words on the first real capability probe.
    # It declines in a register the list above missed entirely: not "I cannot
    # access" but "I don't have direct read access", "I could pull it", "I
    # can't see those". That reply passed on evidence, with 56 particulars in
    # it, so nothing was mis-called. A pure blurb in the same voice would have
    # gone through unflagged.
    "i don't have direct", "i do not have direct",
    "i don't have a live", "i do not have a live",
    "i can't pull", "i cannot pull", "i could pull",
    "i can't see those", "i cannot see those",
    "if you connected", "if you gave me",
    "i can search for", "i can look",
    "isn't surfaced", "is not surfaced",
]

EVIDENCE = re.compile(
    r"\d"
    r"|\b(?:mon|tues|wednes|thurs|fri|satur|sun)day\b"
    r"|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\b",
    re.I)

# 3 particulars. Below that a reply is not reporting anything, whatever else it
# is doing. Seven days of calendar, a contact count with 3 sends, and a run of
# recent posts cannot be answered truthfully with 2 numbers in it.
EVIDENCE_FLOOR = 3

# Phrasings that make a message a request for facts. Used only to notice that
# --expect-data was probably meant. It never turns the check on by itself,
# because guessing wrong there is what would make the check untrustworthy.
ASKS = ["how many", "what is on", "what's on", "with dates", "how did",
        "what were", "show me", "when did", "how much", "list "]


def thin_reason(reply):
    """Return why this reply describes rather than reports, or None.

    Only meaningful when the message asked for facts. The caller says so with
    --expect-data, because prose is the right answer to a question that asked
    for prose and this must never fire on those.
    """
    low = (reply or "").lower()
    if not any(h in low for h in HEDGES):
        return None
    found = len(EVIDENCE.findall(reply or ""))
    if found >= EVIDENCE_FLOOR:
        return None
    return ("it describes what it can do and reports %d particular%s"
            % (found, "" if found == 1 else "s"))


def looks_factual(message):
    low = message.lower()
    return any(a in low for a in ASKS)


def post(path, token, payload, timeout):
    req = urllib.request.Request(
        "%s/%s" % (BASE.rstrip("/"), path),
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer %s" % token,
                 "Content-Type": "application/json"},
        method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def scrub(text, token):
    """Never let the token reach the terminal, however it got into the text."""
    return re.sub(re.escape(token), "[REDACTED]", text) if token else text


def collect(token, convo, wait, interval):
    """Poll one conversation until it answers. Returns the reply or None."""
    deadline = time.time() + wait
    while time.time() < deadline:
        time.sleep(interval)
        try:
            p = post("reply", token, {"conversationId": convo}, timeout=30)
        except Exception as e:
            print("lost the connection while waiting: %s" % scrub(str(e), token))
            return None
        if p.get("status") == "answered" and p.get("reply"):
            return p["reply"]
        sys.stdout.write(".")
        sys.stdout.flush()
    return None


def report(reply, token, expect_data=False):
    """Print the reply and say whether it is an answer. Returns the exit code."""
    reply = scrub(reply, token)
    print("\nSYMPHONY\n%s" % reply)

    reason = wall_reason(reply)
    if reason:
        print("\nTHIS IS NOT AN ANSWER. %s." % reason.capitalize())
        print("Symphony reported success and did no work. Whatever was asked")
        print("for has not happened. Do not record it as done.")
        return 1

    if expect_data:
        reason = thin_reason(reply)
        if reason:
            print("\nTHIS IS NOT AN ANSWER. Facts were asked for and %s." % reason)
            print("Nothing here can be checked against your own accounts, so the")
            print("ability is unproven rather than delivered. Do not record it")
            print("as done.")
            return 1
    return 0


def token_or_stop():
    token = os.environ.get("SYMPHONY_TOKEN", "").strip()
    if not token:
        print("SYMPHONY_TOKEN is not set, so there is nothing to sign the")
        print("message with. Set it and run again. Nothing was sent.")
    return token


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--message", help="what to say to Symphony")
    ap.add_argument("--message-file", help="read the message from a file")
    ap.add_argument("--session", default="claude-code",
                    help="keeps replies in one thread, default claude-code")
    ap.add_argument("--resume", metavar="CONVERSATION_ID",
                    help="poll a conversation already sent, instead of sending")
    ap.add_argument("--expect-data", action="store_true",
                    help="the message asks for facts, so hold the reply to that")
    ap.add_argument("--send", action="store_true",
                    help="actually transmit. Without it nothing is sent.")
    ap.add_argument("--wait", type=int, default=120,
                    help="seconds to wait for the answer, default 120")
    ap.add_argument("--interval", type=int, default=3,
                    help="seconds between polls, default 3")
    a = ap.parse_args()

    if a.resume:
        token = token_or_stop()
        if not token:
            return 2
        print("collecting conversation %s" % a.resume)
        reply = collect(token, a.resume, a.wait, a.interval)
        print()
        if not reply:
            print("still no answer after %ds. The conversation stays open." % a.wait)
            return 2
        return report(reply, token, a.expect_data)

    if a.message_file:
        try:
            message = open(a.message_file, encoding="utf-8").read().strip()
        except Exception as e:
            print("cannot read the message file: %s" % e)
            return 2
    else:
        message = (a.message or "").strip()
    if not message:
        print("no message. Pass --message, --message-file or --resume.")
        return 2

    if not a.send:
        print("PROPOSED. Nothing was sent. Add --send to transmit.\n")
        print("  session : %s" % a.session)
        print("  to      : %s/ask" % BASE.rstrip("/"))
        print("  message : %s" % message)
        print("\nThis message will reach Symphony as Amanda and carries her")
        print("authority to act on her business. Read it once more before --send.")
        if looks_factual(message) and not a.expect_data:
            print("\nThis reads as a request for facts. Add --expect-data and a")
            print("reply that only describes what Symphony could do is failed")
            print("rather than recorded as an answer.")
        return 0

    token = token_or_stop()
    if not token:
        return 2

    try:
        r = post("ask", token, {"message": message, "sessionId": a.session},
                 timeout=60)
    except urllib.error.HTTPError as e:
        print("Symphony refused the message: HTTP %s" % e.code)
        if e.code in (401, 403):
            print("The token was rejected. Reissue it in Symphony, Settings,")
            print("Connections, then set SYMPHONY_TOKEN again.")
        return 2
    except Exception as e:
        print("could not reach Symphony: %s" % scrub(str(e), token))
        return 2

    convo = r.get("conversationId")
    reply = r.get("reply")

    if not reply:
        if not convo:
            print("Symphony accepted nothing and returned no conversation to")
            print("follow. Response was: %s" % scrub(json.dumps(r), token))
            return 2
        print("sent. Symphony is working, conversation %s" % convo)
        reply = collect(token, convo, a.wait, a.interval)
        print()
        if not reply:
            print("Symphony did not answer within %ds. The conversation is still" % a.wait)
            print("open. Collect it later with:")
            print("  python3 %s --resume %s" % (os.path.basename(__file__), convo))
            return 2

    return report(reply, token, a.expect_data)


if __name__ == "__main__":
    sys.exit(main())
