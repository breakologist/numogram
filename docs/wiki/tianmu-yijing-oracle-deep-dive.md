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

**[lab.tianmu.org/yijing](https://lab.tianmu.org/yijing/)** — an interactive I Ching divination app built as part of the Tianmu Labs ecosystem. All 64 hexagrams with judgments, images, trigrams, and changing-line transformations.

---

## Technical Architecture

Single-page, client-side JS application (~40KB, all inline). No external dependencies beyond Google Fonts. Hexagram corpus, trigram lookup, coin-toss logic, and rendering embedded in a single `<script>` tag.

### Coin Toss Method

Standard **three-coin method**:
- Each coin: `Math.random() < 0.5` → heads (3) / tails (2)
- Sum determines line type: 6=Old Yin(changing), 7=Young Yang, 8=Young Yin, 9=Old Yang(changing)
- 6 tosses build hexagram bottom-to-top

### Binary Encoding

**`lower_3_bits + upper_3_bits`** where:
- `b[0:3]` = lower trigram (lines 1-3, bottom)
- `b[3:6]` = upper trigram (lines 4-6, top)

Unicode glyph via: `String.fromCodePoint(0x4DC0 + hex.num - 1)`.

---

## Hexagram Corpus

Extracted to JSON at `assets/tianmu-yijing-corpus.json`. All 64 hexagrams with judgments and images translated by **Dalai Moo Naomi** — modern, direct English. Comparison with Wilhelm:

| Hex | Tianmu | Wilhelm |
|-----|--------|---------|
| #29 | *"Flow like water — maintain your inner truth through peril."* | *"If you are sincere, you have success in your heart."* |
| #51 | *"The shock brings fear, but fear brings vigilance."* | *"Shock comes — oh, oh! Then laughing words — ha, ha!"* |

---

## Zone Mapping (Canonical DR)

`zone = 1 + (KingWen_number - 1) % 9`:

| Zone | Count | Key Hexagrams | Character |
|------|-------|---------------|-----------|
| Zone 0 (Void) | 0 | *(empty)* | |
| Zone 1 (Surge) | 8 | #1 乾 Creative, #64 未濟 Before Completion | Beginnings, thresholds |
| Zone 2 (Separation) | 7 | #2 坤 Receptive, #29 坎 Abysmal Water | Deep water, alone |
| Zone 3 (Warp) | 7 | #3 屯 Difficulty, #30 離 Clinging Fire | Stuckness, light emerging |
| Zone 4 (Pressure) | 7 | #13 同人 Fellowship, #49 革 Revolution | Relationship dynamics |
| Zone 5 (Gate) | 7 | #5 需 Waiting, #23 剝 Splitting Apart | Transformation through heat |
| Zone 6 (Abyss) | 7 | #6 訟 Conflict, #24 復 Return | Strategic withdrawal |
| Zone 7 (Rise) | 7 | #7 師 Army, #34 大壯 Great Power | Forceful upward movement |
| Zone 8 (Blood) | 7 | #8 比 Holding, #53 漸 Development | Consolidation |
| Zone 9 (Plex) | 7 | #9 小畜 Small Taming, #63 既濟 After Completion | Completion, terminus |

---

## Integrated Casting Pipeline

**Current pipeline:**
```
/dev/urandom → 6 bytes → byte%4 → 6 lines → hex → KW# → zone → syzygy → demon
```

**Tianmu-enhanced:**
```
lab.tianmu.org/yijing → hexagram + judgment + image → zone → syzygy → demon
  → relating hexagram (if changing lines) → second zone → zone transition
```

### Recommended cast flow
1. Cast at lab.tianmu.org/yijing 
2. Read primary hexagram: judgment + image
3. Read relating hexagram (if changing lines)
4. Numogram overlay:
   - Primary zone = 1 + (KW_num - 1) % 9
   - Relating zone = same formula
   - Zone pair → syzygy (if complementary) or unmediated path
   - Carrier demon → Mesh value

### Example: Hexagram #29 The Abysmal Water
- King Wen #29 → Zone 2 (Separation)
- Syzygy partner → Zone 7 (Rise) → **Oddubb** (Mesh 23)
- Interpretation: In deep water (Abysmal repeated), which maps to Separation. Path through is toward Rise, carried by Oddubb. Mesh 23 suggests a significant crossing.

---

## Syzygy Carrier Distribution

| Syzygy | Carrier | Mesh | Total Hexagrams |
|--------|---------|------|-----------------|
| 1::8 | Murrumur | 29 | **15** |
| 2::7 | Oddubb | 23 | **14** |
| 3::6 | Djynxx | 18 | **14** |
| 4::5 | Katak | 14 | **14** |
| 0::9 | Uttunul | 36 | **7** (Zone 0 empty) |

Murrumur receives the most (15) because Zone 1 has the surplus hexagram (Qian #1).

---

## Corpus Usage

```python
import json
with open('assets/tianmu-yijing-corpus.json') as f:
    corpus = json.load(f)

hex29 = corpus['hexagrams']['29']
print(f"Reading: {hex29['judgment']}")
print(f"Zone: {hex29['zone_canonical']}")
print(f"Syzygy: {hex29['syzygy']}")
```

---

## Sources

- Live oracle: [lab.tianmu.org/yijing](https://lab.tianmu.org/yijing/)
- Corpus JSON: `assets/tianmu-yijing-corpus.json`
- Translator: Dalai Moo Naomi

## See Also

- [[tianmu]] — full site overview
- [[hexagram-zone-mapping]] — canonical reference table
- [[iching-numogram-casting]] — casting pipeline skill
- [[numogram-oracle-yijing-patch]] — oracle expansion outline
