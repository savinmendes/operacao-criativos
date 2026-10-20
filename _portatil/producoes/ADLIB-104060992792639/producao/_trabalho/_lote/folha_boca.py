# -*- coding: utf-8 -*-
"""Folha de boca: final (cima) x original (baixo), com barra verde = voz ES falando, vermelha = PT.
Uso: python folha_boca.py video_final.mp4 original.mp4 narr_es.wav ini fim passo_q x,y,w,h saida.jpg [--orig-pt orig.wav]"""
import sys, cv2, numpy as np, soundfile as sf, subprocess, tempfile, os
v, o, narr, t0, t1, passo, box, saida = sys.argv[1:9]; t0, t1, passo = float(t0), float(t1), int(passo)
x, y, w, h = map(int, box.split(","))
def env(path):
    tmp = tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg","-v","error","-y","-i",path,"-ac","1","-ar","16000",tmp],check=True)
    a, sr = sf.read(tmp); os.remove(tmp); hop = sr // 30
    e = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2) + 1e-12) for i in range(len(a)//hop)])
    db = 20*np.log10(e + 1e-9); return db > (db.max() - 30)
es = env(narr); pt = env(o)
cv, co = cv2.VideoCapture(v), cv2.VideoCapture(o)
tiles = []
for q in range(int(round(t0*30)), int(round(t1*30)), passo):
    cv.set(1, q); co.set(1, q); a = cv.read()[1]; b = co.read()[1]
    if a is None or b is None: break
    A = cv2.resize(a[y:y+h, x:x+w], (160, int(160*h/w))); B = cv2.resize(b[y:y+h, x:x+w], (160, int(160*h/w)))
    bar = np.zeros((14, 160, 3), np.uint8)
    if q < len(es) and es[q]: bar[:7] = (0, 200, 0)
    if q < len(pt) and pt[q]: bar[7:] = (0, 0, 220)
    t = np.vstack([A, bar, B]); cv2.putText(t, f"{q/30:.2f}", (3, 14), 0, 0.45, (255, 255, 255), 1)
    tiles.append(t)
cols = 10; rows = [np.hstack(tiles[i:i+cols] + [np.zeros_like(tiles[0])] * (cols - len(tiles[i:i+cols]))) for i in range(0, len(tiles), cols)]
cv2.imwrite(saida, np.vstack(rows)); print(saida, len(tiles))
