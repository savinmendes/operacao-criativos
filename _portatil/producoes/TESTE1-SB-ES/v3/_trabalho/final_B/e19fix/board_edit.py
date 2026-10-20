# -*- coding: utf-8 -*-
"""board_clean.png -> board_edit.png com 'Crux' e 'Silentium' (no lugar de 'Cruz' e 'Silentio'), Times Bold condensada como o original."""
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
SRC = r"C:\Users\PICHAU\Downloads\TESTE1-SB-ES\_trabalho\q\board_clean.png"
b = cv2.imread(SRC); out = b.copy()
LAB = {"Crux": (326, 396, 394, 424, "Cruz"), "Silentium": (72, 662, 166, 693, "Silentio")}
for novo, (x0, y0, x1, y1, velho) in LAB.items():
    roi = b[y0:y1, x0:x1]; g = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    m = (g < 75).astype(np.uint8)
    ys, xs = np.nonzero(m); tx0, tx1, ty0, ty1 = xs.min(), xs.max(), ys.min(), ys.max()
    print(velho, "bbox", x0 + tx0, y0 + ty0, x0 + tx1, y0 + ty1, "cor", np.median(roi[m > 0], axis=0))
    cor = tuple(int(c) for c in np.percentile(roi[m > 0], 20, axis=0)[::-1])
    mk = cv2.dilate(m, np.ones((5, 5), np.uint8)) * 255
    roi2 = cv2.inpaint(roi, mk, 5, cv2.INPAINT_TELEA)
    # texto novo: altura total (cap+descendente) = mesma do antigo; largura por caractere = mesma proporção
    H = ty1 - ty0 + 1; Wold = tx1 - tx0 + 1
    f = ImageFont.truetype(r"C:\Windows\Fonts\timesbd.ttf", 120)
    tmp = Image.new("L", (1200, 300), 0); ImageDraw.Draw(tmp).text((20, 40), velho, font=f, fill=255, stroke_width=2, stroke_fill=255); bo = tmp.getbbox()
    sy = H / (bo[3] - bo[1]); sx = Wold / (bo[2] - bo[0])          # escala do antigo (mede a condensação real)
    tmp = Image.new("L", (1400, 300), 0); ImageDraw.Draw(tmp).text((20, 40), novo, font=f, fill=255, stroke_width=2, stroke_fill=255); bn = tmp.getbbox()
    mn = tmp.crop(bn); w = max(1, round((bn[2] - bn[0]) * sx)); h = max(1, round((bn[3] - bn[1]) * sy))
    lim = (x1 - x0) - 6
    if w > lim: w = lim
    mn = mn.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(0.4))
    a = np.asarray(mn, np.float32)[..., None] / 255
    cx = x0 + (tx0 + tx1) / 2; X = int(round(cx - w / 2)); Y = y0 + ty0
    # 'x'/'m' não têm descendente nem ascendente diferente de 'z'/'o': alinha pela linha de base (topo do maiúsculo)
    reg = roi2.astype(np.float32).copy(); out[y0:y1, x0:x1] = roi2
    R = out[Y:Y + h, X:X + w].astype(np.float32)
    out[Y:Y + h, X:X + w] = (R * (1 - a) + np.array(cor[::-1], np.float32) * a).astype(np.uint8)
cv2.imwrite("board_edit.png", out)
z = np.hstack([cv2.resize(b[380:435, 300:425], None, fx=3, fy=3), cv2.resize(out[380:435, 300:425], None, fx=3, fy=3)])
z2 = np.hstack([cv2.resize(b[648:705, 50:190], None, fx=3, fy=3), cv2.resize(out[648:705, 50:190], None, fx=3, fy=3)])
cv2.imwrite("cmp_labels.png", np.vstack([np.hstack([z, np.zeros((z.shape[0], max(0, z2.shape[1] - z.shape[1]), 3), np.uint8)]) if z2.shape[1] > z.shape[1] else z, z2[:, :max(z.shape[1], z2.shape[1])]]))
