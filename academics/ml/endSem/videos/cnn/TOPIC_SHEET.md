# Topic Sheet: Convolutional Neural Networks (ML Lec 12)

Source: `cnn/source/ML_Lec_12_CNN_Learning_Guide.md` (9 sections, 113 coverage items in `COVERAGE.md`)
Audience: B.Tech students revising for the end-sem; they know ANNs, not CNNs
Target length: about 35 minutes, parts: 2 (Part 1 about 18 min, Part 2 about 17 min)
Voice: Sarvam speaker `shubh`, language `en-IN`, calm teacher
Render: `uv run python render.py ...` (not `uv run manim`), `Tex`/`MathTex` only (see `DECISIONS.md`, k)

## Role colours (5)

| Role | Concept in this topic |
|---|---|
| SUBJECT (greys) | image pixels and input volumes (grey by value); zero-padding cells `GREY_E` |
| TOOL (YELLOW) | kernel / filter and its sliding window |
| RESULT (BLUE) | feature map, output volume |
| POSITIVE / NEGATIVE (BLUE / RED) | signed kernel entries (Sobel, Laplacian, unsharp mask) |
| SECOND TOOL (TEAL_C) | pooling window, and the flatten step |
| LEARNED (GREEN_C) | kernels learned by backpropagation; the number of filters K |
| CHANGE / ERROR (ORANGE) | not used |

RGB channels, when shown: `RED_C`, `GREEN_C`, `BLUE_C` at fill opacity 0.35 (style guide §4). Source corrections appear as a `GREY_A` one-line note with the corrected item boxed in yellow.

## Symbol colours

| Symbol | Meaning | Colour |
|---|---|---|
| `W_1`, `H_1`, `D_1` | input width, height, depth | `BLUE_B` |
| `F`, `F_p` | filter size, pooling window size | `YELLOW` (`F_p` in `TEAL_C`) |
| `P` | padding | `GREY_B` |
| `S`, `S_p` | stride | `PURPLE_B` |
| `K` | number of filters | `GREEN_C` |
| `W_2`, `H_2`, `D_2` | output width, height, depth | `BLUE` |
| `r` | dilation rate | `GOLD_C` |
| `b` | bias | `WHITE` |

## Scene plan

Scene files are `cnn/scenes/<name>.py`, class name in CamelCase (`p1_s02_sliding.py` → `P1S02Sliding`). Stage = place in the video shape (style guide §9).

### Part 1: convolution and kernels (guide sections 1–4)

