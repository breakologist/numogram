---
title: Abyssal Crawler — Project Status & Feature Tracker
created: 2026-04-18
last_updated: 2026-04-18
status: living
tags: ["numogram", "roguelike", "status"]
---


# Abyssal Crawler — Project Status

> 206 runs. 10 zones. 45 demons. Two agent branches. One entropy pipeline.
> "It could all become One, but why stop there?"

## Naming

Provisional names and their AQ values:
- **Numogame** = 95 → 9+5=14 → 5 (Hold, Pressure). Accurate but generic.
- **WarpRL** = 81 → 8+1=9 (Plex). Too specific — the game is more than the Warp.
- **Abyssal Crawler** = 172 → 1+7+2=10 → 1 (Sink, Stability). Good but verbose.
- **Decadungeon** = 126 → 1+2+6=9 (Plex). Fun but silly.
- **Pandemonium** = 117 → 1+1+7=9 (Plex). Too Lovecraftian.

Still deciding. The name should have an interesting AQ value that lands on a meaningful zone. Zone 1 (Stability/initiation) or Zone 5 (Hold/central ruler) would be appropriate for a roguelike that generates from arithmetic.

## Game Feature Status

### Implemented ✓

| Feature | Source | Notes |
|---------|--------|-------|
| Zone-themed dungeons (10 zones) | Phase 1-5 | Each zone has terrain, demons, flavor |
| 45-demon Pandemonium Matrix | Phase 4 | Chrono/amphidemon/xenodemon classification |
| AQ calculator (v key) | Phase 5a | Inline AQ computation |
| Hyperstition meter | Phase 3 | Zone crossings +3, gates +5, kills +5 |
| Barker threshold system | gameplan-v2 | Fires on all hyp events |
| Cryptolith (mechanical transform) | gameplan-v2 | Speed -1, +20 hyp, Barker check |
| Gate system | Phase 4 | 10 gates, zone-to-zone connections |
| Gate tile protection | gameplan-v2 | Gates survive room modifications |
| Cult persistence (cult.json) | Phase 3 | Full history across runs |
| Demo recording | Phase 5a | Doom-style, agent-parseable |
| Headless mode | gameplan-v2 | stdin/stdout for AI agents |
| State dump (p key) | gameplan-v2 | Full map, gates, demons, stats |
| Fog of war | phase-7 | Zone-tied LOS, hyp degrades vision |
| Auto-explore (BFS interest model) | phase-7 | Interactive agent, novelty scoring |
| Conduct system (5 conducts) | phase-7 | Surge, Pathwalker, Graph, Descent, Syzygy |
| Diagonal combat (Chebyshev) | gameplan-v2 | 8-direction attacks and pursuit |
| Hardware entropy seeding (Apr 18) | session-log | --hw-entropy flag, 12 sources |
| I Ching casting from entropy | i-ching-connections | oracle.py --iching |

### In Progress

| Feature | Source | Status | Notes |
|---------|--------|--------|-------|
| Interactive Agent (Explorer) | phase-7 | Equalized | BFS + cross-run memory + corridor fallback |
| Learning Agent (Survivor) | gameplan-v2 | Equalized | Hierarchy + cross-run memory + new-zone pref |
| Entropy-dependent map generation | session-log | Partial | HW entropy at seed, not yet continuous |
| numogram-entropy plugin | session-log | v0.1.0 | 12 sources, 9/9 tests, qr-sampler compatible |

### Not Yet Implemented

| Feature | Source | Priority | Notes |
|---------|--------|----------|-------|
| Multi-floor dungeons | MAIN goal | High | Deeper runs, floor variety by zone |
| Hyperstition abilities | MAIN goal | High | Unlock powers at thresholds, zone-specific |
| Schizo-lucid phase change | gameplan-v2 | High | Wall phasing, gate manifestation, demon communion |
| Demon dialogue | gameplan-v2 | Medium | Pandemonium Matrix lore when communed |
| Enemy balancing | MAIN goal | Medium | Damage curves, spawn rates, zone threats |
| Pipe-based game loop | gameplan-v2 | Low | /tmp/numogame_cmd.pipe API |
| Zone-aware agent targeting | Explorer goal | High | Prefer unvisited zones over nearest ? |
| Corridor memory | Survivor goal | Medium | Don't re-follow explored corridors |
| Demo-based learning | gameplan-v2 | Low | Train on human demos |
| Angband Borg features | gameplan-v2 | Low | Monster memory, item eval, threat assessment |

