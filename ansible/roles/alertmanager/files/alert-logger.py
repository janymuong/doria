#!/usr/bin/env python3
"""Receive Alertmanager webhooks and write one journal line per alert."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST, PORT = "127.0.0.1", 9199


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length))
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        for alert in payload.get("alerts", []):
            labels = alert.get("labels", {})
            target = (labels.get("host") or labels.get("service")
                      or labels.get("server") or "-")
            summary = alert.get("annotations", {}).get("summary", "")
            print(
                f"{alert.get('status', '?').upper()} "
                f"severity={labels.get('severity', '-')} "
                f"alert={labels.get('alertname', '-')} "
                f"target={target} "
                f"summary={summary!r}",
                flush=True,
            )
        self.send_response(200)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass  # keep the journal to alert lines only


if __name__ == "__main__":
    HTTPServer((HOST, PORT), Handler).serve_forever()
