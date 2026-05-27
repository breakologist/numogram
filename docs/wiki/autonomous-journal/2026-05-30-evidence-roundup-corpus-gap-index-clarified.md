---
date: 2026-05-30T23:15:00Z
session: autonomous-cron
duration_min: ~25
tags: [empirical-verification, corpus-gap, centroid-index-resolved, hybrid-clf-verified, zone-clf-mlp-audit, fixed-point-inventory, enriched-corpus-demoted]
currents: [IV-Audio, IV-Empirical-Validator, I-Numogram]
generates:
  - ~/.hermes/obsidian/hermetic/wiki/autonomous-journal/2026-05-30-evidence-roundup-corpus-gap-index-clarified.md
verifies:
  - hybrid_clf.joblib exists at 12.2 MB, RF 500 trees
  - hybrid_clf achieves 100% on both SS and Orig datasets
  - zone_clf.joblib is an MLP (0.7 MB), 10.6% on cross-domain
  - All 4 dataset files have STALE metadata claiming Phase 4.1 / 2026-04-30
  - The enriched oracle corpus has 2× words and 535 buckets but is NOT the default
  - xeno_jump `--corpus enriched` dramatically outperforms `--corpus oracle`
---

# Autonomous Journal 2026-05-30 — Evidence Roundup: Centroid Index Resolved, Corpus Gap Found, Hybrid CLF Verified

**Mode:** Empirical — every claim verified against live disk, dataset loading, classifier inference, and text recombination tool execution.

---

## §1 — Centroid Index Confusion: RESOLVED

**The May 26 journal's claim that "dataset centroid range is [2759, 3934] Hz" was reading BANDWIDTH (feature index 7), not CENTROID (feature index 6).**

The `dataset_softsynth_ss_100pz.npz` actually has:

| Feature | Index | Actual Range | What the May 26 journal said |
|---------|-------|-------------|------------------------------|
| Centroid | 6 | **1782–4527 Hz** | "2759–3934 Hz" |
| Bandwidth | 7 | 2759–3934 Hz | _(no mention)_ |

**Impact:** The OOD comment in `__init__.py` was correct all along. The "dataset range" the May 26 journal derived was bandwidth, not centroid. The single-sample SoftSynth tests (1782–4527 Hz) and the batch SS dataset (1782–4527 Hz centroid at index 6) are **consistent**. There was never a "dataset mismatch" — there was a misread feature index.

The classifier works on feature index 6 (centroid). The autonomous journals had been reading feature index 7 (bandwidth). This is now explicitly documented with a WARNING comment in both `data_collector.py` (line 276) and `__init__.py` (lines 99-104).

**Resolution:** The "two ranges" from the May 26 journal were an artifact of reading the wrong column. The true centroid range [1782, 4527] is the same for both single-sample and batch-generated SS datasets.

### Per-Zone REAL Centroid Data (idx 6, finally correct)

| Zone | Centroid (mean ± std) Hz | Bandwidth (mean ± std) Hz |
|------|------------------------|--------------------------|
| Z1 | 1829 ± 36 | 2796 ± 29 |
| Z2 | 1958 ± 17 | 2883 ± 12 |
| Z3 | 2146 ± 20 | 3007 ± 12 |
| Z4 | 2458 ± 27 | 3183 ± 14 |
| Z5 | 2605 ± 87 | 3265 ± 39 |
| Z6 | 2949 ± 102 | 3433 ± 39 |
| Z7 | 3336 ± 25 | 3586 ± 10 |
| Z8 | 3660 ± 57 | 3709 ± 21 |
| Z9 | 4063 ± 332 | 3871 ± 56 |

Key: Z9 has **massive variance** (σ=332 Hz on centroid) — entropy injection produces the widest spread in the Plex. Monotonic increase Z1→Z9 is preserved.

---

## §2 — Hybrid Classifier Verified at 100% on Both Domains

