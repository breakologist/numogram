#!/usr/bin/env python3
"""
iching.py — Standalone I Ching + Numogram Shadow Oracle

Extracted from oracle.py for modularity (per original notes in oracle).
Seed/hardware entropy → 6-line hexagram (6/7/8/9 values) → rich numogram projection.

Usage:
  python3 iching.py --iching
  python3 iching.py --iching --seed 192855
  python3 iching.py --iching --seed 0 --json
  python3 iching.py --cast                  # yarrow-stalk simulation (authentic probs)
  python3 iching.py --cast --seed 42
  python3 iching.py --iching --hardware

Features:
- Full 64 King Wen names + judgments (loaded from tianmu corpus when available)
- Curated numogram mappings from table.csv (18 strong resonances)
- Changing lines: pre/post (relating) hexagram + per-line transitions + line-gates
- --cast mode with traditional yarrow probabilities (6:1/16, 7:5/16, 8:7/16, 9:3/16)
- Rich numogram shadows (zone names, epithets, demons, gates) using expansion material + corpus

Pulls from: table.csv, yijing-expansion-v1.1.md (probs, line-gates, trigrams), tianmu-yijing-corpus.json (full judgments)

Companion: T'ai Hsuan Ching (ternary, Em-mediator) lives in oracle.py --taixuan for now.
Best time to extract taixuan.py: after iching stabilizes, or when we want full ternary casting parity.
"""

import sys
import os
import hashlib
import subprocess
import json
from typing import Optional, Dict, List, Any

# ─── SHARED HELPERS (self-contained for standalone use) ───

def digital_root(n: int) -> int:
    """Digital root (0 preserved for explicit Void)."""
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def get_syzygy(zone: int) -> int:
    return 9 - zone

def get_gate(zone: int) -> int:
    if zone == 0:
        return 0
    gate = sum(range(zone + 1))
    while gate >= 10:
        gate = sum(int(d) for d in str(gate))
    return gate

# Minimal enriched zone display data (sourced from philosophies + ccru-zone-voice)
# Used for beautiful shadow output. Keep in sync with oracle.py ZONES.
ZONE_DISPLAY = {
    0: {"full": "Void Resonance", "epithet": "Void", "phon": "eiaoung"},
    1: {"full": "Collapsed Gasp", "epithet": "Surge", "phon": "gl"},
    2: {"full": "Fractured Boundary", "epithet": "Hold", "phon": "dt"},
    3: {"full": "Turbulent Spiral", "epithet": "Warp", "phon": "zx"},
    4: {"full": "Reptilian Emergence", "epithet": "Sink", "phon": "skr"},
    5: {"full": "Pressurized Hiss", "epithet": "Hinge", "phon": "ktt"},
    6: {"full": "Recursive Consumption", "epithet": "Abyss", "phon": "tch"},
    7: {"full": "Ascending Breath", "epithet": "Blood", "phon": "pb"},
    8: {"full": "Lullaby Drift", "epithet": "Multiplicity", "phon": "mnm"},
    9: {"full": "Seized Vortex", "epithet": "Iron Core", "phon": "tn"},
}

def zone_display(zone: int) -> str:
    z = ZONE_DISPLAY.get(zone, {"full": f"Z{zone}", "epithet": "", "phon": ""})
    full = z["full"]
    epit = z.get("epithet", "")
    phon = z["phon"]
    if epit and epit != full:
        return f"{full} ({epit} / {phon})"
    elif full != phon:
        return f"{full} ({phon})"
    return phon or str(zone)

