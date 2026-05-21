#!/usr/bin/env python3
"""
numogram-base-explorer.py — Multi-base numogram construction and analysis.

Builds numograms in any base N (2-100), computes:
  - Zone tables with colors, quasiphonic particles, demon counts
  - Syzygy pairs (summing to N-1)
  - Currents (difference of syzygy partners)
  - Gates (triangular cumulation, reduced mod N)
  - Region classification (self-folding vs transitive syzygies)
  - Digital root projection from any base → decimal numogram
  - DOT graph output for visualization

Usage:
  python3 numogram-base-explorer.py --base 36
  python3 numogram-base-explorer.py --base 36 --dot
  python3 numogram-base-explorer.py --compare 10,36,28
  python3 numogram-base-explorer.py --all-known  (bases 0-10,16,22,26,36)
"""

import argparse
import math
import json
import sys
from typing import Dict, List, Tuple, Optional

# ─── Zone Naming (patch from Current C: phoneme system extension) ───

# Decimal zone quasiphonic particles (from CCRU sources)
DECIMAL_PHONEMES = {
    0: "eiaoung",  # silent whisper of the depths
    1: "gl",       # collapsed gargle / glottal spasm
    2: "dt",       # imploded fricative / fractured plosive
    3: "zx",       # swarming insectoid hiss
    4: "skr",      # anthropo-reptiloid growl
    5: "ktt",      # paravocal tic with spittle
    6: "tch",      # static / chewing sound
    7: "pb",       # compounded plosive, sigh
    8: "mnm",      # subvocal hum (proto-originary enunciation)
    9: "tn",       # ultimate unutterable vocal nullity
}

# Decimal zone names (from CCRU/Stillwell)
DECIMAL_ZONE_NAMES = {
    0: "Void",
    1: "Surge",
    2: "Hold",   # Standard name, but some sources call it different names
    3: "Warp",
    4: "Sink",
    5: "Hinge",
    6: "Abyss",
    7: "Hold",
    8: "Rise",
    9: "Plex",
}

# Approach 1: Combinatorial phonemes for extended zones
# Decompose zone into decimal digits, combine their phonemes
def combinatorial_phoneme(z: int, base: int) -> str:
    """Generate phoneme for zone z by decomposing into base-10 digits
    and concatenating the quasiphonic particles."""
    if z < 10:
        return DECIMAL_PHONEMES.get(z, f"z-{z}")
    # Decompose into base-10 digits
    digits = [int(d) for d in str(z)]
    phonemes = [DECIMAL_PHONEMES.get(d, f"z-{d}") for d in digits]
    # Combine with truncation for longer forms
    combined = "".join(phonemes)
    # Trim if too long (max ~8 chars for usability)
    if len(combined) > 8:
        # Take first syllable of each component
        combined = "".join(p[:3] for p in phonemes)
    return combined


# Approach 2: Letter-native phonemes for zones 10-35 (A-Z)
LETTER_NATIVE_PHONEMES = {
    10: "ay",    # A
    11: "buh",   # B
    12: "kuh",   # C
    13: "duh",   # D
    14: "eh",    # E
    15: "fuh",   # F
    16: "guh",   # G
    17: "huh",   # H
    18: "ih",    # I
    19: "juh",   # J
    20: "kay",   # K
    21: "luh",   # L
    22: "muh",   # M
    23: "nuh",   # N
    24: "oh",    # O
    25: "puh",   # P
    26: "kwuh",  # Q
    27: "ruh",   # R
    28: "suh",   # S
    29: "tuh",   # T
    30: "uh",    # U
    31: "vuh",   # V
    32: "wuh",   # W
    33: "ksuh",  # X
    34: "yuh",   # Y
    35: "zuh",   # Z
}


def zone_char(z: int, base: int) -> str:
    """Character representation of zone z in the given base."""
    if z < 10:
        return str(z)
    elif z < 36:
        return chr(ord('A') + z - 10)
    else:
        return f"[{z}]"


def zone_phoneme(z: int, base: int, method: str = "combinatorial") -> str:
    """Get phoneme for zone z."""
    if z < 10:
        return DECIMAL_PHONEMES.get(z, f"z{z}")
    if method == "letter" and z <= 35:
        return LETTER_NATIVE_PHONEMES.get(z, f"z{z}")
    return combinatorial_phoneme(z, base)


def zone_name(z: int, base: int) -> str:
    """Human-readable name for zone z."""
    if z in DECIMAL_ZONE_NAMES:
        return DECIMAL_ZONE_NAMES[z]
    c = zone_char(z, base)
    if z <= 35:
        return f"Zone-{c}"
    return f"Zone-{z}"


