# -*- coding: utf-8 -*-
"""Estudo Wyz Camara: fala (faster-whisper small, idioma automático) + folha de contato (1 quadro/1,5 s, legível)."""
import json, subprocess, time
from pathlib import Path
D = Path(__file__).resolve().parent
VID = sorted((D.parent / "UNICOS").glob("*.mp4"))
(D / "fala").mkdir(exist_ok=True); (D / "folhas").mkdir(exist_ok=True)
for k, v in enumerate(VID, 1):
    sh = D / "folhas" / f"{v.stem}.jpg"
    if not sh.exists():
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vf",
                        r"fps=1/1.5,scale=240:-1,drawtext=fontfile='C\:/Windows/Fonts/arial.ttf':text='%{pts\:hms}':x=4:y=4:fontsize=16:fontcolor=yellow:box=1:boxcolor=black,tile=6x7",
                        "-frames:v", "1", str(sh)], check=True)
print("folhas ok", flush=True)
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)
t0 = time.time()
for k, v in enumerate(VID, 1):
    o = D / "fala" / f"{v.stem}.json"
    if not o.exists():
        segs, info = m.transcribe(str(v), vad_filter=True)
        o.write_text(json.dumps({"idioma": info.language, "segs": [[round(s.start, 1), round(s.end, 1), s.text.strip()] for s in segs]}, ensure_ascii=False), encoding="utf-8")
    el = time.time() - t0
    print(f"[{k}/{len(VID)}] {v.stem} | {k/len(VID):.0%} | falta ~{int(el/k*(len(VID)-k))}s", flush=True)
