---
title: SVG Asset Inventory
created: 2026-05-04
updated: 2026-05-04
status: stub
category: reference
tags: [assets, svg, geometry, hyperstition]
---

# SVG Asset Inventory (19 canonical diagrams)

> **Context:** All assets live in `wiki/assets/`. Generated/derived programmatic
> counterparts live in `skills/numogram-visualizer/`.

## Quick reference table

| File | Size | Category | Key geometrical features |
|---|---|---|---|
| [chord-pentagram-v2.svg](assets/chord-pentagram-v2.svg) | 11.4 KB | **Core** | 10-zone star: outer ring (Z0,Z2,Z4,Z6,Z8) radius 240px; inner ring (Z5-Z9) radius 180px; 45 syzygy chords use `quadPath` (bulge 0.7–0.8); cyan pentagram + orange dashed syzygy lines |
| [chord-pentagram.svg](assets/chord-pentagram.svg) | 11.9 KB | **Core** | Earlier iteration; slightly different radial proportions |
| chord-diagram.svg | 10.0 KB | Core | Minimal 10-node circular layout; clean chord skeleton |
| pandemonium-matrix.svg | 15.9 KB | **Core** | Lower-triangle 45-tile grid; TC-set tile colours (blue/cyan/green/violet/pink/amber); syzygy tiles amber+cyan dashed; tile size ~60px, margin ~80px |
| numogram-zone-topology.svg | 11.3 KB | Core | Directed zone-graph; sovereign names + gate labels; straight arrow edges |
| triangular-matrix.svg | 18.4 KB | Geometry | Triangular array scaffolding (vector lines only) |
| trigram-numogram.svg | 10.4 KB | Esoteric | 3-bit (8-trigram) numogram extension |
| trigram-pair-matrix.svg | 24.7 KB | Esoteric | 64-cell matrix (8×8 trigram pairs) |
| barker-spiral.svg | 6.7 KB | Esoteric | 45-arm spiral (zones 0–9 placed on logarithmic-ish spiral); missing-zone gaps visible |
| king-wen-spiral.svg | 27.0 KB | **Esoteric** | 64-hexagram spiral (I-Ching); prime candidate for `king_wen_spiral` archetype |
| hexagram-zone-mapping.svg | 63.2 KB | Esoteric | Hexagram lattice laid across zones; potential hexagram‑augmented oracle |
| entropy-casting-flow.svg | 6.1 KB | Process | Entropy flow diagram; matches `Entropic Casting` skill structure |
| changing-lines-network.svg | 40.0 KB | Process | I-Ching line-change network; high-connectivity graph; MIR correlation canvas |
| periodic-table-schematic.svg | 12.7 KB | Audio | Periodic table style classification; synth‑patch taxonomy template |
| powers-of-2-circular.svg | 8.0 KB | Audio | Powers-of-two circular dial; bit-depth/bit-rate visual aid; rhythmic subdivision dial |
| roguelike-dungeon-architecture.svg | 19.2 KB | **Roguelike** | Brogue-style room accretion + machines; maps to `tree-dungeon-generation` |
| hub-spoke-cyberpunk.svg | 10.6 KB | Roguelike | Hub-room + spoke corridors; ant-farm/skill-tree layout |
| circular-flow-subway.svg | 10.3 KB | Roguelike | Loop circulation (metro map); audio bus routing / spell-cycle viz |

## Geometry lineage

All core diagrams are **reverse‑engineered** into `skills/numogram-visualizer/`
using functions from `skills/numogram-geometry/`:

| Geometry function | Used in | Purpose |
|---|---|---|
| `syzTrianglePoints` | pandemonium_matrix | Syzygy-direction triangle overlay on ZP tiles |
| `quadPath` | chord_pentagram | Curved syzygy chords (cubic Bézier) |
| `midpoint` | chord_pentagram | Phase/Greek-letter label positioning |
| `curveAway` | zone_topology *(planned)* | Curved arrow edge routing |

> **ORACLE:** These functions are not mere helpers — they encode the *harmonic
> skeleton* of the numogram. The pentagram's `quadPath` is identical to the
> curve used when mapping **chord qualities** (major/minor/augmented/diminished)
> onto syzygy arcs. The triangle marker from `syzTrianglePoints` points along
> the **chrono vector** — the direction of time‑flow through the current.

## Cross‑link map

- **Zone pages** (`zone-*.md`) → link to `chord-pentagram-v2.svg` for spatial layout
- **Gate index** (`gate-index.md`) → references `numogram-zone-topology.svg` for sovereignty edges
- **TC‑set** (`tc-set.md`) → uses `pandemonium-matrix.svg` colour key
- **Syzygy** (`syzygy.md`) → chords in `chord-pentagram.svg` are visual proof of the 45 pairs
- **Audio current** (`currents/audio-current.md`) → `powers-of-2-circular.svg` as rhythmic subdivision diagram
- **Roguelike current** (`currents/roguelike-current.md`) → `roguelike-dungeon-architecture.svg` for procedural room grammar

## Archetype status (in `numogram-visualizer/`)

| Archetype | Source asset | Recreation fidelity | Notes |
|---|---|---|---|
| `pandemonium_matrix` | pandemonium-matrix.svg | 100 % | Algorithmic TC‑set + amphi + xeno + syzygy styling; doomcrypt metadata names embedded |
| `chord_pentagram` | chord-pentagram-v2.svg | 100 % | Exact zone coordinates; `quadPath` bulge 0.7–0.8; dynamic `current_zone` highlighting |
| `zone_topology` | numogram-zone-topology.svg | 95 % | Straight edges; `curveAway` integration pending |

## Remaining 16 assets — next‑archetype candidates

| Asset | Priority | Geometry requirements |
|---|---|---|
| `barker-spiral.svg` | HIGH | `loopPath` (logarithmic‑ish spiral); zone placement on arm indices; missing‑zone gap arcs |
| `king-wen-spiral.svg` | HIGH | `loopPath` with 64 hexagram glyphs; spiral pitch consistent with Barker |
| `hexagram-zone-mapping.svg` | MEDIUM | Hexagonal grid layout; zone‑wise colour blocks per hexagram (6 lines × 3 states) |
| `changing-lines-network.svg` | MEDIUM | Force‑directed or radial network; curvy edges (reuse `curveAway`) |
| `roguelike-dungeon-architecture.svg` | MEDIUM | Room rectangles generated by tree‑dungeon; corridor polylines; machine overlay |
| `hub-spoke-cyberpunk.svg` | LOW | Hub circle, radial spokes; could reuse pentagram inner‑ring coords |
| `circular-flow-subway.svg` | LOW | Loop lines with station markers; re‑use `circularArc` helper |
| `entropy-casting-flow.svg` | LOW | Simple Bézier flow; matches entropy visualisations |
| `periodic-table-schematic.svg` | LOW | Grid layout; cell borders; could double as waveform taxonomy |
| `powers-of-2-circular.svg` | LOW | Circular arcs + numeric labels; trivial to regenerate |

---

**See also:**
- [[numogram-visualizer|Numogram Visualizer skill]] — code + archetype API
- [[canonical-numogram-diagrams]] — curated gallery of hand‑drawn diagrams (external sources)
