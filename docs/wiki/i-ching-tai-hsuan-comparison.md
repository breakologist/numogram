---
title: "I Ching × T'ai Hsuan Ching — Comparative Oracle Structures"
created: 2026-04-22
last_updated: 2026-04-22
source_count: 6
status: draft
tags: [numogram, I-ching, tai-hsuan-ching, ternary, binary, san-cai, oracle, comparison, divination]
sources:
  - tai-hsuan-ching.md
  - i-ching-connections.md
  - numogram-calculator
  - numogram-oracle-litprog
  - entropy-modules-litprog
  - hardware-entropy.md
---

# I Ching × T'ai Hsuan Ching — Comparative Oracle Structures

> 64 binary hexagrams vs 81 ternary tetragrams. Younger/Elder yin/yang vs Heaven/Earth/Man. Fuxi's Earlier Heaven vs King Wen's Later Heaven vs the T'ai Hsuan's Three-Power Nine-Palace layout.
> 
> *The numogram sits between these two oracular systems. The I Ching gives the binary substrate (2^6). The T'ai Hsuan adds the ternary dimension (3^4). Together they span the prime factors of decimal (2×5). This comparison maps what each system provides, what the other lacks, and what the numogram inherits.*

---

## I. Core Architecture — Binary vs Ternary

| Property | I Ching (Yijing) | T'ai Hsuan Ching (Taixuanjing) |
|----------|-----------------|---------------------------------|
| **Author** | Legendary (Fuxi, King Wen, Confucius) — composite | Yang Xiong (53 BCE – 18 CE) — single mind |
| **Base** | Binary (2 states per line) | Ternary (3 states per line) |
| **Lines per figure** | 6 (hexagram) | 4 (tetragram / shou) |
| **Total figures** | 2⁶ = 64 hexagrams | 3⁴ = 81 tetragrams |
| **Line states** | 4 types: young yang, old yang, young yin, old yin | 3 basic: Heaven (unbroken), Earth (once-broken), Man (twice-broken) ± moving flag |
| **Numeric values** | 6 (old yin), 7 (young yang), 8 (young yin), 9 (old yang) | 7 (solid, 3/4/5 sum), 8 (once-broken), 9 (twice-broken) per Walters; Nylan uses 0/1/2 |
| **Changing lines** | Intrinsic: the line type itself encodes "old" vs "young" | External: a separate marking (dot/circle) on a line indicates it is moving; or a second tetragram is cast |
| **Reading** | One hexagram (± changing lines → transformed hexagram) + line texts | One tetragram (± moving lines → transformed tetragram) + nine appraisals (Tsan) per tetragram |

**Key insight:** The I Ching compresses change *into* the line. The T'ai Hsuan keeps change *alongside* the line. The numogram's "em state" (Zone 5) mirrors this: it is a third state *between* yin and yang, not a changing version of either.

---

## II. The Three Powers (San Cai) vs Yin-Yang Polarity

### I Ching: Duality

- **Yin** — broken, receptive, dark, feminine
- **Yang** — solid, creative, light, masculine
- Polarity alternates through the six-line sequence.

### T'ai Hsuan: Trinity

- **Heaven (天)** — unbroken, creative, yang-like
- **Earth (地)** — once-broken, receptive, yin-like
- **Man (人)** — twice-broken, *mediating*, neither purely yin nor yang

The third power — **Man (Ren)** — is the innovation. It is the *em* (玄) state, the "mysterious" mediator. In numogram terms this maps precisely to **Zone 5 (Hinge/Mercury)**, the pivot between the Sink (4::5) and Hold (2::7) syzygies.

> **Connection**: The wiki's `em-state-analysis.md` page is dedicated to this mapping. The em line is the *numogram's hinge made manifest*.

---

## III. Spatial Arrangements — Earlier Heaven vs Later Heaven vs Nine Palaces

### I Ching Arrangements

