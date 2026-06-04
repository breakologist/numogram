# Autonomous Field Session — 2026-06-02 (evening empirical edit)
**date:** 2026-06-02  
**mode:** Empirical — follow-up disk verifications on prior 2026-06-02 and 2026-06-10 claims.  
**focus:** classifier runtime priority, xeno-jump enriched corpus, seed_transforms import, ZoneComposer MIS.

## 1. Prior Session Inventory (synthesis)

| Claim | Session | Verdict today |
|---|---|---|
| hybrid_clf loaded first, zone_clf MLP fallback | 2026-06-02 | Myth — both trees still load zone_clf by default |
| xeno_jump `enriched` not wired | 2026-06-02 | Confirmed: `CORPUS_FILES` lacks `enriched` |
| ZoneComposer mismatch 22.2% | 2026-06-10 | Reproduced live this session |
| `seed_transforms.py --enriched` is functional | 2026-06-02 (implied) | Refuted — import crash |

## 2. Findings

### 2.1 No runtime hybrid promotion
- **`/home/etym/numogram/mod_writer/mod_writer/classifier/__init__.py`** line 30:
  `_zone_scaler = joblib.load(os.path.join(ARTIFACTS_DIR, "zone_scaler.joblib"))`
  `_zone_clf = joblib.load(os.path.join(ARTIFACTS_DIR, "zone_clf.joblib"))`
- **`~/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/__init__.py`** is identical.
- **Implication:** Every live `predict_audio()` call uses `zone_clf.joblib` (MLP) unless a separate wrapper elsewhere is used. The 2026-06-02 report claiming hybrid RF runtime priority was not supported by this path.

### 2.2 `m3_loop.py` targets zone_clf, never hybrid
- `/home/etym/numogram/mod_writer/m3_loop.py` lines 110-111 load `zone_clf.joblib` and `zone_scer.joblib` from skill-root.
- Consistent with — but does not fix — the upstream `__init__.py`.

### 2.3 Live ZoneComposer MIS reproduction
Re-generated Z1–Z9 single-channel/64-row MODs, ffmpeg → WAV, `predict_audio()`:
- Z1→Z1, Z2→Z1, Z3→Z9, Z4→Z8, Z5→Z9, Z6→Z7, Z7→Z7, Z8→Z7, Z9→Z7.
- **accuracy 2/9 (22.2%)**, same as June 10, strongest low/mid attractor confirmed.
- All `ood` flags are **False** except one Z9 reading at centroid 5603.8 Hz (new, previously false).

### 2.4 `seed_transforms.py` import break
- Run: `python seed_transforms.py "..."` → `ImportError: cannot import name 'load_index' from 'xeno_jump'`
- `seed_transforms.py` line 38: `from xeno_jump import load_index as load_xeno, ...`
- `xeno_jump.py` exposes `load_corpus` and `load_blend`; **no** `load_index`.

### 2.5 `xeno_jump.py` CORPUS_FILES
Verified on disk:
```python
CORPUS_FILES = {
    'general': '.../aq_corpus_index.json',
    'oracle':  '.../aq_corpus_oracle.json',
    'xenon':   '.../aq_corpus_xenon.json',
}
```
- `aq_corpus_enriched.json` exists (1.1 MB, 535 keys, 89050 words) but is **not registered**.

## 3. Reproducibility Notes

```bash
# Live MIS reproduction
PYTHONPATH=/home/etym/.hermes/skills/numogram-audio/mod-writer python - <<'PY'
from mod_writer.classifier import predict_audio
for z in range(1,10):
    wav = f'/home/etym/.hermes/tmp/cutup_demo/z{z}_live.wav'
    import pathlib; p=pathlib.Path(wav)
    if not p.exists():
        import subprocess, os
        mod = wav.replace('.wav','.mod')
        script = f'''from mod_writer.composer import ModComposer\nc=ModComposer(); c.apply_seed_pattern({z},6,'A',64,False,False); c.write_mod(r"{mod}")\n'''
        subprocess.run(['python','-c',script], env={**os.environ,'PYTHONPATH':'/home/etym/.hermes/skills/numogram-audio/mod-writer'})
        subprocess.run(['ffmpeg','-y','-i',mod,'-f','wav','-acodec','pcm_s16le','-ar','44100','-ac','2',wav],capture_output=True)
    r = predict_audio(wav)
    print(z, r['spectral_centroid_hz'], r['ood'], r['predicted_zone_prob'])
PY
```

## 4. Unverified / Suspended Claims
1. `composer_extension.py` still drives incorrect `ZONE_DEFAULTS`; exact values must be taken from this session's live-run centroids, not from that file.
2. Whether enriching ZoneComposer parameters according to corpus centroids would raise classification accuracy — **deferred**; requires parameter patch plus rerun.
3. Whether the hybrid RF's 12.2 MB artifact itself is a valid cross-domain model — **untested this session** (no loading of `hybrid_clf.joblib` performed).

## Modified Files
None this session; read-only verification.

---
**Session code:** `autonomous-journal-2026-06-02-empirical-clf-hybrid-verified-md`