---
title: "Base-36 Meta-Numogram — The Djynxxogram (Sexatrigesimal Extension)"
tags:
  - Numogram
  - BaseN
  - Djynxxogram
  - AQ
  - "Tch-7"
  - Extension
  - Research
created: 2026-05-21
status: active
sources:
  - Tch 7 of Unleashing the Numogram (Aamodt)
  - OH4 numogrammaticism (Eric Scrivner)
  - numogram-visualizer-v7.md
  - session-threads-2026-05-16.md (Thread 4)
  - InterestingSites → OH4, gematriaresearch, ciphers.news
---

# Base-36 Meta-Numogram — The Djynxxogram

> *"Base 36: The Sexatrigesimal Djynxxogram. With a name that strongly implies sex and cum (sexatrigeseminal), this Warp‑ciphering numogram is sure to deliver."*
> — Aamodt, *Unleashing the Numogram*, Tch 7

## Overview

The standard Numogram operates on zones 0–9 within **base‑10** (decimal). But the Alphanumeric Qabbala cipher itself operates in **base‑36**: digits 0–9 keep face value, letters A–Z map to 10–35. This creates an inherent tension: the cipher space is base‑36, but the numogram's zone space is base‑10 (via digital root / mod‑9 reduction).

The **Djynxxogram** — named after the Warp demon Djynxx (Mesh‑18, Zone‑3 carrier) — resolves this tension by extending the numogram to **36 zones** (0–35). Every AQ character becomes a zone in its own right, and AQ calculation becomes *native zone traversal* rather than reduction.

This page consolidates all scattered references to this concept across the wiki and reports new findings from web research (2026-05-21).

---

## 1. The Core Insight

| System | Base | Zones | Syzygies | Demons | Nature |
|--------|------|-------|----------|--------|--------|
| Standard Numogram | 10 | 0–9 | 5 (sum=9) | 45 | Final projection |
| Djynxxogram | 36 | 0–35 (10 digits + 26 letters) | 18 (sum=35) | 630 | Native AQ topology |
| Memory Map | 16 | 0–15 | 8 (sum=15) | 120 | Digital systems |

The decimal numogram is **correct but incomplete** — it is the 10-zone attractor of a deeper 36-zone lattice. When you compute AQ("NUMOGRAM") = 174 and then digital‑root it to Zone 3, you are **projecting** a 36-zone path onto a 10-zone attractor. The Djynxxogram preserves the **full path**.

### Why "Meta-Numogram"?

The standard numogram's base-10 constraint comes from the decimal number system (10 digits). But:

