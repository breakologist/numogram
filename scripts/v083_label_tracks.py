#!/usr/bin/env python3
"""Label ~200 real tracks using v0.8.3 classifier for listening review."""
import sys, os, json, random, time
import numpy as np
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
from mod_writer.mir_profiler import MIRFeatureExtractor
import joblib

KEY_MAP = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
ZONE_NAMES = {0:'Void',1:'Surge',2:'Separation',3:'Release',4:'Gate',
              5:'Pressure',6:'Abstraction',7:'Blood',8:'Multiplicity',9:'Plex'}

def flatten_new(features):
    vec = []
    ll = features.get('lowlevel', {})
    for band in ['sub_bass','bass','low_mid','mid','high_mid','high']:
        vec.append(float(ll.get(band,0.0)))
    vec.append(float(ll.get('spectral_centroid_hz', 0.0)))
    vec.append(float(ll.get('spectral_bandwidth_hz', 0.0)))
    vec.append(0.0); vec.append(0.0)
    onset = features.get('derived',{}).get('onset_density_hz', 0.0)
    vec.append(min(onset/200.0, 1.0))
    bpm = features.get('midlevel',{}).get('bpm', 0.0)
    vec.append(bpm/200.0 if bpm else 0.0); vec.append(0.0)
    key_str = features.get('midlevel',{}).get('key','')
    key_idx = KEY_MAP.get(key_str,0) if key_str else 0
    onehot = [0]*12; onehot[key_idx] = 1; vec.extend(onehot)
    vec.extend([0,0,1])
    dur = features.get('metadata',{}).get('duration_s', 0.0)
    vec.append(float(dur)/120.0)
    return np.array(vec, dtype=np.float32)

# Load classifier
art_dir = '/home/etym/.hermes/skills/numogram-audio/mod-writer/mod_writer/classifier/artifacts'
clf = joblib.load(os.path.join(art_dir, 'zone_clf_v083.joblib'))
scl = joblib.load(os.path.join(art_dir, 'zone_scaler_v083.joblib'))

# Gather tracks
music_root = '/run/media/etym/Extreme SSD/music'
exts = {'.mp3','.flac','.wav','.m4a','.ogg'}
all_tracks = []
for root, dirs, files in os.walk(music_root):
    for f in files:
        if os.path.splitext(f)[1].lower() in exts:
            all_tracks.append(os.path.join(root, f))
    if len(all_tracks) > 20000: break

random.seed(99)
candidates = random.sample(all_tracks, min(300, len(all_tracks)))

extractor = MIRFeatureExtractor()
results = []
labeled = 0
skipped = 0
n_target = 200
t0 = time.time()

for i, path in enumerate(candidates):
    if labeled >= n_target: break
    if i % 20 == 0:
        elapsed = time.time() - t0
        print(f"  [{i}/{min(n_target*2, len(candidates))}] {labeled} labeled, {skipped} skipped ({elapsed:.0f}s)")
    try:
        feats = extractor.extract(path, use_all=False)
        vec = flatten_new(feats).reshape(1, -1)
        proba = clf.predict_proba(scl.transform(vec))[0]
        max_prob = proba.max()
        zp = int(clf.classes_[proba.argmax()])

        rel = path.replace(music_root, '').lstrip('/')
        bpm_val = feats.get('midlevel', {}).get('bpm', 0)
        key_val = feats.get('midlevel', {}).get('key', '?')
        dur_val = feats.get('metadata', {}).get('duration_s', 0)

        results.append({
            'track': rel,
            'zone': zp,
            'zone_name': ZONE_NAMES[zp],
            'confidence': round(float(max_prob), 4),
            'bpm': round(float(bpm_val), 1) if bpm_val else None,
            'key': key_val,
            'duration_s': round(float(dur_val), 1),
        })
        labeled += 1
    except Exception as e:
        skipped += 1

elapsed = time.time() - t0
print(f"\nDone: {labeled} labeled, {skipped} skipped in {elapsed:.0f}s")

# Distribution
from collections import Counter
zc = Counter(r['zone'] for r in results)
print("\nZone distribution:")
for z in sorted(zc):
    confs = [r['confidence'] for r in results if r['zone'] == z]
    mean_conf = sum(confs)/len(confs)
    print(f"  Z{z} {ZONE_NAMES[z]:<14} {zc[z]:>3}  (mean confidence: {mean_conf:.2%})")

# Save
outdir = '/home/etym/numogram/mod_writer/mod_writer/classifier/artifacts/v083_listening'
os.makedirs(outdir, exist_ok=True)
outpath = os.path.join(outdir, 'v083_predictions.json')
with open(outpath, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nSaved to {outpath}")

# Print diverse selection
print("\n" + "="*70)
print("LISTENING SELECTION — 3 per zone (hi/med/lo confidence)")
print("="*70)
by_zone = {}
for r in results:
    by_zone.setdefault(r['zone'], []).append(r)

for z in sorted(by_zone):
    tracks = sorted(by_zone[z], key=lambda r: -r['confidence'])
    picks = []
    if len(tracks) >= 3:
        picks = [tracks[0], tracks[len(tracks)//2], tracks[-1]]
    else:
        picks = tracks
    for r in picks:
        bpm_str = f"{r['bpm']:.0f} BPM" if r['bpm'] else "—"
        artist = r['track'].split('/')[0] if '/' in r['track'] else ''
        title = r['track'].split('/')[-1][:60]
        print(f"  Z{z} {r['zone_name']:<14} [{r['confidence']:.1%}] {bpm_str:<10} {title}")
    print()
