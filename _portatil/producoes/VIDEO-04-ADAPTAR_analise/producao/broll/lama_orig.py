# -*- coding: utf-8 -*-
"""Extrai takes do original (PNG, matriz bt709 full fixa = etiqueta do arquivo) e apaga a legenda queimada (branco+verde, faixa y 670-770) com LaMa.
Rodar com o python do venv _vg."""
import subprocess, sys, numpy as np, cv2
from pathlib import Path
from PIL import Image
from simple_lama_inpainting import SimpleLama
P = Path(__file__).resolve().parent / "orig"
SRC = r"C:\Users\PICHAU\Downloads\VIDEO 04 ADPTAR.mp4"
CL = {"sb": (12.27, 14.07), "ros": (27.70, 29.20), "sen": (29.95, 31.05), "sbluz": (83.90, 86.05), "chave": (105.40, 108.80)}
lama = SimpleLama()
for n, (a, b) in CL.items():
    d = P / n; d.mkdir(parents=True, exist_ok=True)
    if not list(d.glob("f_*.png")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", SRC, "-t", f"{b - a}", "-vf",
                        "scale=in_color_matrix=bt709:in_range=full:flags=accurate_rnd+full_chroma_int+bitexact,format=rgb24", str(d / "f_%04d.png")], check=True)
    (d / "limpo").mkdir(exist_ok=True)
    for p in sorted(d.glob("f_*.png")):
        o = d / "limpo" / p.name
        if o.exists(): continue
        f = np.asarray(Image.open(p).convert("RGB")); Y0, Y1 = 660, 780
        r, g, bb = [f[Y0:Y1, :, k].astype(int) for k in range(3)]
        core = ((np.minimum(np.minimum(r, g), bb) > 215) | ((g > 120) & (g > r + 50) & (g > bb + 50))).astype(np.uint8)
        n_, lab, st, _ = cv2.connectedComponentsWithStats(core)
        for k in range(1, n_):
            if st[k, cv2.CC_STAT_AREA] < 6 or st[k, cv2.CC_STAT_HEIGHT] > 60: core[lab == k] = 0
        # só linhas típicas da legenda (glifos no meio da faixa)
        m = np.zeros_like(core)
        if core.sum():
            ys, xs = np.where(core)
            # legenda = glifos na linha de maior densidade; caixa justa + contorno/sombra
            yc = int(np.median(ys)); sel = np.abs(ys - yc) < 30; ys, xs = ys[sel], xs[sel]
            if len(ys) > 40: M = 22 if n == "ros" else 0; m[max(0, ys.min() - 9 - M): ys.max() + 14 + M, max(0, xs.min() - 12 - M): xs.max() + 13 + M] = 1
        full = np.zeros(f.shape[:2], np.uint8); full[Y0:Y1] = m
        if full.sum() == 0: Image.fromarray(f).save(o); continue
        a0, a1 = 560, 880; crop = f[a0:a1]
        res = np.array(lama(Image.fromarray(crop), Image.fromarray(full[a0:a1] * 255)))[: a1 - a0, :720]
        al = cv2.GaussianBlur(full[a0:a1].astype(np.float32), (9, 9), 0); al = np.maximum(al, full[a0:a1])[..., None]
        out = f.copy(); out[a0:a1] = np.clip(res * al + crop * (1 - al), 0, 255).astype(np.uint8)
        Image.fromarray(out).save(o)
    print(n, len(list((d / "limpo").glob("*.png"))), flush=True)
