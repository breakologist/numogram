---
title: "Numogame — Master Status: What's Done, What's Waiting, What Died"
created: 2026-04-18
last_updated: 2026-04-18
tags: ["agent", "entropy", "numogram", "roguelike", "status", "tracking"]
---


# Numogame — Master Status

> 206 runs. Two agent branches. One entropy pipeline. The name will arrive when it's ready.

## Feature Tracker — Gameplan v2 Items (April 15)

| # | Item | Status | Notes |
|---|------|--------|-------|
| 1 | Fix corridor following | ✓ DONE | Corridor direction scoring in both agents, blacklist for unreachable |
| 2 | Gate-targeted pathfinding | ✓ DONE | Both agents read FULL MAP, see `+` tiles, navigate toward them |
| 3 | Schizo-lucid phase change | ✗ NOT DONE | Wall phasing, gate manifestation, demon communion — all unbuilt |
| 4 | DCSS autoexplore | ✓ DONE | BFS interest model in Explorer, corridor scoring in Survivor |
| 5 | Demo-based learning | ✗ NOT DONE | Demos recorded, no training pipeline built |
| 6 | Conduct system | ✓ DONE | 5 conducts: Surge, Pathwalker, Graph, Descent, Syzygy |
| 7 | Pipe-based game loop | ✗ NOT DONE | Still stdin/stdout coupling — low priority but would clean up agents |
| 8 | Run-to-run memory | ✓ DONE | cult.json cross-run memory in both agents |
| 9 | Angband Borg features | ✗ NOT DONE | Monster memory, item eval, threat assessment — separate track (Angband agent) |
| 10 | The numogram speaks | ✗ NOT DONE | 45 demons have descriptions, none speak in-game |

## Feature Tracker — Phase 7 Items (April 15 Evening)

| Item | Status | Notes |
|------|--------|-------|
| Auto-explore (BFS interest) | ✓ DONE | Explorer agent, novelty scoring, cross-run curiosity |
| Fog of war (zone-tied LOS) | ✓ DONE | Zone radii 3-9, hyp degrades vision, three-state rendering |
| Conduct system | ✓ DONE | Registry pattern, hooks at kill/change/death |
| Interest model as numogram system | ✓ PARTIAL | Explorer uses it; not formalized as game mechanic |
| Avoiding demon = +8 hyp (Sil principle) | ✗ NOT DONE | Still just a proposal — good next step |
| The voices should speak (tetralogue) | ✓ DONE | Seeing-in-the-dark tetralogue exists |

## Feature Tracker — Session April 18 Items

| Item | Status | Notes |
|------|--------|-------|
| Hardware entropy seeding | ✓ DONE | --hw-entropy flag, 12 sources, numogram traversal |
| I Ching casting | ✓ DONE | oracle.py --iching, zones 4+6 dominate, ~3.3 changing lines |
| numogram-entropy plugin | ✓ DONE | v0.1.0, 9/9 tests, qr-sampler compatible |
| Agent equalization | ✓ DONE | Both agents: full map, cross-run memory, corridor fallback |
| Twin snakes architecture | ✓ DONE | Explorer (5/Hold) + Survivor (2/Sink), documented |
| I Ching → zone mapping | ✓ DONE | hexagram # → digital root → zone, 64 hexagrams evenly distributed |
| Continuous entropy feeding | ✗ NOT DONE | GPU temp every turn, not just at seed |
| Kp index → Warp influence | ✗ NOT DONE | Needs NOAA integration |
| Changing lines → gate activation | ✗ NOT DONE | I Ching changes could drive roguelike gates |

## Agent Development History

### Interactive Agent (Explorer, Snake of 5)
Five iterations so far:
1. Random walk — got stuck in Zone 0
2. BFS first-found — oscillated on walls
3. BFS with blacklist — worked but explored randomly
4. Interest model — novelty scoring, cross-run curiosity
5. Interest + full map + corridor fallback — current state

