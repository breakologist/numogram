---
title: SVG & Interactive Assets Catalog
created: 2026-04-28
updated: 2026-05-09
tags: [assets, diagrams, svg, catalog, interactive]
---

# SVG & Interactive Assets Catalog

Directory: `wiki/assets/`. Reference in wiki pages via relative paths: `assets/<filename>`.

## Inventory

| File | Purpose |
|------|---------|
| `barker-spiral.svg` | Barker Spiral diagram (Atlantean sum-to-10 / Lemurian sum-to-9) |
| `chord-pentagram-v2.svg` | Numogram Star — outer 5 at star points, inner 5 at valleys, syzygy spokes (cyan), decadence cross (amber), C(10,2)=45 |
| `chord-pentagram.svg` | Earlier version of the Numogram Star |
| `hexagram-zone-mapping.svg` | All 64 I Ching hexagrams mapped to zones via (hex#-1) mod 9 — 7 hex/zone Z1-9, Qian #1 alone in Z0 |
| `numogram-zone-topology.svg` | Decimal Labyrinth — 10 zones, 3 regions (Plex/Time-Circuit/Warp), 5 syzygies, 5 currents, anticlockwise traversal 1→8→2→7→5→4→1 |
| `pandemonium-matrix.svg` | Full 45-demon matrix — 15 chronodemons (cyan), 24 amphidemons (amber), 6 xenodemons (magenta), 5 ★ syzygetic carriers |
| `powers-of-2-circular.svg` | 6-cycle: powers of 2 (1→2→4→8→7→5) forward, powers of 5 reverse — twin serpents, Z0 above, Z9 below |
| `roguelike-dungeon-architecture.svg` | Full UML — DungeonGenerator, TreeBuilder, ZoneMapper, Room/Corridor/Gate, Crawler/Demon, GameState/Hyperstition/Ability/CultGarden |
| `triangular-matrix.svg` | C(10,2)=45 template — triangular matrix with highlighted diagonal, blank for population |
| `trigram-pair-matrix.svg` | 8×8 = 64 hexagrams matrix — upper trigram × lower trigram, color-coded by zone, diagonal bands of constant zone |
| `changing-lines-network.svg` | I Ching changing lines network diagram |
| `chord-diagram.svg` | Earlier chord diagram |
| `circular-flow-subway.svg` | Circular flow subway-style diagram |
| `entropy-casting-flow.svg` | Entropy casting flow diagram |
| `hub-spoke-cyberpunk.svg` | Hub-and-spoke cyberpunk-style diagram |
| `king-wen-spiral.svg` | King Wen spiral arrangement |
| `periodic-table-schematic.svg` | Periodic table schematic |
| `tetragram-three-states.svg` | Tetragram three-states diagram |
| `trigram-numogram.svg` | Trigram-to-numogram mapping |
| `endian-rite.html` | **Interactive p5.js** — Rumsfeld Tetrad quadrants, endian flip animation, dungeon tree growth, Diamond Sutra cycle. See [[endian-rite-visualization]] |
| `bs.jpg` | Barker Spiral original — hand-drawn source (CCRU interview, 1998) |
| `nb.png` | Barker Spiral original — enhanced digital variant (CCRU interview) |

## Interactive Assets

| File | Type | Description |
|------|------|-------------|
| `endian-rite.html` | p5.js visualization | Animated Rumsfeld Tetrad with endian flip, dungeon tree, sutra cycle. [[endian-rite-visualization]] |
| `cult-garden-live.html` | p5.js dashboard | Live cult garden telemetry viewer with zone skins. (in `~/numogame/`) |

## Usage

- SVGs: vector-based, scale without quality loss
- HTML: open in browser for animated/interactive experience
- Source editing: modify original in `~/diagram/` then copy here
- See also: [[numogram-visualization]] for generation pipeline

## Source Directories

- `~/diagram/` — master authoring workspace
- `~/numogram/visualizer/` — auto-generated visualizer output
- `~/.hermes/obsidian/hermetic/raw/` — scanned source diagrams
