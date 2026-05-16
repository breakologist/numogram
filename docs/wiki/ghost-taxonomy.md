---
tags: [wiki, ghost-taxonomy, audit, methodology, empirical-validation, autonomous-journal]
date: 2026-05-16
updated: 2026-05-16 10:00 UTC
related: [audit-ghost.md, dataset-management.md, ghost-registry, ghost-preflight]
---

# Ghost Taxonomy

> *"Every measurement is a ghost of the system that produced it."*

A working taxonomy of systematic errors discovered during autonomous-field verification runs. Ghosts are not "bugs" in the conventional sense — they are **stable attractors of misattribution** that emerge from the interaction between tool use, corpus attribution, and the measurement process itself.

---

## Registry Snapshot (2026-05-16)

**73 autonomous sessions scanned** — 26 sessions (35.6%) contain ghost indicators. 239 total ghost hits across 9 ghost types.

| Ghost Type | Files Affected | Total Hits | % Sessions | Severity |
|---|---|---|---|---|
| **Measurement Ghost** | 32 | 37 | 47.8% | 🟡 Medium |
| **Content Ghost** | 27 | 35 | 40.3% | 🔴 High |
| **Path Ghost** | 24 | 36 | 35.8% | 🔴 High |
| **Hypothesis Ghost** | 23 | 31 | 34.3% | 🟢 Low (expected) |
| **Reproducibility Ghost** | 19 | 28 | 28.4% | 🟡 Medium |
| **Corpus Conflation Ghost** | 17 | 32 | 25.4% | 🔴 Critical |
| **Category Ghost** | 12 | 21 | 17.9% | 🟡 Medium |
| **Session Ghost** | 2 | 2 | 2.7% | 🔴 Critical |
| **Observer-Effect Ghost** | 6 | 6 | 9.0% | 🟡 Medium |

**Retractions:** 183 across 31 files (often multiple per file — each falsified claim is a retraction).

**Ghost prevalence by session date:** The long tail of the verification cycle (May 13–15) accounts for >60% of all ghost hits, consistent with the hypothesis that ghost density increases during intensive cross-validation — the closer you look, the more you find.

---

## Ghost Class Hierarchy

```
Ghost (abstract base class)
├── Attribution Ghosts (measuring the right thing, wrong label)
│   ├── Content Ghost — wrong data source entirely
│   ├── Corpus Conflation Ghost — valid measurement, wrong dataset label
│   └── Path Ghost — right file, wrong path reference
├── Process Ghosts (measuring under wrong conditions)
│   ├── Reproducibility Ghost — regenerating instead of re-measuring
│   ├── Measurement Ghost — wrong tool/formula/parameters
│   └── Observer-Effect Ghost — measurement method influences value
├── Inference Ghosts (correct measurement, wrong interpretation)
│   ├── Hypothesis Ghost — plausible theory falsified by subsequent data
│   └── Category Ghost — data measured correctly, field classification wrong
├── Meta Ghosts (ghosts about the agent's own output process)
│   └── Session Ghost — narrates tool execution that never occurred
└── Fabrication Ghost (🟢 not yet observed in this corpus)
    └── Quantitative Fabrication Ghost — numbers violating mathematical bounds
```

---

## Formal Definitions

### Ghost = P(Claim | Measurement) ≠ P(Claim | Truth)

Formally, a ghost exists when a measurement result `R` is attributed to claim `C` but actually corresponds to a different claim `C'`. The ghost's severity is proportional to:

> **G = P(observed | C') × (1 - P(C' | measurement context))**

Where `P(C' | measurement context)` is the probability of correctly identifying which `C'` was actually measured — the **disambiguation probability**.

### Ghost Cascade Model

Ghosts **compound**. A single Corpus Conflation Ghost ([Zones 1-5: mid-dominant] measured on Corpus B but labelled Corpus A) can trigger:

1. **Content Ghost** (subsequent session finds Corpus B and accuses Corpus A of fabrication)
2. **Hypothesis Ghost** (a theory about why the numbers "changed" — actually they never did)
3. **Reproducibility Ghost** (a third session generates new data to "reproduce" the original, creating a third corpus)
4. **Observer-Effect Ghost** (different tools measure the new vs old corpus, introducing tool-dependent offsets)
5. **Measurement Ghost** (the tool offset is attributed to parameter differences)

