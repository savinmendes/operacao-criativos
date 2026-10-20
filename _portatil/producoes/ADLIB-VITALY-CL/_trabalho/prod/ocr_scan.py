# -*- coding: utf-8 -*-
"""OCR quadro a quadro (ou N fps) procurando termos. python ocr_scan.py video.mp4 fps termo1,termo2 [saida.txt]"""
import sys, re, subprocess, unicodedata
import numpy as np
from rapidocr_onnxruntime import RapidOCR
v, fps, termos = sys.argv[1], sys.argv[2], sys.argv[3].split("|")
out = sys.argv[4] if len(sys.argv) > 4 else None
def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.upper()) if unicodedata.category(c) != "Mn").replace(" ", "")
TN = [norm(t) for t in termos]
p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.split(",")
W, H = int(p[0]), int(p[1])
vf = [] if fps == "all" else ["-vf", f"fps={fps}"]
proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", v, *vf, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
eng = RapidOCR()
step = 1 / 30 if fps == "all" else 1 / float(fps)
hits = []; i = 0; last = None; feitos = 0
import time; t0 = time.time()
while True:
    b = proc.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    fr = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    pq = fr[::8, ::8].astype(np.int16)
    if last is not None and np.abs(pq - last).mean() < 1.5:   # quadro quase igual ao último lido: reaproveita
        for t, tn in zip(termos, TN):
            if tn in n: hits.append(f"{i * step:7.2f}s  [{t}]  (igual ao anterior)")
        i += 1; continue
    last = pq; feitos += 1
    if feitos % 100 == 0: print(f"  [{i}] {i * step:.1f}s  ocr={feitos}  {time.time() - t0:.0f}s", flush=True)
    r, _ = eng(fr)
    txt = " | ".join(x[1] for x in (r or []))
    n = norm(txt)
    for t, tn in zip(termos, TN):
        if tn in n:
            hits.append(f"{i * step:7.2f}s  [{t}]  {txt[:160]}")
    i += 1
res = "\n".join(hits) if hits else "nenhum"
print(f"{v}: {i} quadros; achados: {len(hits)}\n{res}")
if out: open(out, "w", encoding="utf-8").write(res)
