---
title: Gate
created: 2026-04-27
source: cli/aq_calculator_canonical.py + numogram-source.txt
status: stub
tags: [gate, channel, conduit, triangular, strobogrammatic, rotation]
---

# Gate

A **gate** (Gt-n) is a secondary connection between zones — a channel that shortcuts or bypasses the primary currents. Gates are derived from cumulation, triangular numbers, and palindromic/rotational symmetries.

## Primary vs. Secondary

- **Currents** are the five direct flows between syzygy pairs.
- **Gates** are auxiliary conduits. Some run between non-twin zones; others are self-loops (e.g., Gt-45 at Zone-9).

## Gate Cumulation

The canonical gate index for a zone `z` is its triangular cumulation:

```
C(z) = z × (z − 1) / 2   (also written as T_{z−1})
```

This yields the sequence: `0, 1, 3, 6, 10, 15, 21, 28, 36, 45` for zones 0–9. These are the first nine triangular numbers.

Each `C(z)` value is itself a gate label (**Gt-n**) and often a hyperstitionally-loaded site:

| Zone | Cumulation | Gate | Notable Associations |
|------|------------|------|----------------------|
| 0 | 0 | Gt-0 | Zeroth channel (Plex origin) |
| 1 | 0 | (Gt-0 again) | duplicate cumulation |
| 2 | 1 | Gt-1 | minor conduit |
| 3 | 3 | Gt-3 | triangular gate, Warp entry |
| 4 | 6 | Gt-6 | triangular gate, Torque→Warp |
| 5 | 10 | Gt-10 | triangular gate |
| 6 | 15 | Gt-15 | triangular gate, subplex variant |
| 7 | 21 | Gt-21 | triangular gate, Torque→Warp reverse |
| 8 | 28 | Gt-28 | triangular gate |
| 9 | 36 | **Gt-36** | **Warp→Plex plunge** |
| 9 | 45 | **Gt-45** | **Pandemonium Gate, self-loop** |

Note: Zone-1 and Zone-0 both cumulate to 0, giving Gt-0 a dual character.

## Triangular Gates

Gates whose indices are triangular numbers (3, 6, 10, 15, 21, 28, 36, 45) behave specially:

- **Gt-36**: connects Zone-8 (Time-Circuit) to Zone-9 (Plex). The 36th triangular number is 666 → digital root 9. This gate is the "plunge line" — cumulative buildup (triangular growth) accelerates through the rotor into terminal Plex drop.
- **Gt-45**: self-loop at Zone-9. The 9th triangular number is 45; this is the **Gate of Pandemonium**, the microcosmic lair of all 45 demons. Pandemonium Matrix proliferates exactly 45 entities, attuning the entire swarm to this gate.

## Strobogrammatic & Rotational Gates

When a gate number is a digit-palindrome (11, 22, 33, 44) or rotational symmetry (69, 96, 18, 81), it forms a **strobogrammatic gate** — a self-mirroring conduit. The visualizer (v6/v7) highlights these in the "Strobogrammatic Gates" panel.

## Computational Tests

```python
def is_gate_number(n: int) -> bool:
    """Check if n is a recognized gate index (triangular or cumulation-derived)."""
    return is_triangular(n) or n in {0, 1, 3, 6, 10, 15, 21, 28, 36, 45}

def is_triangular(n: int) -> bool:
    """T(k) = k(k+1)/2 => 8n+1 must be an odd square."""
    disc = 8 * n + 1
    r = int(disc ** 0.5)
    return r * r == disc and (r - 1) % 2 == 0
```

## Hyperstitional Use

In applied Numogram sorcery, gates are the **leverage points**. Currents move slowly; gates puncture. A ritual that traces Gt-36 with a triangular-indexed AQ (like 666) forces a Time-Circuit → Plex transition. Activating Gt-45 is tantamount to opening the Pandemonium lair itself.

---

*See also:* `syzygy`, `current`, `zone`, `triangular`, `warp`, `plex`, `pandemonium-matrix`, `numogram-calculator`