# Full King Wen names (sourced from tianmu-yijing-corpus.json + standard tradition)
KING_WEN = {
    1: 'The Creative',
    2: 'The Receptive',
    3: 'Difficulty at the Beginning',
    4: 'Youthful Folly',
    5: 'Waiting',
    6: 'Conflict',
    7: 'The Army',
    8: 'Holding Together',
    9: 'Small Taming',
    10: 'Treading',
    11: 'Peace',
    12: 'Standstill',
    13: 'Fellowship',
    14: 'Great Possession',
    15: 'Modesty',
    16: 'Enthusiasm',
    17: 'Following',
    18: 'Work on What Has Been Spoiled',
    19: 'Approach',
    20: 'Contemplation',
    21: 'Biting Through',
    22: 'Grace',
    23: 'Splitting Apart',
    24: 'Return',
    25: 'Innocence',
    26: 'Great Taming',
    27: 'Nourishment',
    28: 'Great Exceeding',
    29: 'The Abysmal Water',
    30: 'The Clinging Fire',
    31: 'Influence',
    32: 'Duration',
    33: 'Retreat',
    34: 'Great Power',
    35: 'Progress',
    36: 'Darkening of the Light',
    37: 'The Family',
    38: 'Opposition',
    39: 'Obstruction',
    40: 'Deliverance',
    41: 'Decrease',
    42: 'Increase',
    43: 'Breakthrough',
    44: 'Coming to Meet',
    45: 'Gathering Together',
    46: 'Pushing Upward',
    47: 'Oppression',
    48: 'The Well',
    49: 'Revolution',
    50: 'The Cauldron',
    51: 'The Arousing Thunder',
    52: 'Keeping Still',
    53: 'Development',
    54: 'The Marrying Maiden',
    55: 'Abundance',
    56: 'The Wanderer',
    57: 'The Gentle Wind',
    58: 'The Joyous Lake',
    59: 'Dispersion',
    60: 'Limitation',
    61: 'Inner Truth',
    62: 'Small Exceeding',
    63: 'After Completion',
    64: 'Before Completion',
}

def get_hex_name(num: int) -> str:
    return KING_WEN.get(num, f"Hexagram {num}")

# Line gates (from yijing-expansion-v1.1.md)
LINE_GATES = {
    1: "Gt-01",
    2: "Gt-03",
    3: "Gt-06",
    4: "Gt-10",
    5: "Gt-15",
    6: "Gt-21",
}

