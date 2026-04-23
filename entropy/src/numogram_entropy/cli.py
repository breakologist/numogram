"""
CLI for numogram-entropy.

Usage:
    numogram-entropy                      # Full report
    numogram-entropy --bytes 64           # 64 bytes of entropy
    numogram-entropy --zone               # Numogram zone from entropy
    numogram-entropy --traverse 8         # Numogram traversal (8 steps)
    numogram-entropy --iching             # I Ching hexagram
    numogram-entropy --stream 10          # Continuous stream
    numogram-entropy --json               # JSON output
"""

import json
import sys
import time

from .core import NumogramEntropy, collect_all, collect_and_aggregate


def _text_report(ne: NumogramEntropy):
    sources = ne.sources_available()
    seed = ne.get_seed(32)
    zone = ne.get_zone()

    print("=== numogram-entropy ===")
    print()
    print("Sources:")
    for k, v in sources.items():
        print(f"  {k}: {v}")
    print()
    print(f"Entropy (32 bytes): {seed.hex()}")
    print()
    print(f"Zone: {zone}")
    print(f"Syzygy: {9 - zone}")
    print(f"Current: {abs(zone - (9 - zone))}")


def _json_report(ne: NumogramEntropy):
    sources = ne.sources_available()
    seed = ne.get_seed(32)
    zone = ne.get_zone()
    path = ne.traverse(steps=5)

    report = {
        "sources": sources,
        "entropy_hex": seed.hex(),
        "zone": zone,
        "syzygy": 9 - zone,
        "current": abs(zone - (9 - zone)),
        "traversal": path,
    }
    print(json.dumps(report, indent=2))


def _stream(count: int, interval: float):
    ne = NumogramEntropy()
    print(f"Streaming {count} samples at {interval}s intervals.")
    print(f"{'#':>4}  {'Zone':>4}  {'Syzygy':>6}  {'Seed (hex)':>16}")
    print("-" * 40)
    for i in range(count):
        seed = ne.get_seed(8)
        zone = ne.get_zone()
        print(f"{i+1:4d}  {zone:4d}  {9-zone:6d}  {seed.hex():>16}")
        if i < count - 1:
            time.sleep(interval)


def _iching():
    ne = NumogramEntropy()
    hexagram = ne.iching()

    # Map to binary for display
    lines_desc = []
    for line in hexagram:
        if line["type"] == "yang":
            lines_desc.append(f"  Line {line['position']}: -------  {line['value']} {'(changing)' if line['changing'] else ''}")
        else:
            lines_desc.append(f"  Line {line['position']}: --- ---  {line['value']} {'(changing)' if line['changing'] else ''}")

    print("=== I Ching from Hardware Entropy ===")
    print()
    # Print top to bottom
    for desc in reversed(lines_desc):
        print(desc)

    changing = [l["position"] for l in hexagram if l["changing"]]
    print()
    if changing:
        print(f"Changing lines: {changing}")
    else:
        print("No changing lines. Stable hexagram.")


def main():
    args = sys.argv[1:]

    if "--json" in args:
        ne = NumogramEntropy()
        _json_report(ne)

    elif "--stream" in args:
        idx = args.index("--stream")
        count = int(args[idx + 1])
        interval = 1.0
        if "--interval" in args:
            iidx = args.index("--interval")
            interval = float(args[iidx + 1])
        _stream(count, interval)

    elif "--zone" in args:
        ne = NumogramEntropy()
        seed = ne.get_seed(8)
        zone = ne.get_zone()
        print(f"Seed: {seed.hex()}")
        print(f"Zone: {zone}")
        print(f"Syzygy: {9 - zone}")
        print(f"Current: {abs(zone - (9 - zone))}")

    elif "--traverse" in args:
        idx = args.index("--traverse")
        steps = int(args[idx + 1])
        ne = NumogramEntropy()
        seed = ne.get_seed(8)
        path = ne.traverse(steps=steps)
        print(f"Seed: {seed.hex()}")
        print()
        for p in path:
            print(f"  Step {p['step']}: zone={p['zone']}  "
                  f"syzygy={p['syzygy']}  current={p['current']}  "
                  f"gate→{p['gate_target']}")

    elif "--iching" in args:
        _iching()

    elif "--bytes" in args:
        idx = args.index("--bytes")
        n = int(args[idx + 1])
        ne = NumogramEntropy()
        print(ne.get_seed(n).hex())

    elif "--help" in args:
        print("numogram-entropy — Hardware entropy digested through numogram traversal")
        print()
        print("Usage:")
        print("  numogram-entropy                  Full report")
        print("  numogram-entropy --bytes N        N bytes of entropy (hex)")
        print("  numogram-entropy --zone           Numogram zone from entropy")
        print("  numogram-entropy --traverse N     Numogram traversal (N steps)")
        print("  numogram-entropy --iching         I Ching hexagram")
        print("  numogram-entropy --stream N       Continuous N-sample stream")
        print("  numogram-entropy --json           JSON output")

    else:
        ne = NumogramEntropy()
        _text_report(ne)
