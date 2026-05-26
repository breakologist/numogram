"""
mod_writer.classifier — MIR features → AQ prediction.

Public API:
  predict_audio(path: str) -> dict
  batch_predict(directory: str, limit=100) -> List[dict]
  load_artifacts() -> (scaler, model)
"""

import os, sys, tempfile, numpy as np, joblib, subprocess

# Ensure mod_writer package importable
_skill_root = os.path.join(os.path.dirname(__file__), "..", "..")
if _skill_root not in sys.path:
    sys.path.insert(0, _skill_root)

from mod_writer.mir_profiler import MIRFeatureExtractor

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
_KEY_MAP = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}

# Zone classifier artifacts (canonical, Phase 4.6+)
_zone_scaler = None
_zone_clf = None


def _load_zone_classifier():
    global _zone_scaler, _zone_clf
    if _zone_scaler is None:
        _zone_scaler = joblib.load(os.path.join(ARTIFACTS_DIR, "zone_scaler.joblib"))
        _zone_clf = joblib.load(os.path.join(ARTIFACTS_DIR, "zone_clf.joblib"))
    return _zone_scaler, _zone_clf


def load_artifacts():
    """Backward compat: return the zone classifier as (scaler, model)."""
    return _load_zone_classifier()


def _flatten(features: dict) -> np.ndarray:
    """Extract 29-dim feature vector — matches data_collector._flatten_features.

    Expected MIRFeatureExtractor output schema:
      lowlevel: sub_bass, bass, low_mid, mid, high_mid, high,
                spectral_centroid_hz, spectral_bandwidth_hz,
                spectral_rolloff, dynamic_complexity
      midlevel: onset_rate, bpm, beat_confidence, key (str), scale (str)
      metadata: duration_s
    """
    vec: list[float] = []
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
    key_idx = _KEY_MAP.get(key_str, 0)
    key_onehot = [0]*12; key_onehot[key_idx] = 1
    vec.extend(key_onehot)
    scale_val = mid.get('scale')
    if scale_val == 'major':
        vec.extend([1,0,0])
    elif scale_val == 'minor':
        vec.extend([0,1,0])
    else:
        vec.extend([0,0,1])
    meta = features.get('metadata', {}) or {}
    dur = meta.get('duration_s') or meta.get('duration') or 0.0
    vec.append(float(dur) / 120.0)
    return np.array(vec, dtype=np.float32)


def predict_audio(path: str) -> dict:
    """Transcode if necessary, extract MIR features, predict zone using the
    canonical zone classifier (Phase 4.6+, RandomForest 500 trees + StandardScaler).

    Returns dict with 'zone' (1-9), 'predicted_zone_prob', plus audio metadata.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext != '.wav':
        fd, wav = tempfile.mkstemp(suffix='.wav'); os.close(fd)
        subprocess.run(
            ['ffmpeg','-y','-i',path,'-f','wav','-acodec','pcm_s16le','-ar','44100','-ac','2',wav],
            capture_output=True, timeout=60
        )
        cleanup = True
    else:
        wav = path; cleanup = False

    try:
        feats = MIRFeatureExtractor().extract(wav, use_all=False)
        
        # OOD detection: check spectral centroid against training range [4817, 9683]
        TRAINING_CENTROID_MIN = 1782
        TRAINING_CENTROID_MAX = 4527
        centroid = feats.get('lowlevel', {}).get('spectral_centroid_hz', 0.0) or 0.0
        is_ood = centroid < TRAINING_CENTROID_MIN or centroid > TRAINING_CENTROID_MAX
        
        vec = _flatten(feats).reshape(1, -1)
        scaler, clf = _load_zone_classifier()
        zone_pred = int(clf.predict(scaler.transform(vec))[0])
        zone_probs = None
        if hasattr(clf, 'predict_proba'):
            zone_probs = clf.predict_proba(scaler.transform(vec))[0].tolist()
        meta = feats.get('metadata', {}) or {}
        return {
            'file': os.path.basename(path),
            'path': path,
            'zone': zone_pred,
            'predicted_zone_prob': zone_probs,
            'duration_s': meta.get('duration_s', 0.0),
            'bpm': feats.get('midlevel', {}).get('bpm'),
            'key': feats.get('midlevel', {}).get('key'),
            'scale': feats.get('midlevel', {}).get('scale'),
            'ood': is_ood,
            'spectral_centroid_hz': round(centroid, 1),
        }
    finally:
        if cleanup and os.path.exists(wav):
            os.unlink(wav)


def batch_predict(directory: str, limit: int = 100) -> list:
    """Walk `directory`, predict first `limit` audio files."""
    exts = {'.mp3','.flac','.wav','.m4a','.ogg'}
    results = []
    count = 0
    for root, dirs, files in os.walk(directory):
        for f in files:
            if os.path.splitext(f)[1].lower() in exts:
                try:
                    r = predict_audio(os.path.join(root, f))
                    results.append(r)
                    count += 1
                    if count >= limit:
                        return results
                except Exception:
                    continue
    return results
