# Oracle Sketch — p5.js Visualiser

> **Thread 10b** · visual-layers-state-map.md
> single-file p5.js sketch · seed-locked · zone-map palette

---

## What it is

A live, standalone p5.js canvas that renders an oracle reading as generative art.
The oracle traverse runs deterministically from a seed; the visual evolves in real
time rather than being a static image. Reload with the same seed → identical
artwork. No TouchDesigner, no build step, no server — drag into a browser and it
runs from a CDN-hosted p5.js 1.9.0.

**File:** `wiki/assets/oracle-sketch.html` · 425 lines · 16 414 bytes
(also mirrored in the export repo at `~/numogram/docs/wiki/assets/`)

---

## Controls

| Control | Behaviour |
|---|---|
| Seed input (top-right) | Integer; sets traverse determinism |
| `0`–`9` buttons | Jumps directly to that zone; triggers white flash |
| `rnd` | Random seed in range 100–99 999; updates seed input |
| `auto` | Toggles auto-advance on / off |
| `pause` / `play` | Freezes frame counter; zone still clickable |

Auto-advance period per zone: `hold = 55 + current_zone × 7 frames`
→ Z0 = 55 frames ≈ 1.8 s; Z9 = 118 frames ≈ 3.9 s at 30 fps.
The asymmetry is intentional — abyssal / hinge zones linger longer.

---

## Five sections in the draw loop

### 1 · `zone_cycle` — deterministic walker grid

A 10×5 text grid occupies the **top-left band**.
Each column = one zone (Z0–Z9 left-to-right).
Each row = a depth layer (top = surface, bottom = depth).
Glyph per cell: `· ○ ● ■ □△ ▽` chosen by modulo on column × row.

The **diagonal sweep highlight** advances one column per second at 30fps
(`t × 0.04 | 0 % 10`).
Active column is drawn at full brightness; inactive columns dim with depth.
A thin zone-name label strip sits below the grid, polarity indicator (−/+) next
to each name.
The whole band drifts ±3 px vertically via sin(t × 0.003).

**Why a grid not a ring?** The spec called for concentric traversal rings; during
implementation a depth-grid proved clinically more readable at glance — the
diagonal sweep gives a clear "zone time" readout without the occlusion that
rings impose on multi-step paths.

---

### 2 · `zone_glyph` — centred zone index

**Canvas centre.** The current zone number is rendered in 72 pt Courier New,
coloured with the zone's palette colour. Below it: the zone's song-ID in
uppercase (e.g. `EIAOUNG`, `GL`, `DT`). Below that: `Polarity · Region · Current`
line (e.g. `− POL  ·  Time-Circuit  ·  Plex CURRENT`).

The 72 pt number is the dominant visual anchor — it is the first thing the eye
registers on any frame.

---

### 3 · `sprite_pulse` — 10×10 ASCII medallion

**Bottom-right quadrant**, translucent rectangular backing, zone-colour border.
Each zone has a unique 10×10 glyph drawn from a palette of box-drawing and
Unicode block characters. Glyphs:

