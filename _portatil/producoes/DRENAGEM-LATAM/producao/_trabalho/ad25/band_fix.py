# -*- coding: utf-8 -*-
"""Apaga o texto da faixa verde do rótulo (MAYA VERRA) quadro a quadro: acha a faixa verde-escura dentro de uma
região de busca, preenche o casco convexo com a cor mediana da faixa e escreve LYMPHORIA girado no ângulo da faixa.
  python band_fix.py in.mp4 out.mp4 --roi x0,y0,x1,y1 [--texto LYMPHORIA] [--min-area 300]"""
import argparse, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument("ent"); ap.add_argument("sai"); ap.add_argument("--roi", required=True)
ap.add_argument("--texto", default="LYMPHORIA"); ap.add_argument("--min-area", type=int, default=300)
ap.add_argument("--prev", default=None)
a = ap.parse_args()
x0, y0, x1, y1 = map(int, a.roi.split(","))
FONT = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf"
cap = cv2.VideoCapture(a.ent); fps = cap.get(5); W = int(cap.get(3)); H = int(cap.get(4))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(fps), "-i", "-",
                      "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", a.sai], stdin=subprocess.PIPE)
n = 0; falhas = 0
while True:
    ok, f = cap.read()
    if not ok: break
    roi = f[y0:y1, x0:x1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    m = cv2.inRange(hsv, (35, 30, 15), (95, 255, 140))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    k, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if k > 1:
        i = 1 + int(np.argmax(st[1:, 4]))
        if st[i, 4] >= a.min_area:
            comp = (lab == i).astype(np.uint8)
            cnt, _ = cv2.findContours(comp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            hull = cv2.convexHull(max(cnt, key=cv2.contourArea))
            raw = cv2.inRange(hsv, (35, 30, 15), (95, 255, 140)) > 0
            cor = np.median(roi[(comp > 0) & raw], axis=0)
            fill = np.zeros_like(comp); cv2.fillConvexPoly(fill, hull, 1)
            fill = cv2.erode(fill, np.ones((3, 3), np.uint8))
            roi[fill > 0] = cor.astype(np.uint8)
            (cx, cy), (rw, rh), ang = cv2.minAreaRect(hull)
            if rw < rh: rw, rh = rh, rw; ang += 90
            if ang > 45: ang -= 180
            if ang < -45: ang += 180
            fs = max(8, int(rh * 0.55))
            fnt = ImageFont.truetype(FONT, fs)
            tw = fnt.getlength(a.texto)
            while tw > rw * 0.8 and fs > 6:
                fs -= 1; fnt = ImageFont.truetype(FONT, fs); tw = fnt.getlength(a.texto)
            img = Image.new("RGBA", (int(tw) + 8, fs + 10), (0, 0, 0, 0))
            ImageDraw.Draw(img).text((4, 2), a.texto, font=fnt, fill=(235, 228, 210, 255))
            img = img.rotate(-ang, expand=True, resample=Image.BICUBIC)
            base = Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)).convert("RGBA")
            base.alpha_composite(img, (int(cx - img.width / 2), int(cy - img.height / 2)))
            roi[:] = cv2.cvtColor(np.array(base.convert("RGB")), cv2.COLOR_RGB2BGR)
        else: falhas += 1
    else: falhas += 1
    p.stdin.write(f.tobytes()); n += 1
p.stdin.close(); p.wait()
print("ok", n, "quadros, sem faixa em", falhas)