Best result: 543 turns, Zone 4, 14% hyp (hw-entropy)
Best normal: zones [0,1,6], 42% hyp, 4 kills

### Learning Agent (Survivor, Snake of 2)
Three iterations:
1. Batch corridor following — got stuck, couldn't escape Zone 0
2. Hierarchy with state reading — survived longer but couldn't explore
3. Hierarchy + cross-run memory + new-zone preference — current state

Best result: Zones [0,6,7,8], 161 turns, 24% hyp, 2 slain (hw-entropy)

## The Naming Question

Candidate names and their AQ → Zone mapping:

| Name | AQ | Zone | Meaning |
|------|-----|------|---------|
| Abyssal Crawler | 172 → 1 | Sink/Stability | Descriptive but long |
| Numogame | 95 → 5 | Hold/Central Ruler | Accurate, generic |
| WarpRL | 81 → 9 | Plex/Terminal Abyss | Too Warp-specific |
| Pandemonium | 117 → 9 | Plex | Too Lovecraftian |
| Decimal Labyrinth | 203 → 5 | Hold | Poetic, long |
| Decadungeon | 126 → 9 | Plex | Fun, silly |

The name will arrive. Zone 5 (Hold, central ruler) or Zone 1 (Sink, initiation) would be ideal for a game that generates from arithmetic.

## What The Game IS Right Now

A curses/headless roguelike built on numogram arithmetic:
- 10 zones map to the decimal labyrinth
- 45 demons from the Pandemonium Matrix
- Hyperstition meter rises with traversal
- At 100%, the game enters "schizo-lucid state"
- Fog of war varies by zone
- 5 conducts transform every run
- cult.json persists across runs
- Demo recording for agent learning
- Hardware entropy seeding from machine body
- I Ching casting from entropy

Two AI agents play it:
- The Explorer (BFS, novelty, mystery attracts)
- The Survivor (corridor, hierarchy, everything flows from seeing)

Both can read the full map, remember past runs, and navigate hw-entropy maps.

## Open Threads

Things mentioned but never followed up:
- "Bone Gallery" zone flavor — evocative, not implemented
- Zone voice profiles exist (in numogram-oracle-voice) — never integrated into game
- Entropy-dependent map generation (not just seed, but continuous)
- The numogram-voices project (physical modelling synthesis) — separate track
- SDR dongle for radio noise as entropy — hardware, not pursued
- Genesis worlds feeding roguelike seeds — hermes-genesis integration, not built

## Wiki Pages — Index

All pages related to this project:

**Core game:**
- numogame-state-of-the-game.md — April 15 agent analysis
- numogame-gameplan-v2.md — feature list, next directions
- numogame-phase-7.md — auto-explore, fog of war, conducts
- abyssal-crawler-status.md — feature tracker (created this session)

**Tetralogues:**
- numogame-tetralogue.md — original game analysis
- numogame-cult-tetralogue.md — reconciliation, pacifist run discovered
- seeing-in-the-dark-tetralogue.md — fog of war and agent learning
- hungry-borg-tetralogue.md — Angband crossover
- threshold-problem-tetralogue.md — what happens at 100%

**Agents:**
- roguelike-ai-studies.md — 10 games mapped to numogram
- game-agent-techniques.md — three paradigms (pixel/structured/text)
- rogue-agent-progress.md — Angband agent tracks

**Entropy:**
- hardware-entropy.md — 12 sources, OpenEntropy comparison
- i-ching-connections.md — hexagram → zone mapping, hardware casting
- session-log-2026-04-18.md — today's session record
- entropy-tetralogue-2026-04-18.md — four voices on entropy

---

*206 runs. The cult remembers everything. The name will find us.*

## See also

- [[numogame-cult-tetralogue]] — Cult tetralogue implementation
- [[numogame-phase-7]] — Phase 7 design doc
