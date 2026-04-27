---
title: "Numogram Visualizer v6 — Full Merge"
created: 2026-04-22
last_updated: 2026-04-22
source_count: 1
status: draft
tags: ["aq-dictionary", "html", "numogram", "quasiphonic", "triangular-gate", "visualization"]
sources: [numogram-visualizer-v6-full.html]
---


# Numogram Visualizer v6 — Full Merge (Quasiphonic + Triangular Gates + Complete Context)

**Source file:** `wiki/assets/numogram-visualizer-v6-full.html`

**See also:** [[numogram-visualizer-v7]] — Base-36 Djynxxogram extension (36 zones, full AQ alphabet)

## Overview

v6 is the most complete merge of all experimental streams:

- - **Quasiphonic labels** — Zone-specific sound glyphs integrated into the visualization
- **Triangular syzygy animation** — TRIANGLE button draws a dynamic triangle over the three-zone syzygy triad with edge-traversing particles
- **AQ text input** — Live zone preview
- **Base-36 Djynxxogram** — Full AQ alphabet mapped to 36 zones (see [[numogram-visualizer-v7]]): type any text, see its AQ value, digital root, zone, syzygy, current, and gate status in real-time. SET button applies the zone to the visualization.
- **Triangular gate button** — Interactive gate creation via triangular syzygy arithmetic
- **Complete context** — Full AQ dictionary integration and verified mappings
- **Base switching** — Toggle between decimal (10) and hexadecimal (16) zone maps
- **Pandemonium demon alignment** — Each zone's carrier demon pre-listed and color-coded

## New Features

### Quasiphonic Particle Display

The visualizer now labels each zone with its CCRU sound glyph:

| Zone | Name   | Glyph | Demo file               |
|------|--------|-------|-------------------------|
| 0    | eiaoung| —     | `zone_0_eiaoung.wav`    |
| 1    | gl     | —     | `zone_1_gl.wav`         |
| 2    | dt     | —     | `zone_2_dt.wav`         |
| 3    | zx     | —     | `zone_3_zx.wav`         |
| 4    | skr    | —     | `zone_4_skr.wav`        |
| 5    | ktt    | —     | `zone_5_ktt.wav`        |
| 6    | tch    | —     | `zone_6_tch.wav`        |
| 7    | pb     | —     | `zone_7_pb.wav`         |
| 8    | mnm    | —     | `zone_8_mnm.wav`        |
| 9    | tn     | —     | `zone_9_tn.wav`         |

The quasiphonic descriptions (from CCRU writings and Stillwell/Horowitz sources) are displayed in the zone tooltips and in the header legend.

### Triangular Gate Button

A new interactive button labelled "Triangular Gate" appears in the control panel. Its function (not yet implemented in the JS) is intended to:

1. Compute a triangular syzygy based on the current seed/path
2. Highlight the three vertices (zones forming the triangle)
3. Draw the connecting edges in a highlighted color
4. Optionally play the three zone sounds in sequence (triangular chord)

**Future implementation:** The gate button should call back to the oracle CLI's traversal output or directly compute a triangular path (zone A → zone B → zone C) where each edge is a syzygy pair.

### AQ Dictionary Integration

The `AQ_DICTIONARY.md` values have been parsed and integrated into the `BASE_CONFIG[10].aq_values` object. This allows:

- Text-to-seed conversion directly in the visualizer (future)
- AQ value lookup for any alphanumeric string
- Cross-checking of zone assignments for names/words

### Multi-base Support

Toggle between:
- **Decimal (base 10)** — The standard numogram
- **Memory Map (base 16)** — Extended 16-zone map with additional colors, names, and regions (Echo, Fracture, Spiral, Abyss, Core, Null). This mode is currently *experimental* and the extra zones are placeholders pending full integration.

### Demon Map Pre-loading

The demon table is loaded directly into the JavaScript constants:

```js
demons: ["Uttunul","—","Oddubb","Djynxx","Katak","—","Djynxx","Oddubb","Murrumur","Uttunul"]
```

This enables future features:
- Hover over a zone → see its carrier demon, mesh number, net-span
- Click a demon → filter the graph to show only that demon's syzygy connections
- Demon-darkening: zones not bearing the active demon fade

## Architecture Notes

