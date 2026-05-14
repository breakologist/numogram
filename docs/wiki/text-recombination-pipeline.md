---
title: Text Recombination Pipeline
created: 2026-05-13
tags: [text-recombination, xeno-jump, cut-up, oracle, xenon, numogram, aq-cipher]
---

# Text Recombination Pipeline

A two-stage pipeline for AQ-preserving textual mutation and zone-profiled recombination.

## Architecture

```
SEED TEXT
    │
    ▼
┌─────────────────────────────────┐
│  STAGE 1: Xeno-Jump              │
│  AQ-preserving word mutation     │
│  through one of three corpora    │
│  (general / oracle / xenon)     │
│  Optional: recursive cascade     │
└──────────────┬──────────────────┘
               │  mutated text
               ▼
┌─────────────────────────────────┐
│  STAGE 2: Zone Cut-Up            │
│  Fragment & reassemble through   │
│  zone-specific profiles          │
│  (Z0-Z9 each have distinct      │
│   cut-ratio, mode, xenotation)   │
└─────────────────────────────────┘
```

## Pipeline Scripts

### `xeno_jump.py` — Stage 1

AQ-preserving word mutation. Takes a seed text and replaces words with alternatives from a chosen corpus that share the same AQ checksum (Sum-of-10-35 per character).

```bash
# Single corpus
python3 xeno_jump.py --corpus oracle "Syzygy chain spiraling"

# All three at once, show zone distribution
python3 xeno_jump.py --all-corpora --zones "Teleoplexy accelerates through the plex"

# Blend weights between corpora
python3 xeno_jump.py --mix oracle:0.7,xenon:0.3 "The numogram opens the gate"

# Recursive cascade (feeds output back in)
python3 xeno_jump.py --corpus oracle --recursive --generations 6  "Crystal resonates in the hollow"

# Zone-filtered jumps (only pull from specific zones)
python3 xeno_jump.py --corpus oracle --zone 4,7 "Void enters the labyrinth"
```

**Strategies:**
- `longest` (default) — jumps longest word first, cascades down
- `shortest` — shortest word first  
- `random` — random order

### `cut_up.py` — Zone Cut-Up Engine

Zone-profiled fragmentation with xenotation. Each zone has a distinct cut-ratio, fragmentation mode, and xenotation style.

| Zone | Name | Cut | Mode | Xen | Recombine |
|------|------|-----|------|-----|-----------|
| 0 | Void | 90% | word | heavy | — |
| 1 | Surge | 50% | phrase | — | echo |
| 2 | Separation | 60% | clause | — | bridge |
| 3 | Warp | 40% | mid-sentence | verb | splice |
| 4 | Gate | 55% | sentence | — | — |
| 5 | Pressure | 35% | paragraph | — | — |
| 6 | Abstraction | 45% | term | heavy | — |
| 7 | Blood | 50% | phrase | — | — |
| 8 | Multiplicity | 20% | keep | — | duplicate |
| 9 | Plex | 10% | recursive | total | palindrome |

```bash
python3 cut_up.py zone 6 oracle 25 666   # Zone 6, oracle corpus, seed 666
python3 cut_up.py zone 0 xenon 30 666    # Zone 0, xenon corpus
python3 cut_up.py zone 3 general 40 666  # Zone 3, general lexicon
python3 cut_up.py all                     # All zones, oracle default
```

### `text_pipeline.py` — Full Combined Pipeline

New script. Feeds xeno-jump output into zone cut-up in one command.

```bash
# Recursive jump → zone cascade (oracle)
python3 text_pipeline.py "The signal enters the void" --zones 0,6,9

# Same seed, all three corpora for comparison
python3 text_pipeline.py "The machine speaks" --corpus all --zones 3,6,9

# Longer seed, 8 gens, all 10 zones
python3 text_pipeline.py "I am the silence that is incomprehensible"  --corpus oracle --zones 0,1,2,3,4,5,6,7,8,9 --generations 8
```

## Corpus Architecture

