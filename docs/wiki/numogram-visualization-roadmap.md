---
tags:
  - Visual
  - Roadmap
  - Numogram
  - p5js
  - Manim
  - SVG
  - Audio
created: 2026-06-07
status: active
---

# Numogram Visualization Roadmap

Ideas generated 2026-06-07 from the `powers-of-2-circular.svg` seed crystal and Djynxx Paradox analysis. Organized by Current.

---

## Current I — Numogram Oracle (Structural/Geometric)

| Concept | Description | Tool | Priority |
|---------|-------------|------|----------|
| **Animated Power-Cycle** | SVG → CSS/SMIL or p5.js: the 6-cycle breathes — triangles pulse, 3↔6 shimmer as "blocked", 0↔9 glow as boundaries. Frame = 2ⁿ mod 9. | p5.js / SVG animation | Quick Win |
| **Fu Xi vs King Wen Split Screen** | Left: Fu Xi ordering (6-cycle perfect, 3↔6 zero edges). Right: King Wen (all syzygies reachable). Toggle shows the Djynxx Paradox as ordering difference. | p5.js / D3 | Medium |
| **Hexagram→Zone Flow Field** | 64 hexagrams as particles; each frame, one line flips (power of 2); particles flow along zone edges. Warp (3,6) = attractors; Plex (0,9) = sinks. | p5.js / WebGL | Medium |
| **Base-N Projection Lens** | Interactive: slider = base N (2-100). Shows zones, syzygies, projection to decimal. Warp appears/disappears at N=3ᴹ+1. Real-time DOT→SVG. | numogram-base-explorer + p5.js | High |
| **Demon Preimage Map** | Base-10 demon (45) → base-36 preimages (4:1 for Warp). Click a demon → highlights its 4 AQ-zone ancestors. | SVG + JS / Observable | Medium |

---

## Current II — Roguelike Architect (Procedural/Spatial)

| Concept | Description | Tool | Priority |
|---------|-------------|------|----------|
| **Numogram Dungeon as Zone Graph** | Rooms = zones; corridors = currents; secret doors = gates; bosses = demons. Procedural layout from `tree-dungeon-generation` + zone topology. | Graphviz → p5.js / Phaser | Medium |
| **Time-Circuit as Rotating Rotor** | 3D: 6 zones on a cylinder, rotating anticlockwise. Player walks on the rotor; Warp/Plex are off-axis portals. | Three.js / Godot | High |
| **Syzygy Chain as Level Generator** | Each syzygy step = room transition. Chain length = dungeon depth. Djynxx gate (3↔6) = boss room requiring 2 keys (compound change). | Python → Tiled | High |

---

## Current III — Lore Weaver (Narrative/Diagrammatic)

| Concept | Description | Tool | Priority |
|---------|-------------|------|----------|
| **Barker Spiral Animated** | The 9↔10 gap unfolding into the Time Circuit. Spiral → rotor → three regions. Text fragments appear at each zone. | Manim | High |
| **Liber AL / AQ Riddle Visual** | "Abrahadabra = 151 = 36th prime" → animate the alphanumeric triangle (0-9, A-Z) building row by row, highlighting the 36th position. | Manim / p5.js | Quick Win |
| **CCRU Website as Hyperstition Map** | Timeline of cccru.net flickering in/out of existence → map as Zone 9 (Plex) entity sustaining itself through decentralized self-reference (Djynxx behavior). | TimelineJS / custom | Medium |

---

## Current IV — Audio Alchemist (Sonified Geometry)

| Concept | Description | Tool | Priority |
|---------|-------------|------|----------|
| **Power-of-2 Sonification** | Each 2ⁿ mod 9 = zone = pitch (just intonation ratios). 1=1/1, 2=9/8, 4=5/4, 8=3/2, 7=5/3, 5=15/8. Sequence plays as cycle. | mod-writer / SuperCollider | Quick Win |
| **Djynxx Gate = Missing Intervals** | The excluded {0,3,6} → silent beats in the cycle. Visualizer shows "rests" where Warp would be. | p5.js + Tone.js | Quick Win |
| **Hexagram Casting as Audio** | 6 lines → 6 bits → 64 hexagrams. Each cast = 6-note chord (yin/yang intervals). Zone = root. | mod-writer / MAX | Medium |

