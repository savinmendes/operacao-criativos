# -*- coding: utf-8 -*-
"""v2: base = base_sem_legenda_lama.mp4 (legenda tirada com LaMa GPU).
- Blocos de lipsync aprovados (ls_<id>.mp4) entram quadro a quadro; nos blocos de quadro inteiro, a faixa da legenda volta a ser a
  do LaMa (máscara da legenda, borda suave), porque a saída do HeyGen foi feita sobre a base antiga (inpaint OpenCV).
- COBRIR: trechos sem lipsync viram um enquadramento (zoom) do próprio quadro em que a boca de quem fala não aparece.
Saída: ../base_lipsync.mp4 (24 fps, bt709 tv)."""
import json, subprocess, sys
from pathlib import Path
import cv2, numpy as np
L = Path(__file__).parent; AD = L.parent
USAR = sys.argv[1].split(",") if len(sys.argv) > 1 else ["c1","m1","c2","c3","m3","m4","m5","d1","d2","d3","d4","d5"]
# (quadro inicial, final exclusivo, recorte x,y,w,h) no tempo novo
COBRIR = json.load(open(L/"cobrir.json", encoding="utf-8")) if (L/"cobrir.json").exists() else []
R0, R1 = 940, 1110; CA, CN = 1286, 70
MK = np.load(AD/"_fix/lama_mask.npy", mmap_mode="r")
B = {k["id"]: k for k in json.load(open(L/"blocos.json", encoding="utf-8"))}
def ler(p, n):
    c = cv2.VideoCapture(str(p)); fr = []
    while len(fr) < n:
        ok, f = c.read()
        if not ok: break
        fr.append(f)
    return fr
mapa = {}
for i in USAR:
    k = B[i]; n = k["b"] - k["a"]; fr = ler(L/f"ls_{i}.mp4", n)
    if len(fr) < n: print("AVISO", i, len(fr), n); fr += [fr[-1]]*(n-len(fr))
    for j in range(n): mapa[k["a"]+j] = (k, fr[j])
cob = {}
for a, b, cr in COBRIR:
    for i in range(a, b): cob[i] = cr
print("blocos:", USAR, "| cobrir:", COBRIR)
c = cv2.VideoCapture(str(AD/"base_sem_legenda_lama.mp4")); N = int(c.get(7))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
out = AD/"base_lipsync.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(out)], stdin=subprocess.PIPE)
for i in range(N):
    ok, f = c.read()
    if i in mapa:
        k, g = mapa[i]
        if g.shape[:2] != (1280, 720) and "crop" not in k: g = cv2.resize(g, (720, 1280))
        if "crop" in k:
            x,y,w,h = k["crop"]; o = f[y:y+h, x:x+w]
            s = cv2.resize(g, (w,h), interpolation=cv2.INTER_AREA)
            d = cv2.GaussianBlur(np.abs(s.astype(np.int16)-o.astype(np.int16)).max(2).astype(np.uint8),(5,5),0)
            m = cv2.dilate((d>10).astype(np.uint8), np.ones((15,15),np.uint8)).astype(np.float32)
            m = cv2.GaussianBlur(m,(21,21),0)[...,None]; m[:4]=0; m[-4:]=0; m[:,:4]=0; m[:,-4:]=0
            f = f.copy(); f[y:y+h, x:x+w] = np.clip(s*m + o*(1-m),0,255).astype(np.uint8)
        else:
            io = i if i < CA else i + CN
            m = cv2.dilate(np.array(MK[io]), np.ones((9,9),np.uint8)).astype(np.float32)
            a = np.maximum(cv2.GaussianBlur(m,(15,15),0), m)[...,None]
            g = g.copy(); g[R0:R1] = np.clip(f[R0:R1]*a + g[R0:R1]*(1-a), 0, 255).astype(np.uint8); f = g
    if i in cob:
        x,y,w,h = cob[i]; f = cv2.resize(f[y:y+h, x:x+w], (720,1280), interpolation=cv2.INTER_LANCZOS4)
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok", out, N)
