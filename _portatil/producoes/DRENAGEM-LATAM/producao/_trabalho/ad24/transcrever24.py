# -*- coding: utf-8 -*-
"""AD24: separa voz (demucs) e transcreve palavra a palavra (faster-whisper small, cpu_threads=4)."""
import json, subprocess, sys, time
from pathlib import Path
P = Path(__file__).parent
A = P / "aud"
voc = A / "htdemucs" / "orig" / "vocals.wav"
t0 = time.time()
if not voc.exists():
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems=vocals", "-j", "1", "-o", str(A), str(A / "orig.wav")],
                   check=True, env={**__import__("os").environ, "OMP_NUM_THREADS": "4", "MKL_NUM_THREADS": "4"})
print(f"demucs ok {time.time()-t0:.0f}s", flush=True)
v16 = A / "voc16.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(voc), "-ac", "1", "-ar", "16000", str(v16)], check=True)
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(str(v16), language="es", word_timestamps=True, condition_on_previous_text=False,
                       vad_filter=True)
pal, frases = [], []
for s in segs:
    frases.append([round(s.start, 2), round(s.end, 2), s.text.strip()])
    pal += [[w.word.strip(), round(w.start, 2), round(w.end, 2)] for w in s.words]
    print(f"[{s.end:6.1f}/776s] {s.end/776:.0%} {s.text.strip()[:60]}", flush=True)
(P / "palavras24.json").write_text(json.dumps(pal, ensure_ascii=False), encoding="utf-8")
(P / "frases24.json").write_text(json.dumps(frases, ensure_ascii=False, indent=0), encoding="utf-8")
print(f"FIM {time.time()-t0:.0f}s", flush=True)