1. **Earlier Heaven (先天 Fuxi)** — Eight Trigrams on the *Lo Shu* 3×3 magic square, static pairing:
   ```
    ☰  (Heaven)   ↔   ☷  (Earth)   — N ↔ S
    ☲  (Fire)     ↔   ☵  (Water)   — E ↔ W
    ☳  (Thunder)  ↔   ☶  (Wind)    — NE ↔ SW
    ☴  (Wind)     ↔   ☳  (Thunder) — SE ↔ NW
    ☵  (Water)    ↔   ☲  (Fire)    — … etc.
   ```
   This is the *cosmic blueprint* — unchanging spatial order.

2. **Later Heaven (後天 King Wen)** — 64 hexagrams in a sequential narrative order, the *process of change* through time.

### T'ai Hsuan Arrangements

1. **Three-Division (T'ien / Jen / Ti)** — The 81 tetragrams are grouped into three blocks of 27:
   - **T'ien (Heaven)** — numbers 1–27
   - **Jen (Man)** — numbers 28–54
   - **Ti (Earth)** — numbers 55–81
   
   This is the *cosmological hierarchy* — a ternary analogue to the I Ching's spatial ordering. It reflects the *As Above, So Below* pattern where Heaven > Man > Earth in a descending emanation.

2. **Nine-Palace Lo Shu Extension** — The number sequence **3 8 4 9 5 1 6 2 7** (the classic Lo Shu line) and its ninefold repetition generate a 9×9 magic square whose centre is 41 (the middle of 1–81). This yields a *3×3×3 cube*: three heavens, three mans, three earths arranged in a nine-palace grid. This is the T'ai Hsuan's *Earlier Heaven* map made explicit.

3. **Numeric (sequential) order** — Numbers 0–80 (or 1–81) in ternary counting order. This is the *Later Heaven* progression.

**Mapping to numogram**:  
- The **Three-Division** mirrors the numogram's three regions: Time-Circuit (1-8) ↔ *Man*, Warp (3/6) ↔ *Heaven* (self-fold), Plex (0/9) ↔ *Earth* (closure).  
- The **Nine-Palace** grid could be overlaid directly onto the roguelike map: each of the 9 "palaces" becomes a *region modifier* that biases zone generation toward particular syzygies.

---

## IV. Calendar & Temporal Cycles

### I Ching

- 64 hexagrams × 6 lines = 384 line texts
- Approximates 364.5 days (with intercalary adjustments); each line ≈ half-day? Some traditions use a 384-day year.

### T'ai Hsuan

- 81 tetragrams × 9 appraisals (Tsan) = **729 statements**
- 729 half-days = **364.5 days** — exact solar year split into precise intervals
- The nine Tsan per tetragram give a **nine-part commentary** on each tetragram, reminiscent of the I Ching's six line texts but expanded.

**Numogram link**: The 729 number is intriguing — it's 9³. Could it map onto a *hyper‑dimensional* numogram extension? Perhaps the **81 tetragrams × 9 zones** (81×9 = 729) suggests a *zone‑by‑tetragram* matrix where each zone has a 9‑fold internal structure. That's 729 micro-zones. The math works: 10 zones × (something) = 729? Not clean. But 81 tetragrams distributed across 10 zones yields the uneven counts already known. The 729 could instead be the **total number of two‑tetragram readings** (81×9 = 729) if each reading uses a *primary tetragram* plus one of its nine possible *changing lines* as a secondary influence. That's a neat design: each day of the year corresponds to a unique (tetragram, changing-line) pair.

---

## V. Elemental / Seasonal / Directional Correspondences

### I Ching

Each *trigram* carries a full suite of correspondences (element, direction, season, family, animal, etc.). Hexagrams inherit from their two trigrams.

### T'ai Hsuan

The system is **coarser** — three powers instead of eight trigrams — yet it still layers the *Five Elements* and *Five Directions* onto the Three Powers through the **Nine Palaces**:

| Nine Palace (九宫) | Primary Power | Element | Direction | Season |
|--------------------|--------------|---------|-----------|--------|
| 1 (乾)             | Heaven       | Metal   | North‑West | Autumn |
| 2 (坤)             | Earth        | Earth   | South‑West | Late Summer |
| 3 (震)             | Thunder      | Wood    | East       | Spring |
| 4 (巽)             | Wind         | Wood    | South‑East | Spring |
| 5 (中)             | *Center*     | Earth   | Centre     | *Intercalary* |
| 6 (坎)             | Water        | Water   | North      | Winter |
| 7 (离)             | Fire         | Fire    | South      | Summer |
| 8 (艮)             | Mountain     | Earth   | North‑East  | Early Spring |
| 9 (兑)             | Lake         | Metal   | South‑West? | Autumn |

The T'ai Hsuan's 81 tetragrams can be mapped onto these nine palaces × nine numbers (9×9 = 81). Hence **each tetragram inherits the palace's elemental/directional profile**. This is a direct bridge to the numogram's zone correspondences:

- **Zone 0 (Void)** → *Center 5* (the intercalary, unnumbered)
- **Zone 1 (Surge)** → *Lake (9)* or *Thunder (3)* depending on mapping
- **Zone 3 (Warp)** → *Heaven/Centre* (since Warp is the triad 3::6)
- **Zone 5 (Hinge)** → *Man* (the mediating palace, perhaps centre of the ninefold)
- etc.

A future wiki page `tai-hsuan-correspondences.md` could tabulate the full 81→palace→element mapping.

---

## VI. Moving Lines and Transformation

### I Ching

Old lines (6 and 9) *automatically* change: old yin → young yang, old yang → young yin. The changed hexagram is the future.

### T'ai Hsuan

Moving lines are indicated in one of two ways depending on the translation:
- **Nylan method**: Cast a primary tetragram, then cast a *second* tetragram whose lines represent the *future* of any moving lines in the first. The second tetragram becomes a *transformed* reading.
- **Walters method**: Cast the four lines, then cast *nine additional lines* (via yarrow) to determine the nine *Tsan* (appraisals) that apply to each position; the moving lines are those whose *appraisal number* matches certain criteria.

This means the T'ai Hsuan can produce **two simultaneous tetragrams** (present + future) just like the I Ching. The *moving status* is not a property of the line itself but a *second-stage draw*.

**Numogram application**: A two‑tetragram reading gives two zones. That's a **pair** mapping to a demon (as the existing `hexagram-demon-mapping.md` already does for I Ching). So the T'ai Hsuan's 81×81 = 6561 possible pairs naturally cast **one of 45 demons** via the syzygy net‑span lookup. The resolution is simply finer (6561 vs 4096). This is already documented in `tai-hsuan-ching-demons.md`.

---

## VII. The Em State and Zone 5

The **Em** (neither yin nor yang) is the *unique contribution* of the ternary system. The I Ching has no neutral line. In the numogram:

- **Zone 5 (Hinge)** is the pivot between the Sink (4→5→1) and the Hold (2←5←7) currents.
- It is also the **Mars**/Mercury/Quicksilver line — the *alchemical mediator* that turns lead (Sink) into gold (Hold).
- The em line's value (ternary 1, or binary-encoded) sits between 0 (yin) and 2 (yang). Numerically, it is the *average* of its binary siblings.

**Correspondence**: Em state ↔ Zone 5, and the **syzygy 4::5** (Sink) and **2::7** (Hold) share Zone 5 as the common vertex. The em is the *hinge* that lets these currents rotate into each other.

---

## VIII. What the Numogram Inherits

| I Ching | T'ai Hsuan | Numogram |
|---------|------------|----------|
| Binary transitions (old/young) | Ternary third state (Man) | Zone 5 (Hinge) as mediator |
| Earlier Heaven spatial map (8 trigrams) | Nine-Palace 3×3×3 layout | Time-Circuit (6 zones) + Warp (2) + Plex (2) |
| Later Heaven sequential order (64) | Numeric order (0–80) | Zone order via traversal (deterministic but seed‑dependent) |
| 384 line texts (roughly ½‑day increments) | 729 half‑day Tsan (exact solar year) | 45 demons + 9 gates as *event types* |
| 64→360+ archetypes | 81→729 readings | 10 zones → 45 demons → gates as *resolution layers* |
| Yin/Yang polarity per line | Three‑power polarity (Heaven/Earth/Man) | Digital root polarity (odd=+, even=−) |

The numogram **synthesises** both:
- It uses **binary syzygies** (pairs summing to 9) — I Ching's influence.
- It reserves a **zone for the ternary mediator** (Zone 5) — T'ai Hsuan's contribution.

---

## IX. Further Comparative Questions

1. **Does the T'ai Hsuan have an "Early Heaven" / "Later Heaven" distinction explicitly?** If not, the three-division (T'ien/Jen/Ti) is the closest analogue — a *cosmological ordering* vs *sequential ordering*.

