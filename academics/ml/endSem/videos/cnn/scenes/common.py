# common.py: shared pieces for the CNN video's scenes (topic colours, narration timing, pixel grids).
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]          # videos/
sys.path.insert(0, str(ROOT))

from theme import *                                  # noqa: E402,F401,F403
from voiced import VoicedScene                       # noqa: E402

# Symbol colours from TOPIC_SHEET.md
SYMBOLS = {"W_1": BLUE_B, "H_1": BLUE_B, "D_1": BLUE_B, "F": YELLOW, "P": GREY_B, "S": PURPLE_B,
           "K": GREEN_C, "W_2": BLUE, "H_2": BLUE, "D_2": BLUE}


class CnnScene(VoicedScene):
    """VoicedScene plus begin()/end(), for lines that need several animations in a row."""
    video_dir = Path(__file__).resolve().parents[1]  # videos/cnn/

    def key(self, n):
        return f"{Path(sys.modules[type(self).__module__].__file__).stem}/l{n:02d}"

    def begin(self, n):
        """Start narration line n. Play any animations, then call end()."""
        line = self.voice[self.key(n)]
        self.add_sound(str(self.video_dir / "audio" / f"{self.key(n)}.wav"))
        self.add_subcaption(line["text"], duration=line["seconds"])
        self._line_start = self.renderer.time
        self._line_end = self._line_start + line["seconds"]

    def at(self, frac):
        """Hold until this fraction (0..1) of the current line has been spoken."""
        target = self._line_start + frac * (self._line_end - self._line_start)
        if target - self.renderer.time > 0.03:
            self.wait(target - self.renderer.time)

    def left(self):
        """Seconds of the current line still to be spoken."""
        return self._line_end - self.renderer.time

    def end(self, gap=0.35):
        """Hold until the current line has finished, plus a short breath."""
        left = self._line_end - self.renderer.time
        assert left > -0.15, f"animations ran {-left:.2f} s past the narration"
        self.wait(max(left, 0) + gap)

    def line(self, n, *animations, run_time=1.5, gap=0.35):
        """One line with at most one group of animations."""
        self.begin(n)
        if animations:
            self.play(*animations, run_time=run_time)
        self.end(gap)

    def reveal(self, n, items, fracs=None, run_time=0.8, gap=0.35, anim=FadeIn):
        """Line n, with items appearing one by one at the given fractions of the line."""
        self.begin(n)
        fracs = fracs or [0.85 * i / len(items) for i in range(len(items))]
        for m, f in zip(items, fracs):
            self.at(f)
            self.play(anim(m), run_time=min(run_time, max(self.left() - 0.1, 0.3)))
        self.end(gap)

    def clear_except(self, *keep, run_time=0.8):
        gone = [m for m in self.mobjects if m not in keep]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)

    def recap(self, title, points, size=32):
        """Recap scene: line 1 = title, lines 2..n+1 = one point each, last line = closing words."""
        head = section_title(title)
        items = VGroup(*[Tex(p, font_size=size, color=SOFT) for p in points]).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        if items.width > 12.6:
            items.scale_to_fit_width(12.6)
        items.move_to(DOWN * 0.3)
        self.line(1, FadeIn(head), run_time=0.8)
        for k, item in enumerate(items):
            self.line(k + 2, FadeIn(item, shift=UP * 0.2), run_time=0.9)
        self.line(len(points) + 2, gap=1.0)
        self.clear_all()

    def clear_all(self):
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


def pixel_grid(values, vmax, cell=CELL):
    """Image grid: each cell is filled grey by value/vmax and shows its number in a readable colour."""
    rows, cols = len(values), len(values[0])
    cells = VGroup()
    for r in range(rows):
        for c in range(cols):
            level = float(values[r][c]) / vmax
            sq = Square(cell, stroke_color=GUIDE, stroke_width=2).set_fill(
                interpolate_color(BLACK, WHITE, level), opacity=1)
            num = MathTex(f"{values[r][c]:g}", font_size=CELL_NUM_SIZE,
                          color=BLACK if level > 0.55 else WHITE).move_to(sq)
            cells.add(VGroup(sq, num))
    cells.arrange_in_grid(rows, cols, buff=0)
    return cells


def label_under(mob, text, buff=0.25):
    return Tex(text, font_size=LABEL_SIZE, color=LABEL).next_to(mob, DOWN, buff=buff)


def tex_grid(labels, border=GUIDE, color=INK, cell=0.9, size=30):
    """Grid of cells holding MathTex strings (labels is a 2D list)."""
    cells = VGroup()
    for row in labels:
        for s in row:
            sq = Square(cell, stroke_color=border, stroke_width=2)
            cells.add(VGroup(sq, MathTex(str(s), font_size=size, color=color).move_to(sq)))
    cells.arrange_in_grid(len(labels), len(labels[0]), buff=0)
    return cells


def kernel_grid(values, cell=CELL, size=CELL_NUM_SIZE, fmt="{:g}"):
    """Kernel: yellow border, entries blue if positive, red if negative, white if zero."""
    g = tex_grid([[fmt.format(v) for v in row] for row in values], border=TOOL, cell=cell, size=size)
    flat = [v for row in values for v in row]
    for c, v in zip(g, flat):
        c[1].set_color(POS if v > 0 else NEG if v < 0 else INK)
    return g


