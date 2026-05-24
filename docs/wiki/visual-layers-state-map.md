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
| Tsubuyaki v6 gallery | p5.js HTML | `numogram-tsubuyaki-v6.html` | ⚠️ Superseded by v7 — eval-based init broken |
| Tsubuyaki v7 gallery | p5.js HTML | `numogram-tsubuyaki-v7.html` | ✓ Working — all 10 canvases, MASK_DATA + masked eval |
| Planchette v1/v2 SVG | `planchette-svg.py` | `planchette-svg.py` | ✓ Frame-angle arcs, gold/indigo overlay |

---

## Porous Layers (implemented-ish, not surfaced)

| Layer | Block |
|---|---|
| `--glyph` inline PNG | `oracle.py` → `--glyph` flag TODO; needs iTerm2 inline image protocol |
| SVG planchette hydration (Tier 2c) | Full spec URL→base64 + gold/indigo frame-angle arcs; partially done in v1/v2 |
| Djynxxogram wheel (Tier 3) | `--planchette --djynxxogram` — 36-zone wheel with glyph path; not coded yet |
| p5.js realtime canvas (Tier 4) | Need to solve TUI 503 before visual QA of v7 gallery |

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

## Ranked Threads (effort × payoff, updated 2026-05-24)

| # | Thread | Effort | Payoff | Status | Commit |
|---|---|---|---|---|---|
| 1 | **Medallion-as-mask** on tsubuyaki canvases | ~15 LOC + v6 patch | High (visible) | ✓ DONE | cdc6938 |
| 2 | **Hardware-palette color graft** into tsubuyaki sketches | ~20 LOC + JSON sidecar | High — ties 3 skills | ✓ DONE | 306a2e6 |
| 3 | **CSS-animated demon cards** (medallion `@keyframes`) | ~40 LOC CSS + base64 | Medium (glossy) | ✓ DONE | 306a2e6 |
| 4 | **ANSI colored oracle output** (`--tty`) | ~30 LOC | Medium (terminal UX++) | ⏳ Pending | — |
| 5 | **Zone-grounded noise textures** in tsubuyaki sketches | ~8 LOC per sketch | High (semantic) | ⏳ Pending | — |
| 6 | **p5.js walker → TouchDesigner bridge** | ~2hrs build + TD wrangling | Very high (realtime) | ⏳ Pending | — |
| 7 | **Stereogram card gallery** | ~200 LOC SVG + dither | Low (skull only) | ⏳ Pending | — |

---

## Thread 1 — Medallion-as-Mask ✓ DONE

**Goal:** p5.js tsubuyaki sketches only draw inside the zone's medallion binary mask.

**Mechanism:**
- `_pixel_hash(x, y, zone)` → 10×10 binary array (0/1 per pixel)
- Pre-computed as `MASK_DATA` JS constant (2102 chars) embedded before ZONE_DATA init
- Each draw cycle: `getImageData(0,0,10,10)` → modulate alpha (`d[i*4+3]`) per mask bit → `putImageData`
- No p5.image/mask API needed — direct Canvas 2D, 1-frame lag-tolerant

**v7 diff:** combined two `<script>` blocks into one, injected `MASK_DATA`, replaced `eval(ZONE_DATA[zid])` with wrapped IIFE.

**Zones visible:**
- Z0 (void): 55% opaque — very sparse diamond
- Z7 (blood): 58% opaque — largest blood-mask bite
- Z9 (plex): 63% opaque — most visible

**File:** `numogram-tsubuyaki-v7.html` (13,517 bytes, commit cdc6938)

---

## Thread 2 — Hardware-Palette Color Graft ✓ DONE

**Goal:** Each tsubuyaki sketch draws in zone hardware palette colors.

**Mechanism:**
- Exported `_HWPALETTE` + `ZONE_HW_PALETTE` as `zone-palettes.json`
- Injected into tsubuyaki gallery as `PALETTE[zid] → [[r,g,b], …]`
- Patches tsubuyaki sketches: `fill(PALETTE[zid][i % n][0], …)` instead of `random()*255`

**Zones of note:**
- Z3 (C64) — 4-color bloom
- Z7 (V-Boy) — dark red channel
- Z5 (APPLE_II_HI — 5 colors; Z8 APPLE_II_LO — 4 colors)

**Sidecar:** `docs/wiki/assets/zone-palettes.json` (4,445 bytes, commit 306a2e6)

---

## Thread 3 — CSS-Animated Demon Cards ✓ DONE

**Goal:** CSS-only animation on existing demon-card medallion images.

**Mechanism:**
- Injected `@keyframes med--zone-medallion` into each card's `<defs>` block
- Added `style="animation:med--zone-medallion 2s ease-in-out infinite"` to every medallion `<image>` tag
- Zero JS, no re-render of pngs

**Snippet applied:**
```css
@keyframes med--zone-medallion{
  0%{opacity:.88;filter:hue-rotate(0deg)}
  50%{opacity:1;filter:hue-rotate(30deg)}
}
```

**File:** `scripts/demon-cards.py` (11,463 bytes, commit 306a2e6) — `--demo` renders cleanly (exit 0).

---

## Oracle `--tty` mode (Thread 4)

**Goal:** ANSI 256-color escape codes during planchette output.

```python
def tty_color(r,g,b): return f"\x1b[38;2;{r};{g};{b}m"
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
// Then: let n = noise(seed + i*dt) instead of standard noise()
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

**Done:** Thread 1 (mask) ✓ → Thread 2 (palette) ✓ → Thread 3 (CSS demon cards) ✓
**Next:** Thread 5 (noise) → Thread 4 (`--tty`) → Thread 6 (TD bridge, TUI first)
**Parked:** Thread 7 (stereogram — weekend project)