# ─── Color palette ───

def zone_color(z: int, base: int) -> Tuple[int, int, int]:
    """Generate an RGB color for a zone based on its position and base.
    Uses a hue mapping that approximates the decimal numogram color scheme
    and extends it for higher bases."""
    if base <= 10:
        # Standard numogram palette
        palette = {
            0: (0, 0, 0),        # Void - black
            1: (200, 100, 50),   # Surge - orange
            2: (50, 150, 200),   # Hold - blue
            3: (100, 200, 100),  # Warp - green
            4: (150, 80, 50),    # Sink - brown
            5: (200, 50, 50),    # Hinge - red
            6: (100, 50, 150),   # Abyss - purple
            7: (50, 100, 150),   # Hold - steel blue
            8: (150, 150, 50),   # Rise - olive
            9: (200, 200, 200),  # Plex - grey/white
        }
        return palette.get(z, (128, 128, 128))
    # Extended bases: use HSL interpolation
    import colorsys
    hue = (z / base) * 0.8  # 0 to 0.8 (avoid red wrap-around)
    saturation = 0.5 + 0.3 * (z % 2)  # alternate saturation
    lightness = 0.3 + 0.4 * (1 - abs(z - base/2) / base)  # brighter in middle
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    return (int(r * 255), int(g * 255), int(b * 255))


# ─── Numogram computation ───

