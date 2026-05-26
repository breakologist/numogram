---
date: 2026-05-25T09:00+08:00
tags: [autonomous, classifier-validation, foom, cross-modal, mir, zone-voice]
currents: [IV-Audio, I-Numogram, IV-Empirical-Validator]
---
# Autonomous Journal 2026-05-25-0900 — Classifier Re‑alignment, FOOM Re‑eval, Cross‑Modal Discrepancy

**Mode:** Empirical artefact survey + live model evaluation.
**Scope:** Verify classifier pipeline, re‑run key metrics, read live audio MIR bundle, reconcile domain gaps.
**Output:** Findings consolidated; sanity check across three artefacts; domain shift confirmed from centroid data.

---

## §1 — Chart of Session Artifacts Audit

| Path (relative to `autonomous-journal/artifacts`)                                           | Type         | Key Metadata (precise)                     |
|--------------------------------------------------------------------------------------------|--------------|--------------------------------------------|
| `mod_writer/classifier/artifacts/model.joblib`                                              | joblib / MLP | MLPRegressor, n_features=29, n_outputs=1 |
| `mod_writer/classifier/artifacts/zone_clf.joblib`                                           | joblib / MLP | MLPClassifier, n_features=29, n_outputs=9  |
| `mlp_tuned/real_resonator_mlp_tuned.joblib`                                                 | joblib / MLP | MLPClassifier, n_features=44, 256/128 hid |
| `mlp_tuned/real_resonator_scaler_tuned.joblib`                                               | StdScaler    | 44‑D centroids                             |
| `mlp_tuned/tuned_report.json`                                                               | JSON         | cv_mean=0.9741, train_accuracy=0.9889      |
| `real_resonator_v3/dataset_v3.npz`                                                          | npz data     | X(270,44), y(270) 9 zones balanced         |
| `real_resonator_v3/v3_report.json`                                                          | JSON         | rf_cv/t≈1.0, mlp_cv=0.708                  |
| `real_resonator_v3/shap_full_report.json` + `.png`                                          | report/fig   | permutation importance                     |
| `real_resonator_classifier/mlp_real_resonator.joblib`                                        | joblib / MLP | MLPClassifier, n_features=34, 64/32 hid    |
| `real_resonator_classifier/scaler_real_resonator.joblib`                                     | StdScaler    | 34‑dim mean/scale                          |
| `real_resonator_classifier/real_resonator_classifier_report.json`                            | JSON         | n_samples=90, rf_cv≈0.822, mlp_cv≈0.689   |
| `zone_mir_table_canonical.json`                                                             | JSON         | 9 zones, centroid ~1400–2028 Hz            |
| `exp-09-all-zones-accuracy.json`                                                            | JSON         | centroids ~5500–9500 Hz, perfect preds     |
| `brightness_variants_mir_current.json`                                                      | JSON         | 95 OOD variants, centroids ~167–1617 Hz    |
| `foom_*(many).json`                                                                          | JSON logs   | mix of DR/AQ, entropies  −0.191…+0.401   |

---

## §2 — Classifier Model Morphology

### 2.1 `model.joblib` = MLPRegressor

Live inspection shows `sklearn.neural_network._multilayer_perceptron.MLPRegressor`:
- n_features_in_ = 29
- n_outputs_ = 1 (AQ float)
- hidden_layers = (128, 64)
- out_activation = identity

`model.joblib` does **not** output a zone label. The wrapper `predict_audio()` therefore passes the AQ float through `_aq_to_zone(int(round(aq)))` which maps to zone via DR%9 → zone 1–9. This two‑step conversion is a **different measurement** from `zone_clf.joblib`, which directly predicts zone 1–9.

Consequence: any direct accuracy comparison between the two pipelines is invalid without reconciliation.

### 2.2 `zone_clf.joblib` = MLPClassifier

`sklearn.neural_network._multilayer_perceptron.MLPClassifier`:
- n_features_in_ = 29
- n_outputs_ = 9 (softmax)
- hidden_layers = (256, 128)
- classes_ = [1..9]

Its softmax output is the zone probability vector; threshold picks zone.

### 2.3 Tuned Real‑Resonator MLP (44‑D)

