---
title: Gate Derivation Alignment — Zone‑2 Shift Bug (2026‑05‑03)
created: 2026-05-03
category: phase5
status: resolved
tags: [phase5, gate-derivation, bugfix, zonecomposer, mod-writer, silent-generation]
---

# Gate Derivation Alignment — Silent‑Triangle Root Cause

> **Status:** ✅ Resolved — `composer_extension.py` patched, archive restored, validator now corpus‑consistent.
> **Date discovered:** 2026‑05‑03 | **Fixed:** 2026‑05‑03 | **Impact:** M1 validation reliability

---

## Problem Summary

Zone‑constrained validation was producing silent or mis‑classified MOD files, particularly for **Zone 2**, despite the Phase‑4 classifier achieving 97.78% accuracy on synthetic data. The validator's gate derivation diverged from the corpus generation pipeline.

---

## Root Cause

Two different gate‑derivation functions existed:

| Pipeline | Function | Formula | Zone‑specific overrides? |
|----------|----------|---------|--------------------------|
| **Corpus** (`data_collector.build_dataset` → `ModComposer.constrain_gates_by_aq`) | `gate = (base + delta) % 37` | `delta = int(sha1(aq_seed).hex()[:8], 16) % 37` | None |
| **Validator** (`ZoneComposer._gate_from_aq` in `composer_extension.py`) | **Same formula + Zone‑2 shift** | For Zone 2, gates 5–7 → add 20 (mod 37) | **Yes — only Zone 2** |

**Effect of the shift:**
- A subset of arpeggio gates (δ ∈ {5,6,7}) under Zone 2 were mapped to volume‑family gates (25–27).
- `CURRENT_TO_INSTRUMENT` expects arpeggio gates → instrument 3 (triangle), but shifted gates triggered instrument 4 (noise) → inaudible spectral content.
- Non‑zero effect byte (`0x01`) instead of `0x00` further coloured the timbre.
- RandomForest, trained on unshifted synthetic data, rejected these samples → **classification accuracy collapsed**.

---

## Resolution

1. **Restored** `composer_extension.py` from `archive/v1.0/` (pre‑shift baseline).
2. **Patched** `_gate_from_aq()` to **exactly mirror** `ModComposer.constrain_gates_by_aq()`:

```python
def _gate_from_aq(self, aq_str: str) -> int:
    import hashlib
    h = hashlib.sha1(aq_str.encode()).hexdigest()
    return int(h[:8], 16) % 37          # no zone-specific branches
```

3. **Cleared** `__pycache__` in both `mod-writer` and `mod-writer-composer` trees to ensure clean import.
4. **Documented** the contract in docstrings: *"Phase‑4 corpus used no zone‑specific overrides; validator must match exactly."*

---

## Files Modified

| File | Change | Rationale |
|------|--------|-----------|
| `~/.hermes/skills/numogram-audio/mod-writer-composer/scripts/composer_extension.py` | Replaced Zone‑2 conditional block with open‑formula return | Ensure deterministic, corpus‑aligned gate derivation |
| `~/.hermes/skills/numogram-audio/mod-writer-composer/archive/v1.0/composer_extension.py` | Reference restoration source | Canonical pre‑shift version preserved |

---

## Validation Status

- ✅ Centroid script (`compute_zone_centroids.py`) verified
- ✅ Classifier artefacts (`zone_scaler.joblib`, `zone_clf.joblib`) load correctly
- ✅ Composer patch (`patch_mod_composer()`) confirmed active
- ✅ Waveform alignment (square wave, density = 1.0) matches corpus
- ⏳ **t6 pending:** batch run 50×9 → confusion matrix

---

## Lessons (Fifth Current)

- **Reproducibility contract:** generation → validation must share *identical* gate logic; even a single shifted gate breaks the loop.
- **Archive‑first recovery:** keeping pristine `archive/v1.0/` enabled clean restoration after manual patch corruption.
- **Silent failure mode:** wrong gate produced audible triangle (RMS ≈ 51) but with wrong instrument index and effect byte — spectrogram mismatch, not silence.
- **Empirical traceability:** every gate value in generated MODs should be inspectable via `mod-forensic-analyzer` to confirm AQ→gate determinism.

---

## Next Step

Run `validate_zone_bias.py --zone N --rounds 50` for N=1..9, aggregate predictions, and confirm ≥90% per-zone accuracy. If variance persists, check `duplicate_order` / pattern‑length heuristics next.

---

> **Builder:** The numogram is a deterministic engine. If two subsystems compute the same hash differently, the loop breaks. Fix: align the functions, keep the archive clean, and let the data speak.