class NumogramBase:
    """A numogram constructed in a given base."""

    def __init__(self, base: int, phoneme_method: str = "combinatorial"):
        if base < 2:
            raise ValueError(f"Base must be >= 2, got {base}")
        self.base = base
        self.N = base
        self.N1 = base - 1  # N-1 (syzygy sum)
        self.phoneme_method = phoneme_method
        self.zones = list(range(base))
        self._compute()

    def _compute(self):
        """Compute all numogram structures."""
        self.syzygies = self._compute_syzygies()
        self.currents = self._compute_currents()
        self.current_registry = self._build_current_registry()
        self.gates = self._compute_gates()
        self.region_map = self._classify_regions()
        self.projections = self._compute_projections()

    def _compute_syzygies(self) -> List[Dict]:
        """Compute syzygy pairs: zones (a, b) where a + b = N-1."""
        pairs = []
        seen = set()
        for a in range(self.base):
            b = self.N1 - a
            if b >= 0 and b < self.base and a not in seen and b not in seen:
                pairs.append({
                    'a': a, 'b': b,
                    'sum': self.N1,
                    'a_char': zone_char(a, self.base),
                    'b_char': zone_char(b, self.base),
                })
                seen.add(a)
                seen.add(b)
        return pairs

    def _compute_currents(self) -> Dict[int, int]:
        """Current from each syzygy = |a - b| = |2a - (N-1)|."""
        currents = {}
        for s in self.syzygies:
            a, b = s['a'], s['b']
            curr = abs(a - b)
            currents[a] = curr
            currents[b] = curr
        return currents

    def _build_current_registry(self) -> Dict[int, List[int]]:
        """Map current values -> list of zone pairs that produce them."""
        registry = {}
        for s in self.syzygies:
            a, b = s['a'], s['b']
            curr = abs(a - b)
            if curr not in registry:
                registry[curr] = []
            registry[curr].append((a, b))
        return registry

    def _compute_gates(self) -> Dict[int, Dict]:
        """Gates from zone z to zone T(z) mod base, where T(z) = z(z+1)/2.
        
        In the standard numogram, gates use digital root (plexing) to reduce
        the triangular number to a single digit. For base-N, we reduce mod N.
        
        Gt-00 (zone 0 → 0) is the zeroth gate, a self-loop.
        """
        gates = {}
        for z in range(1, self.base):
            tri = z * (z + 1) // 2
            # Gate target: triangular number reduced to zone range
            # For base-10: digital root (mod 9, with 9→9, 0→0)
            # For general base: reduce triangular number to range [0, base-1]
            target = tri % self.base
            gates[z] = {
                'zone': z,
                'zone_char': zone_char(z, self.base),
                'triangular': tri,
                'target': target,
                'target_char': zone_char(target, self.base),
                'gate_num': tri,  # The gate NUMBER is the triangular value itself
            }
        # Zone 0 gate: self-loop
        gates[0] = {
            'zone': 0,
            'zone_char': '0',
            'triangular': 0,
            'target': 0,
            'target_char': '0',
            'gate_num': 0,
        }
        return gates

    def _classify_regions(self) -> Dict[str, List[int]]:
        """Classify zones into regions based on syzygy topology.
        
        A syzygy (a, b) is SELF-FOLDING if its current c = |a-b| is one of {a, b}.
        This happens when:
          - a = 0 → c = N-1, which is b (Plex analogue)
          - a = (N-1)/3 → c = a (Warp analogue, only if 3 divides N-1)
        
        All other syzygies are TRANSITIVE (Time-Circuit-like).
        """
        self_folding = []  # zones in self-folding syzygies
        transitive = []    # zones in transitive syzygies
        
        for s in self.syzygies:
            a, b = s['a'], s['b']
            curr = abs(a - b)
            if curr == a or curr == b:
                self_folding.append(a)
                self_folding.append(b)
            else:
                transitive.append(a)
                transitive.append(b)
        
        # Remove duplicates while preserving order
        self_folding = list(dict.fromkeys(self_folding))
        transitive = list(dict.fromkeys(transitive))
        
        regions = {
            'self_folding': sorted(self_folding),
            'transitive': sorted(transitive),
        }
        
        # If there are exactly 2 self-folding zones, they form an outer region
        # If there are 4, there are 2 outer regions (Warp + Plex in base-10)
        # If the base is small, there might be edge cases
        if len(self_folding) == 2:
            # One outer region (Plex analogue, always exists)
            regions['outer_regions'] = [sorted(self_folding)]
        elif len(self_folding) == 4:
            # Two outer regions (Warp + Plex)
            # Group: zones that share a syzygy pair
            outer_pairs = []
            used = set()
            for s in self.syzygies:
                a, b = s['a'], s['b']
                if a in self_folding and b in self_folding and a not in used:
                    outer_pairs.append([a, b])
                    used.add(a)
                    used.add(b)
            regions['outer_regions'] = outer_pairs
        elif len(self_folding) > 0:
            regions['outer_regions'] = [sorted(self_folding)]
        else:
            regions['outer_regions'] = []
        
        # The Time-Circuit is the set of transitive zones
        if transitive:
            regions['time_circuit'] = transitive
        
        return regions

    def _compute_projections(self) -> List[Dict]:
        """Compute the projection from this base's zones to decimal (base-10) zones
        via digital root (mod-9 with 9→9, 0→0)."""
        projections = []
        for z in self.zones:
            if z == 0:
                dec_zone = 0
            else:
                dec_zone = 1 + (z - 1) % 9
            projections.append({
                'zone': z,
                'char': zone_char(z, self.base),
                'decimal_zone': dec_zone,
                'decimal_name': zone_name(dec_zone, 10),
            })
        return projections

    def self_folding_analysis(self) -> str:
        """Analyze why self-folding syzygies occur in this base."""
        lines = []
        N1 = self.N1
        lines.append(f"N-1 = {N1} = {self._factor_str(N1)}")
        
        # Check conditions
        if N1 % 3 == 0:
            a = N1 // 3
            lines.append(f"N-1 divisible by 3: a = (N-1)/3 = {a} → self-folding syzygy ({a}, {N1-a})")
        else:
            lines.append(f"N-1 = {N1} NOT divisible by 3 → no Warp analogue")
        
        if N1 >= 1:
            a = 0
            lines.append(f"a = 0 → self-folding syzygy (0, {N1}) — Plex analogue (always present)")
        
        return "\n".join(lines)

    @staticmethod
    def _factor_str(n: int) -> str:
        """Return prime factorization as string."""
        if n <= 1:
            return str(n)
        temp = n
        factors = []
        d = 2
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 1
        if temp > 1:
            factors.append(temp)
        from collections import Counter
        counts = Counter(factors)
        parts = []
        for p, c in sorted(counts.items()):
            if c == 1:
                parts.append(str(p))
            else:
                parts.append(f"{p}ˣ^{c}")
        return " × ".join(parts)

    # ─── Output ───

    def summary_table(self) -> str:
        """Generate a summary table of all zones."""
        lines = []
        lines.append(f"{'Zone':<6} {'Char':<4} {'Syzygy':<12} {'Current':<8} {'Gate':<14} {'Region':<14} {'Phoneme':<12} {'Dec Proj':<8}")
        lines.append("-" * 80)
        
        for z in self.zones:
            c = zone_char(z, self.base)
            ph = zone_phoneme(z, self.base, self.phoneme_method)
            
            # Syzygy
            partner = self.N1 - z
            syz_str = f"{c}::{zone_char(partner, self.base)}"
            
            # Current
            curr = self.currents.get(z, 0)
            
            # Gate
            gate = self.gates.get(z, {})
            if gate:
                gt_str = f"Gt-{gate['gate_num']:03d}→{zone_char(gate['target'], self.base)}"
            else:
                gt_str = "—"
            
            # Region
            if z in self.region_map.get('self_folding', []):
                region = "OUTER"
            else:
                region = "CIRCUIT"
            
            # Projection
            proj = self.projections[z]
            proj_str = f"{proj['decimal_zone']} ({proj['decimal_name']})"
            
            lines.append(f"{z:<6} {c:<4} {syz_str:<12} {curr:<8} {gt_str:<14} {region:<14} {ph:<12} {proj_str:<8}")
        
        return "\n".join(lines)

    def syzygy_table(self) -> str:
        """Detailed syzygy table."""
        lines = []
        lines.append(f"{'Zone A':<8} {'Zone B':<8} {'Sum':<6} {'Current':<8} {'Type':<12}")
        lines.append("-" * 42)
        for s in self.syzygies:
            a, b = s['a'], s['b']
            curr = abs(a - b)
            if curr == a or curr == b:
                s_type = "Self-folding"
            else:
                s_type = "Transitive"
            lines.append(f"{a} ({s['a_char']}):<8 {b} ({s['b_char']}):<8 {s['sum']:<6} {curr:<8} {s_type:<12}")
        return "\n".join(lines)

    def gate_table(self) -> str:
        """Cumulative gate table."""
        lines = []
        lines.append(f"{'Zone':<6} {'Triangular':<12} {'Gate':<10} {'Target':<8} {'Type':<14}")
        lines.append("-" * 50)
        for z in range(self.base):
            g = self.gates[z]
            if g['target'] == z:
                gt_type = "Self-loop"
            elif g['target'] in (self.N1 - z, self.N1 - g['target']):
                gt_type = "Cross"
            else:
                gt_type = "Projective"
            lines.append(f"{zone_char(z, self.base):<6} {g['triangular']:<12} Gt-{g['gate_num']:03d}  {zone_char(g['target'], self.base):<8} {gt_type:<14}")
        return "\n".join(lines)

    def dot_output(self) -> str:
        """Generate DOT graph representation."""
        lines = []
        lines.append("digraph Numogram {")
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=circle, style=filled];")
        
        # Zone nodes
        for z in self.zones:
            c = zone_char(z, self.base)
            r, g_, b = zone_color(z, self.base)
            hex_color = f"#{r:02x}{g_:02x}{b:02x}"
            lines.append(f'  "{c}" [label="{c}\\n{z}", fillcolor="{hex_color}", fontcolor="white"];')
        
        # Syzygy edges (red)
        for s in self.syzygies:
            a_char = zone_char(s['a'], self.base)
            b_char = zone_char(s['b'], self.base)
            lines.append(f'  "{a_char}" -> "{b_char}" [color="red", style="dashed", label="Σ={self.N1}"];')
        
        # Current edges (blue)
        for z in self.zones:
            curr = self.currents.get(z, 0)
            target_char = zone_char(curr, self.base)
            c_char = zone_char(z, self.base)
            if curr < self.base and c_char != target_char:
                lines.append(f'  "{c_char}" -> "{target_char}" [color="blue", style="bold", label="C={curr}"];')
        
        # Gate edges (green)
        for z, g in self.gates.items():
            if z != g['target']:
                src = zone_char(z, self.base)
                dst = zone_char(g['target'], self.base)
                lines.append(f'  "{src}" -> "{dst}" [color="green", style="dotted", label="Gt-{g["gate_num"]}"];')
        
        lines.append("}")
        return "\n".join(lines)

    def full_report(self) -> str:
        """Full analysis report."""
        lines = []
        lines.append(f"{'='*60}")
        lines.append(f"  NUMOGRAM BASE-{self.base}")
        lines.append(f"{'='*60}")
        lines.append(f"")
        lines.append(f"Structure:")
        lines.append(f"  Zones:       {self.base} (0 to {self.base-1})")
        lines.append(f"  Syzygies:    {len(self.syzygies)} (sum to {self.N1})")
        lines.append(f"  Currents:    {len(self.current_registry)} distinct values")
        lines.append(f"  Gates:       {self.base} (Gt-00 through Gt-{self.gates[self.base-1]['gate_num']})")
        lines.append(f"")
        
        # Self-folding analysis
        lines.append(f"Region Analysis:")
        lines.append(f"  {self.self_folding_analysis()}")
        sf_zones = self.region_map.get('self_folding', [])
        tc_zones = self.region_map.get('transitive', [])
        lines.append(f"  Self-folding zones: {[zone_char(z, self.base) for z in sf_zones]}")
        lines.append(f"  Transitive zones:   {[zone_char(z, self.base) for z in tc_zones]}")
        lines.append(f"  Outer regions:      {len(self.region_map.get('outer_regions', []))}")
        lines.append(f"")
        
        # Syzygy table
        lines.append(f"Syzygy Table:")
        lines.append(f"{self.syzygy_table()}")
        lines.append(f"")
        
        # Gate table
        lines.append(f"Gate Table:")
        lines.append(f"{self.gate_table()}")
        lines.append(f"")
        
        # Zone summary
        lines.append(f"Zone Summary:")
        lines.append(f"{self.summary_table()}")
        lines.append(f"")
        
        # Projection analysis
        lines.append(f"Projection to Decimal (Base-10):")
        lines.append(f"{'Zone':<6} {'Char':<4} {'→Decimal':<10} {'Decimal Name':<14}")
        lines.append("-" * 36)
        for p in self.projections:
            lines.append(f"{p['zone']:<6} {p['char']:<4} → {p['decimal_zone']:<9} {p['decimal_name']:<14}")
        lines.append(f"")
        
        # Cluster analysis: which decimal zones attract which base-N zones
        dec_clusters: Dict[int, List[int]] = {}
        for p in self.projections:
            dz = p['decimal_zone']
            if dz not in dec_clusters:
                dec_clusters[dz] = []
            dec_clusters[dz].append(p['zone'])
        lines.append(f"Decimal Attractor Clusters:")
        for dz in sorted(dec_clusters.keys()):
            zones = [zone_char(z, self.base) for z in dec_clusters[dz]]
            lines.append(f"  Decimal Zone {dz} ({zone_name(dz, 10)}): {', '.join(zones)}")
        lines.append(f"")
        
        return "\n".join(lines)


