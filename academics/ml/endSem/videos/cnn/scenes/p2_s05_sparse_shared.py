# p2_s05_sparse_shared.py: sparse connections, weight sharing, equivariance. Coverage: C080-C082, C091, C092.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *

MEDIA = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media"


def field(r, c, f=2, cols=4):
    """Pixel numbers (1-based, row-major) of the f x f window whose top-left is (r, c)."""
    return [(r + m) * cols + (c + n) + 1 for m in range(f) for n in range(f)]


class P2S05SparseShared(CnnScene):
    def construct(self):
        N, F = 4, 2
        assert field(0, 0) == [1, 2, 5, 6]
        assert field(0, 2) == [3, 4, 7, 8]                       # second unit at stride 2 (what the slides show)
        assert field(0, 1) == [2, 3, 6, 7]                       # second unit at stride 1
        dense_c, conv_c = N * N, F * F
        reduction = (1 - conv_c / dense_c) * 100
        assert (dense_c, conv_c, reduction) == (16, 4, 75.0)
        assert 16 * 16 == 256 and round((1 - 4 / 256) * 100) == 98
        # equivariance check (example values)
        x = np.zeros((5, 6)); x[2, 1] = 1
        k = np.ones((2, 2))
        y, y_shift = correlate2d(x, k, mode="valid"), correlate2d(np.roll(x, 1, axis=1), k, mode="valid")
        assert (np.roll(y, 1, axis=1) == y_shift).all()

        head = section_title("Sparse connections")
        self.line(1, FadeIn(head), run_time=0.8)
        name = Tex(r"local receptive field: each unit sees only an $F \times F$ patch", font_size=30, color=SOFT).move_to(DOWN * 3.0)
        self.line(2, FadeIn(name), run_time=1)

        g = tex_grid([[str(r * N + c + 1) for c in range(N)] for r in range(N)], cell=0.75, size=26).move_to(LEFT * 3.4)
        unit = VGroup(neuron(0.5, radius=0.34), MathTex("h_{11}", font_size=26, color=BLACK)).move_to(RIGHT * 3.6)
        unit[1].move_to(unit[0])
        lines = VGroup(*[Line(c.get_center(), unit.get_left(), stroke_width=1.5, color=LABEL) for c in g])
        cnt = Tex(f"{dense_c} connections", font_size=LABEL_SIZE, color=LABEL).next_to(unit, DOWN, buff=0.4)
        self.begin(3)
        self.play(FadeIn(g), FadeIn(unit), run_time=1)
        self.at(0.55)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.03), FadeIn(cnt), run_time=1.5)
        self.end()

        keep = [i - 1 for i in field(0, 0)]
        w1 = window_at(g, N, 0, 0)
        cnt2 = Tex(f"{conv_c} connections: pixels 1, 2, 5, 6", font_size=LABEL_SIZE, color=LABEL).move_to(cnt)
        self.line(4, *[FadeOut(l) for i, l in enumerate(lines) if i not in keep],
                  *[lines[i].animate.set_color(TOOL).set_stroke(width=3) for i in keep], Create(w1), Transform(cnt, cnt2), run_time=1.5)

        # h12 and the stride (source correction)
        w_s2 = window_at(g, N, 0, 2)
        w_s1 = window_at(g, N, 0, 1, color=DIM)
        l_s2 = Tex("$h_{12}$ at stride 2: pixels " + ", ".join(map(str, field(0, 2))), font_size=LABEL_SIZE, color=SOFT)
        l_s1 = Tex("$h_{12}$ at stride 1: pixels " + ", ".join(map(str, field(0, 1))), font_size=LABEL_SIZE, color=DIM)
        l_note = Tex("the slides do not state the stride", font_size=24, color=LABEL)
        VGroup(l_s2, l_s1, l_note).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.2 + DOWN * 0.2)
        self.begin(5)
        self.play(*[FadeOut(lines[i]) for i in keep], FadeOut(unit), FadeOut(cnt), FadeOut(name), w1.animate.set_stroke(opacity=0.3), run_time=0.8)
        self.play(Create(w_s2), FadeIn(l_s2), run_time=0.9)
        self.at(0.5)
        self.play(Create(w_s1), FadeIn(l_s1), run_time=0.9)
        self.at(0.82)
        self.play(FadeIn(l_note), run_time=0.6)
        self.end()

        self.clear_except(head)
        fig = ImageMobject(str(MEDIA / "image60.png")).scale_to_fit_height(5.2).move_to(DOWN * 0.4)
        fig_l = Tex("lecture slide figure", font_size=LABEL_SIZE, color=LABEL).next_to(fig, RIGHT, buff=0.4)
        self.line(6, FadeIn(fig), FadeIn(fig_l), run_time=1)

        self.play(FadeOut(fig), FadeOut(fig_l), run_time=0.6)
        red = MathTex(r"\text{reduction}", "=", r"\left(1 - \frac{F^2}{W_1 \cdot H_1}\right)", r"\times 100\%", font_size=44).move_to(UP * 0.8)
        self.begin(7)
        self.at(0.45)
        self.play(Write(red), run_time=2)
        self.end()
        num = MathTex(rf"1 - \frac{{{conv_c}}}{{{dense_c}}} =", rf"{reduction:.0f}\%", r"\ \text{fewer connections per unit}", font_size=40).move_to(DOWN * 1.3)
        num[1].set_color(RESULT)
        self.line(8, Write(num), run_time=2, gap=1)

        # weight sharing
        self.clear_except(head)
        share = section_title("Weight sharing")
        g2 = blank_grid(N, N, cell=0.75).move_to(LEFT * 2.6 + DOWN * 0.2)
        ker = tex_grid([["w_1", "w_2"], ["w_3", "w_4"]], border=TOOL, color=TOOL, cell=0.75, size=26).move_to(RIGHT * 3.4 + DOWN * 0.2)
        ker_l = caption(ker, f"the same {conv_c} weights at every position")
        w = window_at(g2, N, 0, 0)
        self.begin(9)
        self.play(Transform(head, share), FadeIn(g2), FadeIn(ker), run_time=1)
        self.at(0.5)
        self.play(Create(w), FadeIn(ker_l), run_time=0.8)
        self.end()
        self.begin(10)
        for r in range(N - 1):
            for c in range(N - 1):
                self.play(w.animate.move_to(window_at(g2, N, r, c)), run_time=0.45)
        self.end()

        self.clear_except(head)
        big = ImageMobject(str(MEDIA / "fig_dense_vs_cnn_connectivity.png")).scale_to_fit_height(5.9).move_to(DOWN * 0.55)
        self.line(11, FadeIn(big), run_time=1, gap=0.5)

        # translation equivariance
        self.play(FadeOut(big), run_time=0.6)
        eq_head = section_title("Translation equivariance")
        maps = [gray_map(a.tolist(), cell=0.42, vmax=1) for a in (x, y, np.roll(x, 1, axis=1), y_shift)]
        maps[0].move_to(LEFT * 3.2 + UP * 0.9); maps[1].move_to(RIGHT * 3.0 + UP * 0.9)
        maps[2].move_to(LEFT * 3.2 + DOWN * 1.9); maps[3].move_to(RIGHT * 3.0 + DOWN * 1.9)
        arr = [arrow_between(maps[0], maps[1]), arrow_between(maps[2], maps[3])]
        labs = [caption(maps[0], "input", UP), caption(maps[1], "feature map", UP)]
        tail = Tex("shift the input by 1: the feature map shifts by 1 (example values)", font_size=24, color=LABEL).to_edge(DOWN, buff=0.4)
        self.line(12, Transform(head, eq_head), FadeIn(maps[0]), FadeIn(maps[1]), GrowArrow(arr[0]), *[FadeIn(l) for l in labs], run_time=1.5)
        self.line(13, FadeIn(maps[2]), FadeIn(maps[3]), GrowArrow(arr[1]), FadeIn(tail), run_time=1.5, gap=1.5)
        self.clear_all()
