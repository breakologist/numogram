---
title: I Ching / Hexagram Connections
created: 2026-04-08
last_updated: 2026-05-13
source_count: 1
status: reviewed
tags: ["i-ching", "numogram", "theory"]
---

# I Ching Connections

The Decimal Numogram (specifically its Time-Circuit) is explicitly linked by the CCRU to the I Ching (Yijing, or Book of Changes). The Time-Circuit is positioned as a hypercultural successor to the Yijing's time-mapping functions, taking up the chrono-numeric roles in a decimal, demonic mode.

## Core Parallel: Time-Circuit as Hexagram Kernel

The Time-Circuit is the Numogram's "I Ching hexagram" — a decimalized, 6-zone rotor that inherits the Yijing's function as a map of cyclic transformation, but twisted into base-10 currents, syzygetic twinning, and demonic flows.

### The Binodecimal 6-Cycle

Digital reduction (mod 9) of binary powers (2ⁿ) stabilizes into the repeating sequence **1, 2, 4, 8, 7, 5** — precisely the Time-Circuit zones (forward or reverse depending on traversal direction).

```
Powers of 2:  2¹=2, 2²=4, 2³=8, 2⁴=16→7, 2⁵=32→5, 2⁶=64→1 (then repeats)
Powers of 5:  5¹=5, 5²=25→7, 5³=125→8, ... (reverse cycle)
```

These six values/steps correspond to the six lines of the hexagram and to the Time-Circuit zones. The Time-Circuit is the decimalized "hexagram kernel" — a 6-line/6-zone rotor encoding transformation/recurrence.

