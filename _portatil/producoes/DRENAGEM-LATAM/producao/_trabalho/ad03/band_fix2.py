# -*- coding: utf-8 -*-
"""Variante do band_fix (ad25) para faixa verde HORIZONTAL do rótulo: acha as linhas da faixa pela fração de
verde, preenche só a faixa (linha a linha, com a cor mediana da própria linha) e escreve LYMPHORIA centrado.
Geometria suavizada no tempo (mediana de 7 quadros) para o texto não tremer.
  python band_fix2.py in.mp4 out.mp4 --roi x0,y0,x1,y1 [--frac 0.45] [--texto LYMPHORIA] [--escala 0.52]"""
import argparse, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument("ent"); ap.add_argument("sai"); ap.add_argument("--roi", required=True)
ap.add_argument("--frac", type=float, default=0.45); ap.add_argument("--texto", default="LYMPHORIA")
ap.add_argument("--escala", type=float, default=0.52); ap.add_argument("--fecho", type=int, default=15)
ap.add_argument("--roi2", default=None, help="ROI no último quadro (interpolada)")
ap.add_argument("--modo", default="verde"); ap.add_argument("--smax", type=int, default=140); ap.add_argument("--vmax", type=int, default=135); ap.add_argument("--vfill", type=int, default=110)
a = ap.parse_args()
x0, y0, x1, y1 = map(int, a.roi.split(","))
FONT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"
cap = cv2.VideoCapture(a.ent); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
Q = []
while True:
    ok, f = cap.read()
    if not ok: break
    Q.append(f)
def mascara(hsv):
    if a.modo == "escuro":  # faixa = pixels escuros e pouco saturados (vidro âmbar é muito saturado; rótulo creme é claro)
        return cv2.inRange(hsv, (0, 0, 20), (179, a.smax, a.vmax))
    return cv2.inRange(hsv, (35, 30, 15), (95, 255, 140))


R0 = np.array([x0, y0, x1, y1], float)
R1 = np.array(list(map(int, a.roi2.split(","))), float) if a.roi2 else R0
ROIS = [tuple(int(round(v)) for v in R0 + (R1 - R0) * (i / max(1, len(Q) - 1))) for i in range(len(Q))]
geo = []
for f, (x0, y0, x1, y1) in zip(Q, ROIS):
    hsv = cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    g = cv2.morphologyEx(mascara(hsv), cv2.MORPH_CLOSE, np.ones((a.fecho, a.fecho), np.uint8)) > 0
    fr = g.mean(axis=1)
    rows = np.where(fr > a.frac)[0]
    if len(rows) == 0: geo.append(None); continue
    # maior sequência contígua (tolerância de 2 linhas)
    runs, s = [], rows[0]
    for p, q in zip(rows[:-1], rows[1:]):
        if q - p > 3: runs.append((s, p)); s = q
    runs.append((s, rows[-1]))
    ya, yb = max(runs, key=lambda r: r[1] - r[0])
    xs = np.where(g[ya:yb + 1].any(axis=0))[0]
    cols = g[ya:yb + 1].mean(axis=0) > 0.5
    xc = np.where(cols)[0]
    if len(xc) < 5: geo.append(None); continue
    geo.append([ya + y0, yb + y0, xc[0] + x0, xc[-1] + x0])
ok_idx = [i for i, v in enumerate(geo) if v]
G = np.array([geo[i] if geo[i] else geo[min(ok_idx, key=lambda j: abs(j - i))] for i in range(len(Q))], float)
Gs = np.array([np.median(G[max(0, i - 3):i + 4], axis=0) for i in range(len(G))])
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.sai], stdin=subprocess.PIPE)
for f, (ya, yb, xa, xb), (x0, y0, x1, y1) in zip(Q, Gs, ROIS):
    ya, yb, xa, xb = int(round(ya)) - y0, int(round(yb)) - y0, int(round(xa)) - x0, int(round(xb)) - x0
    roi = f[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    g = (mascara(hsv) > 0) & (hsv[..., 2] < a.vfill)
    m = 1  # margem
    ult = None
    for y in range(max(0, ya - m), min(roi.shape[0], yb + m + 1)):
        seg = roi[y, xa:xb + 1]; gg = g[y, xa:xb + 1]
        if gg.sum() > 3:
            cor = np.median(seg[gg], axis=0); ult = cor
        else:
            blk = roi[max(0, ya):yb + 1, xa:xb + 1][g[max(0, ya):yb + 1, xa:xb + 1]]
            cor = np.median(blk, axis=0) if len(blk) > 3 else (ult if ult is not None else np.median(seg, axis=0))
        roi[y, xa + 1:xb] = cor.astype(np.uint8)
    bh, bw = yb - ya, xb - xa
    fs = max(8, int(bh * a.escala)); fnt = ImageFont.truetype(FONT, fs); tw = fnt.getlength(a.texto)
    while tw > bw * 0.78 and fs > 6:
        fs -= 1; fnt = ImageFont.truetype(FONT, fs); tw = fnt.getlength(a.texto)
    base = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    d = ImageDraw.Draw(base)
    bb = d.textbbox((0, 0), a.texto, font=fnt)
    cx, cy = (xa + xb) / 2, (ya + yb) / 2
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), a.texto, font=fnt, fill=(238, 232, 214))
    roi[:] = cv2.cvtColor(np.array(base), cv2.COLOR_RGB2BGR)
    p.stdin.write(f.tobytes())
p.stdin.close(); p.wait()
print("ok", len(Q), "quadros; sem faixa em", sum(1 for v in geo if v is None))
