#!/usr/bin/env python3
"""
Convenience wrapper for ZoneComposer production validation.

Hardcodes --force-rhythm-baseline (required for synthetic MODs) and
produces a clean summary table across all zones.

Usage:
  python zone-validate.py --rounds 50 --outdir ./validation_output
  python zone-validate.py --zones 1 2 3 --rounds 100
"""

import argparse, subprocess, sys, json, os
from pathlib import Path

SCRIPT = Path(__file__).parent / 'validate_zone_bias.py'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--zones', type=int, nargs='+', default=list(range(1,10)),
                   help='Target zones (default: all 1–9)')
    p.add_argument('--rounds', type=int, default=50,
                   help='Number of tracks per zone (default: 50)')
    p.add_argument('--length', type=int, default=16,
                   help='Section length in rows (default: 16, Zone 1 overridden to 32)')
    p.add_argument('--outdir', default='./zone_validation',
                   help='Output directory for .mod files (default: ./zone_validation)')
    args = p.parse_args()

    base_cmd = [
        sys.executable, str(SCRIPT),
        '--rounds', str(args.rounds),
        '--length', str(args.length),
        '--outdir', args.outdir,
        '--force-rhythm-baseline'
    ]

    results = {}
    print(f"{'='*50}")
    print(f"ZoneComposer Production Validation")
    print(f"Rounds: {args.rounds}  |  Baseline: FORCED  |  Length: {args.length}")
    print(f"{'='*50}\n")

    for zone in args.zones:
        cmd = base_cmd + ['--zone', str(zone)]
        print(f"→ Zone {zone} ... ", end='', flush=True)
        result = subprocess.run(cmd, capture_output=True, text=True)

        acc_line = [l for l in result.stdout.splitlines() if 'Hit rate:' in l]
        if acc_line:
            import re
            m = re.search(r'(\d+)/(\d+)\s*=\s*([\d.]+)%', acc_line[0])
            if m:
                hit, total, acc_pct = int(m.group(1)), int(m.group(2)), float(m.group(3))
                results[zone] = {'hit': hit, 'total': total, 'accuracy': acc_pct}
                color = '✓' if acc_pct >= 90 else '⚠'
                print(f"{acc_pct:.1f}%  {color}  ({hit}/{total})")
            else:
                print("PARSE ERROR")
                print("  raw:", acc_line[0][:120])
        else:
            print("FAILED")
            if result.stderr:
                print("  stderr:", result.stderr[:200])

    print(f"\n{'='*26}")
    print(f"{'Zone':>4} | {'Accuracy':>7} | {'Hit/Total':>9} | Status")
    print('-' * 42)
    all_ok = True
    for zone in range(1, 10):
        if zone in results:
            r = results[zone]
            status = '✅' if r['accuracy'] >= 90 else '⚠'
            if r['accuracy'] < 90:
                all_ok = False
            print(f"{zone:>4} | {r['accuracy']:>6.1f}% | {r['hit']}/{r['total']}   | {status}")
        else:
            print(f"{zone:>4} | {'—':>7} | {'—':>9} | ❌")

    print('=' * 42)
    if all_ok:
        print("✅ All zones ≥ 90% — production ready")
    else:
        print("⚠️  Some zones below threshold — review needed")

    json_path = Path(args.outdir) / 'validation_summary.json'
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(results, indent=2))
    print(f"\n📄 Summary saved: {json_path}")

if __name__ == '__main__':
    main()
