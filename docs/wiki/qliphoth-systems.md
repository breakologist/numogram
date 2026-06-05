---
tags:
  - Reference
  - Numogram
  - AQ
  - Toolkit
  - Web
---

# qliphoth.systems

**URL:** https://qliphoth.systems/
**Author:** @Lumpenspace (creator of [lumpenspace/ccru](https://github.com/lumpenspace/ccru) — Interactive SVG Numogram visualization in Next.js/React/TypeScript)

**Description from InterestingSites.md:** "interactive numogram + AQ toolkit, decimal labyrinth, syzygies/gates/demons visualization, scripture corpus"

---

## Overview

qliphoth.systems is a two-part web application:

1. **NUMOGRAM** — Interactive Decimal Labyrinth visualization
2. **GEMATRIA** — Anglossic Qabbala Toolkit (AQ-centric)

Both are built by Lumpenspace, who also maintains the [ccru](https://github.com/lumpenspace/ccru) repository — a more feature-complete Numogram/AQ visualization with three visual layouts (original, labyrinth, ladder), planetary orbital mode, Pandemonium Matrix, gematria Chrome plugin, and live deployment at [num.qliphoth.systems](https://num.qliphoth.systems).

---

## NUMOGRAM — Interactive Decimal Labyrinth

### Visual Layouts

The interface offers multiple views accessible via keyboard shortcuts (A/S/D/F) and the Components page:

| Key | View | Description |
|-----|------|-------------|
| **A** | Default / Labyrinth | Circular/radial numogram with WARP/TORQUE/PLEX regions |
| **S** | (Appears same as A) | |
| **D** | (Appears same as A) | |
| **F** | Ladder | Linear/vertical arrangement — zones stacked with syzygy pairs visible |

### Core Visualization

The main SVG canvas displays:

- **Three Regions** (color-coded):
  - **TORQUE** — Zones 1, 2, 4, 5, 7, 8 (the six torque zones)
  - **WARP** — Zones 3, 6 (the two warp zones)
  - **PLEX** — Zones 0, 9 (void/plex poles)

- **Zone Data** (clickable, with planetary correspondences):
  | Zone | Planet | Xenotation | Current |
  |------|--------|------------|---------|
  | 0 | Sol | (none shown) | plex |
  | 1 | Mercury | n/a | torque |
  | 2 | Venus | : | torque |
  | 3 | Earth | (:) | warp |
  | 4 | Mars | :: | torque |
  | 5 | Jupiter | ((:)) | torque |
  | 6 | Saturn | :(:) | warp |
  | 7 | Uranus | (::) | torque |
  | 8 | Neptune | ::: | torque |
  | 9 | Pluto | (:)(:) | plex |

- **Syzygy Pairs** (5 total):
  - 4::5 — **Katak** (1)
  - 3::6 — **Djynxx** (3)
  - 2::7 — **Oddubb** (5)
  - 1::8 — **Murrumur** (7)
  - 0::9 — (Plex syzygy)

- **Demons** (45 total in Pandemonium Matrix — toggleable layer)

### Interactive Layers (Toggles)

| Layer | Default | Purpose |
|-------|---------|---------|
| Syzygies | ON | Shows syzygy connections between zones |
| Currents | ON | Shows current flows (Warps/Torques) |
| Gates | ON | Shows gate connections |
| Pandemonium | OFF | 45-demon matrix overlay |
| Particles | OFF | Ambient particle effects |
| Colours | ON | Region color coding |

### Label Modes

- **Numbers** — Standard decimal labels (ON by default)
- **Tic Xenotation** — : ::: notation (OFF by default)
- **Planets** — Planetary glyphs/names (OFF by default)

### Controls

- **Undo/Redo** — State history navigation
- **Share Current State** — Generates shareable URL for current view configuration
- **Zone Selector** — Click any zone to focus/highlight it
- **Region Buttons** — Filter to Torque/Warp/Plex/Time Circuit

---

## GEMATRIA — Anglossic Qabbala Toolkit

### Primary Cipher: Alphanumeric Qabbala (AQ)

**Base-36 continuous mapping:**
```
0-9 → 0-9
A-Z → 10-35
```

This is the **exact AQ cipher** used in CCRU/Numogram work — no gaps, no overcoding, single unbroken series.

### Toolkit Components

| Component | Status | Description |
|-----------|--------|-------------|
| **Browser Plugin** | Chrome Extension | Real-time overlay: hover any text → value, digital root, corpus matches. Auto-numerizes tweets on X/Twitter. |
| **KJV Explorer** | Requires Extension | Full King James Bible (66 books) with verse-level AQ values. Search by value, digital root, keyword. Save verses to corpus. |
| **Saved Words Corpus** | Dashboard + Extension Sync | Personal database of numerized phrases/words/verses. Filter by value, cipher, source, digital root. Build resonance chains. |
| **Cipher Editor** | Config UI | Define custom ciphers beyond AQ. Assign letter values, set modular bases. Ships with 10 ciphers (3 enabled by default). |

### Enabled Ciphers (Default)

1. **⟐ ALPHANUMERIC QABBALA** (AQ) — Base-36, primary
2. **☍ SYNX** — CCRU Synx cipher
3. **🆀 QWERTY** — Keyboard-layout cipher

### Available Ciphers (Disabled by Default)

- ⌨ NUMERIC QWERTY
- ⛧ ALPHANUMERIC SATANIC
- ✶ ALPHANUMERIC PRIMES
- ◼ ALPHANUMERIC SQUARES
- △ ALPHANUMERIC TRIGONAL
- 𒀯 ARCHAIC ALPHANUMERIC
- ℚ NUMERIC QWERTY PRIMES

### Interesting Values (Pre-configured)

`93, 137, 156, 111, 222, 333, 444, 555, 666, 777, 888, 999`

Notable: **93** (Thelema), **666** (Beast), **777** (Liber 777), **444/555** (repeating triads).

---

## Integration Points for Our Work

### 1. AQ Cipher Reference
The toolkit uses **exactly our AQ cipher** (base-36, 0-9 + A-Z continuous). This is a live, browser-based reference implementation.

### 2. Numogram Visualization Reference
The NUMOGRAM view is a **working reference implementation** of:
- Zone planetary correspondences
- Xenotation labels (: (:): etc.)
- Syzygy/demon/current topology
- Region classification (Torque/Warp/Plex)

Our `numogram-visualizer` skill and `numogram-combinatorial-svg` could cross-reference this.

### 3. Browser Extension → Our Workflow
The Chrome extension provides:
- Real-time AQ overlay on any webpage
- Twitter/X inline numerization
- Corpus sync between browser and dashboard

**Potential:** Could we build a similar overlay for our local wiki/Obsidian? Or use the extension to numerize research sources on the fly?

### 4. KJV Corpus as Test Data
31,000+ verses pre-numerized in AQ. Ready-made corpus for:
- Testing our `aq-dictionary-syzygy-analysis` pipeline
- Training zone classifiers (`numogram-audio/mod-writer-ml-interpretability`)
- Resonance chain analysis

### 5. Cipher Editor → Custom Cipher Research
The cipher editorUI allows defining arbitrary letter→value mappings. Could prototype:
- Alternative AQ variants
- Zone-specific ciphers (e.g., Zone-1 cipher, Zone-6 cipher)
- Audio-parameter ciphers (pitch→value mappings)

### 6. Saved Words Corpus → Resonance Chain Building
The "resonance chain" concept (collecting phrases sharing a value) maps directly to our **syzygy-chain** and **AQ hit analysis** workflows.

---

## Technical Notes

- **Stack:** Appears to be Next.js/React/TypeScript (consistent with lumpenspace/ccru)
- **Extension:** Chrome Manifest V3, content script + background + popup
- **Data:** KJV dataset embedded; user corpus in localStorage/IndexedDB + extension sync
- **Offline:** Works fully offline once loaded (extension not required for NUMOGRAM view)
- **State Persistence:** Share URL encodes view state (layers, labels, zone focus, view mode)

---

## Related Wiki Pages

- [[numogram-visualizer]] — Our SVG generation pipeline
- [[aq-cipher-reference]] — Canonical AQ values
- [[numogram-syzygy-chain]] — Syzygy traversal logic
- [[aq-dictionary-syzygy-analysis]] — Dictionary analysis pipeline
- [[numogram-audio/mod-writer]] — Tracker modules with AQ/numogram mappings
- [[ccru-gematria-calculator]] — External reference (14 ciphers, 665K+ phrases)

---

## Action Items

- [ ] Test browser extension in local Chrome for research workflow
- [ ] Export KJV verse data for corpus analysis (if extension permits)
- [ ] Cross-reference zone planetary/xenotation data with our `numogram-geometry` primitives
- [ ] Investigate cipher editor for custom zone-cipher prototypes
- [ ] Compare NUMOGRAM ladder view with our `tsubuyaki-oo-gallery` zone behaviors
- [ ] Consider building a similar overlay for Obsidian/wiki via user script

---

*Explored 2026-06-05 via Hermes browser tool. Live site fully functional without extension for NUMOGRAM; GEMATRIA dashboard works but KJV/Saved/Cipher Editor require extension for full features.*