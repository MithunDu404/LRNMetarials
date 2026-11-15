# p2_s09_flatten.py: the flatten layer and the classifier head. Coverage: C107-C113.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *

FIG = Path(__file__).resolve().parents[1] / "source" / "extracted_ML_Lec_12_CNN" / "media" / "image68.png"
FLAT = SECOND_TOOL


class P2S09Flatten(CnnScene):
    def construct(self):
        M = np.array([[1, 1, 0], [4, 2, 1], [0, 2, 1]])                     # slide 107
        v = M.flatten()                                                     # row-major
        assert v.tolist() == [1, 1, 0, 4, 2, 1, 0, 2, 1]
        L, N = v.size, 10
        assert (L, L * N, L * N + N, (L + 1) * N) == (9, 90, 100, 100)

        head = section_title("From feature maps to a classifier")

        def box(text, color=DIM):
            t = Tex(text, font_size=LABEL_SIZE, color=SOFT)
            return VGroup(Rectangle(width=max(t.width + 0.4, 1.7), height=1.0, stroke_color=color, stroke_width=3), t)
        bx = [box("conv layers"), box("pooling layers"), box("flatten", FLAT), box(r"dense layer"), box("softmax")]
        row = VGroup(*bx).arrange(RIGHT, buff=0.7).move_to(UP * 0.6)
        ar = [arrow_between(a, b, buff=0.08) for a, b in zip(bx, bx[1:])]
        vol = sheets(0.9, 4, [RESULT], border=RESULT, step=0.12, opacity=0.4).next_to(bx[1], DOWN, buff=0.6)
        vol_l = caption(vol, r"$W \times H \times C$")
        vec = blank_grid(6, 1, cell=0.28, fill=RESULT, opacity=0.5, border=RESULT).next_to(bx[3], DOWN, buff=0.5)
        vec_l = caption(vec, "a 1D vector")
        self.line(1, FadeIn(head), FadeIn(bx[0]), GrowArrow(ar[0]), FadeIn(bx[1]), FadeIn(vol), FadeIn(vol_l), run_time=1.5)
        self.line(2, FadeIn(bx[3]), GrowArrow(ar[3]), FadeIn(bx[4]), FadeIn(vec), FadeIn(vec_l), run_time=1.5)
        self.begin(3)
        self.play(FadeIn(bx[2]), GrowArrow(ar[1]), GrowArrow(ar[2]), run_time=1.2)
        self.at(0.3)
        self.play(Circumscribe(bx[2], color=FLAT), run_time=1)
        self.end()
        probs = Tex("class probabilities", font_size=LABEL_SIZE, color=LABEL).next_to(bx[4], DOWN, buff=0.4)
        self.begin(4)
        self.at(0.7)
        self.play(FadeIn(probs), run_time=0.8)
        self.end()
        cut = DashedLine(bx[2].get_top() + UP * 0.8, bx[2].get_bottom() + DOWN * 2.6, color=FLAT, stroke_width=3)
        left = Tex(r"spatial,\\translation-equivariant", font_size=LABEL_SIZE, color=SOFT).move_to(LEFT * 3.6 + DOWN * 2.5)
        right = Tex(r"global,\\position-sensitive", font_size=LABEL_SIZE, color=SOFT).move_to(RIGHT * 3.6 + DOWN * 2.5)
        self.begin(5)
        self.play(FadeOut(vol), FadeOut(vol_l), FadeOut(vec), FadeOut(vec_l), FadeOut(probs), Create(cut), run_time=1)
        self.at(0.25)
        self.play(FadeIn(left), run_time=0.8)
        self.at(0.6)
        self.play(FadeIn(right), run_time=0.8)
        self.end()
        order = Tex("order: row by row, channel by channel", font_size=LABEL_SIZE, color=LABEL).move_to(UP * 2.1)
        self.line(6, FadeIn(order), run_time=1)

        # slide 107 example
        self.clear_except(head)
        ex_head = section_title("Flatten, worked")
        fig = ImageMobject(str(FIG)).scale_to_fit_height(4.6).move_to(DOWN * 0.4)
        fig_l = Tex("lecture slide figure", font_size=LABEL_SIZE, color=LABEL).next_to(fig, DOWN, buff=0.15)
        self.line(7, Transform(head, ex_head), FadeIn(fig), FadeIn(fig_l), run_time=1.2)

        g = grid(M.tolist(), cell=0.8).move_to(LEFT * 3.4 + DOWN * 0.2)
        col = grid([[int(x)] for x in v], cell=0.55, border=FLAT).move_to(RIGHT * 2.2 + DOWN * 0.4)
        col_l = MathTex(rf"\in \mathbb{{R}}^{{{L}}}", font_size=36).next_to(col, RIGHT, buff=0.4)
        self.begin(8)
        self.play(FadeOut(fig), FadeOut(fig_l), FadeIn(g), run_time=0.8)
        for r in range(3):
            self.play(*[TransformFromCopy(g[r * 3 + c], col[r * 3 + c]) for c in range(3)], run_time=1.1)
        self.play(FadeIn(col_l), run_time=0.5)
        self.end(gap=1)

        self.clear_except(head)
        f1 = MathTex(r"L", "=", r"W \cdot H \cdot C", font_size=46).move_to(UP * 1.6)
        f1[0].set_color(FLAT)
        self.line(9, Write(f1), run_time=1.5)
        f2 = MathTex(r"\text{weights}", "=", r"(W \cdot H \cdot C)", r"\cdot N", font_size=40)
        f3 = MathTex(r"\text{with biases}", "=", r"(L + 1)", r"\cdot N", font_size=40)
        VGroup(f2, f3).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(UP * 0.0)
        self.begin(10)
        self.at(0.3)
        self.play(FadeIn(f2), run_time=0.8)
        self.at(0.7)
        self.play(FadeIn(f3), run_time=0.8)
        self.end()
        num = MathTex(rf"{L} \times {N} = {L * N}\ \text{{weights}}", r"\quad +\ ", rf"{N}\ \text{{biases}}", "=", str(L * N + N), r"\ \text{parameters}", font_size=40).move_to(DOWN * 2.0)
        num[4].set_color(GREEN_C)
        self.line(11, Write(num), run_time=2.5)

        self.clear_except(head)
        t_head = section_title("The trade-off at the flatten boundary")
        flow, boxes, arrows = flow_boxes(["large maps", "long vector", "many dense weights"], size=32, buff=0.9)
        flow.move_to(UP * 0.5)
        cure = Tex("pooling and global average pooling keep $W \\times H$ small", font_size=30, color=SOFT).move_to(DOWN * 1.8)
        self.begin(12)
        self.play(Transform(head, t_head), run_time=0.8)
        self.at(0.2)
        self.play(FadeIn(boxes[0]), run_time=0.6)
        self.at(0.35)
        self.play(GrowArrow(arrows[0]), FadeIn(boxes[1]), run_time=0.6)
        self.at(0.5)
        self.play(GrowArrow(arrows[1]), FadeIn(boxes[2]), run_time=0.6)
        self.at(0.72)
        self.play(FadeIn(cure), run_time=0.8)
        self.end(gap=1.5)
        self.clear_all()
