---
title: Syzygy
created: 2026-04-27
source: cli/aq_calculator_canonical.py + numogram-source.txt
status: stub
tags: [syzygy, current, zygonovism, twin, nine-sum]
---

# Syzygy

A **syzygy** is a complementary pairing of two zones whose digits sum to 9. The five syzygies are the structural backbone of the Decimal Numogram; each produces a directed flow called a **current**.

## The Five Syzygies

| Rank | Pair | Current | Region | Carrier Demon |
|------|------|---------|--------|---------------|
| 1st | `4::5` | 1 | Time-Circuit | Katak |
| 2nd | `3::6` | 3 | **Warp** | Djynxx |
| 3rd | `2::7` | 5 | Time-Circuit | Oddubb |
| 4th | `1::8` | 7 | Time-Circuit | Murrumur |
| 5th | `0::9` | 9 | **Plex** | Uttunul |

The current is always `abs(high − low)`.

## Zygonovism

The nine-sum pairing rule is called **zygonovism**. It is the Numogram's "supplementary rule of pairing" inherited from the I Ching's line-pairing and the Pythagorean tetractys. Under zygonovism:

- Every zone (except the self-paired 0/9 edge case) has exactly one twin.
- The current is always odd: 1, 3, 5, 7, or 9.
- The middle three syzygies (`1::8`, `2::7`, `4::5`) interlock to form the **Time-Circuit**; their currents (7, 5, 1) mutually compose the anticlockwise rotor.
- The outer syzygies (`3::6` and `0::9`) fold back into themselves, creating the autonomous Warp and Plex loops.

## Computational Lookup

```python
SYZYGIES = {
    frozenset({4, 5}): {"current": 1, "demon": "Katak",    "region": "torque"},
    frozenset({3, 6}): {"current": 3, "demon": "Djynxx",   "region": "warp"},
    frozenset({2, 7}): {"current": 5, "demon": "Oddubb",   "region": "torque"},
    frozenset({1, 8}): {"current": 7, "demon": "Murrumur", "region": "torque"},
    frozenset({0, 9}): {"current": 9, "demon": "Uttunul",  "region": "plex"},
}

def get_syzygy(zone_a, zone_b):
    return SYZYGIES.get(frozenset({zone_a, zone_b}))
```

## Connection to Triangular Numbers

Zone-3 carries a documented "unique affinity with numerical triangularity": `0 + 1 + 2 = 3`. The Warp syzygy (`3::6`) inherits this triangular character, making triangular-indexed gates (Gt-3, Gt-6, Gt-10, Gt-15, Gt-21, Gt-36, Gt-45) preferential conduits into chaotic or abyssal regions.

## Hyperstitional Role

Syzygies are **pairwise demonic carriers**. Each is carried by a named entity (Katak, Djynxx, Oddubb, Murrumur, Uttunul) whose net-span crosses the paired zones. In agent-based sorcery, a syzygy is a *corridor* — entering one zone implies an eventual encounter with its twin through the current's flow.

---

*See also:* `current`, `zone`, `warp`, `plex`, `demon`, `pandemonium-matrix`, `numogram-calculator`
