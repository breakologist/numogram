#!/usr/bin/env python3
"""vae_hallucinate.py — End-to-end VAE hallucination for empty zones.

Steps:
  1. Train VAE (d=10) if missing.
  2. Encode full corpus → per-zone latent statistics.
  3. Sample from target empty zones (default 3,4,5,8,9) using chosen geometry.
  4. Decode latent → MIR (via VAE decoder).
  5. Invert MIR → MOD (mir_to_mod.Path B).
  6. Render MOD → WAV (audio-renderer).
  7. Classify WAV → zone prediction.
  8. Report accuracy + artefacts.

M2 validation success criteria:
  - ≥80% of hallucinated tracks classified as their target zone.
  - VAE reconstruction MSE on val set not collapsed.
"""

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

import argparse, json, sys, time, hashlib
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

# ── Make sibling audio-renderer importable ───────────────────────────────────
# data_collector.py pattern: add the audio-renderer directory directly
if str(AUDIO_RENDERER) not in sys.path:
    sys.path.insert(0, str(AUDIO_RENDERER))

# ── Local mod-writer packages ────────────────────────────────────────────────
sys.path.insert(0, str(MOD_WRITER_ROOT))
sys.path.insert(0, str(SKILL_DIR))  # enable import of mir_to_mod


# ── Imports ───────────────────────────────────────────────────────────────────
from renderer           import render_mod_to_wav  # noqa: E402
from synth              import SoftSynth           # noqa: E402
from mod_writer.song    import SongBuilder          # noqa: E402
from mod_writer.classifier import predict_audio
from mir_to_mod import generate as mir_to_mod_generate

from vae_train import VAE
    # noqa: E402

OUTPUT_DIR = SKILL_DIR / 'output'

# ── Helpers ───────────────────────────────────────────────────────────────────
def ensure_vae(latent_dim, epochs=200):
    ckpt = ARTIFACTS_DIR / f'vae_d{latent_dim}.pt'
    if ckpt.exists(): return
    print('[hallucinate] Training VAE …')
    cmd = [sys.executable, str(SKILL_DIR / 'vae_m2' / 'vae_train.py'),
           '--latent-dims', str(latent_dim), '--epochs', str(epochs)]
    subprocess.run(cmd, check=True)

def load_resources(latent_dim):
    scaler = joblib.load(SCALER_PATH)
    ckpt = ARTIFACTS_DIR / f'vae_d{latent_dim}.pt'
    model = VAE(input_dim=29, latent_dim=latent_dim)
    state = torch.load(ckpt, map_location='cpu', weights_only=True)
    model.load_state_dict(state)
    model.eval()
    with open(ARTIFACTS_DIR / f'zone_latent_stats_d{latent_dim}.json') as f:
        stats = json.load(f)
    return scaler, model, stats

