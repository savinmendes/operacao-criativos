# -*- coding: utf-8 -*-
"""Moldura da live (720x1280 RGBA) para o padre Juan Méndez: anel + LIVE do v4, foto do perfil = recorte da referência da página,
arroba padre.juanmendez + selo azul, caixas LIVE / visualizações do v4."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import arroba as A
T = Path(__file__).resolve().parent
REF = np.asarray(Image.open(T / "f700.png").convert("RGB")).astype(np.float32)
H, W = 1280, 720
out = np.zeros((H, W, 4), np.float32)
CX, CY = 90.5, 68.5
yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
# foto do perfil
pg = Image.open(T.parent.parent / "_ref" / "padre_juan_mendez_PAGINA.png").convert("RGB")
fc = pg.crop((612 - 210, 250 - 190, 612 + 210, 250 + 230)).resize((92, 92), Image.LANCZOS)
ph = np.zeros((H, W, 3), np.float32); ph[int(CY) - 46 + 0:int(CY) + 46, int(CX) - 46 + 0:int(CX) + 46] = np.asarray(fc, np.float32)[: 92, : 92]
a_ph = np.clip(46.3 - d, 0, 1)
out[..., :3] = ph * a_ph[..., None]; out[..., 3] = a_ph
# anel do v4 (43.8..49.8)
a_ring = np.clip(d - 45.6, 0, 1) * np.clip(49.8 - d, 0, 1)
out[..., :3] = out[..., :3] * (1 - a_ring[..., None]) + REF * a_ring[..., None]; out[..., 3] = np.maximum(out[..., 3], a_ring)
# etiqueta LIVE embaixo do círculo (pixels saturados/brancos do v4)
r, g, b = REF[..., 0], REF[..., 1], REF[..., 2]
tag = np.zeros((H, W), np.uint8); sl = (slice(100, 130), slice(60, 122))
sat = ((r > 150) & (g < 120)) | ((r > 120) & (b > 120) & (g < 90)) | (REF.min(2) > 200)
tag[sl] = sat[sl]; tag = cv2.morphologyEx(tag, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
ys, xs = np.where(tag); x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
tg = Image.new("L", (W, H), 0); ImageDraw.Draw(tg).rounded_rectangle((69, 106, 113, 124), 4, fill=255); m = np.asarray(tg, np.float32) / 255
out[..., :3] = out[..., :3] * (1 - m[..., None]) + REF * m[..., None]; out[..., 3] = np.maximum(out[..., 3], m)
print("etiqueta", x0, x1, y0, y1)
# caixas LIVE / visualizações (cópia do v4 com cantos arredondados)
bx = Image.new("L", (W, H), 0); ImageDraw.Draw(bx).rounded_rectangle((592, 57, 631, 88), 3, fill=255); ImageDraw.Draw(bx).rounded_rectangle((634, 57, 673, 88), 3, fill=255)
mb = np.asarray(bx, np.float32) / 255
out[..., :3] = out[..., :3] * (1 - mb[..., None]) + REF * mb[..., None]; out[..., 3] = np.maximum(out[..., 3], mb)
# arroba + selo azul (com sombra suave para ler sobre qualquer fundo)
tl = np.zeros((H, W), np.float32); tl[40:140] = A.TL
sh = cv2.GaussianBlur(tl, (0, 0), 2.0) * 0.55
out[..., :3] *= (1 - sh[..., None]); out[..., 3] = np.maximum(out[..., 3], sh)
out[..., :3] = out[..., :3] * (1 - tl[..., None]) + A.COR * tl[..., None]; out[..., 3] = np.maximum(out[..., 3], tl)
ba = np.zeros((H, W), np.float32); ba[A.BY:A.BY + 24, A.BX - 12:A.BX + 12] = A.BA[..., 0]
bc = np.zeros((H, W, 3), np.float32); bc[A.BY:A.BY + 24, A.BX - 12:A.BX + 12] = A.BADGE
out[..., :3] = out[..., :3] * (1 - ba[..., None]) + bc * ba[..., None]; out[..., 3] = np.maximum(out[..., 3], ba)
o = out.copy(); al = np.maximum(o[..., 3:4], 1e-6); o[..., :3] = np.where(o[..., 3:4] > 0, o[..., :3] / al, 0)   # des-premultiplica
Image.fromarray(np.dstack([np.clip(o[..., :3], 0, 255), np.clip(out[..., 3] * 255, 0, 255)]).astype(np.uint8), "RGBA").save(T / "ov" / "moldura_jm.png")
av = Image.open(T / "avatar" / "jm_b.png").convert("RGBA"); av.alpha_composite(Image.open(T / "ov" / "moldura_jm.png"))
av.crop((0, 0, 720, 300)).resize((1440, 600)).save(T / "moldura_teste.png"); print("ok")
