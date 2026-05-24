# Thread 6 Step 1 — p5.js Zone Walker (2026-05-25)

> Schema v3 · threads thread=6 sig=zone-walker

## What landed

`docs/wiki/assets/zone-walker.html` — standalone p5.js zone walker sketch, zero TD dependency.

### Features
| Feature | Parameter |
|---------|-----------|
| Zone count | `ZONE_NAMES.length` = 10 |
| Step algorithm | deterministic per-zone (every zone visits all 3 frames) |
| Colour source | `zone-palettes.json → ZONE_COLORS → SYNTH[1]` primary |
| Fade curve | 4-frame linear fade, `FADE_FRAMES=18` |
| Frame count | `ZONE_FRAMES=18`, `total = 72` |
| FPS target | `frameRate(60)` |
| Mode | IRQ 4 in, IRQ 4 out |

### Zone colour mapping (SYNTH[1] used as primary)

| Zone | Name | SYNTH[1] |
|------|------|---------|
| Z0 | VOID | [187,136,0] amber |
| Z1 | FIRST | [15,56,15] green |
| Z2 | DOUBLING | [85,85,85] grey |
| Z3 | ACCELERANDO | [124,124,124] chrome |
| Z4 | DELAY | [0,40,248] blue |
| Z5 | ATTENTION | [255,0,0] red |
| Z6 | ABJECTIVE | [255,0,0] red |
| Z7 | PUNCTURE | [164,0,0] blood |
| Z8 | BLOOD | [234,93,240] magenta |
| Z9 | PLEX | [29,43,83] iron |

### Files
- `docs/wiki/assets/zone-walker.html` — the sketch
- `docs/wiki/visual-layers-state-map.md` — Thread 6 section updated
- `cli/README.md` — Visual Output Layers section updated (sprites / --tty / noise)

### Next action (Thread 6 Step 2 — MCP TD Bridge)
Wait for `twozero.tox` installed + MCP port 40404 opening → td_list_instances → instantiate → createParam TOP shader.
