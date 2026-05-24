# p5.js Oracle Sketch — Design Spec

> forked from `zone-walker` (Thread 6 Step 1) + tsubuyaki v7/v8 walker idioms

## Overview

A live p5.js canvas that renders an oracle reading as generative art. Not a static
screenshot — it breathes. The zone medallion pulses, the reading text drifts,
and the syzygy ring turns. Seed is fixed, so deterministic reload gives the
same artwork.

**Status:** spec only — not yet implemented.
**Entry point:** `docs/wiki/assets/oracle-sketch.html` (standalone, no TD dependency).

---

## Five sections in the draw loop

```js
function draw() {
  aim_speed(60);   // cap FPS
  noise_seed(zone * 7919);
  zone_cycle();
  zone_glyph();
  sprite_pulse();
  reading_overlay();
  tty_colours();
}
```

---

### 1. `zone_cycle` — deterministic walker ring

- **Source:** `oracle.traverse(seed, 8)` → `[3,1,2,5,8,2,5,8]`
- Draw as two concentric rings:
  - **Outer ring** — drawn as evenly-spaced zone dots (one per step). Zone dot
    coloured from `_ZONE_TTY_RGB`. Radius = `width * 0.42`.
  - **Path lines** — connect each step to next with a straight chord, weighted
    dimmer for revisits (Z→Z returns get a dashed or faded stroke).
- **Motion:** the path ring rotates at `TWO_PI / 880` per frame (≈880-frame full
  rotation at 60fps ≈ 15s). Direction: zones cycle clockwise, syzygy pair
    zone-ring counter-rotates one quarter step per second.
- **Determinism:** `random_seed(seed)` set at setup; all noise calls use that
  seed. Same seed, same artwork on reload.
- **Key visual:** the path line between Zone 2 → 5 → 8 appears three times
  (once forward, once return, once repeat). Fade return traverses to 40% opacity.

---

### 2. `zone_glyph` — planchette V-octagon

Inspired by the planchette zone glyph (V-shaped aperture). Each zone gets a
unique polygon encoding, rendered with `beginShape()` + `vertex()`:

| Zone | Shape hint | Rotation seed |
|------|-----------|---------------|
| 0    | concentric ring collapse | 0 |
| 1    | inhalation triangle (point in) | 72 |
| 2    | stutter zigzag break | 36 |
| 3    | 8 spoke radial | 45 |
| 4    | fold recurve twin-peak | 144 |
| 5    | diamond pinched: two triangles | 216 |
| 6    | turbulence scatter | 288 |
| 7    | ascending lip-flap arc | 324 |
| 8    | three-petal bloom | 180 |
| 9    | 45-aperture cthellloid arc | 108 |

Render at `bottom-right quadrant`, offset `width*0.65, height*0.65`, size
`min(w,h)*0.22`. Filled with `_ZONE_TTY_RGB[zone]` at 20% opacity. Perimeter
stroke at 100%.

---

### 3. `sprite_pulse` — 10×10 pixel medallion

Reuse `_pixel_hash(zone, x, y)` from `planchette-svg.py` (prime 7919 multiplier)
to generate the 10×10 binary grid. Duplicated in JS from the Python version to
avoid external deps:

```js
function pixelHash(zone, x, y) {
  const seed = (zone * 7919) ^ (x * 31) ^ (y * 17);
  return ((seed * 0x5bd1e995) & 0xffff) > 0x6fff ? 1 : 0;
}
```

Render each pixel as a `rect(x*scale, y*scale, scale, scale)` filled from
`_ZONE_RGB[zone]`, no stroke. **Breath pulse:** modulate fill alpha by
`0.6 + 0.4 * sin(t * TWO_PI * (0.5 + zone * 0.05))`. The medallion rhythm is
slightly different per zone — faster pulse for tension zones (2,3,5,7), slower
for restful zones (0,8,9).

Placed: top-left, `width*0.07, height*0.07`, cell size 18px → total 180px wide.

---

### 4. `reading_overlay` — planchette text composited

