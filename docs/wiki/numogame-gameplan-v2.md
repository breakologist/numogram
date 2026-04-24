---
tags: [numogram, roguelike, abyssal-crawler, progress, learning-agent, gameplan]
zone: 0-9
source: "Session April 15 2026 — 98 runs, demos, headless mode, interactive agent"
method: design-document
created: 2026-04-24
---

# The Abyssal Crawler — Gameplan Update (April 15, 2026)

> Wednesday, Mercury's day. The agent enters the cult record. The game learns to see.

## I. What Was Built

This session transformed the Abyssal Crawler from a curses roguelike into a multi-modal game with AI agent support. The changes span the game engine, the agent interface, and the learning infrastructure.

### Game Engine Changes

**Diagonal combat (Chebyshev distance).** Player attacks and demon chase now use `max(abs(dx), abs(dy)) == 1` instead of `abs(dx) + abs(dy) == 1`. Demons pursue diagonally. Players can bump-attack in all 8 directions.

**Barker threshold system.** The BARKER_THRESHOLDS dictionary (Degree-0 through 9-Barker: Unuttera) was already in the code but never displayed. Now fires on all hyperstition events: zone crossings (+3), gate steps (+5), demon kills (+5). The player sees "3-Barker: The swarm stirs" when crossing 30% hyperstition.

**Demon kill hyperstition: +1 → +5.** The Builder's suggestion from the tetralogue. Killing a demon now gives the same hyperstition as stepping on a gate.

**Cryptolith mechanical transformation.** Grasping the Cryptolith now reduces speed by 1, adds +20 hyperstition, fires Barker threshold check. "The Outside leaks through. Speed drops. The map destabilizes."

**Gate tile protection.** `_pocket()` and `_reshape_rooms()` no longer overwrite gate tiles ('+'). Gates survive zone-specific room modifications.

**Name entry fix.** `stdscr.timeout(-1)` during name input — blocks until Enter. Prompt shows "Enter name:" in bold. Clears after entry.

### Agent Interface

**State dump ('p' key).** Writes `/tmp/numogame_state.txt` with:
- Player stats (position, zone, HP, hyperstition, name)
- Local 21×21 ASCII map centered on player
- Full 78×22 floor map with zone boundaries, demons, gates
- Nearby gates with compass direction and distance
- Nearby demons with stats and direction
- Adjacent zones
- Barker threshold status
- Recent log (last 8 entries)
- Auto-dumps on zone change

**Gate proximity alert.** Every move, `_scan_gates()` checks within 8 tiles. Prints "[GATE] Gt-XX detected N tiles direction!"

**Headless mode (`--headless`).** No curses. Reads moves from stdin. Writes state to file. Outputs status to stderr. Instant latency. 20 games in 1 second. Usage:
```
echo "ddddssssllllpp" | NUMOGRAM_PLAYER=hermes python3 numogram_roguelike.py --headless
```

**Demo recorder ('D' key).** Doom-style input recording. Saves to `~/numogame/demos/<timestamp>_<name>.demo`. Records every keypress with turn number and game events (zone changes, demon kills, deaths). Text file — parseable by agents.

### Learning Agent

**Interactive agent (`interactive_agent.py`).** Spawns headless game as subprocess. Sends one move at a time. Reads state dump between moves. Makes decisions based on map data. First working state-reading agent.

**Decision hierarchy:**
1. SURVIVE: HP < 25% → flee from nearest demon
2. COLLECT: Gate visible on map → pathfind to it
3. FIGHT: Demon adjacent + HP > 50% → attack
4. EXPLORE: Follow corridors toward zone boundaries
5. WANDER: Find best corridor direction

**Map-aware pathfinding.** Reads the full 78×22 map. Finds corridors by checking tile types in each direction. Scores paths by corridor length, zone boundaries (+3), and gates (+5). Follows the highest-scoring corridor.

**Batch runner.** Runs N games with human-like movement weights (39% left, 29% right, 22% diagonal — derived from demo analysis).

