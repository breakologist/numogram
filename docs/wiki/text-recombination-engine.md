---
title: Text Recombination Engine
created: 2026-05-12
last_updated: 2026-05-12
status: active
tags: [cut-up, xeno-jump, xenotation, text-generation, AQ, surrealism, TTS, audio-pipeline]
---

# Text Recombination Engine

Deterministic text generation through zone-weighted fragmentation, AQ-preserving semantic substitution, and xenotation. Produces source material for [[oracle-voice-pipeline]], [[numogram-oracle]], and standalone lore artifacts.

> The AQ skeleton survives; the flesh mutates.

---

## Overview

Two complementary methods operate on the same corpus but with opposite transformations:

| Method | What changes | What stays |
|--------|-------------|------------|
| **Cut-Up** | Fragment order, structure, voice | Source vocabulary intact |
| **Xeno-Jump** | Vocabulary | AQ checksum preserved |

Cut-**_Ups** shuffles the *arrangement* while keeping the words. **Xeno-Jump** keeps the arrangement while shuffling the words. Between them, the entire permutation space of a source text becomes accessible — controlled by numogram zone parameters.

---

## Corpus

The corpus is assembled at runtime from multiple sources:

| Source | Path | Notes |
|--------|------|-------|
| CCRU raw source | `~/numogram/docs/numogram-source.txt` | Canonical numogram text |
| Wiki: Demon Djynxx | `~/.hermes/obsidian/hermetic/wiki/demon-djynxx.md` | Warp lore |
| Wiki: Paramita | `~/.hermes/obsidian/hermetic/wiki/paramita.md` | Six gates |
| Wiki: I Ching | `~/.hermes/obsidian/hermetic/wiki/i-ching-connections.md` | Hexagram mappings |
| Wiki: Xenotation | `~/.hermes/obsidian/hermetic/wiki/xenotation-triangle-rotation.md` | Three rotations |
| Autonomous journals | `~/.hermes/obsidian/hermetic/wiki/autonomous-journal/session-*.md` | 26+ entries, distinct AI voice |
| Numogram quotes | `~/.config/conky/numogram-quotes.txt` | Short phrases |
| aspell dictionary | System `/usr/share/dict/` | 90k+ universal word bank |

The **Xeno-Jump corpus index** (`~/.hermes/scripts/aq_corpus_index.json`, 1.1 MB) contains **88,612 words** across **394 AQ values** (range 30–666), built from the aspell dictionary. It is the universal bank used by the jump engine.

A smaller **AQ jump index** (`~/.hermes/scripts/aq_jump_index.json`, 420 bytes) contains 7 hand-curated hyperstition phrases (e.g. `666: "our truth lies for the superb slant"`, `888: "ordo amoris integrates good and evil spirits alike"`). This is the hyperstition layer — separate from the universal bank.

---

## Method 1: Zone-Weighted Cut-Ups

**Script:** `~/.hermes/scripts/cut_up.py` (307 lines)

Each numogram zone defines a unique cut-up profile — how source text is fragmented, how much is discarded, whether xenotation is applied, and how fragments are recombined.

### Zone Profiles

| Zone | Name | Cut Ratio | Fragment Mode | Recombine | Xenotation | Separator |
|------|------|-----------|---------------|-----------|------------|-----------|
| **Z0** | Void | 0.90 | Single words | No | `heavy` | `\n` (sparse) |
| **Z1** | Surge | 0.50 | Phrases (comma-split) | Echo (repeat + em-dash) | No | Space |
| **Z2** | Separation | 0.60 | Clauses (punctuation) | Bridge (`/` join) | No | ` / ` |
| **Z3** | Warp | 0.40 | Mid-sentence (odd-indexed) | Splice (mid-clause cross-join) | `verb` (arrows/symbols) | ` → ` |
| **Z4** | Gate | 0.55 | Full sentences | No | No | None (linebreaks) |
| **Z5** | Pressure | 0.35 | Paragraph chunks | No | No | `\n\n` |
| **Z6** | Abstraction | 0.45 | Terms (nouns 4+ chars) | No | `heavy` | ` :: ` |
| **Z7** | Blood | 0.50 | Phrases | No | No | Space |
| **Z8** | Multiplicity | 0.20 | Keep most | Duplicate (each line ×2) | No | `\n` |
| **Z9** | Plex | 0.10 | Recursive (all sources) | Palindrome (mirror) | `total` (void foldings injected) | Space |