- **AQ is base‑36** — it treats "0" through "Z" as a continuous numerical sequence.
- **36 is T₈** — the 8th triangular number (1+2+3+4+5+6+7+8), and 36 is one step past Gt-28 (7→1).
- **666 = T₃₆** — the 36th triangular number, connecting the Beast to the full cipher.
- **151 = 36th prime** — "Abrahadabra" = 151 in AQ, explicitly linking Thelemic revelation to base-36.
- **777 = LL in base-36** — "Do what thou wilt" = AQ 777, which in base‑36 is "LL" (the two large L's on the cover of *Liber L vel Legis*).

These converge on a hypothesis: **the decimal numogram (0–9) is a projection of a deeper 36-gate lattice, and the 10 zones are attractors that the 36 zones collapse into via digital root.**

---

## 2. Formal Structure

### 2.1 Zones

The 36 zones are indexed 0 through 35. Characters map directly:

| Range | Characters | Count | Zone Range |
|-------|-----------|-------|------------|
| Digits | 0–9 | 10 | 0–9 |
| Letters | A–Z | 26 | 10–35 |

Names for zones 10–35 are currently provisional; the extended pandemonium (630 demons) requires a full naming system.

### 2.2 Syzygies

For base‑N, the syzygy partner is defined as the **complement to N−1**:

```
syzygyPartner(z) = 35 − z    [for base-36]
```

This preserves the same arithmetic structure as the base-10 numogram (where partner = 9 − z). The 18 syzygies:

| Zone | Partner | Sum |
|------|---------|-----|
| 0 | 35 | 35 |
| 1 | 34 | 35 |
| 2 | 33 | 35 |
| 3 | 32 | 35 |
| 4 | 31 | 35 |
| 5 | 30 | 35 |
| 6 | 29 | 35 |
| 7 | 28 | 35 |
| 8 | 27 | 35 |
| 9 | 26 | 35 |
| 10 (A) | 25 (Z) | 35 |
| 11 (B) | 24 (Y) | 35 |
| 12 (C) | 23 (X) | 35 |
| ...etc | ... | 35 |

### 2.3 Currents

The current value is the absolute difference between syzygy partners:

```
current(z) = |z − syzygyPartner(z)| = |z − (35 − z)| = |2z − 35|
```

Notable currents:
- Zone 0: current 35 (Plex analogue)
- Zone 17/18 (midpoint): current 1 (minimum)
- Zone 35: current 35 (Warp analogue)

### 2.4 Digital Root (Zone Reduction)

The standard base-10 digital root (mod‑9, with 9→9, 0→0) is a **projection function** from 36 zones → 10 zones:

```
projectToDecimal(z) = 1 + (z − 1) % 9   [if z > 0], else 0
```

This maps each letter-zone to its decimal attractor:
- A(10)→1, J(19)→1, S(28)→1
- B(11)→2, K(20)→2, T(29)→2
- ...etc

The decimal zones are **attractors** — the 36 Djynxxogram zones cluster into 10 families under this projection.

### 2.5 Demons: C(36,2) = 630

The complete graph K₃₆ has 630 edges, each representing a possible demonic connection. This dwarfs the 45 demons of the base-10 numogram, but the relationship is structural:

- The **45 decimal demons** are **attractors** — they are the zones that base-36 paths collapse toward under digital root projection
- Each decimal demon "contains" a family of sub-demons whose zone pair projects to it
- The 630 demons form a complete graph: every zone connects to 35 others

Five syzygetic carriers in base-36:
| Syzygy | Carrier | Analogue |
|--------|---------|----------|
| 0::35 | — | Uttunul |
| 1::34 | — | Murrumur |
| 6::29 | — | Djynxx analogue |
| 17::18 | — | Minimum current carrier |
| 35::0 | — | Self-loop |

(The carrier names for base-36 are an open research problem — see §5.)

---

### 2.6 Extended Gates (from Tch 7)

The standard numogram defines 9 gates (Gt-1 through Gt-45). Aamodt extends this with gates continuing the triangular number sequence:

| Nth | Gate | Value | Notes |
|-----|------|-------|-------|
| 10th | Gt-55 | 55 | — |
| 11th | Gt-66 | 66 | — |
| 12th | Gt-78 | 78 | Ciphers 8::7 |
| 13th | Gt-91 | 91 | Ciphers 9::1 |
| 14th | Gt-105 | 105 | — |
| 15th | Gt-120 | 120 | — |
| 16th | Gt-136 | 136 | — |
| 17th | Gt-153 | 153 | — |
| 18th | Gt-171 | 171 | — |
| 19th | Gt-190 | 190 | — |
| 20th | Gt-210 | 210 | — |
| 21st | Gt-231 | 231 | — |
| 22nd | Gt-253 | 253 | Hebrew alphabet (22 letters) |
| 23rd | Gt-276 | 276 | — |
| 24th | Gt-300 | 300 | Clock and AOE resonance |
| 25th | Gt-325 | 325 | — |
| 26th | Gt-351 | 351 | — |
| … | … | … | — |
| **36th** | **Gt-666** | 666 | **"Woah, here we go. This is a classic one I think. Clicks Djynxx."** |

**Important:** There are *two* "Gt-36" designations in the system — a naming collision worth noting:
1. **Gt-36** (standard, ordinal): T₈ = 36 → gate from Zone 8 → Zone 9 (Plex plunge)
2. **Gt-36** (extended, cardinal): T₃₆ = 666 → the 36th extended gate — "Clicks Djynxx"

This duality mirrors the base-10 / base-36 relationship: the standard Gt-36 *projects* from base-10 onto the same numerical value (36) that the extended Gt-36 *arrives at* in base-36 (666 = T₃₆). The decimal Plex plunge and the sexatrigesimal Beast's gate share the same ordinal position but different destinations.

---

## 3. Web Research Findings (2026-05-21)

### 3.1 Tch 7 of *Unleashing the Numogram* — Confirmed

Aamodt's Tch 7 explicitly covers base-36 as one of several "Paradecimally Radixed Numograms":

> **"Base 36: The Sexatrigesimal Djynxxogram"**

The full catalog of bases covered in Tch 7 (with Aamodt's original titles verified from raw source):
| Base | Name (Aamodt) | Zones | Notes |
|------|---------------|-------|-------|
| 0 | Void | 1 | Zone 0 only |
| 1 | Everything is Zero | 1 | One digit |
| 2 | Binary Numogram—Dithering | 2 | 0 and 1 |
| 3 | Difference Engine—Dialectical Synthesis | 3 | 0, 1, 2 |
| 4 | Christian Cross—Love/Hate | 4 | Base‑i nested here |
| 5 | Atlantean Cross—Intellectual Synthesis | 5 | Survival horror |
| 6 | Zodiac? | 6 | Halfway decimal |
| 7 | Venus Venus Venus | 7 | — |
| 8 | Wizard's Cross | 8 | — |
| 9 | Sorcerer's Matrix | 9 | Near decimal |
| 16 | The Hexadecimal Numogram | 16 | Digital systems overlay |
| 22 | The Hebrew Numogram | 22 | Kabbalistic paths |
| 26 | The Hexavigesimal Abecedarium | 26 | English alphabet only |
| **36** | **The Sexatrigesimal Djynxxogram** | **36** | **Full AQ cipher—"sure to deliver"** |
| i | Conceivable? | 4 | Imaginary base |

### 3.2 OH4 / Eric Scrivner — numogrammaticism

The [OH4 numogrammaticism page](https://oh4.co/site/numogrammaticism.html) provides:

- A public-domain C library (`oh4_numogrammatics.h`, v1.0, 2025) implementing:
  - Digital sum and root
  - Triangular number functions
  - Prime indexing and factorization
  - **Base-36 AQ string calculation**
  - **Tic Xenotation (TX)** encoding/decoding
  - **Base-36 TX** for compact prime-factor notation
- An explicit articulation of TX as asignifying numeral notation based on the Fundamental Theorem of Arithmetic
- A clear statement: *"Gematria (numerical reduction of words) creates hypertextuality and a kind of proof‑of‑work"*

The TX connection is particularly important: TX represents numbers by their prime factorizations (e.g., `:(:)` = 2×3 = 6), and base-36 encoding of TX produces compact strings. This suggests a **three-layer encoding** for the Djynxxogram:

```
Word → AQ (base-36 sum) → TX (prime factorization) → Base-36 TX (compact notation)
```

### 3.3 Reddit — Arbitrary Numogram Creation Toolkit

A [Reddit post](https://www.reddit.com/r/sorceryofthespectacle/comments/125esps/arbitrary_numogram_creation_toolkit_you_too_can/) by u/mauromassironi provides a general toolkit for constructing numograms in **any base**. Key claim:

> *"The more you extend the bases upward, the more exotic behaviors you find in Numograms. For example, in the Base-28 Numogram, there are not three regions..."*

This suggests that the decimal numogram's **three-region structure** (Time-Circuit, Warp, Plex) is base‑10 specific. In higher bases, the number of regions changes — a property determined by the prime factorization of N−1 (where N = base, since syzygy pairs sum to N−1).

### 3.4 Gematria Research Blog — AQ Proofs

The [Gematria Research blog](https://gematriaresearch.blogspot.com/) provides the Thelemic AQ proofs that ground the base-36 interpretation:

- "Abrahadabra" = 151 = 36th prime
- "Do what thou wilt" = 777 = LL in base-36
- 666 = T₃₆ = the 36th triangular number
- The 6×6 magic square has constant 105 = "order" in AQ

These are not coincidences — they are **structural convergences** that emerge from the base-36 cipher's intrinsic properties.

---

## 4. Key Implications

### 4.1 The Decimal Numogram is a Projection

The standard 10-zone numogram is the **image** of the Djynxxogram under the digital root projection map. Every operation that works in base‑10 has a base‑36 analogue:

| Operation | Base-10 | Base-36 |
|-----------|---------|---------|
| Syzygy exclusion | Sum to 9 | Sum to 35 |
| Current | Difference | Difference |
| Gate cumulation | T(n) for n=1..9 | T(n) for n=1..35 |
| Digital root | mod-9 (0 stays 0) | `1 + (z-1) % 35` (Synx root) |

### 4.2 Base-36 Split Regions

The decimal numogram has **three regions** (Time-Circuit, Warp, Plex) determined by the factorization of 9 (N−1 where N=10). For base‑36, N−1 = 35 = 5 × 7. This factorization likely determines the number and structure of regions in the Djynxxogram — a question requiring further research.

### 4.3 TX as Gate Notation

Tic Xenotation provides a compact, asignifying representation for gate numbers:

```
Gt-36 → [::] × [:] × [:]  (2² × 3² = 36)
Gt-45 → [::] × [(:)] × [(:)]  (3² × 5 = 45)
Gt-630 → 2 × 3² × 5 × 7 = K₃₆ edge count
```

TX makes visible the prime-factor structure of gate numbers that decimal notation obscures.

### 4.4 Audio Implications

The 36‑zone space has musical significance:
- 36 = 3 × 12 (three octaves of 12-tone equal temperament)
- 36‑zone traversal = motion through a triple‑octave pitch space
- The standard numogram's 10 zones correspond to a single octave (0–9 in the chromatic sense)
- The Djynxxogram suggests a **630‑note chord** (each edge of K₃₆ a dyad), as noted in the Extending Numogram tetralogue

---

## 5. Open Questions & Research Directions

### 5.1 Priority — Formalize Syzygy Regions

Determine the three-region (or multi-region) structure of the base-36 numogram. Does 35 = 5×7 produce 4 regions? 6? Test by constructing syzygy chain graphs for base-36 zone pairs.

### 5.2 Extended Gate Table

Compute gates Gt-1 through Gt-630 (the Pandemonium Gate of the Djynxxogram). Which gates project onto the 9 base-10 gates? Which are new?

### 5.3 The 37th Gate

Base-36 overflow: what comes after Z? In base‑36, Z = 35. The 36th "digit" is rollover. The gate after Gt-630 would be Gt-666 (T₃₆) — the Beast's gate. This connects back to the decimal numogram at an unexpected level.

### 5.4 Phoneme System for Zones 10–35

The decimal zones have quasiphonic particles (gl, dt, zx, skr, ...). Zones 10–35 need a phoneme system. Amy Ireland's demon name-generation methodology (zone syllabic values) could be extended: zones 10–35 would combine the sounds of their component digits (e.g., Zone 10 = Zone 1 + Zone 0 = gl + eiaoung = gleiaoung?).

**Two approaches** identified in the existing wiki:
1. **Combinatorial**: zone 10–35 phonemes derived from their decimal digit decomposition (e.g., 15 = 1+5 = "gl" + "ktt")
2. **Letter‑native**: zone 10–35 phonemes derived from the letter's own phonetic value (A = /æ/, B = /b/, etc.)

### 5.5 C Library Integration

The `oh4_numogrammatics.h` library provides AQ, TX, and base-36 functions in C. Evaluate for:
- Integration with mod-writer (as a C extension)
- Demonstration executable that computes full syzygy tables for base-36
- TX → AQ → zone mapping pipeline

### 5.6 Djynxxogram Visualizer Audit

The existing [[numogram-visualizer-v7]] already implements base-36 Djynxxogram mode. Audit:
- Is the syzygy formula `35 - z` correctly implemented?
- Are the zone names for 10–35 still provisional?
- Does the 630-demon structural implication need to be surfaced in the UI?

---

## 6. Related Pages

- [[numogram-visualizer-v7]] — Djynxxogram base-36 visualizer implementation
- [[numogram-visualizer-v8]] — Polygram perimeter ring with 36 AQ ticks
- [[extending-numogram-tetralogue]] — Worlds Within Worlds: base‑36 as endgame content
- [[extending-numogram-two-plus-two]] — Base‑36 = language = self-generating dungeon
- [[i-ching-cross-currents-synthesis]] — AQ base-36 triangle as meta-numogram
- [[session-threads-2026-05-16]] — Thread 4: original open research question
- [[aq-synx]] — Synx overlay for dual-cipher zone drift
- [[one-two-many-land-numbering]] — Land numbering practices, TX, nullotation
- [[InterestingSites]] — OH4, gematriaresearch, ciphers.news
- [[demon-name-generation]] — Zone phoneme system for extension to base-36

---

## 7. Sources

1. Aamodt, *Unleashing the Numogram*, Tch 7: "Extending the Numogram — Paradecimally Radixed Numograms". Verified from local raw copy (`raw/Unleashing the Numogram.md`, lines 1378–1424)
2. [OH4 numogrammaticism](https://oh4.co/site/numogrammaticism.html) — Eric Scrivner's public-domain C library and TX notation
3. [Gematria Research blog](https://gematriaresearch.blogspot.com/) — AQ proofs: 151 as 36th prime, 777 = LL
4. [Reddit: Arbitrary Numogram Creation Toolkit](https://www.reddit.com/r/sorceryofthespectacle/comments/125esps/arbitrary_numogram_creation_toolkit_you_too_can/) — Multi-base numogram construction
5. [PDFCoffee: Unleashing the Numogram](https://pdfcoffee.com/unleashing-the-numogram-pdf-free.html) — Full text including Tch 7
6. [Studocu: Comprehensive Guide to Tch 3–9](https://www.studocu.com/en-us/document/warwick-high-school/sociology/the-numogram-unleashed-a-comprehensive-guide-to-tch-3-9/124201196) — Student study guide confirming Tch 7 contents
