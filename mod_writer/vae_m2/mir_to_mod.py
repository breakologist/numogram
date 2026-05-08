#!/usr/bin/env python3
"""mir_to_mod.py — Convert a 29-dim MIR physical vector to a zone-aligned MOD (Path B).

Path B inversion steps:
  1. Load classifier + scaler (trained on 900-track corpus).
  2. Predict zone from MIR (just to know target).
  3. Derive deterministic aq_seed from rounded MIR (sha1 → int % 100).
  4. Build MOD with SongBuilder(zone, bpm_from_mir, aq_seed).
  5. Optionally render + classify for sanity check.

Matches the gate derivation used in data_collector:
  aq_seed = int(sha1(','.join(f'{v:.3f}' for v in np.round(mir,3))).hexdigest()[:8], 16) % 100
"""

import argparse, json, sys, hashlib
from pathlib import Path
import numpy as np
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────
SKILL_DIR       = Path(__file__).resolve().parent                    # vae_m2/
MOD_COMPOSER    = SKILL_DIR.parent.parent.parent                     # numogram-audio/
MOD_WRITER_ROOT = MOD_COMPOSER / 'mod-writer'
AUDIO_RENDERER  = MOD_COMPOSER / 'audio-renderer'
ARTIFACTS_DIR   = MOD_WRITER_ROOT / 'mod_writer' / 'classifier' / 'artifacts'

CLF_PATH        = ARTIFACTS_DIR / 'zone_clf.joblib'
SCALER_PATH     = ARTIFACTS_DIR / 'zone_scaler.joblib'

# ── Sibling package imports ───────────────────────────────────────────────────
if str(AUDIO_RENDERER) not in sys.path:
    sys.path.insert(0, str(AUDIO_RENDERER))
sys.path.insert(0, str(MOD_WRITER_ROOT))

from mod_writer.song          import SongBuilder

from renderer                 import render_mod_to_wav
from synth                    import SoftSynth

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_classifier_and_scaler():
    """Load trained RandomForest + StandardScaler."""
    clf   = joblib.load(CLF_PATH)
    scaler= joblib.load(SCALER_PATH)
    return clf, scaler

def aq_seed_from_mir(mir: np.ndarray) -> int:
    """Deterministic AQ seed (mod 100) from rounded MIR vector — matches corpus."""
    key = ','.join(f'{v:.3f}' for v in np.round(mir, 3))
    return int(hashlib.sha1(key.encode()).hexdigest()[:8], 16) % 100

def infer_params(mir: np.ndarray, clf, scaler) -> dict:
    """Extract musical params directly from MIR (no classifier zone needed)."""
    zone  = int(clf.predict(scaler.transform(mir.reshape(1,-1)))[0])
    bpm   = int(np.clip(round(mir[11] * 200) if mir[11] > 0 else 125, 60, 180))
    dens  = float(np.clip(mir[10] * 2.0, 0.2, 1.0))
    keys  = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    key   = keys[int(np.argmax(mir[13:25]))] if mir[13:25].max() > 0.5 else 'C'
    scales= ['major','minor','unknown']
    scale = scales[int(np.argmax(mir[25:28]))] if mir[25:28].max() > 0.5 else 'unknown'
    return {'zone':zone, 'bpm':bpm, 'density':dens, 'key':key, 'scale':scale}

def generate(mir: np.ndarray, out_mod: Path, title='VAE-Halluce', target_zone: int = None) -> Path:
    """Write a zone-aligned MOD file from a physical MIR vector."""
    out_mod = Path(out_mod)
    out_mod.parent.mkdir(parents=True, exist_ok=True)
    clf, scaler = load_classifier_and_scaler()
    p = infer_params(mir, clf, scaler)
    aq = aq_seed_from_mir(mir)
    print(f'[mir_to_mod] zone={p["zone"]} bpm={p["bpm"]} key={p["key"]} {p["scale"]} aq={aq}')
    build_zone = target_zone if target_zone is not None else p['zone']
    builder = SongBuilder(title=title, bpm=p['bpm'])
    builder.add_section(zone=build_zone, rows=64, aq_seed=str(aq))
    mod = builder.build(verbose=False)
    mod.write(str(out_mod))
    # Optional: sidecar with MIR + params
    sidecar = out_mod.with_suffix('.mir.json')
    sidecar.write_text(json.dumps({
        'mir_physical': mir.tolist(),
        'zone': p['zone'],
        'aq_seed': aq,
        'params': p,
    }, indent=2))
    return out_mod

# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--mir', required=True, help='.npy file with single 29-dim MIR vector')
    ap.add_argument('--out', required=True, help='Output .mod path')
    ap.add_argument('--title', default='VAE-Halluce')
    args = ap.parse_args()
    vec = np.load(args.mir)
    if vec.ndim > 1:
        vec = vec[0]
    assert vec.shape[0] == 29, f'need 29 features got {vec.shape}'
    generate(vec, Path(args.out), args.title)