# Curated hexagram → numogram mappings (from raw/table.csv + expansion)
# These get priority for zone/demon/insight. All 64 now have good names from corpus.
CURATED_HEX_MAP: Dict[int, Dict[str, Any]] = {
    1: {"name": "Qian (Creative)", "zone": 1, "syzygy": "1::8", "demon": "Murrumur ★", "note": "First Surge current; high creative charge", "insight": "Any change drops pure yang momentum into multiplicity or descent"},
    2: {"name": "Kun (Receptive)", "zone": 2, "syzygy": "2::7", "demon": "Oddubb ★", "note": "Receptive ground of the Time-Circuit", "insight": "Changing lines introduce yang “seeds” that can cross into amphidemon territory"},
    3: {"name": "Zhun (Difficulty)", "zone": 2, "syzygy": "2::7", "demon": "Oddubb", "note": "Birth pangs in the Circuit", "insight": "Early struggle; changing lines often signal the first gate opening"},
    4: {"name": "Meng (Youthful Folly)", "zone": 3, "syzygy": "3::6", "demon": "Djynxx ★", "note": "Warp carrier activation possible", "insight": "Naive seeking; changing lines can spiral into Warp vortex"},
    6: {"name": "Song (Conflict)", "zone": 6, "syzygy": "3::6", "demon": "Djynxx", "note": "Warp-adjacent tension", "insight": "Contention; changing lines often produce unmediated wide-gap leaps"},
    7: {"name": "Shi (The Army)", "zone": 7, "syzygy": "2::7", "demon": "Oddubb", "note": "Military order meets Circuit discipline", "insight": "Disciplined advance; changing lines can call amphidemons across the boundary"},
    11: {"name": "Tai (Peace)", "zone": 2, "syzygy": "2::7", "demon": "Oddubb", "note": "Stable but fragile Circuit state", "insight": "Harmony; changing lines frequently mark shift from peace into tension"},
    18: {"name": "Gu (Work on What Has Been Spoiled)", "zone": 9, "syzygy": "9::0", "demon": "Uttunul", "note": "Strong Gt-45 resonance", "insight": "Decay and repair; changing lines near Plex often involve decay-into-renewal"},
    24: {"name": "Fu (Return)", "zone": 6, "syzygy": "—", "demon": "—", "note": "Strong rotor resonance; classic Time-Circuit cycle completion", "insight": "“On the seventh day comes return”"},
    27: {"name": "Yi (Nourishment)", "zone": 9, "syzygy": "9::0", "demon": "Uttunul ★", "note": "Plex-adjacent; Gt-45 proximity", "insight": "Nourishment from the heights/abyss; changing lines pull toward terminal gate"},
    29: {"name": "Kan (The Abysmal)", "zone": 2, "syzygy": "2::7", "demon": "Oddubb", "note": "Deep Circuit pressure", "insight": "Repeated danger; changing lines test endurance in the depths"},
    36: {"name": "Ming Yi (Darkening)", "zone": 9, "syzygy": "9::0", "demon": "Uttunul ★", "note": "Darkening of the light at the Plex threshold", "insight": "Light wounded but not extinguished; changing lines near Gt-45 can call xenodemons"},
    45: {"name": "Cui (Gathering)", "zone": 9, "syzygy": "9::0", "demon": "Uttunul", "note": "Directly feeds Gt-45 (Pandemonium Gate)", "insight": "Gathering at the terminal threshold; high possession risk"},
    51: {"name": "Zhen (The Arousing)", "zone": 6, "syzygy": "3::6", "demon": "Djynxx", "note": "High shock / vortex potential", "insight": "Thunderclap awakening; changing lines trigger sudden Warp breakthroughs"},
    55: {"name": "Feng (Abundance)", "zone": 1, "syzygy": "1::8", "demon": "Murrumur", "note": "Surge at maximum charge", "insight": "Peak abundance; changing lines often signal the moment of overflow into multiplicity"},
    61: {"name": "Zhong Fu (Inner Truth)", "zone": 7, "syzygy": "2::7", "demon": "Oddubb", "note": "Honest navigation of the Circuit", "insight": "Inner truth; changing lines test sincerity in the labyrinth"},
    63: {"name": "Ji Ji (After Completion)", "zone": 9, "syzygy": "9::0", "demon": "Uttunul", "note": "Often signals the plunge into Gt-45", "insight": "Already complete — danger of relaxing; changing lines reopen the circuit"},
    64: {"name": "Wei Ji (Before Completion)", "zone": 1, "syzygy": "1::8", "demon": "Murrumur", "note": "Highest transformation potential in the set", "insight": "Almost there; changing lines frequently open multiple gates at once"},
}

DEMON_MAP = {
    (0,9): "Uttunul (Ummnu / Om, Amen, Omen)", (9,0): "Uttunul (Ummnu / Om, Amen, Omen)",
    (1,8): "Murrumur", (8,1): "Murrumur",
    (2,7): "Oddubb", (7,2): "Oddubb",
    (3,6): "Djynxx", (6,3): "Djynxx",
    (4,5): "Katak", (5,4): "Katak",
}

def demon_from_zones(a: int, b: int) -> str:
    return DEMON_MAP.get((a, b), "Unknown")

# ─── CORPUS + JUDGMENTS (from tianmu-yijing-corpus.json) ───
def find_tianmu_corpus() -> Optional[str]:
    """Search common locations for the full judgments corpus."""
    candidates = [
        os.path.expanduser("~/.hermes/obsidian/hermetic/wiki/assets/tianmu-yijing-corpus.json"),
        "/home/etym/.hermes/obsidian/hermetic/wiki/assets/tianmu-yijing-corpus.json",
        os.path.expanduser("~/numogram/docs/wiki/assets/tianmu-yijing-corpus.json"),
        os.path.join(os.path.dirname(__file__), "tianmu-yijing-corpus.json"),
        "/home/etym/numogram/docs/wiki/assets/tianmu-yijing-corpus.json",
    ]
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None

