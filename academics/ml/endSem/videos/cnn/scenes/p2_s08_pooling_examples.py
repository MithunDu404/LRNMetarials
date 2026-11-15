# p2_s08_pooling_examples.py: the two worked pooling examples from the slides. Coverage: C102, C104-C106.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *

POOL = SECOND_TOOL
FIG = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media" / "image64.png"


def pool(a, f, s, fn):
    n = conv_out(a.shape[0], f, 0, s)
    return np.array([[fn(a[r * s:r * s + f, c * s:c * s + f]) for c in range(n)] for r in range(n)])


class P2S08PoolingExamples(CnnScene):
    def construct(self):
        A = np.array([[8, 7, 5, 3], [12, 9, 5, 7], [13, 2, 10, 3], [9, 4, 5, 14]])       # slide 94
        B = np.array([[1, 4, 2, 1], [5, 8, 3, 4], [7, 6, 4, 5], [1, 3, 1, 2]])           # slides 98-106
        a_max, a_avg = pool(A, 2, 2, np.max), pool(A, 2, 2, np.mean)
        b_s2, b_s1 = pool(B, 2, 2, np.max), pool(B, 2, 1, np.max)
        assert a_max.tolist() == [[12, 7], [13, 14]] and a_avg.tolist() == [[9, 5], [7, 8]]
        assert b_s2.tolist() == [[8, 4], [7, 5]]
        assert b_s1.tolist() == [[8, 8, 4], [8, 8, 5], [7, 6, 5]]
        assert conv_out(4, 2, 0, 1) == 3 and int((b_s1 == 8).sum()) == 4
        READ = DOWN * 2.8

        head = section_title("Pooling, worked: max and average")
        g = grid(A.tolist(), cell=0.8).move_to(LEFT * 4.0 + UP * 0.2)
        g_l = caption(g, r"$2 \times 2$ window, stride 2")
        self.line(1, FadeIn(head), FadeIn(g), run_time=1.2)
        blocks = VGroup(*[window_at(g, 4, r, c, color=POOL).set_stroke(width=3) for r in (0, 2) for c in (0, 2)])
        self.line(2, FadeIn(g_l), LaggedStart(*[Create(b) for b in blocks], lag_ratio=0.3), run_time=1.8)

        gm = grid(a_max.tolist(), cell=0.8, border=RESULT, num_color=RESULT).move_to(RIGHT * 1.2 + UP * 0.2)
        ga = grid([[int(v) for v in row] for row in a_avg], cell=0.8, border=RESULT, num_color=RESULT).move_to(RIGHT * 4.6 + UP * 0.2)
        gm_l, ga_l = caption(gm, "max", UP), caption(ga, "average", UP)
        self.play(FadeIn(VGroup(*[c[0] for c in gm])), FadeIn(VGroup(*[c[0] for c in ga])), FadeIn(gm_l), FadeIn(ga_l), run_time=0.6)
        read = None
        for k, (r, c) in enumerate(((0, 0), (0, 2), (2, 0), (2, 2))):
            vals = A[r:r + 2, c:c + 2].flatten()
            t = MathTex(rf"\max({', '.join(map(str, vals))}) =", str(vals.max()), r"\qquad",
                        rf"\frac{{{' + '.join(map(str, vals))}}}{{4}} = \frac{{{vals.sum()}}}{{4}} =", f"{vals.mean():g}", font_size=36).move_to(READ)
            t[1].set_color(RESULT); t[4].set_color(RESULT)
            hi = window_at(g, 4, r, c, color=POOL)
            self.begin(3 + k)
            self.play(FadeIn(hi), *([FadeOut(read)] if read else []), run_time=0.5)
            self.play(Write(t[:2]), run_time=1)
            self.play(FadeIn(gm[k][1]), run_time=0.4)
            self.at(0.55)
            self.play(Write(t[2:]), run_time=1)
            self.play(FadeIn(ga[k][1]), run_time=0.4)
            self.end()
            self.remove(hi)
            read = t

        fig = ImageMobject(str(FIG)).scale_to_fit_height(4.8).move_to(DOWN * 0.5)
        fig_l = Tex("lecture slide figure: the same results", font_size=LABEL_SIZE, color=LABEL).next_to(fig, DOWN, buff=0.15)
        self.begin(7)
        self.at(0.6)
        self.clear_except(head, run_time=0.6)
        self.play(FadeIn(fig), FadeIn(fig_l), run_time=0.8)
        self.end(gap=1)

        # second example
        self.clear_except(head)
        head2 = section_title("Max pooling: stride 2, then stride 1")
        h = grid(B.tolist(), cell=0.8).move_to(LEFT * 3.8 + UP * 0.2)
        self.line(8, Transform(head, head2), FadeIn(h), run_time=1.2)
        o2 = grid(b_s2.tolist(), cell=0.8, border=RESULT, num_color=RESULT).move_to(RIGHT * 2.8 + UP * 0.2)
        o2_l = caption(o2, "stride 2", UP)
        w = window_at(h, 4, 0, 0, color=POOL)
        self.begin(9)
        self.play(FadeIn(VGroup(*[c[0] for c in o2])), FadeIn(o2_l), Create(w), run_time=0.8)
        for k, (r, c) in enumerate(((0, 0), (0, 2), (2, 0), (2, 2))):
            self.at(0.08 + 0.17 * k)
            self.play(w.animate.move_to(window_at(h, 4, r, c)), run_time=0.5)
            self.play(FadeIn(o2[k][1]), run_time=0.4)
        self.end()

        o1 = grid(b_s1.tolist(), cell=0.8, border=RESULT, num_color=RESULT).move_to(RIGHT * 2.8 + UP * 0.2)
        o1_l = caption(o1, "stride 1 (overlapping)", UP)
        size = MathTex(r"W_2 = \left\lfloor \frac{4 - 2}{1} \right\rfloor + 1 =", "3", font_size=40).move_to(READ)
        size[1].set_color(BLUE)
        self.begin(10)
        self.play(FadeOut(o2), FadeOut(o2_l), w.animate.move_to(window_at(h, 4, 0, 0)), run_time=0.8)
        self.at(0.3)
        self.play(Write(size), run_time=1.5)
        self.at(0.75)
        self.play(FadeIn(VGroup(*[c[0] for c in o1])), FadeIn(o1_l), run_time=0.8)
        self.end()
        self.begin(11)
        for c in range(3):
            self.at(0.15 + 0.27 * c)
            self.play(w.animate.move_to(window_at(h, 4, 0, c)), run_time=0.5)
            self.play(FadeIn(o1[c][1]), run_time=0.4)
        self.end()
        self.begin(12)
        for k, (r, c) in enumerate([(r, c) for r in (1, 2) for c in range(3)]):
            self.play(w.animate.move_to(window_at(h, 4, r, c)), FadeIn(o1[r * 3 + c][1]), run_time=0.5)
        self.end()
        eights = VGroup(*[SurroundingRectangle(o1[i], color=LOOK_HERE, buff=0, stroke_width=5) for i in range(9) if b_s1.flatten()[i] == 8])
        src = SurroundingRectangle(h[1 * 4 + 1], color=LOOK_HERE, buff=0, stroke_width=5)
        self.line(13, FadeOut(w), FadeOut(size), Create(src), LaggedStart(*[Create(e) for e in eights], lag_ratio=0.2), run_time=1.8, gap=1.5)
        self.clear_all()
