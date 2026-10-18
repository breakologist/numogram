"""Unit tests for iching.py review fixes. Run: python3 -m unittest -v test_iching"""
import collections, io, json, os, random, subprocess, sys, tempfile, unittest
from contextlib import redirect_stdout
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cli/
sys.path.insert(0, HERE)
import iching as I


def lines(bits, changing=()):
    """bits: line 1 (bottom) first, '1' = yang."""
    out = []
    for i, c in enumerate(bits):
        ch = (i + 1) in changing
        v = (9 if ch else 7) if c == "1" else (6 if ch else 8)
        out.append({"pos": i + 1, "value": v, "changing": ch, "symbol": ""})
    return out


class KingWen(unittest.TestCase):
    def test_table_is_permutation(self):
        self.assertEqual(sorted(I.KW_BY_VALUE), list(range(1, 65)))

    def test_known_hexagrams(self):
        # (lower trigram, upper trigram) bottom-first: Qian 111, Kun 000, Zhen 100, Kan 010,
        # Gen 001, Xun 011, Li 101, Dui 110 (Wikipedia, List of hexagrams of the I Ching)
        T = dict(Qian="111", Kun="000", Zhen="100", Kan="010", Gen="001", Xun="011", Li="101", Dui="110")
        for lo, up, n in [("Qian", "Qian", 1), ("Kun", "Kun", 2), ("Zhen", "Kan", 3), ("Kan", "Gen", 4),
                          ("Qian", "Kun", 11), ("Kun", "Qian", 12), ("Zhen", "Kun", 24), ("Xun", "Qian", 44),
                          ("Xun", "Kan", 48), ("Gen", "Gen", 52), ("Dui", "Zhen", 54), ("Xun", "Kan", 48),
                          ("Kan", "Xun", 59), ("Dui", "Kan", 60), ("Li", "Kan", 63), ("Kan", "Li", 64)]:
            self.assertEqual(I.binary_to_kw(T[lo] + T[up]), n, (lo, up))
            self.assertEqual(I.enrich_iching(lines(T[lo] + T[up]))["hex_num"], n)

    def test_corpus_agrees_when_present(self):
        I.load_hex_info(1)
        if not I.BINARY_TO_TRAD:
            self.skipTest("tianmu corpus not found")
        for b, n in I.BINARY_TO_TRAD.items():
            self.assertEqual(I.binary_to_kw(b), n)

    def test_relating(self):
        r = I.enrich_iching(lines("111111", changing=(1,)))
        self.assertEqual((r["hex_num"], r["relating_hex"]), (1, 44))
        r = I.enrich_iching(lines("000000", changing=(6,)))
        self.assertEqual((r["hex_num"], r["relating_hex"]), (2, 23))


class Odds(unittest.TestCase):
    def dist(self, method):
        c = collections.Counter(I._line_value(b, method) for b in range(256))
        return {k: c[k] * 16 // 256 for k in (6, 7, 8, 9)}

    def test_exact_line_odds(self):
        self.assertEqual(self.dist("flat"), {6: 4, 7: 4, 8: 4, 9: 4})
        self.assertEqual(self.dist("coins"), {6: 2, 7: 6, 8: 6, 9: 2})
        self.assertEqual(self.dist("yarrow"), {6: 1, 7: 5, 8: 7, 9: 3})

    def test_default_unchanged(self):
        # flat default reproduces the original byte % 4 lines for a seed
        import hashlib
        data = hashlib.sha256(b"192855").digest()[:6]
        self.assertEqual([l["value"] for l in I.fetch_iching(192855)], [6 + b % 4 for b in data])

    def test_yarrow_deterministic_and_no_global_side_effect(self):
        random.seed(123); expected = random.random()
        random.seed(123)
        a = I.cast_yarrow_lines(42)
        self.assertEqual(random.random(), expected)
        self.assertEqual(a, I.cast_yarrow_lines(42))


class Zones(unittest.TestCase):
    def test_fuxi_properties(self):
        # T2: the 8 doubled hexagrams are exactly zones 0/9; T3: complement -> syzygy
        doubled = {t + t for t in ("111", "000", "100", "010", "001", "011", "101", "110")}
        for v in range(64):
            b = "".join(str((v >> k) & 1) for k in range(6))
            z = I.fuxi_zone(v)
            self.assertEqual(z in (0, 9), b in doubled, b)
            if v not in (0, 63):
                self.assertEqual((z + I.fuxi_zone(63 - v)) % 9, 0)   # syzygy (9::9 for doubled)

    def test_zone_methods(self):
        r = I.enrich_iching(lines("000000"), zone_method="fuxi")
        self.assertEqual(r["numogram_zone"], 0)
        r = I.enrich_iching(lines("100010"), zone_method="kw")       # #3 Zhun -> KW DR 3
        self.assertEqual(r["numogram_zone"], 3)
        r = I.enrich_iching(lines("100010"), zone_method="curated")   # curated table says 2
        self.assertEqual(r["numogram_zone"], 2)
        r = I.enrich_iching(lines("100010"))                          # default: line value 17 -> 8
        self.assertEqual((r["zone_method"], r["numogram_zone"]), ("fuxi", 8))

    def test_no_ummnu_alias(self):
        self.assertEqual(I.demon_from_zones(0, 9), "Uttunul")


class CLI(unittest.TestCase):
    def run_cli(self, *a, home=None):
        env = dict(os.environ, HOME=home or tempfile.mkdtemp())
        return subprocess.run([sys.executable, os.path.join(HERE, "iching.py"), *a],
                              capture_output=True, text=True, env=env, timeout=30)

    def test_text_output_no_crash(self):
        for a in (["--iching", "--seed", "192855"], ["--cast", "--seed", "42"], ["--cast", "--coins", "--seed", "7"],
                  ["--iching", "--seed", "1", "--method", "yarrow", "--zone-method", "fuxi", "--full"]):
            r = self.run_cli(*a)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("Numogram shadow", r.stdout)
        self.assertIn("52 — Keeping Still", self.run_cli("--iching", "--seed", "192855").stdout)

    def test_hardware_tool_is_used(self):
        home = tempfile.mkdtemp(); os.makedirs(os.path.join(home, ".hermes/tools"))
        flag = os.path.join(home, "called")
        with open(os.path.join(home, ".hermes/tools/hardware_entropy.py"), "w") as f:
            f.write(f"import sys\nopen({flag!r},'w').write('1')\nprint('00'*int(sys.argv[2]))\n")
        r = self.run_cli("--iching", "--json", home=home)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(flag))
        self.assertEqual(json.loads(r.stdout)["hex_num"], 2)   # 00 bytes -> all 6 -> Kun


if __name__ == "__main__":
    unittest.main()
