"""Both tools default to the LINE-VALUE zone convention. Run: python3 -m unittest -v test_conventions"""
import os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cli/
sys.path.insert(0, HERE)
import iching as I
import taixuan as T


def hexlines(v):
    return [{"pos": k + 1, "value": 7 if (v >> k) & 1 else 8, "changing": False, "symbol": ""} for k in range(6)]


class SharedDefault(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(T.ZONE_FROM, "value")
        self.assertEqual(I.enrich_iching(hexlines(5))["zone_method"], "fuxi")
        self.assertEqual(I.cast_iching(seed=1)["zone_method"], "fuxi")

    def test_same_reduction_rule(self):
        # Both reduce the figure's line value the same way: 0 only for the all-zero figure.
        for v in range(81):
            self.assertEqual(T.taixuan_zone(v), I.fuxi_zone(v), v)

    def test_iching_default_zone_is_line_value(self):
        for v in range(64):
            self.assertEqual(I.enrich_iching(hexlines(v))["numogram_zone"], I.fuxi_zone(v))

    def test_doubled_trigrams_in_plex(self):
        for t in range(8):
            z = I.enrich_iching(hexlines(9 * t))["numogram_zone"]      # value 9t = trigram t doubled
            self.assertEqual(z, 0 if t == 0 else 9)
        self.assertEqual(sum(1 for v in range(64) if I.fuxi_zone(v) in (0, 9)), 8)

    def test_complements_are_syzygy_partners(self):
        for v in range(1, 63):
            a = I.enrich_iching(hexlines(v))["numogram_zone"]
            b = I.enrich_iching(hexlines(63 - v))["numogram_zone"]
            self.assertEqual((a + b) % 9, 0, v)
        self.assertEqual(I.enrich_iching(hexlines(0))["numogram_syzygy"], "0::9")

    def test_sequence_convention_still_available(self):
        self.assertEqual(I.enrich_iching(hexlines(0b010001), zone_method="kw")["numogram_zone"], 3)  # #3 Zhun
        self.assertEqual(T.taixuan_zone(0, "number"), 1)                                           # #1 Centre

    def test_oracle_delegation_uses_defaults(self):
        env = dict(os.environ, HOME=tempfile.mkdtemp())
        r = subprocess.run([sys.executable, os.path.join(HERE, "oracle.py"), "--iching", "--seed", "192855"],
                           capture_output=True, text=True, env=env, timeout=60)
        self.assertIn("Numogram shadow: Zone 9", r.stdout)                 # 52 Gen/Gen, value 36
        r = subprocess.run([sys.executable, os.path.join(HERE, "oracle.py"), "--iching", "--seed", "192855",
                            "--zone-method", "kw"], capture_output=True, text=True, env=env, timeout=60)
        self.assertIn("Numogram shadow: Zone 7", r.stdout)


if __name__ == "__main__":
    unittest.main()


EXPLORER = os.environ.get("NUMOGRAM_EXPLORER") or os.path.join(HERE, "..", "numogram-base-explorer.py")


@unittest.skipUnless(os.path.exists(EXPLORER), "numogram-base-explorer.py not found (set NUMOGRAM_EXPLORER)")
class TestExplorerGateDefault(unittest.TestCase):
    """Gate default = digital root in base N (mod N-1); --gate-rule mod = last digit (T mod N)."""

    @classmethod
    def setUpClass(cls):
        import importlib.util
        spec = importlib.util.spec_from_file_location("explorer", EXPLORER)
        cls.E = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.E)

    def test_base10_default_is_ccru(self):
        g = self.E.NumogramBase(10).gates
        self.assertEqual(g[8]["triangular"], 36)
        self.assertEqual(g[8]["target"], 9)                       # Gt-36: 8 -> 9
        self.assertEqual([g[z]["target"] for z in range(10)], [0, 1, 3, 6, 1, 6, 3, 1, 9, 9])

    def test_mod_rule_opt_in(self):
        g = self.E.NumogramBase(10, gate_rule="mod").gates
        self.assertEqual(g[8]["target"], 6)                       # 36 mod 10
        self.assertEqual(self.E.NumogramBase(36, gate_rule="mod").gates[23]["target"], 276 % 36)

    def test_base36_dr_matches_oracle(self):
        import oracle as O
        g = self.E.NumogramBase(36).gates
        for c, z in (("N", 23), ("Z", 35)):
            self.assertEqual(g[z]["target"], O.compute_base36_char(c)["gate_target"])

    def test_cli_flag(self):
        r = subprocess.run([sys.executable, EXPLORER, "--base", "10", "--json", "--gate-rule", "mod"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"gate_rule": "mod"', r.stdout)
