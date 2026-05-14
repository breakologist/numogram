"""
Crumple/Reconstruct Trajectory Visualisation — Manim Community

Renders an animated analysis of the crumple cascade:
  • Left panel: per-word edit distance trajectories across generations
  • Right panel: final-generation bucket-size vs edit-distance scatter + Pearson r
  • Colour palette: neon tech / numogram (cyan, magenta, gold, green, red)

Usage:
  manim -pqh manim_trajectory_viz.py CrumpleTrajectory
  (Ensure the JSON file exists at the path specified inside.)
"""

from manim import *
from math import sqrt
import json

# ─── Paths ────────────────────────────────────────────────────────────────────
JSON_PATH = "/home/etym/numogram/docs/wiki/assets/trajectory_varentropy_both.json"

# ─── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0A0A0A"   # background
CYAN      = "#00F5FF"   # primary axes/lines
MAGENTA   = "#FF00FF"   # secondary
GOLD      = "#FFD700"   # highlights
GREEN     = "#39FF14"   # accents
RED       = "#FF3333"   # accents/pivot
LAVENDER  = "#C0A0FF"   # zone 8
PURPLE    = "#9900FF"   # zone 9
ZONE_COLORS = {0:GOLD,1:GOLD,2:"#FF8C00",3:MAGENTA,4:CYAN,5:GREEN,6:"#0080FF",7:RED,8:LAVENDER,9:PURPLE}

