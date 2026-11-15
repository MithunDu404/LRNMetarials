# p2_s04_why_not_dense.py: three reasons a dense network fails on images. Coverage: C077-C079.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *


class P2S04WhyNotDense(CnnScene):
    def construct(self):
        inputs = 1000 * 1000 * 3
        hidden = 1000
        weights = inputs * hidden
        assert inputs == 3_000_000 and weights == 3 * 10 ** 9

        head = section_title("Why not a fully connected network?")
        self.line(1, FadeIn(head), run_time=1)

        r1 = Tex("1. The parameter count explodes", font_size=BODY_SIZE, color=SOFT).move_to(UP * 1.6)
        a = MathTex(r"1000 \times 1000 \times 3 =", r"3{,}000{,}000", r"\ \text{inputs}", font_size=42)
        b = MathTex(r"3 \times 10^6", r"\times", r"10^3", "=", r"3 \times 10^9", r"\ \text{weights}", font_size=42)
        b[4].set_color(NEG)
        VGroup(a, b).arrange(DOWN, buff=0.7).move_to(DOWN * 0.5)
        self.begin(2)
        self.play(FadeIn(r1), run_time=0.8)
        self.at(0.4)
        self.play(Write(a), run_time=1.5)
        self.end()
        self.begin(3)
        self.at(0.5)
        self.play(Write(b), run_time=1.5)
        self.end(gap=1)

        # 2. flattening destroys the layout
        self.clear_except(head)
        r2 = Tex("2. The 2D layout is destroyed", font_size=BODY_SIZE, color=SOFT).move_to(UP * 1.9)
        R = C = 4
        g = blank_grid(R, C).move_to(UP * 0.1)
        p12, p13, far = 0 * C + 1, 0 * C + 2, R * C - 1
        marks = VGroup(*[SurroundingRectangle(g[i], color=LOOK_HERE, buff=0, stroke_width=6) for i in (p12, p13)],
                       SurroundingRectangle(g[far], color=RESULT, buff=0, stroke_width=6))
        flat = [np.array([(i - (R * C - 1) / 2) * CELL, -2.3, 0]) for i in range(R * C)]
        self.begin(4)
        self.play(FadeIn(r2), FadeIn(g), run_time=0.8)
        self.at(0.3)
        self.play(Create(marks), run_time=0.8)
        self.at(0.5)
        self.play(*[g[i].animate.move_to(flat[i]) for i in range(R * C)],
                  *[m.animate.move_to(flat[i]) for m, i in zip(marks, (p12, p13, far))], run_time=1.8)
        self.end()

        # 3. no translation equivariance
        self.clear_except(head)
        r3 = Tex("3. A shifted object uses different weights", font_size=BODY_SIZE, color=SOFT).move_to(UP * 1.9)
        RR, CC, SHIFT = 4, 8, 3
        pic = blank_grid(RR, CC, cell=0.55).move_to(LEFT * 3.2 + DOWN * 0.6)
        unit = neuron(0.6, radius=0.3).move_to(RIGHT * 4.2 + DOWN * 0.6)

        def blob(c0):
            return [r * CC + c for r in (1, 2) for c in (c0, c0 + 1)]
        before, after = blob(1), blob(1 + SHIFT)
        assert not set(before) & set(after)                         # no weight in common after the shift
        lit = VGroup(*[pic[i].copy().set_fill(WHITE, opacity=0.9) for i in before])
        lines1 = VGroup(*[Line(pic[i].get_center(), unit.get_left(), stroke_width=2, color=POS) for i in before])
        lines2 = VGroup(*[Line(pic[i].get_center(), unit.get_left(), stroke_width=2, color=NEG) for i in after])
        note = Tex(f"shift by {SHIFT} pixels: none of the same weights", font_size=LABEL_SIZE, color=LABEL).move_to(DOWN * 2.7)
        self.begin(5)
        self.play(FadeIn(r3), FadeIn(pic), FadeIn(unit), FadeIn(lit), Create(lines1), run_time=1.2)
        self.at(0.25)
        self.play(lit.animate.shift(RIGHT * SHIFT * 0.55), lines1.animate.set_opacity(0.15), run_time=1.2)
        self.play(Create(lines2), FadeIn(note), run_time=1)
        self.end(gap=1.5)
        self.clear_all()
