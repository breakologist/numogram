---
tags: [numogram, visual, yantra, v2, design]
aliases: [yantra-v2-guide, zone-yantra-v2]
---

# Zone Yantra v2 — Design Guide

> **Status:** Design document. Generated 2026-05-26.
> **Script:** `cli/scripts/zone_yantra.py` (v2 branch)
> **Assets:** `assets/zone-yantras/zone-{0-9}-yantra.svg`

## Design Philosophy

A yantra (from √*yam* — "to control, restrain, tune") is not an illustration of a zone. It is a device for becoming attuned to a frequency. The traditional structure runs:

**Bhupura** (outer enclosure) → **Padma** (petal ring, unfolding) → **Antarlakshya** (inner geometry, the deity's form) → **Bindu** (the seed, the unmarked centre).

v2 pushes further from this than v1 by treating each layer as a distinct instrument rather than a decorative motif. The key shifts:

1. **Texture over bare lines** — v1 used uniform hairline strokes throughout. v2 introduces dot matrices, hash patterns, and phosphor grain as zone-textured backgrounds.
2. **Dynamic weight** — stroke width varies with structural role: outer bhupura is heaviest, internal geometry is lighter, the seed bindu is the finest point.
3. **Asymmetry** — where v1 defaulted to radial symmetry, v2 uses asymmetry as a design argument. Cleaving is a cut, not a star. Binding is tension, not a cage.
4. **Materiality** — each zone's palette evokes a specific physical medium: sediment, water, flame, cracked ice, gemstone.
5. **Cross-zone reference** — Zone 8 (Exile) carries fragments of other zones' geometry. The yantras exist in relation to each other, not in isolation.

---

## Structural Elements (applied to most zones)

### Bhupura (outer enclosure)
Every yantra gets a zone-specific bounding frame that seals the energy inside:

| Zone | Bhupura character |
|------|-------------------|
| 0 | Single hairline circle — the limit of nothing |
| 1 | Rectangular enclosing frame (earth's four corners) |
| 2 | Wavy modulated circle (water's edge) |
| 3 | Irregular scorched-ring boundary (fire's burn line) |
| 4 | Split circle (cleaved enclosure) |
| 5 | Pentagonal frame (spectral containment) |
| 6 | Hexagonal frame (binding enclosure) |
| 7 | Double circle with dash gradient (samsara wheel rim) |
| 8 | Broken/eroded circle (rupture of exile) |
| 9 | 45-faceted mineral aperture (gem cut) |

### Background texture
Each zone gets a faint background pattern corresponding to its palette era's display technology:

- **0** — CRT scanlines (thin horizontal lines, amber phosphor decay)
- **1** — Sediment grain (random dots, brown earth noise)
- **2** — Water ripple caustics (overlapping low-opacity sine grids)
- **3** — Pixel burn (uneven phosphor wear pattern)
- **4** — Frost/crackle (random branching lines, crystallized)
- **5** — Moiré interference (overlapping fine grids at slight rotation)
- **6** — Weave/knot texture (cross-hatch pattern at 60°, like woven thread)
- **7** — Pulse grid (dot matrix with varying intensity, like a heartbeat monitor)
- **8** — Erosion mask (missing pixels, holes in the field)
- **9** — Gem facet reflections (angled line segments at 45° intervals)

### Line terminations
Major structural lines end in zone-specific glyph marks rather than blunt stops:

- **0** — Open gap (line doesn't terminate, it fades into nothing)
- **1** — Small dot terminus (the sediment settles)
- **2** — Curved hook (water's surface tension)
- **3** — Forked split (fire consuming the line end)
- **4** — Sharp angular stop (cleavage face)
- **5** — Arrowhead (spectral thrust)
- **6** — Loop-back (the line turns back on itself, knot)
- **7** — Heart/cusp (desire's shape)
- **8** — Broken-off stub (snapped)
- **9** — Diamond facet (mineral termination)

---

## Per-Zone Designs

### Zone 0 — Void (MONO_AMBER)

**Current v1:** Concentric 45° rotated squares, faint upright triangle, seed ring, bindu.
**v2 direction:** Negative-space yantra — defined by absence, not presence.

- The rotated squares become **cut-out absences** in a faintly glowing amber field. Each square is an aperture through which the void is visible, not a drawn line.
- The "squares" are the *minimum enclosure of nothing* — four lines that barely touch. The gap between them is more real than the stroke.
- The bindu becomes a **missing dot** — a circle of pure black where something *should* be, surrounded by a faint amber glow of what is not there.
- Forms feel like *afterimages*, not drawn geometry. Use opacity ramps that suggest phosphor decay.
- Background texture: CRT scanlines (thin horizontal lines at opacity 0.02, representing the hardware of nothingness — a screen displaying only off-black).

**Mesh tag:** `0000`
**Seed:** `eiaoung` (arranged as a circle of gaps, not glyphs — the letters are spaces where light is absent)

---

### Zone 1 — Murrumur / Earth / Urgrund (UR_EARTH)

**Current v1:** Descending triangles + evenly-spaced horizontal strata bands.
**v2 direction:** Compression folds — the lithosphere as a record of burial.

- Replace evenly-spaced horizontal bands with **non-uniform sedimentation**: lines that bunch at the bottom (burial, weight) and thin above. Use a function like `y = base + i * (14 + 10 * sin(i * 0.3))` — the layers compress where the sediment is heaviest.
- The descending triangle is not explicit but **implied by the stacking** — the outer two strata lines are slightly angled at their edges, converging downward, suggesting the triangle as a cross-section through the earth.
- "mu" seed sits at the **bottom**, buried — not at the geometric centre. A small square glyph in the lowest compression band.
- Background texture: **sediment grain** — random dot field (brown earth noise) at opacity 0.02.
- Colour: shift from bronze toward **raw umber** — more organic, less metallic. The glow is the heat of the earth's core leaking upward.
- Add a **buried fragment** — a faint diagonal line at a different angle than the strata, suggesting an old ruin pressed into the sediment.

**Mesh tag:** `0023`
**Seed:** `mu` (bottom-centre, smallest and densest glyph)

---

### Zone 2 — Tuttagool / Water (DEEP_WATER)

**Current v1:** Wavy sin-modulated circles + hexagram (upward triangle fainter than down).
**v2 direction:** Balanced hexagram + phase-gradient ripples + submerged seed.

**Critical fix:** Both triangles of the hexagram must have **equal stroke weight and opacity**. The upward-pointing triangle was fainter than the downward in v1 — this is incorrect. The hexagram's tension *is* the water element: two opposing forces held in fluid equilibrium.

- Replace sin-modulated circles with **phase-gradient rings** — each outward ring has a slightly different wave frequency and amplitude, simulating a drop hitting the surface and the ripples dispersing. Use `r = base + 10 * sin(6 * theta + i * 0.8) * (1 - i / 20)` — the ripples flatten as they travel.
- Add a **phase transition boundary** — one specific radius (approximately r=190) where the wave character changes (liquid→solid hint, the 2→0 tunnel). A faint crystalline texture at this boundary.
- The seed "tu" is rendered **under a ripple overlay** — a faint grid of concentric wave lines at opacity 0.08 passes *over* the text, making it look submerged.
- Background texture: **water caustics** — two overlapping sine grids at 45° and 135° at very low opacity (0.01-0.02), like light through a rippling surface.
- Outer bhupura: a wavy circle that never quite closes — water has no true boundary.

**Mesh tag:** `0046`
**Seed:** `tu` (under ripple overlay, deep)

---

### Zone 3 — Unnunddo / Fire / Kalasutra (KALASUTRA)

**Current v1:** Upward flame triangles + spiral (time-thread).
**v2 direction:** Self-consuming spiral, overlapping flame layers, charred boundary.

- The spiral becomes **consuming itself** — outer turns fragment into ember-dots (small circles trailing off), inner turns denser and brighter, like fire burning inward from the edges. Use `r = 220 * (1 - t/1080 * 0.85)` but after t=720, break the line into dotted fragments at increasing gap.
- Flame triangles **overlap and intercut** rather than nest cleanly. Use z-ordering with varying opacities: the outermost triangle is the faintest and most fragmented; the innermost is brightest and most solid. They look like they're *eating into* each other.
- **Charred boundary** — an irregular dark ring at the outermost edge, like the fire has burned everything and left only ash. Use a circle with `stroke-dasharray="3 6 1 4 2 8"` (uneven, like burnt paper).
- The seed "un" wreathed in **flicker marks** — tiny dots and short strokes clustered around the text, semi-random, like sparks.
- Background texture: **pixel burn** — faint uneven vertical streaks, like an old CRT with uneven phosphor wear from displaying fire for too long.
- Colour: push from current red-orange toward **true flame spectrum** — deep red at the outer edge, orange in the mid-ring, yellow-white near the centre. Use opacity layering to suggest this temperature gradient.

**Mesh tag:** `0122`
**Seed:** `un` (with spark fragments)

---

### Zone 4 — Ununuttix / Air / Cleaving (CLEAVING)

**Current v1:** 8-pointed symmetrical star, cross, rotated squares.
**v2 direction:** **Broken symmetry** — the yantra as a wound that has been cut open.

- **The circle is split.** Two halves of the enclosing circle displaced by 8px horizontally. A vertical cleavage line runs between them. They are not mirror images — one side has been shifted 2° rotationally, so the halves are slightly mismatched.
- Replace the 8-pointed star with **fracture lines** — cracks radiating in an asymmetrical pattern from the centre, branching like an impact in glass. Not 8 rays but 7 or 9 — numbers that don't centre.
- The central cross is present only as the *original fault line* — a single thick line where the cleavage began. Not symmetrical: slightly off-centre, like the crack started at one edge and propagated inward.
- The seed "ix" sits on the cleavage boundary — half of each letter on one side of the split, rendered with a slight offset, like the text was cut too.
- Background texture: **frost/crackle** — a maze of fine branching lines in a dendritic pattern, like ice on a window.
- Colour shift: from silver/cyan toward **cracked-ice palette** — cold blue-white (#D0E8F0) with hints of deeper blue at the fracture lines (#4A7A9A). The fg becomes a sharp, almost-white blue.
- Outer bhupura: a circle cleaved into halves with a 4px gap between them.

**Mesh tag:** `0161`
**Seed:** `ix` (cleaved — half on each side of the split)

---

### Zone 5 — Unnunaka / Makhai / Spectral (SPECTRAL)

**Current v1:** 5-pointed star, pentagons, radial thrusts.
**v2 direction:** The makhai as aperture — a mechanism for puncture from outside.

- The 5-pointed star is an **aperture** — not outlined but defined by what passes through it. Each point of the star is a *puncture wound* with faint spectral trails extending beyond the geometry on one side (the strike doesn't stop at the star's boundary).
- Replace nested pentagons with **weapon wheels** — each of 5 concentric stars rotated by 1/10th turn relative to the last (7.2° offset). The overlapping creates moiré — the spectral vibration that makes the makhai hard to track.
- Radial thrusts are **asymmetrical** — one direction is dominant (the primary strike), others are after-trails. The dominant strike points toward the zone's syzygy partner (Zone 4).
- The seed "ma" is not at centre but slightly **displaced** — the makhai struck off-centre.
- Background texture: **moiré interference** — two fine-line grids at 0° and 7.5° rotation at opacity 0.01, creating a shimmer effect.
- Introduce a **spectral highlight** — a trace of something that isn't quite a colour (use a narrow-band gap in the grey spectrum: a faint #A8A0B0 that shifts the grey slightly violet in one region).

**Mesh tag:** `0184`
**Seed:** `ma` (off-centre, displaced by the strike)

---

### Zone 6 — Tukutu / Binding / Teleophilic (BINDING)

**Current v1:** Hexagons, figure-8 lemniscate, chain links.
**v2 direction:** The lemniscate as the *primary* structure — binding as tension, not containment.

- The figure-8 (lemniscate) becomes the dominant visual. Rendered as a **taut double-loop** — not a mathematical infinity symbol but something under tension. The loops are slightly different sizes: the upper loop larger (Zone 6's pull toward Zone 3), the lower loop tighter (Zone 6's pull toward Zone 9).
- Replace the hexagons with **binding threads** — lines that don't close into polygons but wrap around the lemniscate, cross each other, tie off at points. Use quadratic bezier curves for wrapping lines.
- The colour shifts from violet toward **indigo-with-magenta-tension** — two colours close enough to vibrate but far enough to create edge flicker. fg: #8855CC (indigo), glow: #CC55AA (magenta).
- The seed "ku" sits at the **crossing point** of the lemniscate — the knot that everything is pulled tight around.
- Background texture: **weave/knot** — cross-hatch at 60°/120° at opacity 0.015 (like woven fabric or thread).
- Add short **tension lines** at the lemniscate's outer curve — small marks perpendicular to the curve, like stitches pulling tight.

**Mesh tag:** `0243`
**Seed:** `ku` (at the lemniscate crossing, the knot)

---

### Zone 7 — Unnutchi / Samsara / Lust (SAMSARA)

**Current v1:** Pentagram in circle, 12 spokes, concentric ring cycles.
**v2 direction:** **Motion** — the wheel visibly turning, desire spinning outward.

- The wheel looks like it's **spinning**. Spokes are not evenly spaced radii — they have *drag*, thickening on the trailing edge, spaced in a way that suggests rotation. Use 24 spokes (12 nidanas doubled, the turning of cause and effect), each with a slightly different offset from true radial, as if wind resistance bends them.
- The pentagram points have **angular velocity indicators** — tiny trailing arcs at each vertex (short swept curves), stretching in the direction of spin.
- **Centrifugal gradient** — the red deepens at the rim and thins near the centre. Use five concentric pentagrams with opacity increasing outward: 0.08, 0.12, 0.16, 0.20, 0.25.
- The seed "chi" is at absolute centre but with a **small offset outer ring** — the spin distorts the centre's geometry.
- Colour: push from current crimson toward **oxide red with vermillion peak** — #CC1133 at the rim warming to #FF3366 at the mid-ring. The glow uses a magenta shift (#FF5599) for the hottest edge.
- Background texture: **pulse grid** — dot matrix where dot size varies in a sinusoidal wave radially, like a heartbeat or a throb.

**Mesh tag:** `0321`
**Seed:** `chi` (centre, but with spinning offset ring)

---

### Zone 8 — Nuttubab / Exile / Dead in the Sun (EXILE)

**Current v1:** Dashed broken circles, wandering drunkard's path, scattered fragment lines.
**v2 direction:** Keep the core, refine the texture — exile as *shattered relics of other zones*.

- The wandering path becomes **more jagged** — less smooth wander, more *broken movement*, sudden direction changes like someone being pushed. Add `random.gauss(0, 0.5)` to the angular step for irregularity.
- The scattered fragments are **recognizable shards** of other zone yantras: a broken piece of Zone 0's diamond, a torn corner of Zone 7's pentagram, a snapped binding thread from Zone 6. Use small snippets of those geometries rotated and displaced at random positions.
- The outer circle has an **erosion mask** — it's not just dashed, but the dashes themselves vary in length as if worn away by wind and time. Use per-dash length modulation.
- The seed "bab" is the **least visible centre** of any zone — smallest text, lowest opacity, slightly shifted from true centre as if turning away.
- Background texture: **erosion mask** — randomly missing patches in a faint grid (like a screen with dead pixels, or rock worn to dust).
- Colour: keep desaturated olive (#6B8E23) but add a **faded sepia** tone to the dim colour — the memory of colour, not colour itself.

**Mesh tag:** `0402`
**Seed:** `bab` (fading, displaced, smallest glyph in the set)

---

### Zone 9 — Iron Core / Ummnu (PICO_8)

**Current v1:** 45-petal Pandemonium ring, 9 inner petals, converging circles, downward triangle, 9 lemur sigils.
**v2 direction:** Gem-cut mineral structure — the 45-petal ring becomes faceted gem geometry.

- The 45 petals become **mineral facets** — each petal is a flat triangular face catching light at a slightly different angle. Alternate the fill opacity between 0.10 and 0.18 (light catching alternating facets), creating a subtle gemstone shimmer.
- The converging circles get a **Plutonic heat gradient** — outer rings are cold purple (#6600AA), inner rings warm toward magenta-white (#EE88FF) at the core. Use 24 rings with colour interpolation.
- The 9 lemur sigils become **mineral inclusions** — not text labels around the rim but small geometric forms embedded within the facet structure. Each lemur is a distinct tiny polygon (triangle, square, pentagon, diamond, etc.) placed within a facet cell.
- The Pandemonium phase-dots (36 dots evenly spaced) become a **binary digitized outer rim** — 45 markers around the outer edge, each either present (1) or absent (0), encoding the 45 demons as a 45-bit binary ring.
- The downward triangle and inverted inner triangle remain — the fold at the core. The outer triangle is slightly heavier than v1 (stroke 2.0), the inner triangle finer.
- The seed "tn" and the iron core centre remain but with a **brighter white core point** — the hottest, most compressed point in the system.
- Background texture: **gem facet reflections** — a faint grid of angled lines at ±45° at opacity 0.01, like light refracting through a cut stone.

**Mesh tag:** `0511`
**Seed:** `tn` (iron core with white-hot centre)