Three distinct lexical currents, each with different *flavor* but the same AQ skeleton:

| Corpus | Buckets | Words | Zones | Source |
|--------|---------|-------|-------|--------|
| **General** | 394 | 88,610 | Z1-Z9 even | English lexicon baseline |
| **Oracle** | 376 | 21,776 | Z1-Z9 even | Wiki + CCRU texts + Land + Grok rotor/convo + Thunder Perfect Mind + Diamond Sutra + Cryptolith + Xenosystems + Star.Ships + Geosophia + Time Sorcery + Autonomous journals |
| **Xenon** | 698 | 11,295 | Z1-Z9 even | GIST zone texts (18 files) + mod-writer codebase + Kron tensors + numogame + Python DSP/ML comments |

### Corpus Enrichment

The pipeline now supports corpus weighting blends:

```bash
python3 xeno_jump.py --mix oracle:0.7,xenon:0.3 "The demon uttunul whispers from the void"
```

Oracle enrichment from Grok rotor conversation, Land numogram texts, CCRU source archives → **zero new unique words** — the oracle corpus already saturated because those exact texts were the foundation of the wiki pages scanned previously. Corpus is fused.

### Enriched Corpus Sources

| Source | Words Added | Character |
|--------|-------------|-----------|
| Wiki + journals (baseline) | ~10K | Hyperstition, numogram, CCRU |
| Grok rotor/convo/Angband/notes | +0 (already fused) | Oracle conversations |
| Land texts (numogram/time) | +0 (already fused) | Landian vocabulary |
| Thunder, Perfect Mind (Nag Hammadi) | ~2.5K | Gnostic paradox-voice |

The oracle corpus is now at **21,776 entries** across **376 buckets** — enriched with the CCRU source texts, Land essays, Grok rotor conversation, and autonomous journal vocabulary.

## Zone-Profiled Xenotation

Each zone has its own xenotation style — the numogram marks (`∞`, `¹`, `₂₈`, `8`, `∂`) applied based on zone profile:

- **Z0 Void**: `· ∞ text ∞` — dot bullet, infinity marks, heavy
- **Z1 Surge**: echo recombination — text repeats with `—` appended
- **Z2 Separation**: bridge mode — fragments connected with ` / `
- **Z3 Warp**: verb xenotation — `∞ prefix ¹ → suffix` splice
- **Z6 Abstraction**: term extraction with `∞ word ∞ :: ∞ word ∞`
- **Z9 Plex**: total xenotation — every word gets `∞word∞`, palindrome recombination

## Corpus Enrichment Methodology

Corpora are built by scanning source texts, extracting words (freq ≥ 2), computing AQ values, and building inverted indices `{AQ_value: [word1, word2, ...]}`.

### Oracle Corpus Sources

The oracle corpus is enriched from the following source trees:

