# join.py: join the final 1080p scenes into cnn_part1.mp4 and cnn_part2.mp4 (loudness -14 LUFS) with one .srt each.
# Usage (from videos/):  uv run python cnn/join.py
import json, subprocess
from datetime import timedelta
from pathlib import Path

import srt

slug = Path(__file__).resolve().parent
out = slug / "out"
out.mkdir(exist_ok=True)
scenes = list(json.loads((slug / "script.json").read_text(encoding="utf-8")))


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                                capture_output=True, text=True, check=True).stdout)


for part in ("p1", "p2"):
    names = [s for s in scenes if s.startswith(part)]
    files = []
    for s in names:
        cls = "".join(p.capitalize() for p in s.split("_"))
        f = slug / "media" / "videos" / s / "1080p30" / f"{cls}.mp4"
        assert f.exists(), f"missing final render: {f}"
        files.append(f)
    lst = out / f"list_{part}.txt"
    lst.write_text("".join(f"file '{f.as_posix()}'\n" for f in files), encoding="utf-8")
    target = out / f"cnn_part{part[1]}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", str(target)], check=True)
    # one subtitle file for the part, each scene's cues shifted by the scenes before it
    subs, offset = [], 0.0
    for f in files:
        s_path = f.with_suffix(".srt")
        if s_path.exists():
            for cue in srt.parse(s_path.read_text(encoding="utf-8")):
                cue.start += timedelta(seconds=offset)
                cue.end += timedelta(seconds=offset)
                subs.append(cue)
        offset += duration(f)
    target.with_suffix(".srt").write_text(srt.compose(subs), encoding="utf-8")
    total = duration(target)
    print(f"{target.name}: {int(total // 60)}:{int(total % 60):02d}, {len(files)} scenes, {len(subs)} subtitle cues, "
          f"sum of scenes {offset:.1f} s vs file {total:.1f} s")
