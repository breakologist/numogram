# Oracle Visuals — Current State (2026-05-24)

Tier 0 — Zone Pixel Glyph Planchette (`--planchette`)

## Status
**Implemented** in `oracle.py` — both `~/.hermes/skills/numogram-oracle/oracle.py` and `~/numogram/cli/oracle.py`.

## What it does
`python3 oracle.py --seed 192855 --planchette`
- Runs the normal oracle reading.
- Appends a planchette box showing:
  - Zone number, region name, DECOM particle name
  - Current, Gate target (Gt-N=Z format), Syzygy partner
  - PNG glyph path

`python3 oracle.py --base36 --text "NUMOGRAM" --planchette`
- Same, but the planchette is anchored to the **decimal attractor** (digital root of total AQ across the traversal), not the final Djynxxogram character.

`python3 oracle.py --seed 5 --planchette`
- Works in the normal decimal READING path too — planchette appears right after the reading body.

## Glyph files
All at `~/numogram/docs/wiki/assets/zone-glyphs/zone-{0-9}.png`.

### Zone design conventions (PICO-8 palette)

| Zone | Particle | Lead colour | Concept                                                              |
|------|----------|-------------|-----------------------------------------------------------------------|
| 0    | eiaoung  | black/crimson | Concentric void diamond, ring-zero                                    |
| 1    | gl       | amber       | Door / inhalation reflex, glottal gateway                             |
| 2    | dt       | red         | Imploded fricative _t_, stutter fracture, Shperer fracture angle      |
| 3    | zx       | green       | Buzzing static hiss, radial buzz-cutter spokes                         |
| 4    | skr      | cream       | Agressive reptiloid growl (hkhurrrr), ziggurat-analog mass redundancy |
| 5    | ktt      | gold/pink   | **Atlantean Hinge** — diamond constriction, two triangles pinching, gold centre thread, self-decadence golden ratio |
| 6    | tch      | navy        | Tch / dt astronomical scratches, zonal turbulence, portail-â-worm occlusions |
| 7    | bsigh    | cyan        | Lips-flap-ascent, sigh-swallow, breath-wisp trailing upward           |
| 8    | mnm       | moonlight white | Moan / pleasure-blow, three-fold blooming petals, Lukh/Shuplu spirit-diffraction |
| 9    | tn       | iron/copper | Plex grunt-peak, Iron Core, Cthellloid forty-five aperture, plutonium peak near completion — half of a ternary spoon |

### Visual tiers roadmap

| Tier | Name                      | Status    | Notes                                          |
|------|---------------------------|-----------|------------------------------------------------|
| 0    | Planchette box in reading | ✓ Live    | `--planchette` flag, terminal ASCII box        |
| 1a   | PNG glyph files (×10)     | ✓ Rendered| PICO-8 style, generator script committed       |
| 1b   | `--glyph` shell output    | TODO      | Embedding PNG in terminal (iTerm2 inline images) |
| 1c   | Zone pixel sprites (×10)  | ✓ Rendered| Floyd-Steinberg dither, ZONE_HW_PALETTE hardware palette, `zone_pixel_sprites.py`, 1.7–2.7 K each  |
|| 1d   | `--tty` / `--sprite` ANSI output | ✓ Live    | `oracle.py --tty`; per-line ANSI 256-color via `_ZONE_TTY_RGB`; `--sprite` 10×10 pixel medallion, `--tty` wraps all modes; commits 2b40674 + cda4b25 + 79fa78e |
|| 1e   | Oracle ASCII GIF          | ✓ Prototype | `oracle-ascii-video.py`: traverse zone seq → ASCII stack → tonemap → GIF; 8-frame, 582 KB; see `visual-layers-state-map.md` Thread 10a |
|| 2d   | Noise-grounded sketches   | ✓ Live    | Seed `zone * 7919`, zone-grounded Turbulence; v8 commit 2b40674  |
|| 2    | Syzygy chain SVG          | ✓ Rendered| 5 syzygy cards (1::8,2::7,0::9,3::6,4::5), `scripts/syzygy-card.py`, demo csv generation |
|| 2b   | Demon card SVG            | ✓ Rendered| 45 Pandemonium demon cards, `scripts/demon-cards.py`, per-zone/demo/--carrier filter |
|| 2c   | Planchette SVG hydration | TODO      | Full planchette spec URL→base64, frame-angle arcs, gold/indigo overlay |
| 3    | Djynxxogram planchette    | TODO      | 36-zone wheel with glyph path + reading anchor |
| 4    | Realtime canvas / p5.js Oracle Sketch | ⚡ Spec written | See `oracle-p5js-sketch-spec.md`; no TD dependency; standalone first, TD bridge once MCP 40404 live |
| 5    | Pixel-art planchette gallery | ✓ **New** | `assets/numogram-pixel-planchette-gallery.html` — 10 Floyd-Steinberg sprite cards + oracle metadata |
| 5b   | Syzygy pair gallery       | ✓ **New** | `assets/numogram-syzygy-pair-gallery.html` — 5 pair cards, dual sprites + cross-addition |
| 5c   | Pixel-art traversal GIFs  | ✓ **New** | `scripts/oracle_pixel_traversal.py` — 4 GIFs (seeds 42/137/174/666), 400×400 animated traversals |
| 5d   | Cross-palette matrix      | ✓ **New** | `scripts/cross_palette_matrix.py` — 10 zones × 28 palettes, 280 cells, `assets/matrix-cells/` |
| 6    | Tetralogue-17             | ✓ Written | [[tetralogue-17-pixel-art-labyrinth]] — palettes as bandwidth, debug path as traversal, Mesh-17 |
