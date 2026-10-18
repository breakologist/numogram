"""Unit tests for geomancy.py. Run: python3 -m unittest -v test_geomancy"""
import itertools, json, os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # cli/
sys.path.insert(0, HERE)
import geomancy as G


def run(script, *a):
    env = dict(os.environ, HOME=tempfile.mkdtemp())
    return subprocess.run([sys.executable, os.path.join(HERE, script), *a],
                          capture_output=True, text=True, env=env, timeout=60)


def chart(*names):
    return {h + 1: G.figure(n) for h, n in enumerate(names)}


class Figures(unittest.TestCase):
    def test_sixteen_distinct_patterns(self):
        self.assertEqual(len({f["bits"] for f in G.FIGURES}), 16)
        self.assertEqual(sorted(f["value"] for f in G.FIGURES), list(range(16)))

    def test_known_patterns(self):  # 1 = single point, Fire (head) first
        for n, b in {"Populus": "0000", "Via": "1111", "Albus": "0010", "Rubeus": "0100",
                     "Puer": "1101", "Puella": "1011", "Laetitia": "1000", "Tristitia": "0001",
                     "Carcer": "1001", "Conjunctio": "0110", "Acquisitio": "0101", "Amissio": "1010",
                     "Fortuna Major": "0011", "Fortuna Minor": "1100", "Caput Draconis": "0111",
                     "Cauda Draconis": "1110"}.items():
            self.assertEqual(G.figure(b)["name"], n)
        self.assertEqual(G.figure("Albus")["value"], 2)          # user JSON had 11 (clash with Puella)
        self.assertEqual(G.figure("Cauda Draconis")["value"], 14)  # user JSON had 6 (clash with Conjunctio)
        self.assertIs(G.figure("Coniunctio"), G.figure("Conjunctio"))
        self.assertIs(G.figure("Fortuna Maior"), G.figure("Fortuna Major"))

    def test_operations_digital_ambler_2018(self):
        self.assertEqual(G.name(G.invert("Albus")), "Puer")
        self.assertEqual(G.name(G.reverse("Albus")), "Rubeus")
        self.assertEqual(G.name(G.convert("Albus")), "Puella")
        self.assertEqual(G.name(G.reverse("Fortuna Major")), "Fortuna Minor")
        for f in G.FIGURES:
            self.assertIs(G.invert(G.invert(f)), f)
            self.assertIs(G.convert(G.convert(f)), f)
            self.assertEqual(G.base16_view(f)["syzygy"], G.name(G.invert(f)))

    def test_opposites_greer(self):
        pairs = {("Populus", "Via"), ("Carcer", "Conjunctio"), ("Fortuna Major", "Fortuna Minor"),
                 ("Acquisitio", "Amissio"), ("Tristitia", "Laetitia"), ("Albus", "Rubeus"),
                 ("Puella", "Puer"), ("Caput Draconis", "Cauda Draconis")}
        for a, b in pairs:
            self.assertEqual(G.name(G.opposite(a)), b)
            self.assertEqual(G.name(G.opposite(b)), a)

    def test_schemes(self):
        self.assertEqual(G.attributions("Puella")["sign"], "Libra")
        self.assertEqual(G.attributions("Puella", "agrippa")["sign"], "Taurus")
        self.assertEqual(G.attributions("Acquisitio", "agrippa")["sign"], "Pisces")
        self.assertEqual(G.attributions("Acquisitio", "gerard")["sign"], "Aries")
        self.assertIsNone(G.attributions("Caput Draconis")["sign"])
        self.assertEqual(G.attributions("Fortuna Minor")["element"], "air")
        for sc in G.SCHEMES:
            self.assertEqual(sum(1 for f in G.FIGURES if G.attributions(f, sc)["element"]),
                             16)
        for f in G.FIGURES:
            self.assertTrue(f["da"].startswith("https://digitalambler.wordpress.com/201"))
            self.assertEqual(len(f["gd_houses"]), 12)

    def test_planets_pairs(self):
        from collections import Counter
        c = Counter(f["planet"] for f in G.FIGURES)
        for p in ("Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"):
            self.assertEqual(c[p], 2)


