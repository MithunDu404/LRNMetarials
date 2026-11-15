# p1_s05_padding_math.py: valid vs same padding, P = (F-1)/2, odd F, four reasons. Coverage: C018-C029.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *

S_CELL = CELL_SMALL


class P1S05PaddingMath(CnnScene):
    def construct(self):
        W1, F = 5, 3
        valid = conv_out(W1, F, p=0)
        same_p = (F - 1) // 2
        same = conv_out(W1, F, p=same_p)
        assert (valid, same_p, same) == (3, 1, 5)
        assert W1 + 2 * same_p == 7 and 7 + 2 * 1 == 9            # 5x5 -> 7x7 padded; 7x7 -> 9x9 padded
        assert (5 - 1) // 2 == 2                                   # same padding for F = 5
        assert (4 - 1) / 2 == 1.5 and (4 - 1) == 1 + 2             # F = 4: 1.5 per side -> 1 left, 2 right

        head = section_title("Valid and same padding")
        LX, RX, GY = LEFT * 3.6, RIGHT * 3.6, UP * 0.1
        t_valid = Tex(r"valid: $P = 0$", font_size=BODY_SIZE, color=SOFT).move_to(LX + UP * 2.3)
        t_same = Tex("same: output size $=$ input size", font_size=BODY_SIZE, color=SOFT).move_to(RX + UP * 2.3)
        self.line(1, FadeIn(head), FadeIn(t_valid), FadeIn(t_same), run_time=1)

        # valid
        v_in = blank_grid(W1, W1, cell=S_CELL).move_to(LX + LEFT * 1.4 + GY)
        v_win = Square(F * S_CELL, stroke_color=TOOL, stroke_width=6).move_to(v_in[W1 + 1])
        v_out = blank_grid(valid, valid, cell=S_CELL, fill=RESULT, opacity=0.35, border=RESULT).move_to(LX + RIGHT * 1.9 + GY)
        v_arr = arrow_between(v_in, v_out)
        v_f = MathTex("W_2", "=", "W_1", "-", "F", "+ 1", font_size=34).move_to(LX + DOWN * 2.0)
        v_f[0].set_color(BLUE); v_f[2].set_color(BLUE_B); v_f[4].set_color(YELLOW)
        v_n = MathTex(f"{W1} - {F} + 2(0) + 1 =", str(valid), font_size=34).move_to(LX + DOWN * 2.7)
        v_n[1].set_color(BLUE)
        self.begin(2)
        self.play(FadeIn(v_in), Create(v_win), run_time=1)
        self.at(0.5)
        self.play(Write(v_f), run_time=1.2)
        self.end()
        self.begin(3)
        self.at(0.3)
        self.play(GrowArrow(v_arr), FadeIn(v_out), Write(v_n), run_time=1.5)
        self.end()

        # same
        s_in = blank_grid(W1, W1, cell=S_CELL).move_to(RX + LEFT * 1.5 + GY)
        ring = zero_ring(s_in, p=same_p, cell=S_CELL, size=16)
        s_win = Square(F * S_CELL, stroke_color=TOOL, stroke_width=6).move_to(s_in[0])
        s_out = blank_grid(same, same, cell=S_CELL, fill=RESULT, opacity=0.35, border=RESULT).move_to(RX + RIGHT * 2.1 + GY)
        s_arr = arrow_between(VGroup(s_in, ring), s_out, buff=0.15)
        s_sizes = MathTex(rf"{W1 + 2 * same_p} \times {W1 + 2 * same_p}", r"\ \rightarrow\ ", rf"{same} \times {same}", font_size=34).move_to(RX + DOWN * 2.0)
        s_sizes[2].set_color(BLUE)
        self.begin(4)
        self.play(FadeIn(s_in), run_time=0.8)
        self.at(0.25)
        self.play(LaggedStart(*[FadeIn(c) for c in ring], lag_ratio=0.03), run_time=1.5)
        self.at(0.7)
        self.play(Create(s_win), run_time=0.8)
        self.end()
        self.begin(5)
        self.at(0.45)
        self.play(GrowArrow(s_arr), FadeIn(s_out), FadeIn(s_sizes), run_time=1.5)
        self.end()

        # 7x7 -> 9x9 padded (slide 73)
        self.clear_except(head)
        g7 = blank_grid(7, 7, cell=S_CELL).move_to(LEFT * 2.2 + DOWN * 0.2)
        ring7 = zero_ring(g7, p=1, cell=S_CELL, size=16)
        t7 = MathTex(r"7 \times 7", r"\ \text{with}\ ", "P", r"= 1", r"\ \rightarrow\ ", r"9 \times 9", r"\ \text{padded}", font_size=40).move_to(RIGHT * 3.3 + DOWN * 0.2)
        t7[2].set_color(GREY_B)
        self.line(6, FadeIn(g7), LaggedStart(*[FadeIn(c) for c in ring7], lag_ratio=0.02), FadeIn(t7), run_time=2)

        # derivation
        self.clear_except(head)
        new_head = section_title("How much padding is enough?")

        def colour(m):
            for part in m:
                s = part.get_tex_string()
                if s in ("W_1",): part.set_color(BLUE_B)
                if s in ("W_2",): part.set_color(BLUE)
                if s == "F": part.set_color(YELLOW)
                if s in ("P", "2P"): part.set_color(GREY_B)
            return m
        d0 = colour(MathTex("W_2", "=", "W_1", "-", "F", "+", "2P", "+ 1", font_size=FORMULA_SIZE))
        d1 = colour(MathTex("W_1", "=", "W_1", "-", "F", "+", "2P", "+ 1", font_size=40))
        d2 = colour(MathTex("2P", "=", "F", "- 1", font_size=40))
        d3 = colour(MathTex("P", "=", r"\frac{F - 1}{2}", font_size=FORMULA_SIZE))
        d3[2][0].set_color(YELLOW)
        col = VGroup(d0, d1, d2, d3).arrange(DOWN, buff=0.5).move_to(LEFT * 3.5 + DOWN * 0.3)
        self.line(7, Transform(head, new_head), Write(d0), run_time=2)
        self.begin(8)
        self.play(FadeIn(d1, shift=UP * 0.2), run_time=1)
        self.at(0.35)
        self.play(FadeIn(d2, shift=UP * 0.2), run_time=1)
        self.at(0.65)
        self.play(Write(d3), run_time=1.2)
        self.play(Create(SurroundingRectangle(d3, color=LOOK_HERE, buff=0.18, stroke_width=4)), run_time=0.7)
        self.end(gap=1.2)

        c1 = MathTex(f"{W1} - {F} + 2({same_p}) + 1 =", str(same), font_size=38)
        c1[1].set_color(BLUE)
        c2 = MathTex(r"F = 5:\quad P = \frac{5 - 1}{2} =", str((5 - 1) // 2), font_size=38)
        c3 = MathTex(r"F \in \{1, 3, 5, 7, \dots\}", font_size=38)
        c4 = MathTex(r"F = 4:\quad P = 1.5\ \Rightarrow\ \text{left } 1,\ \text{right } 2", font_size=34, color=GREY_A)
        side = VGroup(c1, c2, c3, c4).arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.3)
        assert side.get_left()[0] > col.get_right()[0] + 1.0 and side.get_right()[0] < 6.6
        self.line(9, FadeIn(c1, shift=UP * 0.2), run_time=1)
        self.line(10, FadeIn(c2, shift=UP * 0.2), run_time=1)
        self.begin(11)
        self.at(0.25)
        self.play(FadeIn(c3, shift=UP * 0.2), run_time=1)
        self.at(0.5)
        self.play(FadeIn(c4, shift=UP * 0.2), run_time=1)
        self.end(gap=1)

        # four reasons, two on screen at a time
        self.clear_except(head)
        why = section_title("Why pad? Four reasons")
        r = [body(t) for t in ("1. Preserves width and height", "2. Keeps edge and corner features",
                               "3. Depth without shrinking", "4. Stable, consistent sizes")]
        VGroup(r[0], r[1]).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        VGroup(r[2], r[3]).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        self.line(12, Transform(head, why), run_time=1)
        self.line(13, FadeIn(r[0], shift=UP * 0.2), run_time=1)
        self.line(14, FadeIn(r[1], shift=UP * 0.2), run_time=1)
        self.play(FadeOut(r[0]), FadeOut(r[1]), run_time=0.6)
        self.line(15, FadeIn(r[2], shift=UP * 0.2), run_time=1)
        self.line(16, FadeIn(r[3], shift=UP * 0.2), run_time=1, gap=1.2)
        self.clear_all()
