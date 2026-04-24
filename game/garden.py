#!/usr/bin/env python3
"""
Cult Garden Launcher - starts the server and opens the browser automatically.

Usage:
    python3 game/garden.py [port]

Default port: 4545
Press Ctrl+C to stop the server.
"""
import subprocess
import sys
import time
import webbrowser
import os

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4545
    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("=== Cult Garden Server ===")
    print(f"  Starting server on port {port}")
    print(f"  Serving from: {script_dir}")
    print("  Press Ctrl+C to stop")
    print("=" * 27)

    # Start server as subprocess
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(port)],
        cwd=script_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Give it a moment to bind
    time.sleep(1)

    # Open browser to the live garden
    url = f"http://localhost:{port}/cult-garden-live.html"
    print(f"Opening: {url}")
    webbrowser.open(url)

    try:
        server.wait()
    except KeyboardInterrupt:
        print("\nStopping server...")
        server.terminate()
        server.wait()
        print("Done.")

if __name__ == "__main__":
    main()