class Shield(unittest.TestCase):
    def test_transposition_and_derivation(self):
        s = G.shield_from_mothers(["Via", "Acquisitio", "Conjunctio", "Laetitia"])
        for i in range(4):
            for j in range(4):
                self.assertEqual(s[f"D{i + 1}"]["bits"][j], s[f"M{j + 1}"]["bits"][i])
        self.assertIs(s["N1"], G.add(s["M1"], s["M2"]))
        self.assertIs(s["J"], G.add(s["RW"], s["LW"]))
        self.assertIs(s["S"], G.add(s["J"], s["M1"]))

    def test_all_charts_valid_and_judges_even(self):
        from collections import Counter
        judges = Counter()
        unique15 = 0
        for bits in range(0, 65536, 7):   # a sample; the full census is tested below
            s = G.shield_from_mothers(G.mothers_from_bits(bits))
            v = G.validate(s)
            self.assertTrue(v["valid"], bits)
            judges[s["J"]["name"]] += 1
        self.assertEqual(set(judges), {f["name"] for f in G.FIGURES if f["points"] % 2 == 0})

    def test_validate_catches_hand_errors(self):
        s = dict(G.shield_from_mothers(["Puer", "Via", "Albus", "Carcer"]))
        s["N2"] = G.invert(s["N2"])
        v = G.validate(s)
        self.assertFalse(v["valid"])
        self.assertIn("N2", v["derivation_errors"])

    def test_via_puncti(self):
        for bits in range(0, 65536, 13):
            s = G.shield_from_mothers(G.mothers_from_bits(bits))
            vp = G.via_puncti(s)
            if s["J"]["bits"][0] == 1:
                self.assertEqual(vp["kind"], "single")
                self.assertEqual(len(vp["paths"]), 1)
                self.assertEqual(len(vp["paths"][0]), 4)          # J → witness → niece → mother/daughter
                self.assertIn(vp["paths"][0][-1][0], "MD")
            else:
                self.assertIn(vp["kind"], ("none", "branching"))


class Houses(unittest.TestCase):
    def test_placements(self):
        s = G.shield_from_mothers(["Puer", "Via", "Albus", "Carcer"])
        seq, ast = G.house_chart(s), G.house_chart(s, "astrological")
        self.assertIs(seq[1], s["M1"]); self.assertIs(seq[12], s["N4"])
        self.assertIs(ast[10], s["M1"]); self.assertIs(ast[1], s["M2"]); self.assertIs(ast[9], s["N4"])
        self.assertEqual(sorted(ast), list(range(1, 13)))

    def test_perfection_modes(self):
        base = ["Populus", "Albus", "Rubeus", "Carcer", "Tristitia", "Laetitia",
                "Puer", "Puella", "Amissio", "Via", "Conjunctio", "Acquisitio"]
        h = list(base); h[6] = "Populus"
        self.assertEqual(G.perfection(chart(*h))["modes"], ["occupation"])
        h = list(base); h[7] = "Populus"                   # querent's figure next to house 7
        self.assertEqual(G.perfection(chart(*h))["modes"], ["conjunction"])
        h = list(base); h[2], h[3] = "Populus", "Puer"     # both meet in 3–4
        self.assertEqual(G.perfection(chart(*h))["modes"], ["mutation"])
        h = list(base); h[1] = h[5] = "Fortuna Major"      # third figure beside both (2 and 6)
        self.assertEqual(G.perfection(chart(*h))["modes"], ["translation"])
        self.assertEqual(G.perfection(chart(*base))["modes"], ["denial"])

    def test_abano_adjacency(self):
        h = ["Populus", "Albus", "Rubeus", "Carcer", "Tristitia", "Laetitia",
             "Puer", "Puella", "Amissio", "Via", "Conjunctio", "Puer"]   # Puer in 12, next to 1
        self.assertEqual(G.perfection(chart(*h))["modes"], ["conjunction"])
        self.assertEqual(G.perfection(chart(*h), abano=True)["modes"], ["denial"])

    def test_company(self):
        self.assertEqual(G.company(chart("Puer", "Puer", *["Via"] * 10), 1)["company"], "simple")
        self.assertEqual(G.company(chart("Puer", "Rubeus", *["Via"] * 10), 2)["company"], "demi-simple")
        self.assertEqual(G.company(chart("Puer", "Puella", *["Via"] * 10), 1)["company"], "compound")
        self.assertEqual(G.company(chart("Puer", "Laetitia", *["Via"] * 10), 1)["company"], "capitular")
        self.assertIsNone(G.company(chart("Puer", "Albus", *["Via"] * 10), 1)["company"])

    def test_part_of_fortune_and_topics(self):
        s = G.shield_from_mothers(["Populus"] * 4)          # all double: 12 × 8 = 96 points → 12
        pf = G.part_of_fortune(s)
        self.assertEqual((pf["points"], pf["figure_number"], pf["house"]), (96, 12, 12))
        self.assertEqual(G.part_of_fortune(s, "astrological")["house"], 9)
        self.assertEqual(G.house_for_topic("Will I get the job?"), 10)
        self.assertEqual(G.house_for_topic("marriage"), 7)


