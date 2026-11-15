# p1_s10_volumes.py: 1D convolution, 3D volumes, depth rule, K filters, parameters. Coverage: C055-C064.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *

FIG = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media" / "image43.png"
RGB = [RED_C, GREEN_C, BLUE_C]


class P1S10Volumes(CnnScene):
    def construct(self):
        seq = list("ABCBCAB")
        L = 3
        n1d = conv_out(len(seq), L)
        assert n1d == 5
        U, NIN, NF = 0.7, 4, 2                                   # drawing: 4x4 input, 2x2 filter (per sheet)
        NOUT = conv_out(NIN, NF)
        assert NOUT == 3

        head = section_title("Inputs with depth")
        self.line(1, FadeIn(head), run_time=0.8)

        row = tex_grid([seq[:5]], cell=0.5, size=24)
        rgb = sheets(1.5, 3, RGB)
        deep = sheets(1.5, 8, [GREY_C], step=0.09)
        trio = VGroup(VGroup(row), rgb, deep).arrange(RIGHT, buff=1.6)
        caps = VGroup(caption(row, "sequence: 1D"), caption(rgb, "colour image: depth 3"), caption(deep, "inside a CNN: depth $D_1$"))
        low = min(c.get_bottom()[1] for c in caps)
        for c in caps:
            c.shift(UP * (low - c.get_bottom()[1]))
        self.begin(2)
        for k, fr in enumerate((0.02, 0.2, 0.48)):
            self.at(fr)
            self.play(FadeIn(trio[k]), FadeIn(caps[k]), run_time=0.9)
        self.end()

        # 1D convolution
        self.clear_except(head)
        s = tex_grid([seq], cell=0.8, size=32).move_to(UP * 0.8)
        win = Rectangle(width=L * 0.8, height=0.8, stroke_color=TOOL, stroke_width=6).move_to(s[1])
        outs = blank_grid(1, n1d, cell=0.8, fill=RESULT, opacity=0.35, border=RESULT).move_to(DOWN * 1.2)
        o_l = caption(outs, f"{len(seq)} values, filter of length {L}: {n1d} outputs")
        self.begin(3)
        self.play(FadeIn(s), run_time=0.8)
        self.at(0.42)
        self.play(Create(win), run_time=0.7)
        self.play(FadeIn(outs[0]), run_time=0.4)
        for k in range(1, n1d):
            self.play(win.animate.move_to(s[k + 1]), FadeIn(outs[k]), run_time=0.6)
        self.play(FadeIn(o_l), run_time=0.5)
        self.end()

        # separate filters per channel: channels never mix
        self.clear_except(head)
        chans = VGroup(*[Square(1.5, stroke_color=GUIDE, stroke_width=2).set_fill(c, opacity=0.35) for c in RGB]).arrange(DOWN, buff=0.35).move_to(LEFT * 3.5 + DOWN * 0.3)
        kers = VGroup(*[Square(0.6, stroke_color=TOOL, stroke_width=4).move_to(c.get_corner(UL) + (RIGHT + DOWN) * 0.3) for c in chans])
        outs3 = VGroup(*[Square(1.1, stroke_color=RESULT, stroke_width=2).set_fill(RESULT, opacity=0.3).move_to(c.get_center() + RIGHT * 4) for c in chans])
        arrs = VGroup(*[arrow_between(c, o) for c, o in zip(chans, outs3)])
        nomix = Tex(r"three separate results:\\the channels never mix", font_size=LABEL_SIZE, color=LABEL).move_to(RIGHT * 4.2 + DOWN * 0.3)
        nomix.scale_to_fit_width(4.4)
        self.begin(4)
        self.play(FadeIn(chans), FadeIn(kers), run_time=1)
        self.at(0.3)
        self.play(FadeIn(arrs), FadeIn(outs3), run_time=1)
        self.at(0.55)
        self.play(FadeIn(nomix), run_time=0.8)
        self.end()

        # the filter is a volume
        self.clear_except(head)
        vol = sheets(NIN * U, 3, RGB).move_to(LEFT * 4.0 + DOWN * 0.1)
        front = vol[-1]
        w1 = MathTex("W_1", font_size=30, color=BLUE_B).next_to(front, DOWN, buff=0.15)
        h1 = MathTex("H_1", font_size=30, color=BLUE_B).next_to(front, LEFT, buff=0.15)
        d1 = MathTex("D_1", font_size=30, color=BLUE_B).next_to(vol, UR, buff=-0.1)
        filt = sheets(NF * U, 3, [TOOL], border=TOOL, opacity=0.25, width=3).move_to(RIGHT * 0.3 + DOWN * 0.1)
        ff = MathTex("F", r"\times", "F", r"\times", "D_1", font_size=32).next_to(filt, DOWN, buff=0.25)
        ff[0].set_color(YELLOW); ff[2].set_color(YELLOW); ff[4].set_color(BLUE_B)
        self.begin(5)
        self.play(FadeIn(vol), FadeIn(w1), FadeIn(h1), FadeIn(d1), run_time=1)
        self.at(0.5)
        self.play(FadeIn(filt), FadeIn(ff), run_time=1)
        self.end()
        rule = MathTex(r"\text{depth of filter}", "=", r"\text{depth of input}", "=", "D_1", font_size=36).move_to(DOWN * 2.6)
        rule[4].set_color(BLUE_B)
        self.line(6, FadeIn(rule), Circumscribe(ff[4], color=LOOK_HERE), Circumscribe(d1, color=LOOK_HERE), run_time=1.5)

        def filt_pos(r, c):                                       # filter front sheet on input cell block (r, c)
            return front.get_corner(UL) + RIGHT * (c + NF / 2) * U + DOWN * (r + NF / 2) * U + (filt.get_center() - filt[-1].get_center())
        self.begin(7)
        self.play(FadeOut(ff), FadeOut(rule), filt.animate.move_to(filt_pos(0, 0)), run_time=1.2)
        self.at(0.45)
        self.play(filt.animate.move_to(filt_pos(0, NOUT - 1)), run_time=1)
        self.play(filt.animate.move_to(filt_pos(NOUT - 1, NOUT - 1)), run_time=1)
        self.end()

        out = blank_grid(NOUT, NOUT, cell=0.6, fill=RESULT, opacity=0.4, border=RESULT).move_to(RIGHT * 1.6 + DOWN * 0.1)
        out_frame = VGroup(*[c.copy().set_fill(opacity=0) for c in out])
        self.begin(8)
        self.play(filt.animate.move_to(filt_pos(0, 0)), FadeIn(out_frame), run_time=1)
        self.at(0.6)
        self.play(TransformFromCopy(filt, out[0]), run_time=1)
        self.end()
        tri = MathTex(r"b + \sum_{c=1}^{D_1}\ \sum_{m=0}^{F-1}\ \sum_{n=0}^{F-1} I(x+m,\ y+n,\ c)\, K(m, n, c)", font_size=34).move_to(DOWN * 2.6)
        if tri.width > 12.5:
            tri.scale_to_fit_width(12.5)
        self.line(9, Write(tri), run_time=2.5)
        self.begin(10)
        k = 1
        for r in range(NOUT):
            for c in range(NOUT):
                if (r, c) == (0, 0):
                    continue
                self.play(filt.animate.move_to(filt_pos(r, c)), FadeIn(out[k]), run_time=0.3)
                k += 1
        self.end()

        # K filters -> depth K
        more = sheets(NOUT * 0.6, 5, [RESULT], border=RESULT, opacity=0.4, step=0.16)
        more.shift(out.get_center() - more[-1].get_center())
        d2 = MathTex("D_2", "=", "K", font_size=40).next_to(more, RIGHT, buff=0.5)
        d2[0].set_color(BLUE); d2[2].set_color(GREEN_C)
        kf = MathTex("K", r"\ \text{filters, one map each}", font_size=32).next_to(more, UP, buff=0.3)
        kf[0].set_color(GREEN_C)
        self.begin(11)
        self.play(FadeOut(tri), FadeOut(filt), run_time=0.6)
        self.at(0.2)
        self.play(FadeIn(kf), LaggedStart(*[FadeIn(m) for m in list(more)[:-1][::-1]], lag_ratio=0.3), run_time=2)
        self.at(0.75)
        self.play(FadeIn(d2), run_time=0.8)
        self.end()

        self.clear_except(head)
        fig = ImageMobject(str(FIG)).scale_to_fit_height(5.6).move_to(DOWN * 0.4)
        fig_l = Tex("lecture slide figure", font_size=LABEL_SIZE, color=LABEL).next_to(fig, RIGHT, buff=0.4)
        self.line(12, FadeIn(fig), FadeIn(fig_l), run_time=1, gap=0.8)

        self.play(FadeOut(fig), FadeOut(fig_l), run_time=0.6)
        full = MathTex(r"O(i, j, k) = b_k + \sum_{c=1}^{D_1}\ \sum_{m=0}^{F-1}\ \sum_{n=0}^{F-1} I(i+m,\ j+n,\ c)\, K_k(m, n, c)", font_size=36).move_to(UP * 1.2)
        if full.width > 12.5:
            full.scale_to_fit_width(12.5)
        self.line(13, Write(full), run_time=2.5)
        p1 = MathTex(r"\text{parameters}", "=", "K", r"\,(", "F", r"^2", "D_1", "+ 1)", font_size=42)
        p2 = MathTex(r"\text{without biases}", "=", "K", r"\cdot", "F", r"^2 \cdot", "D_1", font_size=36)
        for p in (p1, p2):
            p[2].set_color(GREEN_C); p[4].set_color(YELLOW); p[6].set_color(BLUE_B)
        VGroup(p1, p2).arrange(DOWN, buff=0.5).move_to(DOWN * 1.5)
        self.begin(14)
        self.at(0.4)
        self.play(Write(p1), run_time=1.5)
        self.at(0.8)
        self.play(FadeIn(p2), run_time=0.8)
        self.end(gap=1.5)
        self.clear_all()
