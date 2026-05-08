#!/usr/bin/env python3
"""vae_sample.py — Latent sampling + interpolation (syzygy, triangular, pandemonium, plex, entropy)."""

#!/usr/bin/env python3
"""vae_train.py — Train a VAE on the 900-track MIR feature dataset.

Usage:
    python vae_train.py --latent-dims 10 --epochs 300 --batch 64
    python vae_train.py --latent-dims 16 --epochs 400 --batch 128

Outputs:
    artifacts/vae_d{latent_dims}.pt         – checkpoint (best val loss)
    artifacts/vae_d{latent_dims}_latents.npz – z-vectors for the training set
    artifacts/vae_d{latent_dims}_zone_stats.json – per-zone μ/σ
"""

import argparse, json, sys, time
from pathlib import Path
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import joblib

# ── Paths ─────────────────────────────────────────────────────────────────────
# vae_m2/ → scripts/ → mod-writer-composer/ → numogram-audio/
# Sibling skills are directories under numogram-audio/: mod-writer/, audio-renderer/
SKILL_DIR      = Path(__file__).resolve().parent          # vae_m2/
MOD_COMPOSER   = SKILL_DIR.parent.parent.parent           # numogram-audio/
MOD_WRITER_ROOT = MOD_COMPOSER / 'mod-writer'
AUDIO_RENDERER  = MOD_COMPOSER / 'audio-renderer'
ARTIFACTS_DIR   = MOD_WRITER_ROOT / 'mod_writer' / 'classifier' / 'artifacts'
DATASET_NPZ     = ARTIFACTS_DIR / 'dataset_balanced_900.npz'
SCALER_PATH     = ARTIFACTS_DIR / 'zone_scaler.joblib'
MODEL_PATH      = ARTIFACTS_DIR / 'vae_d{latent_dims}.pt'   # .format later

# ── Make sibling audio-renderer importable ───────────────────────────────────
# data_collector.py pattern: add the audio-renderer directory directly
if str(AUDIO_RENDERER) not in sys.path:
    sys.path.insert(0, str(AUDIO_RENDERER))

# ── Local mod-writer packages ────────────────────────────────────────────────
sys.path.insert(0, str(MOD_WRITER_ROOT))

# ── Imports ───────────────────────────────────────────────────────────────────
from renderer           import render_mod_to_wav  # noqa: E402
from synth              import SoftSynth           # noqa: E402
from mod_writer.song    import SongBuilder          # noqa: E402
from mod_writer.classifier import predict_audio    # noqa: E402

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_vae(latent_dim=10):
    from vae_train import VAE
    model = VAE(29, latent_dim)
    model.load_state_dict(torch.load(ARTIFACTS_DIR / f'vae_d{latent_dim}.pt', map_location='cpu'))
    model.eval()
    return model

def load_latent_stats(latent_dim):
    with open(ARTIFACTS_DIR / f'zone_latent_stats_d{latent_dim}.json') as f:
        return json.load(f)

def hardware_entropy_bytes(n_bytes=4):
    try:
        exe = Path.home() / 'numogram-entropy' / '.venv' / 'bin' / 'numogram-entropy'
        if exe.exists():
            result = subprocess.run([str(exe), '--stream', str(n_bytes*2)],
                                    capture_output=True, text=True, timeout=5)
            hexstr = result.stdout.strip().splitlines()[0]
            return bytes.fromhex(hexstr[:n_bytes*2])
        else:
            from numogram_entropy import NumogramEntropy
            ne = NumogramEntropy()
            raw = ne.get_raw_bytes(n_bytes*2)
            return raw[:n_bytes]
    except Exception as e:
        print(f'[warn] HW entropy fail ({e}); os.urandom fallback')
        return os.urandom(n_bytes)

def syzygy_partner(zone): return 9 - zone

