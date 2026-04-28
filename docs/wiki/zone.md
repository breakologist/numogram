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
