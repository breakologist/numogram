#!/usr/bin/env python3
"""
taixuan.py — Standalone T'ai Hsuan Ching (Tai Xuan Jing) + Yuandong/Guanziming 27-Phase Companion

Ternary tetragrams (81) and related trigram-phase systems for mediation, Em-state, and numogram integration.

Extracted and expanded from oracle.py and visualizer-v7 (with new Yuandong Jing 27-phase diagram from Guanziming / Reddit translation).

Core:
- Cast 1 or 2 tetragrams (0–80). --single for one tetragram (great for 9 appraisals).
- Randomness sources (no --seed): hardware_entropy.py (or local copy) → os.urandom → local jitter collector.
  With --seed: deterministic.
- Unicode support (--unicode) using Tai Xuan monograms for compact rendering.
- Full ternary lines + 81 names + Em/mediation + hierarchy + demon lookup.
- 9 appraisals structure (stubbed; full in Nylan) — shown in --single --full.
- 27 Yuandong phases as the 27 departments.
- JSON export suitable for visualizer wiring.

Usage:
  python3 taixuan.py --taixuan
  python3 taixuan.py --taixuan --seed 192855
  python3 taixuan.py --taixuan --full
  python3 taixuan.py --cast --json
  python3 taixuan.py --single          # single tetragram (better for 9 appraisals)
  python3 taixuan.py --single --full --unicode
  python3 taixuan.py --phases          # list the 27 Yuandong phases
  python3 taixuan.py --phase            # cast one 27-phase

Integrates with numogram zones (digital root), syzygies (demon carriers), and the explicit "Man as mediator" (Em) for alchemical / agentic / hyperstitional work.

Companion to iching.py (binary Time-Circuit) — this is the ternary mediator layer.

Sources: taixuanjingrok.md, visualizer-v7.html, Yuandong Jing diagram + translation, Nylan/Walters etc.

[review notes 2026-10-17, code changes marked "# [fix]"]
- Sourced: three line types unbroken / once-broken / twice-broken = Heaven / Earth / Man
  (Liu, JPACT 4, 2021: https://hilo.hawaii.edu/jpact/issues/volume-4-2021/taixuan-jing.php);
  hierarchy 3 fang / 9 zhou / 27 bu / 81 jia (same source; chinaknowledge.org Taixuanjing page).
- NOT in those sources (repo-internal / speculative, kept as features): the label "Em",
  the Sulfur/Salt/Mercury alchemy layer, the nine appraisal phase names, quasiphonic names.
- The 27 "Yuandong" phases are the 27 figures of the Dongji zhenjing 洞極真經
  (Gujin tushu title 擬元洞極真經, "imitating the [Tai]xuan"), attributed to Guan Lang 關朗
  (courtesy name Ziming 子明), author uncertain per Hu Yigui. Three ji: 生 birth (Luoshu 1,4,7),
  育 nurture (2,5,8), 資 material (3,6,9), nine figures each = 27.
  https://www.eee-learning.com/book/4933 ; https://www.eee-learning.com/book/5344
  Identifying them with the Tai Xuan's 27 departments (bu) is this tool's own mapping.
"""

import sys
import os
import hashlib
import subprocess
import json
from typing import Optional, Dict, List, Any, Tuple

# ─── THREE STATES (San Cai / Tria Prima) ───
HEAVEN = 0  # Yang / solid / unbroken — active, initiating (Sulfur)
EARTH = 1   # Yin / once-broken — receptive, structuring (Salt)
MAN = 2     # Em / twice-broken (triple-dash) — mediator, transformer (Mercury)

STATE_NAMES = {HEAVEN: "Heaven", EARTH: "Earth", MAN: "Man/Em (mediator)"}
STATE_SYMBOLS = {
    HEAVEN: "━━━━━━━",      # solid
    EARTH: "━━━   ━━━",     # broken
    MAN:   "━━ ━━ ━━",      # [fix] twice-broken (was "━━━ ● ━━━", the I Ching old-yin mark)
}

STATE_UNICODE = {
    HEAVEN: "⚊",   # Heaven (unbroken)
    EARTH: "⚋",   # Earth (once-broken)
    MAN: "𝌀",     # Man/Em (twice-broken; Unicode names U+1D300 "MONOGRAM FOR EARTH")
}

