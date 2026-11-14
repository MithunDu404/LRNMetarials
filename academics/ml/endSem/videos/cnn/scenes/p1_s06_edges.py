# p1_s06_edges.py: hand-made kernels, Sobel, gradient magnitude, Canny. Coverage: C030-C033, C046, C047.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *


class P1S06Edges(CnnScene):
    def construct(self):
        img = np.zeros((8, 8))
        img[2:6, 2:6] = 1                                      # example values: bright square on dark
        Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        Gy = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])
        assert Gx.sum() == 0 and Gy.sum() == 0
        assert (Gy == -Gx.T).all()
        assert Gx[:, 2].tolist() == [1, 2, 1]
        gx = correlate2d(img, Gx, mode="valid")
        gy = correlate2d(img, Gy, mode="valid")
        mag = np.sqrt(gx ** 2 + gy ** 2)
        assert correlate2d(np.ones((5, 5)), Gx, mode="valid").any() == False      # flat region: no response
        assert gx[2, 0] > 0 and gx[2, -1] < 0 and gx[2, 2] == 0                    # left / right sides only
        assert gy[0, 2] != 0 and gy[-1, 2] != 0 and gy[2, 2] == 0                  # top / bottom sides only
        ridge = np.array([1, 3, 5, 3, 1])
        keep = [(i == 0 or ridge[i] > ridge[i - 1]) and (i == len(ridge) - 1 or ridge[i] > ridge[i + 1]) for i in range(len(ridge))]
        assert keep == [False, False, True, False, False]

        head = section_title("Classic kernels: finding edges")
        jobs = VGroup(*[body(t) for t in ("find edges", "blur away noise", "sharpen detail")]).arrange(RIGHT, buff=1.2)
        self.begin(1)
        self.play(FadeIn(head), run_time=0.8)
        for k, fr in enumerate((0.45, 0.68, 0.85)):
            self.at(fr)
            self.play(FadeIn(jobs[k], shift=UP * 0.2), run_time=0.7)
        self.end()
        self.line(2)

        # Sobel
        pic = gray_map(img.tolist(), vmax=1).move_to(LEFT * 4.7 + DOWN * 0.1)
        pic_l = caption(pic, "test image (example values)")
        kx = kernel_grid(Gx.tolist(), cell=0.7).move_to(LEFT * 0.4 + DOWN * 0.1)
        ky = kernel_grid(Gy.tolist(), cell=0.7).move_to(RIGHT * 3.6 + DOWN * 0.1)
        kx_l = caption(kx, "Sobel $G_x$: right $-$ left", UP)
        ky_l = caption(ky, "Sobel $G_y$: top $-$ bottom", UP)
        self.line(3, FadeOut(jobs), FadeIn(pic), FadeIn(pic_l), run_time=1.2)
        self.line(4, LaggedStart(*[FadeIn(c) for c in kx], lag_ratio=0.08), FadeIn(kx_l), run_time=1.5)
        col = SurroundingRectangle(VGroup(kx[2], kx[8]), color=LOOK_HERE, buff=0, stroke_width=6)
        kx_use = caption(kx, "responds to vertical edges")
        self.begin(5)
        self.play(FadeIn(kx_use), run_time=0.8)
        self.at(0.3)
        self.play(Create(col), run_time=0.8)
        self.end()
        ky_use = caption(ky, "responds to horizontal edges")
        self.line(6, FadeOut(col), LaggedStart(*[FadeIn(c) for c in ky], lag_ratio=0.08), FadeIn(ky_l), FadeIn(ky_use), run_time=1.5)
        sx = MathTex(rf"\text{{sum}} = {Gx.sum()}", font_size=32).next_to(kx_use, DOWN, buff=0.3)
        sy = MathTex(rf"\text{{sum}} = {Gy.sum()}", font_size=32).next_to(ky_use, DOWN, buff=0.3)
        self.line(7, FadeIn(sx), FadeIn(sy), run_time=1)

        # responses on the test image
        rx = signed_map(gx.tolist()).move_to(kx).shift(DOWN * 0.1)
        ry = signed_map(gy.tolist()).move_to(ky).shift(DOWN * 0.1)
        rx_l, ry_l = caption(rx, "$G_x$ response"), caption(ry, "$G_y$ response")
        self.begin(8)
        self.play(*[FadeOut(m) for m in (kx, ky, kx_l, ky_l, kx_use, ky_use, sx, sy)], run_time=0.7)
        self.at(0.45)
        self.play(FadeIn(rx), FadeIn(rx_l), run_time=0.9)
        self.at(0.75)
        self.play(FadeIn(ry), FadeIn(ry_l), run_time=0.9)
        self.end()

        rm = gray_map(mag.tolist()).move_to(rx)
        rm_l = caption(rm, "edge strength $G$")
        f_mag = MathTex("G", "=", r"\sqrt{G_x^2 + G_y^2}", font_size=44)
        f_ang = MathTex(r"\theta", "=", r"\arctan\!\left(\frac{G_y}{G_x}\right)", font_size=44)
        VGroup(f_mag, f_ang).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(RIGHT * 3.7 + DOWN * 0.1)
        self.begin(9)
        self.play(FadeOut(ry), FadeOut(ry_l), FadeOut(rx_l), Transform(rx, rm), FadeIn(rm_l), run_time=1.2)
        self.at(0.2)
        self.play(Write(f_mag), run_time=1.5)
        self.at(0.62)
        self.play(Write(f_ang), run_time=1.5)
        self.end(gap=1.2)

        # Canny
        self.clear_except(head)
        canny = section_title("Canny: a pipeline of four stages")
        names = ["1. Gaussian smoothing", "2. Sobel gradient", "3. Non-maximum suppression", "4. Hysteresis thresholds"]
        flow, boxes, arrows = flow_boxes(names, size=26, buff=0.5)
        flow.scale_to_fit_width(13).move_to(UP * 1.3)
        frames = VGroup(*[b[0] for b in boxes])
        self.line(10, Transform(head, canny), FadeIn(frames), FadeIn(arrows), run_time=1.5)
        self.line(11, FadeIn(boxes[0][1]), run_time=0.8)
        self.line(12, FadeIn(boxes[1][1]), run_time=0.8)

        thick = grid([ridge.tolist()], cell=0.7).move_to(DOWN * 1.3)
        thick_l = caption(thick, "gradient strength across an edge (example values)")
        self.begin(13)
        self.play(FadeIn(boxes[2][1]), FadeIn(thick), FadeIn(thick_l), run_time=1)
        self.at(0.55)
        peak = SurroundingRectangle(thick[keep.index(True)], color=LOOK_HERE, buff=0, stroke_width=6)
        self.play(*[thick[i].animate.set_opacity(0.2) for i, k in enumerate(keep) if not k], Create(peak), run_time=1)
        self.end()

        self.play(FadeOut(thick), FadeOut(thick_l), FadeOut(peak), run_time=0.7)
        axis = Line(LEFT * 5, RIGHT * 5, stroke_width=4, color=LABEL).move_to(DOWN * 1.6)
        lo, hi = axis.point_from_proportion(0.33), axis.point_from_proportion(0.67)
        ticks = VGroup(*[Line(p + UP * 0.18, p + DOWN * 0.18, stroke_width=4, color=INK) for p in (lo, hi)])
        t_lo = MathTex(r"T_{\text{low}}", font_size=34).next_to(ticks[0], DOWN, buff=0.2)
        t_hi = MathTex(r"T_{\text{high}}", font_size=34).next_to(ticks[1], DOWN, buff=0.2)
        g_lab = MathTex("G", font_size=34).next_to(axis, RIGHT, buff=0.2)
        self.line(14, FadeIn(boxes[3][1]), Create(axis), FadeIn(ticks), FadeIn(t_lo), FadeIn(t_hi), FadeIn(g_lab), run_time=1.5)
        zones = VGroup(
            Tex("discard", font_size=LABEL_SIZE, color=DIM).move_to(axis.point_from_proportion(0.165) + UP * 0.55),
            Tex(r"weak: keep only if\\connected to a strong edge", font_size=24, color=SOFT).move_to(axis.point_from_proportion(0.5) + UP * 0.7),
            Tex("strong edge", font_size=LABEL_SIZE, color=RESULT).move_to(axis.point_from_proportion(0.835) + UP * 0.55),
        )
        self.reveal(15, [zones[2], zones[1], zones[0]], fracs=[0.05, 0.3, 0.68], gap=1.5)
        self.clear_all()
