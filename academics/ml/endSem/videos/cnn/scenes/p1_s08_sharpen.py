# p1_s08_sharpen.py: Laplacian, unsharp mask, kernel families. Coverage: C039-C041, C044, C045, C051-C053.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *

TAJ = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media" / "image27.png"


class P1S08Sharpen(CnnScene):
    def construct(self):
        lap4 = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        lap8 = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]])
        ident = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        unsharp = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        assert lap4.sum() == 0 and lap8.sum() == 0 and unsharp.sum() == 1
        assert (ident + lap4 == unsharp).all()
        # sign check on f(x, y) = x^2, whose true Laplacian is +2
        xs = np.tile(np.arange(5.0) ** 2, (5, 1))
        assert correlate2d(xs, lap8, mode="valid")[1, 1] > 0        # centre -8: usual (positive) sign
        assert correlate2d(xs, lap4, mode="valid")[1, 1] < 0        # centre +4: the negative
        flat = np.full((3, 3), 5)
        flat_lap = int((flat * lap4).sum())
        flat_un = int((flat * unsharp).sum())
        assert (flat_lap, flat_un) == (0, 5)

        head = section_title("Classic kernels: sharpening")
        idea = body("built on the second derivative")
        self.line(1, FadeIn(head), FadeIn(idea), run_time=1)
        f = MathTex(r"\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}", font_size=44).move_to(UP * 2.0)
        self.line(2, FadeOut(idea), Write(f), run_time=2)

        k4 = kernel_grid(lap4.tolist(), cell=0.75).move_to(LEFT * 3.2 + DOWN * 0.4)
        k8 = kernel_grid(lap8.tolist(), cell=0.75).move_to(RIGHT * 3.2 + DOWN * 0.4)
        k4_l, k8_l = caption(k4, "4-neighbour Laplacian", UP), caption(k8, "8-neighbour Laplacian", UP)
        s4 = MathTex(rf"\text{{sum}} = {lap4.sum()}", font_size=32).next_to(k4, DOWN, buff=0.3)
        s8 = MathTex(rf"\text{{sum}} = {lap8.sum()}", font_size=32).next_to(k8, DOWN, buff=0.3)
        self.begin(3)
        self.play(FadeIn(k4), FadeIn(k4_l), run_time=1)
        self.at(0.55)
        self.play(FadeIn(s4), run_time=0.7)
        self.end()
        self.begin(4)
        self.play(FadeIn(k8), FadeIn(k8_l), run_time=1)
        self.at(0.5)
        self.play(FadeIn(s8), run_time=0.7)
        self.end()

        n4 = MathTex(r"-\nabla^2", r"\ \text{(the negative)}", font_size=32).next_to(s4, DOWN, buff=0.3)
        n8 = MathTex(r"\nabla^2", r"\ \text{(usual sign)}", font_size=32).next_to(s8, DOWN, buff=0.3)
        fix = Tex("sign note: the guide calls the $-8$ kernel ``inverted''", font_size=LABEL_SIZE, color=SOFT).move_to(DOWN * 3.2)
        fix_box = SurroundingRectangle(VGroup(n4, n8), color=LOOK_HERE, buff=0.15, stroke_width=3)
        self.begin(5)
        self.play(FadeIn(fix), run_time=0.8)
        self.at(0.3)
        self.play(FadeIn(n8), run_time=0.8)
        self.at(0.55)
        self.play(FadeIn(n4), Create(fix_box), run_time=0.8)
        self.end()

        self.clear_except(head)
        taj = ImageMobject(str(TAJ))
        taj.scale_to_fit_width(10.5).move_to(DOWN * 0.3)
        taj_l = Tex("lecture slide figure", font_size=LABEL_SIZE, color=LABEL).next_to(taj, DOWN, buff=0.2)
        self.line(6, FadeIn(taj), FadeIn(taj_l), run_time=1.2, gap=1)

        # unsharp masking
        self.play(FadeOut(taj), FadeOut(taj_l), run_time=0.7)
        um = MathTex(r"I_{\text{sharp}} = I + \alpha\,(I - I_{\text{blur}})", font_size=44).move_to(UP * 2.0)
        self.begin(7)
        self.at(0.15)
        self.play(Write(um), run_time=2.5)
        self.end()
        ku = kernel_grid(unsharp.tolist(), cell=0.75).move_to(RIGHT * 3.6 + DOWN * 0.5)
        ku_l = caption(ku, "unsharp mask", UP)
        self.line(8, FadeIn(ku), FadeIn(ku_l), run_time=1)
        ki = kernel_grid(ident.tolist(), cell=0.75).move_to(LEFT * 4.4 + DOWN * 0.5)
        kl = kernel_grid(lap4.tolist(), cell=0.75).move_to(LEFT * 0.4 + DOWN * 0.5)
        plus = MathTex("+", font_size=48).move_to((ki.get_right() + kl.get_left()) / 2)
        eq = MathTex("=", font_size=48).move_to((kl.get_right() + ku.get_left()) / 2)
        ki_l, kl_l = caption(ki, "identity", UP), caption(kl, "Laplacian", UP)
        self.begin(9)
        self.at(0.25)
        self.play(FadeIn(ki), FadeIn(ki_l), run_time=0.8)
        self.at(0.6)
        self.play(FadeIn(plus), FadeIn(kl), FadeIn(kl_l), FadeIn(eq), run_time=0.8)
        self.end()
        sl = Tex(rf"sum {lap4.sum()}: flat regions go black", font_size=LABEL_SIZE, color=LABEL).next_to(kl, DOWN, buff=0.3)
        su = Tex(rf"sum {unsharp.sum()}: brightness is kept", font_size=LABEL_SIZE, color=LABEL).next_to(ku, DOWN, buff=0.3)
        self.begin(10)
        self.play(Indicate(ki[4], color=POS, scale_factor=1.3), run_time=1)
        self.at(0.25)
        self.play(FadeIn(sl), run_time=0.8)
        self.at(0.62)
        self.play(FadeIn(su), run_time=0.8)
        self.end()

        # flat patch check
        self.clear_except(head)
        patch = grid(flat.tolist(), cell=0.7).move_to(LEFT * 3.6 + DOWN * 0.2)
        patch_l = caption(patch, "flat patch (example values)")
        r1 = MathTex(r"\text{Laplacian} \ \rightarrow\ ", str(flat_lap), font_size=44)
        r2 = MathTex(r"\text{unsharp mask} \ \rightarrow\ ", str(flat_un), font_size=44)
        r1[1].set_color(RESULT); r2[1].set_color(RESULT)
        VGroup(r1, r2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to(RIGHT * 2.6 + DOWN * 0.2)
        self.begin(11)
        self.play(FadeIn(patch), FadeIn(patch_l), run_time=0.8)
        self.at(0.4)
        self.play(FadeIn(r1), run_time=0.8)
        self.at(0.68)
        self.play(FadeIn(r2), run_time=0.8)
        self.end()

        # three families
        self.clear_except(head)
        fam_head = section_title("Three families of classic kernels")
        cols = VGroup(*[VGroup(Tex(t, font_size=40, color=INK), Tex(s, font_size=32, color=c), Tex(d, font_size=30, color=SOFT)).arrange(DOWN, buff=0.5)
                        for t, s, c, d in (("Smoothing", "sum $= 1$", LABEL, r"Gaussian, box"),
                                           ("Edges", "sum $= 0$", LABEL, r"Sobel (1st derivative)\\Laplacian (2nd derivative)"),
                                           ("Sharpening", "sum $= 1$", LABEL, r"unsharp mask $=$\\identity $+$ Laplacian"))])
        cols.arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to(DOWN * 0.2)
        assert cols.width < 13
        self.begin(12)
        self.play(Transform(head, fam_head), run_time=0.8)
        for k, fr in enumerate((0.22, 0.42, 0.72)):
            self.at(fr)
            self.play(FadeIn(cols[k], shift=UP * 0.2), run_time=0.8)
        self.end(gap=1.5)
        self.clear_all()