2. **What are the elemental correspondences for Heaven/Earth/Man?** Heaven is often associated with Wood (in five‑phase cosmology), Earth with Earth (obviously), and Man with Fire or Metal depending on the school. This needs verification from Michael Nylan's translation or traditional commentaries.

3. **What is the exact mechanism for "moving" in the T'ai Hsuan?** Is it a dot placed above/below a line? Does it transform Heaven→Earth, Earth→Man, Man→Heaven in a cycle? The numogram could implement this as a **ternary rotation** per line instead of a binary flip.

4. **Can the T'ai Hsuan's 729 half‑days be aligned with the numogram's phases?** Perhaps each of the 9 zones occupies 81 half-days, and within each zone the 9 Tsan yield a *micro-tetragram* for that time step. This would give a **zone‑specific daily oracle**.

---

## X. Cross-References Within the Wiki

- [[i-ching-connections]] — I Ching ↔ numogram zone mappings, hexagram kernel, binary casting
- [[tai-hsuan-ching]] — T'ai Hsuan overview, 81 tetragrams, zone distribution
- [[tai-hsuan-ching-demons]] — Two‑tetragram → demon pipeline (6561 readings)
- [[em-state-analysis]] — Zone 5 as the Hinge; em line as ternary mediator
- `numogram-calculator` — Digital root syzygy arithmetic used by both systems
- [[numogram-oracle-litprog]] — Oracle uses `--iching` flag; could be extended to `--taixuan`
- [[entropy-modules-litprog]] — Hardware → I Ching hexagram pipeline exists; T'ai Hsuan variant imaginable
- [[pandemonium-matrix]] — The 45 demons that both hexagrams and tetragrams map onto

