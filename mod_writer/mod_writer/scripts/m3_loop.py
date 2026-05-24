#!/usr/bin/env python3
"""
M3 Phase 1 — Offline closed-loop: KS zone synth → WAV → MIR → zone classifier → verify.

Usage:
  python m3_loop.py --all                  # all 10 zones
  python m3_loop.py --zones 2 3 4          # subset
  python m3_loop.py --zone 3 --out /tmp    # single synth (WAV only, no MIR step)

Phase 2 (future): real-time sounddevice stream → rolling 3s windows → live MOD mutation.
"""

import argparse
import os
import sys
import json
import math
import wave
import tempfile
from pathlib import Path

import numpy as np
import joblib

# ──────────────────────────────────────────────────────────────────────────────
# Path setup (outer mod_writer/ is the package root, inner mod_writer/ is the code)
# ──────────────────────────────────────────────────────────────────────────────
NUMOGRAM_ROOT = Path.home() / "numogram"
SKILL_ROOT    = Path.home() / ".hermes" / "skills" / "numogram-audio" / "mod-writer"
_MOD_OUTER    = str(NUMOGRAM_ROOT / "mod_writer")          # /home/etym/numogram/mod_writer
_MOD_INNER    = str(NUMOGRAM_ROOT / "mod_writer" / "mod_writer")  # /home/etym/numogram/mod_writer/mod_writer

if _MOD_OUTER not in sys.path: sys.path.insert(0, _MOD_OUTER)

from mod_writer.mir_profiler import MIRFeatureExtractor   # ← now resolves from outer/ pkg

# ──────────────────────────────────────────────────────────────────────────────
# Karplus-Strong zone synth (canonical params, verified 2026-05-23)
# ──────────────────────────────────────────────────────────────────────────────
ZONE_PARAMS = {
    0: (140, 0.55, 0.30, 0.15),
    1: (180, 0.25, 0.60, 0.10),
    2: (250, 0.45, 0.50, 0.12),
    3: (200, 0.20, 0.70, 0.08),
    4: (120, 0.20, 0.65, 0.10),
    5: (300, 0.15, 0.80, 0.05),
    6: (180, 0.35, 0.55, 0.18),
    7: (160, 0.60, 0.40, 0.20),
    8: (150, 0.45, 0.50, 0.22),
    9: (90,  0.45, 0.35, 0.25),
}

ZONE_NAMES = {
    0: "void", 1: "surge", 2: "breaker", 3: "warp", 4: "gate",
    5: "pressure", 6: "abstraction", 7: "blood", 8: "multiplicity", 9: "plex",
}


def ks_string(f0: float, sr: int = 44100, dur: float = 2.5,
              decay: float = 0.5, brightness: float = 0.5,
              noise_amp: float = 0.2) -> np.ndarray:
    """Karplus-Strong plucked string — fractional-delay loop."""
    n   = int(sr * dur)
    Df  = sr / f0
    D   = int(math.floor(Df))
    rf  = Df - D
    N   = max(D + 4, 5)
    buf = np.zeros(N)
    exc = np.zeros(n)
    exc_len = min(D + 1, n)
    exc[:exc_len] = np.random.randn(exc_len) * noise_amp

    out = np.zeros(n, dtype=np.float64)
    lp  = 0.40 + brightness * 0.40
    z   = 0.0
    wr  = 0

    for i in range(n):
        rd     = wr - Df
        rd_n   = int(math.floor(rd)) % N
        frac   = rd - math.floor(rd)
        delayed = (1.0 - frac) * buf[rd_n] + frac * buf[(rd_n + 1) % N]
        z = lp * z + (1.0 - lp) * delayed
        buf[wr % N]      = z + exc[i]
        out[i]           = delayed
        wr               = (wr + 1) % N

    env = np.exp(-np.arange(n) / (sr * decay))
    return out * env


def synth_zone(zone: int, dur: float = 3.0, sr: int = 44100) -> np.ndarray:
    f0, decay, bright, noise = ZONE_PARAMS[zone]
    return ks_string(f0, sr=sr, dur=dur, decay=decay, brightness=bright, noise_amp=noise)


def wav_write(path: str, audio: np.ndarray, sr: int = 44100):
    pcm16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm16.tobytes())


# ──────────────────────────────────────────────────────────────────────────────
# Classifier
# ──────────────────────────────────────────────────────────────────────────────
def _load_clf():
    clf_path    = str(SKILL_ROOT / "mod_writer" / "classifier" / "artifacts" / "zone_clf.joblib")
    scaler_path = str(SKILL_ROOT / "mod_writer" / "classifier" / "artifacts" / "zone_scaler.joblib")
    if not Path(clf_path).exists():
        raise FileNotFoundError(f"Classifier not found: {clf_path}")
    return joblib.load(clf_path), joblib.load(scaler_path)