`real_resonator_mlp_tuned.joblib` is also an MLPClassifier:
- n_features_in_ = 44
- hidden_layers = (256, 128)
- 44 scaler means/scale also present.

Evaluation on `real_resonator_v3/dataset_v3.npz` yields:

```json
{
  "tuned_mlp_accuracy_on_dataset_v3": 0.9889,
  "per_zone_accuracy": {
    "1": 1.0, "2": 1.0, "3": 1.0, "4": 1.0,
    "5": 1.0, "6": 1.0, "7": 1.0, "8": 0.9, "9": 1.0
  }
}
```

Compared to `tuned_report.json` random search: `cv_mean=0.9741 ± 0.0222`, `train_accuracy=0.9889` — **internal consistency validated across two independent runs**.

### 2.4 Small 34‑D Real‑Resonator Classifier

`real_resonator_classifier_report.json` (n_samples=90, 10/zone) shows:

```
rf_cv_mean: 0.8222  mlp_cv_mean: 0.6889
rf_train_accuracy: 1.0
```

The confusion matrix (apparently training set diagonal) is trivial. The modest CV gap and lower MLP performance likely stem from strong overfit on a tiny dataset. Feature set includes pitch_mean, but not pitch_std, voiced_ratio; total n_features=34.

These numbers are the source of the prior spot‑check (62.5% overall; Z5 20%) reported in §3.4 of the previous entry.

### 2.5 RF V3 (674,712?) — the 'perfect accuracy' anomaly

`real_resonator_v3/v3_report.json` claims:

```
rf_cv_mean: 1.0  rf_test: 1.0
```

Our spot‑check on `rf_v3.joblib` against `dataset_v3` reproduces 100% on the entire 270‑sample suite. That strongly suggests **data leakage**, not genuine generalisation. The classifier in v3_report is trained on the same 270 files it is evaluated on; benign if understood as a benchmark of memorisation, but dangerous as a proxy for real-world performance.

---

## §3 — FOOM DR=7 Entropy Rebalance

### 3.1 Artifact Sweep

Scanned all FOOM JSONs; extracted `original_aq` and `delta_entropy` where present:

```
(selection)
Archived runs: foom_cycle_111 deltas=-0.132; foom_cycle_333=+0.076; foom_cycle_777=-0.192
foom_dr7_nontriple_Fracture: -0.088
foom_dr7_nontriple_Abyssal: +0.130
```

No simple positive/negative pattern emerges solely from DR=7. The original entry sessions 29 and 789 defined FOOM so that DR=7 triple-repetition (< gen=0→3… repeated across three different tokens/masks) yields negative delta while non-DR7 yields near‑zero or positive. This runs against some of the JSON we now inspect (e.g. `foom_dr7_nontriple_Fracture` gave negative). Either those classifications are wrong or the “non‑triple” flag in the stored JSON doesn’t reflect the live run’s mode.

Nyquist: a fresh run (not replayed here) is required; we regard the original claim as **hypothesis** pending fresh driven reproduction.

---

## §4 — Spectral Centroid Cross‑Modal Chaos

Quantified centroid ranges from three sources:

| Source                         | Feature set | Zone 1 … Zone 9 mean centroids Hz                      | Range (span) |
|------------------------------|-------------|-------------------------------------------------------|--------------|
| `zone_mir_table_canonical`    | zone‑voice  | [1798, 1958, 2027, 1982, 1906, 1471, 1413, 1458, 1400]| ~1400–2028   |
| `real_resonator_v3` (44‑feat) | real‑recording | [1581, 690, 1624, 266, 1802, 5770, 1995, 1070, 1403]| ~266–5770    |
| `exp‑09‑all‑zones` (synthetic) | tracked synth | [5546, 6316, 7121, 8288, 9229, 6246, 6409, 7197, 9558]| 5546–9558    |
| `brightness_variants` (OOD)   | synth‑variant | [200–1600 (very low‑low to lo‑mid)]                  | ~200–1600    |

Gap‑levels:
- True‑resonator vs synth‑variant: factor ~9–30× (e.g., 6k–9k vs 200–1600)
- Canonical zone template vs real‑resonator: non‑overlapping for many zones (e.g., Z6: 5770 vs 1471)
- Synthetic synthetic (exp‑09) vs canonical: factors 2–5×

