# -*- coding: utf-8 -*-
"""QA de take IA: transcreve (faster-whisper small, CPU, es) e gera folha de quadros.
python qa_video.py video.mp4"""
import subprocess, sys, json
from pathlib import Path
from faster_whisper import WhisperModel

v = Path(sys.argv[1])
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = m.transcribe(str(v), language="es", word_timestamps=True)
segs = list(segs)
txt = " ".join(s.text.strip() for s in segs)
# deteccao de idioma independente
_, info2 = m.transcribe(str(v), language=None)
print(json.dumps({"arquivo": v.name, "texto": txt, "idioma_detectado": info2.language,
                  "prob": round(info2.language_probability, 2),
                  "palavras": [(round(w.start, 2), round(w.end, 2), w.word) for s in segs for w in (s.words or [])]},
                 ensure_ascii=False))
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)]).decode().strip())
folha = v.with_name(v.stem + "_frames.jpg")
n = 6
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vf",
                f"fps={n / dur:.4f},scale=360:-1,tile={n}x1", "-frames:v", "1", "-q:v", "3", str(folha)], check=True)
print("duracao", round(dur, 2), "folha", folha)
