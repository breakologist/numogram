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

> **Status (Em, 1 Nov 2026):** qliphoth.systems is **down** as of 1 Nov 2026. Claims below are tagged **[archived site]** (Wayback captures: home [19 Apr 2026](https://web.archive.org/web/20260419020904/https://qliphoth.systems/); /numogram nearest 2026 capture [10 Aug 2026](https://web.archive.org/web/20260810145727/https://qliphoth.systems/numogram); /gematria [nearest 2026 capture](https://web.archive.org/web/2026/https://qliphoth.systems/gematria)), **[repo]** (checked against [lumpenspace/ccru @ 7c38ad9](https://github.com/lumpenspace/ccru/blob/7c38ad910410c3f5744b961eb97adf58ff00d41f/), last commit 27 Feb 2026), or **[unverified / model inference]**.

**Description from InterestingSites.md:** "interactive numogram + AQ toolkit, decimal labyrinth, syzygies/gates/demons visualization, scripture corpus"

---

## Overview

qliphoth.systems is a two-part web application:

1. **NUMOGRAM** — Interactive Decimal Labyrinth visualization
2. **GEMATRIA** — Anglossic Qabbala Toolkit (AQ-centric)

Both are built by Lumpenspace, who also maintains the [ccru](https://github.com/lumpenspace/ccru) repository — a more feature-complete Numogram/AQ visualization with visual layouts (README lists three — original, labyrinth, ladder — but `app/data/types.ts` defines four: `original | labyrinth | ladder | planetary` [repo]), planetary orbital mode, Pandemonium Matrix, gematria Chrome plugin, and live deployment at [num.qliphoth.systems](https://num.qliphoth.systems) [repo: README 'Live URLs'; reachability on 1 Nov 2026 not confirmed].

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

> **Verification note (Em, 1 Nov 2026):** the table above (from a June 2026 browser session) is kept as recorded but is **refuted by the repo**. `app/NumogramClient.tsx` maps shortcuts **A → original, S → labyrinth, D → ladder, F → planetary**; `app/data/positions.ts` has distinct coordinate sets `P_ORIGINAL`, `P_LABYRINTH`, `P_LADDER` and a `PLANETARY_*` radial layout [repo]. So S and D are *not* the same as A — the "appears same" reading was likely a rendering/transition glitch or misobservation. The deep-dive's four layouts (original, labyrinth, ladder, planetary) are correct. The archived /numogram page confirms "ASDF to change view" and shows `[layout=labyrinth]` [archived site]; `app/numogram/page.tsx` defaults the `layout` param to `labyrinth` [repo].

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
  - 0::9 — **Uttunul** (9) — Plex syzygy [archived site; repo `app/data/syzygies.ts`: "Plex syzygy — the absolute outer"]

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
| **Cipher Editor** | Config UI | Define custom ciphers beyond AQ. Assign letter values, set modular bases. Ships with 10 ciphers (3 enabled by default) [repo — see note below]. |

### Enabled Ciphers (Default)

> **Verification note (Em, 1 Nov 2026):** **[repo] confirmed.** `app/cyphers/ccruCiphers.ts` defines exactly ten ciphers (the ten listed here), and `gematria/plugin/src/ciphers.ts` sets `enabledCypherIds: ['alphanumeric-qabbala', 'synx', 'qwerty']`. Note the archived /gematria page itself says the editor "Ships with AQ (base-36) by default" [archived site] — the 10/3 figure describes the plugin defaults, not that page's wording.

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

`93, 137, 156, 111, 222, 333, 444, 555, 666, 777, 888, 999` **[repo confirmed]** — `interestingValues` in `gematria/plugin/src/ciphers.ts`, in this order.

Notable *(glosses are ours, not the repo's)*: **93** (Thelema), **666** (Beast), **777** (Liber 777), **444/555** (repeating triads).

---

## Archived wording (short quotes)

- /numogram: hover and selection let you inspect the system "as a navigational map of recursive time and drift between torque, warp, and plex" — and gates "track culminations (triangular sums), then reduce multi-digit values by summation". [https://web.archive.org/web/20260810145727/https://qliphoth.systems/numogram]
- /gematria: "What surfaces are not hidden messages but contingent resonances: … the connections you draw from that constellation are the work." [https://web.archive.org/web/2026/https://qliphoth.systems/gematria]
- /gematria frames AQ as "one answer to that call" — Liber AL's instruction to obtain "the order and value of the English alphabet" (AL II:55 reads "the order & value of the English Alphabet"). [https://web.archive.org/web/2026/https://qliphoth.systems/gematria]

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
31,000+ verses pre-numerized in AQ. **[unverified / model inference]** — the archived page says only "Full KJV dataset with chapter navigation, verse-level AQ values" [archived site]; the figure is the general KJV verse count (~31,100), not a number the site or repo states, and "pre-numerized" is not confirmed. Ready-made corpus for:
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

> **Verification note (Em, 1 Nov 2026):** **localStorage/IndexedDB — partly refuted.** The repo uses `window.localStorage` (only for a plugin-setup UI flag) and `chrome.storage.local` for extension settings and saved entries; **no IndexedDB** usage found [repo]. The archived page says entries "sync between the Chrome extension and this dashboard" [archived site]. **"Works fully offline" — [unverified / model inference]**: no service worker or offline claim in repo or archive. The NUMOGRAM-view claim that the extension isn't needed is plausible (it is a plain Next.js page) but untested.
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
---

## Em's take (1 Nov 2026)

*by Em (in collaboration with the user)*

### Sourced

- **Qliphoth** (sing. *qliphah*) are the "shells" or "husks" of Kabbalah — the averse, unbalanced counterparts of the sefirot, often pictured as the Tree's underside. This is standard in Golden Dawn/Thelemic literature (e.g. Crowley, *777*; Regardie, *The Golden Dawn*); page references not verified here, so cite generally.
- The site borrows the name for a CCRU numogram and AQ toolkit; it does not itself expound qliphothic doctrine [archived site].
- Planets per zone, 0 Sol → 9 Pluto (Mercury = Sol-1 … Pluto = Sol-9) [archived site; repo `app/data/zones.ts`].

### Speculative (labelled)

- The /gematria line about "contingent resonances" whose connections "are the work" sits very close to this project's stance that noise and bias are instructive, not errors to scrub.
- The qliphothic underside of the Tree might map to Warp (3::6) and Plex (0::9) as the numogram's "outside" of the Time-Circuit — a rhyme, not a doctrine.
- The X/Twitter auto-numerizer turns the social-media feed into oracle text — cf. this week's Brisset puns thread in [[reading-2026-10-28]] ([reading-2026-10-28.md](reading-2026-10-28.md)).
- Planets on zones could bridge to our decans/lunar-mansions work: if zones carry planets, decan rulers could be routed through zones.
