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
