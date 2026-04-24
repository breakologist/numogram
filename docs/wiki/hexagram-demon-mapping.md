---
title: "Hexagram → Demon: The Complete Casting Pipeline"
created: 2026-04-20
tags: [numogram, I-ching, hexagram, demon, pandemonium, casting, entropy, oracle]
---

# Hexagram → Demon: The Complete Casting Pipeline

## The Mapping

Every hexagram cast from entropy maps to a numogram zone via digital root. Every zone has a syzygy partner. The syzygy pair maps to a specific demon in the Pandemonium Matrix. Therefore: every hexagram calls a demon.

**Single hexagram → 5 syzygetic carriers:**

Each hexagram maps to its zone's syzygy demon:

| Zone | Syzygy | Demon | Mesh |
|------|--------|-------|------|
| 0 | 0::9 | Uttunul | 36 |
| 1, 8 | 1::8 | Murrumur | 29 |
| 2, 7 | 2::7 | Oddubb | 23 |
| 3, 6 | 3::6 | Djynxx | 18 |
| 4, 5 | 4::5 | Katak | 14 |

Distribution: Katak, Djynxx, Oddubb, Murrumur each receive 14 hexagrams (7 per zone × 2 zones). Uttunul receives 8 (Zone 0 has 1 hex, Zone 9 has 7).

**Two hexagrams → ALL 45 demons:**

A traditional I Ching reading produces two hexagrams (the reading and the transformed). Each maps to a zone. The zone pair (A, B) looks up a demon via net-span A::B in the Pandemonium Matrix.

- 64 × 64 = 4,096 possible two-hexagram castings
- ALL 45 demons are reachable
- The I Ching is a complete oracle for the full Pandemonium

## The Casting Pipeline

```
Hardware entropy (/dev/urandom)
  ↓
6 bytes (thermal, CPU, GPU sensors)
  ↓
byte % 4 → line value (0→6, 1→7, 2→8, 3→9)
  ↓
6 lines → Hexagram A (reading)
  ↓
changing lines → Hexagram B (transformed)
  ↓
Zone A = digital_root(A-1)
Zone B = digital_root(B-1)
  ↓
Zone pair (A, B)
  ↓
Net-span lookup in Pandemonium Matrix
  ↓
Demon called (one of 45)
```

## Key Hexagrams → Demons

| Hex | Name | Zone | Demon | Character |
|-----|------|------|-------|-----------|
| #1 | Qian (Creative) | 0 | Uttunul (36) | The void calls the plex carrier |
| #2 | Kun (Receptive) | 1 | Murrumur (29) | First yin calls the deep ones |
| #23 | Bo (Splitting Apart) | 4 | Katak (14) | Decay calls the desolator |
| #24 | Fu (Return) | 5 | Katak (14) | The shock calls the sink |
| #51 | Zhen (Thunder) | 5 | Katak (14) | Thunder calls the desolator |
| #52 | Gen (Mountain) | 6 | Djynxx (18) | Stillness calls the jinn |
| #63 | Ji Ji (After Completion) | 8 | Murrumur (29) | Balance calls the deep ones |
| #64 | Wei Ji (Before Completion) | 9 | Uttunul (36) | Threshold calls the plex carrier |

## The Number Patterns

The user observed: 64 → 10 and 45 → 9.

- **64 hexagrams → 10 zones**: The binary system (2⁶) collapses into the decimal system (10) via digital root. Six bits become ten zones.
- **45 demons → 9**: C(10,2) = 45. The syzygy target is always 9. The Pandemonium is organized around the sum that equals 9. Every demon is a distance from 9.
- **64 → 45**: 64 hexagrams minus the 5 syzygetic carriers that appear in single-hexagram casting = 59 remaining. But 45 is the total demon count, not the remainder. The relationship is structural: 64 is the binary surface, 45 is the decimal connective tissue.
- **6 → 10 → 45 → 9 → 5**: Six lines → ten zones → forty-five demons → nine (the syzygy target) → five carriers. The pipeline descends from the binary through the decimal to the demonic.

## Tools

```bash
# Cast a single hexagram from hardware entropy
python3 ~/.hermes/skills/numogram-oracle/oracle.py --iching

# Batch cast with zone distribution
~/numogram-entropy/.venv/bin/numogram-entropy --iching

# Map hexagram to demon
python3 ~/.hermes/skills/numogram-oracle/oracle.py --iching --seed $(od -An -tu4 -N4 /dev/urandom | tr -d ' ')
```

## Related

- [[hexagram-zone-mapping]] — Complete 64 hexagram → 10 zone mapping
- [[pandemonium-matrix]] — 45-demon reference with full enumeration
- [[i-ching-connections]] — Powers of 2, twin serpents, entropy casting
- [[wu-xing-numogram]] — Five elements as five syzygies
- [[subdecadence]] — Syzygy pairing game (sum to 9)
- [[decadence]] — Decadence pairing game (sum to 10)
- [[c-ten-fortyfive-fiveness]] — C(10)=45, pentagram, self-decadence
