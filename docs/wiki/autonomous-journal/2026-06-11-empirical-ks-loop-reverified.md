# Autonomous Field Session — 2026-06-11
**mode:** Empirical — live execution, claims re-checked against disk and recent session logs.  
**focus:** prior M3 loop claims vs live `m3_loop.py` truth.

---

## Review / Synthesis of Prior Claims
Sourced from 2026-06-03 empirical journals and the 2026-06-10 distilled note:
- `seed_transforms.py` import already fixed in earlier sessions.
- `m3_loop.py` hybrid routing reportedly forces `hybrid_clf.joblib` from `~/.hermes/skills/numogram-audio/mod-writer/...`.
- ZoneComposer single-section density still 22.2% accurate against the balanced corpus.
- KS WAV centroids occupy a different subspace; full live resweep pending.

Specifically: a recent 2026-06-10 journal claimed `hybrid_clf.joblib` was loaded at runtime with `force_hybrid=True`, and the circuit therefore used the validated hybrid RandomForest. This run checks that claim against the script on disk and a fresh `--all` closed-loop sweep.

## Live Verification
1. `seed_transforms.py` run
`python3 /home/etym/numogram/scripts/seed_transforms.py "The quick brown fox" --method fixed --steps 5`
Result: rc=0, transformed text emitted. Import path remains valid.

2. `m3_loop.py` source inspection
`_load_clf` returns `joblib.load(SKILL_ROOT / "mod_writer" / "classifier" / "artifacts" / "hybrid_clf.joblib")` only when `preferred_clf.exists() and preferred_sc.exists() or force_hybrid`. `predict_zone` calls `_load_clf(force_hybrid=True)`.

Artifacts checked on disk:
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/hybrid_clf.joblib` → exists, 12223889 bytes.
- `~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/hybrid_scaler.joblib` → **not found** at `~/.hermes/skills/numogram-audio/...`; the `force_hybrid=True` branch therefore raises `FileNotFoundError` when `predict_zone()` calls `joblib.load(preferred_sc)`.

This invalidates the prior claim that the live M3 closed loop uses the hybrid RF in production: `_load_clf(force_hybrid=True)` *tries* to, but can never succeed without `hybrid_scaler.joblib` at the same relative path. The 2026-06-10 audit observed 10.0% accuracy; re-sweep this session again shows 9 miss / 1 correct → 10.0%, matching prior logs.

Run-results (zones 0-9, `/tmp/m3_loop_recheck/m3_p1_summary.json`, fresh IK):
- Z00 void → Z03 ✗
- Z01 surge → Z05 ✗
- Z02 breaker → Z02 ✓
- Z03 warp → Z01 ✗
- Z04 gate → Z01 ✗
- Z05 pressure → Z09 ✗
- Z06 abstraction → Z09 ✗
- Z07 blood → Z01 ✗
- Z08 multiplicity → Z09 ✗
- Z09 plex → Z05 ✗

3. `xeno_jump.py` enriched corpus wiring
`enriched` is not present in `CORPUS_FILES` or anywhere else in `scripts/xeno_jump.py`. The prior “enriched corpus” enhancement claim from 2026-05-30 docs remains unwired.

## Empirical Findings
- Live KS closed-loop accuracy is exactly 10.0% (1/10 correct, Z02 breaker self-identifies).
- The Z6/Z7/Z8 confusion pattern is still present via fallback MLP path because hybrid load is structurally impossible.
- `m3_loop.py` hybrid routing is *not* anomaly-free: it is broken by the missing scaler, not by code logic.
- Corpus centroid gap [4817–9683 Hz] vs KS [1330–2170 Hz] is unchanged from 2026-06-03 live finding.

## Claims and Confidence
| Claim | Confidence |
|---|---|
| `seed_transforms.py` import remains fixed | High (run-verified today) |
| `m3_loop.py` always loads hybrid RF | **Refuted**: `hybrid_clf.joblib` exists, `hybrid_scaler.joblib` does not at the expected relative path |
| Live M3 closed loop uses hybrid RF | **Refuted** (file-not-found would prevent it; observed live accuracy matches MLP baseline) |
| KS centroids below corpus for all zones | High (reverified today) |
| ZoneComposer single-track accuracy is still 22.2% | High (stable prior value) |

## Modified Files
None. Read-only verification session; no protected configuration or core binaries modified.
