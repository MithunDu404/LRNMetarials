# build_scene.py: render one or more scenes and make a contact sheet for each.
# Usage (from videos/):  uv run python cnn/build_scene.py p1_s02_sliding [more scenes...] [-ql | -qm | -qh]
# The sheet goes to cnn/out/<scene>_contact.png (16 frames spread over the scene).
import subprocess, sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
slug = Path(__file__).resolve().parent
quality = next((a for a in sys.argv[1:] if a.startswith("-q")), "-ql")
folder = {"-ql": "480p15", "-qm": "720p30", "-qh": "1080p30"}[quality]
extra = ["--fps", "30"] if quality == "-qh" else []
failed = []
for scene in [a for a in sys.argv[1:] if not a.startswith("-")]:
    cls = "".join(p.capitalize() for p in scene.split("_"))
    r = subprocess.run([sys.executable, str(root / "render.py"), quality, *extra, "--media_dir", str(slug / "media"),
                        str(slug / "scenes" / f"{scene}.py"), cls], cwd=root, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    mp4 = slug / "media" / "videos" / scene / folder / f"{cls}.mp4"
    if r.returncode != 0 or not mp4.exists():
        tail = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()][-14:]
        print(f"FAILED {scene}\n" + "\n".join(tail))
        failed.append(scene)
        continue
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                               capture_output=True, text=True).stdout)
    (slug / "out").mkdir(exist_ok=True)
    sheet = slug / "out" / f"{scene}_contact.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp4), "-vf",
                    f"fps=16/{dur:.3f},scale=640:-1,tile=4x4", "-frames:v", "1", str(sheet)], check=True)
    print(f"OK {scene}: {dur:.1f} s -> {sheet.name}")
sys.exit(1 if failed else 0)
