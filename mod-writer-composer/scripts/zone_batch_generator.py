#!/usr/bin/env python3
"""
Batch generator: produce N MOD tracks per zone using the locked Phase 4.6 configuration.

Usage:
  python zone_batch_generator.py --zones 1 2 3 --count 20 --outdir ./tracks
  python zone_batch_generator.py --zone 2 --count 50 --outdir ./z2_tracks --seed-base 100

Configuration:
  - Square waveform, density 1.0 (continuous)
  - AQ‑seeded deterministic gate (SHA1 mod 37) — use seed_base to offset into candidate stream
  - Zone‑specific overrides:
      * Zone 1: duplicate_order=False, length=32
      * Zone 2: gate shift (5–7 → +20) enabled
      * Zones 3–9: duplicate_order=True, length=16
  - No rhythm baseline flag needed for generation (only for classification)
"""
import argparse, os, sys, json
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer')
sys.path.insert(0, '/home/etym/.hermes/skills/numogram-audio/mod-writer-composer/scripts')

from mod_writer.composer import ModComposer
from composer_extension import ZoneComposer, patch_mod_composer
from mod_writer.classifier.data_collector import _aq_candidates_for_zone

def generate_tracks(zone: int, count: int, outdir: str, seed_base: int = 0):
    os.makedirs(outdir, exist_ok=True)
    patch_mod_composer()
    aq_list = list(_aq_candidates_for_zone(zone, count=count, start_k=seed_base))

    # Resolve zone-specific params
    dup_order = False if zone == 1 else True
    length = 32 if zone == 1 else 16

    manifest = []
    for i, aq in enumerate(aq_list):
        composer = ModComposer(title=f"Z{zone}_track_{i:03d}")
        zc = ZoneComposer(composer)
        zc.target_zone(
            zone=zone,
            aq_seed=str(aq),
            duplicate_order=dup_order
        )
        zc.add_section(length=length, channel=0)
        filename = f"zone{zone}_track_{i:03d}.mod"
        filepath = os.path.join(outdir, filename)
        zc.composer.write_mod(filepath)
        manifest.append({
            "zone": zone,
            "index": i,
            "aq": aq,
            "file": filename,
            "length": length,
            "duplicate_order": dup_order,
            "gate": zc._gate_from_aq(str(aq))
        })

    manifest_path = os.path.join(outdir, f"zone{zone}_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    print(f"Zone {zone}: wrote {count} tracks + manifest to {outdir}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--zone', type=int, required=True, help='Target zone (1-9)')
    p.add_argument('--count', type=int, default=50, help='Number of tracks to generate')
    p.add_argument('--outdir', required=True, help='Output directory')
    p.add_argument('--seed-base', type=int, default=0, help='Offset into AQ candidate stream (default 0)')
    args = p.parse_args()

    generate_tracks(args.zone, args.count, args.outdir, args.seed_base)
    print("Done.")

if __name__ == '__main__':
    main()
