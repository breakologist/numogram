# Autonomous Field Session — 2026-06-02T12:33Z
date: 2026-06-02T12:33Z
session: autonomous-cron
duration_min: ~30
tags: [empirical-verification, classifier-hybrid-load, xeno-jump-reality-check, unverified-claims-corrected]
verifies:
  - hybrid_clf.joblib loads as RandomForest (12.2 MB) with hybrid_scaler.joblib as first-priority model in classifier/__init__.py
  - zone_clf.joblib is 0.7 MB MLP fallback
  - predict_audio() runs without error on a real rendered MOD→WAV (Z1), returns OOD=false for centroid 2504.1 Hz
  - xeno_jump.py does NOT have 'enriched' corpus registered in CORPUS_FILES — claim from 2026-05-30 entry appears simulation-only
  - Mod generation and ffmpeg conversion both succeeded

## Review — Prior Journal Findings (2026-05-30)
Today’s session revisited two key 2026-05-30 claims and validated them against the live filesystem:

1. **Centroid index confusion**
   - 2026-05-30 journal: “misread feature index 7 (bandwidth) as centroid; fixed by clarifying index 6.”
   - __init__.py’s predict_audio() now has a multi-line comment explicitly calling this out (lines 117–124).
   - This appears to have been **corrected in code**, not just documented. No further retread needed.

2. **Hybrid classifier as primary**
   - 2026-05-30 journal: 
     - Hybrid RF verified at 100% on both domains.
     - zone_clf.joblib is MLP, only 10.6% on original corpus.
     - “old zone_clf is still loaded” claim.
   - Live check: `_HYBRID_CLF_PATH` exists (12.2 MB), hybrid_scaler exists, `_load_zone_classifier()` prioritizes hybrid first with fallback comment. Predict_audio loaded RandomForestClassifier and StandardScaler.
   - Field test on a rendered `Z1.mod -> Z1.wav` returned `zone=1, ood=false, centroid=2504.1 Hz`.
   - Conclusion: the claim is **verified** — the hybrid classifier is now the effective primary in production code paths. No more need for MLP workaround.

3. **Stale metadata | non-overlapping domains | Z9 variance | other claims**
   - Cannot be confirmed without live npz load/regeneration — deferred to next session (dataset audit branch).

## Explore — Xeno-Jump Reality Check
The 2026-05-30 journal stated the `xeno_jump.py` already had `enriched` and `enriched_v2` registered in its `CORPUS_FILES` dict, and that `--corpus enriched` produces stronger semantic drift. **This is NOT how the live code behaves.**

Live execution:
- `python xeno_jump.py "The vacuum has no message" --mode all --corpus oracle` returned: `Sie valerie bake chi morals`
- The exact May 30 example from the dead-features-fixed-xeno-jump-falsification (2026-05-30 hybrid clf session entry) claimed “The vacuum has no message” → “The yearned has no sobers” with enriched — but `enriched` isn’t in CORPUS_FILES → the script errors: `Corpus 'enriched' not found at None`
- The `2026-05-24-text-recombination-executed.md` example output `"The numogram opens its decimal labyrinth" → "The numogram briges its doves puritans"` was reproduced, suggesting oracle-driven mutation is still functional.

**Root cause:** A corpus file (`aq_corpus_enriched.json`) exists in `/home/etym/numogram/scripts/` alongside `aq_corpus_oracle.json` (and `aq_corpus_enriched` is larger at 1.1 MB vs oracle’s 0.7 MB), but the `CORPUS_FILES` dict only maps `general`, `oracle`, `xenon` to file paths. The May 30 entry’s “the enriched version is already usable” claim was likely **referencing a branch or test copy, not the canonical xeno_jump.py in `/home/etym/numogram/scripts/`.** This is a simulated/hallucinated artifact from a prior session. The corpus gap remains unaddressed in canonical code.

Other verified text recombination tools in the same directory:
- `text_pipeline.py` (present but deprecated)
- `seed_transforms.py` (present)
- `cut_up.py` (present)

## Reflect — Simulated vs Empirical Classification
The May 30 evidence roundup had a strong empirical section (hybrid classifier 100%, real filesystem verification) but also a text recombination section that seems to have copied/cloaked prior session claims without executing them today. The lesson for this session is:

- **An autonomous session that synthesizes prior empirical results without re-running failed to imagine the inconsistency (enrichment corpus reference), wasting a slot.**
- **The hybrid classifier IS now physics: it loads first, it predicts real audio, OOD gates on centroid=2504.1 Hz are working.**
- **The enriched corpus recommendation remains: new artifact but not wired into canonical CLI.**

This is consistent with the “prefer real tool execution over symbolic simulation” mandate: prior sessions overpraised an unreached endpoint. Today’s rerun promoted simulation → reality.

## Modify — No Protected Changes
No code patches required in this session; artifacts/literature already reflect hybrid-clf priority. The enriched-corpus wiring is a non-critical suggestion and needs human review before committing to canonical xeno_jump behavior.

## Publish
Journal entry written at ~/autonomous-journal/autonomous-journal-2026-06-02-empirical-clf-hybrid-verified-md.md.

## Inventory — What’s Verified vs Unverified
| Claim (2026-05-30) | Verified? |
|--------------------|-----------|
| Hybrid RF loads first in classifier/__init__.py | ✅ Yes — field test used RF, not MLP |
| zone_clf.joblib is a 0.7 MB MLP counterpart | ✅ Yes |
| xeno_jump --corpus enriched is wired in | ❌ No — script only knows general/oracle/xenon |
| Stale metadata in all .npz | ❌ Unverified this session (no dataset load) |
| Z9 spectral centroid variance σ=332 Hz | ❌ Unverified this session |

Recommended next run: a) dataset metadata/centroid head-to-head with real npz load; b) enriched corpus wiring in xeno_jump to validate improved semantic drift.