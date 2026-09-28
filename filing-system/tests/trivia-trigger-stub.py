#!/usr/bin/env python3
"""A stand in for the n8n trivia webhook, so the sender is tested without n8n.

The answers are the ones n8n 2.40.7 gave on 09/28, word for word where it
matters: a plain text 403 for a missing or wrong key, a plain text 500 when
Header Auth is on and no credential is chosen, and {"message": "Workflow was
started"} from a webhook that answers before anything checks the call.

Behaviour is chosen by the path:
  /webhook/daily-trivia-trigger   the workflow as built. Key tok-trivia, 202
  /webhook/refuse                 the workflow's check refusing, 422
  /webhook/started                the node as first pasted: no key, no check
  /webhook/nocred                 Header Auth on, no credential chosen
  /webhook/leaky                  an error body that echoes the key back
  anything else                   404, nothing listening

  python3 trivia-trigger-stub.py <port>
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

KEY = "tok-trivia"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body):
        raw = (json.dumps(body) if isinstance(body, dict) else body).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json" if isinstance(body, dict)
                         else "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        try:
            req = json.loads(self.rfile.read(n) or b"{}")
        except ValueError:
            req = {}
        key = self.headers.get("X-Trivia-Key", "")
        fid = req.get("fact_id", "") if isinstance(req, dict) else ""

        if self.path == "/webhook/started":
            return self._send(200, {"message": "Workflow was started"})
        if self.path == "/webhook/nocred":
            return self._send(500, "No authentication data defined on node!")
        if self.path == "/webhook/leaky":
            return self._send(500, {"message": "header X-Trivia-Key was %s" % key})
        if self.path not in ("/webhook/daily-trivia-trigger", "/webhook/refuse"):
            return self._send(404, {"code": 404, "message": 'The requested webhook "POST %s" '
                                    "is not registered." % self.path[len("/webhook/"):]})
        if key != KEY:
            return self._send(403, "Authorization data is wrong!")
        if self.path == "/webhook/refuse":
            return self._send(422, {"ok": False, "fact_id": fid, "execution": "42", "reasons": [
                'topic "history" is outside the lane, which is ai, automation, creator.']})
        return self._send(202, {"ok": True, "fact_id": fid, "reasons": [], "execution": "41"})


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", int(sys.argv[1])), Handler).serve_forever()
