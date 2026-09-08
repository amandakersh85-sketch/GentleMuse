#!/usr/bin/env python3
"""The Symphony relay. Sends one message to Amanda's Symphony agents and waits
for the answer.

Symphony acts as Amanda. A message sent here carries her authority to schedule,
to email her contacts and to act on her business, so the relay proposes by
default and only transmits under --send.

  python3 gm_symphony.py --message "..."            # prints what would be sent
  python3 gm_symphony.py --message "..." --send     # sends and waits
  python3 gm_symphony.py --resume <conversationId>  # collects a late answer

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


def report(reply, token):
    """Print the reply and say whether it is an answer. Returns the exit code."""
    reply = scrub(reply, token)
    print("\nSYMPHONY\n%s" % reply)
    reason = wall_reason(reply)
    if reason:
        print("\nTHIS IS NOT AN ANSWER. %s." % reason.capitalize())
        print("Symphony reported success and did no work. Whatever was asked")
        print("for has not happened. Do not record it as done.")
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
        return report(reply, token)

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

    return report(reply, token)


if __name__ == "__main__":
    sys.exit(main())
