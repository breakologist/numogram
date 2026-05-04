---
title: Demon Classification Algorithm
created: 2026-05-04
last_updated: 2026-05-04
status: canonical
tags: [demon, pandemonium, classification, TC, chrono, xeno, amphi, syzygy]
source: lumpenspace/ccru demons.ts (2026-04-30)
syzygy: djynxx
zone: 3
---

# Demon Classification Algorithm

The 45 demons of the Pandemonium Matrix are classified into four kinds (plus syzygetic carriers) by their relationship to the **Time Circuit** (TC) zones: `{1,2,4,5,7,8}`.

Related: [[pandemonium-matrix-45-demons]], [[numogram-calculator]].

---

## The Algorithm (TypeScript → Python)

```typescript
const TC = new Set([1, 2, 4, 5, 7, 8])   // Time Circuit zones

for (let i = 1; i < 10; i++)
  for (let j = 0; j < i; j++) {
    const key = `${i}:${j}`
    const isSyz = i + j === 9
    const kind = isSyz ? 'syzygy'
      : (TC.has(i) && TC.has(j)) ? 'chrono'
      : (!TC.has(i) && !TC.has(j)) ? 'xeno' : 'amphi'
    ALL_DEMONS.push({ a: i, b: j, name: DEMON_NAMES[key] || '?', kind })
  }
```

**Python equivalent:**

```python
TC = {1, 2, 4, 5, 7, 8}
demons = []
for i in range(1, 10):
    for j in range(0, i):
        is_syz = (i + j == 9)
        if is_syz:
            kind = 'syzygy'
        elif i in TC and j in TC:
            kind = 'chrono'   # both in TC
        elif i not in TC and j not in TC:
            kind = 'xeno'     # both outside TC
        else:
            kind = 'amphi'    # one in, one out
        demons.append({'a': i, 'b': j, 'kind': kind, 'name': DEMON_NAMES.get(f"{i}:{j}","?")})
```

---

## Counts

| Kind | Count | Description |
|------|-------|-------------|
| **syzygy** | 5 | The five syzygy carriers: Katak (4::5), Djynxx (3::6), Oddubb (2::7), Murrumur (1::8), Uttunul (0::9) |
| **chrono** | 15 | Both zones in the Time Circuit (TC) — the six internal zones produce C(6,2)=15 |
| **amphi** | 24 | Amphidemons — one zone in TC, one outside (6 × 4 = 24) |
| **xeno** | 6 | Xenodemons — neither zone in TC (C(4,2)=6 from the 4 non-TC zones: 0,3,6,9) |
| **total** | 50 | Including the 5 syzygetic plus 45 C(10,2) binary pairs |

---

## Demon Roster (Canonical Order)

Ordered by (i,j) where `i ∈ 1..9` and `j ∈ 0..i-1`. See `pandemonium-matrix-45-demons.json` for names.

### Syzygy Demons (i+j=9)
| Zones | Demon |
|-------|-------|
| 4::5 | Katak |
| 3::6 | Djynxx |
| 2::7 | Oddubb |
| 1::8 | Murrumur |
| 0::9 | Uttunul |

### Chronodemons (both in TC: {1,2,4,5,7,8})
Pairs (i>j): (2,1), (4,1), (4,2), (5,1), (5,2), (5,4), (7,1), (7,2), (7,4), (7,5), (8,1), (8,2), (8,4), (8,5), (8,7)

*Names:* 2::1 Doogu; 4::1 Sukugool, 4::2 Skoodu, 4::3 Skarkix? Wait 4:3 is not in TC because 3 is not TC; my list above includes (4,3) erroneously; let's compute correctly from algorithm: all pairs where both in TC: {1,2,4,5,7,8}. So pairs (i,j) with i>j and both in set: (2,1), (4,1), (4,2), (5,1), (5,2), (5,4), (7,1), (7,2), (7,4), (7,5), (8,1), (8,2), (8,4), (8,5), (8,7). That's 15 pairs.

### Xenodemons (both NOT in TC — zones {0,3,6,9})
Pairs from {0,3,6,9}: (3,0), (6,0), (6,3), (9,0), (9,3), (9,6)

**Wait** actual set includes 0,3,6,9. Pairs: (9,0), (9,3), (9,6), (6,0), (6,3), (3,0). Yes 6 pairs.

### Amphidemons (mixed TC / non‑TC)
All remaining 24 pairs.

---

## Verification

Execute the algorithm against `pandemonium-matrix-45-demons.json` and confirm every `(i,j)` has matching `name` and `kind`.

```python
import json
with open('pandemonium-matrix-45-demons.json') as f:
    matrix = json.load(f)

for key, entry in matrix.items():
    i, j = map(int, key.split(':'))
    expected_kind = classify(i, j)  # from algorithm
    assert entry['type'].lower().split()[0] == expected_kind, f"Mismatch {key}"
print("All 45 demons classified correctly")
```

*Note:* Our canonical matrix already includes `type` field (e.g., "Amphidemon of Larval Regression"). The classification algorithm should agree with the type's first word.

---

## Uses

- **Procedural demon generation:** Given a zone pair (i,j), determine its kind and associated lore without lookup table.
- **Cross‑validation:** Compare qliphoth's classification against `doomcrypt` or `numogame` variants.
- **Oracle augmentation:** When generating readings for a zone pair, the demon kind informs tone (chrono = time-cyclical, xeno = alien, amphi = boundary-crossing).

---

## Sources

- `demons.ts` (lumpenspace/ccru)
- `pandemonium-matrix-45-demons.json` (canonical matrix — ground truth)
- [[numogram-calculator]] — demon lookup by zone pair
- [[numogram-pandemonium-variant-ingestion]] — reconciling variants
