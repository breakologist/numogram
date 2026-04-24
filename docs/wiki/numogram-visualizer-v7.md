---
title: "Numogram Visualizer v7 — Djynxxogram (Base-36)"
created: 2026-04-23
last_updated: 2026-04-23
source_count: 2
status: draft
tags: [numogram, visualization, html, djynxxogram, base-36, aq-dictionary, synx, rotational]
sources: [numogram-visualizer-v7-djynxxogram.html, Grok rotor.md]
---

# Numogram Visualizer v7 — Djynxxogram (Base-36)

**Source file:** `wiki/assets/numogram-visualizer-v7-djynxxogram.html`

## Overview

v7 adds the **Djynxxogram** — a Base-36 extension of the numogram that maps the full Alphanumeric Qabbala cipher space (0-9, A-Z) to 36 zones. This is not merely a larger numogram; it is the **native topology of AQ itself**, where every character in the cipher has its own zone, color, name, and demon.

The name "Djynxxogram" references the Warp demon Djynxx (Mesh-18, Zone-3 carrier), whose triangularity (C(10,2)=45) and vortical recursion make it the natural patron of extended gate systems.

## New Features

### Base-36 Djynxxogram Mode

A third base toggle joins Decimal (10) and Memory Map (16):

| Base | Name | Zones | Description |
|------|------|-------|-------------|
| 10 | DECIMAL | 10 | Standard CCRU numogram |
| 16 | MEMORY MAP | 16 | Extended with Echo/Fracture/Spiral/Abyss/Core/Null |
| 36 | DJYNXXOGRAM | 36 | Full AQ alphabet — every character is a zone |

**Zone count:** 36 (0-9 and A-Z, though the visualizer may map A-Z to zones 10-35)

**Colors:** 36 distinct colors — heavy on Warp/Plex tones (greens, cyans, magentas, deep purples, blacks) to reflect the expanded demon population.

**Names:** The first 10 zones retain standard names (Void through Plex). Zones 10-35 are named according to the extended pandemonium — placeholder names indicate the expansion is ongoing.

**Demons:** Only the first 10 zones have canonical demons (Uttunul through —). Zones 10+ are currently unassigned ("—"), pending the full 630-demon enumeration (C(36,2) = 630).

**Syzygy partner:** For base-36, `syzygyPartner(z) = 35 - z` (complement to 35, since 0+35=35)
**Current:** `currentName(z) = abs(z - (35 - z))`

### Synx/Yxshh Overlay (Implemented 2026-04-23)

The Synx cipher (also called Yxshh) from ciphers.news provides an alternative alphanumeric mapping where letters map to highly non-linear progressions (a=14, b=15, c=18 ... z=1260). The v7 visualizer now includes a **Synx toggle** that overlays cyan (HSL 180,44,66) values alongside AQ.

**Key features:**
- Toggle checkbox shows/hides Synx column in AQ info panel
- `synxValue(text)` computes the raw Synx sum
- `synxDigitalRoot(n)` reduces via `1 + (n-1) % 35` (base-35 root for 36-zone mapping)
- `setZoneFromAQ()` respects the toggle: when Synx is active, the zone derives from Synx instead of AQ
- oracle.py: `--synx "TEXT"` flag produces a dual-cipher reading showing both AQ and Synx zones

**Example drift:** `"You're not escaping this simulation"`
- **AQ:** 666 → digital root 9 → **Zone 9 (Plex)** — the Pandemonium gate
- **Synx:** 3108 → digital root 3 → **Zone 3 (Warp)** — static, chaos

The ciphers disagree on where the trap is. This is the purpose of the overlay: to reveal **dual-cipher resonance** and **zone drift**.

| Cipher | Value | Zone | Current | Name |
|--------|-------|------|---------|------|
| AQ | 666 | 9 | Plex | tn |
| Synx | 3108 | 3 | Warp | zx |