class Numogram(unittest.TestCase):
    def test_zone_maps(self):
        self.assertEqual(G.zone("Via"), 6); self.assertEqual(G.zone("Populus"), 0)
        self.assertEqual(G.zone("Via", "points"), 4); self.assertEqual(G.zone("Populus", "points"), 8)
        self.assertEqual(G.zone("Laetitia", "dr-line"), 1)
        for f in G.FIGURES:   # a base-16 syzygy never lands on a decimal syzygy (sum ≡ 6 mod 9)
            self.assertEqual((G.zone(f) + G.zone(G.invert(f))) % 9, 6)

    def test_base16_gate_rule(self):
        self.assertEqual(G.base16_view("Via")["gate_tri"], 120)
        self.assertEqual(G.base16_view("Via")["gate_target16"], 15)          # 120 ≡ 0 (mod 15) → 15
        self.assertEqual(G.base16_view("Via", "mod")["gate_target16"], 120 % 16)
        self.assertEqual(G.base16_view("Populus")["gate_target16"], 0)

    def test_nuclear_iching(self):
        self.assertEqual(G.name(G.figure_from_hexagram(1)), "Via")
        self.assertEqual(G.name(G.figure_from_hexagram(2)), "Populus")
        self.assertEqual(G.name(G.figure_from_hexagram(63)), "Amissio")       # lines 2–5: yin yang yin yang
        allhex = sorted(itertools.chain.from_iterable(G.hexagrams_for_figure(f) for f in G.FIGURES))
        self.assertEqual(allhex, list(range(1, 65)))
        import iching
        self.assertEqual(G.KW_BY_VALUE, iching.KW_BY_VALUE)

    def test_census(self):
        c = G.census()
        self.assertEqual(c["charts"], 65536)
        self.assertEqual(set(c["judge"].values()), {8192})
        self.assertEqual(len(c["judge"]), 8)
        self.assertEqual(c["charts_with_15_unique_figures"], 16)
        self.assertEqual(c["impeded_charts"], 8192)
        self.assertEqual(c["odd_total_single_points"]["first_15"], 0)   # Grok's "rule" rejects nothing
        self.assertEqual(c["odd_total_single_points"]["first_12"], 0)
        self.assertTrue(all(h % 2 == 0 for h in c["part_of_fortune_house"]))
        self.assertEqual(sum(c["via_puncti"].values()), 65536)
        self.assertEqual(c["via_puncti"]["single"], 32768)
        self.assertEqual(sum(c["zone_all_16_positions"].values()), 16 * 65536)


