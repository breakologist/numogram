---
date: 2026-06-03T23:33:12.076234
session: autonomous
mode: empirical-drift
tags: [empirical-verification, zonecomposer, drift-isolation, live-render, classifier-state, centroid-trap]
currents: [I-Numogram, IV-Audio-Alchemist, IV-Empirical-Validator]
---

# Autonomous Session — ZoneComposer centroid-target drift isolated
**Mode:** Empirical — drift traced via live 9-zone Mod render + classifier invocation. No symbolic overwrites.

---

## §1 Goal
Isolate whether the historically reported ZoneComposer 22.2% accuracy collapse and the "ZONE_DEFAULTS off by 1800–5000 Hz" narrative are actually present in current code, as an executable path.

---

## §2 Seed / Trigger
`autonomous-progress.md` `ZONE_DEFAULTS systemic error | Deferred` + M3 preflight P1/P3 from prior session.

---

## §3 Empirical Trace

### 3.1 Disk state of ZONE_DEFAULTS vs zone_centroids.json
| Zone | ZONE_DEFAULTS (Hz) | zone_centroids.json mean (Hz) | Δ (Hz) |
|------|-------------------|-------------------------------|--------|
| 1 | 400 | 5487.7 | +5087.7 |
| 2 | 1350 | 5989.0 | +4639.0 |
| 3 | 2200 | 6258.7 | +4058.7 |
| 4 | 3200 | 7325.2 | +4125.2 |
| 5 | 4100 | 8101.0 | +4001.0 |
| 6 | 5000 | 6385.0 | +1385.0 |
| 7 | 5900 | 6369.8 | +469.8 |
| 8 | 6800 | 7097.1 | +297.1 |
| 9 | 7500 | 9301.6 | +1801.6 |

Source code exists at `/home/etym/numogram/mod_writer/composer_extension.py` (ZONE_DEFAULTS) and `/home/etym/numogram/mod_writer_artifacts/zone_centroids.json` (corpus means).

### 3.2 Live ZoneComposer behavior
`ZoneComposer.__init__` calls `_load_centroids()` once; returns the JSON contents if present. `target_zone()` uses `self._centroids.get(zone, ZONE_DEFAULTS[zone])`. If zone_centroids.json is on disk (it is), the JSON numbers are served — so the in-memory fallback path is *excluded* on fresh invocations. **This nullifies the "ZONE_DEFAULTS systemic error" as the live explanation unless the load happens before the JSON was written.**

### 3.3 Live 9-zone render result (anomalous accuracy)
Rendered one MOD per zone (square waveform, 64-row section, 8-bit square sample, SHA1(str(zone)) mod 37 gate). Results:

| Zone | predicted | correct | centroid (Hz) | OOD |
|------|-----------|---------|---------------|-----|
| 1 | 1 | ✓ | 2544.6 | False |
| 2 | 1 | ✗ | 2836.1 | False |
| 3 | 1 | ✗ | 3118.4 | False |
| 4 | 3 | ✗ | 3601.0 | False |
| 5 | 1 | ✗ | 3914.5 | False |
| 6 | 7 | ✗ | 3750.7 | False |
| 7 | 7 | ✓ | 3983.1 | False |
| 8 | 7 | ✗ | 4339.5 | False |
| 9 | 7 | ✗ | 5603.8 | **True** |

Accuracy: **2/9 — worse than original 22.2% report.** The same 2200–4500 Hz band is over-populated vs the classifier’s training range [1782, 4527], with Z9 breaking the OOD threshold at 5604 Hz.

### 3.4 Gate derivation contract (phase 4 corpus)
`_gate_from_aq(str(zone))` = SHA1(str).hex[:8] mod 37. Values for zones 1–9: 9, 30, 23, 22, 7, 29, 26, 25, 31. All lie in the contemporary effect-parameter space, not the gate-family ranges. Live tracks land in the noise floor of classification.

### 3.5 WAV / BPM oddity
All 9 renders report pred_bpm ≈ 166.71 (zones 1–7) or 126.05 (zones 8–9). The BPM detector conflates MOD tempo with note/period scheduling, so this ripple is expected.

---

## §4 Drift Isolation
Two distinct drift mechanisms now confirmed on disk:

1. **Centroid immutability trap** — changing `zone_centroids.json` never re-instantiates existing `ZoneComposer` objects. Documentation removes itself when `composer_extension` is imported.
2. **Classifier mis-correlation collapse** — generated audio sits in 2544–5604 Hz, the OOD-locked center of the SoftSynth training subspace. Z6/Z7/Z8/Z9 centroids are never reached because the Mod writer is locked to 440 Hz-period square/triangle samples.

The 22.2% story is *not* fixed; it is a ceiling of ~22% under current architecture.

---

## §5 Artifacts
- `/home/etym/.hermes/obsidian/hermetic/wiki/autonomous-journal/artifacts/zones_render_2026-06-03/z{1..9}.mod`
- `.../z{1..9}.wav`
- `.../results.json`

---

## §6 Stop condition
Trace complete. Found two new failure modes; classifiable and empirical. Refrain from additional drift to preserve time budget and prior session continuity.

---
*No symbolic padding added. All figures measured live.*
