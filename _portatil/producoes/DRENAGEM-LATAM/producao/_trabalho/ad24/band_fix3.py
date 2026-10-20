# -*- coding: utf-8 -*-
"""Troca o texto da faixa escura do rótulo (MAYAVERRA -> LYMPHORIA) quadro a quadro, sem IA.
Evolução do ad25/band_fix.py: ROI com chaves (bottle em movimento), faixa preenchida na LARGURA TODA do rótulo
com a cor de fundo coluna a coluna (mantém o degradê/brilho), endireita a faixa pelo ângulo e suaviza no tempo.

  python band_fix3.py in.mp4 out.mp4 --roi "q:x0,y0,x1,y1;q:..." [--texto LYMPHORIA] [--min-area 150]
"""
import argparse
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument("ent"); ap.add_argument("sai"); ap.add_argument("--roi", required=True)
ap.add_argument("--texto", default="LYMPHORIA"); ap.add_argument("--min-area", type=int, default=150)
ap.add_argument("--alfa", type=float, default=0.5, help="suavização temporal (1 = sem)")
a = ap.parse_args()
FONT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"

if ":" in a.roi:
    K = sorted((int(q), list(map(float, r.split(",")))) for q, r in (c.split(":") for c in a.roi.split(";")))
else:
    K = [(0, list(map(float, a.roi.split(","))))]


def roi_em(n):
    if n <= K[0][0]:
        return [int(v) for v in K[0][1]]
    for (q0, r0), (q1, r1) in zip(K, K[1:]):
        if n <= q1:
            t = (n - q0) / (q1 - q0)
            return [int(round(u + (v - u) * t)) for u, v in zip(r0, r1)]
    return [int(v) for v in K[-1][1]]


cap = cv2.VideoCapture(a.ent)
W, H = int(cap.get(3)), int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                      "-i", "-", "-c:v", "libx264", "-crf", "13", "-pix_fmt", "yuv420p", "-r", "30", a.sai],
                     stdin=subprocess.PIPE)