# ─── YUANDONG JING / GUANZIMING 27-PHASE TRIGRAM SYSTEM ───
# [fix] "zh" added from the Dongji zhenjing sequence 生萌息華茂止安燠實 / 育和塞作煥幾抑冥通 /
# 資用達興紊悖靜平序 (eee-learning.com/book/4933; the source's own 次為 order puts 資 before 育).
# The "formula" strings are UNVERIFIED: only 20 of 27 are distinct and several disagree with
# the group (e.g. #4, #6-#8 are in the 生 group but start "One nurture/material").
# From the provided diagram + translation (27 phases, 3^3, birth/nurture/material).
# These are the "27 departments (pu)" in the Tai Xuan cosmological hierarchy
# (3 regions/fang → 9 provinces/chou → 27 departments/pu → 81 families/jia).
# Each department corresponds to 3 tetragram "families".

YUANDONG_PHASES: List[Dict[str, Any]] = [
    {"num": 1, "zh": "生", "name": "Birth", "formula": "One birth, two births, three births"},
    {"num": 2, "zh": "萌", "name": "Sprout", "formula": "One birth, two nurtures, three nurtures"},
    {"num": 3, "zh": "息", "name": "Breath", "formula": "One birth, two materials, three materials"},
    {"num": 4, "zh": "華", "name": "Essence", "formula": "One nurture, two births, three births", "gloss_note": "華 = flowering"},
    {"num": 5, "zh": "茂", "name": "Profuse", "formula": "One birth, two materials, three births"},
    {"num": 6, "zh": "止", "name": "End", "formula": "One nurture, two materials, three nurtures"},
    {"num": 7, "zh": "安", "name": "Quiet", "formula": "One nurture, two nurtures, three births"},
    {"num": 8, "zh": "燠", "name": "Warmth", "formula": "One material, two births, three births", "gloss_note": "[fix] 燠 = warmth (was \"Scatter\")"},
    {"num": 9, "zh": "實", "name": "Reality", "formula": "One birth, two nurtures, three births"},
    {"num": 10, "zh": "育", "name": "Nurture", "formula": "One nurture, two nurtures, three nurtures"},
    {"num": 11, "zh": "和", "name": "Harmony", "formula": "One nurture, two nurtures, three births"},
    {"num": 12, "zh": "塞", "name": "Obstruction", "formula": "One material, two nurtures, three nurtures"},
    {"num": 13, "zh": "作", "name": "Work", "formula": "One material, two materials, three births"},
    {"num": 14, "zh": "煥", "name": "Brilliance", "formula": "One nurture, two births, three births", "gloss_note": "[fix] 煥 = brilliance; variant 渙 = scatter (was \"Warmth\")"},
    {"num": 15, "zh": "幾", "name": "Some", "formula": "One nurture, two births, three materials", "gloss_note": "幾 = incipience / subtle onset"},
    {"num": 16, "zh": "抑", "name": "Suppression", "formula": "One birth, two materials, three materials"},
    {"num": 17, "zh": "冥", "name": "Dark", "formula": "One nurture, two materials, three materials"},
    {"num": 18, "zh": "通", "name": "Through", "formula": "One birth, two materials, three materials"},
    {"num": 19, "zh": "資", "name": "Material", "formula": "One material, two materials, three materials"},
    {"num": 20, "zh": "用", "name": "Use", "formula": "One material, two births, three materials"},
    {"num": 21, "zh": "達", "name": "Smooth", "formula": "One birth, two births, three materials"},
    {"num": 22, "zh": "興", "name": "Prosperous", "formula": "One birth, two births, three nurtures"},
    {"num": 23, "zh": "紊", "name": "Disorderly", "formula": "One material, two births, three births"},
    {"num": 24, "zh": "悖", "name": "Contrary", "formula": "One material, two births, three nurtures"},
    {"num": 25, "zh": "靜", "name": "Tranquil", "formula": "One nurture, two nurtures, three nurtures"},
    {"num": 26, "zh": "平", "name": "Even", "formula": "One material, two materials, three nurtures"},
    {"num": 27, "zh": "序", "name": "Order", "formula": "One material, two materials, three births"},
]

# ─── 81 TETRAGRAM NAMES (from Nylan, The Canon of Supreme Mystery) ───
# Standard "heads" (shou). Index 0-80.
TETRAGRAM_NAMES = [
    "Centre", "Full Circle", "Mired", "Barrier", "Keeping Small", "Contrariety", "Ascent", "Opposition", "Branching out",
    "Defectiveness or Distortion", "Divergence", "Youthfulness", "Increase", "Penetration", "Reach", "Contact", "Holding Back", "Waiting",
    "Following", "Advance", "Release", "Resistance", "Ease", "Joy", "Contention", "Endeavour", "Duties",
    "Change", "Decisiveness", "Bold Resolution", "Packing", "Legion", "Closeness", "Kinship", "Gathering", "Strength",
    "Purity", "Fullness", "Residence", "Law or Model", "Response", "Going to Meet", "Encounters", "Stove", "Greatness",
    "Enlargement", "Pattern", "Ritual", "Flight", "Vastness or Wasting", "Constancy", "Measure", "Eternity", "Unity",
    "Diminishment", "Closed Mouth", "Guardedness", "Gathering in", "Massing", "Accumulation", "Embellishment", "Doubt", "Watch",
    "Sinking", "Inner", "Departure", "Darkening", "Dimming", "Exhaustion", "Severance", "Stoppage", "Hardness",
    "Completion", "Closure", "Failure", "Aggravation", "Compliance", "On the verge", "Difficulties", "Labouring", "Fostering"
]

