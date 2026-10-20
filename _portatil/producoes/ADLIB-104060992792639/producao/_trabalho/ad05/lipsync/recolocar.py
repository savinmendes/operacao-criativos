# -*- coding: utf-8 -*-
"""Recoloca os blocos com lipsync (ls_<id>.mp4) na base_sem_legenda.mp4, quadro a quadro (24 fps).
Bloco com 'crop': a saída (720x1280) volta ao tamanho do recorte e entra só onde mudou (máscara por diferença, borda suave).
Uso: python recolocar.py [id ...]  (ids a usar; padrão = todos com ls_<id>.mp4 existente). Saída: ../base_lipsync.mp4 (bt709 tv)."""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
L = Path(__file__).parent; AD = L.parent
B = json.load(open(L/"blocos.json", encoding="utf-8"))
usar = set(sys.argv[1:]) or {k["id"] for k in B if (L/f"ls_{k['id']}.mp4").exists()}
def ler(p, n=None):
    c = cv2.VideoCapture(str(p)); fr = []
    while n is None or len(fr) < n:
        ok, f = c.read()
        if not ok: break
        fr.append(f)
    return fr
mapa = {}
for k in B:
    if k["id"] not in usar: continue
    n = k["b"] - k["a"]; fr = ler(L/f"ls_{k['id']}.mp4", n)
    if len(fr) < n: print("AVISO", k["id"], "tem", len(fr), "quadros, esperado", n); fr += [fr[-1]]*(n-len(fr))
    for j in range(n): mapa[k["a"]+j] = (k, fr[j])
print("blocos:", sorted(usar))
c = cv2.VideoCapture(str(AD/"base_sem_legenda.mp4")); N = int(c.get(7))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
out = AD/"base_lipsync.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(out)], stdin=subprocess.PIPE)
for i in range(N):
    ok, f = c.read()
    if i in mapa:
        k, g = mapa[i]
        if "crop" in k:
            x,y,w,h = k["crop"]; o = f[y:y+h, x:x+w]
            s = cv2.resize(g, (w,h), interpolation=cv2.INTER_AREA)
            d = cv2.GaussianBlur(np.abs(s.astype(np.int16)-o.astype(np.int16)).max(2).astype(np.uint8),(5,5),0)
            m = cv2.dilate((d>10).astype(np.uint8), np.ones((15,15),np.uint8)).astype(np.float32)
            m = cv2.GaussianBlur(m,(21,21),0)[...,None]
            m[:4]=0; m[-4:]=0; m[:,:4]=0; m[:,-4:]=0
            f = f.copy(); f[y:y+h, x:x+w] = np.clip(s*m + o*(1-m),0,255).astype(np.uint8)
        else:
            f = cv2.resize(g,(720,1280)) if g.shape[:2]!=(1280,720) else g
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok", out, N)