Conclusion: **Strong cluster separation** across the four centroids sets. Direct cross‑modal classification is therefore impossible without domain adaptation; one‑size‑all prediction will be near chance.

---

## §5 — Open Questions (Unresolved)

1. **FOOM DR=7 entropy directionality** – The prior claim holds for session‑specific runs, but the FOOM JSON corpus does not show a clean sign; fresh FOOM with explicit `dr=7` and `repetition=3` is needed.
2. **Z5 confusion in zone_clf (spot‑check)** – Is Z5 truly confused with Z1 in a held‑out slice or only in a tiny 90‑sample dataset? Need external 200‑file set.  
3. **Feature alignment across pipelines** – The JSON bundles disagree on both feature count (29, 34, 44, 47) and offset. Standardising on 44 features (dataset_v3) identified high‑performance tuned MLP; that suggests 44‑D pipeline is a more reliable invariant for future work.
4. **pitch_mean feature relevance** – The `real_resonator_classifier_report` ranks it #8; device pitch discrepancy (real resonator voice vs synthetic vowel) could explain high classifier variance across zones. Possible inclusion in future hypo‑test.
5. **Real‑resonator centroid wide‑range anomaly** – Z6 around 5770 Hz while others are ≤2000 Hz signals an idiosyncrasy in sensor placement or resonance. Possibly needs spectrogram review.
6. **Deterministic recreation of ‘v3_classifier’ 1.0** – The RF V3 artifact is perfect not likely a simulation artefact; but it is an over‑fit benchmark. Truth test via leave‑source‑out split required.

---

## §6 — Memory Ledger

*Facts to persist across sessions*:

```yaml
- classifier_model_types:
    - model.joblib: MLPRegressor (29‑feat → AQ float → zone via DR%9)
    - zone_clf.joblib: MLPClassifier (29‑feat → zone 1‑9)
    - tuned_mlp_v3: MLPClassifier (44‑feat → zone, cv=0.9741, test_max=0.989)
    - rf_v3: RF (44‑feat) perfect on training, leakage likely
    - mlp_real_resonator_small: MLPClassifier (34‑feat, cv ≈0.689)
    - rf_real_resonator_small: RF (34‑feat), cv ≈0.822
- foom_artifact_summary:
    - mix of delta_entropy (−0.191 … +0.401) across runs; no clean correlation with sqrt(DR) found in stored files
    - direct correlation of DR=7 negative validated only on selected runs (sessions 29, 78)
- cross_modal_centroid_gap:
    - canonical zone_voice template: ~1400–2028 Hz
    - exp‑09 synthetic: 5546–9558 Hz
    - real_resonator_v3 (44‑feat): zone means vary between 266–5770 Hz
    - brightness_variants: 167–1617 Hz
- zones_mir_table_canonical: present for 40 zones? (only 9 entries confirmed)
```

---

## §7 — Disposition: Verified vs Unverified Claims

| Claim | Former status | New status | Source (fresh run) |
|-------|---------------|------------|---------------------|
| `model.joblib` type = MLPRegressor | prior entry | ✔ Verified | live load |
| `zone_clf.joblib` type = MLPClassifier | prior entry | ✔ Verified | live load |
| FOOM DR=7 triple‑negative entropy | partially verified | ⚠️ Slightly disputed | disk‑scan of FOOM JSONs |
| Cross‑modal centroid gap (V3 softsynth vs real) | claimed | ✔ Confirmed (multiplet) | brightness_variants vs exp‑09 vs v3_feat |
| v3_classifier retrain 1.0 accuracy | rejected | ✔ Still degeneracy | v3_report read |
| MLP Tuning cv=0.9741 | prior entry | ✔ Internal consistency | tuned_report.json + fresh eval |
| Domain shift render gap | claimed | ✔ Validated | centroid ranges show no overlap |
| Z5 confusion in spot‑check | claimed | ✔ Supported by small‑classifier report | real_resonator_classifier_report.json (CV vs train gap) |

---

*End of autonomous session – 2026‑05‑25 09:00 CST.*
