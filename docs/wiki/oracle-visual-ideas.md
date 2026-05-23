---
title: Oracle Visual Ideas
created: 2026-05-23
status: draft
tags:
  - oracle
  - visual
  - p5js
  - pixel-art
  - manim
  - ascii
  - svg
  - ideas
category: visual
---

# Oracle Visual Ideas

> *"Not a plan. A constellation. These are the ideas that pulled hardest during the oracle visual survey — set down here so we can return to them when the current is right."*
>
> Cross-linked from: [[skills-to-explore]] (pixel-art, p5js, ascii-video combos), [[barker-spiral-v2-exhibition]] (tetralogue visual forms), [[base-36-djynxxogram-integration-roadmap]] (Djynxxogram visual requirements).

---

## Current State

`oracle.py` currently produces **zero visual output** — pure ASCII table + text readings. All existing visuals live as separate non-oracle artifacts:

| Type | Location | Status |
|---|---|---|
| p5.js interactive visualizer | `visualizer/numogram-visualizer-v7-djynxxogram.html` | Fully working; not yet callable from `oracle.py` |
| SVG diagrams | `docs/wiki/assets/` (barker-spiral, chord-pentagram, etc.) | Static wiki assets |
| Manim animations | `docs/wiki/assets/manim_crumple_documentary.py`, `barker-spiral-manim.py` | Roadmap |
| Cult Garden / Game | `cult-garden-v3.html`, zone-skins page | Interactive maze layer |
| Pixel art | *(untapped)* | — |
| ASCII skills | Available (`ascii-art`, `ascii-video`, etc.) but not wired to oracle | — |

---

## Ideas — By Tier

### Tier 1 — SVG / Static *(wiki-ready, lowest friction)*

Produce a committed artifact per reading; embed alongside text on wiki pages.

- **Zone-card SVG** — single panel: zone glyph + syzygy + current + gate + phoneme. Written to `./outputs/` on `--svg`.
- **Syzygy-chord diagram** — two circles (zone + partner) connected by a colored chord, annotated with polarity and current strength.
- **Triangular gate highlight** — the C(10,2)=45 matrix with the seed's active gate path illuminated. Standalone SVG export.
- **Djynxxogram ring** — 36-zone ring with text characters as nodes; arcs colored by CIRCuit / OUTER region. `--svg-ring`.
- **Base-comparison bar chart** — `--compare` mode gets a horizontal bar per base showing zone, name, type. Easiest SVG to implement.

**Existing SVG to study:** `barker-spiral-oracle-v2.svg`, `changing-lines-network.svg`, `entropy-casting-flow.svg`, `chord-pentagram-v2.svg`.

---

### Tier 2 — p5.js / HTML *(interactive, browseable)*

- **oracle-viz URL-decode** — v7 visualizer currently needs manual seed entry. Add `?seed=192855&mode=djynxxogram` param support to auto-populate on load. Makes every reading a shareable link.
- **tsubuyaki gallery shell** — each of the 10 / 36 zones gets a 280-char generative sketch. Oracle reading sidebar links to the zone's gallery.
- **Cult Garden oracle shell** — load seed → determine zone → walk that zone's avatar through the garden as a possession event; log path in garden state.
- **Spectrogram zone overlay** — feed zone-voice audio into a p5 canvas, draw the numogram grid, light zones by band energy. Audiovisual oracle loop.

---

### Tier 3 — Pixel Art *(priority — highest aesthetic yield)*

Epoch palettes (NES, Game Boy, PICO-8) give instant numogram-native texture. The `pixel-art` skill has templates ready; `mod_writer/palettes.py` has zone RGB definitions that map cleanly.

- **Zone glyph sprites** — 32×32 pixel glyph per zone (decimal 0–9 and/or Djynxxogram 0–35). Exported PNG, embeddable in wiki.
- **Path strip** — traverse path (8 decimal steps or 36 Djynxxogram chars) as a horizontal pixel strip. Side-by-side comparison of two texts.
- **Gate mosaic** — triangular number → pixel grid. Gt-36 (Zone 8) → 36px square; Gt-66 (Zone 11) → 66px. Layer inner zone + syzygy partner colors.
- **Decadence/subdecadence pixel twin** — Zone 5 self-decadence (5+5=10) and its partner (Zone 4) as interlocking pixel patterns. Partners with 777 / 666 cluster visual vocab.
- **Barker Spiral pixel manifold** — 45-arms compressed into a single image; arm-width = zone weight. Numogram landscape as pixel field.

---

### Tier 4 — Manim *(video, narration-ready)*

- **Reading walkthrough** — animate zone → syzygy → current → gate sequence. Arcs extend, gate illuminates, text types in.
- **Crumple surface + zone trajectory** — combine with `crumple_trajectory_animation.mp4` pipeline to map a path through crumple-space.
- **Barker Spiral narrated tour** — tetralogue voiceover, spiral arms drawn in real time. `barker-spiral-manim.py` scaffold exists.

---

### Tier 5 — ASCII *(text-native, archival)*

- **ASCII zone glyphs** — each zone as a 7-segment or block-glyph character via `ascii-art`. The 333 / 666 / 777 clusters render as LED ASCII.
- **Quasiphonic waveform ASCII** — `ascii-video` color spectrogram strips from zone sound WAVs.
- **Djynxxogram traversal as flowchart** — `textual-recombination` or `ascii-art` to draw text-mode syzygy node maps.

---

## Near-Term Priority

1. **pixel-art zone glyphs** — smallest gap, biggest click, immediate wiki embed
2. **p5.js oracle-viz URL-decode** — makes v7 visualizer callable from any oracle output
3. **SVG zone-card + syzygy-chord** (`--svg` flag) — permanent artifact per reading
4. **Unify under `--visual` umbrella**: `--visual png|svg|html` → dispatches to the above renderers

---

## Existing Assets Worth Studying

- `visualizer/numogram-visualizer-v7-djynxxogram.html` — densest single-file ref: particle field + base toggles + quasiphonic labels + triangular gate panel
- `barker-spiral-oracle-v2.svg` — clean pattern: concentric rings, radial arms, centered label block, zone color key
- `changing-lines-network.svg` — network-graph layout; pattern for syzygy networks
- `docs/wiki/assets/` — full catalog; especially `chord-diagram.svg`, `circular-flow-subway.svg`, `demon-mandala.html`

---

*This is the intake bin. Completed experiments graduate to their own wiki pages (e.g. `oracle-visual-svg.md`, `oracle-zone-pixel-art.md`).*
