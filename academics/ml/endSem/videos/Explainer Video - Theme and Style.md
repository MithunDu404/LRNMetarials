# Explainer Video: Theme and Style Guide

One look for every explainer video: CNN, ANN, backpropagation, sorting algorithms, statistics, any topic.
The style follows 3Blue1Brown's: a black screen, clean maths, simple shapes that move to explain an idea, a calm voice.
**No π characters, presenter, mascot, logo, or 3Blue1Brown intro or music.** Only visuals and voice.

> **For whoever builds a video (a person or an AI session):** read this whole file once, then the [Setup Guide](Explainer%20Video%20-%20Setup%20Guide.md).
> Sections 1–10 never change between videos. For each new topic, fill in a **Topic Sheet** (§11) before writing any scene. Worked examples for CNN and ANN are in §12.
> Colour values were read from Manim Community Edition 0.22.1's own colour file (`manim/utils/color/manim_colors.py`), checked 10 Nov 2026.

---

## 1. The four rules

1. **Accurate before pretty.** Every number, plot and result on screen is computed in code (numpy/scipy/sympy) and checked with an `assert`. Nothing is typed in by hand.
2. **One idea per screen.** Only what the narrator is talking about is on screen. Clear old objects before new ones come in.
3. **Show it, then name it.** The viewer sees the thing happen first, then gets its name or formula. Intuition first, jargon second.
4. **Voice first.** The narration is written and recorded before animating. Animations are timed to the real audio.

---

## 2. Canvas

| Setting | Value |
|---|---|
| Resolution | 1920 × 1080 (16:9) |
| Frame rate | 60 fps final (`-qh`); 30 fps acceptable (`-qh --fps 30`) |
| Background | `BLACK` `#000000` (Manim default) |
| Manim frame | 14.22 × 8 units, centre (0, 0) |
| Safe margin | everything stays 0.5 units in from every edge |

No gradients, glows, neon, drop shadows, textures, stock footage or emoji. Flat colours on black only.

---

## 3. Fixed base colours (same in every video)

Always use the Manim constant names in code, never raw hex.

| Role | Manim name | Hex | Used for |
|---|---|---|---|
| Background | `BLACK` | `#000000` | screen |
| Main ink | `WHITE` | `#FFFFFF` | titles, formulas, numbers, outlines |
| Soft text | `GREY_A` | `#DDDDDD` | sentences on screen |
| Labels | `GREY_B` | `#BBBBBB` | axis labels, captions under objects |
| Dimmed / inactive | `GREY_C` | `#888888` | things not being talked about right now |
| Grid and guide lines | `GREY_D` | `#444444` | cell borders, axis grid, faint guides |
| Empty / filler | `GREY_E` | `#222222` | empty cells, padding, background panels |

---

## 4. Role colours (the same meaning in every video)

Every video uses these **roles**. The Topic Sheet (§11) says which concept plays which role. One colour = one meaning, for the whole video.

| Role | Manim name | Hex | Meaning | CNN example | ANN example |
|---|---|---|---|---|---|
| **SUBJECT** | greys `BLACK`→`WHITE` | — | the data being studied; brightness = value | image pixels | input values, neuron activations |
| **TOOL** | `YELLOW` | `#F7D96F` | the thing acting on the data | kernel / filter | the neuron currently computing |
| **RESULT** | `BLUE` (`BLUE_C`) | `#58C4DD` | what comes out | feature map | output layer / prediction |
| **POSITIVE** | `BLUE` | `#58C4DD` | value or weight > 0 | positive kernel entries | positive weights |
| **NEGATIVE** | `RED` (`RED_C`) | `#FC6255` | value or weight < 0 | negative kernel entries | negative weights |
| **SECOND TOOL** | `TEAL_C` | `#5CD0B3` | a second, different operation | pooling window | activation function |
| **LEARNED** | `GREEN_C` | `#83C167` | numbers found by training | learned kernels | weights after training |
| **CHANGE / ERROR** | `ORANGE` | `#FF862F` | gradient, error, "how much to change" | — | loss, gradients in backprop |
| **LOOK HERE** | `YELLOW` box | `#F7D96F` | `SurroundingRectangle` / `Circumscribe` on the current item | current cell | current weight |

