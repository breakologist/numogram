#!/bin/bash
# Cult Garden Launcher - starts server and opens browser
# Usage: ./launch-garden.sh [port]
# Default port: 4545

set -e

PORT="${1:-4545}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Cult Garden Server ==="
echo "  Starting server on port $PORT"
echo "  Serving from: $SCRIPT_DIR"
echo "  Press Ctrl+C to stop"
echo "========================"

# Check if port is already in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "WARNING: Port $PORT is already in use."
    echo "Kill existing process? (y/n)"
    read -r resp
    if [[ "$resp" =~ ^[Yy]$ ]]; then
        sudo kill -9 $(lsof -t -i:$PORT) 2>/dev/null || true
        sleep 0.5
    else
        echo "Aborted."
        exit 1
    fi
fi

# Start server in background
cd "$SCRIPT_DIR"
python3 -m http.server "$PORT" &
SERVER_PID=$!

# Give server a moment to start
sleep 1

# Open browser
echo "Opening browser..."
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "http://localhost:$PORT/cult-garden-live.html" 2>/dev/null || true
elif command -v open >/dev/null 2>&1; then
    open "http://localhost:$PORT/cult-garden-live.html" 2>/dev/null || true
else
    echo "Could not detect browser opener (xdg-open/open)."
    echo "Manually open: http://localhost:$PORT/cult-garden-live.html"
fi

# Wait for server (Ctrl+C stops both)
wait $SERVER_PID
