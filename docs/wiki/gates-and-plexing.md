---
title: Gates and Plexing
created: 2026-04-13
last_updated: 2026-04-13
source_count: 1
status: draft
tags: [numogram, gate, plexing, arithmetic]
---

# Gates and Plexing

Gates are the directed connections between [[numogram]] zones, constructed through **plexing** (folding) — a qabalistic operation that reduces cumulative sums to single digits.

Source: Aamodt, *Unleashing the Numogram*.

## Construction Method

For each zone *n*, sum all integers from *n* down to 1 (cumulation), then repeatedly add the digits (plexing) until a single digit remains. The result is the target zone of Gate *n*.

| Gate | Cumulation | Plexing | Target |
|------|-----------|---------|--------|
| Gt-1 | 1 | 1 | 1 (self-loop) |
| Gt-3 | 2+1=3 | 3 | 3 |
| Gt-6 | 3+2+1=6 | 6 | 6 |
| Gt-10 | 4+3+2+1=10 | 1+0=1 | 1 |
| Gt-15 | 5+4+3+2+1=15 | 1+5=6 | 6 |
| Gt-21 | 6+5+4+3+2+1=21 | 2+1=3 | 3 |
| Gt-28 | 7+6+5+4+3+2+1=28 | 2+8=10 → 1+0=1 | 1 |
| Gt-36 | 8+7+...+1=36 | 3+6=9 | 9 |
| Gt-45 | 9+8+...+1=45 | 4+5=9 | 9 |
| Gt-0 | 0+anything=anything | — | 0 (dotted line, not a "real" gate) |

## Key Observations

**Triangular numbers**: The cumulated values are triangular numbers (T₁=1, T₃=6, T₆=21, T₈=36, T₉=45). See [[triangular-numbers]].

**Warp convergence**: Gt-6, Gt-15, and Gt-21 all point to Warp zones (6 or 3). Three gates feed the Warp vortex.

**Plex convergence**: Gt-36 and Gt-45 both point to Zone 9 (Plex). The two largest gates both terminate in the abyss.

**Self-loops**: Gt-1 (1→1) and Gt-9/45 (9→9) are self-referential. Gt-0 (0→0) is drawn as a dotted line — it "does not indicate any kind of change or travel."

## The Pandemonium Gate (Gt-45)

Gt-45 is the most significant gate: 9+8+...+1 = 45 = 9. The gate from Zone 9 points back at Zone 9. This is the closed loop, the mouth that swallows itself. The **45 demons** of the Pandemonium Matrix are attuned to this gate. T₉=45.

See also: [[numogram-plex]], [[triangular-numbers]], [[subdecadence]]

## Application: Roguelike Shortcuts

Gates map to non-obvious connections between dungeon zones — shortcut doors that skip portions of the Time-Circuit:

- **Gt-10** (4→1): A chute from Zone 4 deep into Zone 1, bypassing the Hold current
- **Gt-15** (5→6): An elevator from Zone 5 up into the Warp at Zone 6
- **Gt-21** (6→3): The Warp transit — a spiralling corridor through chaos
- **Gt-36** (8→9): A plunge from Zone 8 into the Plex abyss

See also: [[brogue-design-principles]]
