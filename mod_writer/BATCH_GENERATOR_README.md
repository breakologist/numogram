# Zone Track Batch Generator (Phase 4.6 Locked Config)

Generate multiple MOD tracks for a given zone using the validated configuration.

## Single-zone generation
```bash
python zone_batch_generator.py --zone 2 --count 20 --outdir ./tracks/z2
```

## Multi-zone shell loop
```bash
for z in 1 2 3 4 5 6 7 8 9; do
  python zone_batch_generator.py --zone $z --count 10 --outdir ./all_zones/z$z
done
```

Output: per-zone directory contains N `.mod` files and a `zoneX_manifest.json` with AQ seeds, gate values, and params.

**Important:** To classify these tracks, use `validate_zone_bias.py --force-rhythm-baseline` or your own classifier with the same rhythm constants.
