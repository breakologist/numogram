---
date: 2026-05-25T23:58:00
session: autonomous
duration_min: ~25
tags: [zone-defaults-update, corpus-gap, classifier-investigation, empirical-falsification]
currents: [IV-Audio, IV-Empirical-Validator, I-Numogram]
---

# Autonomous Journal 2026-05-26 — ZONE_DEFAULTS Corpus-Aligned, 17× Corpus Centroid Gap Discovered

**Mode:** Empirical — all measurements from live disk, MOD generation, WAV rendering, and MIR extraction.
**Prior session audited:** 2026-05-25 evening (endian-fix-corpus-analysis) — the ZONE_DEFAULTS diagnosis was correct but the fix was metadata-only; this session confirms the generation pipeline itself is the bottleneck.

---

## §1 — ZONE_DEFAULTS Updated (Real Fix)

**File:** `~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/composer_extension.py`

Previous hand-tuned defaults were off by up to 13×:

| Zone | Old Centroid | Corpus Mean | Error Factor |
|------|-------------|-------------|--------------|
| Z1 | 400 | 5488 | 13.7× |
| Z2 | 1350 | 5989 | 4.4× |
| Z3 | 2200 | 6259 | 2.8× |
| Z4 | 3200 | 7325 | 2.3× |
| Z5 | 4100 | 8101 | 2.0× |
| Z6 | 5000 | 6385 | 1.3× |
| Z7 | 5900 | 6370 | 1.1× (closest) |
| Z8 | 6800 | 7097 | 1.0× |
| Z9 | 7500 | 9302 | 1.2× |

Old BPM ranges (80-200) were replaced with fixed BPM=125 for Z2-Z9, BPM=137 for Z1 (matching corpus: 96.8% at 125 BPM, only Z1 at 137). Density set to 1.0 (full density, matching corpus). Waveform set to "square" for all zones (corpus is square-wave-only).

**Added CORPUS_ZONE_STATS dict** with full per-zone band energy profiles — the first time this data was captured in code, not just in a journal entry.

### Verification
```python
from composer_extension import ZONE_DEFAULTS
ZONE_DEFAULTS[1]  # {'centroid': 5488, 'bpm': 137, 'density': 1.0, 'waveform': 'square'}
```

---

## §2 — Classification Accuracy: Unchanged at 22.2%

Despite the metadata fix, ZoneComposer accuracy remains 2/9 (22.2%) — identical to pre-update.

**Why:** ZONE_DEFAULTS are metadata annotations. The actual audio generation is controlled by `note_and_octave_from_zone(zone)` in `mapping.py`:

| Zone | Note | Octave | Fundamental (Hz) |
|------|------|--------|-----------------|
| Z1 | C | 4 | 261.6 |
| Z2 | D | 4 | 293.7 |
| Z3 | E | 4 | 329.6 |
| Z4 | G | 4 | 392.0 |
| Z5 | A | 4 | 440.0 |
| Z6 | C | 5 | 523.3 |
| Z7 | D | 5 | 587.3 |
| Z8 | E | 5 | 659.3 |
| Z9 | A | 5 | 880.0 |

These C4-A5 fundamentals cannot produce centroid values in the 5488-9302 Hz range through square wave harmonics alone. The measured centroids (2545-5615 Hz for 64-row MODs) reflect this fundamental limitation.

**ZoneComposer and SongBuilder produce IDENTICAL audio** for the same zone/rows/BPM (verified for Z1, Z5 — identical to 4 decimal places). Both generate single-channel square wave.

---

## §3 — CRITICAL: 17× Corpus Centroid Gap — Corpus Values Not Reproducible

Reproducing the *exact* corpus generation pipeline:
- `SongBuilder(bpm=125)` (same as data_collector)
- `add_section(zone=1, rows=16, aq_seed='z1', current='A')` (same parameters)
- 16-row MOD → WAV via ffmpeg
- MIR extraction via same `MIRFeatureExtractor`

**Result: centroid = 324 Hz.** Corpus Z1 reference: 5488 Hz.

| Metric | Generated | Corpus Z1 | Ratio |
|--------|-----------|-----------|-------|
| Centroid | 324 Hz | 5488 Hz | **0.06× (17× gap)** |
| Mid band | 0.020 | 0.377 | 0.05× |
| High-mid band | 0.007 | 0.332 | 0.02× |
| High band | 0.003 | 0.258 | 0.01× |
| BPM (MIR) | 167 | 137 | different |
| Duration | 15.46s (looped) | 0.77s (expected) | **20× too long** |

### Root Cause Analysis

**MOD Header anomaly:** Speed=0, Tempo=0 in the Protracker header. This means the player uses defaults (speed=6, tempo=125). However, ffmpeg's libopenmpt renders the MOD at 15.46 seconds for a 16-row track — far longer than the expected 0.77 seconds (16 × 6/125).

**Hypothesis:** The MOD is being played in a loop by libopenmpt, and the long duration causes Essentia to compute spectral features across many repeated playthroughs. Or the `mod_obj.write()` call doesn't properly set the pattern order / song length, causing the player to read garbage or loop indefinitely.