def get_yuandong_phase(idx: int) -> Dict[str, Any]:
    """1-27 -> phase data (a copy). [fix] Index 0 is treated as 0-based for backward
    compatibility only; callers below pass 1-27."""
    if 1 <= idx <= 27:
        return dict(YUANDONG_PHASES[idx-1])
    if idx == 0:
        return dict(YUANDONG_PHASES[0])
    return {"num": idx, "name": f"Phase {idx}", "formula": ""}

def get_tetragram_hierarchy(n: int) -> Dict[str, Any]:
    """Decompose tetragram n (0-80) into the Tai Xuan cosmological hierarchy.
    81 families (jia) grouped under 27 departments (pu), etc.
    The 27 Yuandong phases correspond to the 27 departments (pu).
    """
    # n in base 3 gives the 4 "digits" for the 4 levels (fang/chou/bu/jia or equivalent)
    digits = []
    tmp = n
    for _ in range(4):
        digits.append(tmp % 3)
        tmp //= 3
    # digits[0] = lowest (jia/family), digits[3] = highest (fang/region)
    department = n // 3   # 0-26
    family = n % 3
    phase = get_yuandong_phase(department + 1)  # 1-27
    return {
        "tetragram": n,
        "name": TETRAGRAM_NAMES[n] if n < len(TETRAGRAM_NAMES) else f"Tetragram {n}",
        "department": department + 1,  # 1-27 pu
        "family_in_dept": family,     # 0-2 within dept (3 families per)
        "phase": phase,
        "base3_digits": digits[::-1],  # highest to lowest for clarity
        "region_fang": digits[3],
        "province_chou": digits[2],
        "department_bu": digits[1],
        "family_jia": digits[0],
    }

