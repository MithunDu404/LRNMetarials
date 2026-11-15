# p1_s04_padding_why.py: border problem, shrinkage, under-sampled edges, padding. Coverage: C014-C017.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *


class P1S04PaddingWhy(CnnScene):
    def construct(self):
        N, F = 5, 3
        sizes = [N]
        while conv_out(sizes[-1], F) >= 1:
            sizes.append(conv_out(sizes[-1], F))
        assert sizes == [5, 3, 1]                                  # 5x5 -> 3x3 -> 1x1
        counts = np.zeros((N, N), int)                             # windows each pixel takes part in
        for r in range(N - F + 1):
            for c in range(N - F + 1):
                counts[r:r + F, c:c + F] += 1
        assert counts[0, 0] == 1 and counts[N // 2, N // 2] == 9

        head = section_title("A problem at the borders")
        img = blank_grid(N, N).move_to(LEFT * 3.6 + DOWN * 0.2)
        self.line(1, FadeIn(head), LaggedStart(*[Create(c) for c in img], lag_ratio=0.03), run_time=1.5)

        win = Square(F * CELL, stroke_color=TOOL, stroke_width=6).move_to(img[0])
        out_note = Tex("part of the kernel is outside", font_size=LABEL_SIZE, color=LABEL).next_to(img, UP, buff=0.75)
        self.line(2, Create(win), FadeIn(out_note), run_time=1.2)
        self.line(3, win.animate.move_to(img[N + 1]), FadeOut(out_note), run_time=1.2)

        # shrinkage chain
        g3 = blank_grid(3, 3, fill=RESULT, opacity=0.35, border=RESULT).move_to(RIGHT * 1.2 + DOWN * 0.2)
        g1 = blank_grid(1, 1, fill=RESULT, opacity=0.35, border=RESULT).move_to(RIGHT * 4.6 + DOWN * 0.2)
        a1, a2 = arrow_between(img, g3), arrow_between(g3, g1)
        labels = VGroup(*[MathTex(rf"{s} \times {s}", font_size=32, color=c).next_to(g, DOWN, buff=0.3)
                          for s, g, c in zip(sizes, (img, g3, g1), (BLUE_B, BLUE, BLUE))])
        labels[1].align_to(labels[0], DOWN)
        labels[2].align_to(labels[0], DOWN)
        loss = MathTex("-(", "F", "-1)", font_size=30).next_to(a1, UP, buff=0.15)
        loss[1].set_color(YELLOW)
        loss2 = loss.copy().next_to(a2, UP, buff=0.15)
        self.line(4, FadeIn(labels[0]), GrowArrow(a1), FadeIn(loss), FadeIn(g3), FadeIn(labels[1]), run_time=1.5)
        self.begin(5)
        self.at(0.3)
        self.play(GrowArrow(a2), FadeIn(loss2), FadeIn(g1), FadeIn(labels[2]), run_time=1.2)
        self.end()

        # how often each pixel is used
        self.begin(6)
        self.play(*[FadeOut(m) for m in (g3, g1, a1, a2, labels, loss, loss2, win)], run_time=0.7)
        nums = VGroup(*[MathTex(str(counts[r, c]), font_size=CELL_NUM_SIZE).move_to(img[r * N + c])
                        for r in range(N) for c in range(N)])
        cap = Tex(r"windows that include each pixel ($3 \times 3$ kernel)", font_size=LABEL_SIZE, color=LABEL).next_to(img, DOWN, buff=0.35)
        self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.04), FadeIn(cap), run_time=2)
        self.end()

        corner = SurroundingRectangle(img[0], color=LOOK_HERE, buff=0, stroke_width=6)
        centre = SurroundingRectangle(img[(N * N) // 2], color=LOOK_HERE, buff=0, stroke_width=6)
        t1 = Tex(f"corner pixel: {counts[0, 0]} window", font_size=BODY_SIZE, color=SOFT)
        t2 = Tex(f"centre pixel: {counts[N // 2, N // 2]} windows", font_size=BODY_SIZE, color=SOFT)
        VGroup(t1, t2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 2.8 + DOWN * 0.2)
        self.begin(7)
        self.at(0.2)
        self.play(Create(corner), FadeIn(t1), run_time=0.8)
        self.at(0.42)
        self.play(Create(centre), FadeIn(t2), run_time=0.8)
        self.end()

        # padding
        ring = zero_ring(img, p=1)
        pad = Tex(r"padding: $P$ extra rows and columns, usually zeros", font_size=30, color=SOFT)
        pad.move_to(RIGHT * 2.9 + DOWN * 0.2)
        if pad.width > 6.6:
            pad.scale_to_fit_width(6.6)
        self.begin(8)
        self.play(*[FadeOut(m) for m in (nums, cap, corner, centre, t1, t2)], run_time=0.7)
        self.at(0.25)
        self.play(LaggedStart(*[FadeIn(c) for c in ring], lag_ratio=0.03), FadeIn(pad), run_time=2)
        self.end(gap=1.5)
        self.clear_all()
