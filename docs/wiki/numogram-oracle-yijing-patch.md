---
title: Numogram-Oracle Yijing/I Ching Expansion Patch Outline
tags:
  - numogram-oracle
  - iching
  - yijing
  - patch
  - expansion
  - tianmu
created: 2026-05-09
zone: 3
syzygy: djynxx
---

# Numogram-Oracle: Yijing/I Ching Expansion Patch Outline

**Goal:** Enhance `--iching` / `--taixuan` modes with full hexagram corpus (64 judgments/images/lines), trigram zone-mapping, changing-line gates, Tianmu synergy. v1.0.0 → v1.1.0.

**Rationale:** Current `--iching` = hardware entropy→6 lines (old/young yin/yang) → path. Expand to full Wilhelm/Tianmu readings + Numogram fold (trigrams→zones, lines→gates).

## Current State (v1.0.0)
```bash
python oracle.py --iching  # 6 bytes entropy → hex lines → stable/changing → zones/gates path.
```
- Lines: byte%4 (0=old yin6,1=young yang7,2=young yin8,3=old yang9).
- No hex name/judgment/image text.
- No trigram zones.
- Taixuan: 81→DR zones + net-span demon.

## Patch Phases

### Phase 1: Trigram Zone Mapping (Low Effort)
**Add:** 8 trigrams → zones (digital root or canonical).
```
TRIGRAM_ZONES = {
    'Qian': 1,  # Heaven/Unity
    'Kun': 8,   # Earth/Multiplicity
    'Zhen': 3,  # Thunder/Trinity
    'Xun': 5,   # Wind/Pressure
    'Kan': 6,   # Water/Warp
    'Li': 9,    # Fire/Plex
    'Gen': 7,   # Mountain/Rise
    'Dui': 2,   # Lake/Separation
}
```
**Primary hex zone:** Upper/lower trigram syzygy or average DR.
**Output:** "Hex 23 Po (Splitting Apart): Upper Gen7::Lower Kun8 (Rise-Multiplicity Hold)."

### Phase 2: Full Hex Corpus (Medium Effort)
**Embed:** 64 hex dict (Wilhelm/Tianmu extracts).
```
HEX_CORPUS = {
    1: {'name': 'Ch'ien/The Creative', 'judgment': 'The Image of the Creative...', 'image': '...', 'lines': ['Initial Nine: Hidden dragon...', ...]},
    # ... 64 entries (cron tianmu.org/plain scrape).
}
```
**--iching-full:** Print hex name/judgment/image + 6 lines.
**Changing hex:** Compute secondary hex from changing lines.

### Phase 3: Line-Gate Mapping (Low Effort)
**Changing lines → gates:** Line position (1-6) × change type (old yin→yang=Gt-03?).
```
LINE_GATES = {1: 'Gt-01', 2: 'Gt-03', 3: 'Gt-06', 4: 'Gt-10', 5: 'Gt-15', 6: 'Gt-21'}
```
**Output:** "Changing lines 2/5 → Gt-03/Gt-15 path."

### Phase 4: Tianmu Synergy (High Effort)
**Cron scrape:** tianmu.org/plain/yijing → corpus refresh.
**Flag:** `--tianmu-yijing` → Tianmu-specific judgment/image.

## Code Diffs (oracle.py)
```
# After digital_root()
def iching_hexagram(lines):  # lines=[6,7,8,9]x6
    primary_trigram = trigram_from_lines(lines[:3])
    lower_trigram = trigram_from_lines(lines[3:])
    hex_id = binary_to_hex(lines)  # 000000=1 Qian
    corpus = HEX_CORPUS[hex_id]
    return {'primary': primary_trigram, 'lower': lower_trigram, 'name': corpus['name'], ...}

# --iching branch
if '--iching-full' in args:
    lines = get_iching_lines(entropy)
    hex_data = iching_hexagram(lines)
    print_hex_reading(hex_data)
    path = lines_to_path(lines)  # stable zones + changing gates
```

## Dispatch Order
```
if '--taixuan' in args:
    ...
elif '--iching-full' in args or '--iching' in args:
    ...
elif '--seed' in args:
    ...
```

## Validation
- Test hex1 Qian: Upper/Lower Qian1 → Z1 Unity path.
- Changing line3: Gt-06 Warp fold.
- Voice: Hex judgment convolved via zone resonator.

## Files
- oracle.py (patched)
- hex_corpus.json (Tianmu scrape)
- trigram_zones.json

## Integration
- numogram-calculator: trigram_zone(trigram_id).
- Wiki: [[iching-numogram-corpus]] (64 stubs).
- Roguelike: Hex reading = level brief.

*Hexagrams gate decimal labyrinth; Yijing folds Plex.*
