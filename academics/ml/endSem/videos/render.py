# render.py: run Manim on this laptop, where Windows Smart App Control blocks ManimPango's DLLs.
# ManimPango is only needed for Text()/MarkupText()/Code (system fonts). Our scenes use Tex/MathTex only,
# so a stand-in module is registered before Manim imports it and the blocked files are never loaded.
# Usage (same arguments as `manim`):
#   uv run python render.py -ql --media_dir cnn/media cnn/scenes/s01_intro.py S01Intro
import sys
from unittest.mock import MagicMock

sys.modules["manimpango"] = MagicMock(name="manimpango stand-in (Text/Code unavailable)")

from manim.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