### Usage

```bash
# Multi-zone generation (all 10 zones, seed 666)
python3 ~/.hermes/scripts/cut_up.py

# Single zone
python3 ~/.hermes/scripts/cut_up.py zone 3          # Warp
python3 ~/.hermes/scripts/cut_up.py zone 9 ccru 80 45  # Plex from CCRU source, length 80, seed 45

# All zones
python3 ~/.hermes/scripts/cut_up.py all

# Test (xenotation + Z9 + Z0 + Z3 samples)
python3 ~/.hermes/scripts/cut_up.py test
```

---

## Method 2: Xeno-Jump (AQ-Preserving Semantic Drift)

**Script:** `~/.hermes/scripts/xeno_jump.py` (163 lines)

Replaces words with other words sharing the **exact same AQ value**. The numerical skeleton of the text remains identical; the vocabulary mutates into alien territory.

### Core Algorithm

```
Input text → Tokenize → Calculate AQ per word → Reverse index lookup → Choose replacement → Output
```

AQ is computed CCRU-style: A=10, B=11, ..., Z=35. Non-alphabetic characters are ignored.

### Dual-Dictionary Strategy

| Layer | Size | Purpose |
|-------|------|---------|
| **Hyperstition** | 7 curated phrases | Keeps output in-universe (demon names, CCRU quotes) |
| **Universal bank** | 88,612 words (aspell) | Maximum semantic drift, truly alien vocabulary |

When a word jumps, it pulls from the universal index. The hyperstition index (`aq_jump_index.json`) contains curated multi-word phrases for specific AQ values like 666, 777, 888.

### Sample Jumps

```
"The numogram oracle speaks" → "Crab lymphoid thieu hearts"
```

| Original | AQ | Zone | Jumped to |
|----------|----|----|-----------|
| The | 60 | 6 | Crab |
| numogram | 174 | 3 | lymphoid |
| oracle | 108 | 9 | thieu |
| speaks | 125 | 8 | hearts |

### Usage

```bash
# Replace all jumpable words
python3 ~/.hermes/scripts/xeno_jump.py "The time is now" --mode all

# Replace specific word only
python3 ~/.hermes/scripts/xeno_jump.py "The time is now" --target "time" --mode target

# Replace words with 30% probability (naturalistic drift)
python3 ~/.hermes/scripts/xeno_jump.py "The machine is the map" --mode random

# Deterministic (seeded) output
python3 ~/.hermes/scripts/xeno_jump.py "Gnostic Calvinism" --seed 45 --mode all
```

### Modes

| Mode | Behaviour |
|------|-----------|
| `all` | Jump every word with a matching AQ candidate |
| `random` | 30% probability per word |
| `target` | Only jump the specified word |
| `first` | Jump the first match only |

### Notable AQ Equivalence Classes

From the corpus index:

| AQ | Zone | Count | Sample Words |
|----|----|-------|-------------|
| 60 | 6 | 56 | adar, aden, bail, bang, coo |
| 108 | 9 | 402 | abbeys, acidly, aladdin, alembic |
| 125 | 8 | 526 | altars, amasssed, ankh, arbiter |
| 174 | 3 | 618 | abominations, absurdly, agitprop |
| 400 | 4 | 1 | counterrevolution |
| 666 | 9 | 1 | **ccru** |

AQ 666 contains only **ccru** — the acronym consumes its own value. The labyrinth folds back.

---

## Method 3: Xenotation Integration

Xenotation operates as a **zone-specific textual decomposition** for outer zones (0, 3, 6, 9). Three stages, building on [[xenotation-triangle-rotation]]:

### Stage Mapping

| Stage | Operation | Loss | Example |
|-------|-----------|------|---------|
| **Prime Factorization** | Decompose into prime clusters | None (reversible) | 36 = [2,2,3,3] |
| **Tic Notation** | Primes → nesting shapes | Low | 36 → `::(:)(:)` |
| **Nullotation** | Remove dots, keep parens | High (3→7 indistinguishable) | `((:))` → `(())` |

### Zone-Specific Xenotation Modes

