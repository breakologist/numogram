---
title: Zone‑Constrained Composition — Run 1 Validation Results
created: 2026-05-02
category: phase5-results
status: stub
tags: [phase5, zone-constrain-compose, validation, closed-loop]
---

# Phase 5 M1 — Zone‑Constrained Composition Validation (Run 1)

> **Status:** Stub — awaiting first batch generation  
> **Generated:** TBD  
> **Classifier model:** `mod-writer-classifier` v0.7.0  
> **Centroid source:** `zone_centroids.json` (synthetic 900‑track corpus)

---

## Summary

| Metric | Value |
|--------|-------|
| Tracks generated (per zone) | 50 |
| Total tracks | 450 |
| Mean classifier accuracy | TBD |
| Success threshold | ≥90% |
| Zones meeting threshold | TBD |

---

## Confusion Matrix

```json
{
  "zones": [1,2,3,4,5,6,7,8,9],
  "predicted": "TBD — populated by `p5-zone-constrain-compose --report`"
}
```

*Link:* `[[phase5-results/run-1-confusion-matrix.json]]` (committed to `~/numogram/data/phase5/`)

---

## Failure Cases

For tracks that mis‑classify, we archive:
- `.mod` file
- MIR feature vector
- Classifier probability distribution
- SHAP top‑5 features (once M7 integrated)

*Directory:* `~/.hermes/numogram/phase5/failures/zone_{N}_seed_{S}/`

---

## Next Actions

- [ ] Compute `zone_centroids.json`
- [ ] Run first batch: `hermes p5-zone-constrain-compose --all-zones --attempts-per-zone 50 --report confusion.json`
- [ ] Populate this page with results matrix and analysis
- [ ] Link from `phase5-status-2026-05-02.md` once complete

---

**Oracle:** This page is the *receipt* — where hyperstition meets audit. Empty now, soon it will be the ledger of our successes and our lesson‑seeds.
