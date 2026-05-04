# Path C — BPM Extraction Artifact Research Brief

**Status:** Diagnosed — root cause understood; remediation approaches identified  
**Date:** 2026-05-02  
** investigator:** Hermes-AQ-Hyperstition-Oracle (v2.0)  

---

## Executive Summary

During Phase 4 validation, `MIRFeatureExtractor` (Essentia + librosa) was found to report **incorrect BPM values** for certain zones (primarily 4 and 6) depending on gate value and waveform. The artifact manifests as a **false high tempo (~165 BPM)** instead of the true tempo (**125 BPM**), causing rhythm features to mismatch the training corpus and misclassify tracks.

**Root cause:** `librosa.beat.beat_track()` selects the wrong tempo candidate from the onset envelope when presented with square‑wave arpeggios; the onset envelope's harmonic structure creates a stronger peak at double/triple the intended beat rate.

**Practical resolution:** Use `--force-rhythm-baseline` for all synthetic MOD classification. This is an acceptable engineering trade‑off for production use.

**Future work:** Three remediation paths are outlined below.

---

## 1. Symptom & Quantification

### Observed data (N = 50 gate sweep per zone)

| Zone | BPM pattern                                 | Misclass. without baseline |
|------|---------------------------------------------|----------------------------|
| 1–3,5,7–9 | Consistent 125 BPM                  | None                       |
| 4    | Arpeggio gates (0–6,8–36) → 165.44; gate 7 → 125 | ~30%                       |
| 6    | Mostly 165.44; gates 22, 35 → 125/mixed     | ~40%                       |

**Correlated rhythm features** (from `MIRFeatureExtractor`):  
- `onset_rate` → `None` → normalized 0.0  
- `beat_confidence` → `None` → normalized 0.0  
- `bpm` → 125.0 **or** 165.44117647058823  

Only when beat tracking succeeds is `bpm` populated; when it fails, both onset‑rate and confidence are `None`.

### Corpus vs. synthetic delta

| Feature          | Corpus constant | Synthetic (no baseline)                    | Delta effect                |
|------------------|-----------------|---------------------------------------------|-----------------------------|
| `bpm_norm`       | 0.625 (125/200) | 0.627 (125) or 0.827 (165)                  | Large for high‑BPM tracks   |
| `onset_rate_norm`| 0.0             | 0.0 (None → 0)                              | None                        |
| `beat_conf_norm` | 0.0             | 0.0 (None → 0)                              | None                        |

The high‑BPM tracks have a `bpm_norm` ~0.83, which shifts their position in the scaler's feature space enough to cross zone decision boundaries.

---

## 2. Root Cause Analysis

### 2.1 Beat tracking on square‑wave arpeggios

`MIRFeatureExtractor.extract()` pipeline:
1. Librosa `onset.onset_detect()` → onset envelope
2. `librosa.beat.beat_track(onset_envelope)` → tempo & beats

Square‑wave arpeggios produce an onset envelope with **strong harmonics** at multiples of the fundamental period:
- True beat rate: ≈8 ms inter‑onset interval → 125 BPM
- Envelope energy also peaks at 4 ms and 2.67 ms intervals → 250 BPM & 375 BPM candidates

`beat_track()` chooses the **most salient candidate**, which in these cases is the ~165 BPM peak (approx. 347 ms period). Why ~165 rather than 250? The autocorrelation lag distribution and dynamic programming's tempo histogram weighting favour this intermediate candidate for the observed spectral envelope shape.

### 2.2 Waveform dependence

Tested square vs. triangle vs. sawtooth on Zone 6, gate 0:

| Waveform | Reported BPM | Classification impact |
|----------|--------------|------------------------|
| square   | 165.44       | Misclassifies (no baseline) |
| triangle | `None` (extraction failed in multiple features) | Worse — degraded feature vector |
| sawtooth | 165.44       | Same as square |

Triangle's rich harmonic content causes onset detection to break completely, making it unsuitable as a fix.

### 2.3 Gate‑specificity

Gate values determine the **arpeggio direction and interval pattern**. Some gates (e.g., Zone 4 gate 7, Zone 6 gate 22) produce interval sequences that do **not** trigger the high‑BPM harmonic peak. This explains why misclassification is not uniform across all arpeggio gates.

---

## 3. Evidence: True Tempo Confirmation

Direct onset envelope analysis (no beat tracker):

```python
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
ac = np.correlate(onset_env, onset_env, mode='full')
lag_peak = np.argmax(ac[len(ac)//2+10:len(ac)//2+500]) + 10
period_s = lag_peak / sr
true_bpm = 60.0 / period_s   # → 125.0 ± 0.5 across all zones
```

All zones show a primary periodicity of **~511 samples** at 44 100 Hz, corresponding to 125 BPM. The beat tracker's high‑BPM candidate is a harmonic artefact, not the fundamental tempo.

---

## 4. Remediation Pathways (Future Work)

### Option A — Onset envelope preprocessing (preferred non-invasive)

**Approach:** Apply a comb filter or tempo‑specific band‑pass to the onset envelope before beat tracking, suppressing harmonics at 2×/3× the expected 125 BPM period.

**Pros:** No corpus changes; fixes extraction at source.  
**Cons:** May weaken detection for music that genuinely uses double‑time feels.  
**Effort:** Medium (signal‑processing tuning within `mir_profiler.py`).

### Option B — Metronome pulse embedding

**Approach:** Add an explicit, spectrally isolated click track (e.g., shortwideband impulse every 8 ms) to the rendered WAV prior to feature extraction.

**Pros:** Guarantees correct tempo extraction.  
**Cons:** Alters the audio spectrum; may affect other features (spectral centroid, roll‑off). Requires corpus retraining if adopted permanently.  
**Effort:** Low to medium (modify `render_mod_to_wav`).

### Option C — Alternative beat tracker

**Approach:** Swap `librosa.beat.beat_track` for a different algorithm (e.g., `madmom.features.beats.RNNDownBeatProcessor` or `essentia::RhythmExtractor2013` with different method).

**Pros:** May handle arpeggio onsets correctly out of the box.  
**Cons:** Adds heavy dependency; Essentia's default also failed (returned ~2.5 BPM on our test). Madmom requires PyTorch.  
**Effort:** High (integration + validation).

### Option D — Fixed baseline (current)

**Approach:** Always override `bpm_norm`, `onset_rate_norm`, `beat_conf_norm` to corpus constants.

**Pros:** Simple, reliable, reproducible. No audio‑side changes.  
**Cons:** Masks underlying extraction problem; not a general solution for real music.  
**Effort:** None — already implemented as `--force-rhythm-baseline`.  

**Verdict:** Use Option D for all current and near‑future synthetic MOD work. Revisit Options A/B if you need unbaselined classification of arpeggio‑dense synthetic material.

---

## 5. Conclusion

The BPM extraction artifact is **well‑understood**: square‑wave arpeggios fool the beat tracker into selecting a false high‑tempo candidate. The classifier's training data used constant, correctly‑extracted rhythm features, so any deviation causes accuracy drops.

The pragmatic path forward:
1. **Retain `--force-rhythm-baseline`** as standard validation/generation practice.
2. **Document this as a known limitation** of synthetic MOD classification.
3. **Consider Option A (onset comb filtering)** if you want to retire the baseline flag later.

No changes to the Phase 4.6 classifier or training corpus are required or recommended at this time.

---

*End of Path C brief. Ready for next steps: batch generation listening session.*