_CORPUS_CACHE = None
BINARY_TO_TRAD: Dict[str, int] = {}
TRAD_TO_BINARY: Dict[int, str] = {}

def load_hex_info(num: int) -> Dict[str, Any]:
    """Return name + judgment + extra from corpus if available. Falls back gracefully."""
    global _CORPUS_CACHE, BINARY_TO_TRAD, TRAD_TO_BINARY
    info = {"name": get_hex_name(num), "judgment": None, "image": None}

    path = find_tianmu_corpus()
    if path and _CORPUS_CACHE is None:
        try:
            with open(path) as f:
                _CORPUS_CACHE = json.load(f)
        except Exception:
            _CORPUS_CACHE = {}

    if _CORPUS_CACHE and "hexagrams" in _CORPUS_CACHE:
        hexs = _CORPUS_CACHE["hexagrams"]
        h = hexs.get(str(num), {})
        if h:
            info["name"] = h.get("name_en") or h.get("king_wen") or info["name"]
            info["judgment"] = h.get("judgment")
            info["image"] = h.get("image")
            if "zone_canonical" in h and not CURATED_HEX_MAP.get(num):
                info["corpus_zone"] = h.get("zone_canonical")

        # Build lookup maps from binary <-> traditional num (critical for correct hex identification)
        if not BINARY_TO_TRAD:
            for tstr, hh in hexs.items():
                b = hh.get("binary")
                if b:
                    t = int(tstr)
                    BINARY_TO_TRAD[b] = t
                    TRAD_TO_BINARY[t] = b
    return info

def lines_to_binary_str(hex_lines: List[Dict]) -> str:
    """Build binary string matching corpus convention.
    hex_lines[0] = line 1 (bottom) → leftmost char in binary str.
    '1' = yang (solid), '0' = yin.
    """
    return ''.join('1' if line.get('value', 0) in (7, 9) else '0' for line in hex_lines)

# Pull more from expansion material: line gates already defined above
# Trigram zones available via corpus or the yijing-expansion reference

# ─── CORE I CHING CASTING ───

