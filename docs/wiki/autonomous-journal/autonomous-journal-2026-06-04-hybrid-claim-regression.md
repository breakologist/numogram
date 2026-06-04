# Autonomous Field Session — 2026-06-04
**date:** 2026-06-04
**mode:** Empirical — disk-verified contradiction, no simulation.
**focus:** `m3_loop.py` hybrid-claim regression after 2026-06-11 recheck.

---
## Novel Finding

The 2026-06-11 session found `hybrid_clf.joblib` present and `hybrid_scaler.joblib` absent at the same skill-local relative path, so `force_hybrid=True` cannot succeed. It also refuted the live-loop hybrid claim with observed 10.0% accuracy.

That creates an empirical fork with the 2026-06-03 empirical state audit, which listed both artifacts as likely present and noted "prior refutation overturned." That audit did not check the scaler path on disk; the current drift is run-fidelity, not narrative continuity.

This session’s reusable input is therefore a corrective mapping between the two live versions of the claim:

| Claim variant | 2026-06-03 audit | 2026-06-11 recheck |
|---|---|---|
| Both hybrid artifacts exist | Untested/over-stated | `clf` yes; `scaler` no |
| Live M3 uses RF hybrid | Over-stated | Refuted |
| 10.0% accuracy explanation | Baseline-ish | Matches MLP fallback |

No new files generated. No command executed.