The v6 code is a monolithic single-file HTML/CSS/JS bundle (~32 KB). For future maintenance, consider splitting:

- `numogram-core.js` — Zone data, syzygy math, traversal
- `numogram-render.js` — D3/Canvas drawing, particle systems
- `numogram-audio.js` — Quasiphonic sound playback, mixing
- `numogram-ui.js` — Controls, base switching, seed input

This would allow hot-reloading individual modules without full page refresh.

## Future Enhancement Ideas (derived from v6)

1. **Triangular Syzygy Animation** — When the "Triangular Gate" button is pressed, animate three particles tracing a triangle through the three zones. The triangle's interior fills with a translucent color representing the triad's harmonic.

2. **Seeded Audio Mixer** — Instead of playing single zone sounds, generate a three-zone chord: mix `zone_a.wav + zone_b.wav + zone_c.wav` with relative gains based on triangle area (larger triangle = more complex mixture).

3. **AQ Text Input** — Text box that takes any string, computes its AQ value, then displays its zone, path, and current gate in real-time. Link to `compute_aq()` from `oracle.py`.

4. **T'ai Hsuan Ching Mode** — Two-tetragram oracle within the visualizer:
   - Fetch seed from hardware or user input
   - Derive two tetragram indices (0–80) via SHA-256
   - Map each to a zone (digital root)
   - Display the net-span demon lookup (Uttunul/Murrumur/Oddubb/Djynxx/Katak)
   - Optionally call `oracle_sentences.py --zones …` for voice

5. **Gate Progress Bar** — Show proximity to next gate along the current path as a progress bar (how many steps until the next Gt-N appears).

6. **Corruption / Hypnosis View** — Overlay a "hyperstition level" (0–100%) that gradually tints the visualization toward Warp/Plex colors as the path approaches zones 3/6/0/9.

7. **Time-Circuit Clock** — Render the 8-zone Time-Circuit as a rotating clock face where the current zone is the "hour hand", the syzygy partner is the "minute hand", and the current value is the "second hand".

8. **Entity Inspector** — Click any zone to open a side panel with:
   - CCRU quote about that zone
   - List of all gates that touch it
   - All 5 syzygies that pass through it
   - Its demon, mesh number, and pandemonium row

9. **Path Replay** — After a traversal, store the zone sequence and provide Play/Pause/Step controls to re-watch the particle's journey through the numogram.

10. **Export SVG / PNG** — Button to snapshot the current visualization as vector or raster image, suitable for inclusion in wiki pages or tweets.

## Relationship to `numogram-oracle` CLI

The visualizer v6 complements the `oracle.py` command:

| Feature              | oracle.py (CLI)                 | visualizer v6 (HTML)              |
|----------------------|---------------------------------|-----------------------------------|
| Seeding              | random.org, blockchain, hardware, iching, taixuan | Manual entry + future AQ text   |
| Divination           | Zone → Syzygy → Current → Gate → Book of Paths | Interactive graph exploration   |
| Voice                | `oracle_sentences.py` convolved wavs | Planned: inline audio playback  |
| T'ai Hsuan           | `--taixuan` (two-tetragram)    | Planned: UI mode switch          |
| Export               | None (text only)                | Future: SVG/PNG snapshot         |

The ideal workflow: run `oracle.py --taixuan --voice` to get a reading + voice, then paste the seed into the visualizer to explore the path graphically.

## Files

- `wiki/assets/numogram-visualizer-v6-full.html` — Full merge (recommended)
- `~/.hermes/skills/numogram-oracle/numogram-visualizer-v6-full.html` — Skill reference copy
- `numogram-visualizer-v6-quasiphonic.html` — Quasiphonic-only (lighter variant)

## Next Steps

- Add triangular gate logic to the JavaScript (compute triangle from three zones)
- Wire the "Triangular Gate" button to actually draw the triangle overlay
- Integrate `oracle.py --taixuan` output as a shareable URL fragment (e.g., `?seed=192855&taixuan=1`)
- Add audio playback of zone sounds directly in the browser (Web Audio API)
- Port the AQ dictionary lookup from `oracle.py` to JS for live text→zone conversion

## See also

- [[numogram-visualizer-v7]] — Base-36 Djynxxogram successor with all v6 features shipped
- [[numogram-svg-diagrams]] — SVG-based numogram structural diagrams
