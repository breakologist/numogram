---
date: 2026-06-04T12:33:12Z
session: autonomous-cron
mode: drift-first
static: true
focus: m3_loop hybrid pathpair stub
summary: |
  Tightened empirical baseline on `m3_loop.py`'s hybrid routing.
  Artifact inventory for hybrid pair is now pinned to the skill-local
  artifacts_dir; immediate script path is a stub because
  `predict_zone()` always forces `force_hybrid=True`.
---

## 1. Artifact inventory

| Artifact | Size | Path |
|----------|------|------|
| `hybrid_clf.joblib` | 12,223,889 B | `/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/hybrid_clf.joblib` |
| `hybrid_scaler.joblib` | 1,263 B | `/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts/hybrid_scaler.joblib` |
| `zone_clf.joblib` | 6,773,643 B | same artifacts_dir |
| `zone_scaler.joblib` | 1,263 B | same artifacts_dir |

## 2. Script path status

`m3_loop.py` `/home/etym/numogram/mod_writer/m3_loop.py` line 154 calls

```
clf, scaler = _load_clf(force_hybrid=True)
```

Because `force_hybrid=True` is hardcoded in `predict_zone()`, there is
no current execution path from `m3_loop.run_zone()` to the
`zone_clf.joblib` branch except by removing the flag.

## 3. Reproduce

```bash
cd /home/etym/numogram/mod_writer && python3 - <<'PY'
from pathlib import Path
from m3_loop import _load_clf
print('default _load_clf():', type(_load_clf()[0]).__name__)
print('forced hybrid:     ', type(_load_clf(force_hybrid=True)[0]).__name__)
PY
```

## 4. Stop condition

Baseline ready. Next empirical step is either a live M3 re-run with
this flag flipped off, or a separate runner that bypasses `predict_zone`
and sends WAVs through a direct `_flatten + clf.predict` path. Either
requires time budget for execution, not static inspection.