| # | Scene | Guide | Coverage IDs | Stage | Main visual | ~Length |
|---|---|---|---|---|---|---|
| 1 | `p1_s01_intro` | §1 | C001, C002 | hook | Title card. A small image grid flattens into one long row and its neighbours scatter; then a yellow kernel slides over the intact grid. | 0:45 |
| 2 | `p1_s02_sliding` | §1 | C004–C011, C013 | intuition, mechanism, worked example | 3×4 grid of symbols, 2×2 yellow kernel, six positions: first two slowly with the full sum, the rest fast, building the 2×3 blue map. Then the same on numbers ([added] example values). Size check 3−2+1, 4−2+1. | 2:45 |
| 3 | `p1_s03_formula` | §1 | C003, C012 | formula | The double-sum formula built term by term, each term pointing at the grid. Side by side: continuous integral with a flipped kernel vs the unflipped discrete sum ("really cross-correlation"). Four stencil steps as a row of boxes. | 1:30 |
| 4 | `p1_s04_padding_why` | §2 | C014–C017 | intuition | 5×5 grid shrinking layer after layer to 1×1. Counter per pixel: corner 1, centre 9 (computed). Then a ring of dark zero cells appears. | 1:15 |
| 5 | `p1_s05_padding_math` | §2 | C018–C029 | formula, worked example | Valid vs same: 5×5 → 3×3 and padded 7×7 → 5×5; 7×7 → 9×9 padded. Derivation of P = (F−1)/2. Odd-F rule with an F = 4 counter-case. Four reasons as four short lines, one at a time. | 2:30 |
| 6 | `p1_s06_edges` | §3 | C030–C033, C046, C047 | mechanism | Sobel Gx and Gy with blue/red entries run on a synthetic image (computed); magnitude and angle formula; Canny as four boxes, with hysteresis on a number line (two thresholds). | 2:15 |
| 7 | `p1_s07_blur` | §3 | C034–C038, C048–C050 | mechanism | Gaussian formula, the 3×3 kernel (sum 16) and 5×5 kernel built as the outer product of 1 4 6 4 1 (sum 256); box kernels; blur computed on the synthetic image. Slide 21 correction on screen. | 2:00 |
| 8 | `p1_s08_sharpen` | §3 | C039–C041, C044, C045, C051–C053 | mechanism, why it matters | Laplacian 4- and 8-neighbour kernels (with the sign note), identity + Laplacian = unsharp mask, sum 0 vs sum 1 on a flat patch (computed). Taj Mahal slide figure. Three kernel families as one summary screen. | 2:15 |
| 9 | `p1_s09_dilated` | §3 | C042, C043, C054 | mechanism, formula | 3×3 kernel taps spreading apart to cover 5×5 with 9 weights; F_eff = r(F−1)+1 for r = 1, 2. Hand-made kernel numbers turn green: learned kernels. | 1:15 |
| 10 | `p1_s10_volumes` | §4 | C055–C064 | mechanism, formula | 1D row A B C B C A B with a length-3 window. RGB volume as three stacked sheets; a filter of the same depth slides across width and height only; one filter → one sheet; K filters → depth K. Triple-sum formula. Parameter count K(F²D₁+1). Slide figure image43. | 2:45 |
| 11 | `p1_s11_recap` | §1–4 | recap of the above | recap | Five lines, one at a time. | 0:40 |

### Part 2: sizes, networks, pooling, flatten (guide sections 5–9)

| # | Scene | Guide | Coverage IDs | Stage | Main visual | ~Length |
|---|---|---|---|---|---|---|
| 1 | `p2_s01_intro` | §5 | C065 | hook | Title card. A layer box with "? × ? × ?" on its output. | 0:30 |
| 2 | `p2_s02_output_size` | §5 | C066–C069 | mechanism, formula | A 1D strip of cells with padding; window stepping with S = 1, then S = 2; the five derivation steps drawn on the strip; the formula growing in three versions (slides 69, 74, 78); D₂ = K. | 2:30 |
| 3 | `p2_s03_alexnet_lenet` | §6 | C070–C076 | worked example | AlexNet conv1: 227, 11, 4, 0 substituted into the formula → 55×55×96; 363 → 364 → 34,944 parameters; 290,400 activations. Same for LeNet-5: 28×28×6, 156, 4,704. Slide figures image48 and image50. All numbers computed. | 2:45 |
| 4 | `p2_s04_why_not_dense` | §7 | C077–C079 | intuition | Three problems of a dense network on images: 3 × 10⁹ weight count, a flattened grid losing neighbours, a shifted shape lighting up different weights. | 1:15 |
| 5 | `p2_s05_sparse_shared` | §7 | C080–C082, C091, C092 | mechanism, formula | 4×4 numbered pixels and h₁₁: 16 lines (dense) vs 4 lines to pixels 1, 2, 5, 6; h₁₂ with the stride note (correction 1). Same four yellow weights reused at every position. Reduction formula → 75%. Shift-in, shift-out demo (computed). | 2:30 |
| 6 | `p2_s06_learning` | §7 | C083–C090 | why it matters | Random kernel numbers turning green during "training"; Xavier / He named; edges → textures → objects as three stages; the six advantages, one line at a time in two screens. | 2:00 |
| 7 | `p2_s07_pooling_idea` | §8 | C093–C101, C103 | intuition, formula | Three problems (correction 3), teal window taking a max and a mean, global average and global max collapsing a map to one number per channel, properties, hyperparameters (correction 4), the size formula with D₂ = D₁, the two trade-offs. | 2:30 |
| 8 | `p2_s08_pooling_examples` | §8 | C102, C104–C106 | worked example | Slide 94 map: max [[12, 7], [13, 14]] and average [[9, 5], [7, 8]]. Slides 98–106 map: stride 2 → [[8, 4], [7, 5]], stride 1 → 3×3. First windows slow, rest fast. Slide figure image64. | 2:15 |
| 9 | `p2_s09_flatten` | §9 | C107–C113 | mechanism, formula | Pipeline boxes conv → pool → flatten → dense → softmax. 3×3 map unrolling row by row into a 9-cell column. L = W·H·C; 9 × 10 + 10 = 100 parameters. Slide figure image68. | 2:00 |
| 10 | `p2_s10_recap` | §5–9 | recap of the above | recap | Five lines, one at a time. | 0:45 |

