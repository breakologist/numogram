---
title: heerich.js — Voxel-to-SVG Geometry Engine
tags:
  - heerich
  - SVG
  - Voxel
  - Geometry
  - Visualization
  - Tooling
  - Reference
---

# heerich.js — Voxel-to-SVG Geometry Engine

> Source: [https://meodai.github.io/heerich/](https://meodai.github.io/heerich/)
> Version: 0.14.0
> License: MIT (inferred)

---

## What It Is

heerich.js is a minimalist JavaScript engine that constructs **3D voxel compositions** and renders them to **pristine SVG**. It projects complex spatial arrangements into resolution-independent vector output — infinitely scalable, DOM-native, stylable via CSS.

The visual language is inspired by **Erwin Heerich** (1922–2004), a German sculptor known for geometric rigour, stacked topologies, deliberate subtractions, and the tension between solid mass and absolute void.

---

## Core Capabilities

### Primitives
- **Box** — rectangular volume by position + size, or centered via `center` + `size`
- **Sphere** — rounded volume via `center` + `radius`
- **Line** — continuous voxelized path between `from`/`to`, with `radius` and `shape` (rounded/square joints)
- **Custom (fill)** — arbitrary geometry via a `test(x, y, z)` evaluation function over `bounds`

### Boolean Operations
- `applyGeometry()` — adds voxels
- `removeGeometry()` — subtracts voxels (same parameters)

Combining these allows: arched doorways (box + sphere subtraction), domed chambers, negative-space corridors, lattice structures.

### Camera Projections
- **Oblique** (default) — traditional isometric-adjacent
- **Perspective** — vanishing-point depth
- **Orthographic** — flat projection
- **Isometric** — equal-angle

Each configurable via `angle`, `distance`, `camY`.

### SVG Output
- `heerich.toSVG({ padding: N })` — returns SVG string, auto-centered
- `heerich.getBounds()` — raw bounding box for custom positioning
- Dirty-flag caching for efficient rapid structural changes

---

## Relevance to the Numogram Project

### 1. Zone Architecture Visualization
Numogram zones can be rendered as voxel chambers — Zone‑0 as a perfect empty cube, Zone‑5 as a tormented lattice, Zone‑9 as an open-frame structure. heerich's boolean operations make this trivial: start with a box, subtract spheres to create gate-arches.

### 2. Syzygy Lattice Diagrams
Triangular syzygies can be rendered as 3D voxel paths — three zones connected by stepped corridors, with gate-thresholds as subtractive arches.

### 3. Roguelike Dungeon Maps
Procedurally generated rooms (from `tree-dungeon-generation`) can be translated to heerich voxels for SVG export — resolution-independent maps for printing, embedding, or documentation.

### 4. Decimal Labyrinth as Isometric SVG
The 10-zone Numogram as an isometric voxel sculpture — each zone a chamber at a different height, connected by stair-like currents and gate-arch bridges.

### 5. Integration with p5.js Visualizers
heerich SVGs can be loaded as textures or overlaid elements in p5.js interactive sketches — static architecture supporting dynamic particles/currents.

---

## Quick Start

```javascript
import { Heerich } from './src/heerich.js'

const h = new Heerich({
  camera: { type: 'oblique', angle: 315, distance: 25 },
  style: { fill: '#2a2a2a', stroke: '#666', strokeWidth: 0.5 },
  gap: 0.05
})

// Create a zone chamber
h.applyGeometry({
  type: 'box',
  center: [5, 2, 5],
  size: [10, 4, 10]
})

// Carve a gate-arch
h.removeGeometry({
  type: 'sphere',
  center: [5, 1, 10],
  radius: 2
})

// Export to SVG
document.body.innerHTML = h.toSVG({ padding: 30 })
```

---

## Related Pages
- [[numogram-visualization]] — SVG diagram pipeline
- [[numogram-svg-diagrams]] — existing SVG geometry
- [[InterestingSites.md]] — Source link with description
