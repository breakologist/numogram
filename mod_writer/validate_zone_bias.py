#!/usr/bin/env python3
"""
Validate zone‑bias: generate N mini‑patterns per target zone, classify via the
Phase 4 zone classifier, and report pass rate. Expected: ≥90% classified as
target zone.

This version uses corpus‑aligned parameters:
  - square waveform (current='A')
  - full density = 1.0 (every row has a note)
  - single gate per track derived from an AQ seed (SHA1‑mod‑37)
  - 16 rows per section (matching synthetic dataset)

Diagnostic:
  --force-rhythm-baseline  Override extracted rhythm features (onset_rate, bpm,
                           beat_confidence) with the corpus baseline values
                           (onset_rate=0, bpm_norm=0.625, beat_conf=0). This
                           isolates gate/waveform effects from audio‑extraction
                           failures in synthetic MOD renders.
"""
import argparse, os, sys, tempfile, joblib, random
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/audio-renderer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer')

from mod_writer.song import SongBuilder
from renderer import render_mod_to_wav
from mod_writer.mir_profiler import MIRFeatureExtractor
from mod_writer.classifier.data_collector import _aq_candidates_for_zone
import numpy as np

# ── Zone classifier artefacts ────────────────────────────────────────────────
ARTIFACTS_DIR = (
    '/home/etym/.hermes/skills/numogram-audio/mod-writer/'
    'mod_writer/classifier/artifacts'
)
ZONE_SCALER = joblib.load(os.path.join(ARTIFACTS_DIR, 'zone_scaler.joblib'))
ZONE_CLF   = joblib.load(os.path.join(ARTIFACTS_DIR, 'zone_clf.joblib'))

# Global override: set by main() when --force-rhythm-baseline is passed
FORCE_RHYTHM_BASELINE = False

# Corpus baseline constants (already normalised to classifier scale)
RHYTHM_BASELINE = {
    'onset_rate_norm': 0.0,    # onset_rate / 200
    'bpm_norm':       0.625,   # 125 BPM / 200  (corpus median across all zones)
    'beat_conf_norm': 0.0,     # beat_confidence / 100
}

def classify_track(mod_path: str) -> int | None:
    """Render a .mod file, extract MIR features, predict zone using Phase 4 zone classifier."""
    try:
        with tempfile.TemporaryDirectory() as tmp:
            wav_path = os.path.join(tmp, 'tmp.wav')
            render_mod_to_wav(mod_path, wav_path)
            feas = MIRFeatureExtractor().extract(wav_path, use_all=False)
            vec = _flatten_features(feas).reshape(1, -1)

            # ── Diagnostic override: force corpus‑matching rhythm features ──────
            if FORCE_RHYTHM_BASELINE:
                # indices from _flatten_features ordering:
                # 10: onset_rate_norm, 11: bpm_norm, 12: beat_conf_norm
                vec[0, 10] = RHYTHM_BASELINE['onset_rate_norm']
                vec[0, 11] = RHYTHM_BASELINE['bpm_norm']
                vec[0, 12] = RHYTHM_BASELINE['beat_conf_norm']

            vec_scaled = ZONE_SCALER.transform(vec)
            zone_pred = ZONE_CLF.predict(vec_scaled)[0]
            return int(zone_pred)
    except Exception as e:
        print(f"[error] classify_track({mod_path}): {e}", file=sys.stderr)
        return None

def _flatten_features(features: dict) -> np.ndarray:
    """Extract 29‑dim feature vector (same as data_collector._flatten_features)."""
    KEY_MAP = {k: i for i, k in enumerate(
        ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    )}
    vec = []
    low = features.get('lowlevel', {})
    for band_name in ['sub_bass','bass','low_mid','mid','high_mid','high']:
        vec.append(low.get(band_name, 0.0))
    vec.append(low.get('spectral_centroid_hz', 0.0) or 0.0)
    vec.append(low.get('spectral_bandwidth_hz', 0.0) or 0.0)
    vec.append(low.get('spectral_rolloff', 0.0) or 0.0)
    vec.append(low.get('dynamic_complexity', 0.0) or 0.0)
    mid = features.get('midlevel', {})
    vec.append((mid.get('onset_rate') or 0.0) / 200.0)
    vec.append((mid.get('bpm') or 0.0) / 200.0)
    vec.append((mid.get('beat_confidence', 0.0) or 0.0) / 100.0)
    key_str = mid.get('key', '')
    key_idx = KEY_MAP.get(key_str, 0)
    key_onehot = [0]*12; key_onehot[key_idx] = 1
    vec.extend(key_onehot)
    scale = mid.get('scale', 'major')
    scale_onehot = [1,0,0] if scale=='major' else ([0,1,0] if scale=='minor' else [0,0,1])
    vec.extend(scale_onehot)
    meta = features.get('metadata', {})
    dur = meta.get('duration_s', 0.0)
    vec.append(dur / 120.0)
    return np.array(vec, dtype=np.float32)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--zone', type=int, required=True, help='Target zone (1-9)')
    parser.add_argument('--rounds', type=int, default=50)
    parser.add_argument('--length', type=int, default=16)
    parser.add_argument('--outdir', default='/tmp/zone_bias_validation')
    parser.add_argument('--force-rhythm-baseline', action='store_true',
                        help='Override extracted rhythm features with corpus baseline')
    parser.add_argument('--save-details', action='store_true',
                        help='Save per-track prediction details to JSON in outdir')
    args = parser.parse_args()

    # Set global override used by classify_track()
    global FORCE_RHYTHM_BASELINE
    FORCE_RHYTHM_BASELINE = args.force_rhythm_baseline

    os.makedirs(args.outdir, exist_ok=True)

    # Build a deterministic list of AQ candidates for this zone
    aq_candidates = list(_aq_candidates_for_zone(args.zone, count=args.rounds, start_k=0))

    # Monkey‑patch to use ModComposer with ZoneComposer
    from composer_extension import patch_mod_composer
    patch_mod_composer()
    from mod_writer.composer import ModComposer

    hits = 0
    details = []
    for i in range(args.rounds):
        composer = ModComposer(title=f"Z{args.zone}_v{i}")
        aq = aq_candidates[i]
        # Determine length: Zone 1 uses contiguous 32‑row pattern; others use 16‑row with duplication
        section_length = 32 if args.zone == 1 else args.length
        # duplicate_order: Zone 1 must be False; others keep corpus‑aligned duplication
        dup_flag = False if args.zone == 1 else True
        composer.target_zone(
            zone=args.zone,
            aq_seed=str(aq),        # deterministic single gate derived from AQ
            duplicate_order=dup_flag
        )
        composer.add_section(length=section_length, channel=0)
        mod_path = os.path.join(args.outdir, f"z{args.zone}_{i:03d}.mod")
        composer.write_mod(mod_path)

        pred = classify_track(mod_path)
        ok = (pred == args.zone)
        hits += int(ok)
        details.append({"idx": i, "file": mod_path, "aq": aq, "pred": pred, "ok": ok})

    rate = hits / args.rounds
    print(f"Target zone: {args.zone}  →  Hit rate: {hits}/{args.rounds} = {rate:.1%}")

    if args.save_details:
        import json
        out_json = os.path.join(args.outdir, f"zone{args.zone}_details.json")
        with open(out_json, 'w') as jf:
            json.dump({'zone': args.zone, 'rounds': args.rounds, 'hits': hits, 'rate': rate, 'tracks': details}, jf, indent=2)
        print(f"[details saved to {out_json}]")
    if rate < 0.9:
        print("⚠  Below 90% threshold — further tuning may be required")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())

