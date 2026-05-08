#!/usr/bin/env python3
"""vae_train.py — Train a VAE on balanced 900-track MIR dataset (29-dim)."""

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

# ── Model ─────────────────────────────────────────────────────────────────────
class VAE(nn.Module):
    def __init__(self, input_dim=29, latent_dim=10, hidden_sizes=(128, 64)):
        super().__init__()
        self.latent_dim = latent_dim
        # Encoder backbone
        enc_layers = []
        prev = input_dim
        for h in hidden_sizes:
            enc_layers += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        self.encoder_backbone = nn.Sequential(*enc_layers)
        self.fc_mu    = nn.Linear(prev, latent_dim)
        self.fc_logvar= nn.Linear(prev, latent_dim)
        # Decoder
        dec_layers = []
        prev = latent_dim
        for h in reversed(hidden_sizes):
            dec_layers += [nn.Linear(prev, h), nn.ReLU()]
            prev = h
        dec_layers.append(nn.Linear(prev, input_dim))
        self.decoder = nn.Sequential(*dec_layers)

    def encode(self, x):
        h = self.encoder_backbone(x)
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        return self.decode(z), mu, logvar


def vae_loss(recon_x, x, mu, logvar, beta=0.01):
    recon_mse = nn.functional.mse_loss(recon_x, x, reduction='sum')
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    return recon_mse + beta * kl


def train_epoch(model, loader, optimizer, device, beta):
    model.train()
    total = 0
    for (x,) in loader:
        x = x.to(device)
        optimizer.zero_grad()
        recon, mu, logvar = model(x)
        loss = vae_loss(recon, x, mu, logvar, beta=beta)
        loss.backward()
        optimizer.step()
        total += loss.item()
    return total / len(loader.dataset)


def eval_epoch(model, loader, device, beta):
    model.eval()
    total = 0
    with torch.no_grad():
        for (x,) in loader:
            x = x.to(device)
            recon, mu, logvar = model(x)
            total += vae_loss(recon, x, mu, logvar, beta=beta).item()
    return total / len(loader.dataset)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--latent-dims", type=int, default=10)
    p.add_argument("--epochs",      type=int, default=300)
    p.add_argument("--batch",       type=int, default=64)
    p.add_argument("--lr",          type=float, default=1e-3)
    p.add_argument("--beta",        type=float, default=0.01)
    p.add_argument("--patience",    type=int, default=30)
    p.add_argument("--seed",        type=int, default=42)
    args = p.parse_args()

    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[vae_train] device={device}  latent={args.latent_dims}")

    # Load data
    data  = np.load(DATASET_NPZ)
    X_raw = data['X'].astype(np.float32)
    zones = data['zones'].astype(int)

    # Scaler
    scaler = joblib.load(SCALER_PATH)
    X = scaler.transform(X_raw)

    # Split
    X_tr, X_va, z_tr, z_va = train_test_split(
        X, zones, test_size=0.2, random_state=args.seed, stratify=zones
    )
    print(f"[vae_train] train={len(X_tr)}  val={len(X_va)}")

    train_ds = TensorDataset(torch.from_numpy(X_tr))
    val_ds   = TensorDataset(torch.from_numpy(X_va))
    train_dl = DataLoader(train_ds, batch_size=args.batch, shuffle=True)
    val_dl   = DataLoader(val_ds,   batch_size=args.batch)

    # Model + optimiser
    model = VAE(29, args.latent_dims).to(device)
    opt   = optim.Adam(model.parameters(), lr=args.lr)
    sched = optim.lr_scheduler.ReduceLROnPlateau(opt, factor=0.5, patience=10)

    best_val, wait = float('inf'), 0
    hist = {'train_loss': [], 'val_loss': []}

    for epoch in range(1, args.epochs + 1):
        tr_loss = train_epoch(model, train_dl, opt, device, args.beta)
        va_loss = eval_epoch(model, val_dl, device, args.beta)
        sched.step(va_loss)
        hist['train_loss'].append(tr_loss)
        hist['val_loss'].append(va_loss)

        if va_loss < best_val:
            best_val = va_loss; wait = 0
            torch.save(model.state_dict(), ARTIFACTS_DIR / f"vae_d{args.latent_dims}.pt")
        else:
            wait += 1

        if epoch % 20 == 0 or epoch == 1:
            print(f"  epoch {epoch:3d}  train={tr_loss:.2f}  val={va_loss:.2f}  (best={best_val:.2f})")
        if wait >= args.patience:
            print(f"  → early stop @ epoch {epoch}")
            break

    print(f"[vae_train] best val={best_val:.2f}  saved vae_d{args.latent_dims}.pt")

    # Encode full dataset
    model.eval()
    with torch.no_grad():
        Z_mu, _ = model.encode(torch.from_numpy(X).to(device))
        Z = Z_mu.cpu().numpy()

    np.savez_compressed(ARTIFACTS_DIR / f"latent_encodings_d{args.latent_dims}.npz",
                        Z=Z, y=data['y'], zones=zones,
                        meta=json.dumps({'latent_dim': args.latent_dims, 'beta': args.beta}))
    print(f"[vae_train] latent encodings saved")

    # Zone statistics
    zstats = {}
    for z in range(1, 10):
        m = zones == z
        Zz = Z[m]
        zstats[str(z)] = {
            'mean': Zz.mean(axis=0).tolist(),
            'std' : Zz.std(axis=0).tolist(),
            'n'   : int(len(Zz))
        }
    with open(ARTIFACTS_DIR / f"zone_latent_stats_d{args.latent_dims}.json", 'w') as f:
        json.dump(zstats, f, indent=2)
    print(f"[vae_train] zone stats saved")

    # History
    with open(ARTIFACTS_DIR / f"vae_history_d{args.latent_dims}.json", 'w') as f:
        json.dump(hist, f, indent=2)
    print("✅ Done.")


if __name__ == "__main__":
    main()
