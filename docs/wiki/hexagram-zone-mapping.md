---
title: "Hexagram → Zone Mapping"
created: 2026-05-13
last_updated: 2026-05-13
status: reference
tags: ["i-ching", "hexagram", "numogram", "zone-mapping", "king-wen", "digital-root"]
related:
  - [[i-ching-connections]]
  - [[iching-numogram-casting]]
  - [[hexagram-demon-mapping]]
  - [[wu-xing-numogram]]
---

# Hexagram → Zone Mapping

Complete reference: all 64 King Wen hexagrams mapped to numogram zones via digital root.

## Zone Derivation

Two valid methods exist (see [[i-ching-connections]] for discussion):

### Method A — Canonical Digital Root (preferred)

```
zone = 1 + (KingWen_number - 1) % 9
```

| Zone | Count | Hexagrams (KW#) |
|------|-------|-----------------|
| Zone 0 (Void) | 0 | _no hexagrams_ |
| Zone 1 (Surge) | 8 | 1, 10, 19, 28, 37, 46, 55, 64 |
| Zones 2-8 | 7 each | (see table) |
| Zone 9 (Plex) | 7 | 9, 18, 27, 36, 45, 54, 63 |

Properties: Zone 0 truly empty. Zone 1 gets an extra hexagram (Qian #1). Zone 9 (Plex) is present.

### Method B — Zero-Inclusive (legacy skill doc)

```
zone = (KingWen_number - 1) % 9
```
Remainder 0 → Zone 0, others → zone. Zone 9 gets 0 hexagrams. Qian #1 sits in Zone 0 (Void).

> **See [[i-ching-connections]] → "The Zone Derivation Offset"** for the structural meaning: Method A treats Zone 0 as void (nothing there); Method B treats Zone 0 as origin (Qian/Heaven = the void-point).

## Syzygy-Carrier Reference

| Zone | Syzygy Partner | Carrier Demon | Net-Span |
|------|---------------|---------------|----------|
| 1 | 8 | Murrumur | 29 |
| 2 | 7 | Oddubb | 23 |
| 3 | 6 | Djynxx | 18 |
| 4 | 5 | Katak | 14 |
| 9 | 0 | Uttunul | 36 |

## Complete 64 Hexagram Table

Derived from trigram pairs: `binary = (upper_trigram << 3) | lower_trigram`. Source: corrected table from autonomous session 2026-05-12.

| # | Name | Upper | Lower | Binary | Dec | Zone (DR) | Syzygy | Demon |
|---|------|-------|-------|--------|-----|-----------|--------|-------|
| 1 | Qian | ☰ | ☰ | 111111 | 63 | 9 | 0 | Uttunul |
| 2 | Kun | ☷ | ☷ | 000000 | 0 | 1 | 8 | Murrumur |
| 3 | Zhun | ☵ | ☳ | 010100 | 20 | 2 | 7 | Oddubb |
| 4 | Meng | ☶ | ☵ | 001010 | 10 | 1 | 8 | Murrumur |
| 5 | Xu | ☵ | ☰ | 010111 | 23 | 5 | 4 | Katak |
| 6 | Song | ☰ | ☵ | 111010 | 58 | 4 | 5 | Katak |
| 7 | Shi | ☵ | ☷ | 010000 | 16 | 7 | 2 | Oddubb |
| 8 | Bi | ☷ | ☵ | 000010 | 2 | 2 | 7 | Oddubb |
| 9 | Xiao Chu | ☴ | ☰ | 011111 | 31 | 4 | 5 | Katak |
| 10 | Lu | ☰ | ☱ | 111110 | 62 | 8 | 1 | Murrumur |
| 11 | Tai | ☷ | ☰ | 000111 | 7 | 7 | 2 | Oddubb |
| 12 | Pi | ☰ | ☷ | 111000 | 56 | 2 | 7 | Oddubb |
| 13 | Tong Ren | ☰ | ☲ | 111101 | 61 | 7 | 2 | Oddubb |
| 14 | Da You | ☲ | ☰ | 101111 | 47 | 2 | 7 | Oddubb |
| 15 | Qian (Humble) | ☷ | ☶ | 000001 | 1 | 1 | 8 | Murrumur |
| 16 | Yu | ☳ | ☷ | 100000 | 32 | 5 | 4 | Katak |
| 17 | Sui | ☱ | ☳ | 110100 | 52 | 7 | 2 | Oddubb |
| 18 | Gu | ☶ | ☴ | 001011 | 11 | 2 | 7 | Oddubb |
| 19 | Lin | ☷ | ☱ | 000110 | 6 | 6 | 3 | Djynxx |
| 20 | Guan | ☴ | ☷ | 011000 | 24 | 6 | 3 | Djynxx |
| 21 | Shi He | ☲ | ☳ | 101100 | 44 | 8 | 1 | Murrumur |
| 22 | Bi (Grace) | ☶ | ☲ | 001101 | 13 | 4 | 5 | Katak |
| 23 | Bo | ☶ | ☷ | 001000 | 8 | 8 | 1 | Murrumur |
| 24 | Fu | ☷ | ☳ | 000100 | 4 | 4 | 5 | Katak |
| 25 | Wu Wang | ☰ | ☳ | 111100 | 60 | 6 | 3 | Djynxx |
| 26 | Da Chu | ☶ | ☰ | 001111 | 15 | 6 | 3 | Djynxx |
| 27 | Yi | ☶ | ☳ | 001100 | 12 | 3 | 6 | Djynxx |
| 28 | Da Guo | ☱ | ☴ | 110011 | 51 | 6 | 3 | Djynxx |
| 29 | Kan | ☵ | ☵ | 010010 | 18 | 9 | 0 | Uttunul |
| 30 | Li | ☲ | ☲ | 101101 | 45 | 9 | 0 | Uttunul |
| 31 | Xian | ☱ | ☶ | 110001 | 49 | 7 | 2 | Oddubb |
| 32 | Heng | ☳ | ☴ | 100011 | 35 | 8 | 1 | Murrumur |
| 33 | Dun | ☰ | ☶ | 111001 | 57 | 3 | 6 | Djynxx |
| 34 | Da Zhuang | ☳ | ☰ | 100111 | 39 | 3 | 6 | Djynxx |
| 35 | Jin | ☲ | ☷ | 101000 | 40 | 4 | 5 | Katak |
| 36 | Ming Yi | ☷ | ☲ | 000101 | 5 | 5 | 4 | Katak |
| 37 | Jia Ren | ☴ | ☲ | 011101 | 29 | 2 | 7 | Oddubb |
| 38 | Kui | ☲ | ☱ | 101110 | 46 | 1 | 8 | Murrumur |
| 39 | Jian | ☵ | ☶ | 010001 | 17 | 8 | 1 | Murrumur |
| 40 | Jie (Delivery) | ☳ | ☵ | 100010 | 34 | 7 | 2 | Oddubb |
| 41 | Xin (Decrease) | ☶ | ☱ | 001110 | 14 | 5 | 4 | Katak |
| 42 | Sheng (Increase) | ☴ | ☳ | 011100 | 28 | 1 | 8 | Murrumur |
| 43 | Guai | ☱ | ☰ | 110111 | 55 | 1 | 8 | Murrumur |
| 44 | Gou | ☰ | ☴ | 111011 | 59 | 5 | 4 | Katak |
| 45 | Cui | ☱ | ☷ | 110000 | 48 | 3 | 6 | Djynxx |
| 46 | Sheng (Ascend) | ☷ | ☴ | 000011 | 3 | 3 | 6 | Djynxx |
| 47 | Kun (Oppress) | ☱ | ☵ | 110010 | 50 | 5 | 4 | Katak |
| 48 | Jing (Well) | ☵ | ☴ | 010011 | 19 | 1 | 8 | Murrumur |
| 49 | Ge (Revolt) | ☱ | ☲ | 110101 | 53 | 8 | 1 | Murrumur |
| 50 | Ding | ☲ | ☴ | 101011 | 43 | 7 | 2 | Oddubb |
| 51 | Zhen | ☳ | ☳ | 100100 | 36 | 9 | 0 | Uttunul |
| 52 | Gen | ☶ | ☶ | 001001 | 9 | 9 | 0 | Uttunul |
| 53 | Jian (Grad.Prog) | ☴ | ☶ | 011001 | 25 | 7 | 2 | Oddubb |
| 54 | Guimei | ☳ | ☱ | 100110 | 38 | 2 | 7 | Oddubb |
| 55 | Feng | ☳ | ☲ | 100101 | 37 | 1 | 8 | Murrumur |
| 56 | Lue (Travel) | ☲ | ☶ | 101001 | 41 | 5 | 4 | Katak |
| 57 | Xun | ☴ | ☴ | 011011 | 27 | 9 | 0 | Uttunul |
| 58 | Dui | ☱ | ☱ | 110110 | 54 | 9 | 0 | Uttunul |
| 59 | Huan | ☴ | ☵ | 011010 | 26 | 8 | 1 | Murrumur |
| 60 | Jie (Limit) | ☵ | ☱ | 010110 | 22 | 4 | 5 | Katak |
| 61 | Zhong Fu | ☴ | ☱ | 011110 | 30 | 3 | 6 | Djynxx |
| 62 | Xiao Guo | ☳ | ☶ | 100001 | 33 | 6 | 3 | Djynxx |
| 63 | Ji Ji | ☵ | ☲ | 010101 | 21 | 3 | 6 | Djynxx |
| 64 | Wei Ji | ☲ | ☵ | 101010 | 42 | 6 | 3 | Djynxx |

## Changing Lines Network

Each hexagram has 6 single-line changes. Total: 64 × 6 / 2 = **192 edges**.

### King Wen: all 5 syzygies are reachable

| Syzygy | Single-bit edges | Status |
|--------|-----------------|--------|
| 1↔8 (Murrumur) | 7 | ✅ |
| 2↔7 (Oddubb) | 6 | ✅ |
| 3↔6 (Djynxx) | 7 | ✅ |
| 4↔5 (Katak) | 4 | ✅ |
| 0↔9 (Uttunul) | N/A (0 hexagrams in Zone 0) | — |

### Fu Xi: the Djynxx Paradox

When hexagrams are numbered by their binary value (Fu Xi/prior heaven), `2^k mod 9` never produces 0, 3, or 6. The 3↔6 syzygy has **ZERO** single-bit edges — structurally blocked. See [[i-ching-connections#the-djynxx-paradox]].

> The paradox is ordering-dependent, not a universal oracle law.

## Trigram Pair Matrix

8×8 trigram grid. Each row is the zone sequence shifted by one. Right = −1 zone; down = −8; right-diagonal = −9 (same zone). See [[i-ching-connections#trigram-pair-matrix]] in the main I Ching page.

## Related

- [[i-ching-connections]] — Theory, twin serpents, Time-Circuit as hexagram kernel, hardware entropy
- [[iching-numogram-casting]] — Skill: complete casting pipeline
- [[hexagram-demon-mapping]] — Two-hexagram → demon casting (all 45 demons reachable)
- [[wu-xing-numogram]] — Trigram elemental associations
- [[numogram-audio-empirical-findings]] — Audio measurement results (I Ching zone traversal)
- [[tai-hsuan-ching-demons]] — 81 tetragram counterpart
