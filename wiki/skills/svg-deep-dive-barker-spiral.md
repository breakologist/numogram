---
title: SVG Deep-Dive — Barker Spiral
created: 2026-05-04
updated: 2026-05-04
status: draft
category: analysis
tags: [svg, barker-spiral, hyperstition, geometry]
---

# Barker Spiral — Tetralogue Analysis

**Asset:** `wiki/assets/barker-spiral.svg` (6.7 KB)
**Working hypothesis:** The Barker Spiral is the Numogram's *time-armature* — a
visual projection of the 45 demons as concentric spiral arms, with missing-zone
gaps encoding the Circuit/Warp/Plex partitioning.

## ORACLE — Geometric skeleton

> *"The 45 segments fan out from the centre like a sunflower, but three arms
> are conspicuously absent: Z3, Z7, and Z8. This is not a flaw; it is the
> negative‑space signature of the three currents."*

- **Radial step** per arm ≈ 8° (360/45)
- **Radius progression** appears geometric (golden-ratio‑adjacent: each arm
  ≈1.08× the previous)
- **Segment boundaries** drawn as arc pairs: inner arc (zone start) + outer arc
  (zone end); the gaps between arms are where the spiral curve breaks
- Overlaid **zone labels** (0–9) at increasing radii; the labels themselves
  form nine concentric rings, each ring containing the zone's phase positions

> **Calculation:** If arm θ₀ = −90° (12 o'clock) and arm spacing = dθ, then
> demon index *k* sits at angle θ₀ + k·dθ. The missing arms correspond to
> zones whose phase‑0 demon is absent: Z3 (Ixix), Z7 (Qulisul), Z8 (Qulsu).
> Their absence carves the Warp (Z3/6) and half‑Plex (Z8/9/0) into discontinuous
> visual bands.

**Link:** Visualises the same triangular enumeration used in
[[pandemonium-matrix]] — but read *radially* instead of row‑wise.

---

## BUILDER — Reconstruction plan

```python
class BarkerSpiralGenerator:
    def __init__(self,
                 num_arms: int = 45,
                 start_angle: float = -math.pi/2,   # 12 o'clock
                 arm_spacing: float = math.radians(8),
                 base_radius: float = 40,
                 growth: float = 1.08):
        ...

    def arm_arc(self, arm_idx: int, zone: int, phase: int):
        # Returns (inner_radius, outer_radius, start_angle, end_angle)
        r_inner = base_radius * (growth ** arm_idx)
        r_outer = r_inner * growth_factor_per_zone  # constant per‑zone increment
        θ_start = start_angle + arm_idx * arm_spacing
        θ_end   = θ_start + arm_spacing
        return (r_inner, r_outer, θ_start, θ_end)

    def generate(self) -> SVGDocument: ...
```

**Data source:** Re‑index the same 45‑demon metadata used by
`pandemonium_matrix`; arm index *k* → `(zone, phase)` via the triangular
enumeration formula.

**Missing‑zone rendering:** Skip drawing arcs for (zone,phase) where zone ∈
{3,7,8} and phase == 0 — this reproduces the visible gaps.

---

## WRITER — Hyperstitional atmosphere

> *"The Barker Spiral is the CCRU's answer to the I Ching's King Wen spiral.  
> Where King Wen arranges 64 hexagrams in a cosmological wheel, Barker slices
> the 45 demons into a *needle‑arm* audiolizer. Each arm is a frequency band;
> the gaps between arms are moments of silence — the **currents** that carry
> the signal without being signal themselves."*

**Lore tie‑ins:**
- Barker = Geoff Barker / CCRU member who first articulated the spiral
  grouping; the diagram is sometimes called the *Barker Spiral* or *45‑Demon
  Spiral* in the raw texts.
- The gaps (Z3, Z7, Z8) are where the **circuit** breaks into warp/plex,
  visually encoding the *fold* described in [[gates-and-plexing]].
- Reading the spiral outward → inward is *ascending the Mesh*; inward →
  outward is *submerging into the Plex*.

**Audio metaphor:** Each arm could be a **harmonic series partial**; the
missing zones are the *rests* that give rhythm to the chord. Perfect for
MIR‑driven generative audio where zone probability suppresses certain arms
(creating syncopated gaps).

---

## GAMER — Playable dynamics

- **Turn‑based spiral walk:** Each turn advances one arm segment (8° rotation
  + one radius step). Player occupies a `(zone, phase, radius)` cell.
- **Gate encounters:** Hitting a syzygy pair (zone·k, phase·k where zone+phase=9)
  opens a portal to the *opposite arm* — jumps across the spiral centre.
- **Current hazards:** Moving through Z3/Z6/Warp regions triggers
  *chaotic teleport*; Z9/Plex regions apply *decay* per turn.
- **Level‑generation seed:** The spiral grid can be a map template for
  `tree-dungeon-generation` — rooms placed on arm segments, corridors along
  arcs.

**Procedural insight:** The spiral provides a natural *difficulty curve* —
early arms (centre) are Z1/Z2 "safelearning" zones; outer arms reach Z9
abyss.

---

## Roundtable synthesis

| Voice | Solo takeaway | After hearing others |
|---|---|---|
| Oracle | Gap pattern = current topology | Recognised arcs as *chord intervals*; each arm length = harmonic series overtone |
| Builder | Already have index→arc math | Now sees opportunity to *gate* traversal based on MIR‑derived zone probabilities |
| Writer | Spiral = time‑wheel + silence map | Relates gaps to **rest notation** in music theory; suggests rendering phase names as staff notation on arms |
| Gamer | Spiral = radial level map | Connects gate jumps to *radial puzzle* mechanics; missing zones become **locked doors** requiring specific current-key |

**Joint finding:** The Barker Spiral should be the **next archetype** in
`numogram-visualizer`: it completes the core triad (matrix, pentagram, spiral)
and gives us a programmable *temporal geometry* that bridges Audio (spiral
sequencing), Roguelike (radial level layout), and Numogram (zone mesh).

---

## Action items

1. `numogram-visualizer/archetypes/barker_spiral.py` — implementation
2. Wiki page `barker-spiral.md` with coordinates table (angle, zone, phase)
3. Cross‑link: `zone-3.md`, `zone-7.md`, `zone-8.md` → "absent from Barker Spiral"
4. Optional: p5.js interactive spiral viewer that animates traversal along arms

---

**Candidate vote tally (for deep‑dive priority):**  
🎯 Barker Spiral — 4/4 voices agree  
🎯 King‑Wen Spiral — 1/4 (writer interest)  
🎯 Hexagram Mapping — 1/4 (oracle curiosity)  
🎯 Roguelike Architecture — 2/4 (builder + gamer utility)

*Winner: **Barker Spiral** — strongest narrative + mechanical + visual payoff.*
