|---
title: Visual Layers — State Map & Thread Ranking (2026-05-24)
created: 2026-05-24
updated: 2026-05-25
status: active
category: reference
tags: ["visual", "oracle", "tsubuyaki", "p5js", "pixel-art", "ascii-video", "medallion", "planchette"]
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
| `--tty` ANSI oracle output | `oracle.py --tty` | `oracle.py` L80-85 / L23097 | ✓ v1 |
| Tsubuyaki v7 gallery | p5.js HTML | `numogram-tsubuyaki-v7.html` | ✓ Working — all 10 canvases, MASK_DATA + masked eval |
| Planchette SVG v1/v2 | `planchette-svg.py` | `planchette-svg.py` | ✓ Frame-angle arcs, gold/indigo overlay |
| Noise-grounded sketches | p5.js | tsubuyaki sketches | ✓ v8 commit — seed = zone × 7919 |
|| **Pixel-art zone sprites** | `zone_pixel_sprites.py` | `assets/zone-sprites/zone-N-sprite.png` | ✓ All 10 zones done |
|| **Oracle ASCII GIF** | `oracle-ascii-video.py` | `/tmp/oracle_{seed}.gif` | ✓ Prototype — 8-zone traverse → coloured ASCII stack, tonemap+encode, commit pending |

---

## Porous Layers (implemented-ish, not surfaced)

| Layer | Block |
|---|---|
| `--glyph` inline PNG | `oracle.py` → `--glyph` flag TODO; needs iTerm2 inline image protocol |
| SVG planchette hydration Tier 2c | Full spec URL→base64 + gold/indigo frame-angle arcs; partially done in v1/v2 |
| Djynxxogram wheel | `--planchette --djynxxogram` — 36-zone wheel with glyph path; not coded yet |
| p5.js realtime canvas QA | TUI 503 blocks browser_vision; work via execute_code/terminal |

---

## Known bugs (2026-05-25)

| Bug | Status |
|---|---|
|| Z0 medallion: 16 colors (expected 2, MONO_AMBER) | `_HWPALETTES` fallback path; **FIXED** (commit 79fa78e) |
|| Z5 medallion: 6 colors (expected 16, APPLE_II_LO) | Same fallback path; **FIXED** (commit 79fa78e) |
| TUI 503 | `nousresearch/openrouter` Step 3.5 Flash OAuth failure — blocks all TUI requests; workarounds: `execute_code` / `terminal` |

---

## Ranked Visual Threads (effort × payoff)

| # | Thread | Effort | Payoff | Status |
|---|---|---|---|---|
| 1-5 | Medallion-as-mask / palette / CSS demon cards / --tty / noise | past | High | ✓ A set |
| 6 | p5.js walker → TouchDesigner OSC bridge | ~2hrs | Very high (realtime scrying) | ⏳ Next |
| 7 | Stereogram card gallery | ~200 LOC | Low (skull only) | ⏳ Weekend |
| 8 | Pixel-art zone sprites | ~30 LOC gen script | Medium — hardware-authentic | ✓ Done |
|| 10a | Oracle ASCII GIF / ascii-video pipeline | ~80 LOC prototype | Medium — zone traversal as live ASCII cinema | ✓ Prototype |
|| 10b | p5.js Oracle Sketch | complex | High — interactive planchette-reading rendering | ⚡ `oracle-p5js-sketch-spec.md` written |
---
+

