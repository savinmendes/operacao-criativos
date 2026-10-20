# -*- coding: utf-8 -*-
"""Gancho do Ranking 03: apaga a mulher em chroma do original (e a legenda PT acima da cabeça) nos quadros 0-2,4 s com LaMa.
A mulher nova (Avatar IV em fundo verde, mulher/C.mp4) é recolocada por cima no montar.py. Quadros em broll/hook/f_*.png
(lidos com bt709/tv); saída broll/hook/limpo/. Máscara da pessoa: rembg u2net_human_seg no recorte 250-720 x 600-1280."""
import numpy as np, cv2
from pathlib import Path
from PIL import Image
from rembg import remove, new_session
from simple_lama_inpainting import SimpleLama
P = Path(__file__).resolve().parent; D = P / "broll" / "hook"; (D / "limpo").mkdir(exist_ok=True)
NQ = 74   # 0 .. 2,45 s
ses = new_session("u2net_human_seg"); lama = SimpleLama()
def legenda(f):
    Y0, Y1 = 670, 800
    r, g, b = [f[Y0:Y1, :, k].astype(int) for k in range(3)]
    core = ((np.minimum(np.minimum(r, g), b) > 205) | ((g > 120) & (g > r + 50) & (g > b + 50))).astype(np.uint8)
    dark = cv2.dilate((np.maximum(np.maximum(r, g), b) < 70).astype(np.uint8), np.ones((9, 9), np.uint8))
    core &= dark
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 6 or st[k, cv2.CC_STAT_HEIGHT] > 48: core[lab == k] = 0
    m = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21)))
    full = np.zeros(f.shape[:2], np.uint8); full[Y0:Y1] = m; return full
for i in range(1, NQ + 1):
    p = D / f"f_{i:04d}.png"; o = D / "limpo" / p.name
    if o.exists(): continue
    f = np.asarray(Image.open(p).convert("RGB"))
    c = Image.fromarray(f[600:1280, 250:720])
    pm = (np.asarray(remove(c, session=ses, only_mask=True)) > 100).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(pm)
    keep = np.zeros_like(pm)
    for k in range(1, n):   # só componentes que encostam na base (a mulher do chroma vem de baixo)
        if st[k, cv2.CC_STAT_TOP] + st[k, cv2.CC_STAT_HEIGHT] >= 670 and st[k, cv2.CC_STAT_AREA] > 3000: keep[lab == k] = 1
    m = np.zeros(f.shape[:2], np.uint8); m[600:1280, 250:720] = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25)))
    m |= legenda(f)
    m[972:] = 0                       # abaixo de 972 o rodapé novo cobre tudo
    if m.sum() == 0: Image.fromarray(f).save(o); continue
    a0, a1 = 560, 1000
    res = np.array(lama(Image.fromarray(f[a0:a1]), Image.fromarray(m[a0:a1] * 255)))[: a1 - a0, :720].astype(np.float32)
    al = np.maximum(cv2.GaussianBlur(m[a0:a1].astype(np.float32), (9, 9), 0), m[a0:a1])[..., None]
    out = f.copy(); out[a0:a1] = np.clip(res * al + f[a0:a1] * (1 - al), 0, 255).astype(np.uint8)
    Image.fromarray(out).save(o)
    if i % 10 == 0: print(i, flush=True)
print("ok")