def _flatten(features: dict) -> np.ndarray:
    """29-dim vector matching classifier training schema."""
    vec: list[float] = []
    low = features.get('lowlevel', {})
    for band in ['sub_bass','bass','low_mid','mid','high_mid','high']:
        vec.append(low.get(band, 0.0))
    vec.append(float(low.get('spectral_centroid_hz', 0.0) or 0.0))
    vec.append(float(low.get('spectral_bandwidth_hz', 0.0) or 0.0))
    vec.append(float(low.get('spectral_rolloff', 0.0) or 0.0))
    vec.append(float(low.get('dynamic_complexity', 0.0) or 0.0))
    mid = features.get('midlevel', {})
    vec.append((float(mid.get('onset_rate') or 0.0)) / 200.0)
    vec.append((float(mid.get('bpm') or 0.0)) / 200.0)
    beatconf = mid.get('beat_confidence', 0.0)
    vec.append((float(beatconf) if beatconf is not None else 0.0) / 100.0)
    key_map = {'C':0,'C#':1,'D':2,'D#':3,'E':4,'F':5,'F#':6,'G':7,'G#':8,'A':9,'A#':10,'B':11}
    key_str = mid.get('key', '') or ''
    key_onehot = [0]*12; key_onehot[key_map.get(key_str, 0)] = 1
    vec.extend(key_onehot)
    scale_val = mid.get('scale', '') or ''
    if scale_val == 'major':   vec.extend([1, 0, 0])
    elif scale_val == 'minor': vec.extend([0, 1, 0])
    else:                       vec.extend([0, 0, 1])
    meta = features.get('metadata', {}) or {}
    dur  = meta.get('duration_s', 0.0) or 0.0
    vec.append(float(dur) / 120.0)
    return np.array(vec, dtype=np.float32)


def predict_zone(wav_path: str) -> dict:
    feats = MIRFeatureExtractor.extract(wav_path, use_all=False)
    vec   = _flatten(feats).reshape(1, -1)
    clf, scaler = _load_clf()
    zone_pred = int(clf.predict(scaler.transform(vec))[0])
    probas    = clf.predict_proba(scaler.transform(vec))[0]
    classes   = clf.classes_.tolist()
    proba_map = {int(c): round(float(p), 4) for c, p in zip(classes, probas)}
    return {
        'zone': zone_pred, 'probas': proba_map, 'features': feats,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Main loop
# ──────────────────────────────────────────────────────────────────────────────
def run_zone(zone: int, out_dir: Path, dur: float = 3.0) -> dict:
    name    = ZONE_NAMES[zone]
    wav_path = str(out_dir / f"z{zone:02d}_{name}.wav")
    print(f"  Z{zone:02d} ({name}): KS synth → {wav_path}")
    audio  = synth_zone(zone, dur=dur)
    wav_write(wav_path, audio)

    print(f"    MIR prediction →", end=" ")
    result = predict_zone(wav_path)
    pred   = result['zone']
    proba  = result['probas'].get(pred, 0.0)
    ok     = "✓" if pred == zone else "✗"
    print(f"Z{zone:02d} → Z{pred:02d}  p={proba:.3f}  {ok}")
    top3   = sorted(result['probas'].items(), key=lambda x: -x[1])[:3]
    ll     = result['features'].get('lowlevel', {})
    meta   = result['features'].get('metadata', {}) or {}
    return {
        'zone': zone, 'name': name, 'predicted': pred,
        'ok': pred == zone, 'proba': proba, 'top3': top3,
        'centroid_hz':  ll.get('spectral_centroid_hz', 0),
        'rms_db':      meta.get('rms_db', 0),
        'bpm':         result['features'].get('midlevel', {}).get('bpm'),
        'wav': wav_path,
    }


def main():
    ap = argparse.ArgumentParser(description="M3 Phase 1: KS-synth → MIR → zone classifier loop")
    ap.add_argument('--zone',  type=int,  default=None,  help='Single zone 0-9')
    ap.add_argument('--zones', type=int,  nargs='+',    help='Zone subset')
    ap.add_argument('--all',   action='store_true',     help='All 10 zones')
    ap.add_argument('--dur',   type=float, default=3.0, help='Synth duration (seconds)')
    ap.add_argument('--out',   type=str,  default='/tmp/m3_loop')
    args = ap.parse_args()

    if args.all:
        zones = list(range(10))
    elif args.zones:
        zones = args.zones
    elif args.zone is not None:
        zones = [args.zone]
    else:
        ap.error("pass --all / --zone N / --zones N N ...")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"=== M3 Phase 1 — Offline closed loop ===")
    print(f"Zones: {zones}  dur={args.dur}s  out={out_dir}\n")

    results = [run_zone(z, out_dir, dur=args.dur) for z in zones]

    # ── Summary ────────────────────────────────────────────────────────────
    n = len(results)
    correct = sum(1 for r in results if r['ok'])
    print(f"\n┌{'─'*58}┐")
    print(f"│ {'Zone':>5}  {'Name':<13} {'→':>8} {'OK':>5}  {'p(pred)':>9}    │")
    print(f"├{'─'*58}┤")
    for r in results:
        s = "✓" if r['ok'] else "✗"
        print(f"│ Z{r['zone']:02d}  {r['name']:<13} → Z{r['predicted']:02d}    {s:<5}  {r['proba']:.4f}       │")
    print(f"├{'─'*58}┤")
    print(f"│ {n-correct:>3} miss / {correct:>3} correct  →  {correct/n*100:.1f}% accuracy                     │")
    print(f"└{'─'*58}┘")

    summary = {
        'phase': 'M3-p1', 'mode': 'offline-closed-loop', 'duration_s': args.dur,
        'results': [{k: v for k, v in r.items() if k != 'features'} for r in results],
        'accuracy': correct / n if n else 0,
    }
    summary_path = out_dir / 'm3_p1_summary.json'
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"\nSummary: {summary_path}")
    return results


if __name__ == '__main__':
    main()