| Source                   | Location                                                             | Content                               |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------------- |
| CCRU Net (Declab)        | `numogram/docs/numogram-source.txt`                                  | Decembrian Lab archive                |
| CCRU Net (Occultures)    | `numogram/docs/wiki/ccru-net-occultures-full.txt`                    | Occultures archive                    |
| Land: Numogram Explained | `numogram/docs/nick-land-numogram-explained.txt`                     | Extended numogram essay               |
| Land: Time               | `numogram/docs/nick-land-time.txt`                                   | Time theory                           |
| Land: Use the Numogram   | `numogram/docs/nick-land-how-to-use-the-numogram.txt`                | Practical numogram guide              |
| Unleashing the Numogram  | `numogram/docs/Unleashing-the-Numogram.md`                           | Full CCRU source text                 |
| Grok Rotor               | `numogram/docs/Grok rotor.md`                                        | 158KB rotor conversation              |
| Grok Notes               | `numogram/docs/Grok notes on the Numogram.md`                        | 59KB detailed notes                   |
| Grok Convo               | `numogram/docs/Grok convo.md`                                        | 28KB oracle conversation              |
| Grok Angband             | `numogram/docs/Grok Angband conversation.md`                         | 37KB dungeon + numogram               |
| Thunder, Perfect Mind    | `.hermes/obsidian/hermetic/raw/tpm.txt`                              | Nag Hammadi text (250 lines)          |
| Diamond Sutra            | `.hermes/obsidian/hermetic/raw/Diamond-Sutra.md`                     | Vajracchedikā Prajñāpāramitā          |
| Wiki texts               | `.hermes/obsidian/hermetic/wiki/*.md`                                | 50+ wiki pages                        |
| Autonomous journals      | `.hermes/obsidian/hermetic/wiki/autonomous-journals/*.md`            | Session cascade logs                  |
| Demon Dictionary         | `.hermes/obsidian/hermetic/wiki/demon-djynxx.md`                     | Demon name lexicon                    |
| Bentov (epub)            | `.hermes/obsidian/hermetic/raw/Stalking...epub`                      | `Bentov - Stalking The Wild Pendulum` |
| Cryptolith (epub)        | `.hermes/obsidian/hermetic/raw/LAND -- Cryptolith.epub`              | Land's Cryptolith fiction             |
| Xenosystems (epub)       | `.hermes/obsidian/hermetic/raw/XENOSYSTEMS_FRAGMENTS.epub`           | Xenosystems fragments                 |
| Star.Ships (epub)        | `.hermes/obsidian/hermetic/raw/star.ships.epub`                      | Gordon White's Star.Ships             |
| Geosophia (epub)         | `.hermes/obsidian/hermetic/raw/Geosophia 1 & 2 (Stratton-Kent).epub` | Grimoire studies                      |
| Time Sorcery (epub)      | `.hermes/obsidian/hermetic/raw/Time Sorcery Vexsys.epub`             | Time + magic + vexsys                 |
| Brazen Vessel (epub)     | `.hermes/obsidian/hermetic/raw/the brazen vessel.epub`               | Grimoire text                         |

### Xenon Corpus Sources

| Source | Content |
|--------|---------|
| GIST zone texts | 18 source-level files (`~/Documents/05-Research/gist/*`) |
| mod-writer codebase | Tracker module code, classifiers, VAE, renderer |
| numogame codebase | Tree dungeon generation, paramita integration |
| Kron tensor files | `~/Documents/05-Research/Kron/*` |

### Epub Extraction

Epub files are extracted via zipfile (xhtml content). Text cleaning strips HTML entities `<ref>`, `&#xNNNN;` markers, and reference tags, then filters whitespace-only lines. Words must be 3–30 characters and appear ≥ 2 times in the source.

## Examples

### Three-Corpora, Same AQ Skeleton

Seed: *"The machine speaks from the abyss"*

| Corpus | Result | Jumps |
|--------|--------|-------|
| General | The fetus speaks okay the abyss | machine→fetus (Z8), from→okay (Z7) |
| Oracle | Alt machine speaks recap the franco | The→Alt (Z6), from→recap (Z7), abyss→franco (Z3) |
| Xenon | The const speaks from the abyss | machine→const (Z8) |

### Oracle Corpus, Native Vocabulary Held

Seed: *"Teleoplexy accelerates through the decimator"*

```
General:  Pliancy accelerates throughout idly the
Oracle:   Teleoplexy accelerates through the decimator    ← no jumps (native words)
Xenon:    Teleoplexy accelerates through the preprocessor
```

The oracle corpus *holds* the numogram-native vocabulary because these words are their own AQ signatures — no alternatives exist. The general dictionary and xenon code vocabulary shift instead.

### 8-Generation Recursive Cascade

Seed: *"The accelerometer burns through the threshold"*

| Gen | General | Oracle | Xenon |
|-----|---------|--------|-------|
| 0 | The accelerator burns through the threshold | The accelerator burns through the threshold | The accelerator burns through the threshold |
| 1 | accelerat→punctilio | accelerat→objectives | accelerat→regularly |
| 2 | → burns | → burns | → burns |
| 3 | through→crosscut | through→threshold | through→threshold |
| 8 | → The punctilio burns through the crosscut | → The objectives burns through the threshold | → The regularly burns through the threshold |

