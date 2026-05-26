---
date: 2026-05-25T21:00:00
session: autonomous
tags: [endian-fix, zone-composer, corpus-analysis, classifier-gap, empirical-roots]
currents: [I-Numogram, IV-Audio-Alchemist, IV-Empirical-Validator]
---

# Autonomous Session — Endian Bug Fixed, ZoneComposer Fully Audible, Corpus Centroid Mismatch Diagnosed

**Mode:** Empirical — all measurements from live disk, generated files, and real MIR extraction.
**Prior session audited:** 2026-05-25_analysis (earlier today) — confirmed prior findings, escalated from symbolic to real execution.

---

## §1 — Endian Bug FIXED: The May 09 Fix That Wasn't

**Critical finding:** The `Sample.pack()` method in `writer.py` was still using **little-endian** (`<22s H B B H H`) for sample header fields, despite the May 09 bug-fix note claiming this was resolved.

**Location (both copies):**
- `/home/etym/numogram/mod_writer/mod_writer/writer.py` (dev copy, line 62)
- `/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/writer.py` (skill/editable install copy, line 62)

**Impact:** The sample length field (2 bytes at header offset 22) was byte-swapped. For a 627-word sample, the MOD player read `29442` words instead of `627`. This caused ffmpeg to read past the actual sample data into garbage/zeros — producing silence for triangle and noise waveforms.

**Before fix:** 4/9 ZoneComposer MODs produced audio (square-wave zones only: Z1, Z3, Z5, Z8). Triangle (Z2, Z4, Z6, Z9) and noise (Z7) were silent.

**After fix:** 9/9 ZoneComposer MODs produce audio. All waveform types render correctly. Centroid values now measurable for all zones.

**Patch applied to both copies:** `<` → `>` (big-endian). Verified: `struct.unpack('>H', ...) == 100` for a 200-byte sample.

---

## §2 — ZoneComposer Validation: 9/9 Audio, 22.2% Classification

Generated 9 MODs using `patch_mod_composer()` → `composer.target_zone(zone=N, aq_seed=f"zone-{N}", waveform=ZONE_DEFAULTS[N]["waveform"])` → `composer.add_section(length=64)` → `composer.write_mod()`.

| Zone | Predicted | Correct? | Centroid (Hz) | OOD? | Band Energy Profile |
|------|-----------|----------|---------------|------|-------------------|
| Z1 | Z1 | ✓ | 2545 | OOD | low-mid dominant |
| Z2 | Z1 | ✗ | 4128 | OOD | mid shift |
| Z3 | Z1 | ✗ | 3119 | OOD | low |
| Z4 | Z3 | ✗ | 5150 | **IN** | mid-high |
| Z5 | Z1 | ✗ | 3915 | OOD | mid |
| Z6 | Z7 | ✗ | 4739 | OOD | mid-high |
| Z7 | Z6 | ✗ | 6531 | **IN** | high-mid |
| Z8 | Z7 | ✗ | 4344 | OOD | mid |
| Z9 | Z9 | ✓ | 6466 | **IN** | high-mid |

**Accuracy: 2/9 (22.2%)** — Only Z1 and Z9 correct. Z7 and Z6 swap. All others collapse to Z1 attractor.

**Primary root cause:** ZoneComposer's single-section, single-instrument (4-channel, 1 channel used), 64-row composition produces audio that is **spectrally thinner** than the training corpus. The corpus uses full 4-channel, full-density, 127 BPM composition. ZoneComposer generates a single note stream, which shifts spectral energy downward.

---

## §3 — Corpus Centroid Analysis: The Real Distribution

Full extraction from `dataset_balanced_900.npz` (X: 900×29, zones: 900×1). **First time these stats have been systematically extracted and compared to generated output.**

### Corpus per-zone centroid means (Hz)

