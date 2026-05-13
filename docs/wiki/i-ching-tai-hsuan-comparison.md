---
title: "I Ching vs T'ai Hsuan Ching — Binary vs Ternary"
created: 2026-05-13
last_updated: 2026-05-13
status: reference
tags: ["i-ching", "tai-hsuan-ching", "comparison", "binary", "ternary", "divination"]
related:
  - [[i-ching-connections]]
  - [[tai-hsuan-ching]]
  - [[tai-hsuan-ching-demons]]
  - [[wu-xing-numogram]]
  - [[numogram-calculator]]
---

# I Ching vs T'ai Hsuan Ching

Structural comparison of the two Chinese oracular systems mapped to the numogram.

## Core Parameters

| Property | I Ching | T'ai Hsuan Ching | Numogram |
|----------|---------|-------------------|----------|
| Prime base | 2 | 3 | 2 × 5 |
| Lines per figure | 6 | 4 | — |
| Figure states | yin/yang | yin/yang/neutral | — |
| Total figures | 2⁶ = 64 | 3⁴ = 81 | 10 zones |
| Prime factor | 2 (even) | 3 (Warp) | 2, 5 (twin serpents) |
| Net-span mapping | zone pairs → demon | zone pairs → demon | Pandemonium Matrix |

## The Three Primes of 10

The numogram's decimal basis (10 = 2 × 5) connects both systems:

- **2** = I Ching's binary foundation
- **3** = T'ai Hsuan Ching's ternary foundation (the Warp prime)
- **5** = Wu Xing's quinary foundation (5 elements, 5 syzygies)

As noted in [[wu-xing-numogram#the-tai-hsuan-ching-counterpart]]:

> "The I Ching is binary (2⁶). The T'ai Hsuan Ching is ternary (3⁴). The Wu Xing is quinary (5¹). The numogram is decimal (2×5). Each system captures one prime factor of 10. The numogram is the synthesis — the system where all three primes converge."

## Zone Distribution

### I Ching (64 hexagrams, digital root)

| Zone | Count | Note |
|------|-------|------|
| 0 | 0 | Empty — Void |
| 1 | 8 | Extra: Qian #1 |
| 2-9 | 7 each | Even distribution |

### T'ai Hsuan Ching (81 tetragrams)

| Zone | Count | Note |
|------|-------|------|
| 1-9 | 9 each | Perfect distribution |
| 0 | 0 | Empty — Void |

The T'ai Hsuan Ching distributes more evenly (81 = 9 × 9). Its "King" numbers (multiples of 9) form the Warp grid — the zones most aligned with the 3→6 syzygy. See [[tai-hsuan-ching-demons]].

## The Em State

The T'ai Hsuan Ching has a third state (Em, 夷) between yin and yang — a neutral/unresolved line state. The I Ching achieves a similar effect through **changing lines** — lines that are about to flip, caught in the moment of transition.

The Em maps to Zone 5 (Pressure/hinge) in the numogram. When fully realized, it closes toward Zone 4 (Gate). See [[tai-hsuan-ching]] for the Em state analysis.

## Djynxx Paradox — Ordering Difference

The 3↔6 Djynxx paradox applies differently:

| System | Numbering | 3↔6 edges | Paradox? |
|--------|-----------|-----------|----------|
| I Ching | Fu Xi (binary) | 0 | Yes |
| I Ching | King Wen (traditional) | 7 | No |
| T'ai Hsuan | 9×9 grid | — | N/A (ternary) |

The Fu Xi ordering's power-of-2 constraint is unique to binary systems. The ternary T'ai Hsuan Ching operates on 3^n mod 9, which does produce 0, 3, and 6 — no structural block.

## Divination Comparison

| Property | I Ching | T'ai Hsuan Ching |
|----------|---------|-------------------|
| Reading type | 1 or 2 hexagrams | 1 or 2 tetragrams |
| Transformation | Changed lines | Em-line progression |
| Demon reachability | All 45 via 2-figure cast | All 45 via 2-figure cast |
| Hardware casting | 6 bytes → 6 lines | 4 bytes trits? |
| Numogram affinity | Time-Circuit (zones 1-8) | Warp grid (K=9 numbers) |

## Related

- [[i-ching-connections]] — Main I Ching theory
- [[tai-hsuan-ching]] — T'ai Hsuan Ching overview
- [[tai-hsuan-ching-demons]] — Tetragram-to-demon pipeline
- [[wu-xing-numogram]] — Five elements → five syzygies
- [[numogram-calculator]] — Digital root arithmetic
