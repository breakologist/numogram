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

---

## Current State

`oracle.py` currently produces **zero visual output** — pure ASCII table + text readings. All existing visuals live as separate assets:

| Type | Location | Status |
|---|---|---|
| p5.js interactive visualizer | `visualizer/numogram-visualizer-v7-djynxxogram.html` | Fully working; not yet callable from oracle.py |
| SVG diagrams | `docs/wiki/assets/` (barker-spiral, chord-pentagram, etc.) | Static wiki assets |
| Manim animations | `docs/wiki/assets/manim_crumple_documentary.py`, `barker-spiral-manim.py` | Roadmap |
| Cult Garden / Game | `cult-garden-v3.html`, zone-skins page | Interactive maze layer |
| Pixel art | Not started | — |
| ASCII skills | Available but not used for oracle | — |

---

## Ideas — Organized by Tier

### Tier 1 — SVG / Static (lowest friction, wiki-ready)

These produce a committed artifact every time; good for the wiki alongside text readings.

- **Zone-card SVG** — single panel: zone glyph + syzygy + current + gate + phoneme. Written to `./outputs/` on `--svg`.
- **Syzygy-chord diagram** — two circles (zone + partner) connected by a colored chord, annotated with polarity and current strength.
- **Triangular gate highlight** — the C(10,2)=45 matrix with the oracle seed's gate path illuminated. Export as standalone SVG.
- **Djynxxogram ring** — 36-zone ring with your text's characters as nodes, arcs colored by CIRCUIT / OUTER region. `--svg-ring`.
- **Base-comparison bar chart** — for `--compare` mode: a horizontal bar per base showing zone, name, and type. Easiest SVG tier to implement.

**Existing SVG assets to study:** `barker-spiral-oracle-v2.svg`, `changing-lines-network.svg`, `entropy-casting-flow.svg`, `chord-pentagram-v2.svg`.

---

### Tier 2 — p5.js / HTML (interactive, browseable)

- **oracle-viz URL-decode** — v7 visualizer currently needs manual seed entry. Add `?seed=192855&mode=djynxxogram` to auto-populate and render on load. Makes every reading a shareable link.
- **tsubuyaki gallery shell** — each of the 10 (or 36) zones gets a 280-char generative sketch. The oracle reading sidebar could link to the zone's gallery page.
- **Cult Garden oracle shell** — load seed → determine zone → walk that zone's avatar through the garden as a possession event; log path in the garden's state.
- **Spectrogram-reactive numogram** — heavy; starts with audio first, then overlays zone grid on spectrogram TOP.

---

### Tier 3 — Pixel Art 🗺️ *(Priority)*

This is where the aesthetic gets distinctive and numogram-native. Epoch palettes (NES, Game Boy, PICO-8) give instant period texture.

- **Zone glyph sprites** — 32×32 pixel glyph per zone (decimal 0–9 and/or Djynxxogram 0–35). One sprite per reading, exported PNG. Great for wiki embed, mod-writer album art, wallpaper source.
- **Path strip** — the traverse path (8 decimal steps or 36 Djynxxogram chars) as a horizontal pixel strip. Each cell = zone-colored tile. Compare two texts side-by-side as paired strips.
- **Gate mosaic** — triangular number → pixel grid. Gt-36 (Zone 8) → 36px square. Gt-66 (Zone 11) → 66px rectangle. Color layering: inner zone + syzygy partner interleaved.
- **Decadence/subdecadence pixel twin** — Zone 5 and its partner (Zone 4) rendered as two interlocking pixel patterns, encoding the 5+5=10 self-decadence fold visually. Would partner well with the keter-crown / 777 cluster visual vocabulary.
- **Manifold** — pixel-art version of the Barker Spiral's 45 arms, each arm = one pixel column, width = zone weight. A compressed numogram landscape as a single image.

The `pixel-art` skill has era-palette templates ready. The mod-writer's `palettes.py` already has zone color definitions that map cleanly into 8-bit RGB.

---

### Tier 4 — Manim (video, narration-ready)

- **Reading walkthrough** — animate zone→syzygy→current→gate sequence. Text fades in; arcs extend; gate illuminates.
- **Crumple surface + zone trajectory** — combine with the existing `crumple_trajectory_animation.mp4` pipeline to map an 8-step path through crumple-space.
- **Barker Spiral narrated tour** — the four-current tetralogue as voiceover, spiral arms drawn in real time. Production pipeline in `barker-spiral-manim.py`.

---

### Tier 5 — ASCII (text-native, archival)

All ASCII skills exist and are viable; only oracle.py hasn't been wired to them yet.

- **ASCII zone glyphs** — `ascii-art` skill to render each zone as a 7×5 or larger glyph, including 333/666/777 clusters.
- **Quasiphonic waveform** — `ascii-video` to render zone sounds as colored ASCII spectrogram strips.
- **Numogram diagram as ASCII flowchart** — the Djynxxogram traversal as a text-mode flowchart.
- **Seven-segment LED cluster** — the 333/666/777 numbers as LED ASCII art with live zone overlay.

---

## Near-Term Priority

1. **pixel-art zone glyphs** — smallest gap, biggest visual impact, immediate wiki embed value
2. **p5.js oracle-viz URL-decode** — makes v7 visualizer callable from oracle output
3. **SVG zone-card + syzygy-chord** — two `--svg` variants, each can be the default `--visual` flag
4. **Wrap the three above into a `--visual` umbrella flag** displatching by `--format png|svg|html`

---

## Assets Already Worth Studying

- `visualizer/numogram-visualizer-v7-djynxxogram.html` — particle field + base toggles + quasiphonic labels + triangular gate panel; the densest single-file ref
- `barker-spiral-oracle-v2.svg` — clean SVG pattern: concentric rings, radial arms, centered label block, zone color key
- `changing-lines-network.svg` — network-graph layout in HTML (good for syzygy networks)
- `docs/wiki/assets/` — the full catalog; especially `chord-diagram.svg`, `circular-flow-subway.svg`, `demon-mandala.html`

---

*This page is the intake bin for oracle visual experiments. Completed work graduates to its own wiki page (e.g. `oracle-visual-svg.md`, `oracle-zone-pixel-art.md`).*
