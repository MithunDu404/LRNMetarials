# p2_s02_output_size.py: stride, the five-step derivation, the output size formula. Coverage: C066-C069.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import *

C_ = 0.7


def paint(m):
    """Colour formula parts by symbol (TOPIC_SHEET.md)."""
    table = {"W_1": BLUE_B, "H_1": BLUE_B, "D_1": BLUE_B, "W_2": BLUE, "H_2": BLUE, "D_2": BLUE,
             "F": YELLOW, "P": GREY_B, "2P": GREY_B, "S": PURPLE_B, "K": GREEN_C}
    for part in m:
        if part.get_tex_string().strip() in table:
            part.set_color(table[part.get_tex_string().strip()])
    return m


def size_formula(out="W_2", inp="W_1", size=FORMULA_SIZE):
    return paint(MathTex(out, "=", r"\left\lfloor \frac{", inp, "-", "F", "+", "2P", "}{", "S", r"} \right\rfloor", "+ 1", font_size=size))


class P2S02OutputSize(CnnScene):
    def construct(self):
        W1, P, F, S = 7, 1, 3, 2                                  # example values for the strip
        span = W1 + 2 * P
        travel = span - F
        jumps = travel // S
        W2 = jumps + 1
        assert (span, travel, jumps, W2) == (9, 6, 3, 4) and W2 == conv_out(W1, F, P, S)
        starts = [k * S for k in range(W2)]
        assert starts == [0, 2, 4, 6] and starts[-1] + F <= span

        head = section_title("Stride")
        strip = blank_grid(1, 9, cell=C_).move_to(UP * 0.3)
        win_at = lambda g, k: VGroup(g[k], g[k + F - 1]).get_center()
        win = Rectangle(width=F * C_, height=C_, stroke_color=TOOL, stroke_width=6).move_to(win_at(strip, 0))
        s_lab = MathTex("S", "= 1", font_size=44).next_to(strip, DOWN, buff=0.5)
        s_lab[0].set_color(PURPLE_B)
        self.line(1, FadeIn(head), FadeIn(strip), Create(win), run_time=1.2)
        self.begin(2)
        self.play(FadeIn(s_lab), run_time=0.6)
        for k in range(1, 5):
            self.play(win.animate.move_to(win_at(strip, k)), run_time=0.5)
        self.end()
        s2 = MathTex("S", "= 2", font_size=44).move_to(s_lab)
        s2[0].set_color(PURPLE_B)
        self.begin(3)
        self.play(win.animate.move_to(win_at(strip, 0)), Transform(s_lab, s2), run_time=0.8)
        for k in (2, 4, 6):
            self.play(win.animate.move_to(win_at(strip, k)), run_time=0.6)
        self.end()

        # derivation on a strip of W1 = 7 cells
        self.clear_except(head)
        d_head = section_title("Deriving the output width")
        core = blank_grid(1, W1, cell=C_).move_to(UP * 1.0)
        note = Tex("example values", font_size=LABEL_SIZE, color=LABEL).to_corner(DR, buff=0.5)
        self.line(4, Transform(head, d_head), FadeIn(core), FadeIn(note), run_time=1)

        ring = zero_ring(core, p=P, cell=C_, size=22)
        ring = VGroup(*[c for c in ring if abs(c.get_center()[1] - core.get_center()[1]) < 0.01])   # left and right only
        assert len(ring) == 2 * P
        full = VGroup(ring[0], *core, ring[1])
        b_span = Brace(full, DOWN, buff=0.15, color=LABEL)
        t_span = paint(MathTex("W_1", "+", "2P", font_size=36)).next_to(b_span, DOWN, buff=0.15)
        self.begin(5)
        self.at(0.25)
        self.play(FadeIn(ring), run_time=0.8)
        self.at(0.65)
        self.play(GrowFromCenter(b_span), FadeIn(t_span), run_time=0.8)
        self.end()

        w = Rectangle(width=F * C_, height=C_, stroke_color=TOOL, stroke_width=6).move_to(win_at(full, 0))
        b_f = Brace(w, UP, buff=0.12, color=TOOL)
        t_f = MathTex("F", font_size=36, color=YELLOW).next_to(b_f, UP, buff=0.12)
        self.line(6, Create(w), GrowFromCenter(b_f), FadeIn(t_f), run_time=1.2)

        rest = VGroup(*full[F:])
        b_rest = Brace(rest, UP, buff=0.12, color=LABEL)
        t_rest = paint(MathTex("W_1", "+", "2P", "-", "F", font_size=36)).next_to(b_rest, UP, buff=0.12)
        self.line(7, GrowFromCenter(b_rest), FadeIn(t_rest), run_time=1.2)

        arcs = VGroup(*[CurvedArrow(full[F - 1 + k * S].get_corner(DR) + DOWN * 0.02, full[F - 1 + (k + 1) * S].get_corner(DR) + DOWN * 0.02,
                                    angle=1.2, stroke_width=3, color=PURPLE_B, tip_length=0.15) for k in range(jumps)])
        t_j = paint(MathTex(r"\left\lfloor \frac{", "W_1", "-", "F", "+", "2P", "}{", "S", r"} \right\rfloor", r"\ \text{jumps}", font_size=34))
        t_j.move_to(DOWN * 2.2 + LEFT * 2.6)
        self.begin(8)
        self.play(FadeOut(b_span), FadeOut(t_span), run_time=0.5)
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.5), run_time=1.5)
        self.at(0.5)
        self.play(FadeIn(t_j), run_time=0.8)
        self.end()
        plus = MathTex("+\\ 1", r"\ \text{(the starting position)}", font_size=34).next_to(t_j, RIGHT, buff=0.4)
        self.line(9, FadeIn(plus), Indicate(w, color=TOOL, scale_factor=1.08), run_time=1)

        main = size_formula().move_to(DOWN * 2.2)
        self.line(10, FadeOut(t_j), FadeOut(plus), Write(main), run_time=2, gap=1)

        nums = MathTex(rf"\left\lfloor \frac{{{W1} - {F} + 2 \cdot {P}}}{{{S}}} \right\rfloor + 1 = {travel // S} + 1 =", str(W2), font_size=40)
        nums[1].set_color(BLUE)
        nums.move_to(DOWN * 2.2)
        self.begin(11)
        self.play(main.animate.scale(0.75).move_to(DOWN * 0.9), FadeOut(b_f), FadeOut(t_f), FadeOut(b_rest), FadeOut(t_rest), FadeOut(arcs), run_time=1)
        self.at(0.3)
        self.play(Write(nums), run_time=2.5)
        self.at(0.78)
        for st in starts:
            self.play(w.animate.move_to(win_at(full, st)), run_time=0.35)
        self.end()

        # full set of formulas
        self.clear_except(head)
        f_head = section_title("The output size formula")
        fw, fh = size_formula("W_2", "W_1", 44), size_formula("H_2", "H_1", 44)
        fd = paint(MathTex("D_2", "=", "K", font_size=44))
        trio = VGroup(fw, fh, fd).arrange(DOWN, buff=0.45).move_to(UP * 0.4)
        self.begin(12)
        self.play(Transform(head, f_head), FadeIn(fw), run_time=1)
        self.play(FadeIn(fh), run_time=0.8)
        self.at(0.55)
        self.play(FadeIn(fd), run_time=0.8)
        self.end()
        flow, boxes, arrows = flow_boxes([r"input $W_1 \times H_1 \times D_1$", r"conv layer $(F,\ P,\ S,\ K)$", r"output $W_2 \times H_2 \times D_2$"], size=30)
        flow.move_to(DOWN * 2.6)
        self.line(13, FadeIn(flow), run_time=1.2)

        self.clear_except(head)
        g_head = section_title("How the formula grew")
        v1 = paint(MathTex("W_2", "=", "W_1", "-", "F", "+ 1", font_size=42))
        v2 = paint(MathTex("W_2", "=", "W_1", "-", "F", "+", "2P", "+ 1", font_size=42))
        v3 = size_formula(size=42)
        labs = [Tex(t, font_size=LABEL_SIZE, color=LABEL) for t in ("no padding, stride 1", "with padding", "with padding and stride")]
        rows = VGroup(*[VGroup(l, v).arrange(RIGHT, buff=0.8) for l, v in zip(labs, (v1, v2, v3))]).arrange(DOWN, buff=0.7, aligned_edge=RIGHT)
        self.begin(14)
        self.play(Transform(head, g_head), run_time=0.8)
        for k, fr in enumerate((0.18, 0.45, 0.72)):
            self.at(fr)
            self.play(FadeIn(rows[k], shift=UP * 0.2), run_time=0.8)
        self.end(gap=1.5)
        self.clear_all()
