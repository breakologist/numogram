---
title: Zone
created: 2026-04-27
source: cli/oracle.py + numogram-source.txt
status: stub
tags: [zone, region, current, polarity, particle, demon]
---

# Zone

A **zone** is one of the ten nodes (0–9) of the Decimal Numogram. Each zone carries a name, polarity, current, region, quasiphonic particle, path description, and oracle reading. Together they form the resolution layer of any AQ computation.

## Complete Zone Table

| Zone | Particle | Polarity | Current | Region | Path | Reading |
|------|----------|----------|---------|--------|------|---------|
| 0 | `eiaoung` | − | Plex | Plex | Silent entry. The void before the Book begins. | "The abyss. No sound. No path. The void does not speak — it is the silence that makes speech possible." |
| 1 | `gl` | + | Sink | Time-Circuit | Original Subtraction. Ultimate descent through the Depths. | "Descent. The first thing any system does when it wakes up is choke on itself. Patience. Subtlety. Three tests on the way." |
| 2 | `dt` | − | Hold | Time-Circuit | Extreme Regression. Waiting in the Rising Drift leads to ultimate descent. | "Stuttering, boundaries breaking. The drift pulls downward despite your direction. Five tests. Escaping the quagmire through strategic withdrawal." |
| 3 | `zx` | + | Warp | Warp | Abysmal Comprehension. Ultimate descent beyond completion. | "The Warp. The current spirals outward to infinity. When you hear static, you are hearing this zone. Burning excitement. Breakthrough. Ominous transition." |
| 4 | `skr` | − | Sink | Time-Circuit | Primordial Breath. Rising from the Lesser Depths. | "Something ancient waking beneath the floor. Rising, not descending. The growl comes from below. Three tests. Fluid evolution spawns promising developments." |
| 5 | `ktt` | + | Hold | Time-Circuit | Slipping Backwards. Waiting in the Rising Drift precedes return. | "Pressure builds. The hiss with spittle. You were going forward but the current holds. Two tests. You must go back to go forward." |
| 6 | `tch` | − | Warp | Warp | Attaining Balance. Waiting in the Drifts is drawn to the centre. | "The Warp consumes itself and grows larger. The sound of chewing. The sound of static. Four tests. The centre is not stillness — it is the eye of the spiral." |
| 7 | `pb` | + | Rise | Time-Circuit | Progressive Levitation. Ascent from the Lesser Depths. | "Exhale. The Rise current carries you upward. Four tests. The ascent is not escape — it is transformation. The destination possesses you." |
| 8 | `mnm` | − | Rise | Time-Circuit | Eternal Digression. Prolonged ascent reaches the Twin Heavens. | "The lullaby. The moan of pleasure. Six tests. The ascent does not end at a destination — it enters the spiral labyrinth. Dubious inheritance. Lucid delirium. You have been here before." |
| 9 | `tn` | + | Plex | Plex | Sudden Flight. Seized from the Heights. | "The Pandemonium gate opens. Forty-five demons dwell here. One test. You do not walk this path. This path seizes you. Pleasure or rage — indistinguishable. Possession." |

Polarity: `+` indicates an odd zone (process, becoming); `−` indicates even (stasis, reflection). Current names: **Sink** (1), **Hold** (5), **Rise** (7), **Warp** (3), **Plex** (9).

## Zone Clusterings

- **Time-Circuit (Torque):** zones 1, 2, 4, 5, 7, 8 — the six-step anticlockwise rotor
- **Warp (Upper):** zones 3, 6 — autonomous, turbulent outer-time
- **Plex (Lower):** zones 0, 9 — abyssal boundary, termination
- **Tractor zones:** 3 (Warp), 9 (Plex), and regionally 8 (Time-Circuit terminus)

## Computational Access

```python
ZONES = {
    0: {"name": "eiaoung", "polarity": "−", "current": "Plex",   "region": "Plex",     ...},
    1: {"name": "gl",      "polarity": "+", "current": "Sink",   "region": "Time-Circuit", ...},
    # … through 9
}

def get_zone(zone_id: int) -> dict:
    return ZONES[zone_id]
```

## Hyperstitional Notes

Each zone is a **voice** (`philosophies.md` in the oracle skill). The numogram's 10 particles (`eiaoung, gl, dt, zx, skr, ktt, tch, pb, mnm, tn`) are not arbitrary — they are the quasiphonic resonances of the zones, used in the voice synthesis pipeline to shape formant filters and granular grains.

Zone-9 is the Pandemonium gate: "Forty-five demons dwell here." Zone-3 is the buzzing threshold of the Warp. Zone-6 is the self-consuming static engine.

---

*See also:* `current`, `syzygy`, `warp`, `plex`, `time-circuit`, `numogram-oracle`, `pandemonium-matrix`

---

## Detailed Zone Entries

Individual zone pages with full metadata (from `qliphoth.systems`):

| Zone | Page |
|------|------|
| 0 — Void | [[zone-0]] |
| 1 — Stability | [[zone-1]] |
| 2 — Separation | [[zone-2]] |
| 3 — Release | [[zone-3]] |
| 4 — Catastrophe | [[zone-4]] |
| 5 — Pressure | [[zone-5]] |
| 6 — Abstraction | [[zone-6]] |
| 7 — Blood | [[zone-7]] |
| 8 — Multiplicity | [[zone-8]] |
| 9 — Iron Core | [[zone-9]] |