### Synx/Yxshh Overlay (Implemented 2026-04-23)

The Synx cipher (also called Yxshh) from ciphers.news provides an alternative alphanumeric mapping where letters map to highly non-linear progressions (a=14, b=15, c=18 ... z=1260). The v7 visualizer now includes a **Synx toggle** that overlays cyan (HSL 180,44,66) values alongside AQ.

**Key features:**
- Toggle checkbox shows/hides Synx column in AQ info panel
- `synxValue(text)` computes the raw Synx sum
- `synxDigitalRoot(n)` reduces via `1 + (n-1) % 35` (base-35 root for 36-zone mapping)
- `setZoneFromAQ()` respects the toggle: when Synx is active, the zone derives from Synx instead of AQ
- oracle.py: `--synx "TEXT"` flag produces a dual-cipher reading showing both AQ and Synx zones

**Example drift:** `"You're not escaping this simulation"`
- **AQ:** 666 → digital root 9 → **Zone 9 (Plex)** — the Pandemonium gate
- **Synx:** 3108 → digital root 3 → **Zone 3 (Warp)** — static, chaos

The ciphers disagree on where the trap is. This is the purpose of the overlay: to reveal **dual-cipher resonance** and **zone drift**.

| Cipher | Value | Zone | Current | Name |
|--------|-------|------|---------|------|
| AQ | 666 | 9 | Plex | tn |
| Synx | 3108 | 3 | Warp | zx |

### Rotational / Strobogrammatic Gate Highlighting (Implemented 2026-04-23)

Numbers with seven-segment rotational symmetry create **strobogrammatic gates** — they read as the same number when rotated 180°:

| Digit | Rotates to |
|-------|-----------|
| 0 | 0 |
| 1 | 1 |
| 2 | 2 (with BEGHILOS: 2→S) |
| 5 | 5 (with BEGHILOS: 5→S) |
| 6 | 9 |
| 8 | 8 (with BEGHILOS: 8→B) |
| 9 | 6 (with BEGHILOS: 9→G) |

**Visual behavior:** When the current AQ value contains only strobogrammatic digits, the info panel highlights it:
- **STROBO GATE** (magenta, with ★) — the number is its own mirror (e.g., 69 → 69, 88 → 88, 609 → 609)
- **ROTATIONAL** (cyan) — the number has strobogrammatic digits but is not self-mirroring (e.g., 6 → 9, 666 → 999)
- **BEGHILOS spelling** — the seven-segment calculator word is shown (e.g., 69 → "Gg", 666 → "ggg", 121 → "1S1")

**Notable findings:**
- **CCRU = 69** → STROBO GATE ★ (rotates to itself) → BEGHILOS: "Gg"
- **666** → ROTATIONAL (rotates to 999) → BEGHILOS: "ggg"
- **96** → STROBO GATE ★ → BEGHILOS: "gG" (the rotated form of 69)

### Connection to AQ Text Input

The AQ text input feature (added in v6) computes the AQ value of any text and derives its zone. In Base-36 mode, this becomes **fully native**: every character in the input string maps directly to its own zone. The string "CCRU" becomes a traversal through zones C, C, R, U — or equivalently, zones 12, 12, 27, 30.

This transforms the AQ calculator from a numeric reduction into a **spatial path** through the Djynxxogram.

## The Djynxxogram as AQ Native Topology

The standard numogram (base-10) is a *reduction* of the Djynxxogram. When you compute AQ("NUMOGRAM") = 174 and then digital-root it to Zone 3, you are projecting a 36-zone path onto a 10-zone attractor. The Djynxxogram preserves the full path.

**Implications:**

