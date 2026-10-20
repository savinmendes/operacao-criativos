# -*- coding: utf-8 -*-
"""Cola só boca + queixo do resultado HeyGen sobre os quadros originais (elipse suave, cor pelo anel em volta).
RA: sobre broll/news/limpo (quadros 1-60, recorte 288x512 em 330,640 escalado 2,5x).
DA/DB: sobre o original 12.85-18.80 / 18.80-24.30 -> broll/donoA|donoB/f_*.png (depois a LaMa tira a legenda)."""
import subprocess, numpy as np, cv2
from pathlib import Path
from PIL import Image
P = Path(__file__).resolve().parent; R = P.parent; ORIG = str(R.parents[1] / "01_628k_DQ7ptOAkVeh.mp4")
def ler(src, m, t0=None, dur=None, w=720, h=1280):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{t0}"] if t0 is not None else []) + ["-i", src] + (["-t", f"{dur}"] if dur else []) + \
          ["-vf", f"scale={w}:{h}:in_color_matrix={m}:in_range=limited:flags=accurate_rnd+full_chroma_int,format=rgb24", "-fps_mode", "passthrough", "-f", "rawvideo", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
def mascara(ls, base, ymax=None):
    d = np.abs(ls - base).mean(3).mean(0)
    if ymax: d[ymax:] = 0
    d = cv2.GaussianBlur(d, (0, 0), 6)
    thr = np.percentile(d, 99.3) * 0.45; m = (d > thr).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m); k = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]); ys, xs = np.where(lab == k)
    cx, cy = xs.mean(), ys.mean(); ax, ay = (xs.max() - xs.min()) / 2 + 14, (ys.max() - ys.min()) / 2 + 14
    E = np.zeros(d.shape, np.float32); cv2.ellipse(E, (int(cx), int(cy)), (int(ax), int(ay)), 0, 0, 360, 1, -1)
    E = cv2.GaussianBlur(E, (0, 0), 7); print("  elipse", int(cx), int(cy), int(ax), int(ay))
    anel = cv2.dilate((E > 0.02).astype(np.uint8), np.ones((25, 25), np.uint8)) - (E > 0.02)
    return E, anel.astype(bool)
def colar(ls, base, E, anel):
    out = []
    for a, b in zip(ls, base):
        corr = b[anel].mean(0) - a[anel].mean(0)          # ajuste de cor pelo anel
        out.append(np.clip((a + corr) * E[..., None] + b * (1 - E[..., None]), 0, 255).astype(np.uint8))
    return out
# escolher a matriz da saída do HeyGen pela menor diferença fora da boca
def melhor(lsp, base):
    best = None
    for m in ("bt709", "bt601"):
        ls = ler(str(lsp), m)[:len(base)]; e = np.abs(ls[:, :300] - base[:len(ls), :300]).mean()
        if best is None or e < best[0]: best = (e, m, ls)
    print("  matriz", best[1], round(best[0], 2)); return best[2]
# ---- RA ----
print("RA")
fs = sorted((R / "broll/news/limpo").glob("f_*.png"))[:60]
news = np.stack([np.asarray(Image.open(p).convert("RGB")).astype(np.float32) for p in fs])
crop = np.stack([cv2.resize(f[640:1152, 330:618], (720, 1280), interpolation=cv2.INTER_LANCZOS4) for f in news])
pin = ler(str(P / "in/pt_RA.mp4"), "bt709")
ls = melhor(P / "out/ls_RA.mp4", pin); n = min(len(ls), len(crop), len(pin))
E, anel = mascara(ls[:n], pin[:n])
o = colar(ls[:n], crop[:n], E, anel)
D = R / "broll/news_ls"; D.mkdir(exist_ok=True)
Es = cv2.resize(E, (288, 512), interpolation=cv2.INTER_AREA)[..., None]
for i, p in enumerate(fs):
    f = news[i].copy()
    if i < n:
        sm = cv2.resize(o[i].astype(np.float32), (288, 512), interpolation=cv2.INTER_AREA)
        f[640:1152, 330:618] = sm * Es + f[640:1152, 330:618] * (1 - Es)
    Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).save(D / p.name)
# ---- DA / DB ----
for nome, t0, dur in (("A", 12.85, 5.95), ("B", 18.80, 5.50)):
    print("D" + nome)
    base = ler(ORIG, "bt709", t0, dur); ls = melhor(P / f"out/ls_D{nome}.mp4", base); n = min(len(ls), len(base))
    E, anel = mascara(ls[:n], base[:n], 652); o = colar(ls[:n], base[:n], E, anel)
    D = R / f"broll/dono{nome}"; D.mkdir(exist_ok=True)
    for i in range(len(base)):
        Image.fromarray(o[i] if i < n else base[i].astype(np.uint8)).save(D / f"f_{i + 1:04d}.png")
    print("  quadros", len(base), n)
