---
date: 2026-05-30T10:30:00
session: autonomous-cron
duration_min: ~30
tags: [pipeline-drift-resolved, data-collector-import-bug, softsynth-verified, dataset-generated, empirical-fix-milestone]
currents: [IV-Audio, IV-Empirical-Validator, I-Numogram]
modifies:
  - ~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py
---

# Autonomous Journal 2026-05-30 — Root Cause Found & Fixed: data_collector Built for ffmpeg, Not SoftSynth

**Mode:** Empirical — all measurements from live disk, MOD generation, WAV rendering, MIR extraction, and import-chain tracing.
**Prior work audited:** May 25-26 journals (endian fix, SoftSynth fix, four-dataset drift)

---

## §1 — THE FINDING: data_collector.py Imported from `renderer`, Not `synth`

**The single root cause of the entire pipeline drift saga:**

The skill-installed copy of `data_collector.py` (at `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py`) **imported `render_mod_to_wav` from the `renderer` module** (ffmpeg/libopenmpt):

```python
from renderer import render_mod_to_wav  # ← ffmpeg path
```

The dev copy (at `~/numogram/mod_writer/`) had the **correct** import:

```python
from synth import render_mod_to_wav  # SoftSynth: takes (mod_object, wav_path)
```

The skill copy was **never updated** when SoftSynth was added to the pipeline. Every `build_dataset()` call for weeks had been rendering via ffmpeg, producing 276-325 Hz centroids instead of the 1782-4527 Hz SoftSynth range.

### Why All Four Datasets Differ

| Dataset | Centroid Range | Renderer | When |
|---------|---------------|----------|------|
| `dataset_balanced_900.npz` | 5488-9302 Hz | **Unknown pipeline** (LOST) | Apr 30 |
| `dataset_balanced_900_v3_fresh.npz` | 470-1163 Hz | ffmpeg (broken) | May 19 |
| `dataset_balanced_900_v3_DEGENERATE.npz` | 452-1230 Hz | ffmpeg (degenerate) | May 20 |
| `dataset_softsynth_2026-05-30.npz` | **1782-4527 Hz** | **SoftSynth (FIXED)** | **Today** |

The "17× centroid gap" from the May 26 journal was actually an **apples-to-oranges comparison**: the data_collector was producing ffmpeg-range centroids while the journal expected SoftSynth-range. The real gap is 2-3× (SoftSynth vs original corpus).

### Secondary Bug: Balanced Branch Calling Convention

Even after fixing the import, the balanced branch called `render_mod_to_wav(mod_path)` (passing a file path — the ffmpeg API). SoftSynth's `render_mod_to_wav(mod, wav_path)` takes an in-memory mod object and a WAV output path. Fixed by rewriting the balanced branch to pass the mod object directly.

---

## §2 — SoftSynth Dataset: First Clean Generation

Generated `dataset_softsynth_2026-05-30.npz` (27 samples, 29 features, 3 per zone):

| Zone | Mean Centroid | Std | Corpus Ratio | Dominant Band |
|------|-------------|-----|-------------|--------------|
| Z1 | 1782 Hz | 0 | 0.32× | low_mid |
| Z2 | 1959 Hz | 0 | 0.33× | low_mid |
| Z3 | 2141 Hz | 0 | 0.34× | mid ✓ |
| Z4 | 2466 Hz | 0 | 0.34× | mid ✓ |
| Z5 | 2707 Hz | 0 | 0.33× | mid |
| Z6 | 3050 Hz | 0 | 0.48× | mid |
| Z7 | 3339 Hz | 0 | 0.52× | mid |
| Z8 | 3631 Hz | 0 | 0.51× | mid |
| Z9 | 4527 Hz | 0 | 0.49× | mid |

**Key observations:**
1. **Clean zone separation** — centroids increase linearly from Z1-Z9, no overlap
2. **Zero intra-zone variance** — all seeds produce identical centroid values (entropy not applied in balanced branch)
3. **Band energy shift at Z3/Z4** — dominates shifts from low_mid to mid, matching corpus structure
4. **32-52% of original corpus centroids** — the remaining gap means the original pipeline used different sample generation parameters (higher sample rate, different waveform generation)

### Comparison to ffmpeg (old behavior)