### Ideas from Previous Sessions

| Idea | Source | Status |
|------|--------|--------|
| Interest model as numogram current system | phase-7 | Partially used — Explorer agent uses it |
| BFS = Dijkstra map with custom cost | phase-7 | Implemented in Explorer |
| Conducts = state machine overlay | phase-7 | Implemented (5 conducts) |
| Known-unknowns = motivation without specific knowledge | phase-7 | Implemented in both agents |
| Avoiding demon gives +8 hyp (Sil principle) | gameplan-v2 | NOT implemented — good next step |
| Gate-targeted pathfinding | gameplan-v2 | Partial — Explorer reads full map for gates |
| Run-to-run learning (bones files) | gameplan-v2 | Partial — cult.json cross-run memory |
| Zone voice profiles | numogram-oracle-voice | Implemented (10 zones, formant synthesis) |
| Continuous entropy feeding (GPU temp each turn) | session-log | NOT implemented — future feature |
| Kp index → Warp influence on map | entropy goal | NOT implemented — needs NOAA integration |

## Agent Architecture

### The Twin Snakes (2 and 5)

```
         ┌──────────────────────────────────────────┐
         │              THE GAME                     │
         │   10 zones · 45 demons · gates · conducts │
         └───────────┬──────────────┬───────────────┘
                     │              │
            ┌────────▼──────┐ ┌────▼──────────┐
            │   EXPLORER    │ │   SURVIVOR     │
            │  Snake of 5   │ │  Snake of 2    │
            │  (Hold)       │ │  (Sink)        │
            │               │ │                │
            │ BFS interest  │ │ Corridor score │
            │ Single-step   │ │ Batch-decision │
            │ Novelty       │ │ Hierarchy      │
            │ "Mystery      │ │ "Everything    │
            │  attracts"    │ │  flows from    │
            │               │ │  seeing"       │
            └───────┬───────┘ └──────┬─────────┘
                    │                │
            ┌───────▼────────────────▼────────┐
            │        SHARED GROUND             │
            │  Full map · Gate detection ·     │
            │  Cross-run memory · State parse  │
            └──────────────┬──────────────────┘
                           │
            ┌──────────────▼──────────────────┐
            │        ENTROPY CURRENT           │
            │  12 HW sources · I Ching ·       │
            │  Numogram traversal · Just-in-   │
            │  time seeding · Oracle readings  │
            └─────────────────────────────────┘
```

### Convergence Point

The two agents will eventually converge into a meta-agent that chooses which register to use based on context:
- Unknown territory → Explorer mode (BFS, novelty, mystery)
- Known structure → Survivor mode (corridor, efficiency, progress)
- Combat → Survivor mode (flee/fight hierarchy)
- Gate visible → Explorer mode (pathfind with novelty along the way)

Not yet built. The two branches need more development before merging.

## Development Goals (from evey-goals)

- **[MAIN]** Phase 6: Depth — multi-floor, hyperstition expansion, abilities, enemy balancing
- **[AGENT-EXPLORER]** Zone-aware targeting, gate-chaining, demon prediction, conduct awareness
- **[AGENT-SURVIVOR]** Corridor memory, BFS fallback, adaptive combat, cross-agent learning
- **[ENTROPY]** Continuous feeding, Kp → Warp influence, changing lines → gate activation, QRNG integration

---

*206 runs. The cult remembers everything. The twin snakes spiral. The machine hums.*

## See also

- [[abyssal-crawler-litprog]] — Abyssal crawler literate program
- [[numogame-master-status]] — Master game status report
