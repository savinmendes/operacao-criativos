# -*- coding: utf-8 -*-
"""Troca trechos de um vídeo por clipes corrigidos (mesma resolução), quadro a quadro, mantendo o áudio.

  python substituir_trechos.py base.mp4 saida.mp4 trechos.json
trechos.json = [{"clipe": "take1_final.mp4", "inicio": 7.367, "quadros": 190}, ...]
  inicio  = segundo no vídeo base onde o clipe entra
  quadros = quantos quadros do clipe usar (opcional: usa o clipe inteiro)
"""
import json
import subprocess
import sys

import cv2

base, saida, cfg = sys.argv[1], sys.argv[2], sys.argv[3]
trechos = json.load(open(cfg, encoding="utf-8"))
cap = cv2.VideoCapture(base)
fps = cap.get(cv2.CAP_PROP_FPS)
W, H = int(cap.get(3)), int(cap.get(4))
troca = {}
for t in trechos:
    c = cv2.VideoCapture(t["clipe"])
    i0 = int(round(t["inicio"] * fps))
    n = t.get("quadros", 10 ** 9)
    k = 0
    while k < n:
        ok, im = c.read()
        if not ok:
            break
        troca[i0 + k] = cv2.resize(im, (W, H)) if im.shape[:2] != (H, W) else im
        k += 1
    print(f"{t['clipe'].split(chr(92))[-1]}: {k} quadros a partir de {t['inicio']}s")

ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", f"{fps}", "-i", "-", "-i", base, "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-threads", "4",
                       "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "copy", saida],
                      stdin=subprocess.PIPE)
i = 0
while True:
    ok, im = cap.read()
    if not ok:
        break
    ff.stdin.write(troca.get(i, im).tobytes())
    i += 1
ff.stdin.close()
ff.wait()
print(f"ok: {saida} | {i} quadros, {len(troca)} trocados")
