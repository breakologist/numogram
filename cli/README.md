# CLI Tools

## oracle.py
Complete divination pipeline — seed → zone → syzygy → current → gate → reading → voice.
Now with Djynxxogram (base-36) traversal mode.

### Standard modes:
- `--seed N` — numeric seed
- `--text "phrase"` — AQ-derived seed (A=10..Z=35)
- `--hardware` — local entropy (12 hardware sources + external)
- `--random` / `--blockchain` / `--earthquake` — external APIs
- `--iching` — I Ching hexagram casting (delegates to sibling iching.py)
- `--iching --seed N` — hexagram from specific seed
- `--taixuan` — T'ai Hsuan two-tetragram oracle (delegates to taixuan.py)
- `--taixuan --single` — single tetragram (best for 9 zan/appraisals)
- `--taixuan --em-stats` — Em-profile for the cast
- `--geomancy` — geomantic shield + house chart (delegates to geomancy.py; all its flags pass through, e.g. `--seed`, `--hardware`, `--json`, `--house`)
- `--synx "TEXT"` — dual-cipher mode (AQ + Synx/Yxshh)
- `--traverse N` — numogram zone path traversal
- `--taixuan` also takes `--unicode`, `--full`, `--voice`, `--hardware`, `--zone-from value|number`, `--netspan`
- `--iching` also takes `--full`, `--method flat|coins|yarrow`, `--zone-method fuxi|kw|curated`
- `--path legacy|hash` — zone path in readings. `legacy` (default) is `n → n·zone + 1`, which always falls into 2 → 5 → 8 within three steps; `hash` derives each step from SHA-256(seed:k)
- `--voice` — zone sound (standard readings) or oracle sentences (`--taixuan`); not wired for `--iching`

**Power-user examples**
```bash
# Hardware-entropy single Tai Xuan with unicode + appraisals + Em stats
python oracle.py --taixuan --single --full --unicode --hardware --em-stats

# I Ching yarrow cast with full relating + JSON for agents
python iching.py --cast --full --json

# Tai Xuan two-tetragram with Em analysis and visualizer export
python taixuan.py --taixuan --em-stats --viz-json

# Rich oracle with voice (T'ai Hsuan)
python oracle.py --taixuan --full --voice --seed 42

# Pure hardware bytes → feed anywhere (the tool prints hex; --seed needs a number:
# oracle.py takes decimal only, iching.py/taixuan.py also accept 0x-hex)
python .hermes/skills/numogram-oracle/hardware_entropy.py --bytes 4 | \
  xargs -I {} bash -c 'python oracle.py --seed $((16#{}))'
# (the code itself looks for ~/.hermes/tools/hardware_entropy.py, or one next to taixuan.py)

# Yuandong 27-phase cast (prints phase, Chinese name, formula, trits; no hierarchy view)
python taixuan.py --phase

# Cross-tool pipeline (hardware seed → I Ching + Tai Xuan)
SEED=0x$(python .hermes/skills/numogram-oracle/hardware_entropy.py --bytes 4)
python iching.py --iching --seed $SEED --full
python taixuan.py --taixuan --seed $SEED --single --full --unicode

# Full ritual stack (hardware → Tai Xuan single + voice)
python oracle.py --taixuan --single --full --unicode --voice --hardware
```

See also: `iching.py` (standalone, highly enhanced)
  python3 iching.py --iching
  python3 iching.py --iching --seed 192855 --json
  python3 iching.py --cast                 # yarrow simulation (traditional probs)
  python3 iching.py --cast --seed N
  python3 iching.py --cast --coins         # three-coin odds (1/8, 3/8, 3/8, 1/8)
  python3 iching.py --iching --method yarrow --zone-method kw   # sequence-number zone

Line odds: `--iching` uses `byte % 4` by default (each of 6/7/8/9 = 1/4; not a traditional method). `--method coins|yarrow` and `--cast` give the traditional odds (yarrow 1/16, 5/16, 7/16, 3/16).
Zones (default = **line values** in both iching.py and taixuan.py): `fuxi` (default) = line value mod 9 (line k weighs 2^(k−1) ≡ 1,2,4,8,7,5; Kun → Zone 0, the other 7 doubled hexagrams → 9, complements are syzygy partners); `kw` = digital root of the King Wen number (sequence convention); `curated` = table.csv zone if present, else KW digital root (the pre-review default). Both KW and line-value zones are always printed.
Hexagram identification uses a built-in King Wen table; the corpus supplies names/judgments only (its `binary` field is written top line first).

Pulls from table.csv (18 curated numogram resonances with insights), yijing-expansion-v1.1.md (yarrow probs 6/7/8/9, line-gates Gt-01 etc.), tianmu-yijing-corpus.json (full 64 names + judgments).

New: pre/post (relating) hex for changing lines, per-line transitions + gates, judgments in output, all 64 names.