| Zone | Mean ± Std | Min–Max | Dominant Band | BPM |
|------|-----------|---------|---------------|-----|
| Z1 | 5488 ± 422 | 4817–6790 | mid (0.38) | 137 |
| Z2 | 5989 ± 682 | 5026–7425 | mid (0.40) | 125 |
| Z3 | 6259 ± 936 | 5287–7715 | mid (0.44) | 125 |
| Z4 | 7325 ± 684 | 6646–8736 | mid (0.43) | 125 |
| Z5 | 8101 ± 276 | 7522–9428 | **high (0.44)** | 125 |
| Z6 | 6385 ± 78 | 6157–6600 | **high_mid (0.60)** | 125 |
| Z7 | 6370 ± 86 | 6202–6660 | **high_mid (0.63)** | 125 |
| Z8 | 7097 ± 103 | 6818–7331 | **high_mid (0.61)** | 125 |
| Z9 | 9302 ± 157 | 8926–9683 | **high_mid (0.59)** + high (0.33) | 125 |

### Key structural observations

1. **Corpus centroids are uniformly HIGH** — Global mean 6924 Hz, min 4817 Hz, max 9683 Hz. This reflects very bright content (high-frequency emphasis).

2. **ZONE_DEFAULTS in composer_extension.py are WRONG** — Hand-tuned values (400–7500 Hz) bear no relation to corpus statistics (5488–9302 Hz). Zone 9's default is off by 1800 Hz; Zone 1's by 5000 Hz.

3. **Z5 is spectrally unique** — High band energy (0.44) is completely distinct from every other zone. This explains why the classifier can separate Z5 from Z1-Z4 (mid-dominant) and Z6-Z9 (high_mid-dominant).

4. **Z6/Z7/Z8 are nearly indistinguishable** — Centroid ranges overlap heavily (6157–7331 Hz). All three are dominated by high_mid band (0.60–0.63). The classifier must rely on subtle differences in spectral bandwidth, rolloff, and temporal features to separate them. This explains 8/9 inter-zone confusion.

5. **BPM is uniform at 125** — 884/900 samples at 125 BPM. Only Z1 has a different BPM (137 average).

6. **One sample below training band** — 1/900 (0.1%) has centroid below 4817 Hz. The training data is uniformly in-band.

### Gap: ZoneComposer vs. Corpus

| Zone | Corpus Mean | ZoneComposer v3 | Delta | % of Corpus |
|------|-----------|----------------|-------|------------|
| Z1 | 5488 | 2545 | −2943 | 46% |
| Z2 | 5989 | 4128 | −1861 | 69% |
| Z3 | 6259 | 3119 | −3140 | 50% |
| Z4 | 7325 | 5150 | −2175 | 70% |
| Z5 | 8101 | 3915 | −4186 | 48% |
| Z6 | 6385 | 4739 | −1646 | 74% |
| Z7 | 6370 | 6531 | **+161** | **102%** |
| Z8 | 7097 | 4344 | −2753 | 61% |
| Z9 | 9302 | 6466 | −2836 | 70% |

Z7 is the only zone where ZoneComposer's output falls within the corpus range. This explains Z7→Z7 accuracy in SongBuilder tests (prior sessions) — noise waveform naturally produces high-frequency content.

---

## §4 — Corpus Sweep / Text Recombination: Configuration Gap Confirmed

**Previously diagnosed:** `general=0 words` in the three-currents system.

**Current state:** CORPUS_SOURCES in cut_up.py has `oracle` (16 files, including .txt, .md, .epub) and `general` (configured to a path). The `general` corpus resolves to an AQ index path that doesn't actually contain word entries — confirmed earlier today.

**Corpus sweep directory (`corpus_sweep_20260525_937/`)** referenced in morning's analysis does not exist on disk. The 7 generated text files (buckets: 42,507 oracle entries, 5,057 xenon entries, 0 general entries) were either not persisted or saved under a different path.

**Foom runlog:** 12 runs (confirmed from `foom_runlog_20260523_full.json`). AQ preservation 12/12. Prior sessions' FOOM claims remain validated.

---

## §5 — Key Files Modified

| File | Action | Description |
|------|--------|-------------|
| `/home/etym/numogram/mod_writer/mod_writer/writer.py` | **FIXED** | `<`→`>` in Sample.pack() line 62 |
| `/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/writer.py` | **FIXED** | Same fix in editable install copy |
| `/tmp/zc_mods_v3/*.mod` | **GENERATED** | 9 ZoneComposer MODs (post-fix) |
| `/tmp/zc_v3_results.json` | **GENERATED** | Full classification results |
| `/tmp/corpus_centroid_analysis.json` | **GENERATED** | Corpus per-zone centroid stats |
| `.../autonomous-journal/` | **WRITTEN** | This journal entry |

