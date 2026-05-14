---
title: "Camofox Browser Setup & Troubleshooting"
created: 2026-05-14
last_updated: 2026-05-14
tags: ["browser", "camofox", "setup", "node", "sqlite"]
status: documented
---

# Camofox Browser Setup

## Quick Start

```bash
cd ~/camofox-browser
npm start
# Server runs on http://localhost:9377
```

For first-time setup:
```bash
npx camoufox-js fetch  # Downloads browser binaries + GeoIP database
```

## Architecture

- **Server:** Express.js on port 9377
- **Browser:** Camoufox (anti-detection Firefox fork, v135.0.1-beta.24)
- **Dependencies:** camoufox-js, playwright, playwright-core, better-sqlite3
- **Sessions:** 30-minute inactivity timeout per userId

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/tabs` | POST | Create new tab (`{"userId", "sessionKey", "url"}`) |
| `/tabs/:tabId/snapshot` | GET | Accessibility tree with element refs |
| `/tabs/:tabId/click` | POST | Click element by ref or CSS selector |
| `/tabs/:tabId/type` | POST | Type text into element |
| `/tabs/:tabId/screenshot` | GET | Capture PNG screenshot |
| `/tabs` | GET | List active tabs |
| `/sessions/:userId` | DELETE | Clear all user data |
| `/health` | GET | Server health check |

## Known Issue: better-sqlite3 + Node 26 ABI Incompatibility

**Symptom:** `Module did not self-register: better_sqlite3.node`

**Cause:** Node 26.1.0 (V8 14+) removed `info.This()` from `PropertyCallbackInfo`, which breaks `better-sqlite3@12.6.2` compilation. The error:
```
../src/objects/statement.cpp:381:50: error: 'const class v8::PropertyCallbackInfo<v8::Value>' has no member named 'This'
```

**Root:** `camoufox-js@0.8.5` pins `better-sqlite3@^12.2.0` which resolves to `12.6.2` — the last version before Node 26 support.

**Fix:**
```bash
cd ~/camofox-browser
npm install better-sqlite3@12.10.0 --save-exact
```

`better-sqlite3@12.10.0` (released 2026-04) includes Node 26 compatibility. The package-lock will update and the native module will compile correctly.

**Verification:**
```bash
node -e "const sqlite3 = require('better-sqlite3'); console.log('OK')"
# Should print "OK" without errors
```

**Long-term:** When `camoufox-js` releases a version with updated better-sqlite3, this override can be removed.

## Server Health Check

```bash
curl -s http://localhost:9377/health
# Expected: {"ok":true,"engine":"camoufox","browserConnected":true,"browserRunning":true}
```

If `browserConnected: false`, the server is running but hasn't launched the browser yet (lazy launch on first tab creation).

## Tab Lifecycle

1. Create tab → get tabId (UUID)
2. Navigate to URL → browser loads page
3. Get snapshot → receive accessibility tree with refs [e1, e2, ...]
4. Click/type using refs
5. Tab expires after 30 minutes of inactivity

## Example: Create Tab and Screenshot

```bash
# Create tab
TAB=$(curl -s -X POST http://localhost:9377/tabs \
  -H "Content-Type: application/json" \
  -d '{"userId": "hermes", "sessionKey": "demo", "url": "https://federatedindustrial.com/tracker"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tabId'])")

# Wait for page load
sleep 8

# Get snapshot
curl -s "http://localhost:9377/tabs/$TAB/snapshot?userId=hermes" | python3 -m json.tool

# Get screenshot (binary PNG)
curl -s "http://localhost:9377/tabs/$TAB/screenshot?userId=hermes" -o /tmp/screenshot.png
```

## Search Macros

The server supports search macros instead of constructing URLs manually:

| Macro | Site |
|-------|------|
| `@google_search` | Google |
| `@youtube_search` | YouTube |
| `@reddit_search` | Reddit |
| `@wikipedia_search` | Wikipedia |
| `@twitter_search` | Twitter/X |

```bash
curl -s -X POST http://localhost:9377/tabs -H "Content-Type: application/json" \
  -d '{"userId": "hermes", "sessionKey": "search", "macro": "@google_search", "query": "numogram CCRU"}'
```

## nanoTracker Exploration (2026-05-14)

Successfully explored nanoTracker via Camofox:
- Loaded `https://federatedindustrial.com/tracker`
- Confirmed UI: dark amber-on-black CRT aesthetic, hex row numbers, CH3/CH4 channel headers
- Transport: BPM 125, SPD 6, ORD 0, PAT 0, ROW 0/64
- Verified snapshot accessibility tree with 43 interactive elements
- Pattern editor shows classic tracker grid layout with dashes/dots for empty cells
- Anime pixel art panels ("LEFT GIRL") as custom visualizers

See [[nanotracker-deep-dive]] for full code analysis (format support, effects, architecture).

## Server Files

- `server.js` — Express routes (NO process.env, NO child_process)
- `lib/config.js` — All process.env reads centralized
- `lib/launcher.js` — Subprocess spawning (camoufox browser binary)
- `lib/snapshot.js` — Accessibility tree generation
- `lib/macros.js` — Search macro URL expansion
- `lib/cookies.js` — Cookie file I/O

## Git Status

The camofox-browser repo (`~/camofox-browser`) is a git repo at version 1.5.2. After any dependency changes (like the better-sqlite3 upgrade), the package.json and package-lock.json files will show as modified.
