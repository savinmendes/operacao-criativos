# caixas de recorte 9:16 por quadro (segue o rosto principal, suavizado dentro de cada tomada)
import json, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; PR = AQ.parent
R = json.load(open(PR / "rostos.json")); CH = json.load(open(PR / "chunks2.json"))
dif = {q: d for q, t, d in json.load(open(PR / "cortes.json"))}
def main(fs): return max(fs, key=lambda f: f[2]-f[0]) if fs else None
for c in CH:
    a, b = c["a"], c["b"]; n = b - a
    F = [main(R[q]) for q in range(a, b)]
    fw = np.median([f[2]-f[0] for f in F if f]); fac = 1.8
    w = min(1080.0, fac * fw); h = w * 16 / 9
    if h > 1920: h = 1920.0; w = h * 9 / 16
    cx = np.array([f[4] if f else np.nan for f in F]); cy = np.array([f[5] if f else np.nan for f in F])
    # tomadas internas (corte = dif > 25 ou salto de boca > 40)
    seg = np.zeros(n, int); s = 0
    for k in range(1, n):
        if dif.get(a+k, 0) > 25 or (not np.isnan(cx[k]) and not np.isnan(cx[k-1]) and np.hypot(cx[k]-cx[k-1], cy[k]-cy[k-1]) > 40): s += 1
        seg[k] = s
    X = np.zeros(n); Y = np.zeros(n)
    for s in range(seg.max()+1):
        idx = np.where(seg == s)[0]; xs = cx[idx]; ys = cy[idx]
        ok = ~np.isnan(xs)
        if not ok.any():  # sem rosto: usa vizinho
            xs[:] = np.nanmedian(cx); ys[:] = np.nanmedian(cy)
        else:
            xs = np.interp(np.arange(len(idx)), np.where(ok)[0], xs[ok]); ys = np.interp(np.arange(len(idx)), np.where(ok)[0], ys[ok])
        k = 7; pad = lambda v: np.convolve(np.pad(v, k, mode="edge"), np.ones(2*k+1)/(2*k+1), "valid")
        X[idx] = pad(xs); Y[idx] = pad(ys)
    x0 = np.clip(X - w/2, 0, 1080 - w); y0 = np.clip(Y - 0.58*h, 0, 1920 - h)
    C = np.stack([x0, y0, np.full(n, w), np.full(n, h)], 1)
    np.save(AQ / f"caixas_{c['nome']}.npy", C)
    print(c["nome"], n, "w,h", round(w), round(h), "tomadas", seg.max()+1)