| Zone | Glyph character set | Visual impression |
|---|---|---|
| Z0 · Void | `·` sparse dots | star-field collapse |
| Z1 · Surge | `╭─╮` `│` `╰─╯` | box / container |
| Z2 · Dt | `░` shade blocks | noise / static |
| Z3 · Warp | `·` `°` scatter | interference pattern |
| Z4 · Sink | `⌄` chevrons descending | funnel |
| Z5 · Hinge | `╭══╗` `▓` blocks | pressure chamber |
| Z6 · Abyss | `⟦ ⟩` brackets | signal in noise |
| Z7 · Hold | `↑` arrows ascending | upward pressure |
| Z8 · Rise | `◯` `/` `\` circles | bloom / organic |
| Z9 · Plex | `╔═╗` `║` `╚═╝` `░` | gate / fortress |

**Breath pulse** — `pulse = 0.55 + 0.45 × sin(t × 0.07 + cz × 0.5)`,
alpha ∈ [0.10, 1.00]. The phase offset per zone prevents all medallions from
pulsing in lockstep. Border and glyph brightness follow the same pulse.

Zone label printed below: `SPRITE Z{cz} · {SONG_ID}`.

---

### 4 · `reading_overlay` — oracle-text card

**Bottom-right card**, translucent dark background (alpha 185), zone-colour
top-bar (3px, alpha 200).
The wrapped reading text is truncated to four lines (`wrapText()`, 26 em max
width).
Zone badge at bottom-right: `Z{cz} — {ZONE_NAME}` at 90% opacity.

Readings source: `ZONES` dict from `oracle.py`, embedded verbatim in the sketch.
No API calls — fully self-contained.

---

### 5 · `signal_trace` — right-edge wave

A thin 16-segment polyline running vertically on the **right edge** (x = width−44).
Synced to frame counter; colour = zone RGB at 35–63% alpha, breathing with
sin(t × 0.06). It is the quietest element — visible but not demanding — and
serves as the sketch's metronome.

---

## Zone colour table

Sourced from [`zone-palettes.json`](https://github.com/breakologist/numogram/blob/master/docs/wiki/zone-palettes.json)
`zone-map` palette · most-saturated RGB per era.

| Zone | Name | Era palette | RGB | Hex |
|---|:---|:---|:---|:---|
| Z0 | Void | MONO_AMBER | (255, 176, 0) | `#FFB000` |
| Z1 | Surge | GAMEBOY_ORIGINAL | (160, 207, 10) | `#A0CF0A` |
| Z2 | Dt | GAMEBOY_POCKET | (0, 0, 0) | `#000000` |
| Z3 | Warp | C64 | (64, 64, 223) | `#4040DF` |
| Z4 | Sink | ZX_SPECTRUM | (0, 252, 254) | `#00FCFE` |
| Z5 | Hinge | APPLE_II_HI | (255, 0, 255) | `#FF00FF` |
| Z6 | Abyss | TELETEXT | (255, 0, 0) | `#FF0000` |
| Z7 | Hold | GAMEBOY_VIRTUALBOY | (239, 0, 0) | `#EF0000` |
| Z8 | Rise | APPLE_II_LO | (0, 168, 241) | `#00A8F1` |
| Z9 | Plex | PICO_8 | (255, 0, 77) | `#FF004D` |

Every RGB triplet in the sketch is sourced from this table — no arbitrary values.

---

## Implementation notes

### Traverse engine (in-browser JS)

The `traverse(s, n)` function in the sketch is a JS re-implementation of the
same digit-decomposition logic used by `oracle.py`:
`next_zone = (zone + step) % 10` where `step ∈ {1, 2, 3}` derived from
`seed % 10` (1→3: three zones per step, 4→7: two, 8→9: one).
The browser traverse produces the same zone sequence as the Python oracle for
the same seed.

### Sprite glyphs

All 10 glyphs are hand-designed Unicode 10×10 grids embedded directly in the
HTML. They were derived by cross-referencing:
1. `planchette --sprite` output (ASCII `U+2588` block grid),
2. `tsubuyaki-oo-gallery` sprite patterns (medallion masks),
3. zone-palette era character-set restrictions (e.g. Z2 uses only `░`,
   Z6 uses only bracket characters).

### Spec vs implementation

The [design spec](oracle-p5js-sketch-spec.md) was written before implementation.
Two meaningful departures:

| Spec called for | Implemented as | Reason |
|---|---|---|
| Concentric ring zone-cycle | 10×5 depth grid | Ring occlusion at 10 zones; grid is scannable at a glance |
| planchette V-octagon glyph (poly vertex) | Large centred zone index | Text readout is more informative; polygon reserved for future sprite-morph |
| `tty_colours` background field | `signal_trace` right-edge wave | Panel background tint proved visually muddy; trace serves as metronome instead |

All other sections map one-to-one or close enough that the spec sections
remain valid documentation.

---

## File locations

| Location | Path |
|---|---|
| Vault (authoritative) | `~/.hermes/obsidian/hermetic/wiki/assets/oracle-sketch.html` |
| Export (public) | `~/numogram/docs/wiki/assets/oracle-sketch.html` |
| Design spec | `wiki/oracle-p5js-sketch-spec.md` |
| Zone palette JSON | `~/numogram/docs/wiki/zone-palettes.json` |
| State map (Thread 10b) | `wiki/visual-layers-state-map.md` |

---

## Cross-references

- [[visual-layers-state-map]] — master thread registry, zone-layer table, bug log
- [[oracle-p5js-sketch-spec]] — original design spec (pre-implementation)
- [[oracle-visual-ideas]] — tier-ranked visual-layer backlog
- [[zone-palettes]] — canonical palette reference, most-saturated-per-era rule
- [[numogram-visualizer-v7]] — SVG visualizer; the precursor that inspired this sketch
- [[tsubuyaki]] — generative p5.js tweet-length sketches (sibling idiom)
