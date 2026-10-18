"""Unit tests for oracle.py review fixes. Run: python3 -m unittest -v test_oracle"""
import os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cli/
sys.path.insert(0, HERE)
import oracle as O


def run(*a, home=None):
    env = dict(os.environ, HOME=home or tempfile.mkdtemp())
    return subprocess.run([sys.executable, os.path.join(HERE, "oracle.py"), *a],
                          capture_output=True, text=True, env=env, timeout=60)


class Core(unittest.TestCase):
    def test_current_labels_follow_syzygy(self):
        names = {(1, 8): "Surge", (2, 7): "Hold", (4, 5): "Sink", (3, 6): "Warp", (0, 9): "Plex"}
        for (a, b), n in names.items():
            self.assertEqual(O.ZONES[a]["current"], n)
            self.assertEqual(O.ZONES[b]["current"], n)

    def test_traverse_legacy_collapses_hash_does_not(self):
        for seed in range(1, 500):
            self.assertEqual(O.traverse(seed, 8, "legacy")[3:6] in ([2, 5, 8], [5, 8, 2], [8, 2, 5]), True)
        tails = {tuple(O.traverse(s, 8, "hash")[3:]) for s in range(200)}
        self.assertGreater(len(tails), 150)
        self.assertEqual(O.traverse(42, 8, "hash"), O.traverse(42, 8, "hash"))

    def test_base36_gate_rule(self):
        self.assertEqual(O.GATE_RULE, "dr")                                         # default: digital root
        self.assertEqual(O.compute_base36_char("N")["gate_target_char"], "V")      # 276 mod 35 = 31
        self.assertEqual(O.compute_base36_char("Z")["gate_target"], 35)            # T(35)=630 ≡ 0 -> 35
        self.assertEqual(O.compute_base36_char("0")["gate_target"], 0)
        O.GATE_RULE = "mod"
        try:
            self.assertEqual(O.compute_base36_char("N")["gate_target"], 276 % 36)  # last digit, opt-in
        finally:
            O.GATE_RULE = "dr"

    def test_decimal_gates_are_digital_root(self):
        # CCRU: Gt-1 1->1, Gt-3 2->3, Gt-6 3->6, Gt-10 4->1, Gt-15 5->6, Gt-21 6->3, Gt-28 7->1, Gt-36 8->9, Gt-45 9->9
        self.assertEqual([O.get_gate(z) for z in range(10)], [0, 1, 3, 6, 1, 6, 3, 1, 9, 9])
        self.assertEqual(O.get_gate(8), 9)                                          # Gt-36: 8 -> 9, not 6
        self.assertEqual(O.get_gate_details(8)["gate_raw"], 36)

    def test_gate_rule_cli(self):
        self.assertIn("digital root", run("--text", "N", "--base36").stdout)
        self.assertIn("mod 36", run("--text", "N", "--base36", "--gate-rule", "mod").stdout)
        self.assertEqual(run("--gate-rule", "last").returncode, 2)


class CLI(unittest.TestCase):
    def test_iching_delegation_works(self):
        for a in (["--iching", "--seed", "192855"], ["--iching", "--seed", "192855", "--full"], ["--iching"]):
            r = run(*a)
            self.assertNotIn("delegate error", r.stdout)
            self.assertIn("Numogram shadow", r.stdout)

    def test_taixuan_flags_honoured(self):
        r = run("--taixuan", "--single", "--unicode", "--full", "--hardware", "--em-stats")
        self.assertIn("Em-state Profile", r.stdout)
        self.assertIn("Tetragram: #", r.stdout)
        self.assertNotIn("NUMOGRAM ORACLE READING", r.stdout)

    def test_voice_flag(self):
        self.assertIn("[Voice]", run("--seed", "1", "--voice").stdout)
        self.assertIn("[Voice]", run("--taixuan", "--seed", "42", "--voice").stdout)

    def test_hardware_tool_is_used(self):
        home = tempfile.mkdtemp(); os.makedirs(os.path.join(home, ".hermes/tools"))
        with open(os.path.join(home, ".hermes/tools/hardware_entropy.py"), "w") as f:
            f.write("print('%016x' % 81)\n")
        self.assertIn("Seed:         81 (hardware)", run("--hardware", home=home).stdout)

    def test_bad_option_rejected(self):
        self.assertEqual(run("--seed", "1", "--path", "bogus").returncode, 2)


if __name__ == "__main__":
    unittest.main()