## Numbers to verify (each gets an assert)

- [added] numeric convolution example in `p1_s02_sliding`: `scipy.signal.correlate2d(image, kernel, mode="valid")`, shape (2, 3).
- Output sizes: 3×4 with 2×2 → 2×3; 5×5 with 3×3, P = 0 → 3; P = 1 → 5; same padding for F = 5 → P = 2; 7×7 with P = 1 → 9×9 padded.
- Window counts for a 3×3 kernel on an unpadded image: corner pixel 1, central pixel 9.
- Kernel sums: Sobel Gx, Gy = 0; Gaussian 3×3 = 16 before scaling; Gaussian 5×5 = 256 and equal to the outer product of [1, 4, 6, 4, 1]; box 3×3 = 9, 5×5 = 25; both Laplacians = 0; unsharp = 1; unsharp = identity + 4-neighbour Laplacian.
- Dilation: F = 3, r = 1 → 3; r = 2 → 5; 9 non-zero weights.
- AlexNet conv1: (227 − 11)/4 + 1 = 55; 11·11·3 = 363; 96·363 = 34,848; 96·364 = 34,944; 55·55·96 = 290,400.
- LeNet-5 conv1: (32 − 5)/1 + 1 = 28; 6·25 = 150; 6·26 = 156; 28·28·6 = 4,704.
- Dense count: 1000·1000·3 = 3,000,000; × 1,000 = 3 × 10⁹.
- Receptive fields on a 4×4 image numbered 1–16, 2×2 kernel: first window {1, 2, 5, 6}; stride 2 second window {3, 4, 7, 8}; stride 1 second window {2, 3, 6, 7}. Reduction 1 − 4/16 = 75%.
- Pooling, slide 94 map [[8,7,5,3],[12,9,5,7],[13,2,10,3],[9,4,5,14]]: max [[12,7],[13,14]], average [[9,5],[7,8]].
- Pooling, slides 98–106 map [[1,4,2,1],[5,8,3,4],[7,6,4,5],[1,3,1,2]]: stride 2 → [[8,4],[7,5]]; stride 1 → [[8,8,4],[8,8,5],[7,6,5]].
- Stride 2 pooling on 4×4: 2 per axis (half), 4 of 16 cells (a quarter).
- Flatten: [[1,1,0],[4,2,1],[0,2,1]] → [1,1,0,4,2,1,0,2,1]; 9·10 = 90 weights, + 10 biases = 100.

## Source mistakes found (shown on screen and spoken, one line each)

- §7 L659: `h12` = {3, 4, 7, 8} with no stride given → the video says this is the stride-2 window; at stride 1 it is {2, 3, 6, 7}.
- §3 L306–307: the centre −8 kernel is called "inverted" → the video says it has the usual sign and the centre +4 kernel is the negative; both sum to 0 and find edges.
- §8 L728: "two engineering bottlenecks" → three.
- §8 L765: "50% spatial reduction" → half per axis, a quarter of the cells.
- Slide 21 (guide L302): average kernels labelled "Gaussian" → labelled average (box) kernels.

## Added content (marked [added] in the script)

- `p1_s02_sliding`: one numeric convolution example, "example values" on screen.
- Synthetic test image (a bright square on a dark background) for the Sobel, blur and sharpen demos, "example values" on screen.
- Title cards and the two recap scenes (bridging only, no new facts).
