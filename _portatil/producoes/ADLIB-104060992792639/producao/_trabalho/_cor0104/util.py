# -*- coding: utf-8 -*-
"""Correcao de cor dos ADs 01-04 (REVISAO-LOTE-C, sem credito HeyGen): funcoes comuns.
Leitura/gravacao = ad13/lipsync3/comum3.py (ffmpeg bt601 + accurate_rnd; inversa exata; etiqueta bt709/tv so no bitstream)."""
import sys, subprocess, numpy as np, cv2
from pathlib import Path
T = Path(__file__).resolve().parent.parent            # producao/_trabalho
UNICOS = T.parents[1] / "UNICOS_HD"
sys.path.insert(0, str(T / "ad13" / "lipsync3"))
from comum3 import quadros, ENC_VF, ENC_TAG          # noqa: E402

def enc(path, fps=30, crf=12):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", str(fps), "-i", "-",
                             *ENC_VF, "-threads", "4", "-c:v", "libx264", "-crf", str(crf), "-preset", "medium", "-pix_fmt", "yuv420p",
                             *ENC_TAG, "-an", str(path)], stdin=subprocess.PIPE)

def ajustar(X, Y, it=4):
    """afim BGR robusta (3x4): Y ~ [X 1] @ A. Devolve A, residuo mediano, fracao de inliers."""
    X = X.reshape(-1, 3).astype(np.float64); Y = Y.reshape(-1, 3).astype(np.float64)
    Xa = np.c_[X, np.ones(len(X))]; ok = np.ones(len(X), bool)
    for _ in range(it):
        A, *_ = np.linalg.lstsq(Xa[ok], Y[ok], rcond=None); r = np.linalg.norm(Xa @ A - Y, axis=1)
        ok = r < max(3.0, 2.5 * np.median(r[ok]))
    return A, float(np.median(r[ok])), float(ok.mean())

def aplicar(A, f):
    return np.clip(f.reshape(-1, 3).astype(np.float32) @ A[:3].astype(np.float32) + A[3].astype(np.float32) + 0.5, 0, 255).reshape(f.shape).astype(np.uint8)

def fit_cv2_para_601(video, n=24):
    """Os PNG do LaMa foram feitos com quadros lidos pelo cv2 (matriz da etiqueta). Ajusta a afim leitura cv2 -> leitura comum3
    do MESMO arquivo (transformacao fixa de matriz), para converter os PNG antes de colar."""
    cap = cv2.VideoCapture(str(video)); N = int(cap.get(7)); idx = set(int(x) for x in np.linspace(5, N - 6, n))
    C = {}; i = 0
    while True:
        ok, f = cap.read()
        if not ok: break
        if i in idx: C[i] = f[::4, ::4].copy()
        i += 1
    Q = {}
    for i, f in enumerate(quadros(video)):
        if i in idx: Q[i] = f[::4, ::4].copy()
    ks = sorted(set(C) & set(Q))
    X = np.vstack([C[k].reshape(-1, 3) for k in ks]); Y = np.vstack([Q[k].reshape(-1, 3) for k in ks])
    A, r, fr = ajustar(X, Y)
    return A, r, fr, (Y.astype(float) - X).mean(0)

def elipse_mask(shape, c, ax):
    m = np.zeros(shape, np.uint8); cv2.ellipse(m, (int(c[0]), int(c[1])), (int(ax[0]), int(ax[1])), 0, 0, 360, 1, -1); return m > 0
