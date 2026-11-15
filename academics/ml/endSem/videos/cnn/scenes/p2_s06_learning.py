# p2_s06_learning.py: learned kernels, initialisation, hierarchy, six advantages. Coverage: C083-C090.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from common import *


class P2S06Learning(CnnScene):
    def construct(self):
        rng = np.random.default_rng(7)
        init = [np.round(rng.normal(0, 0.1, (3, 3)), 2) + 0.0 for _ in range(3)]         # example values, small and zero-centred
        assert all(abs(k).max() < 0.5 for k in init)
        assert not (init[0] == init[1]).all()                                         # symmetry is broken
        trained = np.round(rng.normal(0, 0.6, (3, 3)), 1) + 0.0

        def lk(vals, fmt="{:.2f}", cell=0.8, size=22):
            return tex_grid([[fmt.format(v) for v in row] for row in vals], border=LEARNED, color=LEARNED, cell=cell, size=size)

        head = section_title("Where do the kernels come from?")
        sobel = kernel_grid([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], cell=0.8, size=26).move_to(LEFT * 3.2)
        s_l = caption(sobel, "hand-made (Sobel)")
        learned = lk(trained, "{:.1f}", size=24).move_to(RIGHT * 3.2)
        l_l = caption(learned, "learned by backpropagation")
        arr = arrow_between(sobel, learned, buff=0.6)
        e2e = Tex("end-to-end representation learning", font_size=30, color=SOFT).move_to(DOWN * 2.7)
        self.begin(1)
        self.play(FadeIn(head), FadeIn(sobel), FadeIn(s_l), run_time=1)
        self.at(0.3)
        self.play(GrowArrow(arr), FadeIn(learned), FadeIn(l_l), *[c[0].animate.set_stroke(opacity=0.3) for c in sobel], *[c[1].animate.set_opacity(0.3) for c in sobel], run_time=1.2)
        self.at(0.78)
        self.play(FadeIn(e2e), run_time=0.8)
        self.end()

        self.clear_except(head)
        init_head = section_title("Random initialisation")
        ks = VGroup(*[lk(k) for k in init]).arrange(RIGHT, buff=0.9).move_to(UP * 0.3)
        k_l = caption(ks, "small random weights centred on zero (example values)")
        names = Tex("Xavier (Glorot) \\quad or \\quad He (Kaiming)", font_size=BODY_SIZE, color=SOFT).move_to(DOWN * 2.6)
        self.begin(2)
        self.play(Transform(head, init_head), FadeIn(ks[1]), FadeIn(k_l), run_time=1)
        self.at(0.5)
        self.play(FadeIn(names), run_time=0.8)
        self.end()
        self.begin(3)
        self.at(0.5)
        self.play(FadeIn(ks[0]), FadeIn(ks[2]), run_time=1)
        self.end()

        self.clear_except(head)
        h_head = section_title("A hierarchy of features")
        flow, boxes, arrows = flow_boxes([r"early layers:\\edges, colour blobs", r"middle layers:\\textures", r"deep layers:\\faces, wheels, text"], size=30, buff=0.9)
        self.begin(4)
        self.play(Transform(head, h_head), run_time=0.8)
        for k, fr in enumerate((0.15, 0.55, 0.7)):
            self.at(fr)
            self.play(FadeIn(boxes[k]), *([GrowArrow(arrows[k - 1])] if k else []), run_time=0.8)
        self.end(gap=1)

        self.clear_except(head)
        adv = section_title("Six advantages of CNNs")
        pts = [body(t) for t in ("1. Far fewer parameters", "2. Efficient in computation and memory",
                                 "3. Translation invariance and equivariance", "4. Hierarchical features",
                                 "5. Better generalisation", "6. Robust to noise and small changes")]
        for a, b in ((0, 1), (2, 3), (4, 5)):
            VGroup(pts[a], pts[b]).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        self.line(5, Transform(head, adv), run_time=0.8)
        for k in range(6):
            self.line(6 + k, FadeIn(pts[k], shift=UP * 0.2), run_time=0.9, gap=1.2 if k == 5 else 0.35)
            if k in (1, 3):
                self.play(FadeOut(pts[k - 1]), FadeOut(pts[k]), run_time=0.5)
        self.clear_all()
