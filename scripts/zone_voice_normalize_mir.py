#!/usr/bin/env python3
"""Zone voice WAV: amplitude normalize, extract timbre-only MIR gradient."""
import numpy as np
import librosa
import json
from pathlib import Path

wav_dir = Path.home() / "numogram/session_2026-05-09_13-06-30"
out_dir = Path.home() / ".hermes/obsidian/hermetic/wiki/autonomous-journal/artifacts"
out_dir.mkdir(parents=True, exist_ok=True)

# Load all 9 zone voice WAVs
zone_data = {}
for z in range(1, 10):
    wav_path = wav_dir / f"zone_{z}_pure_44100.wav"
    if not wav_path.exists():
        print(f"⚠️  MISSING: {wav_path}")
        continue
    y, sr = librosa.load(wav_path, sr=44100, mono=True)
    zone_data[z] = {"y": y, "sr": sr, "path": str(wav_path)}
    print(f"Zone {z}: {len(y)} samples, sr={sr}")

# Compute normalized RMS = target RMS for all zones (use Z5 as moderate target)
rms_values = {z: np.sqrt(np.mean(d["y"]**2)) for z, d in zone_data.items()}
print(f"\nOriginal RMS: {', '.join(f'Z{z}={rms_values[z]:.5f}' for z in sorted(rms_values))}")

# Target: normalize all to RMS = 0.025 (between Z2 and Z3, avoids clipping)
target_rms = 0.025
for z, d in zone_data.items():
    if rms_values[z] > 0:
        scale = target_rms / rms_values[z]
        d["y_norm"] = d["y"] * scale
    else:
        d["y_norm"] = d["y"].copy()

# Verify normalized RMS
rms_norm = {z: np.sqrt(np.mean(d["y_norm"]**2)) for z, d in zone_data.items()}
print(f"Normalized RMS: {', '.join(f'Z{z}={rms_norm[z]:.5f}' for z in sorted(rms_norm))}")

# Extract MIR features from both original and normalized
def extract_mir(y, sr):
    """Extract key spectral features."""
    # Spectral centroid
    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    # Spectral bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    # Spectral flatness
    flatness = librosa.feature.spectral_flatness(y=y)[0]
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    # RMS energy (separate from MFCC-based)
    rms_feat = librosa.feature.rms(y=y)[0]
    
    return {
        "centroid_mean": float(np.mean(centroid)),
        "centroid_std": float(np.std(centroid)),
        "bandwidth_mean": float(np.mean(bandwidth)),
        "bandwidth_std": float(np.std(bandwidth)),
        "rolloff_mean": float(np.mean(rolloff)),
        "rolloff_std": float(np.std(rolloff)),
        "flatness_mean": float(np.mean(flatness)),
        "flatness_std": float(np.std(flatness)),
        "zcr_mean": float(np.mean(zcr)),
        "zcr_std": float(np.std(zcr)),
        "rms_mean": float(np.mean(rms_feat)),
    }

results = {}
for z in sorted(zone_data):
    d = zone_data[z]
    orig = extract_mir(d["y"], d["sr"])
    normd = extract_mir(d["y_norm"], d["sr"])
    results[z] = {"original": orig, "normalized": normd}

# Save full results
with open(out_dir / "zone_voice_timbre_mir_20260522.json", "w") as f:
    json.dump(results, f, indent=2)

# Print comparison table
print(f"\n{'Zone':>5} | {'Orig Centroid':>14} | {'Norm Centroid':>14} | {'Orig Flatness':>14} | {'Norm Flatness':>14} | {'Orig ZCR':>10} | {'Norm ZCR':>10}")
print("-" * 100)
for z in sorted(results):
    r = results[z]
    print(f"Z{z:>3} | {r['original']['centroid_mean']:>8.0f} Hz     | {r['normalized']['centroid_mean']:>8.0f} Hz     | "
          f"{r['original']['flatness_mean']:>8.4f}     | {r['normalized']['flatness_mean']:>8.4f}     | "
          f"{r['original']['zcr_mean']:>8.4f} | {r['normalized']['zcr_mean']:>8.4f}")

# Compute gradient analysis
print(f"\n{'='*80}")
print(f"GRADIENT ANALYSIS: Original vs Normalized")
print(f"{'='*80}")

for metric in ["centroid_mean", "bandwidth_mean", "rolloff_mean", "flatness_mean", "zcr_mean", "rms_mean"]:
    orig_vals = [results[z]["original"][metric] for z in sorted(results)]
    norm_vals = [results[z]["normalized"][metric] for z in sorted(results)]
    
    orig_start, orig_end = orig_vals[0], orig_vals[-1]
    norm_start, norm_end = norm_vals[0], norm_vals[-1]
    
    # Check monotonicity: count violations of Z1 < Z2 < ... < Z9 (increasing) or opposite
    orig_inc = sum(1 for i in range(1, len(orig_vals)) if orig_vals[i] > orig_vals[i-1])
    orig_dec = sum(1 for i in range(1, len(orig_vals)) if orig_vals[i] < orig_vals[i-1])
    norm_inc = sum(1 for i in range(1, len(norm_vals)) if norm_vals[i] > norm_vals[i-1])
    norm_dec = sum(1 for i in range(1, len(norm_vals)) if norm_vals[i] < norm_vals[i-1])
    
    print(f"\n{metric}:")
    print(f"  Original:   {orig_start:.2f} → {orig_end:.2f} (Δ={orig_end-orig_start:+.2f}), inc={orig_inc}/8, dec={orig_dec}/8")
    print(f"  Normalized: {norm_start:.2f} → {norm_end:.2f} (Δ={norm_end-norm_start:+.2f}), inc={norm_inc}/8, dec={norm_dec}/8")

# Check if centroid gradient direction changes after normalization
cent_orig = [results[z]["original"]["centroid_mean"] for z in sorted(results)]
cent_norm = [results[z]["normalized"]["centroid_mean"] for z in sorted(results)]
print(f"\n{'='*80}")
print(f"CENTROID TRAJECTORY COMPARISON")
print(f"{'='*80}")
for i, z in enumerate(sorted(results)):
    direction_orig = "↑" if i>0 and cent_orig[i] > cent_orig[i-1] else ("↓" if i>0 else " ")
    direction_norm = "↑" if i>0 and cent_norm[i] > cent_norm[i-1] else ("↓" if i>0 else " ")
    print(f"Z{z}: Orig={cent_orig[i]:>7.0f} Hz {direction_orig}  Norm={cent_norm[i]:>7.0f} Hz {direction_norm}")

print(f"\n{'='*80}")
print(f"CONCLUSION: Is centroid inversion an amplitude artefact?")
cent_orig_first_last = cent_orig[-1] - cent_orig[0]
cent_norm_first_last = cent_norm[-1] - cent_norm[0]
print(f"  Original centroid Δ: {cent_orig_first_last:+.0f} Hz")
print(f"  Normalized centroid Δ: {cent_norm_first_last:+.0f} Hz")
if cent_norm_first_last < cent_orig_first_last:
    print(f"  → Amplitude normalization REDUCED centroid gradient magnitude")
else:
    print(f"  → Amplitude normalization INCREASED centroid gradient magnitude")
if cent_orig_first_last < 0 and cent_norm_first_last < 0:
    print(f"  → INVERTED gradient PERSISTS after normalization — it's a TIMBRAL feature, not an amplitude artefact")
elif cent_orig_first_last < 0 and cent_norm_first_last > 0:
    print(f"  → Centroid inversion WAS an amplitude artefact — gradient NORMALIZED after RMS correction")
else:
    print(f"  → No inversion detected in either case")