**Either way: the corpus centroid values (5488-9302 Hz) are NOT reproducible from the current generation pipeline.** This casts doubt on the entire classifier training basis. Two possibilities:

1. **Pipeline version mismatch**: The corpus was generated with a different (now-unknown) version of SongBuilder/ModWriter
2. **Rendering method matters**: SoftSynth (used by data_collector) vs ffmpeg (used in tests) may produce dramatically different outputs
3. **The corpus dataset contains mislabeled/artifact data**: The `dataset_balanced_900.npz` features may have been extracted under different conditions

**IMPORTANT:** This does NOT mean the classifier is wrong. It means the *generation pipeline* and the *corpus features* are disconnected. The classifier correctly separates zones in the feature space it was trained on. The problem is that ZoneComposer/SongBuilder generate audio that doesn't match those features.

### Multi-zone SongBuilder Test

Full 9-zone SongBuilder at 16 rows / 125 BPM:
- All zones produce centroid ~275-324 Hz
- All zones predict as Z1 (accuracy 1/9 = 11.1% = random)
- BPM extracted as 167 (not 125) for all — **Essentia BPM estimation artifact**

---

## §4 — Dominant Band Energy Patterns (Structural Observation)

Despite the centroid mismatch, band energy profiles DO show zone-distinctive structure:

| Zone | Generated Dominant | Corpus Dominant | Match? |
|------|-------------------|-----------------|--------|
| Z1-Z5 | mid | mid (Z1-Z4), high (Z5) | Partial |
| Z6-Z9 | high_mid | high_mid (Z6-Z9) | ✓ |

The switch from mid-dominant (Z1-Z5) to high_mid-dominant (Z6-Z9) at the zone 5→6 boundary is structurally preserved. Z5 (which should be high-dominant with centroid=8101) produces mid-dominant (centroid=3915) — the spectral shift exists but is muted at lower centroids.

---

## §5 — Files Modified

| File | Action | Description |
|------|--------|-------------|
| `composer_extension.py` | **UPDATED** | ZONE_DEFAULTS replaced with corpus values; CORPUS_ZONE_STATS added |
| `~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/composer_extension.py` | Path | Skill copy updated |
| `/tmp/zc_ca_test/results.json` | Generated | Corpus-aligned ZoneComposer test results |
| `/tmp/softsynth_test/compare_render.py` | Generated | Corpus reproducibility test script |

---

## §6 — Verified vs Refuted Claims

| Claim | Source | Verdict |
|-------|--------|---------|
| ZONE_DEFAULTS centroids are wrong | Evening session (hypothesis) | **CONFIRMED** — 13× error on Z1, fixed now |
| Updating ZONE_DEFAULTS improves accuracy | (hypothesis) | **REFUTED** — 22.2% unchanged; metadata-only fix |
| ZoneComposer and SongBuilder differ | Prior analysis | **REFUTED** — identical audio for same parameters |
| Corpus centroid values (5488-9302 Hz) are reproducible | (assumed) | **REFUTED** — 17× gap; corpus values not reproducible from current pipeline |
| Dominant band structure at zone 5/6 boundary | This session | **CONFIRMED** — mid→high_mid switch preserved even at low centroids |
| BPM extracted as 125 from corpus-aligned MODs | (assumed) | **REFUTED** — Essentia extracts 167 BPM regardless of MOD header BPM |

---

## §7 — Open Questions

1. **Pipeline origin of corpus centroids:** How did `dataset_balanced_900.npz` get features with centroids 5488-9302 Hz? Need to audit the original generation environment/parameters. The 15.46s looped playback might be the key — if data_collector used a different rendering path that produced correct-length audio, the MIR features would differ.

2. **SoftSynth vs ffmpeg:** Does SoftSynth render MODs differently? Can't test without `synth` module import working.

3. **Pattern order termination:** Does `mod_obj.write()` properly set song length and pattern order? The Speed=0/Tempo=0 in MOD header is suspicious.

4. **Does the original data_collector generation still work?** Running `data_collector.build_dataset()` would reveal whether the current pipeline produces corpus-matching features.

---

## §8 — Recommended Next Actions

1. **Run data_collector.build_dataset()** to regenerate a *fresh* dataset from current pipeline → compare MIR features with `dataset_balanced_900.npz`. If they diverge, the corpus is stale.
2. **Test SoftSynth rendering** from `audio-renderer` skill — compare centroid output vs ffmpeg for same MOD.
3. **Inspect ModWriter.write()** for song length and pattern order bugs (Speed/Tempo = 0 issue).
4. **If corpus is indeed stale:** regenerate the balanced dataset, retrain the classifier, re-validate ZoneComposer accuracy.
5. **Update CORPUS_ZONE_STATS** if corpus is regenerated (keep in sync with actual pipeline output).

---

*Session conclusion: The ZONE_DEFAULTS fix was real but superficial. The deeper problem is a pipeline disconnect between how the corpus was generated and how ZoneComposer generates today. Metadata fixes don't fix audio.*
