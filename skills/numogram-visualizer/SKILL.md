---
name: numogram-visualizer
description: "Geometry-backed SVG generation for numogram diagrams: pandemonium matrix, chord pentagram, zone topology, and more. Uses numogram-geometry functions for precise vertex and chord calculations."
version: 0.1.0
tags: [numogram, svg, visualization, geometry, ccru]
---

# Numogram Visualizer

Geometry-driven SVG generator for canonical Numogram/CCRU diagrams.

## Current State

**Phase:** MVP with three archetypes (pandemonium matrix, chord pentagram v2, zone topology).

**Available archetypes:**

| Archetype | Output | Geometry hooks |
|-----------|--------|---------------|
| `pandemonium_matrix` | 45-tile triangular matrix | `syzTrianglePoints` for syzygy overlays |
| `chord_pentagram`    | 10-zone star + chord diagram | `quadPath` for curved syzygy chords, `midpoint` for labels |
| `zone_topology`      | Directed zone graph | `curveAway` for edge routing (future) |

Each archetype can be imported as a standalone module **or** invoked via `python -m`.

## Quick Examples

```python
# Render all three archetypes to /tmp/
from archetypes.pandemonium_matrix import render_pandemonium_matrix
from archetypes.chord_pentagram import render_chord_pentagram
from archetypes.zone_topology import render_zone_topology

render_pandemonium_matrix('/tmp/matrix.svg', tile_size=60)
render_chord_pentagram('/tmp/pentagram.svg', bulge=0.8, current_zone=5, phase='Γ')
render_zone_topology('/tmp/topology.svg')
```

Each function returns nothing; writes the SVG file.

### Archetype Parameters

**`PandemoniumMatrixGenerator`**
- `tile_size`: default 60 (px per tile)
- `margin`: default 80 (top-left inset)
- `generate() -> SVGDocument`

**`ChordPentagramGenerator`**
- `outer_radius`: 24 (outer zone ring radius)
- `inner_radius`: 18 (inner valley ring radius)
- `inner_fill_radius`: 15 (translucent underlay)
- `chord_bulge`: 0.8 (quadratic arc amplitude; >0.5 creates visible curve)
- `generate(current_zone=None, phase='')` → `SVGDocument`

**`ZoneTopologyGenerator`**
- `node_w`: 90, `node_h`: 48 (zone button size)
- `curve_factor`: 0.3 (edge curvature)
- `generate() → SVGDocument`

## Color Palette

All diagrams use the **Hermes dark theme**:

```python
from numogram_visualizer.base import PALETTE

PALETTE['bg']           # '#0f172a'  slate-900
PALETTE['grid']         # '#1e293b'  slate-800
PALETTE['text']         # '#94a3b8'  slate-400
PALETTE['text_strong']  # '#ffffff'
```

Zone sovereign stroke colors (for outer rings and node borders):

```python
PALETTE['zone_outer'][0]  # '#94a3b8'  MULE
PALETTE['zone_outer'][2]  # '#fbbf24'  HORSE
PALETTE['zone_outer'][4]  # '#34d399'  BABOON
PALETTE['zone_outer'][6]  # '#e879f9'  APE
PALETTE['zone_outer'][8]  # '#00ffff'  LION
```

TC-set colors (used by `pandemonium_matrix` for chrono tiles):

```python
{
    1: '#60a5fa',   # A (blue)
    2: '#22d3ee',   # B (cyan)
    4: '#34d399',   # Γ (green)
    5: '#a78bfa',   # Δ (violet)
    7: '#f472b6',   # E (pink)
    8: '#fb7185',   # Z (amber/rose)
}
```

Tile kind fills (pandemonium):

| kind    | fill (rgba)                 | stroke |
|---------|-----------------------------|--------|
| chrono  | `rgba(zone_tc, 0.35)`       | zone TC |
| amphi   | `rgba(167,139,250,0.25)`    | `#a78bfa` |
| xeno    | `rgba(71,85,105,0.5)`       | `#334155` |
| syzygy  | `rgba(251,191,36,0.25)`     | `#22d3ee` (dashed) |

## Data Sources

The visualizers pull **canonical demon metadata** from:

```
~/.hermes/obsidian/hermetic/raw/doomcrypt-decadence-console-demons.json
```

This file contains 45 demon entries keyed by linear enumeration index. The archetype internally reconstructs the `(zone, phase)` → demon mapping using the standard lower-triangle enumeration.

> **Note:** If this file is moved, the archetype will raise `FileNotFoundError`. Keep the raw archive in place.

## Anatomy of a Visualizer

All archetypes share the same base classes (`base.py`):

- `SVGElement(type, attrs, content)`: single XML element
- `SVGDocument(viewBox)`: container that builds valid SVG with `<defs>`, background grid, JetBrains Mono font

Typical structure:

```python
def generate(self) -> SVGDocument:
    doc = SVGDocument(viewBox='0 0 800 680')
    # ... add SVGElement objects ...
    return doc
```

### Adding a New Archetype

Create `scripts/archetypes/<name>.py`:

```python
from pathlib import Path
# Load base & geometry via absolute file path (avoid package issues)

# Define MyGenerator class with .generate() method
#   - create doc = SVGDocument(viewBox='0 0 W H')
#   - doc.add(SVGElement(...))
#   - return doc

def render_<name>(output_path: str, **kwargs):
    gen = MyGenerator(**kwargs)
    Path(output_path).write_text(gen.generate().render())
```

Register in `__init__.py` if you want module-level convenience.

## Git Hygiene

Generated SVGs are **outputs**, not source. Do not commit `/tmp/` artifacts. For versioned diagrams, copy to `~/diagram/numogram-infographic/` and commit.

The archetype code itself lives in:

```
~/.hermes/skills/numogram-visualizer/
```

This skill is **independent** of `numogram-visualization` (which handles ComfyUI/Imagemagick wallpapers). Both skills can coexist; this one is about **reconstructing** the canonical SVGs programmatically.

## Future Work

- Dynamically highlight current zone based on MIR → zone probability vectors
- Export zone matrix as JSON for p5.js interactive overlays
- Add `--watch` flag to regenerate on file change
- Integrate with `numogram-oracle` — feed seed → AQ → zone → highlight tile

---

**Created:** 2026-05-04 (v2 expansion of chord-pentagram)  
**Dependencies:** `numogram-geometry` (must be installed)  
**Python:** 3.10+