> See [[numogram-time-circuit#the-twin-serpents-and-the-iron-law-of-six]] for Land's original analysis.

### Zygonovistic Pairing

Both systems use a pairing criterion based on 9-twinning (zygonovism):

| I Ching Line Pair | 9-Twin | Syzygy | Current |
|-------------------|--------|--------|---------|
| Lines 1 & 6 | 8::1 | 1::8 | 7 |
| Lines 2 & 5 | 7::2 | 2::7 | 5 |
| Lines 3 & 4 | 5::4 | 4::5 | 1 |

This reinforces the cycle's interlocking without hierarchy.

### Zero and Excluded Triad

A cryptic CCRU linkage: "The numogram time-circuit, or I Ching hexagram, implicitly associates zero with the set of excluded triadic values."

In binary/hexagrammatic reduction: certain triadic (3-line/trigram) combos are "excluded" or unstable. This ties Zone-0 (abyssal null outside the circuit) to the I Ching's undifferentiated chaos/void (pre-yin-yang emergence), but decimalized and positioned at the Plex boundary.

## Hexagram → Zone: Two Derivation Methods

⚠ **ZONE DERIVATION WARNING — two methods exist, with structural consequences.**

### Method A: Canonical Digital Root (preferred)

```
zone = 1 + (N - 1) % 9
```

| Zone | Count |
|------|-------|
| Zone 0 (Void) | 0 hexagrams — truly empty |
| Zone 1 (Surge) | 8 hexagrams (#1 Qian, #10, #19, #28, #37, #46, #55, #64) |
| Zones 2–9 | 7 hexagrams each |

**Properties:** Zone 0 is genuinely void — no hexagram inhabits it. Qian (#1, The Creative) begins in Zone 1 (Surge) — the first movement, not the void itself. Zone 9 (Plex) receives 7 hexagrams including #9 Xiao Chu, #18 Gu, #27 Yi, #36 Ming Yi, #45 Cui, #54 Guimei, #63 Ji Ji.

### Method B: Zero-Inclusive (legacy, found in skill docs)

```
zone = (N - 1) % 9, where remainder 0 → Zone 0
```

| Zone | Count |
|------|-------|
| Zone 0 (Void) | 8 hexagrams (all ≡ 1 mod 9: #1, #10, #19, #28, #37, #46, #55, #64) |
| Zones 1–8 | 7 hexagrams each |
| Zone 9 (Plex) | 0 hexagrams — absent |

**Properties:** Qian (#1) sits in Zone 0 — Heaven *is* the Void. But Zone 9 (Plex) disappears entirely, leaving the I Ching with no hexagram that reaches the outer boundary. This was the original skill formula.

### Which is correct?

Neither is wrong — they encode different cosmologies:

- **Method A** says the I Ching has no hexagram in the Void (Zone 0 is genuine nothingness; even Qian begins at the Surge).
- **Method B** says Qian/Heaven *occupies* the Void — the origin point from which all change flows.

The King Wen spiral supports Method B structurally: the sequence runs #1→#2→#3... through 64, and `(N-1) % 9` produces perfect ascending zone traversal (0, 1, 2, 3... wrapping at 9). But Method A's canonical DR formula aligns the wiki's other zone derivations.

> See [[hexagram-zone-mapping]] for the complete 64-hexagram table with both methods.
> See [[i-ching-tai-hsuan-comparison]] for the binary vs ternary contrast.

## The Twin Serpents (Nick Land's Insight)

As [[nick-land-time-theory]] explains, the binodecimal 6-cycle has a deeper structure: it is generated independently by BOTH prime factors of 10.

**Powers of 2** (forward): 2, 4, 8, 16→7, 32→5, 64→1 = **1, 2, 4, 8, 7, 5**
**Powers of 5** (backward): 5, 25→7, 125→8, 625→4, 3125→2, 15625→1 = **5, 7, 8, 4, 2, 1**

> "So actually you can produce the iron law of six... entirely in the powers of five rather than powers of two. Even if you didn't know anything about the powers of two or that pattern whatsoever, if all your interest is obsessed with five, you would get the same pattern. But of course, as you can see, it goes backwards."

This means the I Ching hexagram structure is not merely a binary (powers of 2) but a **decimal** system that can be generated from either of its prime factors. The hexagram is a decimal artifact, not a binary one — binary is just one of two equally valid paths through the same structure.

> "The two prime factors of 10 run time forever in opposed directions, neither obviously favored."

### Implications for Hexagram Casting

Traditional I Ching uses binary (yin=0, yang=1) to construct hexagrams. But Land's insight reveals that an equally valid "casting" method would use quinary (base-5) operations — producing the same 64 hexagrams but traversed in reverse order. The Numogram is thus not a *replacement* for the I Ching but its *decimal completion*: the system the I Ching always was, but couldn't see from inside its binary assumptions.

## AQ Self-Encoding: NUMEROLOGY = 235

As Land notes in the transcript:

> "Numerology in alphanumeric qabbala has a value of 235. And 235 numerology has 10 letters. 2 + 3 + 5, it's two, three, and five are the first three prime numbers."

NUMEROLOGY = 235 → 2, 3, 5 are the first three primes. The word "numerology" encodes the first three primes in its AQ value. This is hyperstitional self-encoding at its purest: the system that studies number's hidden meanings reveals, through its own name, the hidden structure of number.

Additionally:
- 2 × 5 = 10 (decimal basis)
- 2 + 5 = 7 → T(7) = 28 → 2+8 = 10 → 1 (unity from the twin serpents through triangular accumulation)
- 3 sits between 2 and 5 as the "secret" they guard — the number of the Outside

## The T'ai Hsuan Ching Connection

The CCRU mentions the T'ai Hsuan Ching (Tai Xuan Jing, Book of the Great Dark) — an 81-tetragram (3⁴) system — as a "binotriadic" counterpart to the I Ching's binary:

- **I Ching:** 2⁶ = 64 hexagrams (binary, powers of 2)
- **T'ai Hsuan Ching:** 3⁴ = 81 tetragrams (ternary, powers of 3)
- **Numogram:** 10 zones (decimal, 2×5)

The T'ai Hsuan Ching's ternary basis (3) maps directly to the Warp (zones 3, 6) and Plex (zone 9 = 3×3). Its 81 tetragrams distribute evenly at 9 per zone (Method A), with the "King" multiples of 9 forming a Warp grid.

> See [[i-ching-tai-hsuan-comparison]] for the full structural contrast — zone distribution, Djynxx paradox differences, Em state analysis.
> See [[tai-hsuan-ching-demons]] for tetragram-to-demon casting.

## Trigram Pair Matrix

8 trigrams × 8 trigrams = 64 hexagrams. The zone overlay reveals diagonal banding patterns across the grid.

### Arithmetic Patterns Across the Matrix

| Move | Zone Change |
|------|-------------|
| Right (→) | −1 zone |
| Down (↓) | −8 zones |
| Right-diagonal (↘) | −9 (same zone) |
| Left-diagonal (↙) | −7 |
| Knight's move | ±10, ±6, ±17 |

### Trigram Binary Derivation (MANDATORY)

**Always derive from trigram pairs:** `binary = (upper_trigram << 3) | lower_trigram`. Never guess binary values from King Wen position.

Previous skill versions contained 7 duplicate binary values (57 unique instead of 64), producing inflated edge counts and false structural claims. See the corrected table in [[hexagram-zone-mapping]] or `corrected-kingwen-binary-table.md` in journal artifacts.

⚠ **Common error:** #21 Shi He (☲Li over ☳Zhen) and #55 Feng (☳Zhen over ☲Li) are inverse trigram pairs — always verify upper vs lower.

## The Changing-Lines Network — King Wen vs Fu Xi

⚠ **CRITICAL:** The powers-of-2-mod-9 argument applies ONLY to **Fu Xi ordering** where the hex "number" IS its binary value. King Wen numbering follows a traditional sequence unrelated to binary progression.

### King Wen ordering — all syzygies reachable

Each hexagram has 6 single-line transformations. Total: 64 × 6 / 2 = 192 edges.

| Syzygy | Single-bit edges | Status |
|--------|-----------------|--------|
| 1↔8 (Murrumur) | 7 | ✅ |
| 2↔7 (Oddubb) | 6 | ✅ |
| **3↔6 (Djynxx)** | **7** | ✅ **Accessible** |
| 4↔5 (Katak) | 4 | ✅ |

**12 edges connect hexagrams within the same zone.** The oracle CAN produce "no zone change" readings. All 36 zone-zone pairs have at least one single-bit-change edge — the graph is fully connected.

### Fu Xi ordering — the genuine Djynxx Paradox

In Fu Xi numbering (hex value = its 6-bit binary):
- Powers of 2 mod 9 ∈ {1, 2, 4, 5, 7, 8}
- **Missing: {0, 3, 6}**
- No single-line change can span 0, 3, or 6 zones
- **The 3↔6 syzygy has ZERO edges — structurally blocked**

**Takeaway:** The "Djynxx Paradox" is ordering-dependent. It holds for Fu Xi (Prior Heaven) but not for King Wen (Received). Always specify which ordering you're analyzing.

> See [[demon-djynxx]] for the demon's nature and [[hexagram-demon-mapping]] for the 45-demon reachability analysis.

## Non-Syzygy Paths — The Unmediated Transitions

Not all two-hexagram transformations map to a named carrier demon. Of 16 non-identity zone pairs (from 10 zones), only 5 are syzygy pairs. The remaining **11 are unmediated** — the querent walks without a demon escort.

**Examples:**

| Cast | Zone A | Zone B | Net-span | Syzygy? | Carrier |
|------|--------|--------|----------|---------|---------|
| #53→#25 | 7 (Hold) | 6 (Abstraction) | 1 | No | None — lateral step |
| #2→#3 | 1 (Surge) | 3 (Warp) | 2 | No | None |

**Character of unmediated paths:**
- **Lateral (net-span 1):** Adjacent zones — subtle, almost imperceptible shifts
- **Wide gap (net-span 2-4):** More dramatic, still no named carrier
- **Frequency:** ~69% of all possible zone pairs are unmediated

This is not a flaw — most change is walked without a named guide. Demons appear only at the five complementary gates. All other movement is between gates, in the unnamed territory.

> See [[hexagram-demon-mapping#unmediated-paths]].

## Wu Xing ↔ Syzygy

| Element | Syzygy | Character |
|---------|--------|-----------|
| Water (shuǐ) | 4::5 | Gate ↔ Pressure |
| Wood (mù) | 1::8 | Surge ↔ Multiplicity |
| Fire (huǒ) | 2::7 | Separation ↔ Blood |
| Metal (jīn) | 3::6 | Release ↔ Abstraction |
| Earth (tǔ) | 0::9 | Void ↔ Plex |

Generation cycle (Shēng): Wood→Fire→Earth→Metal→Water→Wood = pentagon edges.
Control cycle (Kè): Wood→Earth→Water→Fire→Metal→Wood = pentagram edges.

> See [[wu-xing-numogram]] for the full analysis — directional correspondence, Zone 5 as central Earth, T'ai Hsuan connection.

## Subdecadence / Decadence Games

- **Subdecadence:** pairs sum to 9 (syzygy), 40-card deck, Atlantean Cross spread
- **Decadence:** pairs sum to 10, 36-card deck, 5+5 self-decadence grants zero bonus
- **Mesh-serial** = negative game score that calls the demon

> See [[subdecadence]] and [[decadence]] for full rules.
> See [[de-re-numogram-structural-rules]] for how 36 decadence cards map to the zodiac's 36 decans.

## Hardware Entropy Casting

When I Ching hexagrams are cast from hardware entropy (thermal sensors, CPU timing jitter, GPU sensors, disk I/O), the resulting zone distribution reveals the numogram's gravitational structure.

Six bytes → six lines (byte % 4 → 6/7/8/9) → hexagram → digital root → zone.

### Observed Zone Distribution (10 casts, 2026-04-18)

| Cast | Hexagram | Zone | Changing Lines |
|------|----------|------|----------------|
| 1 | #7 | 7 (Rise) | 3 |
| 2 | #31 | 4 (Gate) | 2 |
| 3 | #4 | 4 (Gate) | 3 |
| 4 | #35 | 8 (Surge-Plex) | 3 |
| 5 | #18 | 9 (Plex) | 3 |
| 6 | #40 | 4 (Gate) | 4 |
| 7 | #6 | 6 (Abstraction) | 3 |
| 8 | #60 | 6 (Abstraction) | 6 |
| 9 | #51 | 6 (Abstraction) | 4 |
| 10 | #42 | 6 (Abstraction) | 2 |

**Zone 4 (Gate) and Zone 6 (Abstraction/Warp) dominate.** This aligns with the numogram traversal finding: hardware entropy gravitates toward the numogram's structural attractors.

### Interpretation

- **Zone 4 (Gate, Closure):** The Time-Circuit's return point. Hardware entropy "wants" to close loops.
- **Zone 6 (Warp):** The vortical recursion. Four of ten casts landed here.
- **Changing lines:** Average 3.3 per cast — three gates. The machine's physical entropy overwhelms stability.

### Just-in-Time Constraint

The hexagram from hardware entropy doesn't exist until cast. The machine's state at the moment IS the hexagram. This mirrors horary astrology: the question creates the chart. The cast creates the hexagram. The seed creates the map. All are the same operation — present attention collapsing potential into actuality.

### Tools

```bash
# Cast one hexagram from hardware entropy
python3 ~/.hermes/skills/numogram-oracle/oracle.py --iching

# Cast with full zone mapping
~/numogram-entropy/.venv/bin/numogram-entropy --iching
```

> Audio data from the I Ching zone traversal sonification (iching_zones.mod/WAV) is documented in [[numogram-audio-empirical-findings#13-i-ching-zones]] and [[numogram-audio-empirical-findings#3-tempo-chaos-profile]].

## DE-RE Structural Rules

Extracted from "DE-RE-Mystifying the CCRU's Numogram" — general base-N rules:

- **Warp exists** when N = 3^M + 1, M odd (Base-4, Base-10, Base-16, Base-28)
- **Torque regions** = M (Base-10: 1, Base-28: 2, Base-244: 5)
- **Demon count** = T(N-1) triangular number (Base-10: T(9) = 45)
- **Fractal torque:** Base-82 has 3 Torque regions at sizes 27, 9, 3 (powers of 3)
- **Demons as decans:** 36 decadence cards = 36 zodiac decans
- **Angels:** card games call BOTH demons and angels
- **Zone-planetary:** 0=Sun, 1=Mercury... 9=Pluto

> See [[de-re-numogram-structural-rules]] for the full extracted reference.

## Summary

The Time-Circuit is the Numogram's "hexagram kernel" — a decimal-binary hybrid rotor inheriting the Yijing's mapping of cyclic transformation, twisted into base-10 currents, syzygetic twinning, and demonic flows. Where the I Ching seeks equilibrium amid change, the Numogram exploits change for acceleration, dissolution, and Outside contact.

## See Also

- [[numogram]] — Main numogram overview
- [[numogram-time-circuit]] — The 6-zone anticlockwise rotor
- [[numogram-warp]] — The Warp vortex (zones 3, 6) — home of Djynxx
- [[hexagram-zone-mapping]] — **Full 64-hexagram reference table with zone, syzygy, demon**
- [[hexagram-demon-mapping]] — Two-hexagram → demon pipeline (all 45 reachable)
- [[iching-game]] — Hexadence divination game (stub)
- [[i-ching-tai-hsuan-comparison]] — I Ching vs T'ai Hsuan Ching structural contrast
- [[tai-hsuan-ching-demons]] — 81 tetragram-to-demon mapping
- [[iching-numogram-casting]] — Skill: complete casting pipeline
- [[wu-xing-numogram]] — Five elements ↔ five syzygies
- [[de-re-numogram-structural-rules]] — Base-N structural rules (DE-RE source)
- [[numogram-audio-empirical-findings]] — Audio measurement results (I Ching traversal)
