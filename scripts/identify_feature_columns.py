#!/usr/bin/env python3
"""Identify V3 fresh dataset feature columns and map col_8."""
import numpy as np
import json
from pathlib import Path

artifacts = Path.home() / "numogram/mod_writer/mod_writer/classifier/artifacts"

# Load the fresh V3 dataset
fresh = np.load(artifacts / "dataset_balanced_900_v3_fresh.npz")
X = fresh['X']
feature_names = X.dtype.names if X.dtype.names else None

print(f"X shape: {X.shape}")
print(f"X dtype: {X.dtype}")

# If structured array, show feature names
if X.dtype.names:
    print(f"\n=== FEATURE NAMES ({len(X.dtype.names)} features) ===")
    for i, name in enumerate(X.dtype.names):
        col_data = X[name]
        z1_mean = np.mean(col_data[:50])
        z9_mean = np.mean(col_data[-50:])
        gradient = z9_mean - z1_mean
        print(f"col_{i:>2}: {name:<40s} Z1_mean={z1_mean:>10.4f}  Z9_mean={z9_mean:>10.4f}  Δ={gradient:>+10.4f}")
else:
    # Raw array — check meta field for feature names
    print(f"X is not structured. Checking meta field...")
    meta_str = str(fresh.get('meta', b''))
    print(f"meta: {meta_str[:500]}")
    
    # Try loading the classifier report for feature importances
    report_path = artifacts / "phase4.3_v3_fresh_report.json"
    if report_path.exists():
        report = json.loads(report_path.read_text())
        if "feature_importance" in report:
            fi = report["feature_importance"]
            print(f"\n=== FEATURE IMPORTANCE ===")
            for i, (name, imp) in enumerate(sorted(fi.items(), key=lambda x: -x[1])):
                print(f"  {name:<40s} importance={imp:.4f}")

# Also load the correlation matrix and inspect
# Try reading data_collector.py for how features are structured
dc_path = Path.home() / "numogram/mod_writer/mod_writer/classifier/data_collector.py"
dc_text = dc_path.read_text()

# Find feature extraction sections
print(f"\n=== FEATURE EXTRACTION IN data_collector.py ===")
for i, line in enumerate(dc_text.split('\n')):
    if any(kw in line.lower() for kw in ['extract', 'feature', 'flatten', 'mir', 'centroid', 'bandwidth', 'rolloff', 'mfcc']):
        if 'import' not in line.lower() and 'def ' not in line.lower()[:4]:
            print(f"  L{i+1}: {line.strip()[:120]}")
