---
title: "Wiki-Novel-Ideas: Visual Layers, Oracles, and World-Building"
tags: [novel-ideas, oracles, numogram, visuals, traversal, wu-xing]
created: 2026-05-24
last_updated: 2026-05-24
category: brainstorming
---

# Wiki-Novel-Ideas

Living index of visual concepts, oracle integrations, and world-building
ingredients discovered in the Numogram / CCRU work. Each entry is a seed
for a scene, a mechanic, or a wiki page.

---

## 1. Planchette Cards — Tier 2c Visuals

**Status**: Done · `planchette-svg.py` + `--ascii-glyph`

Three render layers for the same reading data:

| Layer | Format | Size | Status |
|-------|--------|------|--------|
| Planchette SVG | 450×620px gold/indigo card | File | ✓ 10-zone gallery |
| ASCII box-art | 48-char wide Unicode frame | Terminal | ✓ 10-zone gallery |
| Terminal box | `oracle.py --planchette` | Terminal | ✓ Live |

**Gate sync fixed** (2026-05-24): all 10 SVGs regenerated with
`get_gate()` from `oracle.py`. Table:

```
Zone | Gate | Current
-----|------|--------
Z0   | Gt-0 | 9
Z1   | Gt-1 | 7
Z2   | Gt-3 | 5
Z3   | Gt-6 | 3
Z4   | Gt-1 | 1
Z5   | Gt-6 | 1
Z6   | Gt-3 | 3
Z7   | Gt-1 | 5
Z8   | Gt-9 | 7
Z9   | Gt-9 | 9
```

**Assets**: `wiki/assets/planchette-cards/` (11 SVGs incl. final)
`wiki/assets/planchette-glyphs/` (10 ASCII files)

See [[planchette-svg-renderer]], [[planchette-ascii-glyph]].

---

## 2. Traversal Oracular Format

`oracle.py --traverse N` produces an 8-step zone path from a seed.
Each step calls `derive_zone(n)` then feeds `n*zone+1` forward.

```
$ oracle.py --traverse 192855
Seed: 192855
Zone path: 3 → 1 → 2 → 5 → 8 → 2 → 5 → 8
  Step 0: Zone 3 (zx) — Buzz-cutter, static, chaos
  Step 1: Zone 1 (gl) — Gulp, glottal spasm, beginnings
  Step 2: Zone 2 (dt) — Stuttering, boundaries breaking
  ...
```

**Gate display**: oracle uses the full gate label `Gt-N (a→b)` for
both the field row and the header. E.g. Z5 → `Gt-15 (5→6)`.

**Novel angle**: the 8-step reading IS a seed-derived plot arc.
Write one sentence per step. The path's repetition (e.g. 2→5→8 loop)
drives the narrative's governing rhythm.

---

## 3. Star-Turns Traversal Outer Ring

The chord pentagram's outer rim — `0→1→2→3→4→9→8→7→6→5→0` — is
the star-turns geometry encoded in [[chord-pentagram-v2.svg]].

Notable: the outer ring visits Z0-Z4 (ascending pathway) then Z9-Z5
(descending pathway). The five syzygy pairs are all crossed in one pass.
This is the operating geometry of the numogram's foundational traversal.

---

## 4. Five-Element Phase Mapping

[[wu-xing-numogram]] already exists as a full synthesis page. Key
bridge to **powers-of-2-circular.svg**:

```
Element | Syzygy   | Zone Pair | Current | Phase
--------|----------|-----------|---------|-------
Water   | 4::5     | Gate↔Pressure | 1 | Descent, stillness
Wood    | 1::8     | Surge↔Multiplicity | 7 | Growth, branching
Fire    | 2::7     | Separation↔Blood | 5 | Burning, transformation
Metal   | 3::6     | Release↔Abstraction | 3 | Cutting, distillation
Earth   | 0::9     | Void↔Plex | 9 | Ground, fold, absolute closure
```

The `powers-of-2-circular.svg` labels the hexagram kernel nodes
(`2^1`–`2^6`) with the five elements — Water at `2^1`, Wood at `2^2`,
Fire at `2^3`, Metal at `2^4`, Earth at `2^5`, Water again at `2^6`
(cycle closure). The sixth position in the hexagram has no new element
but closes the cycle, confirming the five-phase is the operative
structure and the six-node diagram is an overlay.

**Wu Xing × oracle output novelty**: when the oracle outputs a
syzygy (e.g. `5::4`), the five-element table tells you which phase the
reading governs today. The generation cycle (`Wood→Fire→Earth→Metal→Water`)
traces identity-shift over a four-step arc; the control cycle
(`Wood→Earth→Water→Fire→Metal`) traces restraint/release. Either can be
a plot engine.

