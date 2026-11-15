# theme.py: shared look for all explainer videos (Manim Community Edition 0.22.1)
from manim import *

config.background_color = BLACK

# Base colours
INK, SOFT, LABEL, DIM, GUIDE, EMPTY = WHITE, GREY_A, GREY_B, GREY_C, GREY_D, GREY_E

# Role colours (see the style guide, section 4)
TOOL        = YELLOW
RESULT      = BLUE
POS, NEG    = BLUE, RED
SECOND_TOOL = TEAL_C
LEARNED     = GREEN_C
CHANGE      = ORANGE
LOOK_HERE   = YELLOW

# Sizes
CELL, CELL_SMALL = 0.6, 0.45
NEURON_R = 0.18
TITLE_SIZE, BODY_SIZE, FORMULA_SIZE, LABEL_SIZE, CELL_NUM_SIZE = 40, 36, 48, 28, 26


def section_title(text):
    """Small title in the top-left corner with a thin underline."""
    t = Tex(text, font_size=TITLE_SIZE, color=INK).to_corner(UL, buff=0.5)
    line = Line(t.get_corner(DL), t.get_corner(DR), stroke_width=1.5, color=DIM).shift(DOWN * 0.12)
    return VGroup(t, line)


def grid(values, cell=CELL, border=GUIDE, num_color=INK, shade=False, show_numbers=True):
    """Grid of squares, one per value. shade=True fills each cell by value (0 = black, 1 = white)."""
    rows, cols = len(values), len(values[0])
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            v = values[r][c]
            sq = Square(cell, stroke_color=border, stroke_width=2)
            if shade:
                sq.set_fill(interpolate_color(BLACK, WHITE, min(max(float(v), 0.0), 1.0)), opacity=1)
            cell_group = VGroup(sq)
            if show_numbers:
                cell_group.add(MathTex(f"{v:g}", font_size=CELL_NUM_SIZE, color=num_color).move_to(sq))
            cells.add(cell_group)
    cells.arrange_in_grid(rows, cols, buff=0)
    return cells


def neuron(activation=0.0, radius=NEURON_R):
    """A neuron: white outline, fill brightness = activation (0..1)."""
    return Circle(radius, stroke_color=INK, stroke_width=2).set_fill(
        interpolate_color(BLACK, WHITE, min(max(float(activation), 0.0), 1.0)), opacity=1)


def layer(activations, gap=0.45):
    """A vertical column of neurons."""
    return VGroup(*[neuron(a) for a in activations]).arrange(DOWN, buff=gap - 2 * NEURON_R)


def connect(left, right, weights=None, max_width=3):
    """Lines between two layers. weights[i][j] (right i, left j) sets colour by sign and width/opacity by size."""
    lines = VGroup()
    for i, r in enumerate(right):
        for j, l in enumerate(left):
            w = 1.0 if weights is None else float(weights[i][j])
            line = Line(l.get_right(), r.get_left(), stroke_color=POS if w >= 0 else NEG,
                        stroke_width=max(0.5, min(abs(w), 1) * max_width),
                        stroke_opacity=0.25 + 0.75 * min(abs(w), 1))
            lines.add(line)
    return lines
