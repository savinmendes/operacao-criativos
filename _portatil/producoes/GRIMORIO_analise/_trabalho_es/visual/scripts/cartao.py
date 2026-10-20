# -*- coding: utf-8 -*-
"""Cartão das 12 palavras (quadros 1452–1795 estáticos + fusão 1796–1810): reconstrói o cartão a partir da mediana limpa
com as traduções ES e reaplica a barra de destaque (cinza translúcido, alfa ~0,58) estimada do quadro original."""
import numpy as np, cv2
from pathlib import Path
T = Path(__file__).resolve().parent.parent / "_tmp"
MED = cv2.imread(str(T / "card_med.png")).astype(np.float32)
ES = cv2.imread(str(T / "card_es.png")).astype(np.float32)
G = np.array([100.0, 105.0, 107.5], np.float32)  # BGR do cinza da barra (ajuste linear k~0,42)
ALFA = 0.58
Q0, Q1, QF = 1452, 1795, 1810
Y0, Y1 = 108, 1178

def barra(orig):
    """mapa alfa (1280x720) da barra de destaque no quadro original (BGR float)."""
    D = np.abs(cv2.GaussianBlur(orig, (0, 0), 1.2) - cv2.GaussianBlur(MED, (0, 0), 1.2)).mean(2)
    A = np.zeros(D.shape, np.float32)
    r = np.percentile(D[380:920, 230:480], 60, axis=1)
    ys = np.where(r > 15)[0]
    if len(ys) < 8: return A
    grupos = np.split(ys, np.where(np.diff(ys) > 2)[0] + 1); ys = max(grupos, key=len)
    if len(ys) < 8: return A
    a, b = ys.min() + 380, ys.max() + 380
    c = np.median(D[a:b + 1, :], axis=0); c = np.convolve(c, np.ones(25) / 25, "same")
    ref = np.percentile(c[230:480], 80)
    if ref < 10: return A
    xs = np.where(c > 0.5 * ref)[0]
    xs = xs[(xs > 100) & (xs < 650)]
    if len(xs) == 0: return A
    x0, x1 = xs.min(), xs.max()
    x = np.arange(720, dtype=np.float32)
    prof = np.clip(np.minimum((x - (x0 - 12)) / 24, ((x1 + 12) - x) / 24), 0, 1)
    A[a:b + 1] = ALFA * prof[None, :]
    return A

def modelo(base, A):
    return base * (1 - A[..., None]) + A[..., None] * G

def aplicar(i, f_base, f_orig, ultimo=None):
    """f_base: quadro da base (BGR uint8); f_orig: quadro original (BGR uint8). Retorna (quadro, estado)."""
    if Q0 <= i <= Q1:
        A = barra(f_orig.astype(np.float32))
        out = f_base.astype(np.float32).copy()
        out[Y0:Y1] = modelo(ES, A)[Y0:Y1]
        return np.clip(out, 0, 255).astype(np.uint8), A
    if Q1 < i <= QF and ultimo is not None:
        A = ultimo
        delta = modelo(ES, A) - modelo(MED, A)
        o = f_orig.astype(np.float32); c = modelo(MED, A)
        # t pela fração do cartão que ainda aparece (regressão o = (1-t)c + t*x, usando a região do texto)
        cs = c[420:880, 200:560]; os_ = o[420:880, 200:560]
        t = 1 - float(np.clip(np.corrcoef(cs.ravel(), os_.ravel())[0, 1], 0, 1)) if i > Q1 + 1 else 0.0
        w = max(0.0, 1 - (i - Q1) / (QF - Q1 + 1))
        out = f_base.astype(np.float32) + w * delta
        return np.clip(out, 0, 255).astype(np.uint8), A
    return f_base, ultimo