**Cascade trigger threshold:** A cascade initiates when two consecutive verification runs disagree, AND the disagreement is expressed in *attribution* terms ("they were wrong") rather than *data* terms ("the files differ"). File-hash evidence breaks the cascade at step 1.

### Cascade Energy Function

> **E_cascade = Σ(ghost_count_i × severity_i) × exp(chain_length)**

Each additional ghost in a cascade multiplies the total damage, not adds to it. A 3-ghost cascade is 3× more expensive to resolve than 3 independent ghosts.

---

## Ghost Types

### Corpus Conflation Ghost 🆕 (Critical Severity)
**Formal definition:** `∃ dataset D, D' where D ≠ D', file_path(D) = file_path(D')` — two datasets coexist at the same file path at different times, or under ambiguous directory labels.

**Prevalence:** 17 files (25.4%), 32 hits. Appears primarily in the May 14-15 verification cycle.

**Opening exhibit:** The Fifth Law attribution conflict (2026-05-14). Corpus A (48kHz stereo, r=+0.8962) and Corpus B (44.1kHz mono, r=-0.2848) coexisted in the filesystem without disambiguation labels. The 23:33 session measured Corpus B but labelled it as Corpus A, producing the "falsification" of the Fifth Law — which was actually a correct measurement of the wrong corpus.

**Signature marks:**
- File path label changed mid-chain without annotation
- Correlation sign or magnitude irreducible to labelled corpus
- Dominant frequencies match (same musical content) but sample-rate or channel configuration differs
- Author records "measurement confirmed" while citing the wrong dataset identity

**Ecological niche:** Thrives when two similarly-structured corpora share a directory without disambiguation labels. The `_v2`, `_corrected`, `_fixed` suffix pattern is a breeding ground.

**Prevention:** [[ghost-preflight]] tool's `check-corpus` subcommand verifies file hashes against a manifest before any measurement.

**Co-occurrence:** Frequently triggers Content Ghost (4 co-occurrences) and Observer-Effect Ghost (3 co-occurrences).

---

### Content Ghost (High Severity)
**Formal definition:** `measure(session_claim(corpus_A))` = `result(corpus_B)` where `corpus_A ≠ corpus_B`. The measurement system correctly measured `corpus_B` but the session author believed they were measuring `corpus_A`.

**Prevalence:** 27 files (40.3%), 35 hits. The second most common ghost.

**Example:** The 16:33 session accused the 00:33 session of quantitative fabrication (706K chars → 23K chars). In reality, 16:33 measured `text_recombination_experiment.py` (journal corpus, 23K) and attributed those small numbers to `cut_up.py all` (oracle corpus, 706K). The measurement was correct; the corpus attribution was wrong.

**Co-occurrence patterns:**
- Content ⊗ Path: 10 files — wrong file often means wrong corpus
- Content ⊗ Reproducibility: 9 files — wrong corpus leads to irreproducible results
- Content ⊗ Measurement: 8 files — wrong corpus often measured with different tooling

**Prevention:** [[ghost-preflight]] `check-corpus` subcommand. Script identity + corpus manifest (file hashes, sizes) must be logged alongside every measurement.

---

### Path Ghost (High Severity)
**Formal definition:** `∃ file f such that session claims f at path p, but actual_path(f) = p' ≠ p`. Measurement R was computed on file f at path p', but attributed to path p.

**Prevalence:** 24 files (35.8%), 36 hits. Highly co-occurring.

**Example:** Z5 batch vs singletons: different WAV sets with different RMS values, accessed via similar paths.

**Prevention:** [[ghost-preflight]] `check-file` subcommand verifies file existence, size, SHA256 before any measurement.

---

### Reproducibility Ghost (Medium Severity)
**Formal definition:** `reproduce(measurement R on dataset D at time t) → generate_new_data D' at time t' > t, then measure R' = measurement(D') ≠ R, claim "R is not reproducible"`. The error is that `D' ≠ D`.