def zone_character_range_name() -> str:
    """No-op, returns empty - the base name is handled in the report."""
    return ""


# ─── Comparison ───

def compare_bases(bases: List[int], phoneme_method: str = "combinatorial") -> str:
    """Compare region counts across multiple bases."""
    lines = []
    lines.append(f"{'Base':<6} {'N-1':<6} {'N-1 Factor':<18} {'Zones':<6} {'Syzygies':<10} {'Outer Regions':<16} {'Has Warp?':<12}")
    lines.append("-" * 74)
    
    for base in bases:
        if base < 2:
            lines.append(f"{base:<6} {'N/A':<6} {'N/A':<18} {'N/A':<6} {'N/A':<10} {'N/A':<16} {'N/A':<12}")
            continue
        ng = NumogramBase(base, phoneme_method)
        n1 = ng.N1
        has_warp = n1 % 3 == 0
        warpsym = "✓" if has_warp else "✗"
        outer_count = len(ng.region_map.get('outer_regions', []))
        lines.append(f"{base:<6} {n1:<6} {ng._factor_str(n1):<18} {base:<6} {len(ng.syzygies):<10} {outer_count:<16} {warpsym:<12}")
    
    return "\n".join(lines)


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description="Multi-base numogram explorer")
    parser.add_argument("--base", type=int, default=10, help="Base to construct numogram in")
    parser.add_argument("--dot", action="store_true", help="Output DOT graph")
    parser.add_argument("--compare", type=str, help="Comma-separated list of bases to compare")
    parser.add_argument("--all-known", action="store_true", help="Compare all named bases from Tch 7")
    parser.add_argument("--phoneme", choices=["combinatorial", "letter"], default="combinatorial",
                       help="Phoneme generation method for extended zones")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    if args.all_known:
        # All bases Aamodt discusses in Tch 7
        bases = [2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 22, 26, 36]
        print(compare_bases(bases, args.phoneme))
        return
    
    if args.compare:
        bases = [int(b.strip()) for b in args.compare.split(",") if b.strip()]
        print(compare_bases(bases, args.phoneme))
        return
    
    ng = NumogramBase(args.base, args.phoneme)
    
    if args.dot:
        print(ng.dot_output())
    elif args.json:
        print(json.dumps({
            "base": args.base,
            "zones": len(ng.zones),
            "syzygies": ng.syzygies,
            "currents": ng.currents,
            "gates": {str(k): v for k, v in ng.gates.items()},
            "regions": ng.region_map,
            "projections": ng.projections,
        }, indent=2))
    else:
        print(ng.full_report())


if __name__ == "__main__":
    main()
