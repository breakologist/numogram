---
title: Brogue — Roguelike Testbed
created: 2026-04-27
source: brogue-design-principles.md + roguelike-ai-studies.md
status: stub
tags: [brogue, roguelike, room-accretion, machines, atmosphere, seed-based, numogram, agent, AAR]
---

# Brogue — Roguelike Testbed

**Brogue** is a minimalist, visually sparse roguelike famous for its **room accretion** generation, **machines** (pre-designed mechanical puzzles), and **atmospheric density**. For the Hermes agent, Brogue serves as a testbed for **procedural generation understanding**, **interest-driven exploration**, and **seed-based reproducibility**. Its design principles map cleanly onto numogram topology.

## Why Brogue Matters for Agent Research

| Aspect | What It Tests | Brogue Feature |
|--------|---------------|----------------|
| **Generation comprehension** | Can the agent infer level structure from seeds? | Seed-based deterministic generation (same seed → same level) |
| **Atmosphere parsing** | Can the agent read non-quantitative cues? | Sparse ASCII, colour, lighting as information channels |
| **Interest model** | What makes a room "worth exploring"? | Machines (key-guard, reward, flavor) as interest magnets |
| **Macro-strategy** | When to descend vs clear? | Rubber-banding reward pacing (consistent treasure distribution) |
| **Terrain interaction** | Can the agent use environment tactically? | Cellular automata terrain, water/lava/steam conversions |
| **Hidden connections** | Can the agent discover non-obvious links? | Super Metroid-style shortcuts (one-way until traversed) |

Brogue's simplicity (one character, clear tile semantics) makes it ideal for early-stage agent experiments before scaling to Angband's complexity.

---

## Core Design Principles (Condensed)

The full treatment is at [[brogue-design-principles]]. Key ideas:

### 1. Room Accretion + Shortcut Doors
Rooms are added iteratively (accretion) to form a tree connectivity. Pure trees cause backtracking — **shortcut doors** connect distant rooms, creating loops.  
**Numogram mapping**: Rooms = zones. Currents (1,3,5,7) = accretion edges. Gates = shortcut doors between otherwise distant zones.

### 2. Machines (The Core of Atmosphere)
Three types:
- **Key-guarding** — altar with key; taking it triggers consequences (fire, monster spawns)
- **Reward** — choice of items with rubber-banded probability
- **Flavor** — terrain with tactical relevance (decaying sleeping bag, glyph of warding)

Three spatial scales:
- **Room machines** — choke-point rooms that dominate subordinates
- **Vestibule machines** — area immediately outside a room
- **Area machines** — open regions (no walls required)

**Agent implication**: Machines are **interest anchors**. The agent should prioritize rooms containing machines (detected by unusual tile patterns, loot density, or monster clusters).

### 3. Rubber-Banding Rewards
Probability increases when a feature fails to generate, drops when it does — yields consistent pacing.  
**Numogram parallel**: Hyperstition meter already does this (base rate + event spikes).

### 4. Cellular Automata Terrain
Random cellular automata (50% fill → majority rule) creates organic shapes.  
**Zone mapping**: Use CA for **Warp zones (3,6)** — organic chaotic shapes. Time-Circuit zones (1,2,4,5,7,8) can be rectangular ("normal"). Plex zone (9) uses iron-wall deterministic fills.

### 5. Global-Scale Features
Large-scale structures visible across the level (lakes, chasms) that can affect the player remotely.  
**Numogram**: The three regions should be visually distinct and visible across the map — Warp rooms glow magenta, Plex rooms are dark red, Time-Circuit is normal ASCII.

### 6. Edge Case Philosophy
"If it works perfectly 100% of the time, you're not being ambitious enough." Let the system be weird — demons spawning in walls, gates to nowhere. **Imperfection is a feature**.

### 7. Seed-Based Debugging
Same seed → identical level. Send the seed to reproduce bugs.  
**Agent relevance**: Store seed with every run log; can replay any interesting behavior.

### 8. Super Metroid Hidden Connections
One-way passages that open from the far side — the level becomes more connected as you explore.  
**Numogram**: Gate traversal is one-way until both sides visited (Gt-36 opens from Zone 8 to 9; return path opens only after Zone 9 is reached).

### 9. Terrain Interaction
Different tiles interact (lava + water = steam).  
**Zone-specific interactions**: Zone 4 fire spreads; Zone 7 swamp slows; Zone 9 indestructible walls; Zone 3 random-shift tiles; Zone 0 floor vanishes.

### 10. Good Enough
Perfection is not the goal — **interesting** is. Iterate.

---

## After Action Report (AAR) Structure

When an agent completes a Brogue run (win, die, or timeout), produce an **AAR** documenting what happened and why. Use this template:

