# -*- coding: utf-8 -*-
import sys, subprocess, tempfile, os
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv) > 2 else "small", device="cpu", compute_type="int8", cpu_threads=4)
for src in sys.argv[1].split(","):
    wav = tempfile.mktemp(suffix=".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
    segs, _ = m.transcribe(wav, language="es", condition_on_previous_text=False)
    with open(src + ".txt", "w", encoding="utf-8") as f:
        for s in segs: f.write(f"{s.start:7.2f}-{s.end:7.2f} {s.text.strip()}\n")
    os.remove(wav); print("ok", src, flush=True)