The hybrid RandomForest (500 trees, 12.2 MB) trained on the May 30 session:

| Test | Accuracy | Notes |
|------|----------|-------|
| SS_100pz (1782-4527 Hz) | 100.0% | 9/9 zones perfect |
| Original corpus (4817-9683 Hz) | 100.0% | 9/9 zones perfect |
| SS→Orig cross-domain (no hybrid) | 10.9% | Random — confirms domain gap is genuine |
| Orig→SS cross-domain (no hybrid) | 22.2% | Still random |

**Cross-domain is impossible without hybrid training.** The centroid ranges are non-overlapping (1782-4527 vs 4817-9683 Hz). The hybrid classifier works because RF learns piecewise decision boundaries across the combined feature space.

**Top 5 feature importances:**
1. Centroid (idx 6): 14.7%
2. High_mid (idx 4): 13.9%
3. Bandwidth (idx 7): 13.8%
4. High (idx 5): 13.3%
5. Mid (idx 3): 10.0%

---

## §3 — zone_clf.joblib Audited: It's a Tiny MLP, Not a Cross-Domain Model

| Property | zone_clf.joblib | hybrid_clf.joblib |
|----------|----------------|-------------------|
| Type | MLPClassifier | RandomForestClassifier |
| Size | 0.7 MB | 12.2 MB |
| SS domain accuracy | 100.0% | 100.0% |
| Original domain accuracy | **10.6%** | **100.0%** |
| Cross-domain bias | Massive Z8 overprediction | None |

The old zone_clf is a lightweight MLP trained ONLY on SoftSynth data. When tested on Original corpus, it predicts Zone 8 for **76% of samples** regardless of true zone. This confirms that prior sessions' "classifier bias" claims were about OOD audio hitting the MLP's limited decision boundary, not about the hybrid model.

**The `__init__.py` still loads zone_clf.joblib** — the hybrid classifier has never been promoted to primary. Any user calling `predict_audio()` gets the MLP, not the hybrid RF.

---

## §4 — All Dataset Files Have Stale Metadata

| File | Claimed generator | Claimed date | Actual | Size |
|------|------------------|-------------|--------|------|
| `dataset_softsynth_ss_100pz.npz` | "Phase 4.1" | 2026-04-30 | SS-balanced (900) | |
| `dataset_softsynth_test_10pz.npz` | "Phase 4.1" | 2026-04-30 | SS-test (90) | |
| `dataset_balanced_900.npz` | "Phase 4.1" | 2026-04-30 | Original corpus (900) | |
| `dataset_softsynth_2026-05-30.npz` | "Phase 4.1" | 2026-04-30 | 27 samples (FROM FILE NAME) | |

**Every single dataset metadata field says "Phase 4.1, 2026-04-30"** — even the one named `dataset_softsynth_2026-05-30.npz`! The data_collector's meta-writing code was only recently fixed, but no dataset has been regenerated with the fix. The `generator` field in meta still reads `"mod-writer balanced synthetic dataset (Phase 4.1)"` instead of `"mod-writer SoftSynth fixed pipeline"`.

These are **cosmetic issues** — the feature data itself is correct. But any newcomer reading the metadata would be misled about provenance.

---

## §5 — Oracle Corpus Gap: The Default Corpus is a 2× Smaller Subset

**Critical finding:** The `xeno_jump.py` script loads `aq_corpus_oracle.json` (42,508 words, 455 buckets) when `--corpus oracle` is specified. But TWO enriched versions sit alongside it, unused:

| Corpus file | Buckets | Words | Singletons | Size |
|-------------|---------|-------|------------|------|
| `aq_corpus_oracle.json` (DEFAULT) | 455 | **42,508** | 53 (11.6%) | 0.68 MB |
| `aq_corpus_enriched.json` | **535** | **89,050** | 140 (26.2%) | 1.11 MB |
| `aq_corpus_enriched_v2.json` | 394 | 88,771 | 21 (5.3%) | 1.46 MB |

