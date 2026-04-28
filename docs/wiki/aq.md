---
title: AQ (Alphanumeric Qabbala Value)
created: 2026-04-27
source: cli/aq_calculator_canonical.py
status: stub
tags: [AQ, qabbala, calculator, cipher, hyperstition]
---

# AQ — Alphanumeric Qabbala Value

The **AQ value** of a string is its raw base-36 sum before reduction. It is the first, unfiltered output of the Alphanumeric Qabbala cipher.

## Computation

```python
def aq_value(text):
    """A=10, B=11, ..., Z=35; digits 0–9 at face value."""
    return sum(AQ_VALUES.get(c.upper(), 0) for c in text if c.isalnum())
```

| Character | Value |
|-----------|-------|
| 0–9 | 0–9 |
| A | 10 |
| B | 11 |
| … | … |
| Z | 35 |

Spaces, punctuation, and non-alphanumerics are ignored.

## Why AQ Matters

The AQ total is the **pre-reduction signature** of a phrase. Two names may reduce to the same zone but have wildly different AQs, indicating scale or intensity. In the oracle's `--text` mode, the AQ is printed alongside the digital root; in the interactive calculator (`aq_calculator_canonical.py`), the AQ feeds into gate cumulation and triangular checks.

Examples from the canonical dictionary:

| Phrase | AQ | Digital Root | Zone |
|--------|----|--------------|------|
| `AL` | 31 | 4 | 4 |
| `666` | 666 | 9 | 9 |
| `777` | 777 | 3 | 3 |
| `english` | 137 | 2 | 2 |
| `lucifer` | 137 | 2 | 2 |
| `the devils library` | 333 | 9 | 9 |
| `evacuate humanity` | 333 | 9 | 9 |
| `Hermetic` | 153 | 9 | 9 |
| `the numogram` | 360 | 9 | 9 |
| `the decimal labyrinth` | 360 | 9 | 9 |

Notice the clustering: `137`, `333`, `360`, `666`, `777` all reduce to extremes (2, 3, 9) — the Warp and Plex zones. High AQ values tend to plunge into the outer loops.

## Relation to Gates and Triangularity

The calculator's `cumulate()` function uses the AQ to compute gate indices: `Gt = C(zone) = zone × (zone − 1) / 2`. The `is_triangular()` predicate checks whether an AQ itself is a triangular number — a property that heavily favours Warp zones (3 and 6) due to the digital root cycle of triangulars: `1 → 3 → 6 → 1 → 6 → 3 → 1 → 9/0`.

## See also

`digital-root`, `zone`, `syzygy`, `gate`, `current`, `numogram-calculator`, `aq-dictionary-augmented`