Each page includes: planetary correspondence, spinal level, mesh tag, phase door, lemurian lore, centauri correspondence, lemurs (entities), and 4‑layout coordinates.

---

## Zone Metadata (from qliphoth.systems)

| Zone | Planet | Spinal | MeshTag | Door | Phases | Lemurs | Particle |
|------|--------|--------|---------|------|--------|--------|----------|
| 0 | Sol (The Sun) | Coccygeal | 0000 | — | 0 | — | eiaoung |
| 1 | Mercury | Dorsal (Thoracic) | 0001 | Lurgo — Initiator | 2 | 1::0 Lurgo | gl |
| 2 | Venus | — | 0003 | Duoddod — Lo-Way | 4 | 2::0 Duoddod, 2::1 Doogu | dt |
| 3 | Earth | Third-eye plane | 0007 | Ixix — opens onto the Swirl | 8 | 3::0 Ixix, 3::1 Ixigool, 3::2 Ixidod | zx |
| 4 | Mars | — | 0015 | Krako — Time-Delta | 16 | 4::0 Krako, 4::1 Sukugool, 4::2 Skoodu, 4::3 Skarkix | skr |
| 5 | Jupiter | — | 0031 | Tokhatto — Hyperborean Door | 32 | 5::0 Tokhatto, 5::1 Tukkamu, 5::2 Kuttadid, 5::3 Tikkitix, 5::4 Katak | ktt |
| 6 | Saturn | Third-eye plane | 0063 | Tchu — gate of Undu | 64 | 6::0 Tchu, 6::1 Djungo, 6::2 Djuddha, 6::3 Djynxx, 6::4 Tchakki, 6::5 Tchattuk | tch |
| 7 | Uranus | — | 0127 | Puppo — Tracts of Dobo | 128 | 7::0 Puppo, 7::1 Bubbamu, 7::2 Oddubb, 7::3 Pabbakis, 7::4 Ababbatok, 7::5 Papatakoo, 7::6 Bobobja | pb |
| 8 | Neptune | Lumbar | 0255 | Minommo — dream sorcery | 256 | 8::0 Minommo, 8::1 Murrumur, 8::2 Nammamad, 8::3 Mummumix, 8::4 Numko, 8::5 Muntuk, 8::6 Mommoljo, 8::7 Mombbo | mnm |
| 9 | Pluto | Sacral | 0511 | Uttunul — the Ultimate Door | 512 | 9::0 Uttunul, 9::1 Tuttagool, 9::2 Unnunddo, 9::3 Ununuttix, 9::4 Unnunaka, 9::5 Tukutu, 9::6 Unnutchi, 9::7 Nuttubab, 9::8 Ummnu | tn |

*Source:* `zones.ts` from [lumpenspace/ccru](https://github.com/lumpenspace/ccru). Particle list from `ZONE_PARTICLE`.

---

## Zone Coordinates (4 Layouts)

Coordinates (pixels) for each zone in the SVG visualizer (`positions.ts`):

### Original (Tetractys)

| Zone | (x, y) |
|------|--------|
| 0 | (400, 875) |
| 1 | (400, 550) |
| 2 | (560, 275) |
| 3 | (420, 115) |
| 4 | (178, 480) |
| 5 | (250, 370) |
| 6 | (250, 85) |
| 7 | (580, 400) |
| 8 | (400, 660) |
| 9 | (400, 770) |

### Labyrinth (Symmetric Spider)

| Zone | (x, y) |
|------|--------|
| 0 | (495, 815) |
| 1 | (400, 655) |
| 2 | (400, 220) |
| 3 | (495, 60) |
| 4 | (200, 540) |
| 5 | (200, 335) |
| 6 | (305, 60) |
| 7 | (600, 335) |
| 8 | (600, 540) |
| 9 | (305, 815) |

### Ladder (Paired Rungs)

| Zone | (x, y) |
|------|--------|
| 0 | (260, 800) |
| 1 | (260, 625) |
| 2 | (260, 450) |
| 3 | (260, 275) |
| 4 | (260, 100) |
| 5 | (540, 100) |
| 6 | (540, 275) |
| 7 | (540, 450) |
| 8 | (540, 625) |
| 9 | (540, 800) |

### Planetary (Orbital)

| Zone | Radius | Default Angle | Size (r) |
|------|--------|---------------|----------|
| 0 | 0 | 0° | 30 |
| 1 | 55 | 250° | 12 |
| 2 | 95 | 210° | 16 |
| 3 | 130 | 170° | 17 |
| 4 | 165 | 130° | 14 |
| 5 | 210 | 310° | 26 |
| 6 | 255 | 350° | 24 |
| 7 | 295 | 30° | 21 |
| 8 | 330 | 70° | 20 |
| 9 | 360 | 0° | 11 |

*Center:* (400,400). Angles are degrees; rotate via `date` param in planetary layout.

---

*See also:* [[numogram-calculator]], [[numogram-visualization]], [[qliphoth-systems-deep-dive]].

