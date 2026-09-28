"""A starting point: a page, a health address, and state kept where the platform backs it up.

It is served at https://apps.fburl.ai/apps/<name>/, with that prefix taken off before it arrives, so
every address a page of yours asks for is RELATIVE ("api/thing", never "/api/thing").
"""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DATA = os.environ.get("DATA_DIR", "/data")
COUNT = os.path.join(DATA, "visits.json")


def visits(add=0):
    try:
        n = json.load(open(COUNT))["visits"]
    except (OSError, ValueError, KeyError):
        n = 0
    if add:
        n += add
        tmp = COUNT + ".tmp"
        json.dump({"visits": n}, open(tmp, "w"))
        os.replace(tmp, COUNT)
    return n


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, kind="text/html; charset=utf-8"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/healthz":                        # HEALTH in lab.conf: 200 only while serving
            return self.send(200, '{"ok": true}', "application/json")
        if path == "/":
            who = self.headers.get("Tailscale-User-Name") or "you"   # set by the platform, never by the browser
            return self.send(200, f"<!doctype html><title>Hello</title><h1>Hello, {who}</h1><p>Visit {visits(1)}.</p>")
        self.send(404, "not here")


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
