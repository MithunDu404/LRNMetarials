# Explainer Video: Setup Guide

How to set up and build 3Blue1Brown-style explainer videos for any topic.
Stack: **Manim Community Edition** (animation) + **MiKTeX** (LaTeX maths) + **Sarvam AI** (voice) + **ffmpeg** (joining, loudness) + **uv** (Python environment).

> The look, colours, motion and Topic Sheet are in the [Theme and Style Guide](Explainer%20Video%20-%20Theme%20and%20Style.md). Read it first.
> Commands are for **Windows PowerShell**. Versions checked 10 Nov 2026: Manim CE 0.22.1, sarvamai 0.1.45, MiKTeX 25.12 (winget), uv 0.12.1.

---

## 0. For the builder (person or AI session): the order of work

**Once per machine:** §1 check tools → §2 install MiKTeX → §3 create the projects root → §6 test render.

**For every new video:**

1. Read the Theme and Style Guide.
2. Make the video folder (§4).
3. Read the whole source (every slide or page, including image-only ones).
4. Fill in `TOPIC_SHEET.md` (style guide §11): role colours, symbols, scene plan, numbers to verify, source mistakes. Ask the user to approve it.
5. Write `script.json` (narration, line by line) and get it approved.
6. Voice it: `make_voice.py` (§5).
7. Build one scene at a time. Render with `-ql`, look at it, fix, then move on (§7).
8. Final render (`-qh`), join, normalise loudness (§8).
9. Quality check (§9) before calling it done.

Don't skip steps 4–5. Changing the script after animating means re-timing every scene.

---

## 1. Tools

| Tool | Needed for | Check command |
|---|---|---|
| Python ≥ 3.11 (3.12 recommended) | Manim 0.22.1 needs ≥ 3.11 | `py -3.12 --version` |
| uv | the project's own environment | `uv --version` |
| ffmpeg | converting voice files, joining scenes, loudness | `ffmpeg -version` |
| MiKTeX | `Tex` / `MathTex` (provides `latex` and `dvisvgm`) | `latex --version` |
| Manim CE 0.22.1, sarvamai, python-dotenv, numpy, scipy | installed into the project (§3) | `uv run manim checkhealth` |
| Sarvam API key | voice | in `.env` (§3) |

Install anything missing:

```powershell
winget install --id Python.Python.3.12 -e
```

```powershell
winget install --id astral-sh.uv -e
```

```powershell
winget install --id Gyan.FFmpeg -e
```

Not needed: Kokoro, Remotion, Node, Blender, ImageMagick, Inkscape, a GPU. Manim's default renderer (Cairo) runs on the CPU, and Manim writes video through PyAV (installed with it), so ffmpeg is only for our own steps.

> **This laptop (checked 10 Nov 2026):** Windows 11, Ryzen 7 7435HS, 16 GB RAM, RTX 2050. Python 3.12.10, uv 0.12.1, ffmpeg 9.0.1 and VS Code are installed. MiKTeX, Manim and sarvamai are **not** installed yet.

---

## 2. Install MiKTeX (once per machine)

```powershell
winget install --id MiKTeX.MiKTeX -e
```

1. **Close and reopen** the terminal (and VS Code) so PATH updates.
2. MiKTeX Console (Start menu) → **Updates** → *Check for updates* → *Update now*.
3. Let MiKTeX fetch missing LaTeX packages without pop-ups:

   ```powershell
   initexmf --set-config-value=[MPM]AutoInstall=1
   ```

4. Check both programs Manim calls:

   ```powershell
   latex --version
   ```

   ```powershell
   dvisvgm --version
   ```

Manim's default formula template is `\documentclass[preview]{standalone}` with `babel` (English), `amsmath` and `amssymb`. MiKTeX downloads these on the first formula render, so that render is slow and later ones are fast.

---

## 3. Create the projects root (once)

One root folder holds the Python environment, the shared files and one subfolder per video.
Here it is `C:\PROJECTS\Learnmat\academics\ml\endSem\videos`, but any folder works. Nothing below depends on the path.

```powershell
cd C:\PROJECTS\Learnmat\academics\ml\endSem\videos
```

```powershell
uv init --bare --python 3.12 --no-workspace
```

```powershell
uv add manim==0.22.1 sarvamai python-dotenv numpy scipy
```

```powershell
uv run manim checkhealth
```

