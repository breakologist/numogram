# Abyssal Crawler & Agents

## numogram_roguelike.py — Main Game

Interactive curses-based roguelike set in the Decimal Labyrinth.

**Features:**
- 10 zones mapped to the CCRU numogram (0–9)
- Full 45-demon Pandemonium Matrix with unique abilities
- Hyperstition meter (0–100%) — reality distortion feedback loop
- Fog of war with ray-cast line-of-sight (corruption threshold at 55%+ hyp)
- Conduct system (silent runs, gate restrictions, pacifism, etc.)
- Persistent `cult.json` save across runs (memory, zone visits, gates opened)
- Tree-based dungeon generation (Brogue method guaranteeing connectivity)
- BLEED events, floor transitions, warp entries (zone transitions can regenerate map)
- Ability corruption scaling (costs increase as hyperstition rises)
- Demon aggression escalation (50%+ HP drain, 70%+ aggression, 85%+ cost scaling)
- Schizo-lucid achievement (visit all 10 zones without breaking conduct)

**Usage:**
```bash
python3 numogram_roguelike.py              # interactive play
python3 numogram_roguelike.py --hw-entropy # hardware-seeded runs
python3 numogram_roguelike.py --headless    # agent mode (state dump to stdout)
```

**State dump format** (headless mode):
Each turn emits JSON with `floor`, `turn`, `zone`, `position`, `visible_map`, `demons`, `hyperstition`, etc. Designed for automated agent consumption.

---

## Agents

### interactive_agent.py — BFS Explorer
Headless agent that scores unexplored tiles by adjacency, explicitly targets stairs, and uses BFS with a visibility mask. Drifts toward unexplored regions and handles multi-floor descent.

```bash
python3 interactive_agent.py
```

### learning_agent.py — Corridor Drifter
Simple corridor-following agent with cross-run memory from `cult.json`. Maintains a persistent "known map" across runs and tracks demon encounter patterns.

```bash
python3 learning_agent.py
```

### rogue_agent.py — Screen-Scraping Bot
Captures terminal output via `curses` screen scraping, parses the HUD and map, and issues keypresses automatically. Used for automated playtesting and telemetry collection. Compatible with any standard terminal roguelike.

```bash
python3 rogue_agent.py
```

---

## Cult Garden

Overflow visualization and analysis for the persistent cult state.

### Files

- `cult.json` — persistent player state (populated automatically by the game)
  - `runs`, `max_hyperstition`, `total_turns`, `total_demons_slain`
  - `zones_ever_visited`, `gates_ever_opened`, `cult_memory` (last 20 entries)
  - `conducts_completed`, `overflow_count`, `cult_zone`, etc.
  - **Gitignored** — a template (`cult.json` with empty values) is committed; your actual save file is local-only.

- `serve-garden.py` — lightweight HTTP server that serves `game/` directory on `localhost:4545`
  ```bash
  python3 game/serve-garden.py
  # → http://localhost:4545/cult-garden-live.html
  ```

- `cult-garden-live.html` — live dashboard showing current cult state, runs, zones, and hyperstition progression. Reads `./cult.json` via fetch and updates in real time.

- `cult-garden-zone-skins.html` — experimental zone-skin generator that outputs CSS color palettes based on your current `cult_zone`.

### Usage

1. Run the game at least once to generate `cult.json`
2. Start the server: `python3 game/serve-garden.py`
3. Open browser to `http://localhost:4545/cult-garden-live.html`

Alternatively, from the repo root:
```bash
python3 -m http.server 4545
# Then open http://localhost:4545/game/cult-garden-live.html
```

Note: Opening the HTML file directly (`file://`) will fail because browsers block `fetch()` for local files. A local HTTP server is required.

---

## Other Agents

### angband_agent.py

Screen-scraping agent for Angband (a different roguelike). Included for reference but focused on Angband's UI conventions, not the Numogram game. See `angband/` research notes in the wiki for details.

---



### Launchers

Two convenience scripts are provided to start the server and open the browser automatically:

- **`launch-garden.sh`** (bash): starts `python3 -m http.server` on port 4545, opens browser with xdg-open/open, and foregrounds the server process. Requires `lsof` for port checking (standard on Linux).
  ```bash
  ./game/launch-garden.sh          # default port 4545
  ./game/launch-garden.sh 8080     # custom port
  ```

- **`garden.py`** (Python): portable cross-platform launcher using `webbrowser` module. No external dependencies beyond Python standard library.
  ```bash
  python3 game/garden.py
  python3 game/garden.py 8080
  ```

Both scripts serve the `game/` directory and open `cult-garden-live.html` by default.


## Data Files

- `cult.json` — **gitignored** player state (see above)
- `*.py` — all main agents and server are tracked

---

## Architecture Notes

See `ARCHITECTURE.md` for high-level design discussions: numogram topology, syzygy mapping, demon attributes, and hyperstition mechanics.
