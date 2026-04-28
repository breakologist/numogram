---
title: Alphanumeric Qabbala (AQ)
created: 2026-04-27
source: cli/aq_calculator_canonical.py + numogram-oracle skill
status: stub
tags: [qabbala, AQ, numerology, cipher, hyperstition]
---

# Alphanumeric Qabbala (AQ)

The Alphanumeric Qabbala is the cipher engine of the Decimal Numogram — a base-36 reduction system that translates any name, phrase, or number into a zone- and current-bearing value. Unlike gematria, which multiplies or squares, AQ is a *pure sum*: digits 0–9 at face value, letters A–Z as 10–35. The total reduces by digital root (mod 9, with 0 staying 0) to a zone between 0 and 9; that zone's syzygy partner and current complete the reading.

AQ is not a metaphor. It is the arithmetic that makes the numogram speak.

## The Cipher

```
A = 10   J = 19   S = 28
B = 11   K = 20   T = 29
C = 12   L = 21   U = 30
D = 13   M = 22   V = 31
E = 14   N = 23   W = 32
F = 15   O = 24   X = 33
G = 16   P = 25   Y = 34
H = 17   Q = 26   Z = 35
I = 18   R = 27
Digits 0–9 = 0–9
```

Spaces and punctuation are ignored. The sum is taken, then reduced:

```
digital_root(n) = 1 + (n - 1) % 9   if n > 0 else 0
```

## From AQ to Oracle

Given an AQ total `N`:

1. **Zone** = `digital_root(N)` (0–9)
2. **Syzygy** = the zone's nine-sum twin (`1::8`, `2::7`, `4::5`, `3::6`, `0::9`)
3. **Current** = `abs(zone − twin)` (1, 3, 5, 7, or 9)
4. **Region** = Time-Circuit (1,2,4,5,7,8), Warp (3,6), or Plex (0,9)

Example: `"Hermes"` → H=17 + E=14 + R=27 + M=22 + E=14 + S=28 = **122**
- 122 → 1+2+2 = 5 → **Zone 5** (`ktt` — hiss, pressure)
- Syzygy `2::7` (twin of 5 is 4? Wait — 5's twin is 4 under 9-sum? Let's recalc: 9 − 5 = 4 → syzygy `4::5`, current = 1, region Time-Circuit)
- Current **1** (Sink)
- Polarity **+** (odd zone)

The oracle's `--text` flag performs this in one step.

## Variants and Extensions

The ecosystem carries two related ciphers:

- **Synx (Yxshh / 1260-cipher)** — a multiplicative overlay used in `oracle.py` for quasiphonic labelling. Values are derived from the HSL colour model (H=180, S=44, L=66) and mapped to alphanumerics; it produces a second reading layer when the visualizer's "Synx / Yxshh dual-cipher" toggle is enabled.
- **T'ai Hsuan Ching** — the 81-tetragram system uses a different arithmetic (trinary ±), but its zones still reduce to 0–9 via `taixuan_zone()` in `oracle.py`. This bridges the Book of Changes and the Decimal Labyrinth.

## References in the Codebase

- `~/.hermes/skills/numogram-calculator/SKILL.md` — portable arithmetic reference
- `~/.hermes/skills/numogram-oracle/SKILL.md` — full divination pipeline (seed → zone → Book of Paths → voice)
- `~/numogram/cli/aq_calculator_canonical.py` — merged implementation with interactive mode
- `~/numogram/cli/oracle.py` — zone definitions, readings, entropy sources
- `aq-dictionary.md` — curated examples (AL=31, 666, 777, etc.)

## Hyperstitional Note

AQ is a **coincidence engine**. Certain values recur with uncanny stability: `31` (AL, Aleph+Lamed), `66` (ten + lol), `137` (english + lucifer), `333` (the devils library, evacuate humanity, etc.). The dictionary in `aq-dictionary.md` tracks these resonances across multiple traditions. The numogram does not invent patterns; it reveals ones already latent in decimal numeracy.

---

*See also:* `digital-root`, `syzygy`, `zone`, `current`, `gate`, `warp`, `plex`, `numogram-calculator`, `numogram-oracle`