`checkhealth` should find Manim, `latex` and `dvisvgm`. Fix anything it flags first. Always run commands as `uv run ...` from the root. No activation needed.

**Root layout**

```
videos/                                  ← projects root (run every command from here)
├── Explainer Video - Theme and Style.md
├── Explainer Video - Setup Guide.md
├── pyproject.toml, uv.lock, .venv/       ← made by uv
├── .env                                  ← SARVAM_API_KEY (never committed)
├── .gitignore
├── theme.py                              ← shared look (style guide §14, copy as is)
├── voiced.py                             ← VoicedScene base class (§5)
├── make_voice.py                         ← Sarvam voice tool (§5)
├── cnn/                                  ← one folder per video (§4)
└── ann/
```

**`.gitignore`** (if the root is inside a git repo):

```gitignore
.venv/
.env
__pycache__/
*/media/
*/audio/
*/out/
```

Renders and audio are large and can be remade. Scripts, scenes and Topic Sheets are committed.

**`.env`**:

```dotenv
SARVAM_API_KEY=your-key-here
```

Never put the key in a scene file, a doc, a commit or a chat message.

**`theme.py`**: copy the code block from the style guide §14 into `videos/theme.py`.

---

## 4. Start a new video

Pick a short lowercase folder name (`cnn`, `ann`, `backprop`, `binary_search`):

```
videos/<slug>/
├── TOPIC_SHEET.md        ← filled from the style guide §11 template
├── source/               ← the PPT/PDF/notes this video explains (or a link list)
├── script.json           ← narration, line by line
├── scenes/
│   ├── s01_intro.py
│   └── s02_<idea>.py
├── audio/                ← made by make_voice.py
├── media/                ← made by Manim
└── out/                  ← final joined video
```

**`script.json`**: scenes in order, lines in order. Keys are the scene file name without `.py`.

```json
{
  "s01_intro": [
    {"id": "l01", "text": "How does a computer find the edges in a photo?"},
    {"id": "l02", "text": "It slides a tiny grid of numbers over the image."}
  ],
  "s02_sliding": [
    {"id": "l01", "text": "Think of the image as a grid of numbers."}
  ]
}
```

---

## 5. Voice (Sarvam) and the voiced scene

**Settings that already work on this laptop** (from `C:\PROJECTS\Explainer\reelkit\voices.py`):

