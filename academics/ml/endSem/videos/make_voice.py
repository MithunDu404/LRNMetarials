# make_voice.py: voice <slug>/script.json with Sarvam.
# Writes <slug>/audio/<scene>/<id>.wav and <slug>/audio/voice.json ({"scene/id": {"seconds", "text"}}).
# Usage:  uv run python make_voice.py <slug> <speaker> [language] [pace]   e.g.  cnn shubh_en_narration en-IN 1.1
import json, os, subprocess, sys, wave
from pathlib import Path
from dotenv import load_dotenv
from sarvamai import SarvamAI

slug, speaker = sys.argv[1], sys.argv[2]
lang = sys.argv[3] if len(sys.argv) > 3 else "en-IN"
pace = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
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
        if wav.exists() and index.get(key, {}).get("text") == text and index[key].get("pace", 1.0) == pace:
            continue                                   # already voiced, same text and pace: no cost
        assert len(text) <= 1500, f"{key} is longer than 1,500 characters; split it"
        wav.parent.mkdir(parents=True, exist_ok=True)
        mp3 = b"".join(client.text_to_speech.convert_stream(
            text=text, language_code=lang, speaker=speaker, model=MODEL,
            pace=pace, speech_sample_rate=SR, output_audio_codec="mp3"))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "-", "-ac", "1", "-ar", "48000", str(wav)],
                       input=mp3, check=True)
        with wave.open(str(wav)) as w:
            index[key] = {"seconds": round(w.getnframes() / w.getframerate(), 3), "text": text, "pace": pace}
        index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"{key}: {index[key]['seconds']} s")
