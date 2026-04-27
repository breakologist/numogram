---
title: Current
created: 2026-04-27
source: cli/aq_calculator_canonical.py
status: stub
tags: [current, syzygy, flow, region, warp, plex, time-circuit]
---

# Current

A **current** is the directed flow produced by a syzygy. It is the absolute difference between the paired zones and determines the character of movement through that region of the Numogram.

## The Five Currents

| Current | Syzygy | Value | Region | Character |
|---------|--------|-------|--------|-----------|
| Sink | `4::5` | 1 | Time-Circuit | Descent, original subtraction |
| Hold | `2::7` | 5 | Time-Circuit | Stasis, waiting in the rising drift |
| Rise | `1::8` | 7 | Time-Circuit | Ascent, progressive levitation |
| Warp | `3::6` | 3 | Warp | Turbulence, spiralling outward |
| Plex | `0::9` | 9 | Plex | Abyssal return, sudden flight |

Current names come from the Qliphothic mapping used in `oracle.py` and the CCRU's *Unleashing the Numogram*. They carry directional semantics:

- **Sink (1)**: downward pull, repeated patience
- **Hold (5)**: jittery equilibrium, strategic stasis
- **Rise (7)**: upward arc, fluid evolution
- **Warp (3)**: vortical acceleration, chaotic breakthrough
- **Plex (9)**: terminal surge, possession

## Flow and Direction

Each current has a **tractor zone** — the lower digit in the pair, towards which the flow is conventionally drawn:

- `4::5` → current **1** pulls toward Zone-5
- `2::7` → current **5** pulls toward Zone-7
- `1::8` → current **7** pulls toward Zone-8
- `3::6` → current **3** pulls toward Zone-3
- `0::9` → current **9** pulls toward Zone-9

In the Time-Circuit, the three currents interlock so that following them anticlockwise visits all six zones in order: `1 → 8 → 2 → 7 → 5 → 4 → 1`.

## Currents as Game Mechanics

In the roguelike (`numogram_roguelike.py`), the current of the player's current zone determines:

- Terrain generation bias (Sink = descending corridors, Rise = ascending shafts)
- Demon aggression patterns (Warp = swarm spawns, Plex = boundary incursions)
- Hyperstition meter decay rate (Plex accelerates decay, Hold stabilises)

## Oracle Readings

The Book of Paths entries for each zone embed the current's character:
- Zone-3 (Warp current): "Abysmal Comprehension. Ultimate descent beyond completion. Burning excitement provokes breakthrough into immersive nightmares."
- Zone-5 (Hold current): "Slipping Backwards. Waiting in the Rising Drift precedes return."
- Zone-9 (Plex current): "Sudden Flight. Seized from the Heights. One test on the way. Possession."

---

*See also:* `syzygy`, `zone`, `time-circuit`, `warp`, `plex`, `numogram-oracle`, `roguelike-ai-studies`
