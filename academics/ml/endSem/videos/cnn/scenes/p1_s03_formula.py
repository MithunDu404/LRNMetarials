# p1_s03_formula.py: the double-sum formula, convolution vs cross-correlation, stencil steps. Coverage: C003, C012.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *


class P1S03Formula(CnnScene):
    def construct(self):
        image = np.array([[1, 2, 0, 1], [0, 1, 3, 1], [2, 1, 0, 0]])     # example values, as in the last scene
        C = image.shape[1]

        head = section_title("The rule, written once")
        img = grid(image.tolist()).move_to(LEFT * 4.6 + UP * 0.3)
        win = window_at(img, C, 0, 1)
        ij = MathTex("(i, j)", font_size=30, color=TOOL).next_to(win, UP, buff=0.15)
        note = Tex("example values", font_size=LABEL_SIZE, color=LABEL).next_to(img, DOWN, buff=0.3)

        f = MathTex("S(i,j)", "=", r"\sum_{m=0}^{M-1}\ \sum_{n=0}^{N-1}", r"I(i+m,\ j+n)", r"\,K(m,n)", font_size=44)
        f[0].set_color(RESULT)
        f[4].set_color(TOOL)
        f.move_to(RIGHT * 2.3 + UP * 0.5)
        if f.width > 7.4:
            f.scale_to_fit_width(7.4)
        plain = Tex(r"sum of kernel weights $\times$ the pixels under them", font_size=LABEL_SIZE,
                    color=LABEL).next_to(f, DOWN, buff=0.6)

        self.line(1, FadeIn(head), FadeIn(img), FadeIn(note), Create(win), run_time=1.5)
        self.line(2, Write(f[0]), FadeIn(ij), run_time=1.2)
        self.line(3, Write(f[1:3]), run_time=1.5)
        self.begin(4)
        self.play(Write(f[3]), Indicate(VGroup(*[img[i] for i in (1, 2, C + 1, C + 2)]), color=WHITE, scale_factor=1.05), run_time=1.6)
        self.at(0.6)
        self.play(Write(f[4]), Indicate(win, color=TOOL, scale_factor=1.08), run_time=1.3)
        self.end()
        self.line(5, FadeIn(plain), run_time=1, gap=1.5)

        # continuous convolution vs CNN cross-correlation (guide figure 1)
        self.play(*[FadeOut(m) for m in (img, win, ij, note, f, plain)], run_time=0.8)
        new_head = section_title("Convolution or cross-correlation?")
        cont_t = Tex("signal processing: convolution", font_size=LABEL_SIZE, color=LABEL)
        cont = MathTex(r"(f * g)(t)", "=", r"\int_{-\infty}^{\infty} f(\tau)\,", r"g(t-\tau)", r"\,d\tau", font_size=36)
        cont[3].set_color(TOOL)
        notes = VGroup(
            Tex(r"$g(-\tau)$: kernel is flipped", font_size=LABEL_SIZE, color=SOFT),
            Tex(r"$g(t-\tau)$: shifted by $t$", font_size=LABEL_SIZE, color=SOFT),
            Tex(r"$\int$: area of overlap", font_size=LABEL_SIZE, color=SOFT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        left = VGroup(cont_t, cont, notes).arrange(DOWN, buff=0.55)

        disc_t = Tex("CNN: cross-correlation", font_size=LABEL_SIZE, color=LABEL)
        disc = MathTex(r"(I * K)(i,j)", "=", r"\sum_{m}\sum_{n} I(i+m,\, j+n)\,", r"K(m,n)", font_size=36)
        disc[3].set_color(TOOL)
        dnotes = VGroup(
            Tex("kernel is not flipped", font_size=LABEL_SIZE, color=SOFT),
            Tex("shifts in whole pixels (stride)", font_size=LABEL_SIZE, color=SOFT),
            Tex(r"$\sum$: sum of products", font_size=LABEL_SIZE, color=SOFT),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        right = VGroup(disc_t, disc, dnotes).arrange(DOWN, buff=0.55)
        k = min(1.0, 6.0 / left.width, 6.0 / right.width)      # same scale on both sides
        for g, x in ((left, -3.55), (right, 3.55)):
            g.scale(k).move_to(RIGHT * x + DOWN * 0.2)
        right.align_to(left, UP)
        divider = Line(UP * 2, DOWN * 2.6, stroke_width=2, color=GUIDE)
        assert left.get_right()[0] < -0.3 and right.get_left()[0] > 0.3 and right.get_right()[0] < 6.61

        self.line(6, Transform(head, new_head), FadeIn(cont_t), Write(cont), run_time=2)
        self.begin(7)
        for k, frac in enumerate((0.0, 0.38, 0.62)):
            self.at(frac)
            self.play(FadeIn(notes[k], shift=UP * 0.2), run_time=0.8)
        self.end()
        self.begin(8)
        self.play(Create(divider), FadeIn(disc_t), Write(disc), run_time=2)
        self.play(FadeIn(dnotes[0], shift=UP * 0.2), run_time=0.7)
        self.at(0.3)
        self.play(FadeIn(dnotes[1], shift=UP * 0.2), FadeIn(dnotes[2], shift=UP * 0.2), run_time=0.8)
        self.at(0.55)
        self.play(Circumscribe(disc_t, color=LOOK_HERE), run_time=1)
        self.end(gap=1.2)

        # the stencil model, four steps
        self.play(*[FadeOut(m) for m in (left, right, divider)], run_time=0.8)
        stencil_head = section_title("The stencil model")
        flow, boxes, arrows = flow_boxes(["1. align the stencil", "2. multiply", r"3. sum, $+$ bias", "4. write the result"],
                                         size=30, buff=0.6)
        if flow.width > 13:
            flow.scale_to_fit_width(13)
        self.begin(9)
        self.play(Transform(head, stencil_head), run_time=0.8)
        for k, frac in enumerate((0.3, 0.47, 0.64, 0.82)):
            self.at(frac)
            anims = [FadeIn(boxes[k])] + ([GrowArrow(arrows[k - 1])] if k else [])
            self.play(*anims, run_time=0.8)
        self.end(gap=1.5)
        self.clear_all()
