# p1_s09_dilated.py: dilated (atrous) convolution, effective size, learned kernels. Coverage: C042, C043, C054.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *


def f_eff(F, r):
    return r * (F - 1) + 1


class P1S09Dilated(CnnScene):
    def construct(self):
        F, N = 3, 7
        assert f_eff(F, 1) == F + (F - 1) * (1 - 1) == 3
        assert f_eff(F, 2) == F + (F - 1) * (2 - 1) == 5
        taps = {r: [(N // 2 + (m - 1) * r, N // 2 + (n - 1) * r) for m in range(F) for n in range(F)] for r in (1, 2)}
        assert len(taps[2]) == 9                                             # still 9 weights
        span = max(c for _, c in taps[2]) - min(c for _, c in taps[2]) + 1
        assert span == f_eff(F, 2) == 5

        head = section_title("Dilated (atrous) convolution")
        g = blank_grid(N, N, fill=GREY_E, opacity=1).move_to(LEFT * 3.6 + DOWN * 0.2)
        cellpos = lambda rc: g[rc[0] * N + rc[1]].get_center()
        tap = VGroup(*[Square(CELL, stroke_color=TOOL, stroke_width=4).set_fill(TOOL, opacity=0.45).move_to(cellpos(rc)) for rc in taps[1]])
        self.line(1, FadeIn(head), FadeIn(g), LaggedStart(*[FadeIn(t) for t in tap], lag_ratio=0.08), run_time=1.5)

        rate = MathTex("r", r"= 1", font_size=44).next_to(g, UP, buff=0.3)
        rate[0].set_color(GOLD_C)
        name = Tex("gaps between the kernel's weights", font_size=LABEL_SIZE, color=LABEL).next_to(g, DOWN, buff=0.3)
        self.line(2, FadeIn(name), run_time=1)
        self.line(3, FadeIn(rate), run_time=0.8)

        rate2 = MathTex("r", r"= 2", font_size=44).move_to(rate)
        rate2[0].set_color(GOLD_C)
        foot = Square(span * CELL, stroke_color=TOOL, stroke_width=2).move_to(g[(N * N) // 2])
        cover = Tex(rf"covers ${span} \times {span}$ with {len(taps[2])} weights", font_size=LABEL_SIZE, color=LABEL).move_to(name)
        self.begin(4)
        self.play(*[t.animate.move_to(cellpos(rc)) for t, rc in zip(tap, taps[2])], Transform(rate, rate2), run_time=1.5)
        self.at(0.5)
        self.play(Create(foot), FadeOut(name), FadeIn(cover), run_time=1)
        self.end()

        fe = MathTex(r"F_{\text{eff}}", "=", "F", "+ (", "F", "- 1)(", "r", "- 1)", "=", "r", "(", "F", "- 1) + 1", font_size=38)
        for i in (2, 4, 11):
            fe[i].set_color(YELLOW)
        for i in (6, 9):
            fe[i].set_color(GOLD_C)
        fe.move_to(RIGHT * 3.1 + UP * 1.2)
        if fe.width > 7.0:
            fe.scale_to_fit_width(7.0)
        self.begin(5)
        self.play(Write(fe[:8]), run_time=2)
        self.at(0.6)
        self.play(Write(fe[8:]), run_time=1.5)
        self.end()
        e1 = MathTex(rf"r = 1:\quad 1 \cdot ({F} - 1) + 1 =", str(f_eff(F, 1)), font_size=38)
        e2 = MathTex(rf"r = 2:\quad 2 \cdot ({F} - 1) + 1 =", str(f_eff(F, 2)), font_size=38)
        e1[1].set_color(YELLOW); e2[1].set_color(YELLOW)
        VGroup(e1, e2).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.1 + DOWN * 0.4)
        self.begin(6)
        self.play(FadeIn(e1), run_time=0.8)
        self.at(0.5)
        self.play(FadeIn(e2), run_time=0.8)
        self.end()
        benefit = Tex("wider receptive field, same resolution", font_size=30, color=SOFT).move_to(RIGHT * 3.1 + DOWN * 2.2)
        self.line(7, FadeIn(benefit), run_time=1)

        # learned kernels
        self.clear_except(head)
        learned_head = section_title("In a CNN, kernels are learned")
        sobel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        rng = np.random.default_rng(12)
        learned = np.round(rng.normal(0, 0.6, (3, 3)), 1) + 0.0                    # example values
        hand = kernel_grid(sobel, cell=0.9, size=30)
        hand_l = caption(hand, "designed by hand")
        new = tex_grid([[f"{v:.1f}" for v in row] for row in learned], border=LEARNED, color=LEARNED, cell=0.9, size=28)
        new_l = caption(new, "learned from data by backpropagation (example values)")
        self.begin(8)
        self.play(Transform(head, learned_head), FadeIn(hand), FadeIn(hand_l), run_time=1)
        self.at(0.45)
        self.play(Transform(hand, new), FadeOut(hand_l), FadeIn(new_l), run_time=1.5)
        self.end(gap=1.5)
        self.clear_all()
