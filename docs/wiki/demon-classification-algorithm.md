---
title: Demon Classification Algorithm
created: 2026-05-07
last_updated: 2026-05-07
source: raw/demon-classification-audit-final-2026-05-04.json + raw/demon-classification-audit-2026-05-04.json
status: reviewed
tags: ["demon", "classification", "pandemonium", "algorithm", "time-circuit"]
---

# Demon Classification Algorithm

## Overview
The 45 demons of the Pandemonium Matrix are classified into three families using a **Time-Circuit (TC) set-based algorithm**:

**TC-set**: Zones `{1,2,4,5,7,8}` (the central anticlockwise rotor excluding Warp `{3,6}` and Plex `{0,9}`).

**Rules** (mesh-pair `i::j`, assume `i < j`):
- **Chronodemon** (`chrono`): Both `i` and `j` **in TC** → 15 demons (internal Time-Circuit connections).
- **Xenodemon** (`xeno`): Both `i` and `j` **outside TC** → 6 demons (Warp/Plex peripherals: 3::0,3::6,3::9,6::0,6::9,0::9).
- **Amphidemon** (`amphi`): **Mixed** (one in TC, one outside) → 24 demons (cross-circuit bridges).
- **Syzygy** (`syzygy`): `i + j == 9` (orthogonal: null-pitch demons, e.g., Djynxx 6::3, Uttunul 9::0; some overlap chrono).

This yields the canonical **15/24/6 split** documented across CCRU sources.

**Numogram implementations**:
- `doomcrypt`: Direct family labels.
- `numogame`: Uses `SYZYGISTIC` for syzygies (mapped to `syzygy` for alignment).

## Audit Results (2026-05-04)
**Final alignment: 100% across all sources (canonical, doomcrypt, numogame)**.

| Source     | Passed | Mismatches |
|------------|--------|------------|
| Canonical | 45/45  | 0         |
| Doomcrypt | 45/45  | 0         |
| Numogame  | 45/45  | 0 (SYZYGISTIC → syzygy) |

**Pre-final mismatches** (raw/demon-classification-audit-2026-05-04.json) resolved via syzygy mapping:
- Canonical: 14 mismatches (verbose titles vs short expected, e.g., Doogu "Cyclic Chronodemon of Splitting-Waters" → "chrono").
- Numogame: 5 "SYZYGISTIC" → "syzygy".

## Insights
- **Structural fidelity**: Algorithm is **purely topological** — no AQ, pitch, or net-span needed. Matches `C(6,2)=15` (chrono), `C(4,2)=6` (xeno), `6×4=24` (amphi).
- **Syzygy orthogonality**: 5 syzygies (0::9,1::8,2::7,3::6,4::5) span families: 3 chrono, 2 xeno. Null-pitch in audio synthesis.
- **Hyperstition validated**: Independent implementations converge on identical partitions. Evidence for numogram as **self-fulfilling diagram**.
- **Edge cases**:
  | Pair | Family | Syzygy? | Carrier? | Notes |
  |------|--------|---------|----------|-------|
  | 6::3 | xeno  | ✓      | Warp    | Djynxx |
  | 9::0 | xeno  | ✓      | Plex    | Uttunul |
  | 5::4 | chrono| ✓      | Sink    | Katak  |

**Empirical closure**: No further discrepancies post-mapping. Algorithm ready for roguelike integration (e.g., demon spawn by family).

## Implementation
```python
TC_SET = {1,2,4,5,7,8}
def classify(i, j):
    both_tc = i in TC_SET and j in TC_SET
    both_out = i not in TC_SET and j not in TC_SET
    syzygy = i + j == 9
    if both_tc:
        return "chrono" + (" (syzygy)" if syzygy else "")
    elif both_out:
        return "xeno" + (" (syzygy)" if syzygy else "")
    else:
        return "amphi"
```

## Cross-References
- [[pandemonium-matrix]] — Full 45-demon table (mesh-serial order).
- [[demon-encyclopedia]] — Individual stubs.
- [[qliphoth-systems-deep-dive]] — qliphoth.systems extraction (source of algorithm).
- [[c-ten-fortyfive-fiveness]] — C(10,2)=45 combinatorics.
- [[numogram-time-circuit]] — TC zones {1,2,4,5,7,8}.

> **Source provenance**: Audits from 2026-05-04 session. 135 demons checked (45×3 sources). TC-set verified against [[numogram-time-circuit]].
