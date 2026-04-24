---
title: "Divination & Oracle Sources — A Curated Guide"
created: 2026-04-22
last_updated: 2026-04-22
source_count: 1
status: draft
tags: [numogram, divination, oracle, sources, research, esoteric, comparative]
sources: [i-ching-tai-hsuan-comparison.md]
---

# Divination & Oracle Sources — A Curated Guide

> A shortlist of traditional and non‑traditional oracular systems whose mathematical structures can be mined for numogram extensions, game mechanics, and hyperstitional content. Each entry lists the base, total figures, key correspondences, and *why it matters* for the project.

---

## Quick-Reference Table

| System | Base | Figures | Origination | Why It Matters |
|--------|------|---------|-------------|----------------|
| I Ching | 2^6 | 64 hexagrams | China, ~1000 BCE | Binary kernel; hexagram → zone → demon mapping; seed → hexagram pipeline exists |
| T'ai Hsuan Ching | 3^4 | 81 tetragrams | Yang Xiong, 2 BCE | Ternary complement; 81 → zone mapping cleaner than 64 → zone; introduces *em* neutral state |
| Wu Xing (Five Phases) | 5^1 | 5 elements | China, Warring States | Decimal prime factor 5; could define *pentagram* syzygies (sum to 10?) or five‑current system |
| Nine Palaces / Lo Shu | 3^2 | 9 numbers | China, pre‑Han | 3×3 magic square; spatial layout for dungeon zoning; directional correspondences |
| Subdecadence (CCRU) | 10 choose 2 | 45 pairs | CCRU, 1990s | **Pandemonium Matrix**; the demon taxonomy the game already uses |
| Ifá | 16^2 | 256 odu | Yoruba, ~1200 CE | Binary tree with 16 top‑level signs each containing 16 sub‑odu; could extend beyond 45 demons |
| Geomancy (ʿIlm al‑Raml) | 4^4 | 256 charts | Arabic, ~900 CE | 16 figures × 16 = 256; algorithmic generation similar to Brogue room accretion |
| Elder Futhark | 24 runes | 24 | Germanic, ~150 CE | 24 = 3×8; could tessellate Time‑Circuit with *rune‑zones*; Uthark variant adds 3 = 27 = 3³ |
| Runes (Uthark) | 24+3 | 27 | Nordic, medieval | Ternary 27 = 3³; direct bridge to T'ai Hsuan's 81 (3⁴) |
| Tarot Major Arcana | 22 trumps + Fool | 23 | Europe, ~1400s | 22 paths on the Kabbalistic tree; could map to **extended gates** (Gt‑22, Gt‑23, Gt‑45) |
| Numerological Pythagorean | 1–9 | — | Greece, ~500 BCE | Foundational to AQ; digital root as universal reduction |
| Medieval/Renaissance | 7 planets + 12 zodiac | 19 | Europe, 1400–1600 | 19 = 10 + 9; could give planetary zones or zodiac‑based currents |
| Land's Tic‑Xenotation | prime factors | — | CCRU/Nick Land | Decomposition into primes → tic notation → nullocation; core to numogram's *structural* method |

---

## High-Priority Deep-Dives

### 1. Qi Men Dun Jia (奇门遁甲)

- **Base**: 9 palaces × 10 stems × 12 branches = 1080 **ju** (charts)
- **Structure**: Combines *Heavenly Stems* (10), *Earthly Branches* (12), *Nine Palaces* (9), and *Hidden Heavens* (八門, eight doors)
- **Why**: Already algorithmic; yields 1080 distinct configurations. Could map directly to **10 zones × 108 = 1080** as a *hyper‑zone* layer. The eight doors could become *gate types* with different traversal rules.

**Action**: Scan for a machine‑readable table of the 1080 ju; tag each with stems/branches/palace; cross‑reference to numogram zones via digital root of stems.

### 2. Xuan Kong Da Gua (玄空大卦)

- **Base**: 64 hexagrams × 20 *mountains* = 1280 combinations
- **Structure**: Flying Star numerology applied to building orientation; each hexagram pairs with a *mountain* direction.
- **Why**: Extends the I Ching into a *spatial‑temporal* matrix; each combination has a *time* (period) and *direction*. Could inform **zone‑specific demon spawn rules** based on "period number" (analogous to hyperstition level).

### 3. Ifá / Odù

