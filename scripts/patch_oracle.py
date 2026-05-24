#!/usr/bin/env python3
"""Patch oracle.py: add --planchette flag and generate_planchette function."""

from pathlib import Path

path = Path("/home/etym/.hermes/skills/numogram-oracle/oracle.py")
src = path.read_text()

assert "do_planchette" not in src, "planchette already applied"

# ── 1. Flag initialisation ────────────────────────────────────────────────
old1 = "    do_base36 = False\n    \n    if \"--voice\" in args:"
new1 = "    do_base36 = False\n    do_planchette = False\n    \n    if \"--voice\" in args:"
assert old1 in src, "old1 not found"
src = src.replace(old1, new1, 1)
print("1/6: flag init applied")

# ── 2. --planchette flag detection ────────────────────────────────────────
old2 = '    if "--base36" in args or "--djynxxogram" in args:\n        do_base36 = True\n    \n    # ── BASE-36 DJYNXXOGRAM MODE ──'
new2 = '    if "--base36" in args or "--djynxxogram" in args:\n        do_base36 = True\n    if "--planchette" in args:\n        do_planchette = True\n    \n    # ── BASE-36 DJYNXXOGRAM MODE ──'
assert old2 in src, "old2 not found"
src = src.replace(old2, new2, 1)
print("2/6: flag detection applied")

# ── 3. Insert generate_planchette before generate_voice ─────────────────────
idx = src.find("def generate_voice(zone):")
assert idx > 0, f"generate_voice not found at {idx} (src len={len(src)})"
planchette_fn = """def generate_planchette(zone: int) -> str:
    \"\"\"Planchettte a brief zone-glyph planchette for oracle output.\"\"\"
    z = ZONES.get(zone, {"name": "???", "particle": "???", "region": "???"})
    gate_target = get_gate(zone)
    syzygy_partner = get_syzygy(zone)
    current = get_current(zone)
    region = z.get("region", "??")
    particle = z.get("name", "???")
    png = os.path.expanduser(
        "~/numogram/docs/wiki/assets/zone-glyphs/zone-{zone}.png".format(zone=zone)
    )

    lines = []
    lines.append("")
    lines.append("  ╔" + "═" * 52 + "╗")
    lines.append("  ║   PLANCHETTE · Zone {znum:<3}  ({region:14})  [{particle}]".format(
        znum=zone, region=region, particle=particle.ljust(8)))
    lines.append("  ╠" + "═" * 52 + "╣")
    lines.append("  ║   Current: {c}    Gate: Gt-{g:<2}→Z{g:2}    Syzygy: {z}::{sy:2} ║".format(
        c=current, g=gate_target, z=zone, sy=syzygy_partner))
    lines.append("  ║   PNG glyph: {png:<40}    ║".format(png=png))
    lines.append("  ╚" + "═" * 52 + "╝")
    return "\\n".join(lines)

"""
src = src[:idx] + planchette_fn + "\n" + src[idx:]
print("3/6: generate_planchette function inserted")

# ── 4. Print planchette before the reading ─────────────────────────────────
old4 = "    # Generate reading\n    reading, zone = generate_reading(seed, source)"
new4 = (
    "    if do_planchette and zone is not None:\n"
    "        print(generate_planchette(zone))\n"
    "        print()\n"
    "    \n"
    "    # Generate reading\n"
    "    reading, zone = generate_reading(seed, source)"
)
assert old4 in src, "old4 not found"
src = src.replace(old4, new4, 1)
print("4/6: planchette printing inserted")

# ── 5. Add to usage block ──────────────────────────────────────────────────
old5 = (
    '        print("  python3 oracle.py --compare --text \'TEXT\'  (cross-base comparison)")\n'
    '        print("  python3 oracle.py --compare --seed 174    (from AQ value)")\n'
    "        sys.exit(1)"
)
new5 = (
    '        print("  python3 oracle.py --compare --text \'TEXT\'  (cross-base comparison)")\n'
    '        print("  python3 oracle.py --compare --seed 174    (from AQ value)")\n'
    '        print("  python3 oracle.py --seed N --planchette  (zone glyph planchette)")\n'
    "        sys.exit(1)"
)
assert old5 in src, "old5 not found (check usage block indentation)"
src = src.replace(old5, new5, 1)
print("5/6: usage block updated")

# ── 6. Verify ──────────────────────────────────────────────────────────────
assert "do_planchette" in src
assert "generate_planchette" in src
assert "--planchette" in src
assert "--seed N --planchette" in src

path.write_text(src)
print("6/6: file written OK")
print(f"Total lines: {len(src.splitlines())}")
