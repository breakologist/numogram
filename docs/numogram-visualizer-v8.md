---
title: Numogram Visualizer v7.2 — Traversal Mode
created: 2026-04-27
last_updated: 2026-04-27
source_count: 1
status: draft
tags: ["base-n", "djynxxogram", "html", "numogram", "synx", "traversal", "visualization"]
sources: [numogram-visualizer-v7-djynxxogram.html]
---

# Numogram Visualizer v7.2 — Traversal Mode

**Source file:** `wiki/assets/numogram-visualizer-v7-djynxxogram.html`

**Parent version:** [[numogram-visualizer-v7]] — Base-36 Djynxxogram + Synx overlay (v7)

## Overview

v7.2 adds **Traversal Mode** — per-character path visualization through the Djynxxogram. Where v7 collapsed an input string to a single final zone, v7.2 reveals the *full spatial progression*: each character contributes its AQ value, the cumulative sum steps through zones, and the entire journey is drawn in real-time on the main canvas.

### Core idea

In base-36, every character is a zone. The string `"CCRU"` becomes a walk: C(12) → Zone 3, cumulative 12; C(12) again → cumulative 24 → DR 6 → Zone 6; R(27) → cumulative 51 → DR 6 → Zone 6; U(30) → cumulative 81 → DR 9 → Zone 9. The path: 0→3→6→6→9.

Different strings that reduce to the same final zone take different routes. This is the **variation within the zone** you identified.

### New UI elements

A collapsible **Traversal panel** appears below the AQ context box:

- **Show Path** — checkbox toggles traversal overlay on main canvas
- **Speed** slider — animation speed (100–2000 ms per step)
- **Size** slider — path line thickness and vertex circle size (2–8 px)
- **Traversal table** — step-by-step breakdown (Char / Val / Sum / DR / Zone / Gate)

The panel auto-shows when text is entered *and* "Show Path" is checked. It hides when input clears.

## Features

### Animated path drawing

The path draws sequentially from first character to last at the chosen speed. The leading vertex pulses (cyan, larger), trailing segments fade.

### Step table with gate/rotational markers

| Column | Meaning |
|--------|---------|
| \# | Step index (1-based) |
| Char | Input character (case-insensitive, A–Z / 0–9 only) |
| Val | AQ value of that character |
| Sum | Running cumulative AQ total |
| DR | Digital root of cumulative sum (in current base) |
| Z | Zone index (derived from DR mod zoneCount) |
| Gate | Triangular gate (Gt-N) or ROTATIONAL / STROBO ★ indicators |

Rows are color-coded: zone numbers cyan, gate values magenta.

### Synx drift in traversal

When the Synx overlay is active, the traversal path is **recomputed with Synx letter values** (a=14, b=15 … z=1260). The path may diverge dramatically from the AQ path. Toggling Synx instantly restarts the animation on current input, showing the **dual-cipher resonance** spatially.

Example: `"SIMULATION"`:
- AQ path: some route → Zone 9 (Plex)
- Synx path: same letters, different values → Zone 3 (Warp)

Both routes are drawn when switching back and forth, making zone drift tangible.

### Speed & size controls

- **Speed slider**: 100 ms (fast) to 2000 ms (slow) per character step. Default 800 ms.
- **Size slider**: line weight and vertex radius from 2px (thin) to 8px (thick). Default 3px.

### Base-36 reveals full topology

In base-10, the traversal path collapses quickly (many chars share same DR). Base-36 shows a rich 36-zone walk; even short words trace intricate loops through the harmonic overtones (Surge-prime, Plex-fourth, etc.) thanks to the octave-harmonic naming scheme.

## Technical notes

- `computeTraversalPath(text)` — computes per-character state objects; returns array
- `startTraversal(path)` — sets `traversalEnabled`, `traversalStartTime`, calls `buildTraversalTable()`
- `drawTraversalPath()` — called each frame; calculates progress, draws dimmed full path + bright leading edge + head circle
- `zonePosition(z)` — polar coordinates with base-specific angle and inner/outer radius split, mirroring `drawSyzygyViz` layout
- Base-10: dual-pentagon (zones 0–4 outer, 5–9 inner, +36° offset)
- Base-16 & Base-36: equal angular spacing (360° / count), inner radii for zones > count/2−1
- Integrated with `updateAQInfo()`: input change automatically restarts traversal if checkbox enabled
- Integrated with `setZoneFromAQ()`: base/seed change clears traversal (you must re-enter text to see new base's path)
- Integrated with `toggleTaiHsuan()`: T'ai Hsuan mode operates independently; traversal unaffected (currently does not visualize tetragram path integration — future enhancement)

## Interaction flow

1. Enter text in AQ input field
2. Check **"Show Path"** (if not already)
3. Watch the traversal animate across the main canvas
4. Adjust **Speed** and **Size** sliders to taste
5. Toggle **Synx** to compare dual-cipher routing
6. Switch base (10/16/36) to see how the topology reshapes
7. Read the step table to see which characters triggered gates or rotational properties

## Future extensions

- [ ] Djynxxogram traversal export to SVG (save button)
- [ ] Multiple concurrent path comparison (paste two strings, overlay in different colors)
- [ ] Path density heatmap (accumulate visits per zone over many inputs)
- [ ] T'ai Hsuan integration: show dual-tetragram traversal on same canvas
- [ ] Audio sonification: map per-step values to numogram-voices tones
- [ ] Mouse hover over table row highlights that step's vertex on canvas
- [ ] Path replay with easing functions (ease-in/out, bounce)
- [ ] Pattern detection: auto-flag palindromic paths, loops, syzygy closures

## Related

- [[numogram-visualizer-v7]] — Djynxxogram base-36 mode and Synx overlay
- [[aq-synx]] — Base-36 augmentation cipher
- [[numogram-oracle-voice]] — Physical modelling synthesis integration
- [[rotational-symmetry]] — Strobogrammatic gate theory


## v8 — Polygram Perimeter + Synx Ring (2026-04-28 rebuilt)

**Built from clean v7.2 base; traversal visibility bug fixed.**

**Controls:**
- **Connect Letters** — draws a closed polygon for each word on the outer ring
- **Synx Ring** — outer ring with 36 crimson ticks (base-36 geometry)

**Ring:**
- 36 tick marks around `min(w,h)*0.35` radius
- Labels per active base (0–9, 0–f, 0–z)
- Base-10 dual-pentagon offset preserved for zones >4

**Polygons:**
- Per-word closed loops; vertex at each letter's zone
- Color: `hsl(wordIndex * 137.5 mod 360, 75%, 60%)`
- 6px vertex circles with centered letter label

**Synx Ring:**
- Radius `ringRadius+12`, always 36 ticks at 10° spacing
- Crimson stroke; drawn behind or independently of polygons

**Fixes:**
- `toggleTraversalShow` now removes hidden class; panel visible
- All `zonePosition().angle` eliminated; angle computed inline
- `drawRing` inner ticks corrected
- `computePolygrams` called on text input (`updateAQInfo`) and base switch