See also: `taixuan.py` (standalone, richly enhanced)
  python3 taixuan.py --taixuan
  python3 taixuan.py --taixuan --seed 192855 --full
  python3 taixuan.py --single --full --unicode
  python3 taixuan.py --single --em-stats
  python3 taixuan.py --phases
  python3 taixuan.py --phase
  python3 taixuan.py --taixuan --viz-json

Pulls 81 tetragram names (Nylan), 9 zan/appraisals (placeholder labels, not Nylan's texts), Yuandong 27-phase "departments" (pu), full 3-9-27-81 hierarchy, Em/mediation stats, alchemy layer (Sulfur/Heaven, Salt/Earth, Mercury/Man-Em), quasiphonic demon-name sketches, and numogram zone/syzygy/demon mapping.

Sourcing: Heaven/Earth/Man line types and the 3-9-27-81 hierarchy are in the sources (Nylan; Liu, JPACT 2021). "Em", the alchemy layer, the appraisal phase names and the quasiphonic names are this project's own additions. The 27 phases are the figures of the *Dongji zhenjing* 洞極真經 (attributed to Guan Lang 關朗, courtesy name Ziming; three groups 生 birth / 育 nurture / 資 material × 9). Treating them as the Tai Xuan's 27 departments is this tool's mapping. The `formula` strings are unverified (only 20 of the 27 are distinct).
Tetragrams are shown by head number 1–81. Zone: `--zone-from value` (default; same line-value convention as iching.py `fuxi`) = digital root of the base-3 line value (Centre → 0); `--zone-from number` = digital root of the head number (sequence convention, 9 heads per zone 1–9). Demons: syzygy carrier only by default; `--netspan` names the net-span demon for any two different zones (45-demon Pandemonium table).

New capabilities:
- Single vs two-tetragram modes
- 9 appraisals (zan) with placeholder phase labels (Center, Ascent, … Return; not from Nylan)
- Em-profile / --em-stats (total Em, mediation level, batch-friendly)
- Alchemy summary (Heaven/Sulfur, Earth/Salt, Man/Mercury)
- Unicode monograms for compactness
- --viz / --viz-json export for visualizer wiring
- Hardware entropy (bundled `hardware_entropy.py` + local jitter collector)
  - 12-source collector (thermals, CPU freq, /proc/*, 256 timing jitter samples, fsync, etc.)
  - `--bytes N`, `--json`, graceful degradation when the script is absent
- Full cosmological hierarchy (3 fang → 9 chou → 27 pu departments → 81 jia) exposed on every cast
- Quasiphonic demon-name sketches (in the style of ccru-zone-voice combinatorial particles)

### Recommended Workflows

| Goal                                      | Recommended Commands                                                                 | Notes |
|-------------------------------------------|--------------------------------------------------------------------------------------|-------|
| Quick numogram reading                    | `oracle.py --seed 192855`<br>`oracle.py --text "YOUR NAME"`<br>`oracle.py --hardware` | Fastest entry point |
| Hardware-entropy seed (pure physical)     | `hardware_entropy.py --bytes 8`<br>then feed the hex as `--seed` to any tool        | Bundled in skill tree too |
| Full I Ching with relating hex            | `iching.py --cast --full`<br>`iching.py --iching --seed 666 --full`                 | Shows changing lines + transformed hex + numogram shadow |
| Single T'ai Hsuan tetragram + appraisals  | `taixuan.py --single --full --unicode`                                              | Best for the 9 zan |
| Two-tetragram Tai Xuan (classic)          | `taixuan.py --taixuan --full`<br>`oracle.py --taixuan --full --voice`               | Em count + hierarchy + alchemy |
| Em-state / mediation analysis             | `taixuan.py --taixuan --em-stats`<br>`taixuan.py --single --em-stats`               | Great for research / agent prompts |
| Yuandong 27-phase "department" cast       | `taixuan.py --phase`<br>`taixuan.py --phases`                                       | Mapped onto the 27 pu by this tool (not in the sources) |
| Visualizer / agent ready data             | `... --json`<br>`taixuan.py --taixuan --viz-json`<br>`iching.py --cast --json`     | Pipe into v7 visualizer or Hermes |
| Rich output with voice                    | `oracle.py --seed N --voice`<br>`oracle.py --taixuan --full --voice` | Formant synthesis (not wired for `--iching`) |
| Cross-base / Djynxxogram exploration      | `oracle.py --base36 --text "NUMOGRAM"`<br>`oracle.py --compare --text "YOUR NAME"` | 10/16/22/26/36 |
| Pure physical entropy (no network)        | `hardware_entropy.py --bytes 8`<br>then `--seed <that-hex>` to oracle/iching/taixuan | 12 local sources + jitter |
| Geomantic shield + house chart            | `geomancy.py --seed 192855 --house 10`<br>`oracle.py --geomancy --hardware --json`     | Judge, Via Puncti, perfection, company |
| Full end-to-end ritual reading            | `oracle.py --taixuan --single --full --unicode --voice --hardware`                  | Everything in one go |

### Djynxxogram mode (v1.2.0):
- `--base36 --text "WORD"` — per-character traversal through all 36 zones
- `--djynxxogram --seed N` — seed → hex → Djynxxogram traversal
- `--compare --text "WORD"` — cross-base comparison (10/16/22/26/36)

### What --base36 shows per character:
Character → AQ value → Djynxxogram zone (0-35) → syzygy partner → current → gate (triangular number → base-36 digital root, mod 35, the analogue of the decimal gate rule — the default; `--gate-rule mod` gives the old last-digit target, T mod 36) → decimal attractor → region (OUTER if zone 0 or Z)

### Zone naming:
Zones 10-35 use letter-native names (A=Aya, B=Buh, C=Kuh... Z=Zuh). 
Decimal zones also expose:
- full_name (poetic, e.g. "Void Resonance", "Iron Core", "Blood")
- epithet (visceral/CCRU, e.g. "Plex", "Warp")
These appear in readings, planchettes, JSON, and I Ching shadows.

### Companion tool:
`../numogram-base-explorer.py` — multi-base numogram constructor supporting any base N (2-36). Computes syzygy/gate/current/region tables, decimal projection clusters, DOT graph output. Gates default to the base-N digital root (mod N−1; in base 10 this is the CCRU rule, e.g. Gt-36: 8 → 9); `--gate-rule mod` gives the last-digit rule (T mod N).

## geomancy.py
Western geomancy (16 figures, shield chart, 12 houses). Stdlib only; every public function returns plain dicts (`cast_geomancy()` is the one-call reading), so a FastAPI wrapper can come later.

```bash
python3 geomancy.py                                   # entropy cast (hardware-entropy path, else os.urandom)
python3 geomancy.py --seed 192855 --house 10          # quesited house 10 (career); default 7
python3 geomancy.py --seed 192855 --topic marriage    # topic word → house (marriage 7, job 10, money 2 …)
python3 geomancy.py --dots "13 7 8 9 10 10 10 10 3 3 3 3 4 5 6 6"   # 16 hand-made rows: M1 fire…M4 earth, odd = •
python3 geomancy.py --mothers Puer,Via,Albus,Carcer --plain        # names, or 4-bit strings like 1101
python3 geomancy.py --seed 7 --json                   # full dict (shield, houses, validation, perfection …)
python3 geomancy.py --figures --scheme agrippa        # reference table
python3 geomancy.py --census --zone-map points        # exact census of all 65,536 charts (≈3 s)
python3 oracle.py --geomancy --seed 7 --full          # same tool through oracle.py (all flags pass through)
```

- Figures: 4 lines Fire/Air/Water/Earth, 1 = single point. `value` is Fire-high (Populus 0, Albus 2, Puer 13, Cauda 14, Via 15).
- Shield: Daughters by transposition, Nieces, Witnesses, Judge, Sentence (Judge + 1st Mother); the GD Reconciler (Judge + quesited figure) is also given. Checks: Judge even, repetition, both sets of inseparables, and every derivation (catches hand-calculation slips).
- Via Puncti on the Fire line (a double-point Judge is reported as "branching"/"none", not as a traditional path).
- Houses: `--houses sequential` (M1–N4 → 1–12; Greer, Digital Ambler, default) or `astrological` (GD paper: 1st figure → 10th house, 2nd → 1st …).
- Perfection: occupation, conjunction, mutation, translation, else denial (`--querent N`, `--abano` drops 12–1 adjacency). Company of the significator houses: simple / demi-simple / compound / capitular. GD Part of Fortune; the GD "Rubeus or Cauda in the 1st" impediment is flagged.
- `--scheme golden-dawn|agrippa|gerard`: sign + attributed element. The structural element (Digital Ambler) is always shown. Per-figure notes are paraphrased from Digital Ambler's "De Geomanteia" posts, URL per figure.
- Numogram hooks (labelled speculative): `--zone-map dr|dr-line|points` figure → decimal zone; base-16 view where syzygy = inversion (15 − n) and the gate follows `--gate-rule dr|mod`; I Ching hexagrams sharing the figure as lines 2–5 (non-historical).
- Bad `--seed`, `--dots`, `--mothers` or option values exit with status 2. Sources and the error list for earlier drafts: `geomancy-notes.md`.

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

Schema (enriched): {"zone","name","full_name","epithet","region","particle","polarity","current","gate",
         "gate_raw","gate_loops","gate_history","gate_lore","syzygy","syzygy_demon","reading","voice_quality","philosophy","color_rgb"}

Gate-loop depth: `gate_loops` is the number of plex-reduction iterations.
--planchette and normal readings now surface:
- full_name + epithet (e.g. "Seized Vortex (Iron Core / tn)", "Ascending Breath (Blood / pb)")
- gate_lore for special gates (Gt-6 Warp vortex, Gt-45 Pandemonium, Gt-21 etc.)
- voice_quality (CCRU-sourced sonic character)
- philosophy line (from zone aesthetics)
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




