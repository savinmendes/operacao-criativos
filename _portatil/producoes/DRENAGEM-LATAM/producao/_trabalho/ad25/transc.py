# -*- coding: utf-8 -*-
import json, subprocess, sys, tempfile
from pathlib import Path
from faster_whisper import WhisperModel
n, vad = sys.argv[1], sys.argv[2] == "1"
src = Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\originais") / f"{n}.mp4"
if len(sys.argv) > 3: src = Path(sys.argv[3])
out = Path(sys.argv[4]) if len(sys.argv) > 4 else Path(r"C:\Users\PICHAU\Downloads\DRENAGEM-LATAM\producao\_trabalho") / f"ad{n}" / "palavras.json"
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(str(wav), language="es", word_timestamps=True, vad_filter=vad, condition_on_previous_text=False)
pal = []
for s in segs:
    for w in s.words:
        pal.append([w.word.strip(), round(w.start, 2), round(w.end, 2)])
    print(f"{s.start:.1f}", s.text, flush=True)
out.write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
print("OK", len(pal))
