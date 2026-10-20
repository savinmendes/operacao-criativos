# -*- coding: utf-8 -*-
"""Tira a legenda amarela PT (glifo amarelo + contorno escuro, mascara JUSTA dilatada ~9 px) com LaMa na GPU
e opcionalmente uma seta vermelha. Gera base_sem_legenda.mp4 (sem audio, bt709/tv) + mascara.npy.
Uso: _vg python lama_base.py config.json
config: {"video": "...mp4", "saida": "base_sem_legenda.mp4", "faixa": [y0, y1], "ctx": [c0, c1],
         "seta": {"caixa": [x0,y0,x1,y1], "de": q0} (opcional), "ate": N (opcional), "cortes_ema": true}"""
import sys, json, time, warnings, subprocess; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
Y0, Y1 = cfg["faixa"]; C0, C1 = cfg["ctx"]; seta = cfg.get("seta"); SOMBRA = cfg.get("sombra", 7)
cap = cv2.VideoCapture(cfg["video"]); N = cfg.get("ate") or int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",f"{fps}","-i","-","-an",
    "-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,cfg["saida"]],stdin=subprocess.PIPE)
def mascara_legenda(f):
    roi = f[Y0:Y1]; hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[...,0], hsv[...,1], hsv[...,2]
    core = ((h >= 15) & (h <= 42) & (s >= 80) & (v >= 140)).astype(np.uint8) & cv2.dilate((v < 90).astype(np.uint8), np.ones((7,7),np.uint8))
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, np.ones((3,3),np.uint8))
    # componentes pequenas demais = ruido (bokeh)
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    for k in range(1, n):
        if st[k, cv2.CC_STAT_AREA] < 25: core[lab == k] = 0
    # glifo + contorno/sombra escura (a sombra desce alguns px): elipse 17 + copia deslocada p/ baixo, depois +9 px
    d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    dn = np.zeros_like(d); dn[SOMBRA:] = d[:-SOMBRA]
    m = cv2.dilate(d | dn, np.ones((9, 9), np.uint8))
    full = np.zeros(f.shape[:2], np.uint8); full[Y0:Y1] = m
    return full
def mascara_seta(f, i):
    full = np.zeros(f.shape[:2], np.uint8)
    if not seta or i < seta["de"]: return full
    if "retangulos" in seta:   # mascara fixa (seta animada por cima de roupa da mesma cor)
        for x0, y0, x1, y1 in seta["retangulos"]: full[y0:y1, x0:x1] = 1
        if seta.get("vermelho_extra"):   # + vermelho saturado que escapar dos retangulos (seta pulando)
            R = np.array(seta["retangulos"]); x0, y0 = R[:, :2].min(0) - 40; x1, y1 = R[:, 2:].max(0) + 40
            hsv = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
            red = (((hsv[...,0] < 8) | (hsv[...,0] > 172)) & (hsv[...,1] > 150) & (hsv[...,2] > 120)).astype(np.uint8)
            full[y0:y1, x0:x1] |= cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))
        return full
    x0, y0, x1, y1 = seta["caixa"]; r = f[y0:y1, x0:x1]; hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV)
    red = (((hsv[...,0] < 10) | (hsv[...,0] > 170)) & (hsv[...,1] > 120) & (hsv[...,2] > 90)).astype(np.uint8)
    if red.sum() < 300: return full
    m = cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))  # inclui o contorno branco
    full[y0:y1, x0:x1] = m
    return full
MK = []; ema = None; prev = None; t0 = time.time(); cortes = []
for i in range(N):
    ok, f = cap.read()
    if not ok: break
    g = cv2.resize(f, (90, 160)).astype(np.float32)
    if prev is not None and np.abs(g - prev).mean() > 20: ema = None; cortes.append(i)
    prev = g
    m = mascara_legenda(f) | mascara_seta(f, i)
    MK.append(np.packbits(m))
    if m.sum() == 0:
        ema = None; ff.stdin.write(np.ascontiguousarray(f).tobytes()); continue
    ys = np.where(m.any(1))[0]; a0 = max(0, min(C0, ys.min() - 60)); a1 = min(1280, max(C1, ys.max() + 60))
    crop = f[a0:a1].copy(); mk = m[a0:a1]
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
    l = np.zeros_like(f, dtype=np.float32); l[a0:a1] = r
    ema = l if ema is None else 0.65 * l + 0.35 * ema
    al = np.maximum(cv2.GaussianBlur(m.astype(np.float32), (11, 11), 0), m)[..., None]
    f = np.clip(ema * al + f * (1 - al), 0, 255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
    if (i + 1) % 100 == 0:
        el = time.time() - t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s", flush=True)
ff.stdin.close(); ff.wait()
np.save(cfg["saida"].replace(".mp4", "_mask.npy"), np.array(MK))
print("ok", i + 1, "quadros", round(time.time() - t0), "s; cortes:", cortes)
