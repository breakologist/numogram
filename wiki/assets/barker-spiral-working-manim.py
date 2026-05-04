from manim import *
import numpy as np

class BarkerSpiral(Scene):
    def construct(self):
        # Title
        title = Tex(r"\\textbf{Barker Spiral}").scale(1.5)
        self.play(Write(title))
        self.wait(1)

        # Create spiral arms
        arms = VGroup()
        for k in range(45):
            angle = -PI/2 + k * 2*PI/45
            r_inner = 0.8 * 1.08**k
            r_outer = r_inner * 1.08
            # Create arc segment
            arc = Arc(angle, 2*PI/45, radius=r_inner)
            outer_arc = Arc(angle, 2*PI/45, radius=r_outer)
            line1 = Line(arc.point_from_proportion(0), outer_arc.point_from_proportion(0))
            line2 = Line(arc.point_from_proportion(1), outer_arc.point_from_proportion(1))
            arm = VGroup(arc, outer_arc, line1, line2)
            arm.set_stroke(BLUE, 1)
            arm.set_fill(BLUE, 0.3)
            arms.add(arm)

        self.play(Create(arms, run_time=5, rate_func=linear))
        self.wait(3)

        # Add zone labels
        labels = VGroup()
        for zone in [0, 1, 2, 4, 5, 6, 9]:
            arm = next(a for a in arms if a.zone == zone and a.phase == 0)
            label = Tex(f"Z{zone}").move_to(arm.get_center() + UP*0.5)
            labels.add(label)
        self.play(Write(labels, run_time=2))
        self.wait(2)

        # Show central 5⊕5 node
        center_node = Circle(radius=0.1, color=GOLD_E).move_to(ORIGIN)
        center_label = Tex(r"5 \\oplus 5 = 10").next_to(center_node, DOWN)
        self.play(Create(center_node), Write(center_label))
        self.wait(2)

        # Animate spiral curve
        spiral_curve = ParametricFunction(
            lambda t: np.array([0 + 3*np.cos(t), 0 + 3*np.sin(t), 0]),
            t_range=[0, 14*PI],
            color=BLUE_C
        )
        self.play(Create(spiral_curve, run_time=4, rate_func=there_and_back))
        self.wait(2)

        # Final summary
        summary = VGroup(
            Tex(r"\\textbf{Barker Spiral: 45 arms, 10 zones}"),
            Tex(r"\\textbf{Missing zones: 3, 7, 8 (gaps in the spiral)}"),
            Tex(r"\\textbf{Center: } 5 \\oplus 5 = 10")
        ).arrange(DOWN, buff=0.5).to_edge(DOWN)
        self.play(Write(summary))
        self.wait(4)