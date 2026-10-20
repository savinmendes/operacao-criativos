# -*- coding: utf-8 -*-
"""v3 AD 13: recorte 9:16 que segue o rosto da MULHER (a esquerda; o Jesus fica a direita, x > 380) por quadro,
suavizado dentro de cada tomada (zera nos cortes de cortes.json), empurrado para a esquerda do rosto do Jesus.
Saida: caixas_<seg>.npy [x0,y0,w,h,mx,my,fw,fh] (mesmo formato do ad17) e rosto_<seg>.txt (caixa p/ checar --rosto)."""
import json, numpy as np
from pathlib import Path
AQ = Path(__file__).parent
CFG = json.loads((AQ / "segs.json").read_text()); R = json.loads((AQ / "rostos.json").read_text())
CORTES = {q for q, d in json.loads((AQ / "cortes.json").read_text())}
W, H, FATOR, MINW = 720, 1280, 2.3, 300
def suav(x, k=9):
    if len(x) < 3: return x
    k = min(k, len(x) // 2 * 2 - 1); pad = np.pad(x, ((k // 2, k // 2), (0, 0)), mode="edge")
    return np.array([pad[i:i + k].mean(0) for i in range(len(x))])
for s in CFG["segs"]:
    a, b, nm = s["a"], s["b"], s["nome"]; n = b - a
    M = np.full((n, 6), np.nan); J = np.full(n, np.nan)
    for k in range(n):
        fs = R.get(str(a + k), [])
        mul = [f for f in fs if (f[0] + f[2]) / 2 < 380]; jes = [f for f in fs if (f[0] + f[2]) / 2 >= 380]
        if mul: M[k] = max(mul, key=lambda f: f[2] - f[0])
        if jes: J[k] = min(f[0] for f in jes)
    # tomadas
    cuts = [0] + [q - a for q in sorted(CORTES) if a < q < b] + [n]
    C = np.zeros((n, 8))
    for t0, t1 in zip(cuts[:-1], cuts[1:]):
        F = M[t0:t1].copy()
        ww = F[:, 2] - F[:, 0]
        if np.isfinite(ww).any():   # descarta deteccoes duplas/largas (fora do padrao da tomada)
            med = np.nanmedian(ww); F[np.isfinite(ww) & ((ww > 1.35 * med) | (ww < 0.7 * med))] = np.nan
        ok = np.isfinite(F[:, 0])
        if not ok.any():   # tomada sem deteccao: usa a vizinha mais proxima
            viz = np.where(np.isfinite(M[:, 0]))[0]; F[:] = M[viz[np.argmin(np.abs(viz - t0))]]
        else:
            for j in range(6): F[:, j] = np.interp(np.arange(len(F)), np.where(ok)[0], F[ok, j])
        F = suav(F)
        jx = np.nanmin(J[t0:t1]) if np.isfinite(J[t0:t1]).any() else None
        for i, f in enumerate(F):
            fx0, fy0, fx1, fy1, mx, my = f; fw, fh = fx1 - fx0, fy1 - fy0
            cw = min(W, max(MINW, FATOR * fw)); ch = cw * 16 / 9
            if ch > H: ch = H; cw = ch * 9 / 16
            cx = (fx0 + fx1) / 2; cy = (fy0 + fy1) / 2 + 0.12 * ch
            x0 = cx - cw / 2
            if jx is not None:
                x0 = max(0, min(x0, fx0 - 0.25 * fw)); cw = max(1.4 * fw, min(cw, jx - 6 - x0)); ch = cw * 16 / 9
            C[t0 + i] = [np.clip(x0, 0, W - cw), np.clip(cy - ch / 2, 0, H - ch), cw, ch, mx, my, fw, fh]
        C[t0:t1, :4] = suav(C[t0:t1, :4], 15)
        if jx is not None: print(f"   {nm} tomada {a+t0}-{a+t1}: jesus x0 {jx:.0f}, recorte x1 max {(C[t0:t1,0]+C[t0:t1,2]).max():.0f}")
    np.save(AQ / f"caixas_{nm}.npy", C)
    V = M[np.isfinite(M[:, 0])]
    x0, y0 = np.percentile(V[:, 0], 5), np.percentile(V[:, 1], 5); x1, y1 = np.percentile(V[:, 2], 95), np.percentile(V[:, 3], 95)
    ro = f"{int(x0-20)},{int(y0-20)},{int(x1-x0+40)},{int(y1-y0+40)}"; (AQ / f"rosto_{nm}.txt").write_text(ro)
    print(nm, n, "q; tomadas", len(cuts) - 1, "; sem rosto", int((~np.isfinite(M[:, 0])).sum()), "; rec w", C[:, 2].min().round(), "-", C[:, 2].max().round(),
          "x1 max", (C[:, 0] + C[:, 2]).max().round(), "; jesus x0 min", np.nanmin(J) if np.isfinite(J).any() else "-", "; rosto", ro)
