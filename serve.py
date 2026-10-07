#!/usr/bin/env python3
"""Local preview that behaves like GitHub Pages: /about serves about.html.

    python3 serve.py [port]
"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


class Pages(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def translate_path(self, path):
        real = super().translate_path(path)
        if not os.path.exists(real) and os.path.exists(real + ".html"):
            return real + ".html"
        return real


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4326
    http.server.ThreadingHTTPServer(("", port), Pages).serve_forever()