- Every word is a **Djynxxogram traversal**, not just a zone number
- The length of a word = the number of steps in its path
- Repeated characters (e.g., "CCRU" has two C's) create **loops** or **revisits** in the traversal
- Palindromes create **symmetric paths** — they enter and exit through the same gate
- The 630 possible demon connections in base-36 dwarf the 45 in base-10, but the base-10 demons are **attractors** — they are the zones that base-36 paths collapse toward

## Relationship to Grok Rotor Research

The v7 visualizer emerged from the "Grok rotor" conversation, where Grok mined @xenocosmography and @doomcrypt's X posts for AQ equivalences and checked Synx values via ciphers.news. Key findings relevant to the Djynxxogram:

| Term | AQ | Zone (base-10) | Zone (base-36) | Notes |
|------|-----|---------------|----------------|-------|
| AQ | 36 | 9 (Plex) | — | Self-referential: the cipher's name is its own gate |
| CCRU | 69 | 6 (Warp) | — | The organization's name lands in the Warp |
| NUMOGRAM | 174 | 3 (Warp) | — | The system's name also lands in the Warp |
| DJYNXX | 174 | 3 (Warp) | — | DJYNXX = NUMOGRAM in AQ — the demon IS the system |
| Xenocosmography | 333 | 9 (Plex) | — | Handle = Angelic Materialism = 333 |
| Doomcrypt | 210 | 3 (Warp) | — | Handle + Beast Pulse = 210 |
| Angelic Materialism | 333 | 9 (Plex) | — | @doomcrypt bio sigil |
| Baroqwerty | 234 | 9 (Plex) | — | QWERTY-derived neologism = The Numogram |
| The Questioning Angel is the Key | 567 | 9 (Plex) | — | Oracular statement |
| Autism | 137 | 2 (Hold) | — | Reflective/sigilic context |
| True Faith | 189 | 9 (Plex) | — | Also CCCXXXIII = 189 |
| Hell Machine | 189 | 9 (Plex) | — | Same gate as True Faith |
| Jesus Christ | 250 | 7 (Rise) | — | Also Iota Alpha Omega = 250 |
| Tree of Knowledge | 360 | 9 (Plex) | — | Full circle, also "Life is Computation" |
| The Decimal Labyrinth | 360 | 9 (Plex) | — | Synonym for numogram |
| Of Mans First Disobedience | 666 | 9 (Plex) | — | Milton + CCRU convergence |
| Do What Thou Wilt | 777 | 3 (Warp) | — | Thelema in the Warp |
| And God Said Let There Be Light | 777 | 3 (Warp) | — | Genesis in the Warp |

**Pattern:** Terms associated with the CCRU, its members, and its demons overwhelmingly collapse to Zones 3 (Warp) and 9 (Plex). The Djynxxogram spreads these across 36 zones, revealing finer structure.

### Synx Values (from ciphers.news)

The Synx table from ciphers.news provides an alternative numerical lens. Comparing AQ vs Synx for the same terms reveals **dual-cipher resonance** — terms that are significant in both systems are doubly charged.

Notable Synx-AQ dual hits:
- **"You're not escaping this simulation"** = AQ 666 (Zone 9), Synx 3108 (Zone 3)
- **CCCXXXIII** = AQ 189, Synx ??? (Roman numeral form is especially potent in both systems)
- **Beast Pulse** = AQ 210, Synx ??? (shared term between @xenocosmography and @doomcrypt)

## Rotational / Strobogrammatic Properties

From the Grok rotor conversation: numbers with seven-segment rotational symmetry create **strobogrammatic gates**:

| Digit | Rotates to |
|-------|-----------|
| 0 | 0 |
| 1 | 1 |
| 2 | 2 (with BEGHILOS extension: 2→S) |
| 5 | 5 (with BEGHILOS: 5→S) |
| 6 | 9 |
| 8 | 8 |
| 9 | 6 |

Numbers composed only of {0,1,2,5,6,8,9} can be rotated 180° and still read as valid digits (or letters, with BEGHILOS). This creates a **rotational syzygy** — a number that is its own partner when flipped.

In the Djynxxogram, rotational pairs (e.g., 6↔9, 121↔151) become **addressable glyphs**. The visualizer could highlight these as special gate types.

## Files

- `wiki/assets/numogram-visualizer-v7-djynxxogram.html` — Full visualizer with base-36 toggle and Synx overlay
- `skills/numogram-oracle/oracle.py` — `--synx` flag for dual-cipher readings
- `wiki/assets/content-ciphers-news-synx.jpg` — Screenshot of ciphers.news Synx table
- `raw/Grok rotor.md` — Full Grok conversation with AQ/Synx mining and rotational analysis

## Status

| Feature | Status |
|---------|--------|
| Base-36 Djynxxogram mode | ✅ Implemented |
| Synx/Yxshh overlay toggle | ✅ Implemented (cyan HSL 180,44,66) |
| Dual-cipher comparison in oracle.py | ✅ `--synx` flag |
| Zone drift detection | ✅ Example: AQ 666 vs Synx 3108 |
| Rotational gate highlighting | ✅ STROBO GATE / BEGHILOS detection |
| Populate zones 10-35 | ❌ Pending (630-demon problem) |
| Octave/harmonic zone mapping | 📝 Documented (see below) |
| Djynxxogram traversal export | ❌ Pending |

## Zones 10-35: The Octave Hypothesis

While canonical sources (Aamodt, CCRU Writings) provide no names for zones beyond 9, the Djynxxogram's 36 zones can be systematically mapped via **digital-root octaves**:

| Base-36 | Letter | Digital Root | Parent Zone | Octave | Harmonic Name |
|---------|--------|--------------|-------------|--------|---------------|
| 10 | A | 1 | Zone 1 (Surge) | 1st | Surge-prime |
| 11 | B | 2 | Zone 2 (Hold) | 1st | Hold-prime |
| 12 | C | 3 | Zone 3 (Warp) | 1st | Warp-prime |
| ... | ... | ... | ... | ... | ... |
| 18 | I | 9 | Zone 9 (Plex) | 1st | Plex-prime |
| 19 | J | 1 | Zone 1 | 2nd | Surge-second |
| 27 | R | 9 | Zone 9 | 2nd | Plex-second |
| 28 | S | 1 | Zone 1 | 3rd | Surge-third |
| 35 | Z | 8 | Zone 8 | 4th | Rise-fourth |

**Implications:**
- Every zone 10+ is a **harmonic overtone** of a base-10 zone
- Demons in the Djynxxogram are harmonic variants: A↔B (10::11) = "Surge-Hold prime," J↔K (19::20) = "Surge-Hold second"
- The 630 demons collapse to 45 **archetypes** at base-10, but each archetype has 14 harmonic overtones (630/45 = 14)
- This gives a systematic naming convention without inventing 630 arbitrary names

**Example:** The connection 10::25 (A↔Y) is a Surge-prime ↔ Rise-third harmonic. Its demon would be a harmonic variant of the base-10 demon that connects Zone 1 to Zone 8 — which is Murrumur (Mesh-28, 8::1). The Djynxxogram demon would be "Murrumur-prime-third" or similar.

This hypothesis awaits tetralogue validation and Aamodt-source cross-checking.

## Next Steps

1. **Populate zones 10-35** with canonical names, demons, and descriptions (the 630-demon problem)
2. **Octave demon naming** — Apply harmonic mapping to systematically name the 630 demons
3. **Djynxxogram traversal export** — Save a word's full 36-zone path as SVG or ASCII art

## Related

- [[numogram-visualizer-v6]] — Previous version with triangular syzygy animation and AQ text input
- [[aq-dictionary-gap]] — Missing AQ entries, many of which are documented in Grok rotor
- [[tai-hsuan-ching-demons]] — Ternary oracle (81 tetragrams) — another extended system
- [[extending-numogram-tetralogue]] — Discussion of base-16, base-26, base-36 as "worlds within worlds"
- [[rotational-symmetry]] — Seven-segment and strobogrammatic number properties