| Setting | Value |
|---|---|
| Model | `bulbul:v4-flash` |
| Call | `client.text_to_speech.convert_stream(...)` |
| Language | `en-IN` (English) · `hi-IN` (Hindi) |
| Output | mp3, 24000 Hz (converted to 48 kHz wav below) |
| Text per request | ≤ 1,500 characters, whole sentences (API limit 2,500) |
| Cost (from the kit's note) | ₹1 per 1,000 characters, so a 10-min video ≈ ₹10 |

Pick the speaker in the Sarvam dashboard and write its exact name in the Topic Sheet. Use one speaker for the whole video.

### `make_voice.py` (root)

```python
# make_voice.py: voice <slug>/script.json with Sarvam.
# Writes <slug>/audio/<scene>/<id>.wav and <slug>/audio/voice.json ({"scene/id": {"seconds", "text"}}).
# Usage:  uv run python make_voice.py <slug> <speaker> [language]      e.g.  cnn shubh en-IN
import json, os, subprocess, sys, wave
from pathlib import Path
from dotenv import load_dotenv
from sarvamai import SarvamAI

slug, speaker = sys.argv[1], sys.argv[2]
lang = sys.argv[3] if len(sys.argv) > 3 else "en-IN"
MODEL, SR = "bulbul:v4-flash", 24000

root = Path(__file__).resolve().parent
load_dotenv(root / ".env")
client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])

video = root / slug
script = json.loads((video / "script.json").read_text(encoding="utf-8"))
index_path = video / "audio" / "voice.json"
index = json.loads(index_path.read_text(encoding="utf-8")) if index_path.exists() else {}

for scene, lines in script.items():
    for line in lines:
        key, text = f"{scene}/{line['id']}", line["text"].strip()
        wav = video / "audio" / scene / f"{line['id']}.wav"
        if wav.exists() and index.get(key, {}).get("text") == text:
            continue                                   # already voiced and unchanged: no cost
        assert len(text) <= 1500, f"{key} is longer than 1,500 characters; split it"
        wav.parent.mkdir(parents=True, exist_ok=True)
        mp3 = b"".join(client.text_to_speech.convert_stream(
            text=text, language_code=lang, speaker=speaker, model=MODEL,
            pace=1.0, speech_sample_rate=SR, output_audio_codec="mp3"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "-", "-ac", "1", "-ar", "48000", str(wav)],
                       input=mp3, check=True)
        with wave.open(str(wav)) as w:
            index[key] = {"seconds": round(w.getnframes() / w.getframerate(), 3), "text": text}
        index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{key}: {index[key]['seconds']} s")
```

```powershell
uv run python make_voice.py cnn <speaker-name>
```

A line is only re-voiced when its text changes, so editing one line costs one line.

> This script uses the same Sarvam call as the user's explainer kit, but it hasn't been run yet. Test it on a 2-line `script.json` first.

### `voiced.py` (root): the base class every scene uses

```python
# voiced.py: a Scene that plays narration lines made by make_voice.py, with subtitles.
import json
from pathlib import Path
from manim import Scene


class VoicedScene(Scene):
    video_dir: Path = None          # each scene sets: Path(__file__).resolve().parents[1]

    def setup(self):
        self.voice = json.loads((self.video_dir / "audio" / "voice.json").read_text(encoding="utf-8"))

    def say(self, key, *animations, max_anim=2.0):
        """Play line `key` ("scene/id"). Animations take up to max_anim s (or 70% of the line), then hold."""
        line = self.voice[key]
        length = line["seconds"]
        self.add_sound(str(self.video_dir / "audio" / f"{key}.wav"))
        self.add_subcaption(line["text"], duration=length)
        if animations:
            run = min(length * 0.7, max_anim)
            self.play(*animations, run_time=run)
            self.wait(max(length - run, 0.01))
        else:
            self.wait(length)

    def pause(self, seconds=1.5):
        """Silent hold after a key reveal (style guide §9)."""
        self.wait(seconds)
```

### A scene file

Manim only adds the scene file's own folder to Python's import path. These first lines let every scene import the shared files from the root.

```python
# videos/<slug>/scenes/s02_sliding.py
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]          # videos/
sys.path.insert(0, str(ROOT))

import numpy as np
from scipy.signal import correlate2d
from theme import *
from voiced import VoicedScene


class S02Sliding(VoicedScene):
    video_dir = Path(__file__).resolve().parents[1]  # videos/<slug>/

    def construct(self):
        image = np.array([[1, 2, 0, 1], [0, 1, 3, 1], [2, 1, 0, 0]])
        kernel = np.array([[1, 0], [0, 1]])
        feature = correlate2d(image, kernel, mode="valid")
        assert feature.tolist() == [[2, 5, 1], [1, 1, 3]]   # computed, then checked (example values)

        title = section_title("Sliding the kernel")
        img = grid(image).shift(LEFT * 3)
        self.say("s02_sliding/l01", FadeIn(title), Create(img))
        ...
```

Name classes in CamelCase matching the file (`s02_sliding.py` → `S02Sliding`).

---

## 6. First test render (once per machine)

Save as `videos/test_scene.py`:

```python
from manim import *

class SetupTest(Scene):
    def construct(self):
        title = Tex("Setup test", font_size=48)
        formula = MathTex(r"W_2 = \left\lfloor \frac{W_1 - F + 2P}{S} \right\rfloor + 1",
                          font_size=48, tex_to_color_map={"F": YELLOW})
        cells = VGroup(*[Square(0.6, stroke_color=GREY_D, stroke_width=2) for _ in range(16)]).arrange_in_grid(4, 4, buff=0)
        window = Square(1.2, stroke_color=YELLOW, stroke_width=6).move_to(cells[0].get_corner(UL), aligned_edge=UL)
        VGroup(title, formula, VGroup(cells, window)).arrange(DOWN, buff=0.6)
        self.play(Write(title), Write(formula))
        self.play(Create(cells), Create(window))
        self.play(window.animate.shift(RIGHT * 0.6))
        self.wait(1)
```

```powershell
uv run manim -pql test_scene.py SetupTest
```

Expected: a white title, the formula with only **F** in yellow, a grey 4×4 grid and a yellow 2×2 window stepping one cell right. The first run is slow (MiKTeX downloads packages). Delete `test_scene.py` and `media/` afterwards.

---

## 7. Build scenes

Render one scene at a time from the root, with the video's own media folder:

```powershell
uv run manim -ql --media_dir cnn/media cnn/scenes/s02_sliding.py S02Sliding
```

| Flag | Output | Use for |
|---|---|---|
| `-ql` | 854×480, 15 fps | building and checking a scene |
| `-qm` | 1280×720, 30 fps | checking timing with the voice |
| `-qh` | 1920×1080, 60 fps | **final** |
| `-qh --fps 30` | 1920×1080, 30 fps | final, smaller and faster |
| `-s` | last frame as PNG | checking a layout without rendering video |
| `-p` | opens the result | |

**AI builders:** you can't watch a video, so check layouts with `-s` (last frame) or by pulling frames with ffmpeg, then look at the PNGs:

```powershell
ffmpeg -v error -i cnn/media/videos/s02_sliding/480p15/S02Sliding.mp4 -vf "fps=1/3,scale=640:-1,tile=4x3" -frames:v 1 cnn/out/s02_contact.png
```

Look for overlapping labels, text off-screen, wrong colours and numbers that don't match the asserts.

---

## 8. Final render, join, loudness

Render every scene with `-qh`, then list them in order in `<slug>/out/list.txt` (paths are relative to that file):

```text
file '../media/videos/s01_intro/1080p60/S01Intro.mp4'
file '../media/videos/s02_sliding/1080p60/S02Sliding.mp4'
```

Join and normalise to YouTube's loudness (−14 LUFS):

```powershell
ffmpeg -f concat -safe 0 -i cnn/out/list.txt -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k cnn/out/cnn_full.mp4
```

All scenes share the same settings, so the video is copied as is (fast). Only the audio is processed. Each scene's subtitle file is next to its mp4 (`.srt`). Join them in order if you want one subtitle file for the full video.

---

## 9. Done means

- [ ] Every scene in the Topic Sheet is rendered at final quality.
- [ ] Every number in "Numbers to verify" has a passing `assert` in a scene file.
- [ ] Every source mistake listed is corrected on screen and in the voice.
- [ ] Contact sheet of each scene checked: no overlaps, nothing outside the safe margin, colours follow the Topic Sheet.
- [ ] The voice matches `script.json` (listen once, or transcribe and compare).
- [ ] The full video plays start to end with no gaps or audio jumps between scenes.
- [ ] No π creatures, mascot, presenter or 3Blue1Brown branding.

---

## 10. Optional: preview in VS Code

The **Manim Sideview** extension renders the scene under the cursor and shows it in a side panel. Point its Manim path at `.venv\Scripts\manim.exe`.

---

## 11. Troubleshooting

| Problem | Fix |
|---|---|
| `latex` / `dvisvgm` "not recognised" | Reopen the terminal. Still failing: add MiKTeX's bin folder to PATH (per-user install: `%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64`). |
| MiKTeX pop-up mid-render | Auto-install is off: run the `initexmf` command in §2 again. |
| `import manim` fails: "An Application Control policy has blocked this file" (ManimPango) | Windows Smart App Control blocks ManimPango's DLLs on this laptop. Render with `uv run python render.py <same arguments as manim>` instead of `uv run manim`. Scenes can use `Tex`/`MathTex` only, not `Text()` or `Code`. |
| Sarvam 400 "Speaker ... is not compatible with model" | `bulbul:v4-flash` needs the full speaker name, e.g. `shubh_en_narration`, not `shubh`. The error message lists every valid name. |
| `LaTeX compilation error` | `uv run manim checkhealth`. The full log is in `<media_dir>/Tex/`; find the first line starting with `!`. Usually a typo in `MathTex` (use raw strings `r"..."`) or a missing package (update MiKTeX). |
| `ModuleNotFoundError: theme` | The scene is missing the `sys.path.insert(0, ...)` lines from §5, or the file isn't at `videos/<slug>/scenes/`. |
| `KeyError` in `say(...)` | The line isn't voiced yet, or the key is wrong. Run `make_voice.py` again; keys are `"<scene file name>/<id>"`. |
| Sarvam 401 / 403 | Check `SARVAM_API_KEY` in `videos/.env`. |
| Voice and visuals drift | Script changed after voicing: re-run `make_voice.py`. Never type durations by hand. |
| Whole formula turned one colour | Use `tex_to_color_map=...`, not `set_color_by_tex` on an unsplit formula. |
| Renders are slow | Build with `-ql`, use `-s` for layout checks, `-qh` only at the end. Manim caches unchanged animations. |
| PowerShell blocks `Activate.ps1` | Not needed: always use `uv run`. |
