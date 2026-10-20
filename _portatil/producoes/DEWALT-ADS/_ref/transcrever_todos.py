# -*- coding: utf-8 -*-
"""Transcreve os 50 ADs em sequência (CPU), salva _transcricoes/<nn>.json com idioma, segmentos e palavras."""
import json, os, glob
from faster_whisper import WhisperModel

os.makedirs("_transcricoes", exist_ok=True)
m = WhisperModel("small", device="cpu", compute_type="int8")
arqs = sorted(glob.glob("*AD.mp4"))
for k, f in enumerate(arqs, 1):
    out = os.path.join("_transcricoes", f.split()[0] + ".json")
    if os.path.exists(out):
        continue
    segs, info = m.transcribe(f, vad_filter=True, word_timestamps=False)
    segs = [{"ini": round(s.start, 2), "fim": round(s.end, 2), "texto": s.text.strip()} for s in segs]
    json.dump({"arquivo": f, "idioma": info.language, "prob": round(info.language_probability, 2),
               "segmentos": segs}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[{k}/{len(arqs)}] {f} {info.language} {len(segs)} seg", flush=True)
print("FIM")
