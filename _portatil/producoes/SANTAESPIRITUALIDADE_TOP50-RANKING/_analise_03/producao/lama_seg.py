# -*- coding: utf-8 -*-
"""Apaga a legenda PT queimada (branca + palavra verde, faixa y 680-800) com LaMa, trecho a trecho.
Rodar com o python do venv _vg:  python lama_seg.py nome1 nome2 ...   (sem nome = todos)
Le cada trecho do original com a matriz bt709/tv da etiqueta -> PNG RGB; grava broll/<nome>/limpo/f_0001.png ..."""
import subprocess, sys, json, numpy as np, cv2
from pathlib import Path
from PIL import Image
from simple_lama_inpainting import SimpleLama
P = Path(__file__).resolve().parent
ORIG = str(P.parents[1] / "03_288k_DQxVwd5kbGY.mp4")
SEG = {  # nome: (src, t0, t1)  Ranking 02
 "jesus":   (ORIG, 66.85, 68.40),
 "vela":    (ORIG, 68.70, 69.95),
 "cruz":    (ORIG, 70.45, 72.15),
 "igreja":  (ORIG, 72.50, 74.05),
 "leitura": (ORIG, 74.45, 76.00),
 "bracos":  (ORIG, 76.70, 79.05),
 "manuscrito": (ORIG, 79.65, 81.65),
 "procissao": (ORIG, 94.00, 95.80),
 "maos":    (ORIG, 119.60, 123.25),
 "nuvens":  (ORIG, 142.40, 143.80),
}
if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
    SEG = {k: tuple(v) for k, v in json.load(open(sys.argv[1], encoding="utf-8")).items()}; nomes = list(SEG)
else:
    nomes = sys.argv[1:] or list(SEG)
Y0, Y1 = 680, 800
lama = SimpleLama()
def mascara(f):
    r, g, b = [f[Y0:Y1, :, k].astype(int) for k in range(3)]
    core = ((np.minimum(np.minimum(r, g), b) > 205) | ((g > 120) & (g > r + 50) & (g > b + 50))).astype(np.uint8)
    dark = cv2.dilate((np.maximum(np.maximum(r, g), b) < 70).astype(np.uint8), np.ones((9, 9), np.uint8))
    core &= dark   # glifo da legenda sempre tem contorno preto em volta
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 6 or st[k, cv2.CC_STAT_HEIGHT] > 48: core[lab == k] = 0
    full = np.zeros(f.shape[:2], np.uint8)
    if core.sum() < 60: return full
    ys, xs = np.where(core); yc = int(np.median(ys)); sel = np.abs(ys - yc) < 34
    if sel.sum() < 60: return full
    m = np.zeros_like(core); m[ys[sel], xs[sel]] = 1
    m = cv2.dilate(m, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
    dn = np.zeros_like(m); dn[6:] = m[:-6]; m = cv2.dilate(m | dn, np.ones((5, 5), np.uint8))
    full[Y0:Y1] = m
    return full
for n in nomes:
    src, a, b = SEG[n]; d = P / "broll" / n; (d / "limpo").mkdir(parents=True, exist_ok=True)
    if not list(d.glob("f_*.png")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", src, "-t", f"{b - a}", "-vf",
                        "scale=in_color_matrix=bt709:in_range=limited:flags=accurate_rnd+full_chroma_int+bitexact,format=rgb24",
                        "-fps_mode", "passthrough", str(d / "f_%04d.png")], check=True)
    ema = None
    for p in sorted(d.glob("f_*.png")):
        o = d / "limpo" / p.name
        if o.exists(): continue
        f = np.asarray(Image.open(p).convert("RGB")); m = mascara(f)
        if m.sum() == 0: Image.fromarray(f).save(o); ema = None; continue
        a0, a1 = 600, 900; crop = f[a0:a1]
        res = np.array(lama(Image.fromarray(crop), Image.fromarray(m[a0:a1] * 255)))[: a1 - a0, :720].astype(np.float32)
        al = np.maximum(cv2.GaussianBlur(m[a0:a1].astype(np.float32), (11, 11), 0), m[a0:a1])[..., None]
        out = f.copy(); out[a0:a1] = np.clip(res * al + crop * (1 - al), 0, 255).astype(np.uint8)
        Image.fromarray(out).save(o)
    print(n, len(list((d / "limpo").glob("*.png"))), flush=True)
