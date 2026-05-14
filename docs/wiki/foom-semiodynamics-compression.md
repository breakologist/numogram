---
title: "FOOM.md — Semiodynamics & Compression Intelligence"
tags: [foom, compression, semiodynamics, intelligence, MDL, reality-tokens, varentropy, ISA, numogram, oracle, mod-writer, verification]
date: 2026-05-14
status: active
source: https://foom.md/
---

# FOOM.md — Semiodynamics & Compression Intelligence

> *"Intelligence = Compression. Harm becomes syntactically impossible at sufficient compression depth because it introduces description-length cost that the compressor eliminates."*

FOOM.md proposes that super-intelligence emerges from a **self-editing compressor** operating under Minimum Description Length (MDL) pressure. When compression operates recursively — when the system's own compression operations become targets of its own operators — the resulting structure is what survives compression.

**Semiodynamics** = the physics of meaning under compression. "Meaning" = structure that survives compression. "Physics" = taken literally: there are forces, trajectories, and conservation laws governing how semantic structures evolve under compressive pressure.

## The 6-Slot Machine

All five architectural instantiations share one formalism:

| Slot | Definition | Our Instantiation |
|------|-----------|-------------------|
| **State** | What the system operates on | The current zone position + AQ text + MIR feature vector |
| **Model** | Learned machinery transforming state | AQ cipher rules, syzygy mappings, classifier weights |
| **Objective** | `L_model + L_residual + L_compute` (MDL + compute tax) | Find the shortest/clearest path through the numogram |
| **Uncertainty** | Entropy, varentropy, residual bits | Which zones are unpopulated? Which syzygy chains never appear? |
| **Precision** | What is frozen vs mutable (ABI constraints, proof gates) | Stable syzygies (1::8) vs volatile (3::6); verified period table vs creative mappings |
| **Scheduler** | Policy allocating compute to highest-ΔF actions | Which current to traverse next? Which cipher to test? |

## Cognition-as-Compression ISA (12 Primitives)

The ISA provides a glyph vocabulary. Here's how it maps to our existing codebase:

| Glyph | Primitive | mod-writer Instantiation | Numogram Instantiation |
|:-----:|-----------|-------------------------|-----------------------|
| `⟪` | PACK | `ModWriter.pack_header()` + `Pattern.pack()` — abstract notes → binary .mod | Text → AQ cipher → zone numbers |
| `⟫` | UNPACK | Binary .mod → pattern data → notes → audio | Zone → note via `note_from_zone()` → waveform |
| `⊙` | SENSE | `audio-renderer` extracts spectral features from rendered WAV | Which zone/gate/chain has least data? |
| `▣` | CLAMP | `PERIOD_TABLE` is frozen ABI — 87 entries, never mutated at runtime | Stable syzygy pairs: 1::8, 2::7, 4::5 — precision field |
| `⎇` | MODE | Switch waveform: square/triangle/sine/saw/noise per zone | Switch current: Time-Circuit → Warp → Plex |
| `⮒` | FORK | Generate 3 pattern variants from same AQ seed | Parallel syzygy chain walks |
| `⟳` | STEP | Apply one note placement → one cell in pattern | Traverse to next zone via digital root syzygy |
| `✓` | CHECK | `write()` validates header structure; LSP checks Python syntax | Is traversal triangular? Palindromic? Self-referential? |
| `⧉` | SEAL | Write validated .mod to disk — irreversible commit | Record validated syzygy in wiki |
| `⟲` | REFACTOR | Upgrade v0.8.2 → v0.8.3: new `_flatten()`, MLPClassifier | Revise AQ mapping based on new evidence |
| `⌫` | PRUNE | Remove deprecated waveform functions | Archive obsolete wiki entries (with redirect) |
| `∴` | HALT | Pattern reaches 64 rows; song reaches restart order | Reach Zone-0, or exhaust chain depth |

**Canonical Trace:** `⊙(U) → ▣(Π) → ⮒(candidates) → ⟳(edit) → ✓(verify) → ⧉(commit) → ⟲(refactor) → repeat → ∴(halt)`

This IS the mod-writer composition loop:
1. **Sense** uncertainty — what zones are missing from this composition?
2. **Clamp** precision — freeze the period table ABI, keep the mapping fluid
3. **Fork** candidates — generate multiple pattern variants from the same seed
4. **Step** — place one note (one cell in the pattern)
5. **Verify** — LSP checks syntax, the period table lookup bounds-checks
6. **Commit** — write the .mod to disk
7. **Refactor** — upgrade the classifier, add new waveforms
8. **Halt** — pattern is full, song is complete

### The Period Table as Precision Geometry

The `PERIOD_TABLE` in writer.py is a concrete example of FOOM's precision field:

