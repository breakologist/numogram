#!/usr/bin/env python3
import sys, os, types, joblib, subprocess, json, shutil
from pathlib import Path
import numpy as np

sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer/scripts')

from mod_writer.composer import ModComposer
from composer_extension import ZoneComposer, patch_mod_composer
from mod_writer.mir_profiler import MIRFeatureExtractor

patch_mod_composer()
extractor = MIRFeatureExtractor()

ARTIFACTS = '/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts'
scaler = joblib.load(os.path.join(ARTIFACTS, 'zone_scaler.joblib'))
clf = joblib.load(os.path.join(ARTIFACTS, 'zone_clf.joblib'))

KEY_MAP = {k: i for i, k in enumerate(['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'])}
def _flatten_features(features):
    low = features.get('lowlevel', {})
    vec = []
    for band in ['sub_bass','bass','low_mid','mid','high_mid','high']:
        vec.append(low.get(band, 0.0))
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

RHYTHM_BASELINE = {'onset_rate_norm': 0.0, 'bpm_norm': 0.625, 'beat_conf_norm': 0.0}
def predict_zone(feats, baseline=False):
    vec = _flatten_features(feats).reshape(1, -1)
    if baseline:
        vec[0, 10:13] = [0.0, 0.625, 0.0]
    return int(clf.predict(scaler.transform(vec))[0])

tmpdir = Path('/tmp/zone_mir_snapshot')
if tmpdir.exists():
    shutil.rmtree(tmpdir)
tmpdir.mkdir()

snapshot = []
for zone in range(1, 10):
    composer = ModComposer(title=f"Z{zone}_snapshot")
    zc = ZoneComposer(composer)
    dup = False if zone == 1 else True
    length = 32 if zone == 1 else 16
    zc.target_zone(zone=zone, aq_seed=str(zone), duplicate_order=dup)
    zc.add_section(length=length, channel=0)
    gate = zc._gate_from_aq(str(zone))

    mod_path = tmpdir / f'z{zone}.mod'
    composer.write_mod(str(mod_path))
    wav_path = tmpdir / f'z{zone}.wav'
    subprocess.run(['ffmpeg','-y','-i',str(mod_path),'-f','wav',str(wav_path)],
                  capture_output=True, timeout=15)

    feats = extractor.extract(str(wav_path), use_all=False)
    mid = feats['midlevel']
    low = feats['lowlevel']
    pred_nb = predict_zone(feats, baseline=False)
    pred_b  = predict_zone(feats, baseline=True)

    snapshot.append({
        'zone': zone, 'aq': zone, 'gate': gate,
        'bpm': mid.get('bpm'), 'onset_rate': mid.get('onset_rate'),
        'beat_conf': mid.get('beat_confidence'),
        'spectral_centroid_hz': low.get('spectral_centroid_hz'),
        'sub_bass': low.get('sub_bass'),
        'pred_no_base': pred_nb, 'pred_base': pred_b
    })

# Print table
print(f"{'Z':>2} | {'Gate':>4} | {'BPM':>6} | {'Onset':>6} | {'Centroid':>7} | {'NoBase':>6} | {'Base':>5}")
print("-" * 61)
for rec in snapshot:
    bpm = rec['bpm'] if rec['bpm'] else 0
    onset = rec['onset_rate'] if rec['onset_rate'] else 0
    cent = rec['spectral_centroid_hz'] if rec['spectral_centroid_hz'] else 0
    print(f"{rec['zone']:>2} | {rec['gate']:>4} | {bpm:>6.1f} | {onset:>6.1f} | {cent:>7.0f} | Z{rec['pred_no_base']:<5} | Z{rec['pred_base']}")

# Save
out = Path('/home/etym/.hermes/obsidian/hermetic/wiki/phase4.6_zone_mir_snapshot.json')
out.write_text(json.dumps(snapshot, indent=2))
print(f"\nSaved: {out}")
