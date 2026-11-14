# Decisions: CNN video (ML Lec 12)

Answered by the user on 11 Nov 2026 with "All defaults" to the Phase 2 questions. Each line is the default that was offered.

| # | Question | Decision |
|---|---|---|
| a | Audience | B.Tech students revising for the end-sem; they have seen ANNs, not CNNs. |
| b | Language and tone | English (`en-IN`), calm teacher. |
| c | Length | Two parts of about 14 minutes. Part 1 = guide sections 1–4, Part 2 = sections 5–9. |
| d | Depth | Everything covered; extra time on exam-style calculations (output size, AlexNet/LeNet parameters, pooling examples). |
| e | Skip / reorder | Nothing skipped. Guide order kept. |
| f | Examples | One small numeric convolution example is added to the symbolic walk-through, marked "[added]" in the script and "example values" on screen, computed in code. |
| g | Source issues | 1–4 are corrected on screen with a one-line note. 5–8 stay as the guide has them. 9 (slide 21) is shown as a correction, as the guide itself says. Details below. |
| h | Real images | The Taj Mahal slide figure is shown as it is. Kernels are run live only on a synthetic test image computed in code. |
| i | Voice | Sarvam speaker `shubh_en_narration`, `en-IN` (plain `shubh` is not a valid name for the model; this variant was chosen by the builder and is pending the user's OK). Voice one scene first and let the user hear it before voicing the rest. |
| j | Title and extras | Slug `cnn`. Title "Convolutional Neural Networks". Title card and recap screen in each part. No quiz. |
| k | Manim blocker | Render through `render.py`, which gives Manim a stand-in for the blocked `manimpango` module. Smart App Control is left alone. `Text()` and `Code` are not available; use `Tex`/`MathTex` only. |

## Source issues (question g)

Corrected on screen, with one spoken line each:

1. §7 L659: `h12` uses pixels {3, 4, 7, 8}. The video states the stride: {3, 4, 7, 8} is the stride-2 window; at stride 1 it would be {2, 3, 6, 7}.
2. §3 L306–307: sign of the Laplacian kernels. The video says the centre −8 kernel is the Laplacian with its usual sign and the centre +4 kernel is its negative; both detect edges and sum to 0.
3. §8 L728: "two bottlenecks" → the video says three, since three are listed.
4. §8 L765: "50% spatial reduction" → half along each axis, a quarter of the cells.
5. Slide 21: uniform 1/9 and 1/25 matrices are average (box) kernels, not Gaussian.

Left as the guide has them:

- §7 L638: the 1000 × 1000 × 3 "ImageNet photograph" (used as an illustrative size).
- §3 L322: dilation expanding the receptive field "exponentially across layers".
- §3 L308–309: unsharp masking formula with a blur beside the identity + Laplacian kernel.
- Figure `fig_dense_vs_cnn_connectivity.png`: "75% to 98% reduction".

## Still needs the user's approval

- Topic Sheet and scene plan (Phase 4).
- Script (Phase 5).
- Sending text to Sarvam (Phase 6), with the character count.