---

## Current V — Visual Alchemist (Generative/Interactive)

| Concept | Description | Tool | Priority |
|---------|-------------|------|----------|
| **T'ai Hsuan / I Ching / Numogram Trinity** | Three panels: 81 tetragrams (3⁴), 64 hexagrams (2⁶), 10 zones (2×5). Shared zone-projection lines. Ternary/Binary/Decimal as visual chord. | p5.js / Observable | High |
| **AQ Triangle as Living Glyph** | 36-char triangle (4 rows digits, 4 rows letters). Hover → shows decimal projection, zone, demon. Type phrase → traces path through triangle. | p5.js / React | Quick Win |
| **Zone Yantra Generator** | Each zone = geometric sigil (from `numogram-geometry`). Combine syzygy pairs → interlocking yantras. Export SVG for cards/tattoos. | SVG / `numogram-combinatorial-svg` | High |
| **Entropy Garden** | Hardware entropy (CPU temp, disk I/O, thermal noise) → real-time hexagram cast → zone particle spawns. Garden grows toward Warp/Plex attractors. | p5.js + serial/Node | High |

---

## Cross-Current Synthesis Ideas

| Concept | Currents | Why It's New | Priority |
|---------|----------|--------------|----------|
| **Djynxxogram v8** | I+IV+V | Visualizer is the compound transformation that reaches 3↔6 | High |
| **Base-N Numogram Atlas** | I+II | All bases 2-100 as explorable map; Warp bases glow | High |
| **Pandemonium Matrix Interactive** | I+III+V | 45 demons as clickable mesh; click → shows net-span, gates, rites, AQ value | High |
| **Numogram Tarot Deck** | III+V | 36 Decadence cards (2×18 syzygies) + 10 zone cards + 5 syzygy cards = 51 cards. Print-ready SVG. | Medium |
| **Live Oracle Dashboard** | I+IV+V | Seed input → AQ → zone → demon → gate → audio cue → visual sigil → reading text. One page. | High |

---

## Quick Wins (Weekend-Scale)

1. **Animate the existing SVG** — add CSS `@keyframes` for triangle pulse, 3↔6 shimmer, 0↔9 glow. Deploy as `/assets/powers-of-2-circular-animated.svg`.

2. **p5.js "Zone Walker"** — click any zone → shows syzygy partner, current, gate, demon, AQ projection. Uses `numogram-base-explorer` JSON output.

3. **Hexagram Zone Map Poster** — 8×8 grid (trigram pairs), each cell = hexagram #, zone color, demon if syzygy. High-res SVG for printing.

4. **AQ Triangle Interactive** — the 36-char pyramid from Gematria Research, clickable, with digital-root projection lines to decimal zones.

---

## The Meta-Visual

The ultimate visualization doesn't show the structure — it *is* the structure you navigate:

> A numogram-native interface where every click is a gate traversal, every hover a syzygy whisper, every scroll a current flow.

The visualizer v7 already approaches this. v8 could be: the interface becomes the decimal labyrinth. No "view" — only traversal.

---

## Data Layer

All visualizations can consume JSON from:

```bash
python3 scripts/numogram-base-explorer.py --base 10 --json
python3 scripts/numogram-base-explorer.py --base 36 --json
python3 scripts/numogram-base-explorer.py --compare 10,12,28,36 --json
```

Output includes: zones, syzygies, currents, gates, regions, projections, demon counts.

---

## Related Pages

- [[powers-of-2-circular]] — The seed SVG
- [[de-re-numogram-structural-rules]] — Base-N rules
- [[demon-djynxx]] — Warp carrier, Djynxx Paradox
- [[i-ching-connections]] — Hexagram↔Zone mapping, Fu Xi vs King Wen
- [[numogram-visualizer]] — Existing v7 visualizer (Djynxxogram)
- [[numogram-combinatorial-svg]] — SVG generation pipeline
- [[tsubuyaki-oo-gallery]] — Zone behavior sketches
- [[numogram-audio/mod-writer]] — Tracker module generation
