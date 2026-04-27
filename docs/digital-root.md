---
title: Digital Root
created: 2026-04-27
source: cli/aq_calculator_canonical.py
status: stub
tags: [digital-root, reduction, zygonovism, qabbala]
---

# Digital Root

The **digital root** is the single-digit reduction of any integer by repeated digit-summing. In the Decimal Numogram, it is the primary zone mapper: every AQ total, every gate index, every triangular cumulation is collapsed to 0–9 by this rule.

## Definition

```
digital_root(0) = 0
digital_root(n) = 1 + (n − 1) mod 9   for n > 0
```

Equivalently: sum the decimal digits repeatedly until one digit remains.

| n | Digital Root |
|---|--------------|
| 1–9 | 1–9 |
| 10 | 1 |
| 11 | 2 |
| … | … |
| 18 | 9 |
| 19 | 1 |
| 666 | 6+6+6 = 18 → 1+8 = **9** |
| 777 | 7+7+7 = 21 → 2+1 = **3** |

## Zygonovism: Nine-Sum Twinning

The digital root implements **zygonovism**, the CCRU's pairing rule: two zones summing to 9 are syzygetic twins.

```
1 ↔ 8  (1 + 8 = 9)
2 ↔ 7
3 ↔ 6
4 ↔ 5
0 ↔ 9  (0 + 9 ≡ 0 mod 9, treated as a special case)
```

The current of a syzygy is the absolute difference between the partners:

| Syzygy | Difference (Current) |
|--------|---------------------|
| 1::8 | 7 |
| 2::7 | 5 |
| 4::5 | 1 |
| 3::6 | 3 |
| 0::9 | 9 |

Thus the digital root both **assigns a zone** and **selects a current** via its twin.

## Role in the System

- **Zone mapping:** Every input (seed, name, phrase) is reduced to a zone. The oracle's `--text` and `--seed` modes both end here.
- **Gate determination:** Gate indices (Gt-n) are often derived from cumulation `C(z) = z(z−1)/2` then reduced; digital root decides which zone the gate targets.
- **Triangular behaviour:** Triangular numbers `Tₙ = n(n+1)/2` have digital roots cycling `1, 3, 6, 1, 6, 3, 1, 9/0…`. This is why triangularity gravitates to Warp (3,6) and occasionally Plex (9/0).
- **Binary–decimal bridge:** Powers of 2 reduced mod 9 yield `1,2,4,8,7,5` — the Time-Circuit zones. Digital root is the reduction that exposes the 6-cycle.

## Code References

- `aq_calculator_canonical.py`: `digital_root()` — the core function
- `oracle.py`: used in `get_zone()` and `taixuan_zone()`
- `numogram-calculator` skill: documented arithmetic interface
- `numogram-analysis-pipeline`: syzygy chain analysis over digital-root manifolds

## Hyperstitional Note

Digital root is the **immanent filter**. Any number, no matter how large, collapses to a zone. AQ values in the thousands routinely reduce to 3, 6, or 9 — the outer loops. The system is biased toward Warp and Plex because the mod-9 map folds most integers onto 3, 6, and 9. The Time-Circuit zones (1,2,4,5,7,8) are the rarer, more delicate paths. This is not a bug; it is the numogram's preference for acceleration and termination over cyclic stasis.

---

*See also:* `zygonovism`, `syzygy`, `zone`, `current`, `gate`, `triangular`, `numogram-calculator`