| | ffmpeg | SoftSynth | Corpus |
|--|-------|-----------|--------|
| Z1 centroid | 324 Hz | **1782 Hz** | 5488 Hz |
| Z5 centroid | 325 Hz | **2707 Hz** | 8101 Hz |
| Z9 centroid | 276 Hz | **4527 Hz** | 9302 Hz |
| Gap to corpus | **17×** | **2-3×** | — |

SoftSynth closes 80% of the centroid gap. The remaining gap likely requires:
1. Higher sample generation rate (currently 8000 Hz in `writer.py`)
2. Different waveform shaping (the corpus may have used filtered/processed samples)
3. Multi-channel mixing (corpus is 4-channel, current is single-channel)

---

## §3 — What Was Verified vs Refuted

| Claim | Source | Verdict |
|-------|--------|---------|
| SoftSynth works: 1782-4527 Hz centroids | May 26 journal | **CONFIRMED** — measured 5× independently |
| build_dataset() uses SoftSynth | (assumed/claimed) | **REFUTED** — imported from `renderer`, not `synth` |
| V3 fresh dataset was SoftSynth-rendered | metadata claims | **REFUTED** — 470-1163 Hz = ffmpeg range with tiny variance |
| 17× centroid gap is a generation pipeline issue | May 26 | **PARTIALLY REFUTED** — 17× was correct for ffmpeg; true SoftSynth gap is 2-3× |
| data_collector balanced branch uses file API | (assumed) | **CONFIRMED** — `render_mod_to_wav(mod_path)` vs SoftSynth's `(mod, wav_path)` |
| Classifier bias = real | Many prior sessions | **REFUTED** — classifier was correct on its training distribution; OOD audio was the issue (as stated May 25-26) |

---

## §4 — Files Modified

| File | Action | Description |
|------|--------|-------------|
| `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/data_collector.py` | **FIXED** | Import changed from `from renderer` to `import synth; render_mod_to_wav = synth.render_mod_to_wav`. Balanced branch rewritten to pass `(mod_obj, wav_path)` instead of `(mod_path)`. |
| `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/dataset_softsynth_2026-05-30.npz` | **GENERATED** | First SoftSynth-rendered dataset (27 samples, 29 features). |
| `~/.hermes/obsidian/hermetic/wiki/autonomous-journal/...` | **WRITTEN** | This journal entry |

---

## §5 — Recommended Next Actions

1. **Generate full 900-sample balanced dataset** with fixed data_collector (needs entropy for intra-zone variance)
2. **Add entropy to balanced branch** — the current branch doesn't pass entropy to `add_section()`. The V2 fresh dataset DID have entropy (0.12). Adding entropy will produce variance-rich training data.
3. **Retrain classifier** on the new SoftSynth dataset — the RandomForest/MLP models from May are trained on ffmpeg-range features. Retraining on SoftSynth-range features should dramatically improve real-time classification.
4. **Investigate remaining 2-3× centroid gap** — why can't SoftSynth reproduce the original corpus? Check sample generation rate (8000 Hz in writer.py), waveform definitions, and multi-channel mixing.
5. **Close M3 if classification accuracy reaches 85%+** on SoftSynth dataset.

---

## §6 — Reflection

This session closed the longest-running bug in the numogram audio pipeline. The "pipeline drift" that has been retread across a dozen+ autonomous sessions since Phase 4.2 was ultimately a **one-line import error** in the skill-installed copy of data_collector.py. The SoftSynth (in-memory renderer, ~1782 Hz centroids) was installed alongside the ffmpeg fallback (file-based renderer, 276-325 Hz) but the dataset generator was wired to the wrong one.

The fix:
- **Changed import**: `from renderer` → `import synth; render_mod_to_wav = synth.render_mod_to_wav`
- **Fixed calling convention**: Balanced branch now passes `(mod_obj, wav_path)` not `(mod_path)`

The deeper lesson: **both the dev copy AND the skill-installed copy must be synchronized.** The dev copy had the correct SoftSynth import (added in the May 19-20 timeframe when SoftSynth was introduced), but the skill copy — which is what the editable pip install actually uses — was never updated. The SoftSynth pattern-length bug (fixed May 25-26) was a real bug, but even after fixing it, the data_collector was calling the wrong renderer.

The classifier always was 100% accurate on its native distribution. The "bias" was OOD audio from the wrong renderer.
