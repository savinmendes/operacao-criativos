# -*- coding: utf-8 -*-
"""Revisão: whisper (es) + termos proibidos + RMS do fim.  python revisar_ad.py video.mp4 saida.txt"""
import re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from faster_whisper import WhisperModel
v = sys.argv[1]
wav = Path(tempfile.mkdtemp()) / "a.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-vn", "-ac", "1", "-ar", "16000", str(wav)], check=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(str(wav), language="es", vad_filter=False, condition_on_previous_text=False)
linhas = [f"{s.start:7.1f}-{s.end:6.1f} {s.text.strip()}" for s in segs]
termos = ["maya", "verra", "vera", "sesenta", "60", "45", "hecho en", "estados unidos", "ozempic", "tiktok", "tik tok", "cofepris",
          "c.ncer", "precio", "d.lar", "\$", "link", "enlace", "target", "walmart", "amazon", "descuento", "probado por", "registro",
          "trt", "testoster", "30 d", "treinta", "sexo", "s3xo"]
ach = [(t, l) for l in linhas for t in termos if re.search(t, l, re.I)]
x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-sseof", "-3", "-i", v, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                                 capture_output=True).stdout, np.int16).astype(float)
rms = [np.sqrt((x[i:i + 8000] ** 2).mean()) for i in range(0, len(x), 8000)]
out = "\n".join(linhas) + "\n\n== termos ==\n" + ("\n".join(f"[{t}] {l}" for t, l in ach) or "nenhum") + \
      "\n== RMS últimos 3 s (0,5 s) ==\n" + " ".join(f"{r:.0f}" for r in rms)
Path(sys.argv[2]).write_text(out, encoding="utf-8")
print("ok", len(ach))