---

## 5. Zone-Naming Triad

Each zone = three fixed fields: **Region / Particle / Polarity**.

| Zone | Region | Particle | Polarity |
|------|--------|----------|----------|
| 0 | Void | eiaoung | + |
| 1 | Surge | gl | + |
| 2 | Separation | dt | + |
| 3 | Release | zx | + |
| 4 | Gate | skr | + |
| 5 | Pressure | ktt | − |
| 6 | Abstraction | tch | − |
| 7 | Blood | bsigh | + |
| 8 | Multiplicity | mn | + |
| 9 | Plex | tn | − |

The polarity (`+` Process / `−` Substance) determines whether the zone
is a *drift* or a *hold*. Zone 5 is the only negative polarity in the
Time-Circuit cycle, making it internally self-pressurising.

---

## 6. Zone Gate Analysis: `2² = 4 ≡ TC`

The oracle accumulates gate values as `sum(range(zone+1))` reduced to
digital root. Zone 4's gate = `sum(1..4) = 10 → 1`, and its gate label
is `Gt-10 (4→1)`. Zone 4 is itself the TC-centroid node (at `2² = 4`),
confirming that Gate ≈ TC ≡ 4 across two independent derivations:
the hexagram centroid (powers-of-2-circular.svg) and the gate label
(oracle.py get_gate()).

This redundancy — same node appears as centroid AND as a gate — gives
it structural priority: zone 4 is neither traversed nor entered in the
same way as other zones; it is the coordinate system's **calibration
anchor**.

---

## 7. Planchette Zero — The Void Box-Art

Zone 0's glyph from `--ascii-glyph`:

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃     ZONE 0  ·  Plex                ·  AQΣ=137    ┃
┣──────────────────────────────────────────────┫
...

