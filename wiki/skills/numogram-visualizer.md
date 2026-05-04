---
title: Numogram Visualizer
created: 2026-05-04
updated: 2026-05-04
status: stub
category: skill
---

# Numogram Visualizer

Geometry‑backed SVG generation for Numogram diagrams. New skill `numogram-visualizer` (v0.1) produces canonical assets from code rather than hand‑editing.

## Archetypes

### Pandemonium Matrix
`numogram-visualizer/scripts/archetypes/pandemonium_matrix.py`

Generates the 45‑tile lower‑triangle with classification‑driven coloring:
- **Chrono** tiles use row zone's TC‑set color (α 0.35)
- **Amphi** tiles use violet (#a78bfa, α 0.25)
- **Xeno** tiles use slate (#475569, α 0.5)
- **Syzygy** tiles use amber fill + cyan dashed stroke + directional triangle

Uses doomcrypt‑decadence‑console‑demons.json as metadata source.

### Chord Pentagram (v2)
`numogram-visualizer/scripts/archetypes/chord_pentagram.py`

Recreates the 10‑zone star layout from `chord-pentagram-v2.svg`:
- Fixed zone coordinates (extracted from v2 asset)
- Outer ring (Z0,Z2,Z4,Z6,Z8) and inner valley ring (Z5‑9 at smaller radius)
- Pentagram outline + inner pentagon (cyan straight lines)
- 45 chords: syzygy chords curved via `quadPath`, others thin gray straight
- Zone labels and status bar

Supports dynamic `current_zone` highlighting and phase string.

### Zone Topology
`numogram-visualizer/scripts/archetypes/zone_topology.py`

Directed graph of the 10 zones with sovereign labels, node rectangles, and arrow edges labeled by gate names. Edges routed through simple straight lines; future `curveAway` integration planned.

## Technical Notes

- Standalone archetypes use **path‑based imports** to load `base.py` and `geometry_wrapper.py` from the same skill, avoiding Python package pitfalls from the hyphenated skill directory name.
- Base class `SVGDocument` provides dark theme background, grid pattern, JetBrains Mono font, and `render()` method.
- Geometry functions from `numogram-geometry`:
  - `syzTrianglePoints` – syzygy direction indicator on matrix tiles
  - `quadPath` – cubic Bezier chord arcs on pentagram
  - `midpoint` – label positioning helper
- All outputs are pure SVG (no external dependencies at render time).

## Usage Example

```bash
# Render the demo set
python -c \
  "from archetypes.pandemonium_matrix import render_pandemonium_matrix; \
   render_pandemonium_matrix('/tmp/matrix.svg')"
```

## Integration Points

- Feed **MIR feature vectors** → zone probabilities → highlight tile(s) in matrix (future)
- Sync with `numogram-oracle` outputs (AQ calculation → zone → pentagram current indicator)
- Embed in TouchDesigner via MCP: load generated SVGs as `TOP` sources

## References

- Original assets: `wiki/assets/chord-pentagram-v2.svg`, `pandemonium-matrix.svg`
- Geometry source: `lumpenspace/ccru` → `geometry.ts`
- Canonical data: `~/.hermes/obsidian/hermetic/raw/doomcrypt-decadence-console-demons.json`
