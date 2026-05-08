#!/usr/bin/env python3
"""
Sample from the VAE latent space using numogram-native geometries.

Modes:
  zone       —Sample from N(μ_z, Σ_z/4) for given zones.
  linear     —Linear interpolation between two zone means.
  syzygy     —Walk complementary syzygy pair (zone ↔ 9-zone).
  triangular —Sample at triangular-number points along the chosen path.
  pandemonium—Walk a triangular syzygy triplet (zone + partners).
  plex       —Fold through Zone 9 (Plex attractor).

Usage:
  python sample_latent.py --mode zone --zone 3 --count 20 --entropy-seed
  python sample_latent.py --mode syzygy --zone 2 --triangular --count 90
  python sample_latent.py --mode pandemonium --zone 4 --entropy-seed
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

import joblib
import numpy as np
import torch

# ── Paths ──────────────────────────────────────────────────────────────────────
HERMES = Path.home() / ".hermes"
MOD_WRITER = HERMES / "skills/numogram-audio/mod-writer"
ARTIFACTS = MOD_WRITER / "mod_writer/classifier/artifacts"
VAE_DIR = Path(__file__).parent.parent / "artifacts" / "vae_d10"  # adjust if d=16

# Load VAE definition dynamically (same as train_vae.py)
sys.path.insert(0, str(MOD_WRITER.parent.parent))  # mod-writer/
exec(open('/home/etym/.hermes/skills/numogram-audio/vae-hallucination/scripts/train_vae.py').read())  # Inline VAE from train_vae.py

# ── Helpers ────────────────────────────────────────────────────────────────────
def digital_root(n: int) -> int:
    dr = sum(int(d) for d in str(n)) % 9
    return 9 if dr == 0 else dr


def syzygy(zone: int) -> int:
    """Complementary syzygy partner (nine‑sum pairing)."""
    return 9 - zone


def triangular_points(n_points: int = 9, T_max: int = 55):
    """Return t in [0,1] at triangular numbers T_k / T_max for k=1..n_points."""
    tri = [k * (k + 1) // 2 for k in range(1, n_points + 1)]
    return [t / T_max for t in tri]


def load_zone_stats():
    with open(VAE_DIR / "zone_stats.json") as f:
        return json.load(f)


def load_vae(latent_dim: int, device):
    model = VAE(input_dim=29, latent_dim=latent_dim).to(device)
    ckpt = VAE_DIR / "vae_best.pt"
    if not ckpt.exists():
        ckpt = VAE_DIR / "vae_final.pt"
    model.load_state_dict(torch.load(ckpt, map_location=device))
    model.eval()
    return model


def get_entropy_bytes():
    """Draw 32 hardware entropy bytes if available, else /dev/urandom."""
    try:
        from numogram_entropy import NumogramEntropy
        ne = NumogramEntropy()
        raw = ne.get_raw_bytes()
        source = "numogram-entropy"
    except Exception:
        raw = os.urandom(32)
        source = "os.urandom"
    return raw, source


# ── Sampling strategies ─────────────────────────────────────────────────────────
def sample_zone(model, zone_stats, zone: int, count: int, device, entropy_hex=None):
    μ = torch.tensor(zone_stats[str(zone)]["mean"], dtype=torch.float32).to(device)
    cov = torch.tensor(zone_stats[str(zone)]["cov"], dtype=torch.float32).to(device)
    # Use Σ/4 to stay inside manifold
    std = torch.sqrt(torch.diag(cov)) / 2.0
    samples = []
    for _ in range(count):
        if entropy_hex:
            # Deterministic perturbation from entropy hex
            seed_int = int(entropy_hex[:8], 16) + len(samples)
            torch.manual_seed(seed_int)
        z = μ + torch.randn_like(std) * std
        samples.append(z.cpu().numpy())
    return np.stack(samples)


def interpolate_linear(μA, μB, t_values):
    """Linear interpolation between two mean vectors."""
    return [(1 - t) * μA + t * μB for t in t_values]


def sample_along_path(model, zone_stats, start_zone, end_zone, t_values, device, entropy_hex=None):
    μ_start = torch.tensor(zone_stats[str(start_zone)]["mean"], dtype=torch.float32).to(device)
    μ_end = torch.tensor(zone_stats[str(end_zone)]["mean"], dtype=torch.float32).to(device)
    points = interpolate_linear(μ_start, μ_end, t_values)
    # Add tiny entropy perturbation if requested
    if entropy_hex:
        raw, _ = get_entropy_bytes()
        eps = torch.tensor([int.from_bytes(raw[i:i+2], 'big') / 65536.0 - 0.5 for i in range(0, 8, 2)][:len(μ_start)], dtype=torch.float32).to(device)
        points = [p + eps * 0.125 for p in points]   # σ/8
    return torch.stack(points).cpu().numpy()


def sample_pandemonium(model, zone_stats, zone: int, t_values, device, entropy_hex=None):
    """Triangular syzygy triplet: zone + two partners (barycentric interior)."""
    from mapping import SYZYGY_PARTNERS  # local import to avoid circular
    partners = SYZYGY_PARTNERS.get(zone, ())
    if not partners:
        raise ValueError(f"Zone {zone} has no partners in SYZYGY_PARTNERS")
    if len(partners) < 2 and zone == 9:
        # pick first two distinct partners
        p1, p2 = partners[:2]
    else:
        p1, p2 = partners[:2]
    μA = torch.tensor(zone_stats[str(zone)]["mean"]).to(device)
    μB = torch.tensor(zone_stats[str(p1)]["mean"]).to(device)
    μC = torch.tensor(zone_stats[str(p2)]["mean"]).to(device)

    # Barycentric sampling: generate (α,β,γ) with sum=1, all ≥0
    points = []
    for t in t_values:
        # Parametric representation: walk edges in sequence zone→p1→p2→zone
        # We'll sample along perimeter for simplicity; interior variant can be added later
        if t < 0.33:
            local_t = t / 0.33
            pts = interpolate_linear(μA, μB, [local_t])
        elif t < 0.66:
            local_t = (t - 0.33) / 0.33
            pts = interpolate_linear(μB, μC, [local_t])
        else:
            local_t = (t - 0.66) / 0.34
            pts = interpolate_linear(μC, μA, [local_t])
        points.append(pts[0])
    arr = torch.stack(points).cpu().numpy()
    if entropy_hex:
        raw, _ = get_entropy_bytes()
        eps = torch.tensor([int.from_bytes(raw[i:i+2], 'big') / 65536.0 - 0.5 for i in range(0, 8, 2)[:arr.shape[1]]], dtype=torch.float32).to(device)
        arr = arr + eps.numpy() * 0.125
    return arr


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Sample VAE latent space with numogram geometries")
    parser.add_argument("--mode", choices=["zone", "linear", "syzygy", "triangular", "pandemonium", "plex"], required=True)
    parser.add_argument("--zone", type=int, help="Target zone (1–9)")
    parser.add_argument("--zones", nargs=2, type=int, help="Two zones for linear interpolation")
    parser.add_argument("--count", type=int, default=20, help="Samples per zone (or total for linear)")
    parser.add_argument("--latent-dim", type=int, default=10)
    parser.add_argument("--triangular", action="store_true", help="Use triangular-number t-values")
    parser.add_argument("--entropy-seed", action="store_true", help="Inject hardware entropy perturbation")
    parser.add_argument("--output", type=str, required=True, help="Output .npz path")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(42)

    # Load VAE and zone stats
    model = load_vae(args.latent_dim, device)
    zone_stats = load_zone_stats()

    # Determine t-values
    if args.triangular:
        t_values = triangular_points(n_points=9)
        if args.mode == "linear" and args.count < 9:
            t_values = t_values[:args.count]  # truncate if count smaller
    else:
        if args.mode == "zone":
            t_values = None  # not used
        else:
            t_values = np.linspace(0, 1, args.count)

    # Sampling
    if args.mode == "zone":
        if args.zone is None:
            parser.error("--zone required for mode=zone")
        entropy_hex = None
        if args.entropy_seed:
            raw, _ = get_entropy_bytes()
            entropy_hex = raw.hex()
        samples = sample_zone(model, zone_stats, args.zone, args.count, device, entropy_hex)
        zone_label = args.zone

    elif args.mode == "linear":
        if args.zones is None:
            parser.error("--zones A B required for mode=linear")
        zA, zB = args.zones
        samples = sample_along_path(model, zone_stats, zA, zB, t_values, device, args.entropy_seed)
        zone_label = f"{zA}_{zB}"

    elif args.mode == "syzygy":
        if args.zone is None:
            parser.error("--zone required for mode=syzygy")
        partner = syzygy(args.zone)
        samples = sample_along_path(model, zone_stats, args.zone, partner, t_values, device, args.entropy_seed)
        zone_label = f"{args.zone}_{partner}"

    elif args.mode == "pandemonium":
        if args.zone is None:
            parser.error("--zone required for mode=pandemonium")
        from mapping import SYZYGY_PARTNERS  # noqa: F401
        samples = sample_pandemonium(model, zone_stats, args.zone, t_values, device, args.entropy_seed)
        zone_label = f"{args.zone}_tri"

    elif args.mode == "plex":
        if args.zone is None:
            parser.error("--zone required for mode=plex")
        # Two variants: zone→9 and 9→zone; we'll do zone→9
        samples = sample_along_path(model, zone_stats, args.zone, 9, t_values, device, args.entropy_seed)
        zone_label = f"{args.zone}_9"

    else:
        raise ValueError(f"Unknown mode {args.mode}")

    # Save
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out_path, samples=samples, mode=args.mode, zone=zone_label, latent_dim=args.latent_dim)
    print(f"[sample_latent] Saved {samples.shape[0]} samples → {out_path}")


if __name__ == "__main__":
    main()
