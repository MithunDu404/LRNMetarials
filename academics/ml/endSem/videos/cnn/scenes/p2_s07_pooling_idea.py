# p2_s07_pooling_idea.py: why pool, four types, properties, hyperparameters, trade-offs. Coverage: C093-C101, C103.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *

POOL = SECOND_TOOL


class P2S07PoolingIdea(CnnScene):
    def construct(self):
        m = np.array([[8, 7, 5, 3], [12, 9, 5, 7], [13, 2, 10, 3], [9, 4, 5, 14]])      # slide 94 map
        block = m[:2, :2]
        assert block.max() == 12 and block.mean() == 9
        assert m.max() == 14 and m.mean() == 7.25
        w2 = conv_out(4, 2, 0, 2)
        assert w2 == 2 and (w2 / 4, w2 * w2 / 16) == (0.5, 0.25)

        head = section_title("Why pool?")
        big = blank_grid(8, 8, cell=0.4, fill=RESULT, opacity=0.35, border=RESULT).move_to(LEFT * 4.3 + DOWN * 0.2)
        big_l = caption(big, "a large feature map")
        fix = Tex("three problems (the guide's text says two, and lists three)", font_size=LABEL_SIZE, color=SOFT).move_to(RIGHT * 1.8 + UP * 2.2)
        fix.scale_to_fit_width(7.8)
        self.begin(1)
        self.play(FadeIn(head), FadeIn(big), FadeIn(big_l), run_time=1)
        self.at(0.45)
        self.play(FadeIn(fix), run_time=0.8)
        self.end()
        probs = [Tex(t, font_size=32, color=SOFT) for t in ("1. Computation and memory", "2. Limited receptive field", "3. Over-sensitive to exact position")]
        VGroup(*probs).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(RIGHT * 1.8 + DOWN * 0.3)
        for k in range(3):
            self.line(2 + k, FadeIn(probs[k], shift=UP * 0.2), run_time=0.9)

        self.clear_except(head)
        pool_head = section_title("Pooling: downsample, keep what matters")
        g = grid(m.tolist(), cell=0.8).move_to(LEFT * 3.4 + DOWN * 0.2)
        g_l = caption(g, "feature map (from the slides)")
        small = blank_grid(2, 2, cell=0.8, fill=RESULT, opacity=0.35, border=RESULT).move_to(RIGHT * 3.2 + DOWN * 0.2)
        arr = arrow_between(g, small, buff=0.5)
        self.line(5, Transform(head, pool_head), FadeIn(g), FadeIn(g_l), GrowArrow(arr), FadeIn(small), run_time=1.5)

        win = window_at(g, 4, 0, 0, color=POOL)
        mx = MathTex(str(block.max()), font_size=36, color=RESULT).move_to(small[0])
        mx_l = Tex("max pooling: keep the largest", font_size=LABEL_SIZE, color=LABEL).next_to(small, UP, buff=0.4)
        self.begin(6)
        self.play(Create(win), FadeIn(mx_l), run_time=1)
        self.at(0.35)
        self.play(TransformFromCopy(g[4][1], mx), run_time=1)
        self.end()
        av = MathTex(f"{block.mean():g}", font_size=36, color=RESULT).move_to(small[0])
        av_l = Tex("average pooling: keep the mean", font_size=LABEL_SIZE, color=LABEL).move_to(mx_l)
        self.line(7, Transform(mx, av), Transform(mx_l, av_l), run_time=1)

        # global pooling
        self.clear_except(head)
        g_head = section_title("Global pooling")
        vol = sheets(1.8, 3, [RESULT], border=RESULT, step=0.22, opacity=0.4).move_to(LEFT * 3.4 + DOWN * 0.1)
        col = blank_grid(3, 1, cell=0.6, fill=RESULT, opacity=0.5, border=RESULT).move_to(RIGHT * 2.6 + DOWN * 0.1)
        ar = arrow_between(vol, col, buff=0.6)
        sz = MathTex(r"W \times H \times D", r"\ \rightarrow\ ", r"1 \times 1 \times D", font_size=40).move_to(DOWN * 2.5)
        gap_l = Tex("global average pooling: one mean per channel", font_size=LABEL_SIZE, color=LABEL).move_to(UP * 2.0)
        gmp_l = Tex("global max pooling: one maximum per channel", font_size=LABEL_SIZE, color=LABEL).move_to(gap_l)
        self.begin(8)
        self.play(Transform(head, g_head), FadeIn(vol), FadeIn(gap_l), run_time=1)
        self.at(0.3)
        self.play(GrowArrow(ar), FadeIn(col), run_time=1)
        self.at(0.5)
        self.play(FadeIn(sz), run_time=0.8)
        self.end()
        self.line(9, Transform(gap_l, gmp_l), run_time=1)

        # properties and hyperparameters
        self.clear_except(head)
        p_head = section_title("Pooling: properties and settings")
        props = [Tex(t, font_size=32, color=SOFT) for t in ("no learnable parameters", r"depth unchanged: $D_{\text{out}} = D_{\text{in}}$", "a little translation invariance")]
        VGroup(*props).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.begin(10)
        self.play(Transform(head, p_head), run_time=0.8)
        for k, fr in enumerate((0.22, 0.38, 0.62)):
            self.at(fr)
            self.play(FadeIn(props[k], shift=UP * 0.2), run_time=0.8)
        self.end()
        self.play(*[FadeOut(p) for p in props], run_time=0.5)
        hy = [MathTex(a, b, font_size=38) for a, b in ((r"F_p", r"\ \text{window: usually } 2 \times 2 \text{ or } 3 \times 3"),
                                                      (r"S_p", r"\ \text{stride: usually } 2"), (r"P_p", r"\ \text{padding: usually } 0"))]
        for h, c in zip(hy, (POOL, PURPLE_B, GREY_B)):
            h[0].set_color(c)
        VGroup(*hy).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.reveal(11, hy, fracs=[0.18, 0.55, 0.78])

        # correction: 50% is per axis
        self.play(*[FadeOut(h) for h in hy], run_time=0.5)
        a4 = blank_grid(4, 4, cell=0.6, fill=RESULT, opacity=0.35, border=RESULT).move_to(LEFT * 4.2 + DOWN * 0.2)
        a2 = blank_grid(w2, w2, cell=0.6, fill=RESULT, opacity=0.35, border=RESULT).move_to(LEFT * 1.2 + DOWN * 0.2)
        aa = arrow_between(a4, a2)
        c1 = MathTex(rf"\text{{width, height: }} 4 \rightarrow {w2}\ \text{{(half)}}", font_size=36)
        c2 = MathTex(rf"\text{{cells: }} 16 \rightarrow {w2 * w2}\ \text{{(a quarter)}}", font_size=36)
        VGroup(c1, c2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.2)
        box = SurroundingRectangle(VGroup(c1, c2), color=LOOK_HERE, buff=0.25, stroke_width=3)
        self.begin(12)
        self.play(FadeIn(a4), GrowArrow(aa), FadeIn(a2), run_time=1)
        self.at(0.45)
        self.play(FadeIn(c1), run_time=0.8)
        self.at(0.7)
        self.play(FadeIn(c2), Create(box), run_time=0.8)
        self.end()

        self.clear_except(head)
        f = MathTex("W_2", "=", r"\left\lfloor \frac{", "W_1", "-", "F_p", "+", "2P_p", "}{", "S_p", r"} \right\rfloor", "+ 1", font_size=46).move_to(UP * 0.7)
        for i, c in zip((0, 3, 5, 7, 9), (BLUE, BLUE_B, POOL, GREY_B, PURPLE_B)):
            f[i].set_color(c)
        d = MathTex("D_2", "=", "D_1", font_size=46).move_to(DOWN * 1.3)
        d[0].set_color(BLUE); d[2].set_color(BLUE_B)
        hh = Tex("(the same for $H_2$)", font_size=LABEL_SIZE, color=LABEL).next_to(f, DOWN, buff=0.3)
        self.begin(13)
        self.play(Write(f), FadeIn(hh), run_time=2)
        self.at(0.65)
        self.play(FadeIn(d), run_time=0.8)
        self.end()

        self.clear_except(head)
        t_head = section_title("Pooling: two trade-offs")
        t1 = Tex("1. A strided convolution can learn to downsample instead", font_size=32, color=SOFT)
        t2 = Tex("2. Exact positions are lost: bad for segmentation", font_size=32, color=SOFT)
        VGroup(t1, t2).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        self.line(14, Transform(head, t_head), FadeIn(t1, shift=UP * 0.2), run_time=1)
        self.line(15, FadeIn(t2, shift=UP * 0.2), run_time=1, gap=1.5)
        self.clear_all()
