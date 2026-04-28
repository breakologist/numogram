---
title: Syzygy Chain Analysis of the AQ Dictionary
tags: [numogram, syzygy, analysis, AQ, fingerprint]
category: Research
---

# Syzygy Chain Analysis of the AQ Dictionary

> **Created**: 2026-04-27 | **Source**: `numogram-chain-fingerprint` batch run (8-step chains) on 46 AQ dictionary entries

## Summary

| Statistic | Value |
|-----------|-------|
| Entries analysed | 46 |
| Unique numeric values | 27 |
| Avg chain length | 8 steps |
| Void-Dominant terms | 25 |
| Gate-Scattered terms | 29 |
| Closed 8-step cycles | 0 |

## Motif Taxonomy

| Motif | Count | Description | Example terms |
|-------|-------|-------------|---------------|
| Gate-Scattered | 29 | Gate variance > 2.5 — high entropy in gate sequence | AL, AQ, kek … |
| Hold-Stable | 12 | ≥30% visits to zones 2/5 — resistance to change, Hold-current heavy | AL, IAO, eloi … |
| Rise-Seeking | 10 | ≥25% visits to zones 7/8 — ascending/positive polarity pull | IAO, three, yi jing … |
| Sink-Dominant | 4 | ≥25% visits to zones 1/4 — descending/negative polarity pull | AL, eloi, the one … |
| Void-Dominant | 25 | ≥40% visits to zones 0/9 — gravitates to Plex extremes (Void/Synthesis) | AQ, kek, lama … |
| Warp-Anchored | 8 | ≥30% visits to zones 3/6 — caught in acceleration loops | ten, lol, Hecate … |

## Observations

1. **Plex attractor dominance** — Zones 0 and 9 account for 54.4% of all zone visits across all chains. The decimal labyrinth naturally accumulates state-time at its synthesis/void endpoints.
2. **No closed 8-step cycles** — with 10-zone syzygy topology, an even-length chain (8 steps) never returns exactly to its start zone. Closed cycles appear at other lengths (2-step: 3↔6, 4-step: certain 4-cycles exist, etc.).
3. **Warp-Anchored seeds all have digital root 3 or 6** — these are the only zones whose syzygy partner is the other Warp zone. Any seed landing in 3 or 6 immediately enters a 2-cycle between 3 and 6: the canonical warp anchor.
4. **Gate variance correlates with void-dominance** — chains that visit zones 0/9 frequently have gates 0 and 9, producing high gate spread (max possible ≈20.25).
5. **Multi-motif terms** — some AQ entries span multiple motifs depending on chain length. Examples: `235 = numerology` (Void-Dominant + Sink-Dominant), `137 = english/lucifer` (Hold-Stable + Rise-Seeking).

## Detailed Chains

### 31 = AL

- **Motifs**: Hold-Stable | Sink-Dominant | Gate-Scattered
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.0 | sink=0.5 | gate_var=6.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-31]]

### 36 = AQ

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-36]]

### 52 = IAO

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-52]]

### 54 = kek

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-54]]

### 63 = lama

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-63]]

### 66 = ten

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-66]]

### 66 = lol

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-66]]

### 77 = eloi

- **Motifs**: Hold-Stable | Sink-Dominant | Gate-Scattered
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.0 | sink=0.5 | gate_var=6.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-77]]

### 96 = Hecate

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-96]]

### 96 = keys

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-96]]

### 101 = three

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-101]]

### 121 = the one

- **Motifs**: Hold-Stable | Sink-Dominant | Gate-Scattered
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.0 | sink=0.5 | gate_var=6.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-121]]

### 128 = yi jing

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-128]]

### 137 = english

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-137]]

### 137 = lucifer

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-137]]

### 151 = abracadabra

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-151]]

### 153 = Hermetic

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-153]]

### 180 = Anglossic

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-180]]

### 189 = CCCXXXIII

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-189]]

### 222 = savoir faire

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-222]]

### 234 = the numogram

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-234]]

### 235 = numerology

- **Motifs**: Rise-Seeking | Sink-Dominant | Gate-Scattered
- **Vector**: void=0.0 | warp=0.0 | hold=0.0 | rise=0.5 | sink=0.5 | gate_var=16.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-235]]

### 250 = Jesus Christ

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-250]]

### 250 = Iota Alpha Omega

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-250]]

### 300 = fifteen fifty one

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-300]]

### 313 = twelve fifty one

- **Motifs**: Hold-Stable | Rise-Seeking
- **Vector**: void=0.0 | warp=0.0 | hold=0.5 | rise=0.5 | sink=0.0 | gate_var=1.0 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-313]]

### 333 = one eight nine zero

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = and that strangely

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = evacuate humanity

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = the devils library

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = the invisible hands

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = the empty summit

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = Angelic Materialism

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = English Occultism

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 333 = Gnostic Calvinism

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-333]]

### 360 = life is computation

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-360]]

### 360 = the decimal labyrinth

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-360]]

### 360 = the tree of knowledge

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-360]]

### 360 = two five dual snakes

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-360]]

### 360 = hermetic cosmogony

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-360]]

### 369 = the three sided shapes

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-369]]

### 369 = that is all hassan sabba

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-369]]

### 666 = of man's first disobediance and the fruit

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-666]]

### 666 = the cybernetic culture research unit

- **Motifs**: Void-Dominant | Gate-Scattered
- **Vector**: void=1.0 | warp=0.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=20.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-666]]

### 777 = And God said, Let there be light, and there was light

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-777]]

### 777 = do what thou wilt shall be the whole of the law

- **Motifs**: Warp-Anchored
- **Vector**: void=0.0 | warp=1.0 | hold=0.0 | rise=0.0 | sink=0.0 | gate_var=2.25 | cycle=0
- *Full chain JSON*: [[workspace/aq_syzygy_analysis.json#seed-777]]
---

## Expanded Analysis (Grok rotor additions, 20 new values)

**New values**: CCRU (81), Doom (83), Faith (89), Santa=Satan (100), Slant family (111/117/171/173), Ayn Rand=Nick Land (140), Problem (144), Solomon (166), Numogram (174), Choronzon (209), Beast Pulse=Doomcrypt (210), Ptotic Eyes (227), Baroqwerty (234), Alphanumeric Qabbala (328), Soy Simulation (369), Synx — devil's spirit (444), Questioning Angel Key (567), ordo amoris (888), Psychodynamics (1848).

**Motif shift**: Void-Dominant drops from 54% to 34%; Hold-Stable rises from 26% to 36%; Rise-Seeking from 22% to 30%. The signal cluster (CCRU, Beast Pulse, Questioning Angel, Doomcrypt) is Hold/Rise-weighted, pulling the overall distribution toward stability and ascent.

**Zone visit distribution** (expanded):

| Zone | Name | Visits | % |
|------|------|--------|---|
| 0 | eiaoung | 64 | 17.0% |
| 1 | gl | 12 | 3.2% |
| 2 | dt | 44 | 11.7% |
| 3 | zx | 44 | 11.7% |
| 4 | skr | 24 | 6.4% |
| 5 | ktt | 24 | 6.4% |
| 6 | tch | 44 | 11.7% |
| 7 | pb | 44 | 11.7% |
| 8 | mnm | 12 | 3.2% |
| 9 | tn | 64 | 17.0% |

**No 8-step closed cycles** persist across both dictionaries.

