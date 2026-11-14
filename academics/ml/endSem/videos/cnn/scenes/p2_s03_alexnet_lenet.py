# p2_s03_alexnet_lenet.py: AlexNet conv1 and LeNet-5 conv1, sizes and parameters. Coverage: C070-C076.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *

MEDIA = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media"


def n(x):
    return f"{x:,}".replace(",", "{,}")


class Layer:
    def __init__(self, W, D, F, K, S, P):
        self.W, self.D, self.F, self.K, self.S, self.P = W, D, F, K, S, P
        assert (W - F + 2 * P) % S == 0
        self.W2 = conv_out(W, F, P, S)
        self.per = F * F * D
        self.weights = K * self.per
        self.params = K * (self.per + 1)
        self.acts = self.W2 * self.W2 * K


class P2S03AlexnetLenet(CnnScene):
    def construct(self):
        alex, lenet = Layer(227, 3, 11, 96, 4, 0), Layer(32, 1, 5, 6, 1, 0)
        assert (alex.W2, alex.per, alex.weights, alex.params, alex.acts) == (55, 363, 34848, 34944, 290400)
        assert (lenet.W2, lenet.per, lenet.weights, lenet.params, lenet.acts) == (28, 25, 150, 156, 4704)

        head = section_title("Two classic first layers")
        names = VGroup(Tex("AlexNet (2012): colour image, stride 4", font_size=BODY_SIZE, color=SOFT),
                       Tex("LeNet-5 (1998): greyscale image, stride 1", font_size=BODY_SIZE, color=SOFT)).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.begin(1)
        self.play(FadeIn(head), run_time=0.8)
        self.at(0.3)
        self.play(FadeIn(names[0]), FadeIn(names[1]), run_time=1)
        self.end()

        def size_part(first, L, title, colors, fig):
            self.clear_except(head)
            new = section_title(title)
            vol = sheets(1.6, L.D, colors).move_to(LEFT * 4.3 + UP * 0.9)
            v_l = MathTex(rf"{L.W} \times {L.W} \times {L.D}", font_size=38, color=BLUE_B).next_to(vol, DOWN, buff=0.35)
            hyp = MathTex("F", f"= {L.F},\\ ", "K", f"= {L.K},\\ ", "S", f"= {L.S},\\ ", "P", f"= {L.P}", font_size=36).move_to(LEFT * 4.0 + DOWN * 1.9)
            for i, c in zip((0, 2, 4, 6), (YELLOW, GREEN_C, PURPLE_B, GREY_B)):
                hyp[i].set_color(c)
            self.line(first, Transform(head, new), FadeIn(vol), FadeIn(v_l), run_time=1.2)
            self.line(first + 1, FadeIn(hyp), run_time=1)
            calc = MathTex(rf"W_2 = \frac{{{L.W} - {L.F} + 2({L.P})}}{{{L.S}}} + 1", rf"= \frac{{{L.W - L.F}}}{{{L.S}}} + 1",
                           rf"= {(L.W - L.F) // L.S} + 1", "=", str(L.W2), font_size=36)
            calc[4].set_color(BLUE)
            calc.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            calc[3:].arrange(RIGHT, buff=0.15).next_to(calc[2], DOWN, buff=0.35, aligned_edge=LEFT)
            calc.move_to(RIGHT * 2.9 + UP * 0.4)
            self.begin(first + 2)
            self.play(Write(calc[0]), run_time=1.5)
            self.at(0.35)
            self.play(FadeIn(calc[1]), run_time=0.7)
            self.at(0.55)
            self.play(FadeIn(calc[2]), run_time=0.7)
            self.at(0.75)
            self.play(FadeIn(calc[3:]), run_time=0.7)
            self.end()
            out = MathTex(rf"\text{{output: }}{L.W2} \times {L.W2} \times {L.K}", font_size=42, color=BLUE).move_to(UP * 2.2 + RIGHT * 1.5)
            pic = ImageMobject(str(MEDIA / fig)).scale_to_fit_width(9.5).move_to(DOWN * 0.8)
            pic_l = Tex("lecture slide figure", font_size=LABEL_SIZE, color=LABEL).next_to(pic, DOWN, buff=0.15)
            self.begin(first + 3)
            self.play(*[FadeOut(m) for m in (vol, v_l, hyp, calc)], run_time=0.6)
            self.play(FadeIn(out), FadeIn(pic), FadeIn(pic_l), run_time=1)
            self.end(gap=0.8)
            self.play(FadeOut(pic), FadeOut(pic_l), FadeOut(out), run_time=0.6)

        def param_lines(L):
            rows = VGroup(
                MathTex(rf"{L.F} \times {L.F} \times {L.D} = {L.per}\ \text{{weights per filter}}", font_size=38),
                MathTex(rf"{L.per} + 1\ \text{{bias}} = {L.per + 1}", font_size=38),
                MathTex(rf"{L.K} \times {L.per + 1} =", n(L.params), r"\ \text{parameters}", font_size=42),
                MathTex(rf"{L.K} \times {L.per} = {n(L.weights)}\ \text{{weights only}}", font_size=34, color=GREY_A),
                MathTex(rf"{L.W2} \times {L.W2} \times {L.K} =", n(L.acts), r"\ \text{output values}", font_size=38),
            ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.3)
            rows[2][1].set_color(GREEN_C)
            rows[4][1].set_color(BLUE)
            return rows

        # AlexNet: lines 2-8
        size_part(2, alex, "AlexNet, first layer", [RED_C, GREEN_C, BLUE_C], "image48.png")
        ra = param_lines(alex)
        self.begin(6)
        self.at(0.2)
        self.play(FadeIn(ra[0]), run_time=0.8)
        self.at(0.7)
        self.play(FadeIn(ra[1]), run_time=0.8)
        self.end()
        self.begin(7)
        self.play(FadeIn(ra[2]), run_time=0.8)
        self.at(0.6)
        self.play(FadeIn(ra[3]), run_time=0.8)
        self.end()
        self.line(8, FadeIn(ra[4]), run_time=1, gap=1)

        # LeNet-5: lines 9-13
        self.clear_except(head)
        new = section_title("LeNet-5, first layer")
        vol = sheets(1.6, 1, [GREY_C]).move_to(LEFT * 4.3 + UP * 0.9)
        v_l = MathTex(rf"{lenet.W} \times {lenet.W} \times {lenet.D}", font_size=38, color=BLUE_B).next_to(vol, DOWN, buff=0.35)
        hyp = MathTex("F", f"= {lenet.F},\\ ", "K", f"= {lenet.K},\\ ", "S", f"= {lenet.S},\\ ", "P", f"= {lenet.P}", font_size=36).move_to(LEFT * 4.0 + DOWN * 1.9)
        for i, c in zip((0, 2, 4, 6), (YELLOW, GREEN_C, PURPLE_B, GREY_B)):
            hyp[i].set_color(c)
        self.line(9, Transform(head, new), FadeIn(vol), FadeIn(v_l), run_time=1.2)
        self.line(10, FadeIn(hyp), run_time=1)
        calc = MathTex(rf"W_2 = \frac{{{lenet.W} - {lenet.F} + 2({lenet.P})}}{{{lenet.S}}} + 1 = {lenet.W - lenet.F} + 1 =", str(lenet.W2), font_size=36)
        calc[1].set_color(BLUE)
        calc.scale_to_fit_width(6.2).move_to(RIGHT * 3.2 + UP * 1.6)
        out = MathTex(rf"\text{{output: }}{lenet.W2} \times {lenet.W2} \times {lenet.K}", font_size=40, color=BLUE).next_to(calc, DOWN, buff=0.5)
        pic = ImageMobject(str(MEDIA / "image50.png")).scale_to_fit_width(6.2).move_to(RIGHT * 3.0 + DOWN * 1.6)
        self.begin(11)
        self.play(Write(calc), run_time=2)
        self.at(0.6)
        self.play(FadeIn(out), FadeIn(pic), run_time=1)
        self.end(gap=0.8)
        self.clear_except(head)
        rl = param_lines(lenet)
        self.reveal(12, [rl[0], rl[1], rl[2], rl[3]], fracs=[0.05, 0.3, 0.5, 0.8], run_time=0.7)
        self.line(13, FadeIn(rl[4]), run_time=1, gap=1)

        # comparison
        self.clear_except(head)
        cmp_head = section_title("What the parameter count depends on")
        hdr = [Tex(t, font_size=LABEL_SIZE, color=LABEL) for t in ("layer", "output", "weights", "with biases")]
        r1 = [Tex("AlexNet conv1", font_size=30, color=SOFT), MathTex(rf"{alex.W2} \times {alex.W2} \times {alex.K}", font_size=32, color=BLUE),
              MathTex(n(alex.weights), font_size=32), MathTex(n(alex.params), font_size=32, color=GREEN_C)]
        r2 = [Tex("LeNet-5 conv1", font_size=30, color=SOFT), MathTex(rf"{lenet.W2} \times {lenet.W2} \times {lenet.K}", font_size=32, color=BLUE),
              MathTex(n(lenet.weights), font_size=32), MathTex(n(lenet.params), font_size=32, color=GREEN_C)]
        table = VGroup(*hdr, *r1, *r2).arrange_in_grid(3, 4, buff=(0.9, 0.5)).move_to(UP * 0.5)
        dep = MathTex(r"\text{parameters} = ", "K", r"\,(", "F", r"^2", "D_1", r"+ 1)\qquad \text{no } W_1,\ \text{no } H_1", font_size=36).move_to(DOWN * 2.0)
        dep[1].set_color(GREEN_C); dep[3].set_color(YELLOW); dep[5].set_color(BLUE_B)
        self.begin(14)
        self.play(Transform(head, cmp_head), FadeIn(table), run_time=1.2)
        self.at(0.5)
        self.play(FadeIn(dep), run_time=1)
        self.end(gap=1.5)
        self.clear_all()