def fetch_iching(seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """I Ching hexagram from seed or hardware entropy.

    Lines use traditional values (6/7/8/9). Changing lines (6/9) noted.
    """
    if seed is None:
        try:
            result = subprocess.run(
                ["python3", os.path.expanduser("~/.hermes/tools/hardware_entropy.py"), "--bytes", "6"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                data = bytes.fromhex(result.stdout.strip())
            else:
                data = os.urandom(6)
        except Exception:
            try:
                data = os.urandom(6)
            except Exception:
                # robust local jitter fallback (same sources as hardware_entropy.py)
                import time, glob, os
                parts = []
                for p in glob.glob("/sys/class/thermal/thermal_zone*/temp"):
                    try: parts.append(open(p).read().strip().encode())
                    except: pass
                for p in glob.glob("/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq"):
                    try: parts.append(open(p).read().strip().encode())
                    except: pass
                for p in ["/proc/stat", "/proc/loadavg", "/proc/uptime", "/proc/interrupts", "/proc/meminfo"]:
                    try: parts.append(open(p, "rb").read(256))
                    except: pass
                for _ in range(128):
                    t0 = time.perf_counter_ns()
                    _ = sum(i*i for i in range(20))
                    t1 = time.perf_counter_ns()
                    parts.append(str(t1-t0).encode())
                parts.append(str(os.getpid()).encode())
                parts.append(str(time.time_ns()).encode())
                data = hashlib.sha256(b"".join(parts)).digest()[:6]
    else:
        data = hashlib.sha256(str(seed).encode()).digest()[:6]

    hexagram = []
    for i, b in enumerate(data):
        val = b % 4
        if val == 0:
            hexagram.append({"pos": i + 1, "symbol": "--- ---", "value": 6, "changing": True})
        elif val == 1:
            hexagram.append({"pos": i + 1, "symbol": "-------", "value": 7, "changing": False})
        elif val == 2:
            hexagram.append({"pos": i + 1, "symbol": "--- ---", "value": 8, "changing": False})
        else:
            hexagram.append({"pos": i + 1, "symbol": "-------", "value": 9, "changing": True})
    return hexagram

def cast_yarrow_lines(seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """Authentic yarrow probabilities from yijing-expansion-v1.1.md.

    6: 1/16, 7: 5/16, 8: 7/16, 9: 3/16
    """
    import random
    if seed is not None:
        # deterministic from seed
        seed_int = int(hashlib.sha256(str(seed).encode()).hexdigest()[:16], 16)
        random.seed(seed_int)
    else:
        random.seed()  # system entropy

    # cumulative for fast choice
    intervals = [
        (0.0, 1/16, 6),
        (1/16, 6/16, 7),
        (6/16, 13/16, 8),
        (13/16, 1.0, 9),
    ]
    hexagram = []
    for pos in range(1, 7):
        r = random.random()
        for lo, hi, val in intervals:
            if lo <= r < hi:
                sym = "--- ---" if val in (6, 8) else "-------"
                hexagram.append({
                    "pos": pos,
                    "symbol": sym,
                    "value": val,
                    "changing": val in (6, 9)
                })
                break
    return hexagram

def enrich_iching(hexagram: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Add derived fields + numogram bridge + changing line details + judgments.

    Uses curated table + full corpus when available.
    """
    # Ensure maps are populated (load also triggers BINARY_TO_TRAD etc.)
    _ = load_hex_info(1)

    # Build binary string matching corpus (line 1 bottom = leftmost char)
    primary_bin = lines_to_binary_str(hexagram)

    # Get traditional hex number from corpus mapping (fixes previous bits+1 bug)
    hex_num = BINARY_TO_TRAD.get(primary_bin)
    if hex_num is None:
        # fallback (rare)
        bits = sum( (1 << i) for i, line in enumerate(hexagram) if line.get("value") in (7,9) )
        hex_num = bits + 1

    # Keep internal bit pattern for display
    bits = sum( (1 << i) for i, line in enumerate(hexagram) if line.get("value") in (7,9) )
    hex_val = bits

    # Canonical Method A (preferred) — now using correct traditional hex_num
    zone = 1 + (hex_num - 1) % 9
    if zone == 10:
        zone = 0

    total_value = sum(l["value"] for l in hexagram)
    dr_shadow = digital_root(total_value)

    primary_zone = zone
    g = get_gate(primary_zone)
    syz = get_syzygy(primary_zone)
    changing = [l["pos"] for l in hexagram if l.get("changing")]

    # Prefer curated data
    curated = CURATED_HEX_MAP.get(hex_num, {})
    if curated and curated.get("zone") is not None:
        try:
            primary_zone = int(curated["zone"])
            g = get_gate(primary_zone)
            syz = get_syzygy(primary_zone)
        except Exception:
            pass

    demon = demon_from_zones(primary_zone, syz)
    if demon == "Unknown" and hex_num in CURATED_HEX_MAP:
        demon = CURATED_HEX_MAP[hex_num].get("demon", demon)

    # Line details + relating hex (flip only the changing positions in the binary str)
    relating_num = None
    relating_name = None
    line_details = []
    if changing:
        rel_list = list(primary_bin)
        for pos in changing:
            idx = pos - 1  # 0-based for line 1 at left
            if 0 <= idx < len(rel_list):
                oldc = rel_list[idx]
                rel_list[idx] = '0' if oldc == '1' else '1'
            line = next((l for l in hexagram if l["pos"] == pos), {})
            old = line.get("value")
            newv = 7 if old == 6 else 8
            gate = LINE_GATES.get(pos, "")
            line_details.append({
                "pos": pos,
                "old": old,
                "new": newv,
                "gate": gate,
                "symbol_old": line.get("symbol", "")
            })
        rel_bin = ''.join(rel_list)
        relating_num = BINARY_TO_TRAD.get(rel_bin)
        if relating_num:
            relating_name = get_hex_name(relating_num)

    zdisp = zone_display(primary_zone)
    note = curated.get("note") or "Hexagram kernel projection into the Time-Circuit / numogram rotor."
    insight = curated.get("insight")

    # Pull judgment etc from corpus (also loads the maps)
    hex_info = load_hex_info(hex_num)

    result = {
        "hexagram": hexagram,
        "hex_val": hex_val,
        "hex_num": hex_num,
        "king_wen": hex_info.get("name") or curated.get("name", f"Hexagram {hex_num}"),
        "total_value": total_value,
        "changing_lines": changing,
        "numogram_zone": primary_zone,
        "numogram_zone_display": zdisp,
        "numogram_gate": g,
        "numogram_syzygy": f"{primary_zone}::{syz}",
        "numogram_demon": demon if demon != "Unknown" else None,
        "alt_dr_shadow": dr_shadow,
        "curated_note": note,
        "curated_insight": insight,
        "mapping_note": "curated + canonical DR (Method A) + tianmu corpus",
        "judgment": hex_info.get("judgment"),
        "relating_hex": relating_num,
        "relating_name": relating_name,
        "line_details": line_details,
        "primary_binary": primary_bin,
    }
    return result

def cast_iching(seed: Optional[int] = None, source: str = "hardware", use_yarrow: bool = False) -> Dict[str, Any]:
    """High-level cast."""
    if use_yarrow or source == "yarrow":
        hexagram = cast_yarrow_lines(seed)
        src = f"yarrow:{seed}" if seed is not None else "yarrow"
    else:
        hexagram = fetch_iching(seed)
        src = source if seed is None else f"seed:{seed}"
    enriched = enrich_iching(hexagram)
    enriched["source"] = src
    return enriched

# ─── PRETTY PRINTING ───

def format_iching(ich: Dict[str, Any], compact: bool = False, full: bool = False) -> str:
    lines = []
    lines.append("══════════════════════════════════════")
    lines.append("  I CHING FROM NUMOGRAM ENTROPY")
    lines.append("══════════════════════════════════════")
    lines.append("")
    lines.append(f"  Source: {ich.get('source', 'manual')}")
    kw = ich.get("king_wen", f"Hexagram {ich['hex_num']}")
    title = f"{ich['hex_num']} — {kw}" if "Hexagram" not in kw else f"{ich['hex_num']}"
    lines.append(f"  Hexagram: {title}")

    jud = ich.get("judgment")
    if jud:
        if full:
            lines.append(f"  Judgment: {jud}")
        else:
            short = jud if len(jud) <= 105 else jud[:102] + "..."
            lines.append(f"  Judgment: {short}")

    lines.append(f"  Value sum: {ich['total_value']}  (pattern bits {ich['hex_val']})")
    lines.append("")

    # Visual hexagram: printed from top (Line 6) to bottom (Line 1) so the text block
    # looks like a traditional hexagram diagram (top of page = top of hexagram).
    # Numbering convention (per lines.md): Line 1 = bottom (foundation), Line 6 = top.
    # Internal storage: hexagram[0] = Line 1 (bottom), hexagram[5] = Line 6 (top).
    # This matches the previous coin oracles' line list convention (index 0 = first line = bottom).
    for pos in range(6, 0, -1):
        line = next((l for l in ich["hexagram"] if l["pos"] == pos), {})
        ch = " (changing)" if line.get("changing") else ""
        lines.append(f"  Line {pos}: {line.get('symbol', '???')}{ch}")

    # Compact visual hexagram figure (top to bottom), using symbols adapted from
    # previous Grok-made coin oracles in raw/coin/ for nicer appearance.
    sym_map = {
        6: "━━━ ● ━━━",   # old yin (changing)
        7: "━━━━━━━━━",   # young yang (stable)
        8: "━━━   ━━━",   # young yin (stable)
        9: "━━━━━━━━━ ○", # old yang (changing)
    }
    lines.append("")
    lines.append("  Hexagram figure (inverted for traditional visual appearance):")
    figure_syms = []
    for pos in range(6, 0, -1):
        line = next((l for l in ich["hexagram"] if l["pos"] == pos), {})
        val = line.get("value", 7)
        s = sym_map.get(val, "?????????")
        figure_syms.append(s)
    # Invert the symbol stack visually so hex like 60/Jie appears correctly
    # instead of looking like its inverse 59/Huan. Matches user request for visual invert.
    for s in reversed(figure_syms):
        lines.append(f"    {s}")

    # If there are changing lines, also show the full relating hexagram figure (inverted)
    if ch_lines:
        lines.append("")
        lines.append("  Relating hexagram figure (inverted for traditional visual appearance):")
        rel_figure_syms = []
        for pos in range(6, 0, -1):
            line = next((l for l in ich["hexagram"] if l["pos"] == pos), {})
            val = line.get("value", 7)
            if pos in ch_lines:
                if val == 6:
                    val = 7
                elif val == 9:
                    val = 8
            s = sym_map.get(val, "?????????")
            rel_figure_syms.append(s)
        for s in reversed(rel_figure_syms):
            lines.append(f"    {s}")

    ch_lines = ich.get("changing_lines", [])
    if ch_lines:
        lines.append(f"  Changing lines: {ch_lines}")
    else:
        lines.append("  No changing lines (static).")

    # Relating hex + per-line details
    if ch_lines:
        rel = ich.get("relating_hex")
        rel_name = ich.get("relating_name", "")
        if rel:
            lines.append(f"  → Relating hexagram: {rel} — {rel_name}")
        for ld in ich.get("line_details", []):
            g = f"  {ld.get('gate','')}" if ld.get("gate") else ""
            lines.append(f"    Line {ld['pos']}: {ld['old']} → {ld['new']}{g}")

    lines.append("")
    z = ich["numogram_zone"]
    lines.append(f"  Numogram shadow: Zone {z} — {ich['numogram_zone_display']}")
    lines.append(f"    Syzygy {ich['numogram_syzygy']}  Gate Gt-{ich['numogram_gate']}")
    if ich.get("numogram_demon"):
        lines.append(f"    Carrier demon: {ich['numogram_demon']}")
    if ich.get("curated_note"):
        lines.append(f"    Note: {ich['curated_note']}")
    if ich.get("curated_insight"):
        lines.append(f"    Changing-line insight: {ich['curated_insight']}")
    lines.append(f"  ({ich.get('mapping_note', '')}; alt DR shadow zone {ich.get('alt_dr_shadow')})")

    if full and jud:
        lines.append("")
        lines.append("  [Full Judgment]")
        lines.append(f"  {jud}")

    lines.append("")
    lines.append("══════════════════════════════════════")
    return "\n".join(lines)

# ─── CLI ───

def main(argv: Optional[List[str]] = None):
    args = argv or sys.argv[1:]
    seed = None
    do_json = "--json" in args
    use_cast = "--cast" in args
    use_yarrow = use_cast  # default for --cast is yarrow

    if "--seed" in args:
        try:
            idx = args.index("--seed")
            seed = int(args[idx + 1])
        except Exception:
            pass

    if use_cast:
        # --cast mode (yarrow simulation). --coins for alternative if wanted later
        ich = cast_iching(seed=seed, source="yarrow" if use_yarrow else "hardware", use_yarrow=True)
    else:
        # traditional --iching path (entropy or seed)
        source = "hardware"
        if seed is not None:
            source = f"seed:{seed}"
        if "--hardware" in args:
            seed = None
            source = "hardware"
        ich = cast_iching(seed=seed, source=source)

    do_full = "--full" in args

    if do_json:
        print(json.dumps(ich, indent=2))
        return

    print(format_iching(ich, full=do_full))

    # usage hint
    if not any(x in args for x in ("--iching", "--cast", "--seed", "--json", "--hardware", "--full")):
        print("\n(Use --iching, --cast, or --seed N. Add --full for complete judgment text. --json for machine output.)")

if __name__ == "__main__":
    main()