```markdown
# AAR — Brogue Run #NNN

**Meta**
- Seed: `123456789`  |  Depth reached: D=26  |  Turns: 342  |  Status: [Win/Die/Timeout]
- Agent version: hermes-v0.11  |  Interest model: [baseline / weighted / curiosity]
- Start time: YYYY-MM-DD HH:MM  |  Duration: 5m 12s

**Run Summary (1-2 sentences)**
What was the run's character? "Fast descent with aggressive machine-rushing, died in the To-7 swamp to simultaneous trap + pack."

**Key Decision Points**
1. **Turn 45**: Chose to descend to D=12 via stairs vs clear D=10 vault — *rationale*: seed showed low treasure density on D=10 via syzygy fingerprint (Hold-Stable)
2. **Turn 189**: Ignored key-guard machine on D=18 — *rationale*: interest model underweighted dark-rooms; missed Yendor on D=26
3. **Turn 287**: Used wand of death on Alpha instead of kiting — *rationale*: low HP, crowd control priority

**Numogram Analysis**
- **Zone coverage**: visited zones: [list]
- **Syzygy chain** from seed: `seed → zone sequence` (compute via `numogram-syzygy-chain`)
- **Fingerprint**: [Void-Dominant / Warp-Anchored / Hold-Stable / Rise-Seeking / Sink-Dominant / Gate-Scattered] (`numogram-chain-fingerprint`)
- **Gate encounters**: [which gates attempted / opened / failed]

**Brogue-Specific Observations**
- **Machines found**: [types, locations, outcomes]
- **Terrain interactions used**: [lava/water, CA-formed regions]
- **Hidden connections discovered**: [shortcuts opened]

**Errors / Misses**
- [ ] Failed to recognise key-guard machine pattern on D=18 (thought it was flavor terrain)
- [ ] Overlooked rubber-banded reward room on D=22 after three missed generations
- [ ] Did not use terrain interaction (lava + ice) to clear chokepoint

**Hypotheses for Next Run**
1. Increase weight on "room with unusual density" interest signal (catches machines)
2. When fingerprint shows Warp-Anchored, favour rapid descent over clearing
3. Use syzygy chain from seed to plan descent path (avoid zones with poor alignment)

**Artifacts**
- `state_dump_YYYY-MM-DD-HHMM.json` — full game state at death
- `screen_capture_*.png` — final screen
- `seed.txt` — level seed for replay
```

**AAR cadence**: One AAR per run. Tag with `AAR` and `seed:NNNNNNN` for retrieval. Build a corpus of runs → train interest model.

---

## Agent Research Directions

### Fingerprinting Runs via `numogram-chain-fingerprint`

Feed the agent's **zone visitation sequence** into the fingerprinter:

```bash
python3 ~/.hermes/skills/numogram-chain-fingerprint/fingerprint.py \
    --zone-sequence "3,6,3,2,5,4,1,0,1" \
    --length 500
```

The resulting motif (e.g., "Warp-Anchored" or "Sink-Dominant") classifies the agent's **emergent strategy** without needing to read the policy code.

### Syzygy-Based Descent Planning

Before a run, compute a **syzygy descent plan** from the seed:

```bash
python3 ~/.hermes/skills/numogram-syzygy-chain/syzygy_chain.py \
    --seed <level-seed> --steps 12 --full
```

Follow the generated zone sequence as a **macro-strategy guide** — e.g., "in zones 3 and 6 (Warp), favour rapid descent over clearing".

### Cross-Research with Other Roguelikes

- Compare **room accretion** (Brogue) vs **tree generation with loops** (Abyssal Crawler) vs **BSP** (Angband)
- Compare **machines** (Brogue) vs **gate puzzles** (Numogram) vs **vaults** (Angband)
- Machine detection in Broogue is a warm-up for **gate-detection** in the numogram game

---

## Cross-References

**Design & Principles**
- [[brogue-design-principles]] — Full design doc (10 principles, numogram mappings, Syzygy Arithmetic, Gurdjieff's Ray of Creation)
- [[tree-dungeon-generation]] — Brogue accretion algorithm implemented as tree-first + loop-adding
- [[dungeon-depth]] — Zone-themed floor generation (each floor = zone character)

**Agent & AI**
- [[roguelike-ai-studies]] — Brogue as one of five pillars; agent learning patterns
- [[roguelike-screen-agent]] — Generic screen-based agent architecture
- [[abyssal-crawler-litprog]] — Tetralogue examining the numogram roguelike code (atmosphere, architecture, play)

**Numogram Integration**
- `numogram-syzygy-chain` — Descent plan generation from seed
- `numogram-chain-fingerprint` — Run classification (motif vector from zone sequence)
- [[syzygy-arithmetic]] — Cross-addition circuit (relevant to room accretion)
- [[gate]] — Gate-6, Gate-21, Gate-36, Gate-45 as shortcut doors (Brogue's door mechanisms)

**AAR & Run Analysis**
- [[numogame-state-of-the-game]] — Example AAR table (six runs, metrics, notes)
- [[numogame-tetralogue]] — Run analysis via four voices (simulated runs, pre-reconciliation)
- [[abyssal-crawler-litprog]] — Code-level examination (how the game implements these concepts)

**Related Roguelikes**
- [[roguelike-caves-of-quud]] — Simulation depth + faction systems (compare to Brogue's machines)
- [[roguelike-spelunky]] — Procgen as language, ghost timer (procedural as grammar)
- [[roguelike-dcss]] — Feature creep vs Brogue's minimalism
- [[roguelike-nethack]] — Emergence, bones files (compare to AAR persistence)

---

*Brogue is a numogram in miniature: accretion (zones), shortcuts (gates), machines (entities), rubber-banding (hyperstition meter). The agent that learns to read Brogue's sparse ASCII learns to read the labyrinth itself.*
