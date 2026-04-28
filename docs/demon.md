---
title: Demon — Numogram Entity
created: 2026-04-27
source: pandemonium-matrix.json + demon-name-generation
status: stub
tags: [demon, entity, pandemonium, net-span, zone, current, carrier]
---

# Demon — Numogram Entity

**Demons** are the inhabitant entities of the Decimal Numogram. They are not metaphorical — they are the connective tissue of the system itself. The complete set of 45 demons forms the **Pandemonium Matrix** (see [[pandemonium]]), a double-triangular distribution across zones and currents.

## Nature & Structure

- **Total population**: 45 demons (triangular cumulation: T₉ = 45)
- **Zone distribution**: Zone `z` contains exactly `z` demons (triangular occupancy: 1+2+…+9=45)
- **Current distribution**: Current `c` carries `10−c` demons (reverse triangular: 9+8+…+1=45)
- **Net-span connectivity**: Each demon connects two zones (`X::Y`), forming a complete directed graph on 10 vertices (C(10,2)=45 edges)
- **Name structure**: 7 characters (CVCVCVC), derived from zone-syllable combination per Amy Ireland's `demon-name-generation`

## The Five Carrier Demons

Five demons sit on pure syzygy pairs (sum=9) and anchor the major currents:

| Demon | Net-Span | Current | Role |
|-------|-----------|---------|------|
| **Katak** | `4::5` | Sink (1) | Carrier of the Sink current |
| **Djynxx** | `3::6` | Warp (3) | Carrier of the Warp current |
| **Oddubb** | `2::7` | Hold (5) | Carrier of the Hold current |
| **Mur Mur** | `1::8` | Rise (7) | Carrier of the Rise current |
| **Uttunul** | `0::9` | Plex (9) | Carrier of the Plex current |

These five form the backbone of the net-span lattice — their connections are the primary syzygies that define the three regions.

## Classes & Roles

Within the 45-demon taxonomy (see `pandemonium-matrix.json` for full list):

- **Chronodemons** — Corridor guardians; tied to zone transition mechanics
- **Amphidemons** — Portal keepers; gate activation conditions
- **Xenodemons** — Extraneous/outside entities; boss encounters; Mesh-Anchored
- **Cyclic Chronodemons** — Recurring through time loops
- **Carrier Demons** — The five syzygy-anchored current bearers (above)

## Individual Demon Pages

Currently documented:

- [[demon-djynxx]] — Warp carrier (6::3), xenodemon, swarmachine, the Jinn
- [[demon-uttunul]] — Plex carrier (9::0), abyssal, the False Nun
- [[demon-name-generation]] — Amy Ireland's combinatorial phonetic system (zone syllables → 7-char names)
- [[demon-player-refinement-notes]] — Gameplay refinement: 50 aspects mapped to mechanics (uses 0(rphan) d(rift>) tables)

**See** [[pandemonium]] for the full 45-member matrix with zone/current distribution tables and net-span connectivity.

## Cross-References

- [[pandemonium]] — Complete 45-demon matrix (double-triangular structure, Gt-45)
- [[pandemonium-matrix.json]] — Canonical JSON database (45 entries with type, zone, current, net-span, aspects)
- [[syzygy]] — Syzygy pairs and carrier demon distribution
- [[gate]] — Gate-45 (Pandemonium Gate) as the microcosmic lair
- [[zone]] — Zone occupancy patterns (Zone z contains z demons)
- [[current]] — Current distribution (Current c carries 10−c demons)
- [[subdecadence]] — The 40-card deck (plus 5 extra) maps directly to the populace demons
- [[demon-name-generation]] — Phonetic construction method (zone syllables → CVCVCVC format)
- [[numogram-visualizer-v7]] — Demon markers displayed on zone map when gate thresholds crossed
- [[tetralogue]] — Voice methodology applied to demon analysis (e.g., fortyfive-demons-tetralogue)
- [[numogram-calculator]] — `get_demon()` net-span lookup function

---

*Demons are the spaces between zones given teeth. The 45 are not inhabitants — they are the connections themselves, animate.*