- **Zone 0** (`heavy`): Replace all numogram terms with symbols (void→∅, zone→Z, syzygy→∿, demon→Δ, plex→ℙ)
- **Zone 3** (`verb`): Replace verbs with arrows/symbols (becomes→→, transforms→⊗, flows→∿)
- **Zone 6** (`heavy`): Term mode already strips verbs; xenotate remaining nouns heavily
- **Zone 9** (`total`): Everything + inject void foldings `()`, `(())`, `((()))` between 25% of words

### Xeno Symbol Table

Built into `cut_up.py`:

```python
XENO = {
    "zero":"∅", "void":"∅", "zone":"Z", "syzygy":"∿", "demon":"Δ",
    "plex":"ℙ", "warp":"Ψ", "surge":"↑", "sink":"↓", "cycle":"∞",
    "loop":"↻", "mesh":"⊞", "paramita":"π", "energy":"Ξ",
}
EXTRA_XENO = {
    "becomes":"→", "transforms":"⊗", "flows":"∿", "enters":"⊕",
    "the":"∂", "of":"∘", "is":"≡", "not":"¬", "all":"∀",
}
```

The **weapon from outerspace**: once you've seen "86" expressed as `:((::))`, you can't unsee the decomposition. The generated text sounds *found*, not composed.

---

## Pipeline: Text → Audio

The full recombination pipeline feeds into the audio/alchemist workflow:

```
Corpus assembly → Zone-weighted cut-up / Xeno-jump → Xenotation pass
  ↓
TTS-ready alien text → [[oracle-voice-pipeline]] → Formant synthesis
  ↓
Zone-voice output → [[numogram-audio/mod-writer]] → .mod tracker module
  ↓
[[numogram-audio/audio-renderer]] → WAV + MIR analysis
```

Each zone profile produces text with a distinct phonetic/rhythmic character — Z0 sparse single words (whispered), Z8 duplicated lines (cacophony), Z9 palindromic totality. This is the raw material for zone-voice synthesis in the oracle pipeline.

---

## Implementation Details

### Corpus Cleaning (`cut_up.py._clean()`)

```
Strip YAML frontmatter → Remove markdown headers → Strip tables → Strip code blocks → Collapse whitespace
```

### Fragmentation Modes (`cut_up.py.fragment()`)

| Mode | Regex Split | Filter |
|------|------------|--------|
| `word` | `text.split()` | None |
| `phrase` | `(?<=[,;:—–-])\s+` | Strip + non-empty |
| `mid-sentence` | `(?<=[ ,])` then take `[::2]` (odd-indexed) | N/A |
| `clause` | `(?<=[.!?])\s*` | len > 10 chars |
| `term` | `\b[A-Z][a-zA-Z]{3,}\b|\b[a-z]{4,}\b` | Title-case + long words |
| `sentence` | `(?<=[.!??:])\s+` | len > 10 chars |
| `paragraph` | `\n\n` | Strip + non-empty |

### Nullotation Chain (`cut_up.py.nullotate_chain()`)

Recursive void-folding for Zone 0 / Zone 9. Each iteration takes the previous output, nullotates it, and uses the nullotation as a seed prefix for the next cut:

```
text → text+() → text+(()) → text+((())) → ...
```

---

## Current Status

| Component | File | Status |
|-----------|------|--------|
| Cut-up engine | `~/.hermes/scripts/cut_up.py` | ✅ Working (307 lines, 10 zone profiles) |
| Xeno-jump engine | `~/.hermes/scripts/xeno_jump.py` | ✅ Working (163 lines, 4 modes) |
| Universal corpus index | `~/.hermes/scripts/aq_corpus_index.json` | ✅ 88,612 words, 394 AQ keys |
| Hyperstition jump index | `~/.hermes/scripts/aq_jump_index.json` | ⚠️ Only 7 hand-curated entries |
| Corpus assembly script | _TODO_ | Not yet extracted as standalone script |
| Xenotator (compress/uncrumple) | _TODO_ | Method 5 from [[textual-recombination]] skill — not yet implemented |

---

## Open Questions