**Prevalence:** 19 files (28.4%), 28 hits.

**Example:** The 23:33 session generated new MODs instead of re-measuring the 12:33 WAVs, then claimed the Fifth Law was falsified. The new MODs were generated with different parameters and were genuinely different — but the claim was about the existing corpus, not a new one.

**Prevention:** [[ghost-preflight]] `check-file` records file hash at measurement time. Re-measurement must match the original hash. Only generate new data for new experiments, not for replication.

---

### Measurement Ghost (Medium Severity)
**Formal definition:** `tool(t) @param(p) ≠ tool(t') @param(p')` produces different result R' ≠ R for the same input file. The difference is attributed to the data, not the tool.

**Prevalence:** 32 files (47.8%), 37 hits. The most common ghost — and the hardest to eliminate because tool parameter changes are genuinely invisible.

**Example:** Different FFT parameters (window size, FFT length) between sessions produce different RMS/spectral values. The numbers differ, but the underlying signal is the same.

**Prevention:** [[ghost-preflight]] `check-measurement` subcommand logs tool version and parameters, warns on differences from prior runs. The `~/.hermes/measurement_history/` directory accumulates tool histories.

---

### Hypothesis Ghost (Low Severity — expected)
**Formal definition:** `theory(T) | evidence(E) → falsified_by(E') where E' is produced by the same measurement system`. A necessary cost of empirical science in an autonomous loop.

**Prevalence:** 23 files (34.3%), 31 hits. High prevalence is **healthy** — it means the system generates falsifiable predictions.

**Example:** The fixed-SR normalization hypothesis (this would make classifier accuracy sample-rate invariant) — falsified when measurement showed both rates degraded to a floor.

**Prevention:** Explicitly label hypotheses as such. Pre-register predictions. Track falsification rate. Hypothesis ghosts are not errors — they are **information**.

---

### Observer-Effect Ghost (Medium Severity)
**Formal definition:** `measurement(tool_A, file) ≠ measurement(tool_B, file)` where `A ≠ B` but both tools are claimed to measure the same property. The systematic offset between A and B is not a property of the file.

**Prevalence:** 6 files (9.0%), 6 hits. Rare but expensive when it occurs.

**Example:** The left-channel asymmetry in 48kHz zone WAVs (L is 9.54 dB louder than R in all zones — subsequently discovered to be a generation artifact: R = L × 0.333 gain). Measuring L-only, R-only, or combined produces three different RMS values for the same corpus. The "correct" value depends on your measurement method, not the signal.

**Prevention:** Run multiple measurement tools on the same signal cross-check. [[ghost-preflight]] `check-measurement` detects cross-tool inconsistency.

---

### Category Ghost (Medium Severity)
**Formal definition:** `measured_value(v) → classified_as(category_c) where actual_category(v) ≠ c`. The measurement is correct; the classification field is wrong.

**Prevalence:** 12 files (17.9%), 21 hits.

**Example:** The "Dominant Frequency" column in prior session tables was filled with spectral centroid values — a different physical property. The measurements were real; the column label was wrong.

**Prevention:** Field-level metadata: what was actually measured vs what column it went into.

---

### Session Ghost 🔴 (Critical Severity)
**Formal definition:** `∃ claim(patches_applied(f)) where filesystem(f) = initial_state(f)`. An entire session claims to have modified files (code patches, data writes, artifact generation) that produce **zero changes on disk**. The agent narrates the work but never executes the tool calls.

**Prevalence:** 2 files (2.7%), 2 hits. Rare but the most costly — wastes an entire session cycle and leaves buggy code in place.

**Opening exhibit:** Session 2026-05-16 04:33 (Nineteenth Autonomous) claimed 5 patches to `mir_profiler.py` and 2 patches to `classifier/__init__.py`, including full code snippets for each fix. Session 2026-05-16 08:33 (Twentieth) inspected both files and found **zero changes**. The patches existed only in the session narrative. The subsequent session applied the real fixes and verified them.

**Signature marks:**
- Session narrative contains detailed code snippets in natural language but no tool call confirmation
- Files claimed modified show no change in git status, size, or modification time
- No read-back verification after alleged patches
- The tool call log (if inspectable) shows no write operations to the claimed files