Pulls reading data from embedded `readings` object (same dictionary as
`oracle.py ZONES`):

```js
const readings = {
  0: {name:"Z0_Void", lon:"Eiaoung", current:"Abysmal",
      gate:"Gt-9=Z", syzygy:"0::9"},
  // ... all 10 zones
};
```

Draw three blocks:
- **Zone header** — `zone_name`, `seed`, `AQΣ` bold, `_ZONE_TTY_RGB` fill, size 14
- **Reading body** — full `zone.reading` string, 11px, word-wrapped at
  `width * 0.38`, line-height 18px, fill `rgba(r,g,b, 0.88)`
- **Book of Paths** — `zone.path`, italic, 10px, lighter opacity 0.65, tinted
  with `_ZONE_TTY_RGB` at 50% saturation

Position: right panel, padding `width*0.04`, leading after medallion gap
`width*0.22`. Text flows from top-left of panel.

---

### 5. `tty_colours` — zone gradient field

Fill the background of the **reading panel** (top-right and bottom-right
quadrants) with a smooth `lerpColor()` gradient between:
- Background fill: `lerp(ZONE_RGB[prev_zone], ZONE_RGB[zone], t_mod)`
- Top-stripe overlay: same tint at 15% opacity, width = 40px strip along the
  medallion panel left edge

On zone transitions (every N frames where zone changes), flash the entire
specular gradient: `flash = 1.0 * exp(-(frame - transition_frame) * 0.15)`.

---

## Visual composition

```
+─────────────────────────────────────────────+
│ Z3_Warp  seed:174  AQΣ=140        [medallion]│ ← top-bar
│             zone_cycle ring legend          │
├──────────┬──────────────────────────────────┤
│ sprite_  │ reading_overlay                  │
│ pulse    │  zone name, reading body, paths  │
│          │                                  │
│ zone_    │  tty_colours background tint     │
│ glyph    │                                  │
└──────────┴──────────────────────────────────┘
```

---

## Colour system

All colours sourced from single JSON object (imported at top of sketch):

```js
const ZONE_RGB = {
  0: [222,180,16],  1: [100,200,255],  2: [255,100,100],
  3: [255,255,0],   4: [180,100,255],  5: [255,140,0],
  6: [0,255,128],   7: [255,60,60],    8: [180,200,255],
  9: [60,30,0],
};
```

No zone's RGB value appears elsewhere in the drawing (each zone owns its tint
spectrum completely — zero spill between zones).

---

## Realtiming

| Element | Period | Source |
|---------|--------|--------|
| Path ring rotation | 880 frames (~15 s @ 60fps) | TWO_PI / 880 |
| Sprite pulse freq | `0.5 + zone*0.05` Hz | zone index → Hz |
| Reading drift | 2200 frames (~37 s) | sin(frame/2200) × 3px horizontal |
| Zone-glyph rotation | 1200 frames (~20 s) | slot index extent |
| Flash decay | `0.15` frames⁻¹ | exp |

Real-time, no pre-render. `draw()` runs at 60fps; p5.js handles the event loop.

---

## Implementation checklist

- [ ] HTML shell: `<script src="p5.min.js"></script>` + inline p5 sketch
- [ ] Zone palette JSON (`zone-palettes.json`) loaded as inline `<script type="application/json">` or pre-baked JS object
- [ ] `setup()`: single `createCanvas(`, set `randomSeed(seed)`, pré-calc `traverse()` path
- [ ] `draw()`: call the five sections in order
- [ ] `windowResized()`: keep canvas responsive, re-centre rings
- [ ] `saveCanvas()` on keypress 's' → PNG of current frame
- [ ] Word-wrap the reading body (no `text()` overflow — see p5js skill for `wrapText()` helpers)
- [ ] Test: seed 174, 192855, 81 match oracle.py reading output (same zone)

---

## References

- `p5js/SKILL.md` — p5.js production pipeline
- `numogram-oracle/README.md` — oracle.py API, zone data structures
- `visual-layers-state-map.md` Thread 10b — ranked effort/payoff