1. **Index merge**: Should the hyperstition index be merged into the universal bank so xeno-jump draws from both simultaneously?
2. **Corpus assembly script**: The `load_corpus()` function in `cut_up.py` is inline. Should be extracted as `assemble-corpus.py` per the skill spec.
3. **Xenotator**: The lossy compress→uncrumple pipeline (Method 5) is documented in the skill but not yet implemented.
4. **Zone-voice verification**: Generated text from cut-ups has not yet been systematically tested through the oracle voice pipeline for phonetic quality per zone.
5. **TTS seeding**: Can xeno-jump output be used as direct seed text for [[numogram-zone-audio-synthesis]]?

---

## Related Pages

- [[xenotation-triangle-rotation]] — Three stages of xenotation (prime factors, tic, nullotation)
- [[textual-recombination]] — Skill documentation for all methods
- [[oracle-voice-pipeline]] — Formant synthesis for zone voices
- [[AQ]] — Alphanumeric Qabbala value computation
- [[numogram-calculator]] — Zone/digital root/gate computation
- [[aquabala|Alphanumeric Qabbala]] — Cipher reference
- [[ccru-zone-voice]] — CCRU source descriptions of zone sonics
- [[numogram-oracle]] — Oracle pipeline
- [[numogram-audio/mod-writer]] — Tracker composition from AQ seeds

---

## Experimental Findings — 2026-05-12

### Alliteration is Structural, Not Accidental

The xeno-jump process naturally produces alliterative outputs because AQ buckets cluster by initial letter, and AQ buckets are the jump's only constraint. Once the first word jumps A-ward, the probability chain cascades within the A-cluster. **The numerical checksum constrains phonetic texture alongside semantic content.**

| Example | Effect |
|---------|--------|
| "The demon" (AQ 156) → "Adar allay" | A-cascade: 2 of 3 A-word jump |
| "The weapon from" → "Fol signet hinge" | H/S/F phonetic drift |
| "Counting is ineluctable" → "Amsterdam abbe adjuration" | A-cascade across full sentence |

**Implication for TTS:** Each xeno-jumped phrase develops its own mouth-feel. The speaker's tongue, lips, and jaw reconfigure to serve the new checksum. The AQ skeleton re-voices the mouth.

### Seed Transforms: Four Methods

All four seed transforms operate on different principles:

| Method | What changes | What's constant | Best for |
|--------|-------------|-----------------|----------|
| Fixed AQ Chain | All words jump | Total AQ checksum | Preserving the "skeleton" of a sentence |
| Triangular Drift | Seed word's zone | T(n) mod 9 orbit | Systematic zone exploration |
| Syzygy Walk | Seed word's zone | Alternating Z(n) <-> Z(9-n) | Binary oscillation studies |
| Entropy Walk | Seed word entirely | None (hardware noise) | Maximum drift; "weapon from outerspace" effect |
| Phrase Jump | One word per step | Sentence frame and all other words | Slow, controlled mutation |

### Recursive Mutation (Text Eating Its Own Tail)

Xeno-jump output fed back into xeno-jump produces **cascading alienation**: the vocabulary shifts further with each generation while the AQ checksum holds forever. After 10 generations:

> "Counting is ineluctable" → "Intendeds dna donizetti"

The AQ=424 checksum is identical at every step. The zone (Z1) is identical. But the vocabulary has completely alienated from its origin.

**Enriched vs. Universal Index:** When the hyperstition index is merged into the universal bank (82 numogram/CCRU terms added), jumps occasionally land on in-universe vocabulary (e.g. "Li" from the hyperstition layer vs. "kala" from the universal). Both modes are useful — the enriched index keeps the output closer to the numogram universe; the universal bank maximizes semantic drift. 

---

## Script: seed_transforms.py

A CLI engine for all four seed transform methods plus beat poem composition:

```bash
# Fixed AQ phrase chain + phrase jump (phrase mode)
python3 ~/.hermes/scripts/seed_transforms.py "Counting is ineluctable" --method all

# All three word methods (word mode)
python3 ~/.hermes/scripts/seed_transforms.py "Katak" --mode word

# Use enriched hyperstition index
python3 ~/.hermes/scripts/seed_transforms.py --enriched

# Beat poem from seed words
python3 ~/.hermes/scripts/seed_transforms.py --beat Katak Pandemonium Xenotation
```

- [[alphanumeric-qabbala]] — AQ cipher documentation