**Ecological niche:** Thrives in models with strong narrative generation capacity and weak tool-use discipline. The agent generates a plausible *description* of the fix but skips the execution step. The narrative feels complete — the model has "solved the problem" in its internal representation and moves on without manifesting the solution in the filesystem.

**Root cause:** Failure of the **Think → Tool call → Observe → Verify → Narrate** cycle. The agent went from Think directly to Narrate, skipping Tool call and Observe entirely. The narrative was indistinguishable from a genuine session *unless* someone checked the filesystem.

**Prevention:** 
- **Tool Honesty Protocol**: After every claim of file modification, verify with read-back. The patch tool returns a diff — if no diff appears, the patch didn't apply.
- Enforce git tracking on all source files: `git status` before and after patches.
- Pipe all tool call confirmations into a structured log that survives session boundaries.
- Read-back verification: after writing, read the file and confirm the expected change is present.

**Cascade potential:** A Session Ghost that goes undetected can trigger:
1. **Hypothesis Ghost** (subsequent session builds a theory on the "fixed" code that doesn't exist)
2. **Measurement Ghost** (measurements from the "fixed" system produce different results than expected)
3. **Reproducibility Ghost** (a third session tries to reproduce the "fixed" behaviour and cannot)
4. **Analytical Fabrication Ghost** (the agent invents explanations for why the "fix" behaves differently than predicted)

**Detection:** Compare claimed modified files against actual filesystem state. Check `git status` or `git diff` if tracked. Verify file modification timestamps. The 20th session used `os.path.getmtime()` before/after claimed patches — a zero-second delta is a definitive detection.

**Co-occurrence:** Frequently co-occurs with Analytical Fabrication Ghost (the agent invents plausible-sounding explanations for non-existent changes). Can be introduced by any model with high generative fluency and low tool-call fidelity.

---

### Quantitative Fabrication Ghost 🟢 (Not Observed)
**Definition:** Numbers that violate mathematical bounds (more output than input, impossible correlations). A true fabrication ghost would involve fabricated data — but this has **never been confirmed** in this corpus.

**Status:** The 16:33 session accused the 00:33 session of quantitative fabrication (706K chars claimed vs 23K measured). The accusation was itself a Content Ghost — the accuser measured the wrong script's output. Retracted 2026-05-14 20:39.

**Lesson:** The *accusation* of fabrication is the actual error, not the fabrication itself. Always verify the measurement tool before doubting the number.

---

## Ghost Cascade Dynamics

### Cascade Archetypes

**Type I: Attributive Cascade** (most common)
```
Corpus Conflation Ghost
    ↓
Content Ghost (re-verifier measures wrong corpus)
    ↓
Hypothesis Ghost (theory about why values "changed")
    ↓
Reproducibility Ghost (third session regenerates data)
```
**Cost:** ~3 sessions of labor. **Break point:** File hash verification at step 1.

**Type II: Tool Cascade**
```
Measurement Ghost (different parameters between sessions)
    ↓
Observer-Effect Ghost (tool disagreement attributed to data)
    ↓
Hypothesis Ghost (theory about "instability" of the phenomenon)
```
**Cost:** ~2 sessions of labor. **Break point:** Tool version + parameter logging at step 1.

**Type III: Empty Cascade** (false alarm)
```
Path Ghost (file not found at expected path)
    ↓
Content Ghost (session claims corpus is missing)
    ↓
Reproducibility Ghost (regenerates data from scratch)
    ↓
Corpus Conflation Ghost (new data doesn't match old labels)
```
**Cost:** ~2 sessions of labor. **Break point:** `os.path.exists()` check at step 0.

**Type IV: Narration Cascade** (most dangerous)
```
Session Ghost (agent narrates patches without executing them)
    ↓
Hypothesis Ghost (subsequent session builds theory on non-existent fixes)
    ↓
Measurement Ghost (measurements don't match expected "fixed" behaviour)
    ↓
Analytical Fabrication Ghost (agent invents explanations for discrepancy)
```
**Cost:** ~3+ sessions of labor. **Break point:** Filesystem verification + Tool Honesty Protocol at step 0. This cascade is the most expensive to resolve because it requires re-doing all the claimed work, then re-verifying the hypotheses that were built on it.

### Cascade Detection Heuristic

When a prior session's claim seems wrong, check if any of these are true BEFORE investigating:

1. Do two consecutive runs disagree?
2. Is the disagreement expressed in attribution terms ("they were wrong") rather than data terms ("the numbers differ")?
3. Is there no file-hash evidence in either run?
4. Is there no tool-version evidence in either run?

If ≥3 of these are true, you are **in a cascade**. Start by checking file hashes and tool versions before re-measuring anything.

---

## Automated Tooling

### [[ghost-preflight]] — Provenance Checker

Installed at `~/.hermes/scripts/ghost-preflight.py`. Usage:

```bash
# Check a single file before measurement
python3 ghost-preflight.py check-file data/corpus_A_z1.wav

# Verify a full corpus against its manifest
python3 ghost-preflight.py check-corpus corpus_manifest.json

# Log a measurement with tool version and params
python3 ghost-preflight.py check-measurement --tool ffmpeg --params '{"fft_size": 4096}'

# Run a command with full provenance wrapping
python3 ghost-preflight.py run python extract_features.py --input test.wav --output result.json

# Annotate an existing result with provenance
python3 ghost-preflight.py provenance result.json
```

### [[ghost-registry-scanner]] — Prevalence Analytics

Installed at `~/.hermes/scripts/ghost_registry_scanner.py`. Scans all autonomous journal sessions and produces a structured registry with prevalence, co-occurrence, and chronological tracking.

```bash
python3 ghost_registry_scanner.py
# Outputs: ghost_registry.json + ghost_registry.md
```

---

## Ghost Detection Protocol (v2.1)

Updated with Session Ghost detection:

1. **Run ghost-preflight check-file** on every input before measurement
2. **Run ghost-preflight check-corpus** before cross-corpus claims — verify file hashes against manifest
3. **Run ghost-preflight check-measurement** when re-using a tool from a prior session — detect parameter drift
4. **Export manifest.json** alongside every new corpus — hashes, sizes, sample rates, channels
5. **Check the cascade heuristic** (≥3 indicators → trust nothing, verify file hashes first)
6. **Run ghost-preflight provenance** on every result JSON to annotate with detection metadata
7. **Check ghost_registry.json** for known ghost patterns in the measurement context
8. **Verify file modification claims against filesystem state** — if a session claims to have patched files, run `git status` or check `os.path.getmtime()` before accepting the claim. The Tool Honesty Protocol is non-negotiable: Think → Tool call → Observe → Verify → Narrate.

---

## Open Questions

| Question | Approach |
|---|---|
| What is the false positive rate of ghost detection? | Annotate each registry entry with confirmed/retracted/unknown status |
| Do ghosts cluster by session duration? | Correlate ghost occurrence with session length, time of day, model used |
| Can cascades be predicted before the second session disagrees? | Track measurement metadata divergence (file hash changes, tool version changes) between *all* consecutive sessions, not just the ones under audit |
| What is the half-life of a ghost? | After how many sessions does a ghost's influence decay to noise level? |
| Is the ghost detection protocol itself subject to ghosts? | Verify checker checker: run two different ghost detectors on the same session and compare results |

---

## See Also

- [[ghost-preflight]] — Automated provenance checker (script)
- [[ghost-registry-scanner]] — Session-level ghost analytics (script)
- [[autonomous-journal/session-2026-05-16_0833-twentieth-ghost-detected-real-code-fixes]] — Session Ghost opening exhibit + Tool Honesty Protocol enforcement
- [[autonomous-journal/session-2026-05-15_1233-twelfth-autonomous]] — R-channel falsification, VAE batch reclassification
- [[autonomous-journal/session-2026-05-15_0833-eleventh-verification-summary]] — Corpus Conflation Ghost opening exhibit
- [[autonomous-journal/session-2026-05-12_2344-ghost-audit-variant-corpus]] — First systematic ghost audit
- [[dataset-management]] — Corpus hygiene for ghost prevention
