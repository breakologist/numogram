|---
title: Visual Layers — State Map & Thread Ranking (2026-05-24)
created: 2026-05-24
status: active
category: reference
tags: ["visual", "oracle", "tsubuyaki", "p5js", "pixel-art", "medallion", "planchette"]
---

# Visual Layers — State Map & Thread Ranking

> Scored and ordered by effort × payoff. Medallion-as-mask leads because it closes the loop between pixel-art skill and tsubuyaki gallery in a single file patch.

---

## Live Layers

| Layer | Tool | File | Status |
|---|---|---|---|
| ASCII planchette box | `oracle.py --planchette` | `oracle.py` L674 | ✓ Live |
| ASCII glyph planchette | `oracle.py --planchette --ascii-glyph` | `oracle.py` L574 | ✓ Live — `_GLYPH` dict, 48-col width |
| PNG zone glyphs | PIL / planchette-svg.py | `~/numogram/docs/wiki/assets/zone-glyphs/` | ✓ Rendered (PICO-8) |
| Syzygy SVG cards | `scripts/syzygy-card.py` | `assets/syzygy-cards/` | ✓ Rendered — 5 pairs |
| Demon card SVGs | `scripts/demon-cards.py` | `assets/demon-cards/` | ✓ Rendered — 45 demons |
| SVG planchette w/ medallion | `planchette-svg.py` | `planchette-svg.py` L160+ | ✓ v1 — ZONE_HW_PALETTE integrated |
| Tsubuyaki v5 gallery | p5.js HTML | `numogram-tsubuyaki-v5.html` | ✓ Working |
| Tsubuyaki v6 gallery | p5.js HTML | `numogram-tsubuyaki-v6.html` | ⚠️ Builds; p5.js canvas rendering broken (eval-based init, script ordering) |
| Planchette v1/v2 SVG | `planchette-svg.py` | `planchette-svg.py` | ✓ Frame-angle arcs, gold/indigo overlay |

---

## Porous Layers (implemented-ish, not surfaced)

| Layer | Block |
|---|---|
| `--glyph` inline PNG | `oracle.py` → `--glyph` flag TODO; needs iTerm2 inline image protocol |
| SVG planchette hydration (Tier 2c) | Full spec URL→base64 + gold/indigo frame-angle arcs; partially done in v1/v2 |
| Djynxxogram wheel (Tier 3) | `--planchette --djynxxogram` — 36-zone wheel with glyph path; not coded yet |
| p5.js realtime canvas (Tier 4) | Script insertion order in v6 gallery prevents p5 from executing |

---

## Known bugs

| Bug | Status |
|---|---|
| Z0 medallion: 16 colors (expected 2, `MONO_AMBER`) | Traced to `_HWPALETTES` fallback path; fix deferred |
| Z5 medallion: 6 colors (expected 16, `APPLE_II_LO`) | Same fallback path; fix deferred |
| TUI 503 | `nousresearch/openrouter` Step 3.5 Flash OAuth failure — blocks all TUI requests; workarounds: `execute_code` / `terminal` |

---

## Zone-Walker / TouchDesigner bridge

Already planned as Tier 4. Shortest path: build p5.js sketch first (can do without TUI, terminal-only), verify it runs, then add MCP call to TouchDesigner. This is the real-time audio-visual scrying loop described in Soul v2.0.

---

## Ranked Threads (effort × payoff)

| # | Thread | Effort | Payoff | Dependencies |
|---|---|---|---|---|
| 1 | **Medallion-as-mask** on tsubuyaki canvases | ~15 LOC + v6 patch | High (visible) | v6 gallery, `_pixel_hash` |
| 2 | **Hardware-palette color graft** into tsubuyaki sketches | ~20 LOC + JSON sidecar | High — ties 3 skills | `_HWPALETTE` from pixel-art |
| 3 | **CSS-animated demon cards** (medallion `@keyframes`) | ~40 LOC CSS + base64 embed | Medium (glossy) | medallion PNGs already exist |
| 4 | **ANSI colored oracle output** (`--tty`) | ~30 LOC | Medium (terminal UX++) | `_HWPALETTE` RGB tuples |
| 5 | **Zone-grounded noise textures** in tsubuyaki sketches | ~8 LOC per sketch | High (semantic) | Seed = `zone * 7919` |
| 6 | **p5.js walker → TouchDesigner bridge** | ~2hrs build + TD wrangling | Very high (realtime) | `touchdesigner-mcp` skill |
| 7 | **Stereogram card gallery** | ~200 LOC SVG + dither | Low (skull only) | `numogram-visualizer` |

