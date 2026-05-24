#!/usr/bin/env python3
"""
M3 Phase 2 — Zone-feature profiling: MIR stats per KS zone.

Extract MIR features for each synthesised zone and report whether the
spectral-temporal feature space separates the zones (KS-domain benchmark, no
classifier involved).  Run after Phase 1 has populated WAVs:

  python m3_profile.py --src /tmp/m3_loop --out /tmp/m3_profile.json
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np

# ── identical path bootstrap to m3_loop.py ────────────────────────────────
_NUMOGRAM = Path.home() / "numogram"
_MOD_OUTER = str(_NUMOGRAM / "mod_writer")
_MOD_INNER = str(_NUMOGRAM / "mod_writer" / "mod_writer")
if _MOD_OUTER not in sys.path:
    sys.path.insert(0, _MOD_OUTER)
from mod_writer.mir_profiler import MIRFeatureExtractor

# same synth constants as m3_loop
ZONE_PARAMS = {
    0: (140, 0.55, 0.30, 0.15),
    1: (180, 0.25, 0.60, 0.10),
    2: (250, 0.45, 0.50, 0.12),
    3: (200, 0.20, 0.70, 0.08),
    4: (120, 0.20, 0.65, 0.10),
    5: (300, 0.15, 0.80, 0.05),
    6: (180, 0.35, 0.55, 0.18),
    7: (160, 0.60, 0.40, 0.20),
    8: (150, 0.45, 0.50, 0.22),
    9: (90,  0.45, 0.35, 0.25),
}
ZONE_NAMES = {
    0: "void", 1: "surge", 2: "breaker", 3: "warp", 4: "gate",
    5: "pressure", 6: "abstraction", 7: "blood", 8: "multiplicity", 9: "plex",
}

# zone ordering for tables
ZONES = list(range(10))


def synth_and_profile(zone: int, dur: float = 3.0, sr: int = 44100) -> dict:
    """Synthesise zone, run MIR, return summary dict."""
    import math, wave, tempfile, numpy as np

    f0, decay, bright, noise = ZONE_PARAMS[zone]
    n = int(sr * dur); Df = sr / f0; D = int(math.floor(Df))
    rf = Df - D; N = max(D + 4, 5)
    buf = np.zeros(N); exc = np.zeros(n)
    exc_len = min(D + 1, n)
    exc[:exc_len] = np.random.randn(exc_len) * noise
    out = np.zeros(n, dtype=np.float64)
    lp = 0.40 + bright * 0.40; z = 0.0; wr = 0
    for i in range(n):
        rd = wr - Df; rd_n = int(math.floor(rd)) % N
        frac = rd - math.floor(rd)
        delayed = (1.0 - frac) * buf[rd_n] + frac * buf[(rd_n + 1) % N]
        z = lp * z + (1.0 - lp) * delayed
        buf[wr % N] = z + exc[i]; out[i] = delayed; wr = (wr + 1) % N
    env = np.exp(-np.arange(n) / (sr * decay))
    audio = out * env

    # write WAV
    pcm16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tf:
        with wave.open(tf, 'wb') as wf:
            wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
            wf.writeframes(pcm16.tobytes())
        wav_path = tf.name

    feats = MIRFeatureExtractor.extract(wav_path, use_all=False)
    os.unlink(wav_path)
    return feats


def main():
    ap = argparse.ArgumentParser(description="M3 Phase 2: Zone MIR profiling")
    ap.add_argument('--src',  type=str, default='/tmp/m3_loop', help='WAVs dir (optional; if present, use existing WAVs)')
    ap.add_argument('--out',  type=str, default='/tmp/m3_profile.json')
    ap.add_argument('--seed', type=int, default=None, help='Random seed for repeatable synthesis')
    ap.add_argument('--dur',  type=float, default=3.0)
    ap.add_argument('--n',    type=int,   default=1, help='Samples per zone (averaged)')
    args = ap.parse_args()

    if args.seed is not None:
        np.random.seed(args.seed)

    print(f"=== M3 Phase 2 — Zone MIR profiling (n={args.n} per zone) ===\n")
    print(f"{'Zone':>5} | {'Name':<13} | {'centroid':>10} | {'rms_d':>7} | {'bandw':>7} | {'bpm':>8} | {'key':>5} | scale")
    print('-' * 78)

    zone_profiles = {}
    for z in ZONES:
        n = args.n
        centres = []
        rms_dbs = []
        bws     = []
        bpms    = []
        keys    = []
        scales  = []

        for _ in range(n):
            feats = synth_and_profile(z, dur=args.dur)
            ll = feats.get('lowlevel', {})
            ml = feats.get('midlevel', {})
            meta = feats.get('metadata', {}) or {}
            centres.append(ll.get('spectral_centroid_hz', 0))
            rms_dbs.append(meta.get('rms_db', 0))
            bws.append(ll.get('spectral_bandwidth_hz', 0))
            bpms.append(ml.get('bpm', 0) or 0)
            keys.append(ml.get('key', '?') or '?')
            scales.append(ml.get('scale', '?') or '?')

        mean_centroid = np.mean(centres)
        mean_rms      = np.mean(rms_dbs)
        mean_bw       = np.mean(bws)
        mean_bpm      = np.median(bpms) if len(bpms) > 1 else bpms[0]
        key_common    = max(set(keys), key=keys.count)
        scale_common  = max(set(scales), key=scales.count)

        name = ZONE_NAMES[z]
        print(f"Z{z:02d}   | {name:<13} |  {mean_centroid:>8.0f}  |  {mean_rms:>5.2f}  | {mean_bw:>7.0f}  |  {mean_bpm:>6.1f}  | {key_common:>5} | {scale_common}")

        zone_profiles[z] = {
            'name': name,
            'n': n,
            'centroid_hz_mean': float(round(mean_centroid, 1)),
            'rms_db_mean':      float(round(mean_rms, 3)),
            'bandwidth_hz_mean':float(round(mean_bw, 1)),
            'bpm_median':       float(round(mean_bpm, 2)),
            'key_common':       key_common,
            'scale_common':     scale_common,
            'per_sample': [{'centre': round(c,1), 'rms_db': round(r,3), 'bw':round(b,1), 'bpm':round(b2,2), 'key':k,'scale':s}
                           for c,r,b,b2,k,s in zip(centres, rms_dbs, bws, bpms, keys, scales)],
        }

    # centroid ordering
    cs = {z: zone_profiles[z]['centroid_hz_mean'] for z in ZONES}
    ordered = sorted(ZONES, key=lambda z: cs[z])
    print(f"\nCentroid order (low → high): {[f'Z{z} ({cs[z]:.0f}Hz)' for z in ordered]}")
    print(f"  Range: {min(cs.values()):.0f}–{max(cs.values()):.0f} Hz  span: {max(cs.values())-min(cs.values()):.0f} Hz")
    print(f"  Ratio: {max(cs.values())/min(cs.values()):.1f}×")

    # save
    out = {
        'mode': 'm3-phase2-zone-profiles',
        'seed': args.seed,
        'dur':  args.dur,
        'n_per_zone': n,
        'zones': zone_profiles,
        'centroid_order': ordered,
        'centroid_span': max(cs.values()) - min(cs.values()),
        'centroid_ratio': max(cs.values()) / min(cs.values()), 
    }
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {args.out}")


if __name__ == '__main__':
    main()
