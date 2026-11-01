---
title: I Ching / Hexagram Connections
created: 2026-04-08
last_updated: 2026-11-01
source_count: 1
status: reviewed
tags: ["i-ching", "numogram", "theory"]
---

# I Ching Connections

> **Errata (2026-10-17):** line pairs are 1&4, 2&5, 3&6 (CCRU [declab](http://ccru.net/declab.htm); Wilhelm), weights 1+8, 2+16, 4+32 → 1::8, 2::7, 4::5. Single-line edges under King Wen DR: 1↔8 = 5, 2↔7 = 5 (were 7, 6). Zone pairs: 45, not 16. No hexagram reaches Zone 0 under a DR mapping, so at most 36 demons are reachable, not 45.

The Decimal Numogram (specifically its Time-Circuit) is explicitly linked by the CCRU to the I Ching (Yijing, or Book of Changes). The Time-Circuit is positioned as a hypercultural successor to the Yijing's time-mapping functions, taking up the chrono-numeric roles in a decimal, demonic mode.

> **Verification note (Em, 1 Nov 2026):** the paragraph above says the Time-Circuit is "positioned as a hypercultural successor" to the Yijing. The source is more modest: CCRU's Decimal Numogram page says the I Ching and the Nma numogram "share a hypercultural matrix" and lists immanent and historical evidence for that claim. It says nothing of succession [ccru.net, [declab](http://www.ccru.net/declab.htm)]. Read "successor" and the later "decimal completion" wording as wiki interpretation, not CCRU doctrine.

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
| Lines 1 & 4 | 8::1 | 1::8 | 7 |
| Lines 2 & 5 | 7::2 | 2::7 | 5 |
| Lines 3 & 6 | 5::4 | 4::5 | 1 |

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

> **Verification note (Em, 1 Nov 2026):** the claim that quinary casting produces "the same 64 hexagrams but traversed in reverse order" is **speculation**. CCRU says only that the 6-cycle "is also generated in reverse by quintuplicative numbering" [ccru.net, declab]. That is a statement about digital roots, 5ⁿ → 5, 7, 8, 4, 2, 1. It is not a casting method. The Land quotations on this page come from the 2026 *Dangerous Maybe* transcript (see [[nick-land-time-theory]]); they were not checked against ccru.net.

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

> **Verification note (Em, 1 Nov 2026):** the CCRU source here is one paragraph of declab. It calls the T'ai Hsuan Ching a "binotriadic parallel" of 81 tetragrams that reverses which numerical values are foregrounded and which are implicit. It also suggests that the Tao Te Ching's 81 sections show the same triadic/binary conflict was at work in early Taoism [ccru.net, declab]. The mapping of the ternary basis onto the Warp and Plex, and the "King multiples of 9" grid, are **wiki speculation**, not CCRU's.

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
| 1↔8 (Murrumur) | 5 | ✅ |
| 2↔7 (Oddubb) | 5 | ✅ |
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

Not all two-hexagram transformations map to a named carrier demon. Of 45 non-identity zone pairs (from 10 zones; 36 among zones 1–9), only 5 are syzygy pairs. The remaining **40 are unmediated** — the querent walks without a demon escort.

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

## CCRU Sources on the I Ching and Chinese Material (added Em, 1 Nov 2026)

These are sourced facts. Each is tagged with its source, and CCRU text is paraphrased, with only short quotations marked. Speculation is kept in its own labelled subsection below.

### Decimal Numogram § 2, "Numogram and I Ching" [ccru.net, [declab](http://www.ccru.net/declab.htm)]

- The I Ching and the Numogram are said to "share a hypercultural matrix". Both are described as **zygonomies** (double-numbering systems), and both treat subdivisions of decimal arrays, with the *Ten Wings* commentary cited as a hint of this.
- The digital roots of binary powers settle into a six-step cycle **1, 2, 4, 8, 7, 5**. CCRU matches these steps to the **six lines of the hexagram** and to the **Time-Circuit zones**, and calls the result the **binodecimal 6-Cycle**. The same cycle is generated in reverse by powers of 5.
- Line pairing follows the zygonovic (9-twin) rule **8:1, 7:2, 5:4**, which CCRU maps onto the traditional hexagram line pairs (1st/4th, 2nd/5th, 3rd/6th).
- Zero and the triad: the time-circuit, or hexagram, implicitly links **zero with the excluded triadic values** (3, 6, 9). CCRU cites evidence of an early struggle between triadic and binary numbering in ancient China. It suggests that binary domination of decimal numbering leaves a triadic residue "consistent with nullity". The hexagram puts a triadic factor back in, because its reduced values sum to **27 = 3³** (1+2+4+8+7+5 = 27; checked).
- The **T'ai Hsuan Ching** (81 tetragrams) is treated as a "binotriadic parallel", and the Tao Te Ching's 81 sections are read as a sign of the same numerical conflict.
- § 3 of the same page describes a Nma ritual: the time-circuit as a three-stage **hydro-cycle** (ocean → evaporation → downpour), carried by Mur Mur, Oddubb and Katak, which CCRU compares with the Hindu Trimurti. This is not Chinese material, but it is the ritual form CCRU gives the circuit itself. See [[numogram-time-circuit]].

### Zone 6 page: Horovitz, the 64 and the hexagrams [ccru.net, [Zn6](http://www.ccru.net/zones/Zn6.htm)]

- Zone-6 initiates and envelops the **Sixth Phase of Pandemonium, which has 64 impulse-entities**. Chaim Horovitz "qabbalistically relates" this phase or 'Tone' to the **hexagrams of the I Ching** and to the **yantras of the Ur-Oriyan Yoginis**.
- In the numeral notes on the same page, the six lines of the hexagram stand for the six stages of change found by archaic Taoism. These are numerically equivalent to the reduced binary powers 1, 2, 4, 8, 7, 5.
- Arithmetic check [repo, `zones.ts` `phaseCount: 64` for zone 6]: phase *n* holds 2ⁿ entities. Zone 1 has 2 entities and zone 7 has 128 [ccru.net, Zn1/Zn7], so 2⁶ = 64 = the number of hexagrams. Zone 6 is a **Warp** zone [ccru.net, Zn6; repo `ZONE_REGION`]. The 64 therefore sits *outside* the Time-Circuit whose zones the hexagram lines correspond to. The hexagram count (zone 6) and the hexagram's line-values (Time-Circuit zones) belong to different regions.
- See [[zone-6]] (which already notes the Horovitz link) and [[zone-6-hinge-portrait]].

### "Fei Ch'ien Rinse Out: sino-futurist under-currency" [ccru.net, [archive/rinse.htm](http://www.ccru.net/archive/rinse.htm)]

The CCRU archive lists the text as "a sino-futurist meditation". It was published by Steve Goodman (Kode9) in *Pli* (Warwick Journal of Philosophy) 7 (1998), pp. 155–72 [PhilPapers GOOFCR], and Wikipedia's *Sinofuturism* article credits it with coining the term. *Fei-ch'ien* ("flying money") is the Tang-dynasty remittance certificate, and the text uses it to frame underground banking and Triad numerology. How it relates to the I Ching:

- **Form:** the 27 numbered sections count down in **binary**, from [11011] (= 27) to [1], followed by a final "[0] White out". The closing section notes that the Death of a Thousand Cuts "had taken exactly twenty-seven minutes". So the text's own structure is a binary countdown to zero through 27 = 3³, the same total the declab page gives for the hexagram's reduced line-values. (The structure is observed directly; any intent behind the shared 27 is **not** stated in the text.)
- **§ 6 [10110]:** recounts the Leibniz–Bouvet exchange. Leibniz sent his binary arithmetic to the Jesuit Bouvet in China, and Bouvet answered with the I Ching. Goodman treats Leibniz's reading of it as a universalist, neo-Confucian capture of the yin-yang as a "binary machine". (Historical context: this is the well-known 1701–03 correspondence.)
- **§ 7 [10101]:** "Shaolin takes the I Ching for software", with **3** as the encryption system's immobile motor. The section sets out the build: two kinds of line (rigid/yang, supple/yin), trigrams 2³ = 8, and 64 = 8² permutations. It argues that changing lines are "lines of becoming", so yin-yang cannot be read as a dialectic.
- **Note 11** quotes Deleuze & Guattari (*What Is Philosophy?*) on hexagrams as projected "figures" rather than concepts. Goodman calls this valid against Confucianism but doubtful for a "yin-positive Taoism".
- **§ 21 [111]** quotes Triad lore on 3 and 9 (digital reduction to 9) and the officer codes 489 / 438 / 426 / 415 / 432 / 49, with their digit sums (21, 15).

### Other Chinese material on ccru.net

- *Cyberhype-4: Chinese Whisper Markets* ([archive/cyberhype4.htm](http://www.ccru.net/archive/cyberhype4.htm), *Mute*, 10 Sep 2001): diaspora trading networks, guanxi, development from the periphery; the epigraph is attributed to a Taoist source. It contains no I Ching content [ccru.net, search summary].
- *One or Many Chinas?* ([archive/onechina.htm](http://www.ccru.net/archive/onechina.htm)): a Deleuze–Guattari critique of state 'unity' applied to the One China principle. No I Ching content.
- *Powers of Illusion* ([archive/illusionpower.htm](http://www.ccru.net/archive/illusionpower.htm)): the Forbidden City as introverted imperial staging. No I Ching content.
- None of these mentions gua qi or the T'ai Hsuan beyond what is listed above. The archive search used site search results. These three pages were not read in full.

### Speculation (labelled, Em)

- *Speculation:* Rinse Out's binary countdown 27 → 0 can be read as a performance of declab's claim that binary numbering of decimal leaves a residue "consistent with nullity": the count ends in "[0] White out". Neither text cross-references the other.
- *Speculation:* the zone-6 = 64 relation in this wiki's hexagram tables is the strongest CCRU-sourced link between hexagram *count* and a zone. The DR-of-King-Wen-number mappings ([[hexagram-zone-mapping]]) are wiki constructions, not CCRU.

### Cross-links

- [[hexagram-47-translations]] — Kun / Oppression across translations
- [[reading-2026-10-26]], [[reading-2026-10-28]] — oracle readings using these mappings
- [[zone-6]], [[zone-6-hinge-portrait]] — the 64-phase zone
- [[tai-hsuan-ching]], [[tai-hsuan-ching-demons]], [[i-ching-tai-hsuan-comparison]] — the 81-tetragram parallel
- [[gua-qi-wen]] — gua qi (hexagram–calendar) material
- [[time-circuit]], [[numogram-time-circuit]] — the 6-cycle zones

## See Also

- [[numogram]] — Main numogram overview
- [[numogram-time-circuit]] — The 6-zone anticlockwise rotor
- [[numogram-warp]] — The Warp vortex (zones 3, 6) — home of Djynxx
- [[hexagram-zone-mapping]] — **Full 64-hexagram reference table with zone, syzygy, demon**
- [[hexagram-demon-mapping]] — Two-hexagram → demon pipeline (36 reachable under a DR mapping; see errata)
- [[iching-game]] — Hexadence divination game (stub)
- [[i-ching-tai-hsuan-comparison]] — I Ching vs T'ai Hsuan Ching structural contrast
- [[tai-hsuan-ching-demons]] — 81 tetragram-to-demon mapping
- [[iching-numogram-casting]] — Skill: complete casting pipeline
- [[wu-xing-numogram]] — Five elements ↔ five syzygies
- [[de-re-numogram-structural-rules]] — Base-N structural rules (DE-RE source)
- [[numogram-audio-empirical-findings]] — Audio measurement results (I Ching traversal)
