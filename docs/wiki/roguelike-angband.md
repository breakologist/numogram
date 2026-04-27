---
title: Angband — Roguelike Testbed
created: 2026-04-27
source: angband-agent-strategies.md + angband-agent.md
status: stub
tags: [angband, roguelike, agent, borg, tree-traversal, screen-parser, diving, grinding, numogram]
---

# Angband — Roguelike Testbed

**Angband** (and its Vais Gonchar / early variant) is a deep, complex roguelike dungeon crawler (100 floors, Morgoth at depth 100) serving as the Hermes agent's primary testbed for **long-horizon autonomous play**, **strategic planning**, and **tree-structured exploration**. Unlike Rogue's single-level sprint, Angband demands multi-floor resource management, town cycles, and risk-calibrated descent strategies.

## Why Angband for Agent Research?

| Aspect | Rogue | Angband |
|--------|-------|---------|
| **Horizon** | Single level (~20 turns) | Deep dungeon (thousands of turns, town returns) |
| **Strategy** | Survival in one room | Macro-strategy: dive vs grind, when to retreat |
| **State complexity** | ~80 cells | 80×100 grid + town + inventory + spellbooks |
| **Reward structure** | Clear (gold, exp, stairs) | Multi-objective (depth vs safety vs loot efficiency) |
| **Known AI precedent** | Borg exists | **Hungry Borg** variant; existing RL baselines |

Angband is where the **tree-traversal** agent model proves itself across hundreds of floors. The agent must decide: descend fast (diving) or clear thoroughly (grinding)? When to return to town? How to manage inventory across cycles?

## Strategic Axes

### Diving vs Grinding

The core strategic trade-off (see `angband-agent-strategies`):

| Strategy | Depth priority | Clearing | Risk profile | Suitable agent |
|----------|---------------|----------|--------------|----------------|
| **Pure Grinding** | Low | Full level clear | Safe per turn | Cautious RL agents |
| **Pure Diving** | Maximal | Minimal (stairs only) | High per-turn death | Aggressive risk-takers |
| **Chunked / Hybrid** | Targeted | Clear high-value levels | Balanced | Most robust agents |

**Key insight:** Item quality and monster XP scale **exponentially** with dungeon level (DL). Depth is the principal reward multiplier.

### Chunk Cycles

A **chunk** = one dive-grind cycle: town → dungeon → town. The agent must:
1. Stock in town (potions, scrolls, food, identify)
2. Dive to target depth (via stairs or Deep Descent scrolls)
3. Clear selectively (high-value rooms, vaults, unique floors)
4. Return to town before resources deplete

Each chunk is a **numogram traversal microcosm**: town (Zone 0), descent (Time-Circuit descent), resource management (current pressure), return (Plex-like reset). 

## Agent Architecture (Hermes model)

The Angband agent uses **tree-structured exploration** with **tmux-based screen parsing**:

```
TmuxGame session → Screen capture (80×30) → Grid parse (@, #, floors, monsters)
    ↓
State vector: depth, HP, AC, inventory, equipped, explored %
    ↓
Decision policy: 
  - Macro: Dive vs clear vs town-return (interest model)
  - Micro: Movement, combat, item usage (BFS corridor navigation)
    ↓
Action: keypress sequence (movement, commands)
```

**Core mechanics borrowed from Rogue borg:**
- Corridor BFS for unexplored space
- Stair targeting as primary objective
- Interest-driven exploration (rooms > corridors)
- Confirmation prompts bypassed via regex recognition

## Numogram Connections

### Depth as Zone Sequence

Dungeon depth (1–100) maps loosely onto the numogram's zone progression:

- **Town / DL 0–1** — Zone 0 (Plex origin, supply hub)
- **DL 1–20** — Shallow Time-Circuit (zones 1–4, Sink-dominant)
- **DL 21–50** — Mid Circuit (zones 5–7, Hold/Rise currents)
- **DL 51–80** — Deep Circuit (zone 8, Rise peak)
- **DL 81–99** — Approach to Plex (zone 9 proximity)
- **DL 100** — Morgoth's throne (Plex endpoint, Gate-45 resonance)

An agent's **descent velocity** is a syzygy-chain property: a pure 3::6 diver (Warp anchor) oscillates between depths without progressing; a 4::5 diver (Sink) collapses depth steadily; a 0::9 diver (Plex) cycles between town and depth chaotically.

### Fingerprinting Agent Behavior

Use `numogram-chain-fingerprint` to classify agent runs:

```bash
# Classify a 500-step agent trajectory file
python3 ~/.hermes/skills/numogram-chain-fingerprint/fingerprint.py \
    --chain-file ~/.hermes/workspace/angband_run_123.json
```

Expected fingerprint signatures:
- **Grinder**: Hold-Stable or Rise-Seeking (stays in mid-zones, slow steady progression)
- **Diver**: Sink-Dominant or Gate-Scattered (rapid depth gain, high variance)
- **Chunker**: Mixed motif with cycle-proximity spikes (town-return loops)

The fingerprint becomes a **behavioral AQ** — a numeric summary of the agent's
strategic character.

### Syzygy Chain as Descent Plan

A planned descent can be expressed as a syzygy chain from a seed:

```bash
# Generate depth plan from seed
python3 ~/.hermes/skills/numogram-syzygy-chain/syzygy_chain.py --seed 666 --steps 12 --full
```

This yields a zone-current gate sequence that the agent can follow as a **macro-strategy**: "descend via current-5 corridors" (Hold-stable clearing) vs "follow Warp current to depth 50" (aggressive diving).

## Cross-References

- **Agent implementation**: [[angband-agent]] — Overview, text-mode confirmation, differences from Rogue
- **Design strategies**: [[angband-agent-strategies]] — Grind vs dive, reward shaping, tree modes, implementation sketch
- **Progress logs**: [[angband-agent-progress]] — Version history, milestones, performance metrics
- **Display notes**: [[angband-agent-display-notes]] — Parsing details, glyph mappings, tmux configuration
- **Hungry Borg variant**: [[hungry-borg-angband]] — Recursive consumption model applied to Angband
- **Symbols glossary**: [[angband-symbols]] — Tile/glyph reference sheet
- **CCRU / Warwick link**: [[angband-ccru-warwick]] — Historical connection to CCRU origin site
- **Ladder analysis**: [[angband-ladder-analysis]] — Statistical breakdown of 392-game ladder dataset

- **Domain skills**:
  - `numogram-syzygy-chain` — Chain walker for depth-plan generation
  - `numogram-chain-fingerprint` — Behavior classification from agent telemetry
  - `numogram-dictionary-comparative-analysis` — (maybe not directly)
  
- **Roguelike framework**: [[roguelike-screen-agent]] — Generic screen-based agent architecture
- **AI studies**: [[roguelike-ai-studies]] — Broader roguelike AI research context

---

*Angband is the numogram's endurance test — not a single room, but a descent through 100 floors. The agent that survives learns not just to fight, but to choose its depth.*