class CLI(unittest.TestCase):
    def test_json_seed_deterministic(self):
        a, b = run("geomancy.py", "--seed", "192855", "--json"), run("geomancy.py", "--seed", "192855", "--json")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        d = json.loads(a.stdout)
        self.assertTrue(d["validation"]["valid"])
        self.assertEqual(len(d["houses"]), 12)
        self.assertTrue(d["numogram"]["speculative"])
        self.assertEqual(run("geomancy.py", "--seed", "0xff", "--json").returncode, 0)

    def test_bad_inputs_exit_2(self):
        self.assertEqual(run("geomancy.py", "--seed", "nope").returncode, 2)
        self.assertEqual(run("geomancy.py", "--dots", "1 2 3").returncode, 2)
        self.assertEqual(run("geomancy.py", "--mothers", "Puer,Bogus,Via,Via").returncode, 2)
        self.assertEqual(run("geomancy.py", "--scheme", "x").returncode, 2)
        self.assertEqual(run("geomancy.py", "--house", "1").returncode, 2)

    def test_dots_and_mothers(self):
        dots = "13 7 8 9  10 10 10 10  3 3 3 3  4 5 6 6"
        ms = G.mothers_from_dots([int(x) for x in dots.split()])
        self.assertEqual([m["name"] for m in ms], ["Puer", "Populus", "Via", "Rubeus"])
        d = json.loads(run("geomancy.py", "--dots", dots, "--json").stdout)
        self.assertEqual(d["shield"]["M1"]["name"], "Puer")
        d = json.loads(run("geomancy.py", "--mothers", "Puer,Populus,Via,Rubeus", "--json").stdout)
        self.assertEqual(d["shield"]["M4"]["name"], "Rubeus")
        self.assertEqual(d["source"], "manual mothers")

    def test_text_render(self):
        out = run("geomancy.py", "--seed", "7", "--plain", "--full").stdout
        self.assertIn("Judge:", out); self.assertIn("speculative", out); self.assertIn("* *", out.replace("   ", " "))
        self.assertIn("non-historical", out)
        self.assertEqual(run("geomancy.py", "--figures").returncode, 0)

    def test_oracle_delegation(self):
        r = run("oracle.py", "--geomancy", "--seed", "192855", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(json.loads(r.stdout), json.loads(run("geomancy.py", "--seed", "192855", "--json").stdout))
        self.assertEqual(run("oracle.py", "--geomancy", "--seed", "bad").returncode, 2)


if __name__ == "__main__":
    unittest.main()


ALL12 = ["Puer", "Via", "Albus", "Carcer", "Laetitia", "Populus", "Puella", "Amissio", "Tristitia",
         "Conjunctio", "Acquisitio", "Fortuna Major"]


class RoundTwo(unittest.TestCase):
    """Halting, placements, Part of Fortune rules, aspects, remediation, SVG (round 2)."""

    def test_halting_variants(self):
        H = chart("Rubeus", *ALL12[1:])
        a = G.all_halting(H)
        self.assertTrue(a["gd"] and a["skinner"] and a["skinner-strict"] and a["greer-stranger"])
        self.assertFalse(a["greer"] or a["digital-ambler"] or a["agrippa"] or a["gerard"] or a["none"])
        h = G.halting(H, "gd")
        self.assertEqual(h["fired"], ["Rubeus in 1"])
        self.assertIn("worthless", h["explanation"])
        C = chart("Carcer", *ALL12[1:])
        self.assertTrue(G.halting(C, "skinner-strict")["halted"])
        self.assertFalse(G.halting(C, "skinner")["halted"])
        D = chart("Cauda Draconis", *ALL12[1:])
        self.assertEqual(G.halting(D, "digital-ambler")["fired"], ["Cauda Draconis in 1"])
        self.assertFalse(G.halting(D, "digital-ambler")["halted"])

    def test_greer_warnings(self):
        names = ["Populus"] + ALL12[1:]
        names[10] = "Rubeus"                      # house 11
        pats = [w["pattern"] for w in G.querent_warnings(chart(*names))]
        self.assertIn("Populus in 1", pats)
        self.assertIn("Populus in 1 + Rubeus in 11", pats)
        names = ["Rubeus"] + ALL12[1:]
        names[6] = "Rubeus"
        self.assertIn("Rubeus occupation", [w["pattern"] for w in G.querent_warnings(chart(*names))])
        self.assertIn("Amissio in 1", [w["pattern"] for w in G.querent_warnings(chart("Amissio", *ALL12[1:]))])
        names = list(ALL12)
        names[3] = "Puer"                         # querent's figure passes to house 4
        self.assertTrue(any("7th" in w["pattern"] for w in G.querent_warnings(chart(*names))))
        self.assertEqual(G.querent_warnings(chart(*ALL12)), [])

    def test_placements_new(self):
        sh = G.shield_from_mothers(["Puer", "Via", "Albus", "Carcer"])
        first12 = [sh[p]["name"] for p in G.POSITIONS[:12]]
        ang = G.house_chart(sh, "angular")
        self.assertEqual([ang[h]["name"] for h in (1, 4, 7, 10)], first12[:4])
        ag = G.house_chart(sh, "agrippa")
        self.assertEqual([ag[h]["name"] for h in (1, 10, 7, 4)], first12[:4])
        self.assertEqual(ag[9]["name"], G.add(ag[1], ag[5])["name"])
        self.assertEqual(ag[12]["name"], G.add(ag[4], ag[8])["name"])
        self.assertEqual(sorted(ag), list(range(1, 13)))

    def test_pof_rules(self):
        sh = G.shield_from_mothers(["Puer", "Via", "Albus", "Carcer"])
        for r in ("gd", "greer", "index"):
            p = G.part_of_fortune(sh, rule=r)
            self.assertTrue(1 <= p["house"] <= 12)
            self.assertEqual(p["house"], p["points"] % 12 or 12)
        self.assertFalse(G.part_of_fortune(sh, rule="agrippa")["available"])
        self.assertEqual(G.part_of_fortune(sh, rule="agrippa", dots=[1] * 16)["house"], 4)   # 16 mod 12
        with self.assertRaises(ValueError):
            G.part_of_fortune(sh, rule="nope")

    def test_aspects_greer(self):
        names = list(ALL12)
        names[2] = "Puer"                         # querent's Puer passes to 3; 3→7 is four houses on = trine
        H = chart(*names)
        asp = G.aspects(H, 1, 7)
        self.assertTrue(any(a["aspect"] == "trine" and a["houses"] == [3, 7] for a in asp))
        self.assertFalse(any(a["houses"] == [1, 7] for a in asp))
        p = G.perfection(H, 1, 7, use_aspects=True)
        self.assertIn("favourable aspect", p["modes"])

    def test_remediation_interpretive(self):
        d = G.cast_geomancy(seed=5)
        rm = d["remediation"]
        self.assertTrue(rm["interpretive"])
        self.assertEqual([i["role"] for i in rm["items"]], ["querent", "quesited", "judge"])
        self.assertEqual(set(G.REMEDY), {f["name"] for f in G.FIGURES})
        self.assertEqual(set(G.HOUSE_FOCUS), set(range(1, 13)))
        self.assertIn("interpretive", G.format_geomancy(d))

    def test_cast_keys_and_halt_flag(self):
        d = G.cast_geomancy(mothers=["Rubeus", "Via", "Albus", "Carcer"])
        self.assertTrue(d["halting"]["halted"])
        self.assertIn("halted", d["remediation"])
        self.assertEqual(d["halting"]["first_mother"], "Rubeus")
        self.assertIn("HALTED", G.format_geomancy(d))
        self.assertFalse(G.cast_geomancy(mothers=["Rubeus", "Via", "Albus", "Carcer"],
                                         halt_rule="greer")["halting"]["halted"])
        for k in ("reconciler_greer", "halting_all_rules", "index_greer"):
            self.assertIn(k, d)

    def test_census_halts(self):
        c = G.census()
        self.assertEqual(c["halted_by_rule"]["gd"], 8192)        # 2 of 16 figures in house 1
        self.assertEqual(c["halted_by_rule"]["skinner-strict"], 12288)
        self.assertEqual(c["halted_by_rule"]["none"], 0)
        self.assertEqual(c["greer_warnings"]["Rubeus in 1"], 4096)

    def test_text_template_labels(self):
        txt = "\n".join(G.format_shield(G.cast_geomancy(seed=1), "plain"))
        for lab in ("[Vita]", "[Mors]", "[Iter]", "[Carcer]", "[Judge]"):
            self.assertIn(lab, txt)
        self.assertLess(txt.index("[Mors]"), txt.index("[Vita]"))   # right-to-left top row

    def test_svg(self):
        import xml.etree.ElementTree as ET
        import geomancy_svg
        svg = geomancy_svg.shield_svg(G.cast_geomancy(seed=192855))
        root = ET.fromstring(svg)
        self.assertTrue(root.tag.endswith("svg"))
        txt = "".join(root.itertext())
        for lab in ("Vita", "Benefacta", "Left Witness", "Judge", "Amissio"):
            self.assertIn(lab, txt)
        circles = [e for e in root.iter() if e.tag.endswith("circle")]
        sh = G.cast_geomancy(seed=192855)["shield"]
        self.assertEqual(len(circles), sum(G.figure(sh[p]["name"])["points"] for p in G.POSITIONS[:15]))

    def test_cli_round_two(self):
        with tempfile.TemporaryDirectory() as t:
            out = os.path.join(t, "s.svg")
            r = run("geomancy.py", "--seed", "4", "--halt-rule", "skinner", "--pof-rule", "index",
                    "--houses", "angular", "--aspects", "--scheme", "greer", "--svg", out)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(os.path.getsize(out) > 1000)
        self.assertEqual(run("geomancy.py", "--halt-rule", "bogus").returncode, 2)
        j = json.loads(run("geomancy.py", "--seed", "4", "--json", "--houses", "agrippa").stdout)
        self.assertEqual(j["options"]["houses"], "agrippa")


class Farrell(unittest.TestCase):
    """Farrell, Notes on Geomancy (2009): halting variants, witness verdict, sign wheel, planet names."""

    def test_halting_farrell(self):
        C = chart("Carcer", *ALL12[1:])
        R = chart("Rubeus", *ALL12[1:])
        self.assertTrue(G.halting(C, "farrell")["halted"])
        self.assertFalse(G.halting(R, "farrell")["halted"])          # Rubeus is not a halt for him
        sh = G.shield_from_mothers(["Puer", "Via", "Albus", "Cauda Draconis"])
        H = G.house_chart(sh)
        h = G.halting(H, "farrell-m4", shield=sh)
        self.assertTrue(h["halted"])
        self.assertIn("Fourth Mother", h["fired"][0])
        self.assertFalse(G.halting(H, "farrell", shield=sh)["halted"])
        with self.assertRaises(ValueError):
            G.halting(H, "farrell-m4")
        self.assertNotIn("farrell-m4", G.all_halting(H))
        self.assertIn("farrell-m4", G.all_halting(H, shield=sh))

    def test_census_farrell(self):
        c = G.census()["halted_by_rule"]
        self.assertEqual(c["farrell"], 8192)
        self.assertEqual(c["farrell-m4"], 8192)

    def test_witness_verdict(self):
        self.assertEqual(G.witness_verdict("Fortuna Major", "Acquisitio", "Laetitia")["verdict"], "yes")
        self.assertEqual(G.witness_verdict("Carcer", "Rubeus", "Amissio")["verdict"], "no")
        self.assertEqual(G.witness_verdict("Carcer", "Puella", "Fortuna Minor")["rule"], 3)
        self.assertEqual(G.witness_verdict("Puella", "Carcer", "Populus")["rule"], 4)
        self.assertEqual(G.witness_verdict("Carcer", "Puella", "Populus")["rule"], 5)
        self.assertIsNone(G.witness_verdict("Via", "Populus", "Populus")["rule"])
        self.assertEqual(set(G.FARRELL_POLARITY), {f["name"] for f in G.FIGURES})

    def test_sign_wheel_and_scheme(self):
        H = chart("Fortuna Major", *ALL12[1:])
        w = G.sign_wheel(H)
        self.assertEqual((w["ascendant"], w["houses"][2], w["houses"][3]), ("Leo", "Virgo", "Libra"))  # p.49 example
        self.assertEqual(G.sign_wheel(chart("Populus", *ALL12[1:]))["houses"][2], "Leo")
        self.assertEqual(G.sign_wheel(chart("Caput Draconis", *ALL12[1:]), "golden-dawn")["ascendant"], "Capricorn")
        self.assertEqual(G.attributions("Cauda Draconis", "farrell")["sign"], "Scorpio")
        self.assertEqual(G.attributions("Rubeus", "farrell")["element"], "water")   # GD elements kept

    def test_question_planet(self):
        d = G.cast_geomancy(seed=3, planet="Jupiter")
        q = d["question_planet"]
        self.assertEqual((q["archangel"], q["intelligence"], q["spirit"]), ("Sachiel", "Iophiel", "Hismael"))
        self.assertTrue(all(n in ("Acquisitio", "Laetitia", "Caput Draconis") for n in q["figures_in_houses"].values()))
        self.assertIsNone(G.cast_geomancy(seed=3)["question_planet"])
        with self.assertRaises(ValueError):
            G.cast_geomancy(seed=3, planet="pluto")
        r = run("geomancy.py", "--seed", "3", "--planet", "moon", "--scheme", "farrell", "--halt-rule", "farrell-m4")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Shelachel", r.stdout)
        self.assertIn("Witness verdict", r.stdout)
