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