def triangular_numbers(n=9):
    T10 = 55
    return [ (i*(i+1)//2) / T10 for i in range(1, n+1) ]

def pandemonium_triplet_vertices(zone):
    partners = {
        1: (5,9), 2: (4,8), 3: (6,9),
        4: (2,7), 5: (1,6), 6: (3,5),
        7: (4,9), 8: (2,9), 9: (1,3,5,7,8)
    }
    if zone == 9:
        return [(1,3,9), (1,5,9), (3,5,9), (2,4,9), (2,8,9), (4,7,9)]
    p = partners[zone]
    return [(zone, p[0], p[1])]

# ── Sampling ───────────────────────────────────────────────────────────────────
def sample_from_zone(zone, count, stats, latent_dim, entropy_hex=None):
    mu    = np.array(stats[str(zone)]['mean'], dtype=np.float32)
    sigma = np.array(stats[str(zone)]['std'],  dtype=np.float32) * 0.25
    if entropy_hex:
        seed = int(entropy_hex, 16) % (2**32)
        rng  = np.random.RandomState(seed)
        return rng.randn(count, latent_dim).astype(np.float32) * sigma + mu
    return np.random.randn(count, latent_dim).astype(np.float32) * sigma + mu

def linear_interp(zA, zB, steps):
    t = np.linspace(0, 1, steps)
    return (1-t)[:,None] * zA + t[:,None] * zB

def triangular_sample(zone, stats, latent_dim):
    t_weights = triangular_numbers(9)
    mu    = np.array(stats[str(zone)]['mean'])
    sigma = np.array(stats[str(zone)]['std']) * 0.25
    points = []
    for w in t_weights:
        direction = np.random.randn(latent_dim).astype(np.float32)
        points.append(mu + direction * sigma * w)
    return np.stack(points)

# ── Main ────────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mode', choices=['zone','linear','syzygy','triangular','pandemonium','plex','entropy'], required=True)
    p.add_argument('--latent-dim', type=int, default=10)
    p.add_argument('--count', type=int, default=20)
    p.add_argument('--zone', type=int)
    p.add_argument('--zA', type=int)
    p.add_argument('--zB', type=int)
    p.add_argument('--steps', type=int, default=10)
    p.add_argument('--seed', type=int)
    p.add_argument('--triplet', type=str)
    p.add_argument('--entropy', action='store_true')
    p.add_argument('--out', type=str, default='samples.npz')
    args = p.parse_args()

    model = load_vae(args.latent_dim)
    stats = load_latent_stats(args.latent_dim)

    if args.mode == 'zone':
        ent_hex = hardware_entropy_bytes(8).hex() if args.entropy else None
        Z = sample_from_zone(args.zone, args.count, stats, args.latent_dim, ent_hex)
        meta = {'mode':'zone','zone':args.zone,'count':args.count,'entropy':args.entropy}

    elif args.mode == 'linear':
        muA = np.array(stats[str(args.zA)]['mean'])
        muB = np.array(stats[str(args.zB)]['mean'])
        Z = linear_interp(muA, muB, args.steps)
        meta = {'mode':'linear','zA':args.zA,'zB':args.zB,'steps':args.steps}

    elif args.mode == 'syzygy':
        if args.seed is None: print('--seed required'); return
        start_zone = sum(int(d) for d in str(args.seed)) % 9 or 9
        chain = [start_zone]
        for _ in range(args.steps-1): chain.append(syzygy_partner(chain[-1]))
        Z_list = [sample_from_zone(z,1,stats,args.latent_dim)[0] for z in chain]
        Z = np.stack(Z_list)
        meta = {'mode':'syzygy','seed':args.seed,'chain':chain,'steps':args.steps}

    elif args.mode == 'triangular':
        if args.zone is None: print('--zone required'); return
        Z = triangular_sample(args.zone, stats, args.latent_dim)
        meta = {'mode':'triangular','zone':args.zone,'points':9}

    elif args.mode == 'pandemonium':
        if args.triplet is None: print('--triplet required'); return
        a,b,c = map(int, args.triplet.split())
        muA, muB, muC = [np.array(stats[str(z)]['mean']) for z in (a,b,c)]
        half = args.steps // 2
        leg1 = linear_interp(muA, muB, half)
        leg2 = linear_interp(muB, muC, args.steps - half)
        Z = np.vstack([leg1, leg2[1:]])
        meta = {'mode':'pandemonium','triplet':(a,b,c),'steps':args.steps}

    elif args.mode == 'plex':
        if args.zone is None: print('--zone required'); return
        muZ = np.array(stats[str(args.zone)]['mean'])
        mu9 = np.array(stats['9']['mean'])
        Z = linear_interp(muZ, mu9, args.steps)
        meta = {'mode':'plex','zone':args.zone,'steps':args.steps}

    elif args.mode == 'entropy':
        if args.zone is None: print('--zone required'); return
        ent_hex = hardware_entropy_bytes(8).hex()
        Z = sample_from_zone(args.zone, args.count, stats, args.latent_dim, entropy_hex=ent_hex)
        meta = {'mode':'entropy','zone':args.zone,'count':args.count,'entropy_hex':ent_hex}

    # Decode latent → MIR
    model.eval()
    with torch.no_grad():
        X_scaled = model.decode(torch.from_numpy(Z.astype(np.float32))).numpy()
    scaler = joblib.load(SCALER_PATH)
    X_physical = scaler.inverse_transform(X_scaled)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out, Z=Z, X_scaled=X_scaled, X_physical=X_physical,
                       meta=json.dumps(meta))
    print(f'[vae_sample] saved {len(Z)} vectors → {out}')
    print(f'  meta: {meta}')

if __name__ == '__main__':
    main()