def cast_yuandong_phase(seed: Optional[int] = None) -> Dict[str, Any]:
    """Cast a single 27-phase using ternary (3 positions)."""
    # [fix] old cast: 0-26 index fed to a 1-27 lookup, so index 0 and 1 both gave #1 and
    # #27 never appeared; it also wrote into the shared table. Unseeded now uses _get_entropy.
    h = hashlib.sha256(str(seed).encode()).digest() if seed is not None else _get_entropy(4)
    phase_idx = int.from_bytes(h[:4], "big") % 27          # 0-26, uniform to 1e-9
    trits = [phase_idx // 9, phase_idx // 3 % 3, phase_idx % 3]
    phase = get_yuandong_phase(phase_idx + 1)
    phase["trits"] = trits
    phase["seed"] = seed
    return phase

# ─── CORE TAI XUAN (81 Tetragrams) ───

def _get_entropy(nbytes: int) -> bytes:
    """Get nbytes of entropy.
    Priority (inspired by numogram-entropy-source + domain/entropy-sources + wiki/hardware-entropy.md):
    1. ~/.hermes/tools/hardware_entropy.py (the project's 12-source collector: thermals, CPU freq jitter,
       GPU via nvidia-smi, /proc/*, timing jitter 256 samples, fsync, kernel entropy pool, etc.)
    2. os.urandom (strong system CSPRNG)
    3. Pure-local collector (thermals + /proc + perf_counter timing jitter + pid + monotonic) hashed.
       This is drawn directly from the sources you pointed to (numogram-entropy-source SKILL.md lists
       the exact 12 sources, hardware-entropy.md details /sys and /proc interfaces, domain skill has
       the external ones as optional supplements).
    """
    if nbytes <= 0:
        return b''

    # 1. The canonical hardware_entropy script (supports --bytes N, returns hex)
    #    (from hardware-entropy skill + external sources in domain/entropy-sources)
    #    Also checks alongside this module for the skill-tree copy.
    try:
        candidates = [
            os.path.expanduser("~/.hermes/tools/hardware_entropy.py"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "hardware_entropy.py"),
        ]
        for tool in candidates:
            if os.path.exists(tool):
                result = subprocess.run(
                    ["python3", tool, "--bytes", str(nbytes)],
                    capture_output=True, text=True, timeout=8
                )
                if result.returncode == 0 and result.stdout.strip():
                    hexdata = result.stdout.strip()
                    if hexdata.startswith('{'):
                        import json
                        j = json.loads(hexdata)
                        hexdata = j.get('hex') or j.get('bytes') or ''
                    return bytes.fromhex(hexdata)[:nbytes]
    except Exception:
        pass

    # 1b. Try the numogram-entropy-source package CLI if present (it does the full
    #     12-source + SHA + numogram traversal dance described in its SKILL.md)
    try:
        cli = os.path.expanduser("~/numogram-entropy/.venv/bin/numogram-entropy")
        if os.path.exists(cli):
            # Ask for a stream and take raw bytes from it; fall back to --zone etc.
            res = subprocess.run([cli, "--stream", "1"], capture_output=True, text=True, timeout=6)
            if res.returncode == 0 and res.stdout.strip():
                # crude extraction of numeric entropy from output
                import re
                nums = [int(x) for x in re.findall(r'\b(\d{3,})\b', res.stdout)][:nbytes]
                if nums:
                    return bytes(nums[:nbytes]).ljust(nbytes, b'\0')[:nbytes]
    except Exception:
        pass

    # 2. Strong system randomness
    try:
        return os.urandom(nbytes)
    except Exception:
        pass

    # 3. Local collector inspired by the skills (no external deps)
    import time, glob  # [fix] no local `import os` (it shadowed the module: steps 1-2 never ran)
    parts = []
    # thermals (3 zones)
    for p in glob.glob('/sys/class/thermal/thermal_zone*/temp'):
        try:
            parts.append(open(p).read().strip().encode())
        except Exception:
            pass
    # cpu freq jitter (4 cores)
    for p in glob.glob('/sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq'):
        try:
            parts.append(open(p).read().strip().encode())
        except Exception:
            pass
    # /proc noise sources listed in the skill
    for p in ['/proc/stat', '/proc/loadavg', '/proc/uptime', '/proc/interrupts',
              '/proc/diskstats', '/proc/net/dev', '/proc/meminfo', '/proc/vmstat',
              '/proc/sys/kernel/random/entropy_avail']:
        try:
            with open(p, 'rb') as f:
                parts.append(f.read(256))
        except Exception:
            pass
    # timing jitter (256 samples, as in the skill)
    for _ in range(256):
        t0 = time.perf_counter_ns()
        _ = sum(i * i for i in range(20))  # tiny deterministic work
        t1 = time.perf_counter_ns()
        parts.append(str(t1 - t0).encode())
    # fsync timing (storage jitter)
    try:
        fd = os.open('/tmp', os.O_RDONLY)
        for _ in range(16):
            t0 = time.perf_counter_ns()
            os.fsync(fd)
            t1 = time.perf_counter_ns()
            parts.append(str(t1 - t0).encode())
        os.close(fd)
    except Exception:
        pass
    # pid + coarse time for extra mixing
    parts.append(str(os.getpid()).encode())
    parts.append(str(time.time_ns()).encode())
    parts.append(str(time.monotonic_ns()).encode())

    blob = hashlib.sha256(b''.join(parts)).digest()
    return blob[:nbytes]


def fetch_taixuan(seed: Optional[int] = None) -> int:
    """One tetragram index 0-80.
    - With --seed: deterministic from SHA256(seed)
    - No seed: from hardware_entropy, os.urandom, or mixed time fallback.
    """
    if seed is not None:
        data = hashlib.sha256(str(seed).encode()).digest()[:4]
    else:
        data = _get_entropy(4)
    return int.from_bytes(data, "big") % 81


def cast_two_taixuan(seed: Optional[int] = None) -> Tuple[int, int]:
    """Two tetragrams.
    When no seed: a single entropy call is split so upper and lower are different.
    """
    if seed is not None:
        h = hashlib.sha256(str(seed).encode()).digest()
        a = int.from_bytes(h[:4], "big") % 81
        b = int.from_bytes(h[4:8], "big") % 81
        return a, b

    # One good entropy source → two values
    blob = _get_entropy(8)
    a = int.from_bytes(blob[:4], "big") % 81
    b = int.from_bytes(blob[4:8], "big") % 81

    # Extremely unlikely collision, but make them different
    if a == b:
        b = (b + 1) % 81
    return a, b

def represent_tetragram(n: int) -> List[int]:
    """0-80 -> [bottom, ..., top] where 0=Heaven, 1=Earth, 2=Man/Em.
    Matches visualizer-v7 convention (lines[0]=bottom).
    """
    lines = []
    for _ in range(4):
        lines.append(n % 3)
        n //= 3
    return lines  # [0]=bottom ... [3]=top

def render_tetragram(n: int, label: str = "", use_unicode: bool = False) -> str:
    """Pretty text rendering of one tetragram.
    use_unicode=True uses the Tai Xuan Jing monogram symbols for compactness.
    """
    states = represent_tetragram(n)
    lines_out = []
    syms = STATE_UNICODE if use_unicode else STATE_SYMBOLS
    for i in range(3, -1, -1):  # top to bottom for visual
        s = states[i]
        sym = syms.get(s, "???")
        name = STATE_NAMES.get(s, "")
        lines_out.append(f"  {sym}  {name}")
    title = f"{label} #{n + 1}" if label else f"Tetragram #{n + 1}"  # [fix] head number
    return f"{title}\n" + "\n".join(lines_out)

ZONE_FROM = "value"   # [fix] default = line values (same convention as iching.py fuxi); --zone-from number


def taixuan_zone(n: int, zone_from: Optional[str] = None) -> int:
    """Tetragram index 0-80 -> decimal zone.
    "value" (default, unchanged): digital root of the base-3 line value (= index), 0 only for
    Centre. Same convention as iching.py's default "fuxi" zone (binary weights 1,2,4,...,
    here ternary 1,3,9,27): all-heaven/all-yin figure -> 0, other multiples of 9 -> 9.
    "number": digital root of the head number 1-81 (Centre = 1); nine heads per zone 1-9.
    """
    if (zone_from or ZONE_FROM) == "number":
        n = n + 1
    if n == 0:
        return 0
    while n >= 10:
        n = sum(int(d) for d in str(n))
    return n

def get_em_count(tetra: int) -> int:
    """Number of Man/Em (2) lines in the tetragram (0-4)."""
    return sum(1 for s in represent_tetragram(tetra) if s == MAN)

def enrich_taixuan(upper: int, lower: int) -> Dict[str, Any]:
    """Rich reading for a two-tetragram cast. Includes names, Em/mediation, and hierarchy (27 departments etc.)."""
    zu = taixuan_zone(upper)
    zl = taixuan_zone(lower)
    syz = f"{zu}::{zl}"
    is_syzygy = (zu + zl) == 9
    demon = demon_from_zones(zu, zl) if is_syzygy else None
    if demon is None and NETSPAN:      # [fix] opt-in: --netspan names every distinct pair
        demon = netspan_demon(zu, zl)

    emu = get_em_count(upper)
    eml = get_em_count(lower)
    total_em = emu + eml
    mediation = "pure polarity" if total_em == 0 else (
        "strong mediator / Mercury state" if total_em >= 4 else
        f"moderate mediation ({total_em}/8 Em lines)"
    )

    upper_h = get_tetragram_hierarchy(upper)
    lower_h = get_tetragram_hierarchy(lower)

    return {
        "upper": upper,
        "lower": lower,
        "upper_zone": zu,
        "lower_zone": zl,
        "upper_name": upper_h["name"],
        "lower_name": lower_h["name"],
        "syzygy": syz,
        "is_syzygy": is_syzygy,
        "demon": demon,
        "em_upper": emu,
        "em_lower": eml,
        "total_em": total_em,
        "mediation_level": mediation,
        "upper_hierarchy": upper_h,
        "lower_hierarchy": lower_h,
        "upper_number": upper + 1,       # [fix] head number 1-81 (names are indexed 0-80)
        "lower_number": lower + 1,
        "zone_from": ZONE_FROM,
        "upper_render": represent_tetragram(upper),
        "lower_render": represent_tetragram(lower),
    }

# Demon map (shared with oracle / iching for consistency)
# [fix] Ummnu (Om, Omni, Amen, Omen) is Mesh-44, net-span 9::8, not an alias of Uttunul (9::0)
# (http://www.ccru.net/digithype/pandemonium.htm).
TAIXUAN_DEMON_MAP = {
    (0,9): "Uttunul", (9,0): "Uttunul",
    (1,8): "Murrumur", (8,1): "Murrumur",
    (2,7): "Oddubb", (7,2): "Oddubb",
    (3,6): "Djynxx", (6,3): "Djynxx",
    (4,5): "Katak", (5,4): "Katak",
}

def demon_from_zones(a: int, b: int) -> str:
    return TAIXUAN_DEMON_MAP.get((a, b), "Unknown")


# [fix] Full 45-demon net-span lookup, ordered by mesh number (mesh = T(hi-1) + lo).
# Names as in http://www.ccru.net/digithype/pandemonium.htm (via repo pandemonium-matrix.md).
NETSPAN_DEMONS = [
    "Lurgo", "Duoddod", "Doogu", "Ixix", "Ixigool", "Ixidod", "Krako", "Sukugool", "Skoodu",
    "Skarkix", "Tokhatto", "Tukkamu", "Kuttadid", "Tikkitix", "Katak", "Tchu", "Djungo",
    "Djuddha", "Djynxx", "Tchakki", "Tchattuk", "Puppo", "Bubbamu", "Oddubb", "Pabbakis",
    "Ababbatok", "Papatakoo", "Bobobja", "Minommo", "Murrumur", "Nammamad", "Mummumix",
    "Numko", "Muntuk", "Mommoljo", "Mombbo", "Uttunul", "Tutagool", "Unnunddo", "Ununuttix",
    "Ununak", "Tukutu", "Unnutchi", "Nuttubab", "Ummnu",
]


def netspan_demon(a: int, b: int) -> Optional[str]:
    """Demon for any pair of distinct zones 0-9 (None for a == b)."""
    hi, lo = max(a, b), min(a, b)
    return None if hi == lo else NETSPAN_DEMONS[hi * (hi - 1) // 2 + lo]

# Single tetragram -> primary demon via its zone (from tai-hsuan-ching-demons.md)
ZONE_PRIMARY_DEMON = {
    0: "Uttunul", 1: "Murrumur", 2: "Oddubb", 3: "Djynxx",
    4: "Katak", 5: "Katak", 6: "Djynxx", 7: "Oddubb",
    8: "Murrumur", 9: "Uttunul",
}

def get_appraisals(tetra_num: int, which: Optional[int] = None) -> List[str]:
    """Return the 9 appraisals (zan/tsan) structure for a tetragram.
    Full texts in Nylan's Canon of Supreme Mystery.
    Phases keyed to time-of-day or developmental stages.
    Stubs with hints; expand with actual translations as needed.
    """
    phase_names = [
        "Center", "Ascent", "Flourishing", "Compliance", "Maturity",
        "Decline", "Crisis", "Resolution", "Return"
    ]
    phase_hints = [
        "The situation in its central, balanced state.",
        "Rising energy, beginning of movement.",
        "Peak development, full expression.",
        "Adaptation and following the flow.",
        "Consolidation and stability.",
        "Waning, preparation for change.",
        "Point of tension or turning.",
        "Integration after transformation.",
        "Return to source, completion of cycle."
    ]
    apps = [f"Appraisal {i+1} ({phase_names[i]}): {phase_hints[i]} [full in Nylan]" for i in range(9)]
    if which is not None and 1 <= which <= 9:
        return [apps[which-1]]
    return apps

def em_profile(tetragrams: List[int]) -> Dict[str, Any]:
    """Compute Em-state profile / stats for one or more tetragrams.
    Useful for batch analysis, Em-state research, or --em-stats.
    Returns counts, total, mediation category, etc.
    """
    counts = [get_em_count(t) for t in tetragrams]
    total = sum(counts)
    avg = total / len(counts) if counts else 0
    max_em = max(counts) if counts else 0
    if total == 0:
        med_level = "pure polarity (no mediation)"
    elif total >= 4:
        med_level = "strong mediator / Mercury state"
    else:
        med_level = f"moderate mediation ({total}/8 Em lines across cast)"
    return {
        "tetragrams": tetragrams,
        "em_counts": counts,
        "total_em": total,
        "avg_em": round(avg, 2),
        "max_em": max_em,
        "mediation_level": med_level,
        "num_tetragrams": len(tetragrams),
    }

def alchemy_summary(data: Dict[str, Any]) -> str:
    """Alchemy layer: Heaven (Sulfur/active), Earth (Salt/receptive), Man/Em (Mercury/mediator).
    Inspired by tria prima and Em-state work.
    """
    if data.get("mode") == "single":
        em = data.get("em_count", 0)
        if em == 0:
            return "Pure polarity — Sulfur (Heaven) or Salt (Earth) dominance, no mediation."
        elif em >= 3:
            return "Strong Mercury (Man/Em) — dissolution, recombination, agentic transformation phase."
        else:
            return "Mixed — active (Sulfur) and receptive (Salt) with emerging Mercury mediation."
    else:
        total_em = data.get("total_em", 0)
        if total_em >= 4:
            return "Strong Mercury mediation across the pair — alchemical work: solve et coagula."
        elif total_em > 0:
            return "Partial mediation — the tetragram pair invites intervention/reconciliation."
        return "Polarity dominant — classic Sulfur/Salt tension without active Mercury."

def taixuan_demon_quasiphonic(zone_a: int, zone_b: int) -> str:
    """Future 'true' Taixuan-specific demon name generator.
    Modelled on ccru-zone-voice.md quasiphonic combinatorial (e.g. gl + ktt).
    Currently zone-particle based; extend with tetragram trit particles for true specificity
    (e.g. decompose 4 trits into phonemes, blend with syzygy).
    """
    zone_particles = {0:"eia",1:"gl",2:"dt",3:"zx",4:"skr",5:"ktt",6:"tch",7:"pb",8:"mnm",9:"tn"}
    p1 = zone_particles.get(zone_a % 10, "x")
    p2 = zone_particles.get(zone_b % 10, "x")
    # Simple blend; could be more sophisticated like base36
    return f"{p1}{p2}"  # e.g. "glktt" style for Katak etc.

NETSPAN = False   # [fix] set by --netspan

# ─── CAST + OUTPUT ───

def cast_taixuan(seed: Optional[int] = None, two: bool = True) -> Dict[str, Any]:
    if two:
        u, l = cast_two_taixuan(seed)
        enriched = enrich_taixuan(u, l)
        enriched["seed"] = seed
        enriched["mode"] = "two-tetragram"
        return enriched
    else:
        t = fetch_taixuan(seed)
        h = get_tetragram_hierarchy(t)
        return {
            "tetragram": t,
            "number": t + 1,                 # [fix]
            "zone_from": ZONE_FROM,
            "zone": taixuan_zone(t),
            "name": h["name"],
            "render": represent_tetragram(t),
            "em_count": get_em_count(t),
            "hierarchy": h,
            "demon": ZONE_PRIMARY_DEMON.get(taixuan_zone(t), "Unknown"),
            "appraisals": get_appraisals(t),
            "seed": seed,
            "mode": "single",
        }

def format_taixuan(data: Dict[str, Any], full: bool = False, use_unicode: bool = False) -> str:
    lines = []
    lines.append("══════════════════════════════════════")
    lines.append("  T'AI XUAN CHING ORACLE")
    lines.append("══════════════════════════════════════")
    lines.append("")

    if data.get("mode") == "two-tetragram":
        lines.append(f"  Seed: {data.get('seed', 'hardware')}")
        # [fix] show the head number (1-81); "#26 Duties" was index 26 = head 27 Duties
        lines.append(f"  Upper: #{data['upper'] + 1} {data.get('upper_name', '')} → Zone {data['upper_zone']}")
        lines.append(f"  Lower: #{data['lower'] + 1} {data.get('lower_name', '')} → Zone {data['lower_zone']}")
        lines.append(f"  Syzygies: {data['syzygy']}")
        if data.get("demon"):
            lines.append(f"  Net-span demon: {data['demon']}")
            lines.append(f"  Quasiphonic name sketch: {taixuan_demon_quasiphonic(data['upper_zone'], data['lower_zone'])}")
        else:
            # per tai-hsuan-ching-demons.md suggestion for ungoverned
            lines.append(f"  Cross-pairing (ungoverned) — under {data['upper_zone']}/{data['lower_zone']} influence")
            lines.append(f"  Quasiphonic sketch: {taixuan_demon_quasiphonic(data['upper_zone'], data['lower_zone'])}")
        lines.append(f"  Em count: upper {data['em_upper']} / lower {data['em_lower']} (total {data['total_em']})")
        lines.append(f"  Mediation: {data['mediation_level']}")
        lines.append(f"  Alchemy: {alchemy_summary(data)}")

        # Hierarchy (27 depts etc.)
        uh = data.get('upper_hierarchy', {})
        lh = data.get('lower_hierarchy', {})
        if uh:
            lines.append(f"  Upper dept: {uh.get('department')} ({uh.get('phase',{}).get('name','')}) family {uh.get('family_in_dept')}")
        if lh:
            lines.append(f"  Lower dept: {lh.get('department')} ({lh.get('phase',{}).get('name','')}) family {lh.get('family_in_dept')}")

        if full:
            lines.append("")
            lines.append("  Upper:")
            lines.append(render_tetragram(data['upper'], "UPPER", use_unicode=use_unicode))
            lines.append("  Lower:")
            lines.append(render_tetragram(data['lower'], "LOWER", use_unicode=use_unicode))
    else:
        # Single tetragram mode
        lines.append(f"  Tetragram: #{data['tetragram'] + 1} {data.get('name','')} → Zone {data['zone']}")  # [fix]
        lines.append(f"  Demon: {data.get('demon', 'Unknown')} (quasiphonic: {taixuan_demon_quasiphonic(data['zone'], data['zone'])})")
        lines.append(f"  Em lines: {data['em_count']}/4")
        lines.append(f"  Hierarchy: Dept {data['hierarchy']['department']} ({data['hierarchy']['phase']['name']}) family {data['hierarchy']['family_in_dept']}")
        lines.append(f"  Alchemy: {alchemy_summary(data)}")
        if full:
            lines.append("")
            lines.append(render_tetragram(data['tetragram'], use_unicode=use_unicode))
            lines.append("")
            lines.append("  9 Appraisals (zan/tsan — see Nylan for full text):")
            for app in data.get('appraisals', []):
                lines.append(f"    {app}")

    lines.append("")
    lines.append("══════════════════════════════════════")
    return "\n".join(lines)

# ─── CLI ───

def main(argv: Optional[List[str]] = None):
    global ZONE_FROM, NETSPAN
    args = sys.argv[1:] if argv is None else argv  # [fix]
    if "--zone-from" in args:
        ZONE_FROM = args[args.index("--zone-from") + 1]
        if ZONE_FROM not in ("value", "number"):
            print("--zone-from must be value or number"); sys.exit(2)
    NETSPAN = "--netspan" in args
    seed = None
    do_json = "--json" in args
    do_full = "--full" in args
    do_two = "--taixuan" in args or "--two" in args or not ("--single" in args)
    do_phase = "--phase" in args or "--phases" in args

    if "--seed" in args:
        try:
            idx = args.index("--seed")
            a = args[idx + 1]
            seed = int(a, 16) if a.lower().startswith("0x") else int(a)  # [fix] 0x-hex accepted
        except Exception:
            # [fix] used to fall back silently to a hardware cast
            print(f"--seed needs an integer (decimal or 0x-hex), got {args[idx + 1:idx + 2]}")
            sys.exit(2)

    if do_phase:
        if "--list" in args or "--phases" in args and "--cast" not in args:
            print("Yuandong Jing / Guanziming 27 Phases (from diagram + translation):")
            print("  (Dongji zhenjing 洞極真經; formula column unverified, see source notes)")
            for p in YUANDONG_PHASES:
                print(f"  {p['num']:2d}. {p.get('zh', '')} {p['name']}: {p['formula']}")
            return
        ph = cast_yuandong_phase(seed)
        print("══════════════════════════════════════")
        print("  YUANDONG JING — 27-PHASE CAST")
        print("══════════════════════════════════════")
        print(f"  Phase {ph['num']}: {ph.get('zh', '')} {ph['name']}")
        print(f"  Formula: {ph['formula']}")
        print(f"  Trits: {ph.get('trits')}")
        print("══════════════════════════════════════")
        return

    # --cast and --taixuan both request the classic two-tetragram oracle
    if "--cast" in args:
        do_two = True
    if "--single" in args or "--one" in args:
        do_two = False

    use_unicode = "--unicode" in args or "--uni" in args

    data = cast_taixuan(seed=seed, two=do_two)

    if "--em-stats" in args or "--em-profile" in args:
        # Batch-like Em stats for the current cast
        if data.get("mode") == "two-tetragram":
            tetras = [data["upper"], data["lower"]]
        else:
            tetras = [data["tetragram"]]
        profile = em_profile(tetras)
        print("Em-state Profile:")
        print(json.dumps(profile, indent=2))
        if do_json:
            return
        # fall through for normal output too

    if "--viz" in args or "--viz-json" in args:
        # Export for v7 visualizer taiHsuanPanel or similar
        if data.get("mode") == "two-tetragram":
            viz = {"upper": data["upper"], "lower": data["lower"], "seed": seed or "hardware"}
        else:
            viz = {"tetragram": data["tetragram"], "seed": seed or "hardware"}
        print(json.dumps(viz, indent=2))
        return

    if do_json:
        print(json.dumps(data, indent=2))
        return

    print(format_taixuan(data, full=do_full, use_unicode=use_unicode))

    if not any(x in args for x in ("--taixuan", "--cast", "--seed", "--json", "--full", "--phase", "--single", "--em-stats", "--viz")):
        print("\n(Use --taixuan/--cast for two, --single for one (appraisals). --em-stats/--em-profile for Em batch.")
        print(" --phase Yuandong27, --seed, --full, --json, --unicode/--uni, --viz/--viz-json for visualizer.")
        print("Hardware entropy preferred. See taixuanjingrok.md for demon quasiphonics, Em-stats, alchemy, appraisals.")

if __name__ == "__main__":
    main()
