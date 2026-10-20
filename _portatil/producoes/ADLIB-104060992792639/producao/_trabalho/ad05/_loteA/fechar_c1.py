# -*- coding: utf-8 -*-
"""Lote A (08/10), sem credito: fecha a boca da Clara nas pausas da voz ES dentro do c1 (q0-74 a 24 fps, 0-3,13 s),
com a mesma logica do fechar.py (AD 01) / processar_v3.py (AD 05): em cada pausa ES >= 5 q, cola a boca+queixo do quadro
mais fechado do proprio c1, alinhado por pontos estaveis do rosto, com rampa de 3 quadros.
Le _antes_loteA/base_lipsync.mp4 e reescreve base_lipsync.mp4 (so os quadros do c1 mudam)."""
import sys, os, subprocess
from pathlib import Path
import numpy as np, cv2
os.environ.setdefault("GLOG_minloglevel", "2")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import checar_lipsync as cl
AD = Path(__file__).resolve().parent.parent; FPS = 24
A, B = 0, 75                      # c1: q0-74 (q75 = corte de camera)
MINQ, RAMPA = 5, 3
ESTAVEIS = [33, 133, 362, 263, 168, 6, 197, 195, 5, 4, 1, 234, 454, 127, 356]
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
cap = cv2.VideoCapture(str(AD / "_antes_loteA/base_lipsync.mp4")); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
R = cl.Rastreador(alvo=(380, 0, 300, 320))
P = [R.pontos(fr[q]) for q in range(A, B)]
ab = np.array([cl._abertura(p) if p is not None else np.nan for p in P])
n = B - A
es = cl.envelope(cl.ler_audio(AD / "narr_clara.wav"), 16000, float(FPS), len(fr))[A:B]
fal = es > np.nanmax(es) - 30
runs, k = [], 0
while k < n:
    if not fal[k]:
        j = k
        while j < n and not fal[j]: j += 1
        if j - k >= MINQ and k > 0: runs.append((k, j))   # ignora o silencio antes da 1a palavra (q0)
        k = j
    else: k += 1
def mascara(p, shape):
    lab = (p[13] + p[14]) / 2; queixo = p[152]; nariz = p[2]
    c = (lab + queixo) / 2 + np.array([0, 0.05 * np.linalg.norm(queixo - nariz)])
    ax = int(0.62 * np.linalg.norm(p[61] - p[291]) + 10); ay = int(0.62 * np.linalg.norm(queixo - nariz) + 6)
    m = np.zeros(shape[:2], np.float32)
    cv2.ellipse(m, (int(c[0]), int(c[1])), (ax, ay), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, ax / 6))
orig = [f.copy() for f in fr]
for a, b in runs:
    viz = [q for q in range(n) if np.isfinite(ab[q]) and fal[q]]   # referencia: quadro mais fechado durante a fala ES do c1
    r = min(viz, key=lambda q: ab[q]); pr = P[r]
    for q in range(a, b):
        w = min(1.0, (q - a + 1) / RAMPA, (b - q) / RAMPA) if b < n else min(1.0, (q - a + 1) / RAMPA)
        pk = P[q]
        if pk is None: continue
        M, _ = cv2.estimateAffinePartial2D(pr[ESTAVEIS].astype(np.float32), pk[ESTAVEIS].astype(np.float32))
        if M is None: continue
        g = cv2.warpAffine(orig[A + r], M, (720, 1280), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        ms = mascara(pk, fr[A + q].shape)[..., None] * w
        fr[A + q] = np.clip(g * ms + fr[A + q] * (1 - ms), 0, 255).astype(np.uint8)
    print(f"pausa q{a}-{b} ({a/FPS:.2f}-{b/FPS:.2f} s) ref q{r} ab={ab[r]:.3f} (abertura media antes {np.nanmean(ab[a:b]):.3f})")
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-","-threads","4",
    "-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
for f in fr: ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); print("ok quadros", len(fr))

