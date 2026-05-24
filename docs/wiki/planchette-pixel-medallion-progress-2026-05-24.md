# Planchette Pixel-Art Medallion — Session Progress 2026-05-24

> Quick at-a-glance: what landed, what we found, what's next.

## What Shipped

### Palette layer in `planchette-svg.py`
- **`ZONE_HW_PALETTE`** map: each of the 10 zones gets a distinct hardware-accurate palette from the `pixel-art` skill
- **`_HWPALETTES`** loaded at runtime via `importlib.util` from `~/.hermes/skills/creative/pixel-art/scripts/palettes.py`
- **`_hw_palette()`** fallback synth for when the skill file is absent
- **`_pixel_color(zone, x, y)`** — picks colour per pixel position using `(x*(zone+1) + y*(zone+2)) % n` index into the palette

### Zone → Palette mapping

| Zone | Palette | Colors | Notes |
|------|---------|--------|-------|
| Z0 Void | MONO_AMBER | 2 | Eiaoung amber-on-black |
| Z1 Hold | GAMEBOY_ORIGINAL | 4 | Classic green |
| Z2 Sink | GAMEBOY_POCKET | 4 | Grayscale |
| Z3 Ascend | C64 | 16 | Full C64 palette |
| Z4 Descend | ZX_SPECTRUM | 8 | Bright spectrum clash |
| Z5 Reduce | APPLE_II_LO | 16 | Lo-res Apple II |
| Z6 Increase | TELETEXT | 8 | BBC teletext |
| Z7 Warp | GAMEBOY_VIRTUALBOY | 4 | Deep red only |
| Z8 Tremble | MSX | 15 | MSX-1 colour set |
| Z9 Rapture | PICO_8 | 16 | PICO-8 fantasy |

### Verified pixel counts

All 10 zones render as 10×10 medallion PNGs embedded in the SVG:

| Zone | Unique colors in medallion |
|------|--------------------------|
| Z0 | **16** ⚠️ *(MONO_AMBER loaded — investigate fallback)* |
| Z1 | 5 (correct, GAMEBOY_ORIGINAL) |
| Z2 | 4 (correct) |
| Z3 | 16 (correct, C64 full palette) |
| Z4 | 8 (correct) |
| Z5 | 6 *(APPLE_II_LO = 16 colors expected — shortfall, see below)* |
| Z6 | 8 (TELETEXT = 8, correct) |
| Z7 | **4** ✅ Game Boy Virtual Boy deep reds — exactly right |
| Z8 | 15 (MSX = 15, correct) |
| Z9 | 16 (PICO_8 = 16, correct) |

### Known issues
- **Z0 shows 16 colors** — MONO_AMBER has only 2, but Z0 medallion is currently sampling from PICO_8 (which also maps to zone 0 through fallback path). Likely `_HWPALETTES` returning PICO_8 instead of MONO_AMBER, or palette conflict after reload.
- **Z5 shows 6 colors vs expected 16** — need to check if APPLE_II_LO is loading correctly or if the position-hash is simply concentrating in a narrow band.

## Skills touched
- `creative/pixel-art` — PALETTES table inspected; all 28 keys enumerated; zone→palette map drafted
- `numogram-oracle` — bumped to **v1.2.3-dev** for this session's work
- `planchette-json-format.md` — new wiki page documenting the JSON schema

## Value unlocked
- Every planchette card now carries a **unique numogram-native pixel signature** per zone — not decorative, but indexable: palette → current → gate → colour count
- Opens the door to: pixel-art tsubuyaki (gallery per zone), MIR ↔ palette mapping (centroid → hardware palette), and a future **pixel glyph → audio** transcode layer

## Pending / Next session
- [ ] Fix Z0 / Z5 palette shortfall — verify `_HWPALETTES` import once for all zones  
- [ ] `_pixel_hash` upgrade: swap geometric hash for a real zone-shaped glyph (spiral, glyph, cross — matches `--ascii-glyph` output shape)
- [ ] Tsubuyaki pixel gallery: generate one p5.js sketch per zone, each rendering the medallion palette live
- [ ] `planchette-gallery` subdirectory cleanup — currently has `planchette-gallery/planchette-gallery/` nest
- [ ] Pixel-medallion as audio-visual transducer: zones 3/7/9 as spectrogram palettes in TouchDesigner
- [ ] Wiki pages for every palette key (`pico-8.md`, `zx-spectrum.md`, etc.) — zone→palette references