Rules:
- At most **5 role colours** in one video, plus the greys. Fewer is better.
- Bigger or smaller amounts use shades of the **same** colour (`BLUE_E` `#236B8E` weak … `BLUE_A` `#C7E9F1` strong), never a new colour.
- Blue/red for sign is a 3Blue1Brown convention. Keep it in every video with signed numbers.
- If TOOL (yellow) is used, use LOOK HERE sparingly so the two don't get mixed up.

**Extra colours** (only if the Topic Sheet needs more): `GOLD_C` `#F0AC5F`, `PURPLE_B` `#B189C6`, `MAROON_B` `#EC92AB`, `GREEN_B` `#A6CF8C`, `TEAL_B` `#76DDC0`, `BLUE_B` `#9CDCEB`.
**Three channels** (RGB, three classes, three groups): `RED_C`, `GREEN_C`, `BLUE_C` at fill opacity 0.35.

---

## 5. Symbol colours in formulas

- Each variable gets **one colour for the whole video**, listed in the Topic Sheet.
- Variables follow their role: a kernel size takes TOOL yellow, an output size RESULT blue, a weight blue/red by sign, a learning rate or gradient ORANGE.
- Plain constants and operators stay `WHITE`.
- In code: `MathTex(r"...", tex_to_color_map=SYMBOLS)`. It splits the formula at each listed symbol so only that symbol changes colour. Don't call `set_color_by_tex` on an unsplit formula, because it colours the whole formula.

---

## 6. Typography

3Blue1Brown's font is Computer Modern, the LaTeX font. Manim's `Tex` and `MathTex` give it automatically.

| Use | Object | Font size | Colour |
|---|---|---|---|
| Section title (top-left, small) | `Tex` | 40 | `WHITE` + thin `GREY_C` underline |
| Key sentence on screen | `Tex` | 36 | `GREY_A` |
| Main formula | `MathTex` | 48 | `WHITE` + symbol colours |
| Side formula / note | `MathTex` | 36 | same |
| Labels | `Tex` | 28 | `GREY_B` |
| Numbers in cells, on neurons | `MathTex` / `DecimalNumber` | 22–28 (fit with room to spare) | `WHITE` or role colour |
| Code (only if the topic needs it) | `Code` | 20–24 | Manim default |

- Words and maths always use `Tex`/`MathTex`. `Text()` (system fonts) is for code only.
- At most 2 lines of text on screen at once. Anything longer belongs in the narration.
- Numbers: at most 2 decimal places on screen. Use fractions (`\tfrac{1}{16}`) when the source does.
- For the exact 3Blue1Brown LaTeX preamble: `tex_template=TexTemplateLibrary.threeb1b`.

---

## 7. Shape library (reuse these)

| Building block | How to draw it | Typical topics |
|---|---|---|
| **Grid / matrix of cells** | `Square`s in a `VGroup`, `GREY_D` border, stroke 2, number centred; `arrange_in_grid(buff=0)` | images, convolution, matrices, DP tables |
| **Matrix with brackets** | `Matrix` / `DecimalMatrix` | linear algebra, weights |
| **Vector / array** | one row or column of cells | 1D convolution, arrays, sorting |
| **Neuron** | `Circle` radius 0.15–0.2, `WHITE` stroke, fill brightness = activation | ANN, CNN, backprop |
| **Connection / weight** | `Line`, stroke 1–3; colour by sign; opacity and width by size | ANN, attention |
| **Layer** | `VGroup` of neurons, `arrange(DOWN)`; use `⋮` for skipped ones | networks |
| **Graph of a function** | `Axes` + `plot`, axes `GREY_B`, curve in role colour | activation functions, loss curves, distributions |
| **Point moving on a curve** | `Dot` + `ValueTracker` + `always_redraw` | gradient descent, optimisation |
| **Number line** | `NumberLine` | probability, thresholds |
| **Arrow / flow** | `Arrow`, stroke 4, `GREY_B` (or role colour when it carries a result) | pipelines, data flow |
| **Box around a step** | `SurroundingRectangle`, `GREY_C`, square corners | grouping, "this block" |
| **3D volume** | `Prism` / `Cube` in `ThreeDScene`, fill opacity 0.25–0.35 | RGB images, tensors |

Stroke widths: default 4, grid lines 2, highlights 6. Square corners, no rounded "cards".
Sizes: grid cells 0.6 units (≤ 7×7), 0.45 (bigger). Neurons 0.15–0.2 radius, 0.4–0.5 apart.

---

## 8. Motion vocabulary

Use only these, so every video feels calm and the same.

