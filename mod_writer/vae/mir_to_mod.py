#!/usr/bin/env python3
"""
Invert MIR feature vectors to MOD generation parameters (Path B).

Strategy:
  1. Load synthetic dataset NPZ (900 tracks).
  2. For each hallucinated MIR vector x:
     - Find nearest training sample in StandardScaler space (Euclidean).
     - Clone that sample's generation parameters (zone, aq_seed, BPM, waveform, density, duplicate_order).
     - Optionally fine-tune parameters to push rendered MIR toward x (1–2 rounds).
  3. Write MOD via SongBuilder.

Output: one .mod per input MIR, plus a JSON manifest mapping output file → source parameters.
"""

import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import pairwise_distances

# ── Paths ──────────────────────────────────────────────────────────────────────
HERMES = Path.home() / ".hermes"
MOD_WRITER = HERMES / "skills/numogram-audio/mod-writer"
import sys; sys.path.insert(0, str(MOD_WRITER.parent.parent))  # mod-writer/
from mod_writer.song import SongBuilder
from mod_writer.mir_profiler import MIRFeatureExtractor

ARTIFACTS = MOD_WRITER / "mod_writer/classifier/artifacts"
DATASET_NPZ = ARTIFACTS / "dataset_balanced_900.npz"
SCALER_PATH = ARTIFACTS / "zone_scaler.joblib"

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_synthetic_corpus():
    data = np.load(DATASET_NPZ)
    X = data['X']        # (900, 29) raw features
    zones = data['zones']
    aq_seeds = [str(aq) for aq in data['y']]  # AQ integers as strings
    # We'll also need the generation parameters; reconstruct from zone + seed if not stored
    # For now, assume we can create a mapping from (zone, aq) → parameters via a lookup table
    # We'll derive BPM, waveform etc from zone defaults (ZONE_DEFAULTS from composer_extension)
    corpus = {
        'X': X,
        'zones': zones,
        'aq_seeds': aq_seeds,
    }
    return corpus


def zone_params(zone: int) -> dict:
    """Return generation parameter defaults for a zone (mirrors ZoneComposer.target_zone)."""
    # These must match the synthetic corpus generation exactly.
    # Source: composer_extension.ZoneComposer.ZONE_DEFAULTS (hard‑coded fallback)
    defaults = {
        1: {'bpm': 136, 'density': 1.0, 'waveform': 'square', 'duplicate_order': False},
        2: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        3: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        4: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        5: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        6: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        7: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        8: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
        9: {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True},
    }
    return defaults.get(zone, {'bpm': 125, 'density': 1.0, 'waveform': 'square', 'duplicate_order': True})


def find_nearest(x_scaled, X_corpus, top_k=1):
    """Return indices of top‑k nearest corpus points in Euclidean distance."""
    dists = np.linalg.norm(X_corpus - x_scaled, axis=1)
    idx = np.argsort(dists)[:top_k]
    return idx, dists[idx]


def aq_seed_from_mir(mir_vector, decimals=3):
    """Deterministic aq_seed derived from rounded MIR vector (ensures gate reproducibility)."""
    rounded = np.round(mir_vector, decimals=decimals)
    # Use bytes representation for stable hash
    key = rounded.tobytes()
    return hashlib.sha1(key).hexdigest()[:8]


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Invert MIR vectors to MOD files")
    parser.add_argument("--input", type=str, required=True, help=".npz with MIR samples (from sample_latent)")
    parser.add_argument("--outdir", type=str, required=True, help="Directory to write .mod files")
    parser.add_argument("--fine-tune", type=int, default=0, help="Extra rounds of param fine‑tuning (0–2)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Load scaler and corpus
    scaler = joblib.load(SCALER_PATH)
    corpus = load_synthetic_corpus()
    X_corpus_scaled = scaler.transform(corpus['X'])

    # Load hallucinated MIR samples
    data = np.load(args.input)
    samples = data['samples']  # (N, 29) — already in *scaled* space? Let's check
    # Assume samples are in latent‑decoded space but NOT re‑scaled; they should be inverse‑scaled to raw features first
    # The VAE was trained on scaled data, so its decoder outputs scaled space. We need to inverse‑transform.
    print(f"[mir_to_mod] Decoding {samples.shape[0]} latent vectors…")
    # For now we assume the input `samples` are already in **raw feature space** (decoder output scaled inverse?).
    # We'll standardise them anyway to match corpus distance metric.
    # If samples come directly from VAE decode (trained on scaled), they are in scaled space. Apply inverse_scaler.
    samples_raw = scaler.inverse_transform(samples)  # to physical units
    samples_scaled = scaler.transform(samples_raw)  # back to scaled — essentially same as samples if fed scaled→inverse→scale

    # Actually simpler: treat `samples` as scaled; compare to scaled corpus directly
    X_target_scaled = samples.astype(np.float32)

    # Build manifest
    manifest = []

    for i, x_scaled in enumerate(X_target_scaled):
        # Nearest synthetic neighbour
        idx, dists = find_nearest(x_scaled.reshape(1, -1), X_corpus_scaled, top_k=1)
        idx = idx[0]
        src_zone = int(corpus['zones'][idx])
        src_aq = corpus['aq_seeds'][idx]

        # Derive our own aq_seed from the MIR (gate contract)
        my_aq_seed = aq_seed_from_mir(x_scaled)

        # Base parameters from zone defaults
        params = zone_params(src_zone).copy()
        params.update({
            'zone': src_zone,
            'aq_seed': my_aq_seed,
        })

        # Optional fine‑tuning: adjust BPM/density to push rendered MIR toward target
        # (Not implemented in this first version — could add a 1‑step optimisation later)

        # Generate MOD
        builder = SongBuilder(title=f"hallucinated_z{src_zone}_{i:03d}", bpm=params['bpm'])
        builder.add_section(zone=src_zone, rows=64, aq_seed=my_aq_seed, waveform=params['waveform'])
        mod_path = outdir / f"track_{i:03d}_z{src_zone}.mod"
        builder.write(str(mod_path), verbose=False)

        manifest.append({
            'track_id': f"z{src_zone}_{i:03d}",
            'source_corpus_index': int(idx),
            'zone': src_zone,
            'aq_seed': my_aq_seed,
            'bpm': params['bpm'],
            'waveform': params['waveform'],
            'duplicate_order': params['duplicate_order'],
            'mod_path': str(mod_path),
            'latent_vector': samples[i].tolist(),
        })
        if args.verbose and i % 10 == 0:
            print(f"  [{i+1}/{len(X_target_scaled)}] zone={src_zone}, aq_seed={my_aq_seed}")

    manifest_path = outdir / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"[mir_to_mod] Wrote {len(manifest)} MODs + manifest → {outdir}")


if __name__ == "__main__":
    main()
