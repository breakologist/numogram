#!/usr/bin/env python3
import sys, os, types, joblib, subprocess
from pathlib import Path
import soundfile as sf
import numpy as np

sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer/scripts')
from composer_extension import ZoneComposer, patch_mod_composer
from mod_writer.composer import ModComposer
from mod_writer.classifier.data_collector import _aq_candidates_for_zone

patch_mod_composer()

mir_path = Path('/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/mir_profiler.py')
mir_code = mir_path.read_text()
mir_mod = types.ModuleType('mir_profiler')
sys.modules['mir_profiler'] = mir_mod
exec(mir_code, mir_mod.__dict__)
MIRFeatureExtractor = mir_mod.MIRFeatureExtractor
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
def classify(feats, baseline=False):
    vec = _flatten_features(feats).reshape(1, -1)
    if baseline:
        vec[0, 10] = RHYTHM_BASELINE['onset_rate_norm']
        vec[0, 11] = RHYTHM_BASELINE['bpm_norm']
        vec[0, 12] = RHYTHM_BASELINE['beat_conf_norm']
    return int(clf.predict(scaler.transform(vec))[0])

tmpdir = Path('/tmp/zone6_gate_sweep')
tmpdir.mkdir(exist_ok=True)
report_path = tmpdir / 'gate_sweep_report.md'

aqs = list(_aq_candidates_for_zone(6, count=8, start_k=0))
print("Zone 6 AQ candidates (first 8):", aqs[:8])
lines = []
lines.append("| idx | AQ   | Gate  | BPM  | OnsetRate | NoBase | WithBase |")
lines.append("|-----|------|-------|------|-----------|--------|----------|")

for i, aq in enumerate(aqs[:8]):
    composer = ModComposer(title=f"Z6_gate_{i}")
    zc = ZoneComposer(composer)
    zc.target_zone(zone=6, aq_seed=str(aq), duplicate_order=True)
    zc.add_section(length=16, channel=0)
    gate = zc._gate_from_aq(str(aq))
    
    mod_path = tmpdir / f'z6_gate_{i:02d}_aq{aq}.mod'
    composer.write_mod(str(mod_path))
    
    wav_path = tmpdir / f'z6_gate_{i:02d}.wav'
    subprocess.run(['ffmpeg','-y','-i',str(mod_path),'-f','wav',str(wav_path)],
                  capture_output=True, timeout=15)
    
    feats = extractor.extract(str(wav_path), use_all=False)
    mid = feats['midlevel']
    bpm = mid.get('bpm')
    onset = mid.get('onset_rate')
    
    pred_nb = classify(feats, baseline=False)
    pred_b  = classify(feats, baseline=True)
    
    line = f"| {i} | {aq} | {gate} | {bpm} | {onset} | Z{pred_nb} | Z{pred_b} |"
    lines.append(line)
    print(f"  AQ={aq:3}  gate={gate:3}  bpm={bpm}  → noBase=Z{pred_nb}  base=Z{pred_b}")

report_path.write_text('\\n'.join(lines) + '\\n')
print("\\nReport:", report_path)