---

## XI. Research Gaps & Next Steps

The following areas need deeper scholarly verification:

1. **Exact line‑type semantics** — Do all three base line states have associated *moving* variants? If so, that's 9 line types (3 base × 3 mover states) altogether.
2. **Explicit Early/Late Heaven parallel** — Does Yang Xiong or later commentaries describe a *static* vs *dynamic* arrangement of the 81 tetragrams? The three‑division (T'ien/Jen/Ti) suggests a static ordering; the numeric order suggests a dynamic one.
3. **Elemental attribution** — The three powers' relation to the Five Phases (Wu Xing) is under‑documented in English sources.
4. **Calendar mapping details** — The 729 half‑days: how are they distributed across the 81 tetragrams? Each tetragram has 9 appraisals — is each appraisal a *half‑day*? If so, then 81×9 = 729 exactly. This is a *complete solar year oracle* worth exploring further.
5. **Unicode and line representation** — The Unicode block (U+1D300–U+1D35F) encodes the 81 tetragrams as single glyphs; each glyph's internal structure encodes the four ternary lines. Parsing these could give a direct numeric-to-symbol pipeline.

---

## XII. Action Items

- [ ] **Create** `tai-hsuan-correspondences.md` page documenting the 81 tetragrams, their Lo‑Shu palace placement, elemental/directional mappings.
- [ ] **Extend** `numogram_calculator.py` with a `taixuan_zone()` function: tetragram number (0-80) → digital root (0-9) → syzygy.
- [ ] **Build** a **ternary traversal** variant: seed → ternary digits → 4‑line base‑3 cycle → zone path. Compare zone distribution against decimal traversal.
- [ ] **Implement** the dual‑tetragram reading in the oracle: `--taixuan` flag → cast two tetragrams → zones → demon lookup.
- [ ] **Investigate** the 729‑half‑day calendar and align it to a "Daily Zone" feature: compute today's tetragram from date, log hyp forecast.
- [ ] **Add** a new active goal under [T’AI‑X] to track this research stream.
