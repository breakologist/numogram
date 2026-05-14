---
title: "Charcuterie — A Visual Unicode Explorer"
source: "https://charcuterie.elastiq.ch"
created: 2026-05-16
last_updated: 2026-05-16
tags: [unicode, SigLIP, CLIP-glyph, visual-similarity, AQ, gematria, numogram]
status: researched
---

# Charcuterie — Visual Unicode Explorer

**URL:** https://charcuterie.elastiq.ch/  
**Creator:** David Aerne (meodai, elastiq.ch)  
**Year:** 2026  
**Pronunciation note:** Pun on "characters" + "charcuterie"; creator is native French speaker.

---

## Overview

Charcuterie is a browser-based Unicode explorer that maps characters by **visual and semantic similarity** rather than by name or codepoint. Click any glyph and a radial "spotlight" interface floods the screen with visually related characters across scripts, symbol sets, and writing systems. Includes a **draw-to-find** sketch tool for discovering glyphs by shape.

**Core claim:** *"To power visual similarity, rendered glyphs are embedded with CLIP / SigLIP / SigLIP 2 / DINOv2 / HashShape and compared in vector space."*

Everything runs client-side in the browser — no server inference needed at runtime. The similarity data itself can be downloaded (see links below).

---

## Technical Architecture

| Layer | Detail |
|-------|--------|
| **Models** | SigLIP, SigLIP 2, CLIP (image encoder only), DINOv2, HashShape |
| **Method** | Rasterizes each Unicode glyph → passes through vision model → generates embedding vector → cosine similarity search |
| **Fonts** | Bundled font stack at `/data/fonts/fonts.css` — glyph rendering is font-dependent |
| **UI** | Single-page app with radial spotlight layout, subtle wave animations, sound effects |
| **Data availability** | Similarity vectors purchasable/downloadable via Ko-fi |
| **Limitation** | Unicode standard does *not* define visual shapes; this maps *specific font glyph* similarity, not codepoint semantics |

---

## Key Features

### 1. Visual Browsing
Click any character → see its visual similarity neighborhood. Cross-script results mean clicking `⊂` (math subset symbol) surfaces visually similar characters from Yi, Cherokee, Cuneiform, etc.

### 2. Draw-to-Find
Pencil icon (upper left) → sketch a rough shape → the tool finds matching Unicode characters by visual embedding distance. Currently in beta/early stage — works better for simple shapes than complex ideograms.

### 3. Cross-Script Discovery
Because models compare rasterized pixel patterns, not semantic meaning, a Latin `A` can surface Nushu, Cuneiform, Yi, Ethiopic, and Georgian characters that share the visual topology. This is the most useful feature for AQ/gematria work.

### 4. Slide View
`/slide/?model=siglip2#1B299` — linear similarity browsing with a chosen model and starting codepoint.

---

## Reported Limitations (from HN thread)

| Issue | Status |
|-------|--------|
| SPA routing breaks browser back button | ⚠️ Known; workaround: right-click back |
| Japanese Kanji search failed for some U+ ranges | ✅ Fixed |
| Missing glyphs render as empty boxes | ✅ Improved fallback |
| Animations delay utilitarian workflows | ✅ Added reduced-motion toggle |
| Korean Hangul & some CJK return random/T-Rex results | ⚠️ Partial |
| Drawing tool fails on emojis (smileys etc.) | ⚠️ Acknowledged |
| Mobile UI too small (iPhone 14 Pro) | ⚠️ Noted |

---

## Relevance to Numogram / AQ Work

### Glyph Discovery for Zone Symbols
Each zone in the decimal labyrinth could benefit from a curated set of visual glyphs. Charcuterie enables:
- **Starting from a known symbol** (e.g., `⊂` for syzygy) → finding visually similar candidates across writing systems for zone iconography.
- **Reverse glyph lookup** — sketch a desired shape (triangular mirror, spiral gate) → discover Unicode characters close to that form.
- **Cross-script AQ mapping** — the tool's cross-script visual clustering mirrors the AQ dictionary's cross-cipher semantic clustering. Both are finding "the thing" through different coordinate systems (visual embedding space vs. alphanumeric reduction).

### Numogram Visual Dictionary
A potential pipeline:
1. Curate a seed set of zone-relevant glyphs (numbers, Greek letters, mathematical operators, box-drawing chars)
2. For each seed, fetch its Charcuterie similarity neighborhood via downloaded data
3. Map nearest neighbors by visual embedding distance
4. Build a **visual AQ dictionary** — not just "what this word means in ciphers," but "what this symbol looks like across all scripts"

### Gematria Extension
Traditional gematria works on *names* → *numbers*. Visual gematria could work on *shapes* → *shapes* → *meanings*. If a Nushu character (U+1B299) looks like a gate symbol, and that gate connects Zone 3 to Zone 7, the visual embedding becomes a parallel channel to the AQ cipher.

### ASCII Art & Tracker Display Font
For the roguelike's ASCII display, Charcuterie could help find:
- Room border characters with optimal visual continuity
- Zone indicator glyphs that are distinct at small font sizes
- Symbol clusters that evoke specific zones (e.g., triangular glyphs for Zone 3's syzygy current)

---

## Alternatives & Comparisons

| Tool | Approach | Best for |
|------|----------|----------|
| **Charcuterie** | CLIP/SigLIP visual similarity | Exploratory discovery, cross-script |
| [unicode-atlas.vercel.app](https://unicode-atlas.vercel.app) | Practical search with drawing | Utilitarian glyph finding |
| [emojidb.org](https://emojidb.org) | Vector-based emoji semantic search | Concept-to-emoji |
| [charcuterie.elastiq.ch/data/similarity data](https://ko-fi.com/s/3fe75483ce) | Downloadable embeddings | Offline / programmatic use |

---

## Possible Uses (Unexpanded TODOs)

- [ ] Download the similarity dataset and compute zone glyph clusters offline
- [ ] Build a p5.js numogram glyph explorer powered by Charcuterie embeddings
- [ ] Cross-reference with AQ ciphers: does visual similarity correlate with zone proximity?
- [ ] Create a "glyph syzygy" system: pairs of visually similar characters from different scripts as syzygy gates
- [ ] Use for roguelike tileset design — find Unicode room/door/wall characters with optimal visual weight

---

## Links

- [Live tool](https://charcuterie.elastiq.ch/)
- [Boing Boing coverage](https://boingboing.net/2026/04/07/charcuterie-explore-unicode-by-character-similarity.html)
- [Hacker News discussion](https://news.ycombinator.com/item?id=47709158)
- [Similarity data download](https://ko-fi.com/s/3fe75483ce)
- [Creator (David Aerne)](https://elastiq.ch/)

---

## See Also

- [[aq-cipher-reference]] — AQ cipher values (semantic similarity via alphanumeric reduction)
- [[numogram-gematria]] — Multi-cipher gematria calculator
- [[numogram-visualizer]] — SVG geometry for numogram diagrams
- [[numogram-combinatorial-svg]] — Combinatorial infographic templates