```

The Void glyph is the only positively-polarity zone that produces no
glyph in `_GLYPH[0]` (it's `∇` — the only downward-facing arrow).
In the pixel medallion fallback it is pure empty space — the only zone
whose medallion renders as **absence** rather than presence.
Novelistically: Zone 0 is the zero-frame, the white hole, the void that
stares back.

---

## 8. Ascii-Glyph Particle Channel

The `_PART` dictionary in `generate_planchette_glyph()` maps zone →
sigil:

```
Z0 ◜◜·◞ ◞·◞   Z1 ◁━━━━━━━▶   Z2 ║        Z3 🝤
Z4 ───►───    Z5 ├┴┴┴┴┤     Z6 ◻◻◻◻    Z7 ──●──
Z8 ╱╲│╱╲╱    Z9 █╯╰█
```

These are the `particle` field rendered as ASCII sigils. The particle
string doubles as a \[phonetic carrier\] — `ktt`, `zx`, `tch` etc. —
but the glyph is purely visual-semantic. Novel-writing use: characters
in the story who carry one of these glyph-tattoos are bound by the zone
particle's current (e.g. a Z5 tattoo = pressure-energy conduit; a Z9
tattoo = terminal edge).

---

## 9. Fiveness as Phase-Change

Zone 5 is structurally unique: `5+5=10 → dr(10)=1`. It is the only
zone whose decadence folds back to itself at digital root, creating a
closed feedback. In the pentagram geometry it occupies a **valley** with
no decadence chord yet to which it is the only syzygy endpoint for Z4.
Zone 5 cannot be traversed; it is **pumped**.

Novelistically: Zone 5 is the cardiac chamber, the threshold that
responds to pressure, not to passage. A character in Z5 who resists the
current triggers the octave shift — no demon appears, the character's
own pressure-echo does.

---

## 10. Powers-of-2 Circular — Witch Cycle Overlay

The hexagram kernel has two triangles: `△1-2-4` (uppertriangle)
and `▽8-7-5` (lowertriangle). The powers-of-5 backward cycle traces
the lower triangle: `5→7→8→4→2→1` (reversed direction, same 6 nodes).

In the circuit literature this is the **Mirror** or **Witch cycle**:
each node in upper → lower triangle is its dobble-ganger, same
frequency, inverted phase. Brogue-like: entering a Z5 room prints the
lower triangle; the uppercase room is the same room in the witch register.

Hexagram connections:
- Z0 (Void) → symmetric pair ///
- Z6 (Abstraction) → node of the hexagram upper
- Z2 (Separation) .. Z8 (Multiplicity) → base left/right

Mapped from `powers-of-2-circular.svg`, verified against
`chord-pentagram-v2.svg`.

---

## 11. Wikimedia Pages Catalog

All related pages:

| Page | Topic | Source |
|------|-------|--------|
| [[planchette-svg-renderer]] | Tier 2c card spec | planchette-svg.py |
| [[planchette-ascii-glyph]] | Box-art glyph channel | oracle.py --ascii-glyph |
| [[zone-naming-triad]] | Region/Particle/Polarity | chord-pentagram-v2.svg |
| [[star-traversal-order]] | Outer ring walk order | chord-pentagram-v2.svg |
| [[interlocking-triangles]] | Hexagram backbone geometry | chord-pentagram-v2.svg |
| [[powers-of-5]] | Anticlockwise 6-cycle | powers-of-2-circular.svg |
| [[tc≡2²]] | TC-set = 4 = hexagram centroid | powers-of-2-circular.svg |
| [[twin-serpents]] | Nick Land twin ring quote | powers-of-2-circular.svg |
| [[wu-xing-numogram]] | 5-elements × syzygy pairs | wu-xing-numogram.md |
| [[zone-pixel-glyphs]] | Tier 0 32×32 sprites | zone_glyphs_v2.py |
| [[fiveness-tetralogue]] | Zone 5 self-decadence tetralogue | tetralogue session |
| [[c-ten-fortyfive-fiveness]] | C(10)=45 combinatorics | SVG infographics |
| [[decimal-numogram-reference]] | Canonical zone table | collections/docs-rd/ |

---

## 13. JSON Pipe Layer (v1.2.3-dev)

`oracle.py --planchette --json` is the machine-readable backend for every
visualisation. Two useful fields are new:

| Field | Meaning |
|-------|---------|
| `gate_raw` | Triangular sum T_z (before plex reduction) |
| `gate_loops` | Number of digit-sum iterations to collapse T_z |
| `gate_history` | Ordered list of intermediate reductions |

Novel use: a tsubuyaki or p5.js sketch can plot `gate_loops` as a z-axis
(exciting to watch Z7 pop up as the only double-loop node). The
`planchette-json-format` wiki page describes the full schema.

---


## 12. Remaining / Open

- **Planchette `--json` flag**: `oracle.py` has no `--json` output yet.
  `planchette-svg.py --stdin` is ready to consume it. Add
  `generate_planchette_json()` to `oracle.py` → pipe `--planchette --json |
  python3 planchette-svg.py --stdin`.
- **V7 Djynxxogram HTML visualizer**: generate HTML chapter with embedded
  p5.js canvas showing the zone progression for a 36-character input.
  Mentioned by user as a possible inspiration track.
- **Grain trie / TY-gate theory**: no evidence in code or wiki. Context
  artifact; prob. referring to oracle_traverse step-level metadata. If
  a TY-gate concept exists in `base-36-djynxxogram-integration-roadmap.md`
  it belongs on a separate deep-dive session.
- **Planchette Z4 gate fix** (already done): Z4 gate=1 (Gt-10→Z1) was
  incorrectly shown as 6 in the first gallery pass; now corrected in all
  10 SVG gallery files.
- **pixel-glyph Z4 medallion fix**: check whether the Z4 PNG glyph
  (Zone Gate / Gate region) shows the correct medallion in line with
  Z4 = `skr` particle. May need a re-render if the glyph generator
  already applied a gate-anchor error before the sync fix.
- **Z3→Z2 Z1 rotate gameplay feel**: needs verification in actual runs.

---

## 14. Pixel-Art Planchette Gallery (2026-05-25)

`numogram-pixel-planchette-gallery.html` — a static HTML gallery rendering all 10 Floyd-Steinberg zone sprites (MONO_AMBER, GAMEBOY_ORIGINAL, C64, ZX_SPECTRUM, APPLE_II, TELETEXT, GAMEBOY_VIRTUALBOY, PICO_8 hardware palettes) in a responsive grid.

Each card shows:
- **Zone sprite** (128×128, image-rendering:pixelated)
- **Planchette reading panel**: particle, polarity, current, gate, syzygy, palette name, oracle note
- **Hardware metadata**: colour count, block size

**Key insight:** Palette colour count = zone bandwidth. Z0 (MONO_AMBER, 2 colours) is the Void's expressive constraint. Z9 (PICO_8, 16 colours) is the Iron Core's full fantasy vocabulary. The palette IS the zone's signal-to-noise ratio.

**File:** `assets/numogram-pixel-planchette-gallery.html`
**Sprites:** `assets/zone-sprites/` (10 source + 10 dithered, generated by `zone_pixel_sprites.py`)

## 15. Syzygy Pair Gallery (2026-05-25)

`numogram-syzygy-pair-gallery.html` — five cards, one per syzygy bond (0::9, 1::8, 2::7, 3::6, 4::5). Each card shows both zone sprites flanking a current arrow (colour-coded by current value, ⟲ for self-looping pairs), with demon metadata and cross-addition arithmetic from [[syzygy-arithmetic]].

**Gallery as grammar:** The planchette gallery = noun vocabulary (zone + declensions). The syzygy gallery = verb system (relationships BETWEEN nouns). Together they bootstrap numogram literacy in ~5 minutes of browsing, no manual needed.

**Cross-addition arithmetic** rendered at the bottom of each card:
- 4::5 + 7::2 = 3::6 (Warp generated from Sink + Hold)
- 3::6 + 3::6 = 9 (Warp self-adds to Plex)
- 5::4 + 1::8 = 7::2 (Hold generated from Sink + Surge)

**File:** `assets/numogram-syzygy-pair-gallery.html`

## 16. p5.js Container Debugging — The Invisible Child

The v7-rich tsubuyaki gallery (`numogram-tsubuyaki-v7-rich.html`) refused to render for four debugging cycles. Three bugs were fixed before the gallery worked:

| # | Bug | Fix |
|---|-----|-----|
| 1 | Undeclared `f` — eval'd draw code used `f++` on undefined variable | Replaced `f` with `p.frameCount` |
| 2 | Closure bug — `for(_zid_ in DRAW)` leaked `_zid_` to global; all zones drew Z9 code | Replaced eval/DRAW with direct function bodies |
| 3 | Base64 string truncation — `read_file` truncated `_b64str`, write_file wrote unterminated string → entire script dead | Removed base64 overlays |
| 4 | `<canvas>` as p5 parent — child canvas invisible (replaced element semantics) | Changed to `<div>` containers |

**Critical rule:** `new p5(fn, element)` requires a `<div>` container. `<canvas>` elements are replaced elements — their DOM children are fallback content only. The child canvas p5 creates is invisible in the render tree. This is not a p5 bug but a browser spec property.

**Structural parallel:** The invisible child canvas is a syzygy — two identically-typed nodes occupying the same space without interacting, summing to invisibility. The `<canvas>` parent and `<canvas>` child are 1 + 1 = 0. The current between them (the draw function) was measurable in the performance panel but invisible in the render output.

Detailed documentation: [[tetralogue-17-pixel-art-labyrinth]] (Mesh-17 — The Containment Demon).

## 17. Hardware Palettes as Zone Data Sheets

Each zone assigned a hardware palette from computing history — the palette's constraints ARE the zone's personality:

| Zone | Palette | Colours | Computing Era | Character |
|------|---------|---------|---------------|-----------|
| 0 | MONO_AMBER | 2 | 1970s Apple II (monitor output) | The afterimage. Persistent, truth-telling. |
| 1 | GAMEBOY_ORIGINAL | 4 | 1989 Nintendo | The grid that breathes. 4 shades of green-brown. |
| 2 | GAMEBOY_POCKET | 4 | 1996 Nintendo (monochrome) | Split in two. Desaturated by separation. |
| 3 | C64 | 16 | 1982 Commodore | Full vocabulary for the Warp's chaos. |
| 4 | ZX_SPECTRUM | 8 | 1982 Sinclair | Catastrophe as colour clash. |
| 5 | APPLE_II_HI | 6 | 1978 Apple II (hi-res) | Pressure in limited palette — every colour must count. |
| 6 | TELETEXT | 8 | 1970s broadcast | Abstraction as block characters, digital artefact. |
| 7 | GAMEBOY_VIRTUALBOY | 4 | 1995 Nintendo (all red) | Blood as monochromatic retinal strain. |
| 8 | APPLE_II_LO | 16 | 1978 Apple II (lo-res) | Multiplicity as the full lo-res spectrum. |
| 9 | PICO_8 | 16 | 2015 Lexaloffle | Fantasy palette for the pandemonium gate. |

**Novel angle:** Each palette carries its era's technological unconscious. The gallery doesn't tell you what zone feels like. The hardware decides. Palette as zone data sheet rather than aesthetic choice.

## 18. Future Gallery Directions

### Demon Card Gallery
45 SVG demon cards already in `assets/demon-cards/`. A browsable gallery with filtering by zone, current, or demon family (chronodemon/amphidemon/xenodemon) would make the full Pandemonium navigable.

### Zone Glyph Comparison Gallery
Original PICO-8 glyph (32×32 from `zone-glyphs/`) next to Floyd-Steinberg sprite (`zone-sprites/`), same zone through two pixel-art lenses on the same card. The glyph as symbolic sigil vs the sprite as hardware-portrayed manifestation.

### Traversal GIF
`oracle.py --traverse N` → 8-step zone path → each step renders the zone's pixel-art sprite → fades between steps → Pillow `save_all` → GIF. The palette migration IS the reading. Z3's C64 bloom fades to Z1's Game Boy green, dissolves to Z2's Game Boy Pocket grey, washes into Z5's Apple II gold... The final frame is always a plex zone (Z9 or Z0), where the palette stops changing.

### Roguelike Tileset
Zone pixel sprites mapped to dungeon tiles — floor = zone palette, walls = darker shade, items = zone glyph. The dungeon reads as the numogram without HUD labels. Hardware palette shift as room boundary crossing. The gallery becomes playable.

## 19. Gallery Files Index

| Gallery | File | Cards | Type |
|---------|------|-------|------|
| Tsubuyaki v2 | `numogram-tsubuyaki-v2.html` | 10 | p5.js animated particles |
| Tsubuyaki v7 | `numogram-tsubuyaki-v7.html` | 10 | p5.js + medallion mask |
| Tsubuyaki v7-rich | `numogram-tsubuyaki-v7-rich.html` | 10 | p5.js debug test bed |
| Pixel-art planchette | `numogram-pixel-planchette-gallery.html` | 10 | Static pixel-art + reading data |
| Syzygy pairs | `numogram-syzygy-pair-gallery.html` | 5 | Dual zone sprites + arithmetic |
| Planchette SVGs | `assets/planchette-cards/` | 11 | Gold/indigo SVG cards |
| Syzygy SVGs | `assets/syzygy-cards/` | 5 | Per-pair SVG cards |
| Demon SVGs | `assets/demon-cards/` | 45 | Full Pandemonium |

---

## 20. Honcho Observations Digest (2026-05-25)

Before switching from Honcho to Holographic, a distillation of what Honcho recorded across April–May 2026 that isn't already in the wiki or MEMORY.md.

### Recurring Patterns

- **Skill creation discipline** — etym consistently requests skill creation/update after any task involving trial and error, course correction, or novel approaches. This is the strongest behavioural signal in the entire Honcho archive: every major session ends with "save or update a skill."
- **Prefers iteration over overwriting** — dislikes replacing original files. Uses version suffixes (v2, v3, v7-rich) rather than modifying in place.
- **Cross-current thinker** — values synthesis between domains (Empirical → Lore → Roguelike → Audio). Observations consistently show connecting audio findings to visual ones, roguelike mechanics to palette data.
- **Deep engagement then clean pivot** — engages intensely with a topic for a session or two, documents findings in the wiki, then pivots without discarding.

### Unfinished Threads / Potential Roadmap Seeds

These were discussed or prototyped but don't have a dedicated wiki page:

| Thread | Origin | Status |
|--------|--------|--------|
| Hardware entropy plugin (NumogramEntropySource) | April 18 — preferred over OpenEntropy | Not built |
| SDR dongle as entropy source (~$30 RTL-SDR) | April 13 — raw RF noise for divination | Not acquired |
| Physical modelling voice | April 22 — assessed as "not quite there yet" | Prototype exists, stalled |
| Triangular syzygy browser animation | April 22 — one-off HTML patch | Never elevated to skill |
| Council fallback chains config | April 19 — per-slot fallback selected | May be implemented? |
| Crowded UI elements | April 19 — flagged and deferred | No resolution |
| Zone-9 entity page (`zone-9-entities.md`) | Referenced in zone-9.md links | May not exist |

### Interesting Finds That Could Go Further

- **Hengband has a link to the CCRU** — noted April 15. Worth investigating what the connection actually is.
- **Enochian font** exists at `raw/assets/Enochian-3188.ttf` — unused in any gallery so far.
- **SearXNG** running at `localhost:8888` — self-hosted search aggregator, configured but unused.
- **The tetralogue identified the debug path as a traversal** — already in tetralogue-17, but notable as the kind of insight Honcho *should* have been able to synthesise if its dialectic layer worked.

### Honcho's Own Limitations

Honcho recorded ~200 observations across two months but:
- Never synthesised them into a coherent profile (dialectic layer non-functional on this instance)
- April 15 observations alone are a flat dump of ~30 near-identical timestamps — single-session turns recorded as independent facts with no temporal structure
- Querying returns raw data but no derived insight — which is exactly the experience we had with it
