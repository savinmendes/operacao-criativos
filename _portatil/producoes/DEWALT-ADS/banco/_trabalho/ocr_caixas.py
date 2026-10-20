# -*- coding: utf-8 -*-
"""Passo 1 da limpeza: RapidOCR a cada PASSO quadros, dentro das zonas, e guarda as caixas de texto (720x1280).
Uso: python ocr_caixas.py config.json   (config: video, caixas_json, passo, zonas:[[x0,y0,x1,y1]], ignorar: regex, ate)"""
import sys, json, re, time, subprocess
import numpy as np
from rapidocr_onnxruntime import RapidOCR
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
ocr = RapidOCR(); passo = cfg.get("passo", 2); ign = re.compile(cfg.get("ignorar", "^$"), re.I); ace = re.compile(cfg["aceitar"]) if cfg.get("aceitar") else None
zonas = cfg.get("zonas", [[0, 0, 720, 1280]]); ate = cfg.get("ate")
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-i", cfg["video"], "-vf",
                       "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
                       "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
T = 720 * 1280 * 3; out = {}; i = 0; t0 = time.time()
while True:
    b = pr.stdout.read(T)
    if len(b) < T or (ate and i >= ate): break
    if i % passo == 0 and i >= cfg.get("ini", 0):
        f = np.frombuffer(b, np.uint8).reshape(1280, 720, 3); bx = []
        for x0, y0, x1, y1 in zonas:
            r, _ = ocr(np.ascontiguousarray(f[y0:y1, x0:x1]))
            for pts, txt, sc in (r or []):
                t = txt.strip()
                if float(sc) < 0.5 or ign.search(t.replace(" ", "")) or len(re.sub(r"\W", "", t)) < 2: continue
                if ace and not ace.search(t.replace(" ", "")): continue
                p = np.array(pts); bx.append([int(p[:, 0].min()) + x0, int(p[:, 1].min()) + y0, int(p[:, 0].max()) + x0, int(p[:, 1].max()) + y0, t])
        out[i] = bx
        if i % 60 == 0: print(f"[{i}] {time.time()-t0:.0f}s {[b[4] for b in bx]}", flush=True)
    i += 1
pr.kill()
json.dump(out, open(cfg["caixas_json"], "w", encoding="utf-8"), ensure_ascii=False)
print("ok", i, "quadros", round(time.time() - t0), "s")
