#!/usr/bin/env python3
"""
Cult Garden Server — Serves the live garden HTML and cult.json
from the game/ directory on localhost:4545.

Usage:
    python3 game/serve-garden.py
    # Then open http://localhost:4545/cult-garden-live.html
"""
import http.server
import socketserver
import os
import sys

PORT = 4545
ROOT = os.path.dirname(os.path.abspath(__file__))

class CultHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        # CORS for local development (allows fetching cult.json from same origin anyway,
        # but this also permits cross-origin if needed)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):
        # quieter logs
        if "cult.json" in args[0] or "cult-garden" in args[0]:
            print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CultHandler) as httpd:
        print(f"=" * 60)
        print(f"  CULT GARDEN SERVER")
        print(f"  Serving from: {ROOT}")
        print(f"  URL: http://localhost:{PORT}/cult-garden-live.html")
        print(f"  Press Ctrl+C to stop")
        print(f"=" * 60)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")
            sys.exit(0)
