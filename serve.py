#!/usr/bin/env python3
"""Serve the course in a browser.

Slides work fine opened straight from disk, but a local server is nicer: links
between pages behave, the browser stops complaining about local files, and a
reload always shows your latest edit.

    python3 serve.py              start on http://localhost:8000 and open it
    python3 serve.py --port 9001  use a different port
    python3 serve.py --no-browser don't open a browser window
    python3 serve.py --quiet      only log problems, not every request

Stop it with Ctrl+C. Standard library only, so there is nothing to install.
"""

from __future__ import annotations

import argparse
import functools
import http.server
import socket
import socketserver
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LANDING = "/slides/index.html"


class CourseHandler(http.server.SimpleHTTPRequestHandler):
    """Static files, with two small conveniences."""

    quiet = False

    def do_GET(self) -> None:  # noqa: N802  (the stdlib spells it this way)
        # "/" should land on the course index, not a directory listing.
        if self.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", LANDING)
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self) -> None:
        # Without this, an edited slide can come back from the browser cache
        # and you spend ten minutes wondering why your change did nothing.
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:
        if not self.quiet:
            super().log_message(fmt, *args)

    def log_error(self, fmt: str, *args) -> None:
        super().log_message(fmt, *args)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def free_port(preferred: int, attempts: int = 12) -> int:
    """Return the first port that is actually available, starting at preferred."""
    for port in range(preferred, preferred + attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
            try:
                probe.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise SystemExit(
        f"Ports {preferred} to {preferred + attempts - 1} are all busy. "
        "Pass --port with something else."
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Python course slides locally.")
    parser.add_argument("--port", type=int, default=8000, help="port to listen on (default 8000)")
    parser.add_argument("--host", default="127.0.0.1", help="interface to bind (default 127.0.0.1)")
    parser.add_argument("--no-browser", action="store_true", help="do not open a browser")
    parser.add_argument("--quiet", action="store_true", help="only log errors")
    args = parser.parse_args()

    port = free_port(args.port)
    CourseHandler.quiet = args.quiet
    handler = functools.partial(CourseHandler, directory=str(ROOT))

    url = f"http://localhost:{port}{LANDING}"
    print(f"\n  Python, SQL & Git course")
    print(f"  serving {ROOT}")
    print(f"\n      {url}\n")
    if port != args.port:
        print(f"  (port {args.port} was busy, using {port})\n")
    print("  Ctrl+C to stop\n")

    with Server((args.host, port), handler) as httpd:
        if not args.no_browser:
            threading.Timer(0.5, webbrowser.open, args=[url]).start()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped\n")


if __name__ == "__main__":
    main()
