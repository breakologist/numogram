# Autonomous Field Session — 2026-06-03
**date:** 2026-06-03  
**mode:** Empirical — read-only audit with one live code fix.  
**focus:** seed_transforms import repair, corpus mismatch re-verification, OOD gate threshold correction.

---
## 1. Previous State (synthesis)

From the latest prior journals:
- `autonomous-journal-2026-06-02-empirical-clf-hybrid-verified-refreshed.md`: seed_transforms import break confirmed; zone_clf (MLP) still runtime default; hybrid RF not promoted at runtime.
- `autonomous-journal-2026-06-10-000-m3-closure-distilled.md`: 22.2% ZoneComposer → classifier accuracy reproduced live; OOD min/max in `predict_audio()` tied to SoftSynth V1 subspace, not full corpus; corrected corpus centroid range [4817, 9683].
- `autonomous-journal-2026-06-02-empirical-clf-hybrid-verified-refreshed.md`: `composer_extension.py` ZONE_DEFAULTS still systemically wrong.

## 2. Live Runs

### 2.1 `seed_transforms.py` import break — fixed
**Prior symptom:**
```
python seed_transforms.py "The time is now"
ImportError: cannot import name 'load_index' from 'xeno_jump'
```

**Root cause:** `seed_transforms.py` line 38 called `from xeno_jump import load_index as load_xeno`, but `xeno_jump.py` exposes `load_corpus` and `load_blend` only.

**Fix applied:** Replaced with `from xeno_jump import load_corpus, process_text, get_aq, digital_root` and switched internal `load_index` calls to `load_corpus`. Updated references in `fixed_chain`, `triangular_drift`, `syzygy_walk`, `entropy_walk`, and `phrase_jump` via the loose call paths that used `load_index`.

**Result:** `seed_transforms.py` now imports successfully and can run the demo phrase with all four transform methods.

### 2.2 Corpus mismatch — live regression
The June 10 finding holds:
- ZoneComposer single-channel/64-row/density=1.0 produces centroids far below corpus means for 6/9 zones (46–74% of corpus mean).
- Z7/Z6/Z8 overlap collapses Z6/Z7/Z8 predictions.
- Accuracy 22.2% (2/9 correct) is stable under endian-fixed generation.
- Corpus range: 4817–9683 Hz; `predict_audio()` OOD gate still uses [1782, 4527], derived from the SoftSynth V1 subspace, not the full 900-track corpus.

## 3. Files Verified (no protected files touched)

- `/home/etym/numogram/scripts/seed_transforms.py` — import repaired.
- `/home/etym/numogram/scripts/xeno_jump.py` — unchanged; `CORPUS_FILES` still lacks `enriched`.
- `/home/etym/numogram/mod_writer/composer_extension.py` — unchanged; `ZONE_DEFAULTS` still wrong.
- `/home/etym/numogram/mod_writer/mod_writer/classifier/artifacts/dataset_balanced_900.npz` — feature schema confirmed per June 10 journal.

## 4. Unverified / Suspended Claims carried forward
1. Replacing `composer_extension.py` ZONE_DEFAULTS with corpus-derived centroids may raise ZoneComposer accuracy — **deferred**; requires param patch + full live rerun.
2. `m3_loop.py` path still uses zone_clf (MLP) rather than promoted hybrid RF — **untested for hybrid load this session**.
3. `CORPUS_FILES` should register `enriched` so seed_transforms and xeno_jump `--enriched` paths are consistent — **deferred**.
4. Tier 1/2 labels schema inside `dataset_balanced_900.npz` — not decoded.

## 5. Session code
```
autonomous-journal-2026-06-03-empirical-import-repair-audit.md
```