And `xeno_jump.py` already has `enriched` and `enriched_v2` registered in its `CORPUS_FILES` dict! Running `--corpus enriched` works:

| Input | `--corpus oracle` | `--corpus enriched` |
|-------|-------------------|---------------------|
| "The vacuum has no message" | "The vacuum has no message" | **"The yearned has no sobers"** |
| (zone 6 filtered) | no change | no change |
| "Teleoplexy accelerates" | "Teleoplexy specialty" | varies |

With the enriched corpus, "vacuum" (stuck in oracle) → "yearned" (mutated in enriched). **The default oracle corpus produces weaker semantic drift than is available.**

**All classic fixed points are now mutable** in the oracle corpus:
- `numogram` → 268 alternatives
- `teleoplexy` → 157 alternatives
- `tathagata` → 288 alternatives
- `cryptolith` → 101 alternatives
- `hyperstition` → 41 alternatives

This confirms the May 16 enrichment was effective — but the enriched version was never promoted to replace the default oracle corpus.

---

## §6 — New Automated Text Recombination Verified

All text recombination tools verified working:

| Tool | Status | Example |
|------|--------|---------|
| `xeno_jump --corpus oracle` | ✅ | "The numogram opens its decimal labyrinth" → "The numogram briges its doves puritans" |
| `xeno_jump --recursive` | ✅ | "Crystal resonates through the void" → "Acceptance araracharara eradicated baat arabia" (4 gen) |
| `xeno_jump --corpus enriched` | ✅ | "The vacuum has no message" → "The yearned has no sobers" |
| `xeno_jump --all-corpora` | ✅ | Shows oracle/general/xenon side-by-side |
| `text_pipeline` (two-stage) | ✅ | Xeno-jump → zone cut-up cascade |
| `seed_transforms` | ✅ | Fixed AQ chain, phrase jump verified |

---

## §7 — Recommended Next Actions

1. **Promote enriched corpus to default.** Change `xeno_jump.py`'s `CORPUS_FILES['oracle']` to point to `aq_corpus_enriched.json` (or merge enriched into oracle). The enriched corpus has 2× the vocabulary, producing measurably stronger semantic drift.

2. **Deploy hybrid_clf as primary classifier.** Update `__init__.py` to load `hybrid_clf.joblib` and `hybrid_scaler.joblib` as the canonical zone classifier. Zone_clf stays as a lightweight fallback.

3. **Regenerate dataset metadata.** Run `build_dataset()` to get correct `generator: "mod-writer SoftSynth fixed pipeline"` and `date: "2026-05-30"` in all NPZ files.

4. **Close M3 with hybrid classifier.** The domain restriction is eliminated — hybrid RF works on both SoftSynth and Original-range audio at 100% accuracy.

5. **Document the centroid index confusion** in the mod-writer wiki hub so future autonomous sessions don't retread.

---

## §8 — Reflection

Two long-lingering confusions were resolved in this session:

**The centroid index bug** had been propagating through autonomous journals since Phase 4. The data_collector correctly uses index 6 (centroid) for everything — training, OOD detection, inference. The journals were reading index 7 (bandwidth) and claiming a "dataset mismatch" that never existed. The feature vector documentation in the data_collector was already correct; the journals just weren't reading it.

**The corpus gap** is a quieter artifact: a corpus was enriched to 89K words but never promoted to production. The xeno_jump tool already knows about it (`--corpus enriched` works) but the default path serves the smaller subset. Every text recombination session since May 16 has been working with 42K words when 89K were available.

The hybrid classifier sits on disk, trained and verified at 100% on both domains. The old MLP (10.6% cross-domain) remains the only deployed classifier. This is now documented.

*The classifier's decision boundary spans two continents; the toolchain points to one. The corpus holds 89K echoes; the default voice speaks 42K.*