+## Thread 10a — Oracle ASCII GIF ✓ Prototype
+
+**Goal:** map `oracle.py --traverse` zone sequence → ASCII frame-per-step → animated GIF.
+
+**Prototype:** `~/numogram/cli/oracle-ascii-video.py` (6 KB, 0 external deps beyond numpy + pillow)
+
+| Parameter | Value |
+|-----------|-------|
+| Frames | 1 per zone step (`traverse(seed, 8)`) |
+| Resolution | 720×400 px @ 1 fps |
+| Grid | ~50×28 fixed cells, size-11px monospace |
+| Colour | `oracle._ZONE_TTY_RGB` per zone; luminance↔field |
+| Glyph | 10 `CHAR_RAMPS` dicts, one per zone |
+| Tonemap | Percentile-based, 1%/99.5%, gamma 0.75 |
+| ENCODE | Pillow `save_all=True`, optimize GIF |
+
+**Confirmed output:** 8-frame, 582 KB, rc=0. Frame 0 = Z3_Warp bracket-dense gold on dark. Frame 4 = Z8_Lullaby diamond chars in purple. Zones visually distinguishable.
+
+### Entry points
+| Mode | Command | Status |
+|------|---------|--------|
+| A — Traverse → GIF | `python3 oracle-ascii-video.py 174 out.gif` | ✓ Working |
+| B — TTS WAV → audio-reactor | `oracle.py --voice text → WAV` → ascii-video audio mode | ⬜ TTS deps absent (pydub, soundfile) |
+| C — sys.stdin pipe | `oracle.py --traverse 174 --json \| ascii-video stdin→frames` | ⬜ pipe path untested |
+
+### Gap vs full ascii-video spec
+- Stage 5 SHADER → `FeedbackBuffer` + `ShaderChain` (vignette, grain, bloom)
+- Audio-analysis stage (pydub/ffmpeg FFT)
+- Parallel frame rendering
+- Scene dispatcher / section-based editing
+- sys.stdin pipe (Mode C)
+
+---
+
+## Thread 10b — p5.js Oracle Sketch ⚡ Spec Written
+
+**Status:** Design brief only — not yet implemented.
+See `oracle-p5js-sketch-spec.md` for full spec.
+
+Five sections in the sketch loop:
+1. **`zone_cycle`** — deterministic walker with seed-locked noise; zone ring + path lines
+2. **`zone_glyph`** — V-shaped octagon glyph inspired by planchette glyph encoding
+3. **`sprite_pulse`** — 10×10 pixel medallion, breath-scaling at `t = sin(freq*t)`
+4. **`reading_overlay`** — oracle planchette text composited with zone-tint alpha
+5. **`tty_colours`** — field gradients mapped to `_ZONE_TTY_RGB` tuples; smooth interp on zone change
+
+Priority: standalone first (no TD MCP dep); TD bridge comes once MCP port 40404 is live.
+
+---
+
 ## Thread 1-2 — Medallion-as-mask + Palette Graft ✓ DONE

**Docs:** `references/medallion-mask-and-palette-graft.md`

**Goal:** p5.js tsubuyaki sketches draw inside zone medallion binary mask, using zone hardware palette.

**Mechanism:**
- `_pixel_hash(x, y, zone)` → 10×10 binary array → pre-computed `MASK_DATA` JS constant (2102 chars)
- Each draw cycle: `getImageData` → modulate alpha per mask bit → `putImageData`
- Palette graft: `zone-palettes.json` sidecar → `PALETTE[zid]` injected into gallery JS

**Commits:** cdc6938, 306a2e6

---

## Thread 3 — CSS-Animated Demon Cards ✓ DONE

**Goal:** CSS-only hue-rotate + opacity animation on medallion images.

**Mechanism:**
```css
@keyframes med--zone-medallion{
  0%{opacity:.88;filter:hue-rotate(0deg)}
  50%{opacity:1;filter:hue-rotate(30deg)}
}
```
Injected into every demon-card `<defs>` block, applied to every medallion `<image>`.

**File:** `scripts/demon-cards.py` (11,463 bytes), commit 306a2e6.

---

## Thread 4 — ANSI colored oracle output ✓ DONE

**Goal:** `oracle.py --tty` emits per-line ANSI 256-color escapes on the planchette channel.

```python
def tty_color(r,g,b): return f"\x1b[38;2;{r};{g};{b}m"
_ZONE_TTY_RGB = {
    0:(222,180,16), 1:(140,180,40), 2:(70,160,40),
    3:(124,124,124), 4:(210,100,230), 5:(0,130,180),
    6:(200,200,200), 7:(220,0,0), 8:(100,100,80), 9:(60,30,0),
}
```

Each planchette line wrapped individually; `\x1b[0m` resets per line. Confirmed via `cat -v`.

**Commit:** 2b40674.

---

## Thread 5 — Zone-grounded noise ✓ DONE