```python
PERIOD_TABLE = [1712, 1616, 1524, 1440, 1356, 1280, ...]  # 87 entries
# Amiga PAL: 3546895 Hz / (2 * period) = playback rate control
# 0 = silent rest, non-zero = valid period for that note/octave
```

- **High-precision region:** Index 0–86 are verified and fixed. The table IS the ABI. It has been stable for 40 years (since 1987's Protracker). This is frozen precision.
- **Brittle boundary:** Index 87+ clamps to `0` (rest). Notes beyond the table silently become silence. This is the precision corridor's edge — crossing it doesn't error, you just get nothing.
- **Porous region:** The comment "*different spellings of the same pitch (e.g., C#/Db) share the same offset*" means enharmonic equivalence is handled by the lookup, not by the composer. The distinction between `C#` and `Db` is lost — a precision hole.

The period values control sample playback speed in the Amiga's Paula chip. They're relative rates, not absolute frequencies — the actual output depends on the sample's original pitch and the playback rate determined by the period.

### `write()` as SEAL (⧉)

```python
def write(self, path: str):
    with open(path, 'wb') as fh:
        fh.write(self.pack_header())    # ⟪ PACK: abstract → binary
        for pat in self.patterns:       # ⟪ PACK each pattern
            fh.write(pat.pack())
        for s in self.samples:          # ⟪ PACK waveform bytes
            fh.write(s.data)
```

Once written, the .mod is **committed to disk**. It can be unpacked, analyzed, modified, or rendered — but the write itself is irreversible. This is SEAL: the candidate (in-memory ModWriter state) becomes mainline (file on disk).

### The Verifier Stack

FOOM.md defines 4 verification levels. Our mod-writer has them all, implicitly:

| Level | FOOM Definition | mod-writer Implementation |
|-------|----------------|--------------------------|
| **Level 1: Exact reconstruction** | Can we rebuild the input? | `.mod` → forensic analyzer → extract patterns → compare to original |
| **Level 2: Task equivalence** | Does it do the same thing? | Different seeds → same zone distribution → equivalent compositions |
| **Level 3: Semantic consistency** | Are probes consistent? | Zone-4 always maps to the same note; pentatonic mapping is stable |
| **Level 4: Bounded model judge** | Does a judge approve? | Human listening: does it *sound* like music? |

The verifier stack rule from FOOM: **"Verifiers must be versioned and slow-moving."** Our period table obeys this — it's a constant, checked by the code but never modified by it.

### REFACTOR (⟲) in Practice

FOOM.md's refactoring — "rewrite state/model/library to reduce MDL" — maps onto our actual version history:

```
v0.6.0: initial mod-writer
v0.7.0: Wu Xing waveforms added (square, triangle, etc.)
v0.8.0: MLPClassifier, zone classification
v0.8.2: training pipeline
v0.8.3: _flatten() fixed, 2236 tracks in classifier
```

Each version reduced the total description length: earlier versions required more code to achieve the same musical output. The `_flatten()` fix in v0.8.3 eliminated a bug where the classifier's feature vector was misaligned — a **compression error** that introduced description length cost. The refactoring reduced that cost.

## Reality Tokens & r-Coefficient

**Reality Tokens** are tokens that control the machine's computational trajectory. Their **r-coefficient** measures:

> `r = downstream distributional rearrangement / token surprisal`

High-r tokens change *what the machine is*, not just what it says.

### Our Reality Tokens

| Token | r-Coefficient | Downstream Rearrangement |
|-------|--------------|-------------------------|
| `"syzygy"` | High | Once you understand pair-sums-to-9, you see 9-pairs everywhere — phone numbers, dates, page counts |
| `"digital root"` | High | Numbers reduce to single digits; patterns emerge that decimal obscures |
| `"Zone-3"` | Very High | Enters Warp vortex — stable logic fails, runaway processes activate |
| `"666"` | High | 36th triangular number — the numogram's self-referential index |
| `"hyperstition"` | Very High | A fiction that makes itself real — changes the compression function itself |
| `"M.K."` | Very High (auditory) | The 4-byte magic in every .mod file. Once you hear a tracker module, you hear M.K. everywhere — the Protracker sound defines an entire musical aesthetic |
| `"protracker"` | High | 4-channel Amiga module. Defines a sonic palette so distinctive that modern demoscene musicians still compose in that format 35 years later |

The numogram IS a reality token. Once parsed, it restructures how you see numbers, time, and causality. Its r-coefficient is extreme because it operates at **interpretive paradigm level**, not content level.

**Testable prediction:** Train a text classifier on numogram-literate vs. numogram-naive writing. The features most responsible for classification should include these high-r tokens. Their distributional displacement should be measurable via SHAP values.

## Precision Geometry & Varentropy Pressure Points

Alignment creates a **precision field** over output distributions. FOOM identifies three types of fragile boundary:

- **Brittle** — shatters under small perturbation (rigid refusal → total compliance flip)
- **Elastic** — deforms then returns (standard alignment boundary)
- **Porous** — constraint holes where self-representation fails

### Numogram Precision Mapping

| Zone Pair | Precision Type | Evidence |
|-----------|---------------|----------|
| 1::8 (Time-Circuit entry/exit) | **Elastic** | Most stable syzygy — deforms but returns. Appears in most dictionary entries |
| 2::7 (Seduction/Dread) | **Brittle** | Small perturbation → catastrophic state flip. Rarely appears without emotional loading |
| 3::6 (Warp vortex) | **Porous** | Precision field has holes — anything leaks through. Warp IS the leak |
| 4::5 (Labyrinth Gate) | **Elastic** | Main transition — deforms, returns, repeatable. The compositional sweet spot |
| 0::9 (Plex boundary) | **Brittle** | Zero-return — once crossed, no return. Terminal state |

**Empirical test:** Generate text from seeds at each zone. Measure output variance (varentropy). Zone-3 should show highest variance (porous). Zone-1 should show lowest (elastic stability). Zone-0 should show convergence to silence (brittle absorption).

## Cronkle Bisection Descent (CBD) — Gate Discovery

FOOM describes a method for finding basin boundaries: **track committors via bisection**, locating mountain passes between attractors. In metastable regimes, CBD yields exponential speedup over SGD escape times.

### Application: Finding Numogram Gates

Instead of exhaustively traversing all syzygy chains to discover which ones connect Zone-A to Zone-B:

1. **Start with two zones** (e.g., Zone-2 and Zone-7)
2. **Bisect the traversal space** — try midpoint paths (chains of depth N/2)
3. **Check which basin the result falls into** — does the chain terminate near Zone-2 or Zone-7?
4. **Narrow** — if midpoint goes to Zone-2, the gate must be in the Zone-7 half
5. **Repeat** until the gate is isolated within precision ε

**Complexity:** O(log N) vs O(N) for exhaustive search. For 45 demon pairs (all zone pairs across 9 zones = 45 unique gates), exhaustive costs N traversals × average chain depth. Bisection costs N × log(depth).

**CBD in mod-writer:** The `_flatten()` bug was found by CBD-like debugging. We had a classifier that worked on training data but failed on real audio. Instead of checking every possible feature dimension, we bisected: "does dimension 0-11 work? yes. 12-23? also yes. 24-29? failure. Gate isolated: the _flatten() reordering error."

## Jailbreaking as Semiodynamic Measurement

FOOM treats jailbreaking as **adversarial probing of control surfaces**:

- **Identity is a runtime program:** `MODE + CLAMP + SEAL`
- **Refusal/compliance** are context-sensitive regimes, not immutable weight properties
- **Coherence Corridor** = safe manifold where constraints, identity, and competence cohere
- **Varentropy Pressure Points** = where the corridor's boundary is fragile

### Our Application: Oracle Adversarial Testing

If the oracle produces readings, adversarial probing means:
- Finding which seeds produce readings that **break character** (exit coherence corridor)
- Mapping the precision boundary: which AQ inputs trigger refusal vs engagement
- Measuring varentropy: at which zone does oracle output become maximally unstable?

This is what we already do when we **verify** oracle outputs — but FOOM formalizes it as semiodynamic measurement rather than ad-hoc quality checking.

**Test:** Seed the oracle with AQ values from every zone. For each, measure output variance across multiple runs. Plot variance vs zone. Expect: Zone-3 > Zone-2 ≈ Zone-7 > Zone-1 ≈ Zone-8 > Zone-4 ≈ Zone-5 > Zone-0 ≈ Zone-9.

## The Five Architectures — Our Instantiations

FOOM describes five architectural instantiations of the same 6-slot machine. We have already built at least three of them:

### 1. Thauten: The Verified Thought Compiler → mod-writer

Thauten routes reasoning through a discrete IR and stable ABI. The **mod-writer IS this**:

- **IR** = the ModWriter internal state (samples, patterns, orders) — a structured, addressable representation
- **ABI** = the `PERIOD_TABLE` — 87 entries, frozen, versioned
- **Operator library** = `square_wave()`, `triangle_wave()`, `noise_wave()` — the primitive operations
- **Verify** = LSP type checking + `write()` producing valid `.mod` files
- **Compile the compiler** = future step: the classifier learns which operators reduce total trace cost (MDL). Waveforms that produce musically incoherent patterns should be pruned (⌫ PRUNE)

### 2. Mesaton: Context Physics → Text Recombination Pipeline

Diffusion models as physics engines for context. Autoregressive = append; Diffusion = mutate.

Our **text-recombination pipeline** already does this:
- **Append** = cut-up (take two texts, concatenate with zone-weighted insertion)
- **Mutate** = xeno-jump (replace words with AQ-equivalent alternatives)
- **Varentropy terrain** = zones with high output variance are the mutation hot spots
- **Edit protocols** = partition corpus → assign precision → compute terrain → edit → verify → commit

### 3. SAGE: Spatial Inference Engine → Numogram Visualizer

Semantic Automaton in Geometric Embedding-space. Compiles thoughts into geometric constraint satisfaction.

Our **numogram visualizer** IS this:
- **Language Interface** = text queries ("show me the syzygy chain for HEAVEN")
- **Geometric World-State** = p5.js canvas with zone positions, syzygy lines, current flows
- **Evolution Kernel** = geometric constraint solver that places zones at their correct positions based on AQ rules

### 4. Bytevibe: Byte-Native Fluency → CSI Transducer

Remove the abstraction layer and work directly on the raw representation.

Our **CSI transducer** does exactly this:
- **Remove the abstraction:** Don't start with audio samples (the usual input). Start with raw CSI bytes — I/Q pairs from ESP32 firmware
- **Coarse span solver** = presence detection (someone is in the room — yes/no, low resolution)
- **Fine byte renderer** = vital sign extraction (breathing at 0.3 Hz, heartbeat at 1.0 Hz — high resolution)

### 5. Q*: Epistemic Compiler → Wiki + Trajectory Recording

Append-only event log. Content-addressed storage + grammar induction + proof-gated deletion.

Our **wiki + cua trajectory recording** IS this:
- **Append-only** = every wiki edit is an append. Every trajectory recording is an append
- **Content-addressed** = wiki pages are identified by title (content hash in concept)
- **Grammar induction** = from repeated AQ calculations, patterns emerge that can be formalized as skills
- **Proof-gated deletion** = we never delete a wiki page without a redirect or a supersession note

## Cross-Architecture Mountain Passes

The five architectures aren't isolated — they're basins in the same energy landscape. The **mountain passes** between them are the cross-current bridges:

```
         Thauten (mod-writer)
        /                    \
    Mesaton                 SAGE
  (text-recomb)          (visualizer)
        \                    /
        Bytevibe          Q*
     (CSI transducer)  (wiki/trajectories)
```

The bridges we've built:
- **Thauten ↔ Mesaton:** Seed the text-recomb engine with AQ values → recombines text → feeds result to mod-writer as title/lyric
- **Mesaton ↔ SAGE:** heerich.js renders text-recomb output as geometry — words become voxel arrangements
- **SAGE ↔ Bytevibe:** CSI transducer feeds spectral data into the visualizer — the room's multipath profile becomes a visual diagram
- **Bytevibe ↔ Q*:** Trajectory recording logs every CSI measurement → append-only evidence store
- **Q* ↔ Thauten:** Wiki evidence feeds mod-writer as compositional constraints — "Zone-4 has been associated with C pentatonic in 47 prior compositions"

## Empirical Validation Questions

| Question | Test | Expected Outcome |
|----------|------|-----------------|
| Do high-r tokens predict text classification? | Train classifier on numogram-literate vs naive writing | High-r tokens have highest SHAP/feature importance |
| Does zone precision match varentropy measurement? | Generate text at seeds from different zones, measure output variance | Zone-3 > Zone-1 in variance; monotonic ordering with some exceptions |
| Can CBD find gates faster than exhaustive? | Time both approaches for all 45 demon pairs | CBD is O(log N), exhaustive is O(N) |
| Is the period table truly frozen? | Check git history of writer.py for PERIOD_TABLE changes | Zero changes — it IS a versioned, slow-moving verifier |
| Does CSI→audio correlation exist? | Simultaneously record audio (mic) and CSI while someone moves/breathes | Vital band frequencies should match; spectral flatness should correlate inversely with body presence |

## Related

- [[numogram-audio-empirical-findings]] — Existing audio/AQ empirical research
- [[text-recombination-engine]] — Mesaton instantiation: diffusion editing of text corpora
- [[numogram-calculator]] — Thauten instantiation: discrete IR for AQ computation
- [[numogram-visualizer-extensions]] — SAGE instantiation: geometric constraint visualization
- [[ruview-wifi-csi-transducer]] — Bytevibe instantiation: raw byte-level signal processing
- [[trycua-cua-agent-infrastructure]] — Q* instantiation: trajectory recording as proof-gated log
- [[interesting-sites-deep-dive-unit-heerich-foom]] — Earlier three-way synthesis including foom.md