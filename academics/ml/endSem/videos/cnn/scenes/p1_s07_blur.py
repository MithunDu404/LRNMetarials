# p1_s07_blur.py: Gaussian and average kernels, slide 21 correction. Coverage: C034-C038, C048-C050.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *


class P1S07Blur(CnnScene):
    def construct(self):
        img = np.zeros((8, 8))
        img[2:6, 2:6] = 1                                      # example values
        g3 = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
        v = np.array([1, 4, 6, 4, 1])
        g5 = np.outer(v, v)
        assert g3.sum() == 16 and g5.sum() == 256
        assert g5.tolist() == [[1, 4, 6, 4, 1], [4, 16, 24, 16, 4], [6, 24, 36, 24, 6], [4, 16, 24, 16, 4], [1, 4, 6, 4, 1]]
        b3, b5 = np.ones((3, 3)), np.ones((5, 5))
        assert b3.sum() == 9 and b5.sum() == 25
        assert np.isclose((g3 / 16).sum(), 1) and np.isclose((g5 / 256).sum(), 1) and np.isclose((b3 / 9).sum(), 1)
        blur_g = correlate2d(img, g3 / 16, mode="valid")
        blur_b = correlate2d(img, b3 / 9, mode="valid")
        assert 0 < blur_g[0, 0] < 1 and 0 < blur_b[0, 0] < 1 and np.isclose(blur_g[2, 2], 1)

        head = section_title("Classic kernels: blurring")
        pic = gray_map(img.tolist(), vmax=1).move_to(LEFT * 4.9 + DOWN * 0.1)
        pic_l = caption(pic, "test image (example values)")
        hood = Square(3 * 0.4, stroke_color=TOOL, stroke_width=6).move_to(pic[2 * 8 + 2])
        self.line(1, FadeIn(head), FadeIn(pic), FadeIn(pic_l), Create(hood), run_time=1.5)

        f = MathTex(r"G(x, y) = \frac{1}{2\pi\sigma^2}\, e^{-\frac{x^2 + y^2}{2\sigma^2}}", font_size=44).move_to(RIGHT * 1.9 + UP * 1.5)
        self.line(2, Write(f), run_time=2.5)
        sigma = 1.0
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.1, 1], x_length=5.5, y_length=2.0, tips=False,
                  axis_config={"color": LABEL, "stroke_width": 2, "include_ticks": False}).move_to(RIGHT * 1.9 + DOWN * 1.3)
        curve = ax.plot(lambda x: np.exp(-x ** 2 / (2 * sigma ** 2)), color=TOOL, stroke_width=4)
        s_line = DoubleArrow(ax.c2p(0, 0.45), ax.c2p(sigma, 0.45), buff=0, stroke_width=3, color=LABEL, tip_length=0.15)
        s_lab = MathTex(r"\sigma", font_size=32).next_to(s_line, UP, buff=0.08)
        ax_l = caption(ax, "weight against distance from the centre")
        self.begin(3)
        self.play(Create(ax), Create(curve), FadeIn(ax_l), run_time=1.5)
        self.at(0.6)
        self.play(GrowFromCenter(s_line), FadeIn(s_lab), run_time=0.8)
        self.end()

        # 3x3 and 5x5 Gaussian kernels
        self.clear_except(head, pic, pic_l)
        k3 = frac_kernel(r"\frac{1}{16}", g3.tolist(), cell=0.7).move_to(LEFT * 0.9 + UP * 0.2)
        k3_s = MathTex(rf"\text{{entries add up to }} {g3.sum()}", font_size=30).next_to(k3, DOWN, buff=0.35)
        self.begin(4)
        self.play(LaggedStart(*[FadeIn(c) for c in k3[1]], lag_ratio=0.08), run_time=1.5)
        self.at(0.5)
        self.play(FadeIn(k3_s), run_time=0.7)
        self.at(0.7)
        self.play(FadeIn(k3[0]), run_time=0.7)
        self.end()
        k3_l = caption(k3_s, "low-pass filter")
        self.line(5, FadeIn(k3_l), run_time=0.8)

        k5 = frac_kernel(r"\frac{1}{256}", g5.tolist(), cell=0.55, size=22).move_to(RIGHT * 4.1 + UP * 0.2)
        vec = MathTex(r"[1\ 4\ 6\ 4\ 1]^T\,[1\ 4\ 6\ 4\ 1]", font_size=30).next_to(k5, UP, buff=0.35)
        k5_s = MathTex(rf"\text{{entries add up to }} {g5.sum()}", font_size=30).next_to(k5, DOWN, buff=0.35)
        assert k5.get_right()[0] < 6.61 and k5.get_left()[0] > k3.get_right()[0] + 0.3
        self.begin(6)
        self.play(FadeIn(vec), run_time=0.8)
        self.at(0.25)
        self.play(LaggedStart(*[FadeIn(c) for c in k5[1]], lag_ratio=0.03), run_time=1.5)
        self.at(0.62)
        self.play(FadeIn(k5_s), FadeIn(k5[0]), run_time=0.8)
        self.end()
        k5_l = caption(k5_s, r"binomial approximation, $\sigma \approx 1$")
        self.line(7, FadeIn(k5_l), run_time=0.8)

        # average / box
        self.clear_except(head, pic, pic_l)
        a3 = frac_kernel(r"\frac{1}{9}", b3.astype(int).tolist(), cell=0.7).move_to(LEFT * 0.9 + UP * 0.2)
        a5 = frac_kernel(r"\frac{1}{25}", b5.astype(int).tolist(), cell=0.55, size=22).move_to(RIGHT * 4.1 + UP * 0.2)
        a_t = Tex("average (box) kernels: every weight equal", font_size=LABEL_SIZE, color=LABEL).move_to(RIGHT * 1.7 + UP * 2.3)
        self.begin(8)
        self.play(FadeIn(a_t), run_time=0.8)
        self.at(0.3)
        self.play(FadeIn(a3), run_time=0.8)
        self.at(0.5)
        self.play(FadeIn(a5), run_time=0.8)
        self.end()
        a_l = Tex("no distance weighting: blurs edges heavily", font_size=LABEL_SIZE, color=LABEL).move_to(RIGHT * 1.7 + DOWN * 2.2)
        self.line(9, FadeIn(a_l), run_time=0.8)

        # results on the test image
        self.clear_except(head, pic, pic_l)
        rg = gray_map(blur_g.tolist(), vmax=1).move_to(LEFT * 0.4 + DOWN * 0.1)
        rb = gray_map(blur_b.tolist(), vmax=1).move_to(RIGHT * 3.6 + DOWN * 0.1)
        rg_l, rb_l = caption(rg, r"Gaussian $3 \times 3$"), caption(rb, r"average $3 \times 3$")
        self.line(10, FadeIn(rg), FadeIn(rg_l), FadeIn(rb), FadeIn(rb_l), run_time=1.2)

        # slide 21 correction
        self.clear_except(head)
        fix_head = section_title("Correction to slide 21")
        wrong = frac_kernel(r"\frac{1}{9}", b3.astype(int).tolist(), cell=0.7).move_to(LEFT * 2.6)
        w_lab = Tex("``A $3 \\times 3$ Gaussian Kernel''", font_size=30, color=SOFT).next_to(wrong, UP, buff=0.4)
        strike = Line(w_lab.get_left(), w_lab.get_right(), stroke_width=4, color=NEG)
        right_lab = Tex("average (box) kernel", font_size=30, color=INK).next_to(wrong, DOWN, buff=0.4)
        right_box = SurroundingRectangle(right_lab, color=LOOK_HERE, buff=0.15, stroke_width=4)
        real = frac_kernel(r"\frac{1}{16}", g3.tolist(), cell=0.7).move_to(RIGHT * 3.3)
        real_l = Tex("a Gaussian kernel: larger near the centre", font_size=LABEL_SIZE, color=LABEL).next_to(real, DOWN, buff=0.4)
        self.begin(11)
        self.play(Transform(head, fix_head), FadeIn(wrong), FadeIn(w_lab), run_time=1.2)
        self.at(0.45)
        self.play(Create(strike), FadeIn(right_lab), Create(right_box), run_time=1)
        self.at(0.75)
        self.play(FadeIn(real), FadeIn(real_l), run_time=1)
        self.end(gap=1.5)
        self.clear_all()