---

## Thread 1 — Medallion-as-Mask (next)

**Goal:** p5.js tsubuyaki sketches only draw inside the zone's medallion binary mask.

**Mechanism:**
- `_pixel_hash(x, y, zone)` → 10×10 binary array (0/1 per pixel)
- Pre-compute as JS literal embedded in `ZONE_DATA[zid].maskBits`
- In each p5 sketch: build a 10×10 `p5.Image`, set pixels from `maskBits`, scale × 5 → 50×50
- Apply via `drawingContext.globalCompositeOperation = 'destination-in'` + `image(medallionImg)`
- Draw the zone sketch in layer below, medallion washes it to the shape

**Why it matters:** closes the loop between `pixel-art` skill → `planchette-svg.py` medallion → tsubuyaki gallery. A single edit. Z7 (blood zone) → red-black mask; Z0 (void) → 2-pixel diamond letting only a sliver through; Z3 (C64) → color-fringed full mask.

---

## Thread 2 — Hardware-Palette Color Graft

**Goal:** Each tsubuyaki sketch draws in zone hardware palette colors.

**Mechanism:**
- Export `_HWPALETTE` from `planchette-svg.py` as JSON sidecar (`~/numogram/docs/wiki/assets/zone-palettes.json`)
- Inject `PALETTE` object into gallery script
- In each sketch: `let c = PALETTE[zid][i % PALETTE[zid].length]` instead of `random()*255`

**Zones of note:**
- Z3 (C64) → 4-color bloom
- Z7 (V-Boy) → dark red channel
- Z9 (PICO-8) → full pocket candy

---

## Medallion-animated Demon Cards (Thread 3)

**Goal:** CSS-only animation on existing demon-card medallions.

```css
/* Already have <img src="data:image/png;base64,..." class="zone-medallion" alt="Z7"> */
.zone-medallion { animation: medallion-breath 2s ease-in-out infinite; }
@keyframes medallion-breath {
  0%, 100% { filter: hue-rotate(0deg) brightness(1); opacity: .85; }
  50%       { filter: hue-rotate(45deg) brightness(1.2); opacity: 1; }
}
```

**Cost:** One CSS block injected into `demon-cards.py` → re-render. Zero JS.

---

## Oracle `--tty` mode (Thread 4)

**Goal:** ANSI 256-color escape codes during planchette output.

```python
def tty_color(r, g, b): return f"\x1b[38;2;{r};{g};{b}m"

# In generate_planchette():
print(f"  {tty_color(*ZONE_RGB[zone])}Zone {zone} — {zname}\x1b[0m")
```

Z0 → amber on black. Z7 → red. Z9 → iron/copper.

---

## Zone-grounded noise textures (Thread 5)

```javascript
// Before the main loop in a sketch:
let seed = zone * 7919;
noiseDetail(4, 0.5);
// Then: let n = noise(seed + i*dt) instead of noisemod()
```

Z0 (void) → static grain. Z5 (Atlantean hinge) → striated, two-triangle pinch. Z9 (plex) → full plenum. **2-line swap per sketch.** Pilot on Z7 first.

---

## TouchDesigner p5.js walker bridge (Thread 6)

p5.js zone-walker sketch → OSC `{'zone':3,'frame':1200}` → TD TOP shader → realtime numogram visualizer. Skill: `touchdesigner-mcp`.

Shortest path: build the p5.js sketch first (terminal works fine), verify zone transitions feel right, then drop in the MCP sender.

---

## Stereogram card gallery (Thread 7)

SVG tarot cards + a pixel-depth map = autostereogram. zone-grounded depth → pixel-art dither → base64 SVG. ~200 LOC. Low priority; fun if you have a day to kill.

---

## Execution order

**Proposed:** Thread 1 (mask) → Thread 2 (palette) → Thread 5 (noise) → Thread 3 (CSS demon cards) → Thread 4 (`--tty`) → then pause for review. Thread 6 (TD bridge) is a whole afternoon by itself; Thread 7 is an optional weekend.
