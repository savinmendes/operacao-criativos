# -*- coding: utf-8 -*-
"""Cola só boca+queixo do HeyGen (ls/out/<job>.mp4) sobre o quadro-fonte (elipse suave, cor pelo anel de pele, nitidez casada).
Base: quadros q0..q1 de base_visual_es (com crop -> volta à posição no quadro cheio) ou, no 'avc', o próprio v_<job>.mp4 enviado.
Saída: ls/patch/<job>.pkl {k_local: (x, y, RGBA)} + ls/patch/<job>_prev.mp4 (quadro cheio com a boca nova)."""
import sys, pickle, numpy as np, cv2
from scipy.ndimage import uniform_filter1d
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import cor, checar_lipsync as cl
from plano import *
nome = sys.argv[1]; j = JOBS[nome]; kind, q0, q1 = j["src"]
if kind == "base":
    Fb = cor.ler(BASE, q0, q1).copy(); X, Y, w, h = j["crop"]; fps = 30
else:
    Fb = cor.ler(T / "ls" / "in" / f"v_{nome}.mp4").copy(); X, Y, w, h = 0, 0, 720, 1280; fps = 25
Ho = cor.ler(T / "ls" / "out" / f"{nome}.mp4")
n = min(len(Fb), len(Ho)); print(nome, "base", len(Fb), "heygen", len(Ho))
B = np.stack([cv2.resize(f, (w, h), interpolation=cv2.INTER_AREA if w < 720 else cv2.INTER_CUBIC) for f in Ho[:n]])
A = Fb[:n, Y:Y + h, X:X + w]
det = cl.Rastreador(); geo = []
for k in range(n):
    p = det.pontos(cv2.cvtColor(B[k], cv2.COLOR_RGB2BGR))
    if p is None: geo.append(None); continue
    fw = np.linalg.norm(p[234] - p[454]); mouth = p[[13, 14, 61, 291, 0, 17]].mean(0); chin = p[152]; nose = p[2]
    cx = mouth[0] * 0.85 + chin[0] * 0.15; cy = nose[1] * 0.35 + chin[1] * 0.65
    geo.append((cx, cy, 0.36 * fw, (chin[1] - nose[1]) * 0.62, fw))
idx = [i for i, g in enumerate(geo) if g is not None]
print("rosto em", len(idx), "de", n)
G = np.array([geo[i] for i in idx]); G = np.array([np.interp(np.arange(n), idx, G[:, c]) for c in range(5)]).T
G = uniform_filter1d(G, size=5, axis=0, mode="nearest")
sem = np.ones(n); sem[idx] = 0; sem = uniform_filter1d(sem, 3) > 0.01
def mask(g):
    cx, cy, ax, ay, fw = g; m = np.zeros((h, w), np.float32)
    cv2.ellipse(m, (int(cx), int(cy)), (max(1, int(ax)), max(1, int(ay))), 0, 0, 360, 1.0, -1)
    return cv2.GaussianBlur(m, (0, 0), max(3, 0.06 * fw))
ds, la = [], []
for k in range(0, n, max(1, n // 15)):
    m = mask(G[k]); dentro = m > 0.02; cx, cy, ax, ay, fw = G[k]
    big = np.zeros((h, w), np.uint8); cv2.ellipse(big, (int(cx), int(cy)), (int(ax * 1.7), int(ay * 1.55)), 0, 0, 360, 1, -1)
    anel = (big > 0) & ~dentro
    if anel.sum() < 50: continue
    ds.append(np.median(A[k][anel].astype(np.float32) - B[k][anel].astype(np.float32), 0))
    x0, y0, x1, y1 = [int(v) for v in (cx - ax * .7, cy - ay * .7, cx + ax * .7, cy + ay * .7)]
    la.append(cv2.Laplacian(cv2.cvtColor(A[k][y0:y1, x0:x1], cv2.COLOR_RGB2GRAY), cv2.CV_64F).var())
d = np.nanmedian(np.array(ds), 0).astype(np.float32); la = np.nanmedian(la)
if not np.all(np.isfinite(d)): d = np.zeros(3, np.float32)
def sharp(f, amt, sig=1.2): return cv2.addWeighted(f, 1 + amt, cv2.GaussianBlur(f, (0, 0), sig), -amt, 0)
k0 = n // 2; cx, cy, ax, ay, fw = G[k0]; x0, y0, x1, y1 = [int(v) for v in (cx - ax * .7, cy - ay * .7, cx + ax * .7, cy + ay * .7)]
amt = 0.0
for t in np.arange(0, 3.01, 0.1):
    sq = np.clip(sharp(B[k0].astype(np.float32), t)[y0:y1, x0:x1], 0, 255).astype(np.uint8); amt = t
    if cv2.Laplacian(cv2.cvtColor(sq, cv2.COLOR_RGB2GRAY), cv2.CV_64F).var() >= la * 0.9: break
print(f"cor anel {d.round(1)} | unsharp {amt:.1f}")
(T / "ls" / "patch").mkdir(exist_ok=True)
camadas = {}
for k in range(n):
    if sem[k]: continue
    m = mask(G[k]); ys, xs = np.where(m > 0.004)
    if len(xs) == 0: continue
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    bb = np.clip(sharp(B[k].astype(np.float32) + d, amt)[y0:y1, x0:x1] + 0.5, 0, 255).astype(np.uint8)
    a = (m[y0:y1, x0:x1] * 255 + 0.5).astype(np.uint8)
    camadas[k] = (X + x0, Y + y0, np.dstack([bb, a]))
pickle.dump({"fps": fps, "n": len(Fb), "camadas": camadas}, open(T / "ls" / "patch" / f"{nome}.pkl", "wb"))
e = cor.escritor(T / "ls" / "patch" / f"{nome}_prev.mp4", fps=fps, crf=12)
for k in range(len(Fb)):
    o = Fb[k].copy()
    if k in camadas:
        x, y, L = camadas[k]; hh, ww = L.shape[:2]; al = L[..., 3:4].astype(np.float32) / 255
        o[y:y + hh, x:x + ww] = np.clip(L[..., :3] * al + o[y:y + hh, x:x + ww] * (1 - al) + 0.5, 0, 255).astype(np.uint8)
    e.stdin.write(o.tobytes())
e.stdin.close(); e.wait(); print("ok", nome, len(camadas), "quadros com boca")
