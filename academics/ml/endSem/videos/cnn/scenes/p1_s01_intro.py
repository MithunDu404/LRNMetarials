# p1_s01_intro.py: title card and hook. Coverage: C001, C002.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
from scipy.signal import correlate2d
from common import *


class P1S01Intro(CnnScene):
    def construct(self):
        # Example values: a dark region on the left, a bright region on the right.
        image = np.array([[1, 1, 8, 9],
                          [0, 2, 9, 8],
                          [1, 1, 8, 9],
                          [0, 2, 9, 8]])
        kernel = np.array([[-1, 1],
                           [-1, 1]])                       # responds to a dark-to-bright step
        feature = correlate2d(image, kernel, mode="valid")
        assert feature.shape == (3, 3)
        assert feature.tolist() == [[2, 14, 0], [2, 14, 0], [2, 14, 0]]
        rows, cols = image.shape

        # l01: title card
        title = Tex("Convolutional Neural Networks", font_size=60, color=INK)
        part = Tex("Part 1: convolution and kernels", font_size=BODY_SIZE, color=SOFT)
        card = VGroup(title, part).arrange(DOWN, buff=0.5)
        self.line(1, Write(title), FadeIn(part, shift=UP * 0.3), run_time=2)
        self.play(FadeOut(card), run_time=0.8)

        # l02: a picture is a grid of numbers
        head = section_title("A picture is a grid of numbers")
        img = pixel_grid(image, vmax=9).move_to(UP * 0.9)
        note = Tex("example values", font_size=LABEL_SIZE, color=LABEL).to_corner(DR, buff=0.5)
        self.line(2, FadeIn(head), LaggedStart(*[FadeIn(c) for c in img], lag_ratio=0.05), FadeIn(note), run_time=2)

        # l03: flatten row after row; two vertical neighbours are marked first
        a, b = 0 * cols + 2, 1 * cols + 2                      # pixels (0,2) and (1,2)
        home = [c.get_center() for c in img]
        marks = VGroup(*[SurroundingRectangle(img[i], color=LOOK_HERE, buff=0, stroke_width=6) for i in (a, b)])
        self.begin(3)
        self.play(Create(marks), run_time=1)
        self.at(0.38)
        flat = [np.array([(i - (rows * cols - 1) / 2) * CELL, -2.0, 0]) for i in range(rows * cols)]
        for r in range(rows):
            moves = [img[r * cols + c].animate.move_to(flat[r * cols + c]) for c in range(cols)]
            moves += [marks[k].animate.move_to(flat[i]) for k, i in enumerate((a, b)) if i // cols == r]
            self.play(*moves, run_time=1.0)
        self.end()

        # l04: neighbours end up far apart
        gap_cells = b - a
        assert gap_cells == cols == 4
        arrow = DoubleArrow(flat[a] + UP * 0.55, flat[b] + UP * 0.55, buff=0, stroke_width=4, color=LABEL,
                            max_tip_length_to_length_ratio=0.12)
        apart = Tex(f"neighbours, now {gap_cells} cells apart", font_size=LABEL_SIZE, color=LABEL).next_to(arrow, UP, buff=0.2)
        self.line(4, GrowFromCenter(arrow), FadeIn(apart), run_time=1.2)

        # l05: convolution keeps the grid and slides a kernel over it
        new_head = section_title("Convolution keeps the grid")
        shift = LEFT * 0.6 + DOWN * 0.9
        ker = grid(kernel.tolist(), border=TOOL)
        for cell, v in zip(ker, kernel.flatten()):
            cell[1].set_color(POS if v > 0 else NEG)
        ker.move_to(LEFT * 4.6)
        ker_label = label_under(ker, "kernel")
        self.begin(5)
        self.play(FadeOut(arrow), FadeOut(apart), FadeOut(marks), Transform(head, new_head),
                  *[img[i].animate.move_to(home[i] + shift) for i in range(rows * cols)], run_time=1.8)
        img_label = label_under(img, "image")
        window = Square(2 * CELL, stroke_color=TOOL, stroke_width=6).move_to(
            VGroup(img[0], img[cols + 1]).get_center())
        self.play(FadeIn(ker), FadeIn(ker_label), FadeIn(img_label), run_time=1)
        self.at(0.55)
        self.play(TransformFromCopy(ker, window), run_time=1)
        for _ in range(2):
            self.play(window.animate.shift(RIGHT * CELL), run_time=0.7)
        self.end()

        # l06: one weighted sum at every stop
        out = grid(feature.tolist(), num_color=RESULT, border=RESULT).move_to(RIGHT * 4.2 + img.get_center()[1] * UP)
        out_label = label_under(out, "feature map")
        start = VGroup(img[0], img[cols + 1]).get_center()
        self.begin(6)
        self.play(window.animate.move_to(start), FadeIn(VGroup(*[c[0] for c in out])), FadeIn(out_label), run_time=1)
        for r in range(3):
            for c in range(3):
                self.play(window.animate.move_to(start + RIGHT * c * CELL + DOWN * r * CELL),
                          FadeIn(out[r * 3 + c][1]), run_time=0.55)
        self.end(gap=1.2)

        # l07: what Part 1 covers
        self.clear_all()
        items = VGroup(*[Tex(t, font_size=BODY_SIZE, color=SOFT) for t in
                         ("1. Convolution", "2. Padding", "3. Classic kernels", "4. Images with depth")])
        items.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        self.line(7, LaggedStart(*[FadeIn(i, shift=UP * 0.2) for i in items], lag_ratio=0.5), run_time=4)
        self.clear_all()
