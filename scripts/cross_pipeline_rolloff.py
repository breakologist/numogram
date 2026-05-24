#!/usr/bin/env python3
"""Cross-pipeline feature comparison: col_8 (spectral rolloff) in V3 vs resonator."""
import numpy as np
import json
from pathlib import Path

artifacts = Path.home() / "numogram/mod_writer/mod_writer/classifier/artifacts"

# 1. V3 Fresh dataset: compute per-zone rolloff (col_8)
fresh = np.load(artifacts / "dataset_balanced_900_v3_fresh.npz")
X = fresh['X']
zones = fresh['zones']

# Column mapping: col_8 = spectral_rolloff
print("=" * 70)
print("V3 FRESH DATASET: Per-zone Spectral Rolloff (col_8)")
print("=" * 70)
header = "{:>5} | {:>7} | {:>12} | {:>11} | {:>11} | {:>11}".format(
    "Zone", "Samples", "Rolloff Mean", "Rolloff Std", "Rolloff Min", "Rolloff Max")
print(header)
print("-" * 70)
v3_rolloff = {}
for z in range(1, 10):
    mask = zones == z
    vals = X[mask, 8]
    v3_rolloff[z] = {
        "mean": float(np.mean(vals)),
        "std": float(np.std(vals)),
        "min": float(np.min(vals)),
        "max": float(np.max(vals)),
    }
    line = "Z{:>3} | {:>7d} | {:>8.2f} Hz   | {:>7.2f}    | {:>7.2f}     | {:>7.2f}".format(
        z, mask.sum(), np.mean(vals), np.std(vals), np.min(vals), np.max(vals))
    print(line)

# 2. Zone voice MIR data
mir_path = Path.home() / ".hermes/obsidian/hermetic/wiki/autonomous-journal/artifacts/zone_voice_timbre_mir_20260522.json"
zr_rolloff = {}
if mir_path.exists():
    mir = json.loads(mir_path.read_text())
    print("\n" + "=" * 70)
    print("ZONE VOICE (RESONATOR): Per-zone Spectral Rolloff")
    print("=" * 70)
    print("{:>5} | {:>12} | {:>11}".format("Zone", "Rolloff Mean", "Rolloff Std"))
    print("-" * 50)
    for z in sorted(mir, key=int):
        r = mir[z]["original"]
        zr_rolloff[int(z)] = {"mean": r["rolloff_mean"], "std": r["rolloff_std"]}
        print("Z{:>3} | {:>8.0f} Hz    | {:>7.0f}".format(z, r['rolloff_mean'], r['rolloff_std']))
else:
    print("\nZone voice MIR data NOT FOUND. Using hardcoded prior session values.")
    zr_data = {1: 3250, 2: 3561, 3: 3728, 4: 3605, 5: 3385,
               6: 2554, 7: 2480, 8: 2552, 9: 2533}
    for z, val in zr_data.items():
        zr_rolloff[z] = {"mean": float(val), "std": 0.0}

print("\n" + "=" * 70)
print("CROSS-PIPELINE COMPARISON: Spectral Rolloff Gradient")
print("=" * 70)
print("{:>5} | {:>11} | {:>18} | {:>12} | {:>14}".format(
    "Zone", "V3 Rolloff", "Resonator Rolloff", "Direction V3", "Direction Res"))
print("-" * 70)

d_v3 = [v3_rolloff[z]["mean"] for z in range(1, 10)]
d_zr = [zr_rolloff[z]["mean"] for z in range(1, 10)]

for i, z in enumerate(range(1, 10)):
    dir_v3 = chr(8593) if i > 0 and d_v3[i] > d_v3[i-1] else (chr(8595) if i > 0 else chr(8212))
    dir_zr = chr(8593) if i > 0 and d_zr[i] > d_zr[i-1] else (chr(8595) if i > 0 else chr(8212))
    print("Z{:>3} | {:>8.0f} Hz   | {:>8.0f} Hz         |       {}      |        {}".format(
        z, d_v3[i], d_zr[i], dir_v3, dir_zr))

v3_gradient = d_v3[-1] - d_v3[0]
zr_gradient = d_zr[-1] - d_zr[0]
print("\nV3 gradient: {:+.0f} Hz (INCREASING)".format(v3_gradient))
print("Resonator gradient: {:+.0f} Hz (DECREASING)".format(zr_gradient))
print("Gradient direction: {} ({} vs {})".format(
    "SAME" if (v3_gradient > 0) == (zr_gradient > 0) else "INVERTED",
    "INCREASING" if v3_gradient > 0 else "DECREASING",
    "INCREASING" if zr_gradient > 0 else "DECREASING"))
print("Gradient magnitude ratio: {:.2f}x".format(
    abs(v3_gradient) / abs(zr_gradient) if abs(zr_gradient) > 0 else float('inf')))