def window_at(g, cols, r, c, f=2, color=TOOL):
    """A square outline covering the f x f block of grid g whose top-left cell is (r, c)."""
    block = VGroup(g[r * cols + c], g[(r + f - 1) * cols + c + f - 1])
    side = g[0][0].width * f
    return Square(side, stroke_color=color, stroke_width=6).move_to(block.get_center())


def body(text, size=BODY_SIZE, color=SOFT):
    return Tex(text, font_size=size, color=color)


def bullet_lines(texts, size=BODY_SIZE):
    """Short lines, left-aligned, centred on screen."""
    return VGroup(*[body(t, size) for t in texts]).arrange(DOWN, buff=0.5, aligned_edge=LEFT)


def flow_boxes(texts, size=LABEL_SIZE, buff=0.7, color=DIM):
    """A row of boxed steps joined by arrows. Returns (group, boxes, arrows)."""
    boxes = VGroup()
    for t in texts:
        label = Tex(t, font_size=size, color=SOFT)
        boxes.add(VGroup(SurroundingRectangle(label, color=color, buff=0.2, stroke_width=2), label))
    boxes.arrange(RIGHT, buff=buff)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, stroke_width=4, color=LABEL,
                            max_tip_length_to_length_ratio=0.25) for a, b in zip(boxes, boxes[1:])])
    return VGroup(boxes, arrows), boxes, arrows


def conv_out(w, f, p=0, s=1):
    """Output size of a convolution or pooling along one axis."""
    return (w - f + 2 * p) // s + 1


def blank_grid(rows, cols, cell=CELL, fill=GREY_D, opacity=0.55, border=GUIDE):
    """Grid of plain cells (no numbers)."""
    g = VGroup(*[Square(cell, stroke_color=border, stroke_width=2).set_fill(fill, opacity=opacity)
                 for _ in range(rows * cols)])
    g.arrange_in_grid(rows, cols, buff=0)
    return g


def zero_ring(inner, p=1, cell=CELL, size=20):
    """p rings of dark zero-padding cells around the grid `inner` (which must be laid out with buff 0)."""
    left, top = inner.get_left()[0], inner.get_top()[1]
    cols, rows = round(inner.width / cell), round(inner.height / cell)
    ring = VGroup()
    for r in range(-p, rows + p):
        for c in range(-p, cols + p):
            if 0 <= r < rows and 0 <= c < cols:
                continue
            sq = Square(cell, stroke_color=GUIDE, stroke_width=2).set_fill(EMPTY, opacity=1)
            sq.move_to([left + (c + 0.5) * cell, top - (r + 0.5) * cell, 0])
            ring.add(VGroup(sq, MathTex("0", font_size=size, color=LABEL).move_to(sq)))
    return ring


def arrow_between(a, b, buff=0.25):
    return Arrow(a.get_right(), b.get_left(), buff=buff, stroke_width=4, color=LABEL, max_tip_length_to_length_ratio=0.2)


def gray_map(arr, cell=0.4, vmax=None):
    """Image as grey cells (no numbers): 0 = black, vmax = white."""
    vmax = float(vmax if vmax is not None else max(abs(float(v)) for row in arr for v in row) or 1)
    g = VGroup(*[Square(cell, stroke_color=GUIDE, stroke_width=1).set_fill(
        interpolate_color(BLACK, WHITE, min(max(float(v) / vmax, 0), 1)), opacity=1) for row in arr for v in row])
    g.arrange_in_grid(len(arr), len(arr[0]), buff=0)
    return g


def signed_map(arr, cell=0.4):
    """Filter response as cells: blue = positive, red = negative, strength = opacity."""
    vmax = max(abs(float(v)) for row in arr for v in row) or 1
    g = VGroup(*[Square(cell, stroke_color=GUIDE, stroke_width=1).set_fill(
        POS if v >= 0 else NEG, opacity=abs(float(v)) / vmax) for row in arr for v in row])
    g.arrange_in_grid(len(arr), len(arr[0]), buff=0)
    return g


def frac_kernel(num_tex, values, cell=0.6, size=CELL_NUM_SIZE):
    """A kernel with a scalar factor in front, e.g. 1/16 [ ... ]. Returns VGroup(factor, kernel)."""
    k = kernel_grid(values, cell=cell, size=size)
    f = MathTex(num_tex, font_size=38)
    return VGroup(f, k).arrange(RIGHT, buff=0.2)


def caption(mob, text, direction=DOWN, buff=0.25, size=LABEL_SIZE, color=LABEL):
    return Tex(text, font_size=size, color=color).next_to(mob, direction, buff=buff)


def sheets(side, depth, colors, border=GUIDE, step=0.18, opacity=0.35, width=2):
    """A volume drawn as `depth` stacked square sheets; sheet 0 is the front one. colors cycles."""
    s = VGroup()
    for i in reversed(range(depth)):
        s.add(Square(side, stroke_color=border, stroke_width=width).set_fill(colors[i % len(colors)], opacity=opacity)
              .shift((RIGHT + UP) * step * i))
    return s            # s[-1] is the front sheet