# ──────────────────────────────────────────────────────────────────────────────
class CrumpleTrajectory(Scene):
    def construct(self):
        self.camera.background_color = BG

        # ── Load JSON data ───────────────────────────────────────────────────────
        with open(JSON_PATH) as f:
            data = json.load(f)

        traj        = data["trajectory"]
        orig_words  = data["original_words"]
        corpus_size = data["parameters"]["corpus_size"]
        gens        = [t["generation"] for t in traj]
        final_gen   = gens[-1]

        # Build per-word edit series (list over generations)
        n_words = len(orig_words)
        edit_series = []   # per word: list of edit distances for each generation index
        bucket_finals = [] # final bucket size per word
        recon_words = []   # reconstructed word at final generation

        for i in range(n_words):
            series = []
            b_final = None
            recon_final = None
            for t in traj:
                g = t["generation"]
                if g == 0:
                    series.append(0)
                else:
                    wd_list = t.get("word_details", [])
                    if i < len(wd_list):
                        wd = wd_list[i]
                        ed = wd["edit_distance"]
                        series.append(ed if ed is not None else 0)
                        if g == final_gen:
                            b_final = wd["bucket_size"]
                            recon_final = wd["reconstructed"]
                    else:
                        series.append(0)
                        if g == final_gen:
                            b_final = 0
                            recon_final = "?"
            edit_series.append(series)
            bucket_finals.append(b_final)
            recon_words.append(recon_final)

        # ── Panel 1: Edit distance trajectories ─────────────────────────────────
        max_edit = max(max(s) for s in edit_series if s)
        axes1 = Axes(
            x_range=[0, final_gen, 1],
            y_range=[0, max_edit*1.15, max(1, int(max_edit/5))],
            axis_config={"color": CYAN, "include_tip": False, "stroke_width": 2, "include_numbers": False},
            x_axis_config={},
            y_axis_config={}
        ).scale(0.9).to_edge(LEFT, buff=0.5)

        x_lab1 = Text("Generation", font_size=32, color=GOLD, font="monospace").next_to(axes1, DOWN).to_edge(RIGHT, buff=0.8)
        y_lab1 = Text("Edit Distance", font_size=32, color=GOLD, font="monospace").next_to(axes1, LEFT).to_edge(LEFT, buff=0.5)

        self.play(Create(axes1), Write(x_lab1), Write(y_lab1), run_time=1.5)

        colors = [CYAN, MAGENTA, GREEN, GOLD, RED, LAVENDER, PURPLE]

        # Draw each word's trajectory
        lines = VGroup()
        for i, series in enumerate(edit_series):
            col = colors[i % len(colors)]
            points = [axes1.c2p(g, e) for g, e in zip(gens, series)]
            line = VMobject().set_stroke(col, width=4)
            line.set_points_smoothly(points)
            lines.add(line)
            self.play(Create(line), run_time=0.4)

        self.wait(1)

        # Label original words on left side
        orig_labels = VGroup()
        for i, word in enumerate(orig_words):
            label = Text(word, font_size=28, color=colors[i % len(colors)], font="monospace")
            label.next_to(axes1.c2p(0, 0), UP, buff=0.3 + i*0.35)
            orig_labels.add(label)
        self.play(FadeIn(orig_labels, lag_ratio=0.2), run_time=1)
        self.wait(1)

        # ── Panel 2: Scatter (final bucket vs final edit) ────────────────────────
        max_bucket = max(bucket_finals) if bucket_finals else 1
        axes2 = Axes(
            x_range=[0, max_bucket*1.2, max(1, int(max_bucket/5))],
            y_range=[0, max_edit*1.15, max(1, int(max_edit/5))],
            axis_config={"color": CYAN, "include_tip": False, "stroke_width": 2, "include_numbers": False},
            x_axis_config={},
            y_axis_config={}
        ).scale(0.9).to_edge(RIGHT, buff=0.5)

        x_lab2 = Text("Bucket Size", font_size=32, color=GOLD, font="monospace").next_to(axes2, DOWN).to_edge(RIGHT, buff=0.8)
        y_lab2 = Text("Edit Distance (final)", font_size=32, color=GOLD, font="monospace").next_to(axes2, LEFT).to_edge(RIGHT, buff=0.5)

        self.play(Create(axes2), Write(x_lab2), Write(y_lab2), run_time=1)

        dots = VGroup()
        for i, (bs, ed) in enumerate(zip(bucket_finals, [s[-1] for s in edit_series])):
            col = colors[i % len(colors)]
            dot = Dot(axes2.c2p(bs, ed), color=col, radius=0.1)
            dots.add(dot)
            self.play(FadeIn(dot), run_time=0.2)

        # Compute Pearson r
        xs = bucket_finals
        ys = [s[-1] for s in edit_series]
        n = len(xs)
        mx = sum(xs)/n; my = sum(ys)/n
        cov = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
        stdx = sqrt(sum((x-mx)**2 for x in xs))
        stdy = sqrt(sum((y-my)**2 for y in ys))
        r = cov/(stdx*stdy) if stdx and stdy else 0.0

        r_text = Text(f"Pearson r = {r:.3f}", font_size=36, color=GREEN, font="monospace")
        r_text.next_to(axes2, UP, buff=0.2)
        self.play(Write(r_text))

        # Label reconstructed words under points
        recon_labels = VGroup()
        for i, word in enumerate(recon_words):
            lbl = Text(word, font_size=24, color=colors[i % len(colors)], font="monospace")
            lbl.next_to(dots[i], DOWN, buff=0.15)
            recon_labels.add(lbl)
        self.play(FadeIn(recon_labels, lag_ratio=0.3), run_time=1)

        self.wait(2)

        # ── Summary overlay ─────────────────────────────────────────────────────
        summary_box = RoundedRectangle(width=6, height=4, corner_radius=0.3,
                                        fill_color="#111111", fill_opacity=0.9,
                                        stroke_color=CYAN, stroke_width=2)
        summary_box.to_edge(LEFT).shift(LEFT*3 + DOWN*0.5)
        summary = VGroup()
        summary.add(Text("CRUMPLE TRAJECTORY", font_size=32, color=GOLD, font="monospace"))
        summary.add(Text(f"Original:  \"{data['original_aq']}\"", font_size=24, color=CYAN, font="monospace"))
        summary.add(Text(f"Corpus:   {corpus_size} words", font_size=24, color=CYAN, font="monospace"))
        summary.add(Text(f"Strategy: {data['parameters']['creative_strategy']} ({data['parameters']['bucket_key']}-bucket)", font_size=24, color=CYAN, font="monospace"))
        summary.add(Text(f"Recovery: {data['summary']['final_recovery_rate']:.1%}", font_size=28, color=GREEN, font="monospace"))
        summary.add(Text(f"AQ preserved: {'✅' if data['summary']['aq_preserved'] else '❌'}", font_size=28, color=GREEN if data['summary']['aq_preserved'] else RED, font="monospace"))
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary.move_to(summary_box.get_center())
        self.play(FadeIn(summary_box), FadeIn(summary))
        self.wait(5)
