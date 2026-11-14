# p1_s02_sliding.py: kernel, sliding window, dot product, feature map. Coverage: C004-C011, C013.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *


class P1S02Sliding(CnnScene):
    def construct(self):
        image = np.array([[1, 2, 0, 1], [0, 1, 3, 1], [2, 1, 0, 0]])     # example values
        kernel = np.array([[1, 0], [0, 1]])
        feature = correlate2d(image, kernel, mode="valid")
        assert feature.tolist() == [[2, 5, 1], [1, 1, 3]]
        R, C = image.shape
        F = kernel.shape[0]
        OR, OC = R - F + 1, C - F + 1
        assert (OR, OC) == feature.shape == (2, 3)
        Y = UP * 0.7
        READ = DOWN * 2.3

        # ---------- symbolic walk-through (slides 2-9) ----------
        head = section_title("Sliding the kernel")
        img = tex_grid([[f"I_{{{r+1}{c+1}}}" for c in range(C)] for r in range(R)]).move_to(LEFT * 1.4 + Y)
        ker = tex_grid([[f"K_{{{m+1}{n+1}}}" for n in range(F)] for m in range(F)],
                       border=TOOL, color=TOOL).move_to(LEFT * 5.3 + Y)
        out = tex_grid([[f"O_{{{r+1}{c+1}}}" for c in range(OC)] for r in range(OR)],
                       border=RESULT, color=RESULT).move_to(RIGHT * 4.2 + Y)
        img_l, ker_l = label_under(img, "image"), label_under(ker, "kernel")
        out_l = label_under(out, "feature map (activation map)")

        def sym_sum(r, c):
            parts = [f"O_{{{r+1}{c+1}}}", "="]
            for m in range(F):
                for n in range(F):
                    parts += [f"I_{{{r+m+1}{c+n+1}}}", f"K_{{{m+1}{n+1}}}", "+"]
            t = MathTex(*parts[:-1], font_size=38).move_to(READ)
            t[0].set_color(RESULT)
            for i in range(3, len(t), 3):
                t[i].set_color(TOOL)
            return t

        self.line(1, FadeIn(head), LaggedStart(*[Create(c) for c in img], lag_ratio=0.05), FadeIn(img_l), run_time=2)
        self.line(2, LaggedStart(*[Create(c) for c in ker], lag_ratio=0.1), FadeIn(ker_l), run_time=1.5)
        self.line(3, Indicate(ker, color=TOOL, scale_factor=1.1), run_time=1.5)
        win = window_at(img, C, 0, 0)
        self.line(4, Create(win), run_time=1)

        readout = sym_sum(0, 0)
        self.begin(5)
        self.at(0.22)
        self.play(Write(readout), run_time=min(6, self.left() - 0.5))
        self.end()
        frob = Tex("dot product (Frobenius inner product): one number", font_size=LABEL_SIZE,
                   color=LABEL).next_to(readout, DOWN, buff=0.35)
        self.line(6, FadeIn(frob), run_time=1)

        self.begin(7)
        self.play(FadeIn(VGroup(*[c[0] for c in out])), run_time=0.7)
        self.play(TransformFromCopy(readout[0], out[0][1]), run_time=0.9)
        self.end()

        self.begin(8)
        self.play(win.animate.move_to(window_at(img, C, 0, 1)), FadeOut(frob), run_time=0.9)
        self.play(Transform(readout, sym_sum(0, 1)), run_time=1.2)
        self.at(0.8)
        self.play(FadeIn(out[1][1]), run_time=0.8)
        self.end()

        self.begin(9)
        self.play(win.animate.move_to(window_at(img, C, 0, 2)), Transform(readout, sym_sum(0, 2)), run_time=1)
        self.play(FadeIn(out[2][1]), run_time=0.8)
        self.end()

        self.begin(10)
        self.play(FadeOut(readout), run_time=0.6)
        for r, c in ((1, 0), (1, 1), (1, 2)):
            self.play(win.animate.move_to(window_at(img, C, r, c)), FadeIn(out[r * OC + c][1]), run_time=0.7)
        self.end()

        stride = Tex("sliding window, stride $= 1$", font_size=BODY_SIZE, color=SOFT).move_to(READ)
        self.begin(11)
        self.at(0.2)
        self.play(FadeIn(stride), run_time=0.8)
        for r in range(OR):
            for c in range(OC):
                self.play(win.animate.move_to(window_at(img, C, r, c)), run_time=0.4)
        self.end()

        box = SurroundingRectangle(out, color=RESULT, buff=0.12, stroke_width=4)
        self.line(12, Create(box), FadeIn(out_l), run_time=1.2)

        flow, boxes, arrows = flow_boxes([r"patch $\times$ kernel", "sum", r"$+$ bias", "one cell"])
        flow.move_to(READ)
        order = [boxes[0], arrows[0], boxes[1], arrows[1], boxes[2], arrows[2], boxes[3]]
        self.begin(13)
        self.play(FadeOut(stride), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(m) for m in order], lag_ratio=0.4), run_time=3)
        self.end()

        # ---------- the same with numbers [added, example values] ----------
        self.begin(14)
        self.play(*[FadeOut(m) for m in (img, ker, out, img_l, ker_l, out_l, win, box, flow)], run_time=0.8)
        img2 = grid(image.tolist(), cell=0.9).move_to(img)
        ker2 = grid(kernel.tolist(), cell=0.9, border=TOOL, num_color=TOOL).move_to(ker)
        out2 = grid(feature.tolist(), cell=0.9, border=RESULT, num_color=RESULT).move_to(out)
        note = Tex("example values", font_size=LABEL_SIZE, color=LABEL).to_corner(DR, buff=0.5)
        self.play(FadeIn(img2), FadeIn(ker2), FadeIn(VGroup(*[c[0] for c in out2])), FadeIn(note), run_time=1)
        self.end()

        def num_sum(r, c):
            parts = []
            for m in range(F):
                for n in range(F):
                    parts += [rf"{image[r+m, c+n]} \cdot {kernel[m, n]}", "+"]
            t = MathTex(*parts[:-1], "=", str(feature[r, c]), font_size=40).move_to(READ)
            t[-1].set_color(RESULT)
            return t

        win2 = window_at(img2, C, 0, 0)
        read2 = num_sum(0, 0)
        self.begin(15)
        self.play(Create(win2), run_time=0.7)
        self.play(Write(read2), run_time=4)
        self.play(TransformFromCopy(read2[-1], out2[0][1]), run_time=0.8)
        self.end()

        self.begin(16)
        self.play(win2.animate.move_to(window_at(img2, C, 0, 1)), Transform(read2, num_sum(0, 1)), run_time=1.2)
        self.at(0.45)
        self.play(FadeIn(out2[1][1]), run_time=0.6)
        self.play(FadeOut(read2), run_time=0.5)
        for r, c in ((0, 2), (1, 0), (1, 1), (1, 2)):
            self.play(win2.animate.move_to(window_at(img2, C, r, c)), FadeIn(out2[r * OC + c][1]), run_time=0.5)
        self.end()

        s_in = MathTex(rf"{R} \times {C}", font_size=36, color=BLUE_B).next_to(img2, DOWN, buff=0.3)
        s_out = MathTex(rf"{OR} \times {OC}", font_size=36, color=BLUE).next_to(out2, DOWN, buff=0.3)
        self.line(17, FadeOut(win2), FadeIn(s_in), FadeIn(s_out), run_time=1)

        def size_line(a, b, n_in, n_out):
            t = MathTex(a, "=", b, "-", "F", "+ 1", "=", f"{n_in} - {F} + 1", "=", str(n_out), font_size=40)
            t[0].set_color(BLUE)
            t[2].set_color(BLUE_B)
            t[4].set_color(YELLOW)
            t[-1].set_color(BLUE)
            return t
        f1, f2 = size_line("H_2", "H_1", R, OR), size_line("W_2", "W_1", C, OC)
        VGroup(f1, f2).arrange(DOWN, buff=0.3).move_to(DOWN * 2.5)
        self.begin(18)
        self.at(0.42)
        self.play(Write(f1), run_time=1.5)
        self.at(0.72)
        self.play(Write(f2), run_time=1.5)
        self.end(gap=1.5)
        self.clear_all()
