#!/usr/bin/env python3
"""Fix generate_planchette format strings in oracle.py."""

from pathlib import Path

path = Path("/home/etym/.hermes/skills/numogram-oracle/oracle.py")
src = path.read_text()
lines = src.splitlines()

# Fix line 587 (index 586): Current/Gate/Syzygy format string
old_row = '    lines.append("  ║   Current: {c}    Gate: Gt-{g:<2}→Z{g:2}    Syzygy: {z}::{sy:2} ║".format(\n        c=current, g=gate_target, z=zone, sy=syzygy_partner))'
new_row = '    lines.append("  ║   Current: {c:2}    Gate: Gt-{g:<2}=Z{g:<2}    Syzygy: {z}::{sy:<2} ║".format(\n        c=current, g=gate_target, z=zone, sy=syzygy_partner))'

assert old_row in src, f"old_row not found. Searching near...\n" + \
    "\n".join(f"  {i+587:4d} | {lines[i]}" for i in range(585,590))
src = src.replace(old_row, new_row, 1)
print("1/2: Current/Gate/Syzygy row fixed")

# Fix line 584 header alignment (particle right-pad → left-pad)
old_header = '    lines.append("  ║   PLANCHETTE · Zone {znum:<3}  ({region:14})  [{particle}]".format(\n        znum=zone, region=region, particle=particle.ljust(8)))'
new_header = '    lines.append("  ║   ZONE {znum} · {region:<15}[{particle}]".format(\n        znum=zone, region=region, particle=particle.rjust(8)))'
assert old_header in src, "old_header not found"
src = src.replace(old_header, new_header, 1)
print("2/2: header fixed")

path.write_text(src)
print("Format strings updated.")

# quick test
test_src = path.read_text()
assert "format(c=current" in test_src
print("OK")
