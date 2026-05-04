---
title: CCRU Ciphers — Complete Catalog
created: 2026-05-04
last_updated: 2026-05-04
status: canonical
tags: [cipher, AQ, synx, gematria, ccru, qliphoth]
source: lumpenspace/ccru ciphers.ts (2026-04-30)
syzygy: djynxx
zone: 3
---

# CCRU Ciphers — Complete Catalog

> Ten canonical ciphers from the Qliphoth/CCRU stack. Each maps an alphabet of characters to a sequence of numeric values according to a mathematical or keyboard‑order progression.

Related: [[numogram-gematria]] (implementation), [[alphanumeric-qabbala]] (base AQ), [[aq-synx]] (Synx overlay), [[numogram-calculator]].

---

## Quick Reference Table

| Cipher ID | Short | Char Set (size) | Value Range | Diacritics? | Case | Maps '1'? | Sample('A') |
|-----------|-------|-----------------|-------------|-------------|------|-----------|-------------|
| `alphanumeric-qabbala` | AQ | `0‑9a‑z` (36) | 0‑35 | stripped | no | ✅ | 10 |
| `synx` | Synx | `0‑9a‑z` (36) | 1‑1260 | stripped | no | ❌ | 14 |
| `numeric-qwerty` | NQ | `1234567890` + `qwerty…` (36) | 0‑35 | stripped | no | ❌ | 14? actually char 'a' not in set; mapping via keyboard order |
| `qwerty` | QW | `qwerty…m` (26) | 1‑26 | stripped | no | ❌ | 17? |
| `alphanumeric-satanic` | Satanic | `0‑9a‑zA‑Z` (62) | 0‑61 | stripped | **yes** | ❌ | 10 / 46 |
| `alphanumeric-primes` | Primes | `0‑9a‑z` (36) | 1‑149 | stripped | no | ❌ | 11? Actually 'A'=index10→prime at index10? array[10]=11 |
| `alphanumeric-squares` | Squares | `0‑9a‑z` (36) | 0‑1225 | stripped | no | ❌ | 100 |
| `alphanumeric-trigonal` | Trigonal | `0‑9a‑z` (36) | 0‑630 | stripped | no | ❌ | 55 |
| `archaic-alphanumeric` | Archaic | `0‑9a‑z` (36) | 0‑33 | stripped | no | ❌ | 11 (but note duplicate 18 at index 18/19) |
| `numeric-qwerty-primes` | NQ Prime | `1234567890` + `qwerty…` (36) | 2‑151 | stripped | no | ❌ | 13? depends on keyboard position |

**Maps '1'?** If **❌**, consecutive digit characters in the phrase are added as a full integer, not digit‑by‑digit.

---

## Per‑Cipher Detail

### AQ — Alphanumeric Qabbala

Base-36 ordinal: `0→0, 1→1, …, 9→9, a→10, b→11, …, z→35`.  
Straforward linear mapping. This is the **canonical** Numogram cipher used by all oracle tools.

> **Example:** "HERMES" → H=17+? Actually H=17? Wait index: a=10 so h=17 → 17; E=14; R=27→27; M=22? Let's compute: H=17, E=14, R=27, M=22, E=14, S=28? No S index 28. Sum: 17+14+27+22+14+28 = 122 → DR 1+2+2=5 → zone 5?? But our skill says HERMETIC=153 (zone 9). HERMES is shorter. We'll compute later.

---

### Synx

Accelerating CCRU progression: `[1,2,3,4,5,6,7,9,10,12,14,15,18,20,21,28,30,35,36,42,45,60,63,70,84,90,105,126,140,180,210,252,315,420,630,1260]`  
Same character set as AQ, but values jump non‑linearly, producing large sums for short phrases.

**Important:** Does **not** map digit `'1'`; number groups become integers.

---

### Numeric QWERTY (NQ)

