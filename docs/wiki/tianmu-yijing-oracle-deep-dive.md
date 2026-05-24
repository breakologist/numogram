---
title: Tianmu Yijing Oracle — Deep Dive & Numogram Bridge
tags:
  - Yijing
  - I Ching
  - Tianmu
  - Numogram Oracle
  - Hexagram
  - Zone Mapping
  - Corpus
created: 2026-05-16
related:
  - [[tianmu]]
  - [[hexagram-zone-mapping]]
  - [[numogram-oracle-yijing-patch]]
  - [[iching-numogram-casting]]
  - [[InterestingSites]]
---

# Tianmu Yijing Oracle — Deep Dive & Numogram Bridge

**[lab.tianmu.org/yijing](https://lab.tianmu.org/yijing/)** — an interactive I Ching divination app built as part of the Tianmu Labs ecosystem. All 64 hexagrams with judgments, images, trigrams, and changing-line transformations. The second arm of the Good Works Initiative's oracle suite (alongside the Elder Futhark runes).

---

## Technical Architecture

The entire app is a **single-page, client-side JavaScript application** (~40KB, all inline). No external dependencies beyond Google Fonts (EB Garamond, VT323, Noto Serif SC). The hexagram corpus, trigram lookup, coin-toss logic, and rendering are embedded in a single `<script>` tag in the HTML.

### Coin Toss Method

Uses the standard **three-coin method**:
- Each coin: `Math.random() < 0.5` → heads (value 3) / tails (value 2)
- Sum of 3 coins determines line type:
  - **6** → Old Yin ⚋ (changing) — yin line that will transform to yang
  - **7** → Young Yang ⚊ (stable)
  - **8** → Young Yin ⚋ (stable)
  - **9** → Old Yang ⚊ (changing) — yang line that will transform to yin
- 6 tosses build the hexagram bottom-to-top

### Binary Encoding

Binary strings follow the convention: **`lower_3_bits + upper_3_bits`** (trigram order: bottom-up).

| Field | Meaning |
|-------|---------|
| `b[0:3]` | Lower trigram (lines 1-3, bottom of hexagram) |
| `b[3:6]` | Upper trigram (lines 4-6, top of hexagram) |

Example: Hexagram #3 (Difficulty at the Beginning) has `b:'010001'`:
- Lower `010` = ☵ Kan (Water) — inner situation
- Upper `001` = ☳ Zhen (Thunder) — outer condition

The JS builds the hexagram Unicode glyph via: `String.fromCodePoint(0x4DC0 + hex.num - 1)` — King Wen ordering from Unicode range U+4DC0–U+4DFF.

### Display Flow

1. User clicks "Toss" → coin animation with 陽/陰 characters
2. Lines displayed bottom-up with bar/gap CSS 
3. After 6 tosses → "Reveal" button
4. Shows: hexagram Unicode glyph, King Wen number, Chinese name, pinyin, English name, trigram pair, judgment, image, line details
5. If changing lines present → shows the **relating hexagram** (transformed) with its own judgment

---

## Hexagram Corpus

Extracted and structured as JSON at `assets/tianmu-yijing-corpus.json`. All 64 hexagrams with:

- **King Wen number** (1-64)
- **Binary string** (6-bit, lower/upper trigram)
- **Chinese name, pinyin, English name**
- **Judgment** — plain English interpretation
- **Image** — natural metaphor / wise person's teaching
- **Trigram pair** — lower and upper trigram with symbols

The translator is **Dalai Moo Naomi** (same as the Dao De Jing translation). The English is modern, direct, and characterful — avoiding Wilhelm's archaisms and transliterations. Example contrast:

| Source | Hexagram #29 Judgment |
|--------|----------------------|
| **Tianmu** | *"Sincerity in the heart brings success. Danger upon danger. Flow like water — maintain your inner truth through peril."* |
| **Wilhelm** | *"The Abysmal repeated. If you are sincere, you have success in your heart. Whatever you do succeeds."* |

---

## Zone Mapping (Canonical DR)

Using the established formula `zone = 1 + (KingWen_number - 1) % 9`:

| Zone | Count | Hexagrams (KW#) | Character |
|------|-------|-----------------|-----------|
| **Zone 1** (Surge) | 8 | #1 乾, #10 履, #19 臨, #28 大過, #37 家人, #46 升, #55 豐, #64 未濟 | Creative Beginning, Treading, Approach |
| **Zone 2** (Separation) | 7 | #2 坤, #11 泰, #20 觀, #29 坎, #38 睽, #47 困, #56 旅 | Receptive, Peace, The Abysmal |
| **Zone 3** (Warp) | 7 | #3 屯, #12 否, #21 噬嗑, #30 離, #39 蹇, #48 井, #57 巽 | Difficulty, Standstill, The Well |
| **Zone 4** (Pressure) | 7 | #4 蒙, #13 同人, #22 賁, #31 咸, #40 解, #49 革, #58 兌 | Folly, Fellowship, Revolution |
| **Zone 5** (Gate) | 7 | #5 需, #14 大有, #23 剝, #32 恆, #41 損, #50 鼎, #59 渙 | Waiting, Possession, The Cauldron |
| **Zone 6** (Abyss) | 7 | #6 訟, #15 謙, #24 復, #33 遯, #42 益, #51 震, #60 節 | Conflict, Modesty, The Arousing |
| **Zone 7** (Rise) | 7 | #7 師, #16 豫, #25 無妄, #34 大壯, #43 夬, #52 艮, #61 中孚 | Army, Enthusiasm, Inner Truth |
| **Zone 8** (Blood) | 7 | #8 比, #17 隨, #26 大畜, #35 晉, #44 姤, #53 漸, #62 小過 | Holding, Following, Small Exceeding |
| **Zone 9** (Plex) | 7 | #9 小畜, #18 蠱, #27 頤, #36 明夷, #45 萃, #54 歸妹, #63 既濟 | Small Taming, Work on Spoiled, After Completion |
| **Zone 0** (Void) | 0 | *(empty)* | No hexagram corresponds directly to the void-point |

### Zone Character Analysis

The zone assignments reveal meaningful thematic clustering:

- **Zone 1 (Surge)** opens with **Qian/The Creative** — pure yang, the initiating force. Closes with **Wei Ji/Before Completion** — the threshold just before the cycle ends. Surge energy: beginnings, thresholds, unfinished business.
- **Zone 2 (Separation)** holds **Kun/The Receptive** — pure yin. Also grabs the triad of difficult waters: **Kan/The Abysmal**, **Kun/Oppression**, **Lu/The Wanderer**. Separation is the zone of being in deep water, alone.
- **Zone 3 (Warp)** contains **Zhun/Difficulty at the Beginning** and **Pi/Standstill** — stuckness and blockage. But also **Li/The Clinging Fire** and **Xun/The Gentle Wind** — light and penetration emerging from constraint.
- **Zone 4 (Pressure)** clusters social hexagrams: **Tong Ren/Fellowship**, **Xian/Influence**, **Ge/Revolution**, **Dui/The Joyous Lake**. Pressure governs relationship dynamics.
- **Zone 5 (Gate)** is the crucible: **Xu/Waiting**, **Da You/Great Possession**, **Bo/Splitting Apart**, **Ding/The Cauldron**. Transformation through heat and time.
- **Zone 6 (Abyss)** — conflict, modesty, return, retreat. The zone of strategic withdrawal before renewal.
- **Zone 7 (Rise)** — the army, enthusiasm, innocence, great power, breakthrough. Forceful upward movement.
- **Zone 8 (Blood)** — holding together, following, great taming, progress. Consolidation and slow accumulation.
- **Zone 9 (Plex)** — small taming, work on what has been spoiled, nourishing, darkening of the light. The terminal zone where things are gathered, finished, completed — then begins again.

---

## Syzygy Carrier Distribution

Using the canonical zone mapping, each hexagram calls one of 5 syzygy carriers:

| Syzygy | Carrier | Mesh | Hexagrams (Zone → Partner) |
|--------|---------|------|---------------------------|
| 1::8 | Murrumur | 29 | Z1 (8 hexagrams) → Z8 / Z8 (7) → Z1 — **15 total** |
| 2::7 | Oddubb | 23 | Z2 (7 hexagrams) → Z7 / Z7 (7) → Z2 — **14 total** |
| 3::6 | Djynxx | 18 | Z3 (7 hexagrams) → Z6 / Z6 (7) → Z3 — **14 total** |
| 4::5 | Katak | 14 | Z4 (7 hexagrams) → Z5 / Z5 (7) → Z4 — **14 total** |
| 0::9 | Uttunul | 36 | Z9 (7 hexagrams) → Z0 — **7 total** (Zone 0 empty) |

**Murrumur** receives the most hexagrams (15) because Zone 1 has the surplus hexagram (Qian #1). **Uttunul** receives 7 — all from Zone 9, reaching toward the empty Zone 0.

---

## Integrated Casting Pipeline

The Tianmu Yijing Oracle can now bridge directly with the existing numogram oracle pipeline:

### Current pipeline (hardware entropy through the skill system)
```
/dev/urandom → 6 bytes → byte%4 → 6 lines (6/7/8/9) 
  → hexagram (binary) → King Wen # 
    → zone (canonical DR) → syzygy partner → carrier demon
```

### Tianmu-enhanced pipeline
```
lab.tianmu.org/yijing (coin toss interface) 
  → hexagram (binary) → judgment + image from Tianmu corpus 
    → zone → syzygy → demon 
      → relating hexagram (if changing lines) 
        → second zone → zone transition path (mediated or unmediated)
```

The Tianmu corpus enriches the pipeline with:
- **Full judgments** — plain English, modern, accessible
- **Images** — nature metaphors for additional oracular depth
- **Trigram pair** — upper/lower context
- **Changing-line transformation** — relating hexagram for zone transition analysis

### Recommended cast flow

```
1. Visit lab.tianmu.org/yijing
2. Quiet your mind, hold your question
3. Cast coins (6 tosses)
4. Read primary hexagram: judgment + image
5. IF changing lines → read relating hexagram
6. Numogram overlay:
   a. Primary zone = 1 + (KW_num - 1) % 9
   b. Relating zone = same formula on transformed hex
   c. Zone pair → syzygy (if complementary) or unmediated path
   d. Carrier demon → Mesh value → gate sequence
7. Synthesize: hexagram oracle text + zone reading + demon carrier
```

---

## Examples

### Example 1: Hexagram #29 — The Abysmal Water

**Tianmu reading:** *"Sincerity in the heart brings success. Danger upon danger. Flow like water — maintain your inner truth through peril."*

**Numogram overlay:**
- King Wen #29 → Zone 2 (Separation)
- Syzygy partner → Zone 7 (Rise) → **Oddubb** (Mesh 23)
- Reading: You are in deep water (Abysmal repeated), which maps to Separation zone. The path through is toward Rise (Zone 7), carried by Oddubb. The Mesh of 23 suggests a significant but navigable crossing.

### Example 2: Hexagram #1 → #44 (changing lines)

Imagine casting Qian #1 (The Creative) with changing lines that transform it to Gou #44 (Coming to Meet).

**Tianmu readings:**
- Primary: *"Supreme success through perseverance. The creative force moves ceaselessly..."*
- Relating: *"The maiden is powerful — do not marry her. A force appears unexpectedly..."*

**Numogram overlay:**
- Primary zone: #1 → Zone 1 (Surge) ↔ Zone 8 (Blood) — Murrumur
- Relating zone: #44 → Zone 8 (Blood) ↔ Zone 1 (Surge) — Murrumur
- Zone pair: 1→8 → mediated by Murrumur (same syzygy carrier both ways)
- Reading: The creative surge moves directly toward multiplicity/blood. The carrier Murrumur mediates both directions — whatever enters this path is shaped by the 1↔8 current.

---

## Cross-Corpus Comparison

### Tianmu vs Wilhelm judgments

Tianmu's translations are notably more **direct and action-oriented** than Wilhelm's:

| Hex | Tianmu | Wilhelm |
|-----|--------|---------|
| #12 否 | *"Standstill — the way of inferior people prevails. Perseverance of the wise one."* | *"Standstill. Evil people do not further the perseverance of the superior man."* |
| #51 震 | *"Thunder comes — shock and awe. Then laughter. The shock brings fear, but fear brings vigilance."* | *"Shock comes — oh, oh! Then laughing words — ha, ha!"* |
| #64 未濟 | *"The fox nearly completes the crossing. If its tail gets wet, there is nothing that furthers."* | *"Before completion. Success. But if the little fox, after nearly completing the crossing, gets his tail in the water, there is nothing that would further."* |

Tianmu's version speaks in **imperatives and observations** ("Flow like water") where Wilhelm uses **descriptive statements** ("Whatever you do succeeds"). This makes the Tianmu corpus better suited for direct oracular use — the text itself instructs rather than merely describes.

---

## Technical Integration

The extracted corpus is available as structured JSON:

**Path:** `assets/tianmu-yijing-corpus.json`

Schema:
```json
{
  "source": "Tianmu Yijing Oracle",
  "translator": "Dalai Moo Naomi",
  "extracted": "2026-05-16",
  "hexagrams": {
    "1": {
      "num": 1,
      "unicode": "䷀",
      "binary": "111111",
      "lower_trigram": {"bin": "111", "name": "乾", "pinyin": "Qián", "en": "Heaven", "symbol": "☰"},
      "upper_trigram": {"bin": "111", "name": "乾", "pinyin": "Qián", "en": "Heaven", "symbol": "☰"},
      "name_cn": "乾",
      "pinyin": "Qián",
      "name_en": "The Creative",
      "judgment": "Supreme success through perseverance...",
      "image": "Heaven moves with vigour...",
      "king_wen": 1,
      "zone_canonical": 1,
      "syzygy_partner": 8,
      "syzygy": "1::8 (Murrumur/29)"
    }
  }
}
```

### Usage in oracle pipeline
```python
import json
with open('assets/tianmu-yijing-corpus.json') as f:
    corpus = json.load(f)

# After casting determines KW #29
hex29 = corpus['hexagrams']['29']
print(f"Reading: {hex29['judgment']}")
print(f"Zone: {hex29['zone_canonical']}")
print(f"Syzygy: {hex29['syzygy']}")
```

---

## Future Work

1. **Cron-scrape refresh** — set up a periodic check of lab.tianmu.org/yijing for corpus updates (the library is "living — continuously expanding")
2. **--tianmu-yijing flag** — add to the numogram oracle CLI for direct integration
3. **Zone transition heatmap** — compute all 64×64 = 4,096 possible casting transitions and their syzygy/unmediated distribution
4. **Trigram zone matrix** — 8×8 grid of trigram pairs → zones → syzygy demons, similar to the King Wen trigram pair matrix but with Tianmu's binary encoding
5. **Sonification scheme** — map hexagram judgment → audio synthesis parameters per zone (the water hexagrams in Zone 2 could inform the Abysmal formant parameters)

---

## Source

- Live oracle: [lab.tianmu.org/yijing](https://lab.tianmu.org/yijing/)
- Corpus JSON: `assets/tianmu-yijing-corpus.json` (vault) / `docs/wiki/assets/` (export)
- Extracted: 2026-05-16
- Translator: Dalai Moo Naomi (same as Dao De Jing)

## See Also

- [[tianmu]] — full site overview (Good Works Library, Lab projects, theology)
- [[hexagram-zone-mapping]] — canonical 64-row reference table
- [[iching-numogram-casting]] — full casting pipeline skill
- [[numogram-oracle-yijing-patch]] — expansion outline for oracle.py
- [[dao-de-jing-tianmu]] — companion Dao De Jing translation

## Companion Diagrams (Canonical DR Zone Method)

New SVGs generated from the Tianmu corpus, using `zone = 1 + (KW-1) % 9`:

| Diagram | File | Description |
|---------|------|-------------|
| **Hexagram→Zone Mapping** | `assets/hexagram-zone-mapping-tianmu.svg` | 10-zone column layout. 8 hex in Z1, 7 in Z2-Z9, Z0 empty (Void). Each card: Unicode glyph, KW#, pinyin, English name, trigram symbols, syzygy carrier. |
| **Trigram-Pair Matrix** | `assets/trigram-pair-matrix-tianmu.svg` | 8×8 matrix sorted by binary descending. Upper (cols) × Lower (rows). Color-coded by zone with legend. Diagonal banding shows zone clustering. |