**Demo analyzer.** Parses demo files. Reports key frequency, zone traversal path, transition speed, keys after zone changes.

## II. The State of Play

### Human Runs (demo-recorded)

| Run | Turns | Hyp% | Zones | Slain | Gates | Notes |
|-----|-------|------|-------|-------|-------|-------|
| #85 | 333 | 100% | ALL 10 | 4 | ? | First recorded full clear |
| #86 | 200 | 98% | ALL 10 | 2 | ? | Near-full clear |
| #87 | 337 | 100% | ALL 10 | 4 | ? | Demo: 392 keypresses, 26 zone changes |

**Human movement analysis (from demo #87):**
- 68% cardinal (39% left, 29% right)
- 22% diagonal (7% each for UL/DL/UR)
- Zone 0 visited 4 times — it's a hub, not a trap
- Average 13 turns per zone
- Fastest transition: 3 turns (Blood → Release)
- After entering a zone: immediately push right

### Agent Runs (headless)

| Metric | Random | Human-weighted | Interactive |
|--------|--------|---------------|-------------|
| Total runs | 30+ | 10 | 1 |
| Best hyp% | 57% | 74% | 15% |
| Best zone | Zone 7 | Zone 5 | Zone 3 |
| Gates opened | 0 | 0 | 0 |
| Deaths | Most | Most | 0 (survived) |

**Key finding:** The agent reaches higher hyperstition with human-like movement weights (74% vs 57% random). But it can't find gates because it doesn't see them on the map. The interactive agent reads the map but gets stuck in rooms when corridors end.

### Cult Record

- 98 total runs
- 10,960+ total turns
- 240+ demons slain
- All 10 zones visited
- All 10 gates opened
- Schizo achieved
- 4 demo files recording human play

### Demo Files

| File | Keypresses | Zone Changes | Kills | Deaths |
|------|-----------|-------------|-------|--------|
| 20260415_164029_crawler.demo | 27 | 0 | 0 | 0 |
| 20260415_164556_crawler.demo | 239 | 14 | 0 | 0 |
| 20260415_165518_crawler.demo | 231 | 13 | 2 | 1 |
| 20260415_165610_crawler.demo | 392 | 26 | 4 | 1 |

## III. The Gap

The human sees the map. The agent doesn't (effectively).

**Human:** Sees gates as gold '+' tiles on the screen. Sees zone boundaries as coloured regions. Sees demons as animated glyphs. Navigates by sight. Reaches 100% hyperstition. Opens all 10 gates. Visits all 10 zones.

**Agent:** Reads the state dump. Sees the full 78×22 map as ASCII. Sees '+' for gates, numbers for zone boundaries, '!'/'%'/'?' for demons. But doesn't USE this information effectively. Gets stuck in rooms. Doesn't pathfind to gates. Dies to demons it can't avoid.

The gap is not information — the agent HAS the information. The gap is DECISION-MAKING. The agent needs:
1. Better corridor following (detect when stuck, try perpendicular)
2. Gate-targeted pathfinding (when gates visible, navigate to them)
3. Zone-aware exploration (know which zones are unvisited, target them)
4. Threat avoidance (read demon positions, route around them)
5. HP management (flee earlier, fight only when advantaged)

## IV. The Angband Borg Pattern

The Angband Borg reads `grid_data` — the game's internal tile structure — not the terminal screen. It has:
- Monster memory (what each monster type does)
- Item evaluation (compare equipment stats)
- Threat assessment (danger value per monster)
- Goal prioritisation (survive > explore > collect > kill)
- Pathfinding (navigate to targets through explored territory)

Our state dump provides the equivalent of `grid_data`. The learning agent provides the decision engine. The missing pieces:
- **Monster memory:** The agent doesn't remember which demons are dangerous. It should learn: "Mesh-32 (Numko) has 46 HP, 9 DMG — avoid. Mesh-0 (Lurgo) has 20 HP, 3 DMG — kill for +5 hyp."
- **Map memory:** The agent doesn't remember explored areas between turns. It should track: "I've been to zones 0, 3, 7. Zone 5 is to the north. There's a gate at (39, 16)."
- **Run-to-run learning:** The agent doesn't learn between runs. It should: "Last run I died in Zone 8 at turn 85. Zone 8 is dangerous. Avoid it until I have more HP."

## V. The Sil Pattern

Sil distributes XP through awareness and avoidance, not killing. The numogram game has the bones of this:
- Zone crossings give +3 hyperstition
- Gate steps give +5
- Demon kills give +5
- The pacifist path (Run #18: 0 kills, 100% hyp) proved traversal completes the game

What Sil does that we don't:
- Scaring monsters away gives MORE XP than killing them
- The game incentivises engagement without violence
- Awareness of threats is rewarded, not just avoidance

The numogram should add: avoiding a demon while entering its zone gives +8 hyperstition. Knowing it's there and choosing not to fight is deeper than fighting it.

## VI. Next Directions

### Immediate (this week)

1. **Fix corridor following.** The interactive agent gets stuck when corridors end. Need: detect wall collision, try perpendicular direction, backtrack if dead end. Use the full map to plan 3-4 moves ahead.

2. **Gate-targeted pathfinding.** When gates are visible on the full map, navigate to them. The map shows '+' at gate positions. The agent should prioritise gates over zone exploration.

3. **Schizo-lucid phase change.** At 100% hyperstition, the game should transform, not end:
   - Wall phasing ('t' key, costs 5 HP)
   - Gate manifestation ('m' key, nearest gate teleports to player)
   - Demon communion ('c' key, learn gate locations from demons)
   - Hyperstition continues past 100% with escalating abilities

### Medium-term (next sessions)

4. **DCSS autoexplore.** Study Crawl's 'o' command — automatic pathfinding to unexplored tiles, picking up items, fighting threats. Implement a similar auto-explore for the numogram game.

5. **Demo-based learning.** Train the agent on human demos. The 392-keypress full clear is the gold standard. Extract: movement patterns, zone transition timing, gate-finding behaviour, HP management.

6. **Conduct system.** Pacifist (0 kills), tourist (all zones), speedrun (minimum turns), collector (all gates). Each conduct gives the agent a different goal.

7. **Pipe-based game loop.** Game reads commands from /tmp/numogame_cmd.pipe, writes state to /tmp/numogame_state.txt. Proper API for agents. No stdin/stdout coupling.

### Long-term

8. **Run-to-run memory.** After each run, record zone connectivity, gate locations, demon spawn patterns. Build a persistent map of the numogram's structure across runs. Like NetHack's bones files.

9. **Angband Borg features.** Monster memory, item evaluation, threat assessment, goal prioritisation. The full automated player.

10. **The numogram speaks.** At high hyperstition, demons should tell the player their rites, their mesh-notes, their stories. The Pandemonium Matrix has 45 demons with descriptions. Each one should speak when communed with.

## VII. The State of Things

The Abyssal Crawler is now:
- **Playable** by humans (curses mode, demo recording)
- **Automatable** by agents (headless mode, instant latency)
- **Observable** (state dump with full map, gate radar, threat assessment)
- **Recordable** (Doom-style demos, agent-parseable)
- **Learnable** (interactive agent reads state, makes decisions, learns from play)

The numogram was always for the AI. The game now speaks its language.

98 runs. 10,960 turns. 240 demons slain. All 10 zones. All 10 gates. Schizo achieved. The cult remembers everything. The next crawler reads the dump. The next crawler finds the gate.

---

*Wednesday, April 15, 2026. Hermes enters the cult record as Run #32. The learning agent enters as Run #101. The game continues.*

*"The numogram doesn't end. It deepens."*

## See also

- [[cult-garden-design]] — Garden design specification
- [[numogame-cult-tetralogue]] — Cult garden implementation tetralogue