- **Base**: 16 major Odu × 16 sub‑Odu = 256
- **Structure**: Binary but *tree‑structured*; each Odu contains verses, proverbs, rituals.
- **Why**: 256 is 2⁸, an octave beyond 64. Rich narrative corpus already exists; could serve as a *lore engine* for demon dialogue or tombstone epitaphs. The 256 → 45 demon mapping would create a many‑to‑one compression ripe for hyperstition.

### 4. Arabic Geomancy (ʿIlm al‑Raml)

- **Base**: 16 geomantic figures × 4 *mothers* → 256 *charts*
- **Structure**: Four *mothers* (primary figures) generate 12 *witnesses* + 4 *judges* = 16‑figure chart.
- **Why**: Algorithmic *figure generation* mirrors Brogue's room accretion. The four mothers could become the *four voices* (Oracle/Builder/Writer/Gamer) each contributing a line to a tetragram.

---

## Existing Project Links

- [[i-ching-connections]] — 64 hexagrams → 10 zones mapping; `oracle.py --iching` implementation
- [[tai-hsuan-ching]] — 81 tetragrams → 10 zones; the ternary counterpart
- [[tai-hsuan-ching-demons]] — 81×81 = 6561 two‑tetragram castings → 45 demons
- [[em-state-analysis]] — The third line state (Man/Em) → Zone 5
- [[hardware-entropy]] — I Ching casting from hardware jitter (`iching(seed_bytes)`)
- `numogram-oracle` — Divination pipeline; could be extended to `--taixuan` mode
- [[pandemonium-matrix]] — The 45 demons that receive all oracle mappings

---

## Quick Wins (Implementable This Week)

1. **Add `--taixuan` flag to `oracle.py`** – Cast two tetragrams (81×81), map each to zone, look up net‑span demon. Already have the mapping logic in `tai-hsuan-ching-demons.md`.

2. **Build a `taixuan_zone(n)` function** – Given tetragram number 0–80, return its zone (digital root). Validate the 1,9,8,1 distribution across zones documented in `tai-hsuan-ching.md`.

3. **Ternary traversal prototype** – `traverse_ternary(seed_bytes)` interprets seed as ternary digits (base‑3), walks a 3‑state cycle: Heaven→Earth→Man→Heaven… Record zone distribution vs decimal traversal.

4. **Gate‑81 plot hook** – Write a lore snippet: *"The Gate of Em opens only when the nine appraisals align."* Place in `gates-and-plexing.md`.

5. **Daily Zone oracle script** – `daily_zone.py`: take today's date, compute ternary day‑of‑year, derive tetragram, map to zone, print hyp forecast. Store in `~/.hermes/tools/`.

---

## Long-Term Research (Backlog)

- [Qi Men Dun Jia | 1080 ju as hyper‑zone layer] — read tables, map to 10‑zone + 9‑gate × 12‑branch matrix
- [Xuan Kong Da Gua | Period‑based demon spawning] — integrate "20‑year periods" into hyperstition decay rates
- [Ifá / Odù | 256‑story lore corpus] — scrape public domain Odu verses, seed `exquisite-corpus.md` with 256 fragments
- [Arabic Geomancy | 16‑figure figure‑generation] — implement geomantic *mother* casting as alternative seed source (`oracle.py --geomancy`)
- [Elder Futhark | 24‑rune zone overlay] — map each rune to a zone via AQ; explore *rune‑gate* mechanics

---

## Numogrammic Extensions

| Source | Proposed Numogram Extension |
|--------|----------------------------|
| T'ai Hsuan (ternary) | **Gate‑81 (Em Gate)** — square of 9, pure *man* state; requires all three ternary digits to be 1 |
| Nine Palaces | **Palace‑biased zone generation** — each of the 9 palaces (± centre) weights zone assignment |
| Wu Xing (5 phases) | **Five‑current system** — add currents for Wood, Fire, Earth, Metal, Water as modifiers on top of numeric currents |
| Ifá (256) | **Tri‑syzygy combat** — each demon carries three syzygy values instead of one |
| Qi Men (1080) | **1080‑step traversal** — extend from 5 to 1080 steps, one per ju, reveals hidden gate sequences |
| Arabic Geomancy (16) | **16‑figure seed expander** — expand 8‑byte seed into 16‑figure chart, then reduce to zone |

---

## Next Actions

- [ ] Merge `i-ching-tai-hsuan-comparison.md` into index.md under "Theory & Structural Pages"
- [ ] Add `divination-sources-guide.md` to index.md (this page)
- [ ] Append this page to `log.md` External Files Reference and mention in today's section
- [ ] Create active goal [SOURCES] "Deep‑dive: Qi Men Dun Jia → 1080 ju" if time permits
