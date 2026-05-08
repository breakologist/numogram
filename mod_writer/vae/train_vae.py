#!/usr/bin/env python3
"""
Train a VAE on the 29‑dim MIR feature dataset (900 synthetic tracks).

Usage:
  python train_vae.py --latent-dim 10 --epochs 300 --batch-size 32 --seed 42
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import time

import joblib
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

# ── Paths ──────────────────────────────────────────────────────────────────────
HERMES = Path.home() / ".hermes"
MOD_WRITER = HERMES / "skills/numogram-audio/mod-writer"
ARTIFACTS = MOD_WRITER / "mod_writer/classifier/artifacts"
DATASET_NPZ = ARTIFACTS / "dataset_balanced_900.npz"
SCALER_PATH = ARTIFACTS / "zone_scaler.joblib"

# ── Model ─────────────────────────────────────────────────────────────────────
class VAE(nn.Module):
    """MLP‑VAE for 29‑dim MIR features."""
    def __init__(self, input_dim=29, latent_dim=10, hidden=[128, 64]):
        super().__init__()
        self.latent_dim = latent_dim
        # Encoder: → 2×latent (μ & logσ)
        enc_layers = []
        prev = input_dim
        for h in hidden:
            enc_layers.append(nn.Linear(prev, h))
            enc_layers.append(nn.ReLU())
            prev = h
        self.encoder_body = nn.Sequential(*enc_layers)
        self.fc_mu = nn.Linear(prev, latent_dim)
        self.fc_logvar = nn.Linear(prev, latent_dim)

        # Decoder: latent → input_dim
        dec_layers = []
        prev = latent_dim
        for h in reversed(hidden):
            dec_layers.append(nn.Linear(prev, h))
            dec_layers.append(nn.ReLU())
            prev = h
        dec_layers.append(nn.Linear(prev, input_dim))
        self.decoder = nn.Sequential(*dec_layers)

        # Auxiliary zone prediction head (Builder's suggestion: anchor latent space)
        self.zone_head = nn.Linear(latent_dim, 9)  # zones 1–9

    def encode(self, x):
        h = self.encoder_body(x)
        mu = self.fc_mu(h)
        logvar = self.fc_logvar(h)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        x_recon = self.decode(z)
        zone_logits = self.zone_head(z)
        return x_recon, mu, logvar, zone_logits


def vae_loss(x_recon, x, mu, logvar, zone_logits, zone_labels, beta=0.01):
    """Reconstruction (MSE) + KL + auxiliary zone classification loss."""
    recon = F.mse_loss(x_recon, x, reduction='sum')
    kl = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    zone_loss = F.cross_entropy(zone_logits, zone_labels)
    return recon + beta * kl + 0.1 * zone_loss, recon, kl, zone_loss


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Train VAE on MIR features")
    parser.add_argument("--latent-dim", type=int, default=10)
    parser.add_argument("--epochs", type=int, default=300)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--val-size", type=float, default=0.2)
    parser.add_argument("--beta-start", type=float, default=0.0)
    parser.add_argument("--beta-end", type=float, default=0.01)
    parser.add_argument("--beta-anneal-epochs", type=int, default=100)
    parser.add_argument("--patience", type=int, default=30)
    args = parser.parse_args()

    # Reproducibility
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train_vae] Device: {device}")

    # ── Load dataset ────────────────────────────────────────────────────────────
    print(f"[train_vae] Loading {DATASET_NPZ}")
    data = np.load(DATASET_NPZ)
    X = data['X'].astype(np.float32)
    zones = data['zones'].astype(np.int64)  # 1–9
    y_aq = data['y'].astype(np.int64)

    print(f"[train_vae] X shape: {X.shape}, zones: {sorted(set(zones.tolist()))}")

    # Standardise using saved scaler (same as classifier)
    scaler = joblib.load(SCALER_PATH)
    X_scaled = scaler.transform(X).astype(np.float32)

    # Train/val split (stratify by zone)
    X_tr, X_va, z_tr, z_va = train_test_split(
        X_scaled, zones, test_size=args.val_size, random_state=args.seed, stratify=zones
    )
    print(f"[train_vae] Train: {len(X_tr)}, Val: {len(X_va)}")

    train_ds = TensorDataset(torch.from_numpy(X_tr), torch.from_numpy(z_tr))
    val_ds = TensorDataset(torch.from_numpy(X_va), torch.from_numpy(z_va))
    train_dl = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_dl = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)

    # ── Model ───────────────────────────────────────────────────────────────────
    model = VAE(input_dim=29, latent_dim=args.latent_dim).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=10, factor=0.5)

    # Output dir
    out_dir = Path(__file__).parent / "artifacts" / f"vae_d{args.latent_dim}"
    out_dir.mkdir(parents=True, exist_ok=True)

    history = {"train_loss": [], "val_loss": [], "train_recon": [], "val_recon": [], "train_kl": [], "val_kl": []}
    best_val = float('inf')
    patience_counter = 0

    # β annealing
    def beta(epoch):
        if epoch < args.beta_anneal_epochs:
            return args.beta_start + (args.beta_end - args.beta_start) * (epoch / args.beta_anneal_epochs)
        return args.beta_end

    print(f"[train_vae] Starting training for {args.epochs} epochs…")
    start = time.time()

    for epoch in range(1, args.epochs + 1):
        model.train()
        train_loss = train_recon = train_kl = 0
        for xb, zb in train_dl:
            xb, zb = xb.to(device), zb.to(device)
            optimizer.zero_grad()
            x_recon, mu, logvar, zone_logits = model(xb)
            loss, recon, kl, _ = vae_loss(x_recon, xb, mu, logvar, zone_logits, zb - 1, beta=beta(epoch))
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
            train_recon += recon.item()
            train_kl += kl.item()

        model.eval()
        val_loss = val_recon = val_kl = 0
        with torch.no_grad():
            for xb, zb in val_dl:
                xb, zb = xb.to(device), zb.to(device)
                x_recon, mu, logvar, zone_logits = model(xb)
                loss, recon, kl, _ = vae_loss(x_recon, xb, mu, logvar, zone_logits, zb - 1, beta=beta(epoch))
                val_loss += loss.item()
                val_recon += recon.item()
                val_kl += kl.item()

        # Averages
        n_tr = len(train_dl)
        n_va = len(val_dl)
        tr_loss = train_loss / n_tr; tr_rec = train_recon / n_tr; tr_kl = train_kl / n_tr
        va_loss = val_loss / n_va; va_rec = val_recon / n_va; va_kl = val_kl / n_va

        history["train_loss"].append(tr_loss); history["val_loss"].append(va_loss)
        history["train_recon"].append(tr_rec); history["val_recon"].append(va_rec)
        history["train_kl"].append(tr_kl); history["val_kl"].append(va_kl)

        scheduler.step(va_loss)

        if epoch % 20 == 0 or epoch == 1:
            print(f"  Ep {epoch:3d} | train_loss={tr_loss:.2f} (recon={tr_rec:.2f}, kl={tr_kl:.2f}) | "
                  f"val_loss={va_loss:.2f} (recon={va_rec:.2f}, kl={va_kl:.2f}) | β={beta(epoch):.3f}")

        # Early stopping
        if va_loss < best_val - 1e-4:
            best_val = va_loss
            patience_counter = 0
            torch.save(model.state_dict(), out_dir / "vae_best.pt")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"[train_vae] Early stopping at epoch {epoch} (no val improvement for {args.patience} epochs)")
                break

    elapsed = time.time() - start
    print(f"[train_vae] Done in {elapsed:.1f}s. Best val loss: {best_val:.2f}")

    # Save final model and history
    torch.save(model.state_dict(), out_dir / "vae_final.pt")
    with open(out_dir / "history.json", "w") as f:
        json.dump(history, f, indent=2)

    # Encode full dataset and save latent vectors
    model.eval()
    with torch.no_grad():
        X_tensor = torch.from_numpy(X_scaled).to(device)
        mu_full, _ = model.encode(X_tensor)
        Z = mu_full.cpu().numpy()

    latent_path = out_dir / "Z_train.npz"
    np.savez_compressed(latent_path, Z=Z, zones=zones, y=y_aq, X_original=X)
    print(f"[train_vae] Latent encodings saved to {latent_path}")

    # Compute per‑zone latent statistics (μ_z, Σ_z)
    zone_stats = {}
    for z in range(1, 10):
        mask = zones == z
        if mask.sum() == 0:
            continue
        Z_z = Z[mask]
        zone_stats[int(z)] = {
            "mean": Z_z.mean(axis=0).tolist(),
            "cov": np.cov(Z_z, rowvar=False).tolist(),
            "n": int(mask.sum())
        }
    with open(out_dir / "zone_stats.json", "w") as f:
        json.dump(zone_stats, f, indent=2)
    print(f"[train_vae] Zone statistics saved.")

    print(f"[train_vae] Artifacts in {out_dir}")


if __name__ == "__main__":
    main()
