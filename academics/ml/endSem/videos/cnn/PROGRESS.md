# Progress: CNN video (ML Lec 12)

Source: `cnn/source/ML_Lec_12_CNN_Learning_Guide.md` (947 lines, 9 sections) plus 9 figures in `cnn/source/extracted_ML_Lec_12_CNN/media/`.
Process: `Explainer Video - Builder Prompt.md` (phases 1 to 7).

## Current phase

**Phase 7 finished on 11 Nov 2026.** Final files: `cnn/out/cnn_part1.mp4` (21:05) and `cnn/out/cnn_part2.mp4` (18:53), 1920x1080, 30 fps, -14.2 LUFS, each with a `.srt`.
Next step: none required. Open items are in "Not verified" below. To change a line: edit `cnn/build_script.py`, run it, re-run `make_voice.py cnn shubh_en_narration en-IN 1.1` (only changed lines are re-voiced), `uv run python cnn/build_scene.py <scene> -qh`, then `uv run python cnn/join.py`.

Voice: `shubh_en_narration`, `en-IN`, pace 1.1 (user asked for 1.10x on 11 Nov 2026). `make_voice.py` now takes the pace as an optional 4th argument. 233 lines, 37.1 min of speech.
Tools added: `render.py` (root), `cnn/build_script.py`, `cnn/build_scene.py` (render + contact sheet), `cnn/join.py`, `cnn/scenes/common.py`.

## Not verified

- Nobody has listened to the audio except the user's check of the intro at pace 1.0. Pronunciation of spoken symbols ("W 1", "I one one") and numbers across the other 20 scenes is unheard.
- Voice/visual sync is enforced only by timing code (animations are placed at fractions of each line and cannot overrun it); it was not watched.
- Contact sheets (16 frames per scene) were checked at 480p for every scene; the 1080p renders were not re-inspected frame by frame.

Script source of truth: `cnn/build_script.py`. Edit narration there and run `uv run python cnn/build_script.py`; it regenerates `script.json` and `SCRIPT_REVIEW.md` and fails if any of the 113 coverage IDs is no longer referenced.

Phase 2 answers ("All defaults") are in `DECISIONS.md`.
Blocker resolved (decision k): render with `uv run python render.py <manim args>`, never `uv run manim`. A test scene with `theme.py`, `MathTex`, `DecimalNumber`, a grid and a subcaption rendered correctly at `-ql` on 11 Nov 2026. `Text()` and `Code` are unavailable.

## Done

- Phase 1: both guides and the whole source read; all 9 figures opened; folder created; source copied; `COVERAGE.md` written.
- Phase 3 (environment check, run early on 11 Nov 2026):
  - OK: uv 0.12.1, ffmpeg 9.0.1, MiKTeX 25.12 (`latex`), dvisvgm 3.4.3, `SARVAM_API_KEY` present in `.env`, `theme.py`, `voiced.py`, `make_voice.py` match the guides.
  - OK imports: numpy, scipy, cairo, av, PIL, moderngl, sarvamai.
  - **BLOCKED:** `import manim` fails. Windows Smart App Control (enforced) blocks `.venv/Lib/site-packages/manimpango/enums.cp313-win_amd64.pyd` (Code Integrity events 3077/3033). Nothing can be rendered until the user decides how to handle this.
  - Note: the venv is Python 3.13.14, the setup guide says 3.12. Not a problem by itself.
  - MiKTeX warns it has never checked for updates.

## Blocker options (user's choice, not yet decided)

1. Render through a small wrapper that supplies a stand-in `manimpango` module, so the blocked file is never loaded. Works because the style guide uses only `Tex`/`MathTex`; `Text()` and `Code` would not work.
2. The user changes Smart App Control themself (Windows Security; turning it off cannot be undone without resetting Windows).
3. Render on another machine or in WSL.

## Scenes

Planned: 21. Scripted: 21. Voiced: 21. Built: 21. Checked: 21 (contact sheets in `cnn/out/`). All 113 coverage items are marked done.
Outputs will be `cnn/out/cnn_part1.mp4` and `cnn/out/cnn_part2.mp4`.

## Suspected source issues (to be settled in Phase 2, question g)

1. §7, line 659: `h12` uses pixels {3, 4, 7, 8}. With the 2×2 kernel at stride 1 the second window is {2, 3, 6, 7}; {3, 4, 7, 8} means stride 2. The stride is not stated.
2. §3, lines 306 to 307: sign labels. Centre −8 with +1 neighbours is the ordinary (positive) Laplacian; centre +4 with −1 neighbours is the negated one. The guide calls the −8 kernel "inverted".
3. §8, line 728: says "two engineering bottlenecks" and lists three.
4. §8, line 765: stride 2 "yielding a 50% spatial reduction" is 50% per axis, 75% fewer cells.
5. §7, line 638: "an ImageNet photograph (1000 × 1000 × 3)". ImageNet images are not that size; the number works only as an illustration.
6. §3, line 322: dilation "expands receptive field exponentially across layers" holds only when the rate grows layer by layer.
7. §3, line 308 vs 309: unsharp masking is defined with a blur, `I + α(I − I_blur)`, but the kernel shown is identity + Laplacian. Related, not identical.
8. Figure `fig_dense_vs_cnn_connectivity.png` says "75% to 98% reduction"; the text derives only 75%. (16 × 16 = 256 weights vs 4 shared gives 98.4%.)
9. Slide 21 mislabel (average kernels called Gaussian): already noted by the guide itself.
