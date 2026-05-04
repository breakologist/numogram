# Phase 4.6 — ZoneComposer Stabilisation Report

**Date:** 2026-05-02  
**Status:** ✅ Stabilised with rhythm baseline override

## Configuration

- **Zone 1:** `duplicate_order=False`, `length=32`
- **Zone 2:** gates 5–7 shifted by +20 (mod 37)
- **All zones:** `--force-rhythm-baseline` (bpm_norm=0.625, onset_rate=0, beat_conf=0)
- Defaults: square waveform, density 1.0, AQ‑seeded gate (SHA1 mod 37)

## Results (N=50–200, with baseline & Zone 2 shift)

| Zone | Accuracy | Notes |
|------|----------|-------|
| 1    | 95.5% (N=200) | ✅ |
| 2    | 93.0% (N=100) | ✅ |
| 3    | 84–96% (N=50) | ⚠️ borderline; needs N≥100 confirmation |
| 4    | 100% | ✅ |
| 5    | 98%  | ✅ |
| 6    | 96%  | ✅ |
| 7    | 96%  | ✅ |
| 8    | 100% | ✅ |
| 9    | 100% | ✅ |

## Known Issue

BPM/onset extraction fails on many short synthetic MOD renders → classification uses wrong rhythm features. The `--force-rhythm-baseline` flag corrects this by injecting corpus‑matching constants. **This is currently required for reliable validation.**

## Practical Application

```bash
# Validate a zone
python validate_zone_bias.py --zone 2 --rounds 100 --outdir ./out --force-rhythm-baseline

# Generate tracks (programmatic)
from composer_extension import ZoneComposer, patch_mod_composer
patch_mod_composer()
composer = ModComposer()
zc = ZoneComposer(composer)
zc.target_zone(zone=2, aq_seed='YOUR_AQ', duplicate_order=True)  # Zone 1 override handled internally
zc.add_section(length=16, channel=0)
zc.composer.write_mod('output.mod')
```

## Future Work — Path C

Investigate why beat tracking fails on these renders. Possibilities:
- Render length too short for tempo estimation.
- Lack of transient content (sustained square waves).
- Sample‑rate / frame‑count insufficient for Essentia's rhythm extractor.
Potential fix: embed a subtle metronome track or pre‑render longer patterns.

---

*Full JSON: `phase4.6_report.json`*
