# -*- coding: utf-8 -*-
"""B-rolls originais do Ranking 04: extrai os quadros (matriz bt709/tv da etiqueta -> RGB) e mede a caixa da legenda PT
queimada (texto branco/amarelo/vermelho com contorno preto, faixa y 760-1080). Grava broll/<nome>/f_*.png e broll/caixas.json.
A legenda PT é coberta por caixa opaca no mesmo lugar (sem LaMa)."""
import subprocess, json, numpy as np, cv2
from pathlib import Path
from PIL import Image
P = Path(__file__).resolve().parent; ORIG = str(P.parents[1] / "04_252k_DNohD8kRh4a.mp4")
SEG = {  # nome: (t0, t1) sem os quadros de dissolve
 "rosa_olha": (13.20, 13.95), "rosa_reza": (14.05, 17.30), "vela_livro": (23.45, 27.10),
 "cruz_mar": (43.75, 44.40), "cruz_sol": (44.60, 45.25), "maos": (45.55, 46.20), "terco": (49.25, 49.95),
 "moca_branca": (48.25, 48.95), "moca_sorri": (50.65, 51.25), "mesa": (53.45, 55.35), "familia": (59.65, 61.50),
 "piggy": (74.00, 75.95), "selfie": (101.80, 104.55), "pedra": (52.55, 53.30),
}
Y0, Y1 = 740, 1100
def mascara(f):
    r, g, b = [f[Y0:Y1, :, k].astype(int) for k in range(3)]
    claro = (np.minimum(np.minimum(r, g), b) > 200) | ((r > 190) & (g > 170) & (b < 110)) | ((r > 170) & (g < 60) & (b < 60))
    dark = cv2.dilate((np.maximum(np.maximum(r, g), b) < 60).astype(np.uint8), np.ones((7, 7), np.uint8))
    m = (claro.astype(np.uint8) & dark)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    out = np.zeros_like(m)
    for k in range(1, n):
        if 6 <= st[k, cv2.CC_STAT_AREA] and st[k, cv2.CC_STAT_HEIGHT] <= 44: out[lab == k] = 1
    return out
cx = {}
for n, (a, b) in SEG.items():
    d = P / "broll" / n; d.mkdir(parents=True, exist_ok=True)
    if not list(d.glob("f_*.png")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a}", "-i", ORIG, "-t", f"{b - a}", "-vf",
                        "scale=in_color_matrix=bt709:in_range=limited:flags=accurate_rnd+full_chroma_int+bitexact,format=rgb24",
                        "-fps_mode", "passthrough", str(d / "f_%04d.png")], check=True)
    acc = np.zeros((Y1 - Y0, 720), np.float32); fs = sorted(d.glob("f_*.png"))
    for p in fs: acc += mascara(np.asarray(Image.open(p).convert("RGB")))
    m = (acc >= max(2, 0.08 * len(fs))).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 41), np.uint8))
    n2, lab, st, _ = cv2.connectedComponentsWithStats(m)
    ks = [k for k in range(1, n2) if st[k, cv2.CC_STAT_AREA] > 150]
    if not ks: cx[n] = None; print(n, len(fs), "sem legenda"); continue
    x0 = min(st[k, 0] for k in ks); y0 = min(st[k, 1] for k in ks); x1 = max(st[k, 0] + st[k, 2] for k in ks); y1 = max(st[k, 1] + st[k, 3] for k in ks)
    cx[n] = [int(max(0, x0 - 16)), int(Y0 + y0 - 12), int(min(720, x1 + 16)), int(Y0 + y1 + 12)]
    print(n, len(fs), cx[n])
cx["selfie"] = [110, 925, 610, 1012]   # a medição pegou a camisa branca; legenda PT do selfie é 1 linha em ~930-1005
json.dump(cx, open(P / "broll" / "caixas.json", "w"), indent=1)