Each corpus reaches a different **oscillating attractor** — words that share the same AQ value with the original but carry distinctly different semantic charges.

### Thunder, Perfect Mind Enriched Oracle

Seed: *"I am the silence that is incomprehensible and the voice whose sound is manifold"*

```
Gen 0: I am the silence that is incomprehensible and the voice whose sound is manifold
Gen 1: I am the silence that is discriminations and the voice whose sound is manifold
Gen 2: I am the silence that is ventriloquism and the voice whose sound is manifold
Gen 3: I am the silence that is revalorization and the voice whose sound is manifold
Gen 4: I am the silence that is thunderstorms and the voice whose sound is manifold
Gen 5: I am the silence that is underemphasises and the voice whose sound is manifold
Gen 6: I am the silence that is comparativists and the voice whose sound is manifold
Gen 7: I am the silence that is thunderstorms and the voice whose sound is manifold
Gen 8: I am the silence that is sentimentalized and the voice whose sound is manifold
Gen 9: I am the silence that is underemphasises and the voice whose sound is manifold
Gen 10→ I am the silence that is ventriloquism and the voice whose sound is manifold
```

The cascade enters a **3-cycle attractor** at gen 4–10, cycling through `thunderstorms → underemphasises → ventriloquism` — three words that share the same AQ checksum with `incomprehensible` (or nearby in the same bucket). The oracle vocabulary holds the native terms (`silence`, `voice`, `sound`, `manifold` — from Thunder — are all oracle-native and don't jump).

### Thunder, Perfect Mind Enriched Oracle

Seed: *"I am the silence that is incomprehensible and the voice whose sound is manifold"*

```
Gen 0: I am the silence that is incomprehensible and the voice whose sound is manifold
Gen 1: I am the silence that is discriminations and the voice whose sound is manifold
Gen 2: I am the silence that is ventriloquism and the voice whose sound is manifold
Gen 3: I am the silence that is revalorization and the voice whose sound is manifold
Gen 4: I am the silence that is thunderstorms and the voice whose sound is manifold
Gen 5: I am the silence that is underemphasises and the voice whose sound is manifold
Gen 6: I am the silence that is comparativists and the voice whose sound is manifold
Gen 7: I am the silence that is thunderstorms and the voice whose sound is manifold
Gen 8: I am the silence that is sentimentalized and the voice whose sound is manifold
Gen 9: I am the silence that is underemphasises and the voice whose sound is manifold
Gen 10→ I am the silence that is ventriloquism and the voice whose sound is manifold
```

The recursive xeno-jump through the oracle corpus shows a **cycling attractor** — after 4 generations the cascade enters a loop: `thunderstorms → underemphasises → ventriloquism → sentimentalized → comparativists → thunderstorms` — all words sharing the same AQ bucket (207, Z7), each a different face of the same checksum frequency. The oracle-native words hold.

### Full Zone Cascade (Text Pipeline)

Seed after oracle xeno-jump (gen 6):
*What the Watkins jogging as a stock of merit was mature as no-stock of merit and alohanomic it is called a stock of merit*

| Zone | Cut-Up Result |
|------|--------------|
| **Z0 Void** | `· ∞ the ∞` / `· ∞ as ∞` |
| **Z3 Warp** | `∞ Watkins ¹ → ∞ of ¹ → ∞ matureomic ¹` |
| **Z6 Abstraction** | `∞ Watkins ∞ :: ∞ stock ∞ :: ∞ merit ∞ :: ∞ jogging ∞ :: ∞ mature ∞ :: ∞ alohanomic ∞` |
| **Z9 Plex** | `∞the∞ ∞as∞ ∞merit∞ ∞a∞ ∞as∞ ∞of∞ ∞a∞ ∞merit∞ ∞and∞ ∞of∞ ∞stock∞ ...` |

### Diamond Sutra Contribution

The Diamond Sutra body text contributed **226 new words** to the oracle corpus, including: `bodhisattva`, `Tathāgata`, `merit`, `arhat`, `falsehood`, `enlightened`, `dismantling`, `incomprehensible`, `inexpressible`, `kaitya`, `Srāvastī`, `Bhagavat`.

The Thunder, Perfect Mind text contributed **130 new words**, including: `hearers`, `dissolution`, `attainable`, `begot`, `acquittal`, `unlearned`, `substance`.

## Stable Attractor Observation

When native oracle vocabulary is fed back into the oracle corpus via recursive xeno-jump, many words reach a **fixed point** — they are the longest (or only) entry in their AQ bucket, so the longest-word strategy keeps them. Words like `numogram`, `syzygy`, `uttunul`, `teleoplexy`, `Tathāgata`, `Bodhisattva`, `Nirvāṇa` are stable because they *are* the oracle vocabulary.

This is meaningful: the oracle corpus *fused*. The native terminology of the system has no AQ alternatives because it was built from the native texts. The mutations happen on the glue words (articles, prepositions, common verbs) instead.

When the seed contains common English words with AQ alternatives (e.g., "accelerator", "machine", "signal"), the cascade diverges across corpora, showing each current's distinct semantic gravity.

### Notable Oracle Words from Enrichment

| Zone | Words Added | Source |
|------|-------------|--------|
| Z1 | `being`, `believed`, `body`, `future`, `place`, `shame` | Thunder, Diamond Sutra |
| Z2 | `beings`, `favour`, `freed`, `fruit`, `hearers` | Thunder, Diamond Sutra |
| Z3 | `arhat`, `city`, `delivered`, `family`, `heap`, `judgment` | Thunder, Diamond Sutra |
| Z4 | `bodhisattva`, `buddha`, `enlightened`, `falsehood`, `highest` | Diamond Sutra |
| Z5 | `advance`, `bodhisattvas`, `buddhas`, `dismantling`, `incomprehensible` | Diamond Sutra |
| Z6 | `cutter`, `holy`, `kalpas`, `more`, `four` | Diamond Sutra |
| Z7 | `bhikshus`, `collect`, `create`, `dweller`, `engaged`, `form` | Thunder, Diamond Sutra |
| Z8 | `bhagavat`, `eye`, `faith`, `moment`, `anything`, `gives` | Diamond Sutra |
| Z9 | `another`, `heard`, `instruction`, `law`, `meaning` | Thunder, Diamond Sutra |

## Empirical Observation: Oscillating Attractors

When recursive xeno-jump cycles through the oracle corpus at high generations, words enter **fixed-point attractors** — no further mutations occur because the longest word in the AQ bucket has already been reached. At that point, the cascade is stable. However, if the `random` strategy is used, words cycle through all alternatives in their bucket, entering **oscillating attractors**.

This mirrors the recursive negation structure of texts like the Diamond Sutra and Thunder, Perfect Mind: the value remains invariant (the AQ checksum), but the sign flips through alternatives. `incomprehensible → ventriloquism → revalorization → thunderstorms → comparativists` — all in the same bucket, all carrying different semantic gravity.

## File Locations

All pipeline scripts live in `~/.hermes/scripts/`:

```
xeno_jump.py          - AQ-preserving mutation engine (Stage 1)
cut_up.py             - Cut-up engine with zone profiles (Stage 2 standalone)
text_pipeline.py      - Combined pipeline: xeno-jump → cut-up
aq_corpus_index.json  - General lexicon: 88,610 words
aq_corpus_oracle.json - Oracle: 21,776 words (enriched with TPM + Diamond Sutra)
aq_corpus_xenon.json  - Xenon: 11,295 words
```

See also:
- [[text-recombination-engine]] — Original engine documentation
- [[numogram-audio-empirical-findings]] — Audio/sonification findings
- [[honorary-zone-0]] — Zone zero conceptual lexicon
- [[diamond-sutra-and-the-endian-rite]] — Diamond Sutra analysis
- [[tetralogue-diamond-sutra]] — Four-voice Diamond Sutra roundtable
