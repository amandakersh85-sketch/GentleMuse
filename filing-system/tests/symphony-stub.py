#!/usr/bin/env python3
"""A stand in for Symphony, so the relay is tested without spending credits.

Behaviour is chosen by what the message contains:
  WALL   the credit wall that the live endpoint returned on 09/08
  SLOW   accepted first, answered on the third poll
  NEVER  accepted, then pending forever
  AUTH   401, as a rejected token
  none   answered straight from /ask

  python3 symphony-stub.py <port>
"""
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

WALL = ("You’ve reached your daily credit limit, so your agents paused "
        "midway. They’ll pick up where they left off when your credits "
        "reset tomorrow. To keep them going now with no daily limit, upgrade "
        "to a Premium plan. [Upgrade](https://symphony.wix.com/packages)")

STATE = {}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body):
        raw = json.dumps(body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        req = json.loads(self.rfile.read(n) or b"{}")

        if not self.headers.get("Authorization", "").startswith("Bearer "):
            return self._send(401, {"error": "no token"})

        if self.path.endswith("/ask"):
            msg = req.get("message", "")
            if "AUTH" in msg:
                return self._send(401, {"error": "token rejected"})
            if "WALL" in msg:
                return self._send(200, {"conversationId": "c-wall", "reply": WALL})
            if "SLOW" in msg:
                STATE["c-slow"] = 0
                return self._send(200, {"conversationId": "c-slow",
                                        "status": "accepted"})
            if "NEVER" in msg:
                return self._send(200, {"conversationId": "c-never",
                                        "status": "accepted"})
            return self._send(200, {"conversationId": "c-fast",
                                    "reply": "Booked. Tuesday at 10, and I "
                                             "emailed her the address."})

        if self.path.endswith("/reply"):
            convo = req.get("conversationId", "")
            if convo == "c-slow":
                STATE["c-slow"] = STATE.get("c-slow", 0) + 1
                if STATE["c-slow"] >= 3:
                    return self._send(200, {"conversationId": convo,
                                            "status": "answered",
                                            "reply": "Done. Three follow ups "
                                                     "went out this morning."})
                return self._send(200, {"conversationId": convo,
                                        "status": "pending"})
            return self._send(200, {"conversationId": convo,
                                    "status": "pending"})

        return self._send(404, {"error": "no such path"})


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