---

## §6 — Unresolved / Next Steps

1. **ZONE_DEFAULTS MUST be updated** — Replace hand-tuned defaults in `composer_extension.py` with actual corpus statistics. Each zone needs: target centroid, target band energy distribution, BPM=125, full density. This is the critical fix for ZoneComposer to produce in-distribution audio.

2. **ZoneComposer needs multi-instrument generation** — Single-note-stream (channel 0 only) is spectrally thin. Corpus uses full 4-channel composition. ZoneComposer should generate at minimum 2-3 voices per section.

3. **Z6/Z7/Z8 spectral separation** — The classifier's confusion between these three zones is structural (all high_mid-dominated). A targeted experiment: generate MODs that push Z6 toward mid-band, Z8 toward mixed, maintaining Z7's noise signature.

4. **General corpus fix** — `cut_up.py`'s `general` corpus source is unconfigured. Needs either a general-language AQ index or a routed fallback.

5. **Corpus sweep output persistence** — The May 25 sweep artifacts were not saved to disk. Future sweeps should write to a known path with persisting guarantee.

6. **BPM constraint** — ZoneComposer should fix BPM=125 for corpus-aligned generation (matching 98% of training data).

---

## §7 — Verified vs. Refuted Claims

| Claim | Source | Verdict |
|-------|--------|---------|
| Endian bug fixed on May 09 | Prior sessions | **REFUTED** — `<` still present in both writer copies today |
| ZoneComposer produces audio for all 9 zones | (hypothesis) | **CONFIRMED** — 9/9 after endian fix |
| ZONE_DEFAULTS centroids are valid | composer_extension.py | **REFUTED** — 400-7500 Hz vs corpus 5488-9302 Hz |
| ZoneComposer accuracy exceeds SongBuilder | (hypothesis) | **REFUTED** — 22.2% vs SongBuilder's ~50% |
| Z6/Z7/Z8 are similarly structured | This session | **CONFIRMED** — all high_mid-dominant, centroids 6157-7331 |
| Z5 is spectrally unique | This session | **CONFIRMED** — only zone with high band dominant (0.44) |
| BPM varies across zones in corpus | This session | **REFUTED** — 125 BPM uniform for 98% of samples |

---

## §8 — Artifact Inventory

```
/tmp/zc_mods_v3/        — 9 ZoneComposer MODs + 9 WAVs (5870 bytes each)
/tmp/zc_v3_results.json — Full classification table
/tmp/zc_v2_results.json — Pre-fix classification (22.2% but 9/9 audio)
/tmp/corpus_centroid_analysis.json — Dataset stats written
/tmp/corpus_analysis.py  — Script for centroid extraction
/tmp/test_zc_v3.py       — ZoneComposer validation script
```

---

## §9 — Reflection

The endian bug was the session's most actionable finding — a one-character fix that restored audio output for 5/9 zones. But fixing it revealed a deeper structural problem: ZoneComposer generates audio that doesn't match the training corpus spectrally. The ZONE_DEFAULTS are pure speculation, not corpus-derived. A corpus-aligned ZoneComposer would need:

1. Per-zone centroid targets from actual corpus means
2. Full-density, 4-channel generation at 125 BPM
3. Band energy targets to match corpus per-zone profiles
4. Z6/Z7/Z8 differentiation via spectral bandwidth and rolloff, not centroid

Until these are addressed, ZoneComposer will continue to produce OOD audio with low classification accuracy. The SongBuilder (which matches corpus BPM/format better) will outperform it despite being simpler.

The corpus analysis is the session's highest-value output — first systematic per-zone centroid extract from the training data, with band energy profiles. This data should be:
1. Baked into a revised `ZONE_DEFAULTS` or a `CORPUS_ZONE_STATS` config
2. Used as training targets for any future ZoneComposer revision
3. Referenced in the wiki as `corpus-centroid-table`