# ── Sampling functions (mirrored from vae_sample) ────────────────────────────
def syzygy_partner(zone): return 9 - zone
def triangular_weights():
    T10 = 55
    return [ (i*(i+1)//2) / T10 for i in range(1,10) ]

def latent_zone_sample(zone, count, stats, latent_dim, entropy_hex=None):
    mu    = np.array(stats[str(zone)]['mean'], dtype=np.float32)
    sigma = np.array(stats[str(zone)]['std'],  dtype=np.float32) * 0.25
    if entropy_hex:
        seed = int(entropy_hex,16) % (2**32)
        rng  = np.random.RandomState(seed)
        return rng.randn(count, latent_dim).astype(np.float32) * sigma + mu
    return np.random.randn(count, latent_dim).astype(np.float32) * sigma + mu

def linear_interp(zA, zB, steps):
    t = np.linspace(0,1,steps)
    return (1-t)[:,None]*zA + t[:,None]*zB

def triangular_sample(zone, stats, latent_dim):
    mu    = np.array(stats[str(zone)]['mean'])
    sigma = np.array(stats[str(zone)]['std']) * 0.25
    t_weights = triangular_weights()
    points = [ mu + np.random.randn(latent_dim).astype(np.float32)*sigma*w for w in t_weights ]
    return np.stack(points)

def pandemonium_path(a,b,c,steps,stats,latent_dim):
    muA,muB,muC = [np.array(stats[str(z)]['mean']) for z in (a,b,c)]
    half = steps//2
    leg1 = linear_interp(muA,muB,half)
    leg2 = linear_interp(muB,muC,steps-half)
    return np.vstack([leg1, leg2[1:]])

# ── Main pipeline ─────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--latent-dim', type=int, default=10)
    p.add_argument('--empty-zones', type=str, default='3,4,5,8,9')
    p.add_argument('--samples-per-zone', type=int, default=20)
    p.add_argument('--mode', type=str, default='zone',
                   choices=['zone','linear','syzygy','triangular','pandemonium','plex','entropy'])
    p.add_argument('--zA', type=int)
    p.add_argument('--zB', type=int)
    p.add_argument('--steps', type=int, default=10)
    p.add_argument('--seed', type=int)
    p.add_argument('--triplet', type=str)
    p.add_argument('--entropy', action='store_true')
    args = p.parse_args()

    ensure_vae(args.latent_dim)
    scaler, model, stats = load_resources(args.latent_dim)

    empty_zones = [int(z) for z in args.empty_zones.split(',')]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = {
        'latent_dim': args.latent_dim,
        'mode': args.mode,
        'empty_zones': empty_zones,
        'samples_per_zone': args.samples_per_zone,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'results': {},
    }

    all_results = []
    for zone in empty_zones:
        print(f'\n[hallucinate] Zone {zone} — mode={args.mode}')

        # Acquire latent vectors
        if args.mode == 'zone':
            ent_hex = None
            if args.entropy:
                try:
                    from numogram_entropy import NumogramEntropy
                    ne = NumogramEntropy()
                    ent_hex = ne.get_raw_bytes(8).hex()
                except: ent_hex = None
            Z = latent_zone_sample(zone, args.samples_per_zone, stats, args.latent_dim, ent_hex)

        elif args.mode == 'linear':
            if not (args.zA and args.zB): raise ValueError('--zA/--zB required')
            muA = np.array(stats[str(args.zA)]['mean'])
            muB = np.array(stats[str(args.zB)]['mean'])
            Z = linear_interp(muA, muB, args.steps)

        elif args.mode == 'syzygy':
            if args.seed is None: raise ValueError('--seed required')
            start = sum(int(d) for d in str(args.seed)) % 9 or 9
            chain = [start] + [syzygy_partner(chain[-1]) for _ in range(args.steps-1)]
            Z = np.stack([latent_zone_sample(z,1,stats,args.latent_dim)[0] for z in chain])

        elif args.mode == 'triangular':
            Z = triangular_sample(zone, stats, args.latent_dim)

        elif args.mode == 'pandemonium':
            if not args.triplet: raise ValueError('--triplet required (e.g. \"2 4 8\")')
            a,b,c = map(int, args.triplet.split())
            Z = pandemonium_path(a,b,c,args.steps,stats,args.latent_dim)

        elif args.mode == 'plex':
            muZ = np.array(stats[str(zone)]['mean'])
            mu9 = np.array(stats['9']['mean'])
            Z = linear_interp(muZ, mu9, args.steps)

        # Decode latent → scaled MIR → physical
        model.eval()
        with torch.no_grad():
            X_scaled = model.decode(torch.from_numpy(Z.astype(np.float32))).numpy()
        X_physical = scaler.inverse_transform(X_scaled)

        # Generate MOD+WAV per vector
        zone_results = []
        for i, mir_vec in enumerate(X_physical):
            track_id = f'z{zone}_{i:03d}_{args.mode}'
            mod_path = OUTPUT_DIR / 'mod' / f'{track_id}.mod'
            wav_path = OUTPUT_DIR / 'audio' / f'{track_id}.wav'
            aq = int(hashlib.sha1(','.join(f'{v:.3f}' for v in np.round(mir_vec,3)).encode()).hexdigest()[:8], 16) % 100

            # Delegate to mir_to_mod (Path B inversion)
            mir_to_mod_generate(
                mir=mir_vec,
                out_mod=mod_path,
                title=track_id,
                target_zone=zone
            )


            wav_path.parent.mkdir(parents=True, exist_ok=True)
            render_mod_to_wav(str(mod_path), str(wav_path))
            pred = predict_audio(str(wav_path))
            pz   = pred['zone']

            entry = {
                'track_id': track_id,
                'target_zone': zone,
                'predicted_zone': pz,
                'aq_seed': aq,
                'mod': str(mod_path),
                'wav': str(wav_path),
            }
            if args.entropy and 'ent_hex' in locals(): entry['entropy_hex'] = ent_hex
            zone_results.append(entry)

            if (i+1) % 10 == 0:
                hits = sum(r['predicted_zone']==zone for r in zone_results)
                print(f'  [{zone}] {i+1}/{len(Z)}  hits={hits}/{i+1}  {hits/(i+1)*100:.0f}%')

        hits = sum(r['predicted_zone']==zone for r in zone_results)
        acc  = hits / len(zone_results) if zone_results else 0.0
        summary['results'][str(zone)] = {
            'count': len(zone_results),
            'hits': int(hits),
            'accuracy': float(acc),
            'tracks': zone_results,
        }
        print(f'  ✅ Zone {zone}: {hits}/{len(zone_results)}  ({acc*100:.1f}%)')
        all_results.extend(zone_results)

    # Final report
    total  = sum(v['count'] for v in summary['results'].values())
    thits  = sum(v['hits']  for v in summary['results'].values())
    summary['total_samples']  = int(total)
    summary['total_hits']     = int(thits)
    summary['overall_accuracy'] = float(thits/total) if total else 0.0

    report_path = OUTPUT_DIR / 'm2_report.json'
    with open(report_path, 'w') as f: json.dump(summary, f, indent=2)
    print(f'\n✅ M2 done — overall {thits}/{total} = {summary["overall_accuracy"]*100:.1f}%')
    print(f'Report saved → {report_path}')

if __name__ == '__main__':
    main()
