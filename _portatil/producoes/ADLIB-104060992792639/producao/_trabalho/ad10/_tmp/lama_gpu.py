"""LaMa (GPU) na legenda PT (amarela, y 960-1090) e nas setas vermelhas PT (y 740-985) do NN.mp4.
Uso: python lama_gpu.py NN quadros  -> _tmp/lama/NNNN.png (faixa y R0-R1) e _tmp/lama_mask.npy
Máscara JUSTA: glifo amarelo + contorno escuro dilatados 9 px; seta = vermelho + borda branca (dilatado 11) + brilhos brancos perto."""
import os, sys, time, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
NN, N = sys.argv[1], int(sys.argv[2]); SETA0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
R0, R1 = 700, 1130
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
cap = cv2.VideoCapture(f'../../../../UNICOS_HD/{NN}.mp4'); MK = np.zeros((N, R1-R0, 720), np.uint8); t0 = time.time()
K9 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
for i in range(N):
    ok, f = cap.read(); roi = f[R0:R1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV); h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = np.zeros(roi.shape[:2], np.uint8)
    # legenda amarela (y 960-1090)
    ya, yb = 960-R0, 1090-R0
    core = ((h >= 15) & (h <= 42) & (s >= 80) & (v >= 140)).astype(np.uint8)
    core[:ya] = 0; core[yb:] = 0
    core = cv2.morphologyEx(core, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(core)
    keep = np.zeros_like(core)
    for k in range(1, n):
        if st[k, 4] >= 12: keep[lab == k] = 1
    if keep.sum() > 150:
        dark = cv2.dilate(keep, np.ones((9, 9), np.uint8)) & (v < 110).astype(np.uint8)
        m |= cv2.dilate(cv2.dilate(keep, K9) | dark, np.ones((9, 9), np.uint8))
    # seta vermelha (y 740-985)
    b, g, r = cv2.split(roi.astype(np.int16))
    red = ((r > 150) & (g < 90) & (b < 90)).astype(np.uint8); red[:740-R0] = 0; red[985-R0:] = 0
    red = cv2.morphologyEx(red, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    if i >= SETA0 and red.sum() > 300:
        ys, xs = np.where(red)
        m |= cv2.dilate(red, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (23, 23)))
        x0, x1, y0, y1 = max(0, xs.min()-110), min(720, xs.max()+110), max(0, ys.min()+20), min(R1-R0, ys.max()+40)
        wht = ((np.minimum(np.minimum(b, g), r) > 228)).astype(np.uint8)
        box = np.zeros_like(wht); box[y0:y1, x0:x1] = 1
        m |= cv2.dilate(wht & box, np.ones((7, 7), np.uint8))
    MK[i] = m
    out = f'lama/{i:04d}.png'
    if m.sum() == 0: cv2.imwrite(out, roi); continue
    rr = lama(Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)), Image.fromarray(m * 255))
    rr = cv2.cvtColor(np.array(rr), cv2.COLOR_RGB2BGR)[:roi.shape[0], :roi.shape[1]]
    cv2.imwrite(out, rr)
    if (i+1) % 200 == 0:
        el = time.time()-t0; print(f"[{i+1}/{N}] {100*(i+1)//N}% falta ~{el/(i+1)*(N-i-1):.0f} s", flush=True)
np.save('lama_mask.npy', MK); print("ok", time.time()-t0)