est = None  # cx, cy, w, h, ang, L, R  (suavizado)
n = falhas = 0
while True:
    ok, f = cap.read()
    if not ok:
        break
    x0, y0, x1, y1 = roi_em(n)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    roi = f[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (35, 30, 15), (95, 255, 140))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    medida = None
    if k > 1:
        i = 1 + int(np.argmax(st[1:, 4]))
        if st[i, 4] >= a.min_area:
            cnt, _ = cv2.findContours((lab == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hull = cv2.convexHull(max(cnt, key=cv2.contourArea))
            (cx, cy), (rw, rh), ang = cv2.minAreaRect(hull)
            if rw < rh:
                rw, rh = rh, rw; ang += 90
            if ang > 45: ang -= 180
            if ang < -45: ang += 180
            # endireita para achar a largura do rótulo (creme logo abaixo da faixa)
            M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
            rot = cv2.warpAffine(roi, M, (roi.shape[1], roi.shape[0]), flags=cv2.INTER_LINEAR,
                                 borderMode=cv2.BORDER_REPLICATE)
            ya = int(min(rot.shape[0] - 2, cy + rh / 2 + 2))
            yb = int(min(rot.shape[0] - 1, cy + rh / 2 + max(6, rh * 1.3)))
            hv = cv2.cvtColor(rot[ya:yb], cv2.COLOR_BGR2HSV)
            claro = ((hv[..., 2] > 135) & (hv[..., 1] < 90)).mean(axis=0) > 0.25
            c = int(np.clip(cx, 0, len(claro) - 1))
            gap = max(4, int(rh * 0.5))
            L = c
            while L > 0 and claro[max(0, L - gap):L].any(): L -= 1
            R = c
            while R < len(claro) - 1 and claro[R + 1:R + 1 + gap].any(): R += 1
            L, R = L + 1, R - 1
            if R - L < rw * 0.8:  # não achou o creme: usa a própria faixa
                L, R = cx - rw / 2, cx + rw / 2
            medida = np.array([cx + x0, cy + y0, rw, rh, ang, L + x0, R + x0], float)
    if medida is None:
        falhas += 1
        if est is None:
            p.stdin.write(f.tobytes()); n += 1
            continue
    else:
        est = medida if est is None else a.alfa * medida + (1 - a.alfa) * est
    cx, cy, rw, rh, ang, L, R = est
    # recorte endireitado em volta da faixa
    pad = int(rh * 1.5 + (R - L) * 0.2 + 10)
    X0, Y0 = int(max(0, min(L, cx - rw / 2) - pad)), int(max(0, cy - rh / 2 - pad))
    X1, Y1 = int(min(W, max(R, cx + rw / 2) + pad)), int(min(H, cy + rh / 2 + pad))
    pat = f[Y0:Y1, X0:X1].copy()
    ccx, ccy = cx - X0, cy - Y0
    M = cv2.getRotationMatrix2D((ccx, ccy), ang, 1.0)
    rp = cv2.warpAffine(pat, M, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    l, r = int(L - X0 + 2), int(R - X0 - 2)
    t, b = int(round(ccy - rh / 2 + 1.5)), int(round(ccy + rh / 2 - 1.5))
    l, r = max(0, l), min(rp.shape[1], r)
    t, b = max(0, t), min(rp.shape[0], b)
    if r - l > 8 and b - t > 4:
        band = rp[t:b, l:r].astype(np.float32)
        lum = band.mean(axis=2)
        cor = np.zeros((r - l, 3), np.float32)
        for j in range(r - l):
            col = band[:, j]; lj = lum[:, j]
            sel = lj <= np.percentile(lj, 45)
            cor[j] = col[sel].mean(axis=0)
        cor = cv2.blur(cor.reshape(1, -1, 3), (15, 1)).reshape(-1, 3)
        # perfil vertical leve (borda de cima/baixo), a partir das linhas escuras
        vert = np.array([np.percentile(lum[y], 40) for y in range(b - t)], np.float32)
        vert = vert / max(1.0, np.median(vert))
        novo = cor[None, :, :] * np.clip(vert, 0.85, 1.15)[:, None, None]
        rp[t:b, l:r] = np.clip(novo, 0, 255).astype(np.uint8)
        # texto
        hh = b - t
        fs = max(7, int(hh * 0.55))
        fnt = ImageFont.truetype(FONT, fs)
        while fnt.getlength(a.texto) > (r - l) * 0.72 and fs > 6:
            fs -= 1; fnt = ImageFont.truetype(FONT, fs)
        img = Image.fromarray(cv2.cvtColor(rp, cv2.COLOR_BGR2RGB))
        d = ImageDraw.Draw(img)
        tw = fnt.getlength(a.texto)
        bb = fnt.getbbox(a.texto)
        tx = (l + r) / 2 - tw / 2
        ty = (t + b) / 2 - (bb[1] + bb[3]) / 2
        d.text((tx, ty), a.texto, font=fnt, fill=(236, 230, 212))
        rp = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        # volta para o ângulo original e cola só a faixa
        mask = np.zeros(rp.shape[:2], np.uint8); mask[t:b, l:r] = 255
        Mi = cv2.getRotationMatrix2D((ccx, ccy), -ang, 1.0)
        back = cv2.warpAffine(rp, Mi, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        mb = cv2.warpAffine(mask, Mi, (pat.shape[1], pat.shape[0]), flags=cv2.INTER_LINEAR)
        mb = cv2.GaussianBlur(mb, (3, 3), 0).astype(np.float32)[..., None] / 255
        f[Y0:Y1, X0:X1] = (back * mb + pat * (1 - mb)).astype(np.uint8)
    p.stdin.write(f.tobytes()); n += 1
p.stdin.close(); p.wait()
print("ok", n, "quadros, sem faixa em", falhas)
