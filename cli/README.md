# CLI Tools

## oracle.py
Complete divination pipeline — seed → zone → syzygy → current → gate → reading → voice.
Now with Djynxxogram (base-36) traversal mode.

### Standard modes:
- `--seed N` — numeric seed
- `--text "phrase"` — AQ-derived seed (A=10..Z=35)
- `--hardware` — local entropy (12 hardware sources)
- `--random` / `--blockchain` / `--earthquake` — external APIs
- `--iching` — I Ching hexagram casting
- `--iching --seed N` — hexagram from specific seed
- `--taixuan` — T'ai Hsuan two-tetragram oracle
- `--taixuan --seed N --voice` — tetragrams with zone sound
- `--synx "TEXT"` — dual-cipher mode (AQ + Synx/Yxshh)
- `--traverse N` — numogram zone path traversal
- `--voice` — generate audio via formant synthesis

### Djynxxogram mode (v1.2.0):
- `--base36 --text "WORD"` — per-character traversal through all 36 zones
- `--djynxxogram --seed N` — seed → hex → Djynxxogram traversal
- `--compare --text "WORD"` — cross-base comparison (10/16/22/26/36)

### What --base36 shows per character:
Character → AQ value → Djynxxogram zone (0-35) → syzygy partner → current → gate (triangular number → mod-36 target) → decimal attractor → region (OUTER if zone 0 or Z)

### Zone naming:
Zones 10-35 use letter-native names (A=Aya, B=Buh, C=Kuh... Z=Zuh). Combinatorial quasiphonic particles (Amy Ireland's method) also computed via digit-decomposition of the 10 canonical phonemes.

### Companion tool:
`../numogram-base-explorer.py` — multi-base numogram constructor supporting any base N (2-36). Computes syzygy/gate/current/region tables, decimal projection clusters, DOT graph output.

## aq_calculator_canonical.py
Verified canonical AQ calculator. Tests: AQ=36, CODE=63, HYPERSTITION=286, NUMOGRAM=174, CCRU=81.

## philosophies.md
Zone descriptions and oracular phrases for voice generation.

## Planchette Channel (Tier 2c)

`oracle.py --planchette` prints a fixed-width ASCII card per zone:
  ╔══════════════════════════════════════════════════╗
  ║   ZONE N — REGION        [ PARTICLE ]             ║
  ╠══════════════════════════════════════════════════╣
  ║   Current: C   Gate: Gt-N(=Z?)   Syzygy: a::b     ║
  ║   PNG: path/to/assets/zone-N.png                  ║
  ╚══════════════════════════════════════════════════╝

`--planchette --ascii-glyph` draws the zone box-art Unicode card
instead of the ASCII header block (tube-ASCII frame + particle sigil +
gate-arc ring + reading verse).  Assets: `wiki/assets/planchette-glyphs/`.

`--planchette --json` emits a single-line JSON dict (no human text)
for pipe consumption by `planchette-svg.py --stdin`.

Schema: {"zone","name","region","particle","polarity","current","gate",
         "gate_raw","gate_loops","gate_history","syzygy","reading"}

Gate-loop depth: `gate_loops` is the number of plex-reduction iterations
needed to collapse `gate_raw` (= triangular sum) to a single digit:

 gate | raw | loops | history
 -----|-----|-------|--------
  Z1  |  1  |  0    | []           Z3  |  6  |  0    | []
  Z2  |  3  |  0    | []           Z4  | 10  |  1    | [1]
  Z5  | 15  |  1    | [6]          Z6  | 21  |  1    | [3]
  Z7  | 28  |  2 🔁 | [10,1] ⬅ only multi-loop
  Z8  | 36  |  1    | [9]          Z9  | 45  |  1    | [9]

JSON endpoint: `oracle.py --seed N --planchette --json` → single-line
object on stdout. No reading text mixed in. Suitable for piping directly
into `planchette-svg.py --stdin`.
## Visual Output Layers

### Zone pixel sprites (`zone_pixel_sprites.py`)

Generates hardware-authentic zone glyph sprites using Floyd-Steinberg dithering and
the `ZONE_HW_PALETTE` map from `planchette-svg.py`.

```bash
python3 cli/scripts/zone_pixel_sprites.py          # all 10 zones
python3 cli/scripts/zone_pixel_sprites.py 3 7 9    # specific zones
python3 cli/scripts/zone_pixel_sprites.py --no-pixel   # source only, no dither
```

| Zone | Palette          | Colors | Block |
|------|------------------|--------|-------|
| Z0   | MONO_AMBER       | 2      | 6     |
| Z1   | GAMEBOY_ORIGINAL | 4      | 8     |
| Z2   | GAMEBOY_POCKET   | 4      | 8     |
| Z3   | C64              | 16     | 8     |
| Z4   | ZX_SPECTRUM      | 8      | 10    |
| Z5   | APPLE_II_HI      | 6      | 10    |
| Z6   | TELETEXT         | 8      | 10    |
| Z7   | GAMEBOY_VIRTUALBOY | 4    | 8     |
| Z8   | APPLE_II_LO      | 16     | 10    |
| Z9   | PICO_8           | 16     | 6     |

Output: `docs/wiki/assets/zone-sprites/zone-N-sprite.png` (+ `zone-N-source.png`).

**Bug fix:** Zones not in `pixel_art.PRESETS` (Z1, Z4, Z5, Z7, Z8, Z9) fall back to
`preset='c64'` for enhancement tuning, then pass `palette=<UPPERCASE_PALETTE_NAME>`
as a `**override` kwarg — merged as `{**PRESETS[preset], **overrides}` inside `pixel_art()`.

### `--tty` ANSI colored oracle output

```bash
python3 oracle.py --seed 192855 --planchette --tty
```

Colours every planchette line with a per-zone ANSI 256-color escape derived from the
`_ZONE_TTY_RGB` dict.  Verified with `cat -v`.  Zone colours:

| Zone | RGB         |
|------|-------------|
| Z0   | (222,180,16) amber  |
| Z3   | (124,124,124) silver|
| Z7   | (220,0,0) blood-red |
| Z9   | (60,30,0) iron      |

### Zone-grounded noise textures (tsubuyaki sketches)

In sketch JavaScript, replace `noise(x,y)` with a zone-locked noise function:

```javascript
let _z_seed = zone * 7919;   // prime multiplier = non-overlapping seed
noiseDetail(4, 0.5);
let n = noise(_z_seed + i * dt);
```

Each zone gets a unique noise character.  Landed in tsubuyaki v7.2/v8 commit `2b40674`.