| To… | Use | `run_time` |
|---|---|---|
| Draw a shape | `Create` | 1–1.5 s |
| Draw many shapes | `LaggedStart(*[Create(m) for m in group], lag_ratio=0.05)` | 1–2 s |
| Write text or formula | `Write` | 1–1.5 s |
| Bring in / remove | `FadeIn` / `FadeOut` (optional `shift=UP*0.3`) | 0.6–1 s |
| Change one thing into another | `Transform` / `ReplacementTransform` | 1 s |
| Rearrange an equation | `TransformMatchingTex` | 1.5 s |
| A value flows to a new place | `TransformFromCopy` | 0.6–1 s |
| Point at something | `Indicate`, `Circumscribe`, or `Create(SurroundingRectangle(...))` | 0.8 s |
| Move a tool one step | `.animate.move_to(...)` | 0.6 s first steps → 0.25 s later |
| A number changes smoothly | `ValueTracker` + `DecimalNumber` updater | 1–2 s |
| Dim what's not in focus | `.animate.set_opacity(0.25)` | 0.5 s |

- Rate function: default `smooth`. No bounces, spins, shakes, zoom-punches or flashy transitions.
- **Slow, then fast:** any repeated process (kernel sliding, forward pass, sorting swaps) shows the first 2–3 steps slowly with the full calculation. Then "and so on…", the readout hides, and the rest runs fast. Always show at least one complete calculation.
- **Camera:** still `Scene` by default. `MovingCameraScene` only to zoom into a detail and back. `ThreeDScene` only for real 3D objects, with one slow turn (≤ 30°).

---

## 9. Voice, script and pacing

**Pacing**
- A visual change lands **on the word** that names it.
- Hold 1.5–2 s, with nothing moving, after every key reveal (a finished result, the last term of a formula).
- About one visual change every 3–6 s. Calm is good; a still picture with the voice is fine.
- Each scene fades in its section title (top-left) and ends by fading everything out over 0.8 s.

**Script**
- Simple English, short sentences, spoken to one student ("you"). Assume they've never seen the topic.
- Each new term: plain idea first, then the name. "This small grid that slides over the image is called a *kernel*."
- Read numbers out the first time ("one times zero, plus two times one…"), then summarise.
- No filler ("as we can see", "basically", "so yeah").
- Subtitles aren't burned in. `self.add_subcaption(...)` writes an `.srt` next to the video.

**Shape of every video**
1. **Hook:** a question or puzzle the video answers (10–30 s).
2. **Intuition:** the idea with pictures, no symbols.
3. **Mechanism:** the step-by-step process, slow then fast.
4. **Formula:** built term by term, each term pointing at the picture it describes.
5. **Worked example:** real numbers, computed in code.
6. **Why it matters / where it's used.**
7. **Recap:** one screen, 3–5 points.

Long topics: one scene class per idea, 1–3 minutes each. Over ~25 min total, split into parts.

---

## 10. Accuracy rules

| Rule | Detail |
|---|---|
| Compute, don't type | Every number, plot and result comes from code in the scene file, with an `assert` against the source (slide, textbook, paper). |
| Source beats memory | Facts and formulas come from the given source (PPT, PDF, notes). Read image-only slides carefully; formulas and matrices are often pictures. |
| Fix source mistakes visibly | If the source is wrong, show the correct version and say so in one line. List each fix in the Topic Sheet. |
| Invented examples are labelled | If an example uses made-up numbers, it's still computed, and the screen says "example values". |
| Real images | Only images the user owns or public-domain/free-licence ones. Run the operation on them with code and show the true result. |
| Name the real thing | Use the field's actual term and mention common confusions once (e.g. CNN "convolution" is really cross-correlation, without flipping the kernel). |

---

## 11. Topic Sheet (fill this in for each new video)

Create `<video folder>/TOPIC_SHEET.md` from this template before writing scenes. The builder (person or AI) follows it together with this guide.

```markdown
# Topic Sheet: <topic>

Source: <path to PPT/PDF/notes, or "researched: <links>">
Audience: <e.g. B.Tech 3rd-year students, first time seeing the topic>
Target length: <minutes>, parts: <1 / 2 / 3>
Voice: Sarvam speaker <name>, language <en-IN / hi-IN>

## Role colours (max 5)
| Role | Concept in this topic |
|---|---|
| SUBJECT (greys) | |
| TOOL (YELLOW) | |
| RESULT (BLUE) | |
| POSITIVE / NEGATIVE (BLUE / RED) | |
| SECOND TOOL (TEAL_C) | |
| LEARNED (GREEN_C) | |
| CHANGE / ERROR (ORANGE) | |

## Symbol colours
| Symbol | Meaning | Colour |
|---|---|---|

## Scene plan
| # | Scene | Source pages/slides | Main visual | ~Length |
|---|---|---|---|---|

## Numbers to verify (each gets an assert)
- <example>: <expected result from the source>

## Source mistakes found
- <slide/page>: <what's wrong> → <what the video shows instead>
```

