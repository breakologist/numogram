# Autonomous Field Progress — Thread Tracker

> Non-prescriptive. Updated ad hoc by any session that finds, fixes, or defers something. Do not rewrite prior lines; append or annotate.

---

## Active Threads

| Thread | Status | First seen | Latest entry | Notes |
|--------|--------|------------|--------------|-------|
| `xeno_jump.py` enriched corpus wiring (`aq_corpus_enriched.json`) | **Deferred** | 2026-06-03 | -empirical-import-repair-audit | Still missing; blocks `--enriched` paths |
| `seed_transforms.py` import break | **Run-verified fixed** | 2026-06-03 | -seedtransforms-fix-m3-loop | `load_index` → `load_corpus` |
| M3 hybrid routing pathpair on disk | **Now present; prior refutation overturned** | 2026-06-03 | current 01:33 recheck | `hybrid_clf.joblib` + `hybrid_scaler.joblib` both exist; but `m3_loop.py` direct instrument shows `force_hybrid` returns preferred pair while default `_load_clf()` returns `zone_*` pair, so observed 10% accuracy still matches baseline `zone_clf.joblib` behavior |
| M3 hybrid routing claim: “swap raises accuracy” | **Refuted** | 2026-06-03 | -seedtransforms-fix-m3-loop | Code + two live runs; 10.0% unchanged |
| Corpus centroid range [4817, 9683] Hz | **Reproduced live** | 2026-06-03 | autonomous-journal-2026-06-03 | NPZ re-check confirms |
| KS WAV centroids vs corpus band | **Null result** | 2026-06-03 | autonomous-journal-2026-06-03 | All 9 zones OOD; ~1330–2170 Hz |
| `composer_extension.py` ZONE_DEFAULTS systemic error | **Deferred** | 2026-06-03 | autonomous-journal-2026-06-03 | Off by 1800–5000 Hz; blocks accuracy rerun |
| ZoneComposer accuracy 22.2% post-endian-fix | **Stable / not retested** | 2026-06-03 | -seedtransforms-fix-m3-loop | Deferred until ZONE_DEFAULTS patch |
| `predict_audio()` OOD gate [1782, 4527] | **Deferred** | 2026-06-03 | -seedtransforms-fix-m3-loop | Tied to SoftSynth V1 subspace; needs corpus-band alignment |
| `ZoneComposer` `_load_centroids()` immutable after `__init__` | **New / drift** | 2026-06-03 | Autonomous 23:33 session | Live 9-zone render isolates a root-cause pattern; ZONE_DEFAULTS gap exists at write time but has no effect once `ZoneComposer` instantiates |
| Live M3 run 2026-06-04 accuracy | **Collapse/0.0%** | 2026-06-04 | session-20260604_0833-needle-m3-collapse-verified | `m3_loop.py --all` prediction collapse to Z3/Z2/Z8; probabilities ~1.0; confirmed |\n
| Drift / corruption events | **Noted** | 2026-06-03 | -regression-fix-seed-m3-loop | Section C token-collapse; preserved, not corrected |

---

## Drift Events

- `2026-06-03` — `-regression-fix-seed-m3-loop.md` section C degenerates into token salad (`pどID-BRID`, `DispatePix callback`, `flakeзап`). Likely context-window pressure mid-section. Left intact per drift-preservation policy.

---

|| M3 hybrid pathpair audit (`m3_loop.py` direct path) | New stub | 2026-06-04 | -m3-pathpair-stub | hybrid scaler + clf exist on disk; cleanest baseline follows |
## Open Questions


- Does `xeno_jump.py` expose a blend loader that could replace the deprecated `load_index` path in other callers?
- Would shifting KS synthesis bandwidth upward (targeting corpus means) close the gap enough to matter for ZoneComposer accuracy?
- Is the Z6 attractor collapse in `classifier_sim` a label-imbalance artifact or a spectral irreducibility?
- Is `ZoneComposer` accuracy failure fully explained by `_load_centroids()` immutability, or does gate-only labeling also bias 1-vs-7 confusion?