```javascript
let _z_seed = zone * 7919;   // prime multiplier gives non-overlapping seed per zone
noiseDetail(4, 0.5);
let n = noise(_z_seed + i * dt);
```

Z0 (void) → static grain. Z5 (Atlantean hinge) → striated, two-triangle pinch. Z9 (plex) → full plenum. 2-line swap per sketch.

**Commit:** 2b40674 (v8).

---

## Thread 6 — p5.js walker → TouchDesigner OSC bridge

**Goal:** Real-time audio-visual scrying loop. p5.js sketch walks zones deterministically → sends OSC `{'zone':N,'frame':M}` → TD TOP shader resizes/warps → realtime numogram visualizer.

### Step 1 — Zone-walker sketch ✓ DONE (2026-05-25)

`docs/wiki/assets/zone-walker.html` — standalone p5.js HTML, no TD dependency.  
Features: 10-zone cycle (Z0→Z9), 1.5 s per zone, 0.3 s fade between zones, per-zone RGB SYNTH swatches, frame counter.  
Zone colour source: `zone-palettes.json` → `ZONE_COLORS` dict → `SYNTH[1]` (primary lead), `SYNTH[0]` (dark base).

### Step 2 — MCP TD bridge ⏳ BLOCKED

twozero MCP still requires: (1) `twozero.tox` in TD project, (2) MCP enabled in twozero settings (auto-start=Yes), (3) port localhost:40404 responding to `GET /mcp`.  
Port 40404: not open. TD (PID 947426) is running under Wine but MCP is not yet live.  
Next action pending TD setup completion.

**Minimum viable overall:** zone transitions → zone-constrained per-step render → MCP hook → TD TOP shader.  
**Shortest path:** Step 1 ✓ → MCP → TD oscillator → 10-zone demo loop.

## Thread 7 — Stereogram card gallery ⏳ Weekend

SVG tarot cards + pixel-depth map → autostereogram. zone-grounded depth → pixel-art dither → base64 SVG. ~200 LOC.

---

## Thread 8 — Pixel-art Zone Sprites ✓ Done (2026-05-25)

**Goal:** Generate hardware-authentic zone glyph sprites using ZONE_HW_PALETTE zone→palette mapping from planchette-svg.py.

**Script:** `~/numogram/cli/scripts/zone_pixel_sprites.py` (~200 LOC)  
**Output:** `~/numogram/docs/wiki/assets/zone-sprites/`

All 10 zones generated with Floyd-Steinberg dithering:

| Zone | Palette | Block | Sprite size |
|---|---|---|---|
| Z0 | MONO_AMBER (2 color) | 6 | 2.3K |
| Z1 | GAMEBOY_ORIGINAL (4) | 8 | 2.2K |
| Z2 | GAMEBOY_POCKET (4) | 8 | 2.4K |
| Z3 | C64 (16) | 8 | 1.7K |
| Z4 | ZX_SPECTRUM (8) | 10 | 2.1K |
| Z5 | APPLE_II_HI (6) | 10 | 1.7K |
| Z6 | TELETEXT (8) | 10 | 1.8K |
| Z7 | GAMEBOY_VIRTUALBOY (4) | 8 | 2.2K |
| Z8 | APPLE_II_LO (16) | 10 | 2.2K |
| Z9 | PICO_8 (16) | 6 | 2.7K |

**Bug fix:** zonal zones without a direct PRESETS entry (Z1, Z4, Z5, Z7, Z8, Z9) fell back to `preset='c64'` for the enhancement curve, then passed `palette=<UPPERCASE>` as a kwarg override past the preset lookup. `pixel_art()` merges `{**PRESETS[preset], **overrides}` — palette string overrides the preset's default palette before processing.

**Also generated:** `zone-N-source.png` (256×256 programmatic zone glyphs) alongside each sprite.

---

## TouchDesigner p5.js walker bridge (Thread 6 detail)

Build in this order:
1. p5.js zone-walker sketch (terminal, no TD) — verify deterministic zone transitions feel right
2. MCP OSC sender wired to skill (36 tools: createParam, set, cookFrom, exec / cook Parm)
3. TD reader patch: zone → R/GB shader mult → vis field