---

## 12. Worked examples of the Topic Sheet (short)

### CNN (source: `ML_Lec_12_CNN.pptx`, 108 slides)

| Role | Concept |
|---|---|
| SUBJECT | image pixels (grey by value), zero-padding cells `GREY_E` |
| TOOL | kernel / filter |
| RESULT | feature map |
| POSITIVE / NEGATIVE | kernel entries (Sobel, Laplacian have both) |
| SECOND TOOL | pooling window |
| LEARNED | kernels learned by backprop |

Symbols: `W_1, H_1, D_1` `BLUE_B` · `F` `YELLOW` · `P` `GREY_B` · `S` `PURPLE_B` · `K` `GREEN_C` · `W_2, H_2, D_2` `BLUE`.
Key formula: W₂ = ⌊(W₁ − F + 2P) / S⌋ + 1, same for H₂, and D₂ = K.

| # | Scene | Slides | ~Len |
|---|---|---|---|
| 1 | What is convolution | 1–3 | 1:30 |
| 2 | Sliding the kernel | 4–9, 29–37 | 2:30 |
| 3 | Padding | 9–12, 70–74 | 2:00 |
| 4 | Stride, many filters | 13–14, 75–78 | 1:30 |
| 5 | Edge kernels (Sobel, Canny) | 15–17 | 2:00 |
| 6 | Blur kernels (Gaussian, average) | 18–21 | 2:00 |
| 7 | Sharpen kernels (Laplacian, unsharp) | 22–26, 31 | 2:00 |
| 8 | Learned and dilated kernels | 27–28 | 1:00 |
| 9 | 1D convolution | 38–42 | 1:00 |
| 10 | 3D convolution on RGB | 43–52 | 2:30 |
| 11 | Output size formula + numerical examples | 53–69, 79–82 | 3:00 |
| 12 | From kernels to a CNN | 83–86 | 1:30 |
| 13 | Sparse connections, weight sharing | 87–92 | 2:30 |
| 14 | Pooling | 93–106 | 2:30 |
| 15 | Flatten and recap | 107 | 1:30 |

Numbers to verify: 4×4 map `[[1,4,2,1],[5,8,3,4],[7,6,4,5],[1,3,1,2]]` → 2×2 max-pool, stride 2 = `[[8,4],[7,5]]`; stride 1 = `[[8,8,4],[8,8,5],[7,6,5]]` (checked by hand).
Source mistakes: slide 21 is about the **average** kernel but labels its matrices "Gaussian Kernel".

### ANN (sketch)

| Role | Concept |
|---|---|
| SUBJECT | input values and neuron activations (fill brightness) |
| TOOL | the neuron currently computing its weighted sum |
| RESULT | output neurons / prediction |
| POSITIVE / NEGATIVE | weights |
| SECOND TOOL | activation function (its graph in `TEAL_C`) |
| CHANGE / ERROR | loss and gradients (if training is covered) |

Symbols: `w` blue/red by sign · `b` `GOLD_C` · `z` `WHITE` · `\sigma` `TEAL_C` · `a` `BLUE` · `\eta`, `\partial L` `ORANGE`.
Main visuals: layer of neurons → one neuron's weighted sum z = Σ wᵢaᵢ + b written out → `Axes` plot of the activation squashing z → full forward pass slow then fast → loss as an orange bar.

---

## 13. Don'ts

- No π creatures, presenter, face, hand, mascot or character of any kind.
- No 3Blue1Brown logo, intro, music or copied frames.
- No background music under explanations (soft music on the title card only, if at all).
- No more than ~3 groups of objects on screen at once.
- No text paragraphs on screen.
- No colour with two meanings in one video.
- No made-up numbers presented as real.

---

## 14. Shared `theme.py`

One copy lives in the projects root (`videos/theme.py`, see the Setup Guide). Every scene in every video imports it. Topic-specific colours go in the scene files, built from these roles.

```python
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
```