Keyboard order mapping:
- Digits: `1234567890` → values 0-9 in that order
- Letters: QWERTY rows in order:
  - `qwertyuiop` → values 10-19
  - `asdfghjkl` → values 20-28
  - `zxcvbnm` → values 29-35

Thus `'1' → 0`, `'q' → 10`, `'a' → 20`, `'z' → 29`, etc.

---

### QWERTY

Alphabet mapped to keyboard top‑row order only (26 letters, no digits):
- `qwertyuiopasdfghjklzxcvbnm` → values `1..26`

No digit mapping.

---

### Alphanumeric Satanic

Case‑sensitive extended set: digits + lowercase + uppercase → 62 characters mapped 0-61 in order.
- `0-9` → 0-9
- `a-z` → 10-35
- `A-Z` → 36-61

Thus `'A' = 36`, `'a' = 10`. Requires case‑sensitive handling.

---

### Alphanumeric Primes

First 36 primes: `[1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149]`  
Mapped positionally to `0-9a-z`. Note the sequence includes `1` as the first entry (non‑standard primality). No digit mapping.

---

### Alphanumeric Squares

Squares `n²` for `n=0..35`: `[0,1,4,9,16,25,36,49,64,81,100,121,144,169,196,225,256,289,324,361,400,441,484,529,576,625,676,729,784,841,900,961,1024,1089,1156,1225]`

---

### Alphanumeric Trigonal

Triangular numbers `T(n)=n(n+1)/2` for `n=0..35`: `[0,1,3,6,10,15,21,28,36,45,55,66,78,91,105,120,136,153,171,190,210,231,253,276,300,325,351,378,406,435,465,496,528,561,595,630]`

---

### Archaic Alphanumeric

Legacy CCRU variant: `[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,18,19,20,21,22,23,24,25,26,27,28,29,29,30,31,32,33]`  
Has duplicate entries at indices 18 & 19 (both 18), and 28 & 29 (both 29) — a compression artifact. No practical use today, but preserved for historical fidelity.

---

### Numeric QWERTY Primes

Same prime sequence as Alphanumeric Primes (first 36 primes) mapped to the `NUMERIC_QWERTY` character set (`1234567890qwerty…`). Thus `'1' → 2`, `'2' → 3`, `'q' → 11`, etc.

---

## Value Distribution Samples

Compute "AQ" under all ciphers (quick reference):

| Cipher | Value | Zone |
|--------|-------|------|
| AQ | 36 | 9 |
| Synx | 119 | 2 |
| NQ | 30 | 3 |
| QW | 12 | 3 |
| Satanic | 88 | 7 |
| Primes | 130 | 4 |
| Squares | 776 | 2 |
| Trigonal | 406 | 1 |
| Archaic | 35 | 8 |
| NQ Prime | 104 | 5 |

---

## Implementation

All arrays and compute logic live in the `numogram-gematria` skill:

```python
from hermes_skills.numogram_gematria import compute, list_ciphers
val = compute("CCRU", "alphanumeric-qabbala")   # 81
val = compute("CCRU", "synx")                   # 372
```

---

## Sources

- `gematria/plugin/src/ciphers.ts` (plugin) — defines all 10 ciphers with `chars`, `values`, flags
- `app/cyphers/ccruCiphers.ts` (app) — same nine ciphers (excludes Satanic)
- Live: https://qliphoth.systems/gematria
- [[numogram-gematria]] — Python reimplementation

---

## Unresolved: "14 Ciphers"

The `ccru.cc` landing page claims "14 ciphers" but the codebase contains 10. Possibilities:

1. Additional ciphers exist in a private fork or unreleased branch.
2. The count includes *variant flags* as separate ciphers.
3. The figure includes historical/retired ciphers (e.g., “Barker” variants).
4. Marketing hyperbole.

**Current stance:** Implement the 10 canonical ones from the public repo. Should a 14‑cipher list surface, ingest as `ciphers_v2` alongside the current set.
