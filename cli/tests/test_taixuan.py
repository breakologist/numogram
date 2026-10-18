"""Unit tests for taixuan.py review fixes. Run: python3 -m unittest -v test_taixuan"""
import collections, json, os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cli/
sys.path.insert(0, HERE)
import taixuan as T


class Tetragrams(unittest.TestCase):
    def test_lines_and_names(self):
        self.assertEqual(len(T.TETRAGRAM_NAMES), 81)
        self.assertEqual(T.represent_tetragram(0), [0, 0, 0, 0])            # 1 Centre: all unbroken
        self.assertEqual(T.represent_tetragram(1), [1, 0, 0, 0])            # 2 Full Circle: family line once-broken
        self.assertEqual(T.TETRAGRAM_NAMES[26], "Duties")                   # head 27
        self.assertEqual(T.represent_tetragram(26)[::-1], [0, 2, 2, 2])     # region 1, then 3,3,3
        self.assertEqual(T.TETRAGRAM_NAMES[80], "Fostering")

    def test_display_uses_head_number(self):
        d = T.cast_taixuan(seed=42)
        out = T.format_taixuan(d)
        self.assertIn(f"#{d['upper'] + 1} {T.TETRAGRAM_NAMES[d['upper']]}", out)
        self.assertEqual(d["upper_number"], d["upper"] + 1)

    def test_zone_modes(self):
        val = collections.Counter(T.taixuan_zone(i, "value") for i in range(81))
        num = collections.Counter(T.taixuan_zone(i, "number") for i in range(81))
        self.assertEqual(val[0], 1); self.assertEqual(val[9], 8)            # default, unchanged
        self.assertEqual(dict(num), {z: 9 for z in range(1, 10)})           # head 1 Centre -> zone 1
        self.assertEqual(T.taixuan_zone(0, "number"), 1)
        # value mode depends only on the bottom two lines (weights 1,3,9,27 -> 1,3,0,0 mod 9)
        for i in range(1, 81):
            self.assertEqual(T.taixuan_zone(i, "value") % 9, (i % 3 + 3 * (i // 3 % 3)) % 9)

    def test_unicode_twice_broken(self):
        self.assertEqual(T.STATE_UNICODE[T.MAN], "\U0001D300")
        self.assertNotIn("●", T.STATE_SYMBOLS[T.MAN])


class Demons(unittest.TestCase):
    def test_netspan_table(self):
        self.assertEqual(len(set(T.NETSPAN_DEMONS)), 45)
        self.assertEqual(T.netspan_demon(9, 0), "Uttunul")
        self.assertEqual(T.netspan_demon(8, 9), "Ummnu")
        self.assertEqual(T.netspan_demon(1, 0), "Lurgo")
        self.assertEqual(T.netspan_demon(6, 3), "Djynxx")
        self.assertIsNone(T.netspan_demon(4, 4))
        for (a, b), name in T.TAIXUAN_DEMON_MAP.items():
            self.assertEqual(T.netspan_demon(a, b), name)

    def test_syzygy_only_by_default(self):
        self.assertIsNone(T.enrich_taixuan(25, 15)["demon"])     # zones 7, 6: not a syzygy
        T.NETSPAN = True
        try:
            self.assertEqual(T.enrich_taixuan(25, 15)["demon"], "Bobobja")   # 7::6
        finally:
            T.NETSPAN = False


class Phases(unittest.TestCase):
    def test_table(self):
        self.assertEqual([p["num"] for p in T.YUANDONG_PHASES], list(range(1, 28)))
        self.assertEqual("".join(p["zh"] for p in T.YUANDONG_PHASES),
                         "生萌息華茂止安燠實育和塞作煥幾抑冥通資用達興紊悖靜平序")
        self.assertEqual(T.YUANDONG_PHASES[7]["name"], "Warmth")

    def test_cast_covers_all_27_without_mutation(self):
        seen = collections.Counter(T.cast_yuandong_phase(s)["num"] for s in range(5400))
        self.assertEqual(sorted(seen), list(range(1, 28)))
        self.assertTrue(min(seen.values()) > 120)
        self.assertFalse(any("trits" in p for p in T.YUANDONG_PHASES))
        ph = T.cast_yuandong_phase(5)
        self.assertEqual(ph["num"] - 1, ph["trits"][0] * 9 + ph["trits"][1] * 3 + ph["trits"][2])


class Entropy(unittest.TestCase):
    def test_hardware_tool_is_used(self):
        home = tempfile.mkdtemp(); os.makedirs(os.path.join(home, ".hermes/tools"))
        flag = os.path.join(home, "called")
        with open(os.path.join(home, ".hermes/tools/hardware_entropy.py"), "w") as f:
            f.write(f"import sys\nopen({flag!r},'w').write('1')\nprint('00'*int(sys.argv[2]))\n")
        r = subprocess.run([sys.executable, os.path.join(HERE, "taixuan.py"), "--single", "--json"],
                           capture_output=True, text=True, env=dict(os.environ, HOME=home), timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(os.path.exists(flag))
        self.assertEqual(json.loads(r.stdout)["tetragram"], 0)

    def test_seeded_deterministic(self):
        self.assertEqual(T.cast_taixuan(seed=7), T.cast_taixuan(seed=7))


if __name__ == "__main__":
    unittest.main()
