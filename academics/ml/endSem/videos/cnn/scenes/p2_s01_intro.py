# p2_s01_intro.py: title card and hook for Part 2. Coverage: C065.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *


class P2S01Intro(CnnScene):
    def construct(self):
        title = Tex("Convolutional Neural Networks", font_size=60, color=INK)
        part = Tex("Part 2: sizes, networks, pooling, flatten", font_size=BODY_SIZE, color=SOFT)
        card = VGroup(title, part).arrange(DOWN, buff=0.5)

        vol_in = sheets(1.6, 3, [RED_C, GREEN_C, BLUE_C])
        conv = VGroup(Rectangle(width=2.0, height=1.1, stroke_color=TOOL, stroke_width=4), Tex("conv layer", font_size=LABEL_SIZE, color=SOFT))
        vol_out = sheets(1.2, 5, [RESULT], border=RESULT, step=0.14)
        chain = VGroup(vol_in, conv, vol_out).arrange(RIGHT, buff=1.3).move_to(UP * 0.6 + LEFT * 1.6)
        a1, a2 = arrow_between(vol_in, conv), arrow_between(conv, vol_out)
        q = MathTex(r"?\times ?\times ?", font_size=40, color=RESULT).next_to(vol_out, DOWN, buff=0.35)
        head = section_title("What size comes out?")

        self.begin(1)
        self.play(Write(title), FadeIn(part, shift=UP * 0.3), run_time=1.5)
        self.at(0.4)
        self.play(FadeOut(card), run_time=0.6)
        self.play(FadeIn(head), FadeIn(vol_in), GrowArrow(a1), FadeIn(conv), GrowArrow(a2), FadeIn(vol_out), run_time=1.2)
        self.at(0.8)
        self.play(FadeIn(q), run_time=0.6)
        self.end()

        nxt = VGroup(Rectangle(width=2.0, height=1.1, stroke_color=DIM, stroke_width=3), Tex("next layer", font_size=LABEL_SIZE, color=DIM))
        nxt.next_to(vol_out, RIGHT, buff=1.3)
        a3 = arrow_between(vol_out, nxt).set_color(DIM)
        self.begin(2)
        self.at(0.45)
        self.play(GrowArrow(a3), FadeIn(nxt), run_time=1)
        self.end()

        strip = blank_grid(1, 11, cell=0.6).move_to(DOWN * 2.3)
        win = Rectangle(width=1.8, height=0.6, stroke_color=TOOL, stroke_width=6).move_to(strip[1])
        step = MathTex(r"\text{step } 1", font_size=32).next_to(strip, UP, buff=0.25)
        step2 = MathTex(r"\text{step } 2", font_size=32).move_to(step)
        self.begin(3)
        self.play(FadeIn(strip), Create(win), FadeIn(step), run_time=1)
        self.at(0.22)
        for k in range(2, 6):
            self.play(win.animate.move_to(strip[k]), run_time=0.45)
        self.at(0.62)
        self.play(win.animate.move_to(strip[1]), Transform(step, step2), run_time=0.7)
        for k in (3, 5, 7, 9):
            self.play(win.animate.move_to(strip[k]), run_time=0.45)
        self.end()

        self.clear_all()
        items = VGroup(*[Tex(t, font_size=BODY_SIZE, color=SOFT) for t in
                         ("1. Stride and the output size formula", "2. AlexNet and LeNet-5", "3. Why not a dense network?",
                          "4. Pooling", "5. Flatten")]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        self.reveal(4, list(items), fracs=[0.08, 0.38, 0.52, 0.78, 0.88], run_time=0.6, gap=1)
        self.clear_all()
