# -*- coding: utf-8 -*-
"""Sobreposições do Ranking 03 (720x1280): faixa vermelha ES (cobre a PT 58-662 x 158-314), rodapé de telejornal ES
com logo inventado NV / NOTIVISIÓN (cobre o rodapé PT "20:57 JN"), moldura da live do Juan no layout do padre original
(bisbo.paulorb -> padre.juanmendez), TRANSMISIÓN ELIMINADA, DEUTERONOMIO 8:18. EN VIVO / TOCA / seta / selo reaproveitados."""
import shutil, numpy as np, cv2
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
P = Path(__file__).resolve().parent; O = P / "ov"; O.mkdir(exist_ok=True)
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
def pf(s, w="ExtraBold"): return ImageFont.truetype(str(POP / f"Poppins-{w}.ttf"), s)
def sombra(im, r=6, a=170, dy=4):
    al = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * a / 255))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); sh.putalpha(al); out = Image.new("RGBA", im.size); out.alpha_composite(sh, (0, dy)); out.alpha_composite(im); return out
rng = np.random.default_rng(11); W, H = 720, 1280
# ---------- faixa vermelha (papel rasgado), opaca, maior que a PT ----------
x0, x1, y0, y1 = 48, 672, 146, 328
pts = []
for x in np.linspace(x0, x1, 40): pts.append((x, y0 + rng.uniform(-5, 0)))
for y in np.linspace(y0, y1, 12): pts.append((x1 + rng.uniform(0, 6), y))
for x in np.linspace(x1, x0, 40): pts.append((x, y1 + rng.uniform(0, 6)))
for y in np.linspace(y1, y0, 12): pts.append((x0 + rng.uniform(-6, 0), y))
ban = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ban); d.polygon(pts, fill=(200, 14, 18, 255))
arr = np.asarray(ban).astype(np.int16); noise = rng.normal(0, 6, arr.shape[:2]).astype(np.int16)
for k in range(3): arr[..., k] = np.clip(arr[..., k] + noise * (arr[..., 3] > 0), 0, 255)
ban = Image.fromarray(arr.astype(np.uint8), "RGBA"); d = ImageDraw.Draw(ban)
L = ["MUJER ES DESPEDIDA", "Y ALGO INCREÍBLE", "SUCEDE"]
fs = 44; f = pf(fs)
while max(f.getlength(t) for t in L) > (x1 - x0 - 50): fs -= 1; f = pf(fs)
for k, t in enumerate(L):
    d.text((360, 186 + k * 54), t, font=f, anchor="mm", fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(60, 0, 0, 255))
sombra(ban, 5, 120, 3).save(O / "faixa.png")
# ---------- rodapé de telejornal (cobre o PT de 962 para baixo) ----------
rod = np.zeros((H, W, 4), np.float32)
for y in range(950, H):
    c = (0, 34, 154) if y < 1136 else (2, 38, 125)
    rod[y, :, :3] = c; rod[y, :, 3] = 1.0 if y >= 972 else (y - 950) / 22
rod = Image.fromarray(np.clip(rod * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA"); d = ImageDraw.Draw(rod)
d.text((170, 1076), "20:57", font=pf(44, "Bold"), anchor="mm", fill=(255, 255, 255, 255))
lg = Image.new("RGBA", (220, 130), (0, 0, 0, 0)); dl = ImageDraw.Draw(lg)
dl.text((110, 50), "NV", font=pf(84), anchor="mm", fill=(255, 255, 255, 255))
grad = np.linspace(255, 150, 130)[:, None] * np.ones((130, 220)); la = np.asarray(lg).astype(np.float32)
la[..., 0] = np.minimum(la[..., 0], grad * 0.80); la[..., 1] = np.minimum(la[..., 1], grad * 0.88); la[..., 2] = np.minimum(la[..., 2], grad)
lg = Image.fromarray(la.astype(np.uint8), "RGBA"); dl = ImageDraw.Draw(lg)
dl.text((110, 112), "NOTIVISIÓN", font=pf(19, "Bold"), anchor="mm", fill=(255, 255, 255, 235))
rod.alpha_composite(sombra(lg, 4, 110, 2), (60, 1092))
d.line((262, 985, 262, 1242), fill=(255, 255, 255, 255), width=3)
txt = "MINUTOS DESPUÉS DE SER DESPEDIDA, MUJER REZA LA ORACIÓN DE SAN BENITO Y RECIBE UNA OFERTA DE TRABAJO"
fr = pf(25, "Bold"); lines = []; cur = ""
for w in txt.split():
    t = (cur + " " + w).strip()
    if fr.getlength(t) > 400: lines.append(cur); cur = w
    else: cur = t
lines.append(cur)
yt = 1112 - (len(lines) - 1) * 37 / 2
for k, t in enumerate(lines): d.text((280, yt + k * 37), t, font=fr, anchor="lm", fill=(255, 255, 255, 255))
rod.save(O / "rodape.png")
# ---------- moldura da live (layout do padre do original, arroba padre.juanmendez) ----------
REF = np.asarray(Image.open(P / "ref" / "p_25.0.png").convert("RGB")).astype(np.float32)
mol = np.zeros((H, W, 4), np.float32)
yy, xx = np.mgrid[0:H, 0:W]; CX, CY = 83.5, 77.5; dd = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
av = Image.open(P / "avatar" / "jm_a.png").convert("RGB")
fc = np.asarray(av.crop((220, 170, 470, 420)).resize((84, 84), Image.LANCZOS)).astype(np.float32)
ph = np.zeros((H, W, 3), np.float32); ph[int(CY) - 42:int(CY) + 42, int(CX) - 42:int(CX) + 42] = fc
a_ph = np.clip(41.5 - dd, 0, 1); mol[..., :3] = ph * a_ph[..., None]; mol[..., 3] = a_ph
a_ring = np.clip(dd - 41.5, 0, 1) * np.clip(47.8 - dd, 0, 1)
mol[..., :3] = mol[..., :3] * (1 - a_ring[..., None]) + REF * a_ring[..., None]; mol[..., 3] = np.maximum(mol[..., 3], a_ring)
def copia_rr(box, r=5):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255); m = np.asarray(m, np.float32) / 255
    mol[..., :3] = mol[..., :3] * (1 - m[..., None]) + REF * m[..., None]; mol[..., 3] = np.maximum(mol[..., 3], m)
copia_rr((64, 113, 104, 128), 4)          # etiqueta LIVE sob o círculo
copia_rr((498, 53, 564, 100), 5)          # LIVE
copia_rr((572, 55, 650, 100), 5)          # olho + contagem
fo2 = ImageFont.truetype(OS, 68)
nm = Image.new("RGBA", (W * 2, 200), (0, 0, 0, 0)); ImageDraw.Draw(nm).text((322, 180), "padre.juanmendez", font=fo2, anchor="ls", fill=(255, 255, 255, 255))
nm = nm.resize((W, 100), Image.LANCZOS); nma = np.zeros((H, W, 4), np.float32); nma[0:100] = np.asarray(nm, np.float32)
xfim = 161 + ImageFont.truetype(OS, 34).getlength("padre.juanmendez")
sh = cv2.GaussianBlur(nma[..., 3], (0, 0), 2.0) / 255 * 0.45
mol[..., :3] *= (1 - sh[..., None]); mol[..., 3] = np.maximum(mol[..., 3], sh)
ta = nma[..., 3] / 255; mol[..., :3] = mol[..., :3] * (1 - ta[..., None]) + 255 * ta[..., None]; mol[..., 3] = np.maximum(mol[..., 3], ta)
bx, by = int(xfim + 17), 78
yb, xb = np.mgrid[0:26, 0:26]; ba = np.clip(11.5 - np.sqrt((yb - 12.5) ** 2 + (xb - 12.5) ** 2), 0, 1)
bm = np.zeros((H, W), np.float32); bm[by - 13:by + 13, bx - 13:bx + 13] = ba
bc = np.zeros((H, W, 3), np.float32); bc[by - 13:by + 13, bx - 13:bx + 13] = REF[78 - 13:78 + 13, 405 - 13:405 + 13]
mol[..., :3] = mol[..., :3] * (1 - bm[..., None]) + bc * bm[..., None]; mol[..., 3] = np.maximum(mol[..., 3], bm)
# barra de comentário + reticências + coração (pílula 10-613 x 1174-1255, coração em 677,1215)
bb = Image.new("L", (W * 2, H * 2), 0); db = ImageDraw.Draw(bb)
db.rounded_rectangle((20, 2348, 1226, 2510), 81, outline=255, width=5)
for x in (1108, 1131, 1154): db.ellipse((x - 5, 2427, x + 5, 2437), fill=255)
tt = np.linspace(0, 2 * np.pi, 200); hx = 16 * np.sin(tt) ** 3; hy = -(13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt))
db.line([(1354 + 2.9 * a, 2432 + 2.9 * b) for a, b in zip(hx, hy)], fill=255, width=5, joint="curve")
bb = np.asarray(bb.resize((W, H), Image.LANCZOS), np.float32) / 255 * 0.92
sh = cv2.GaussianBlur(bb, (0, 0), 1.5) * 0.35
mol[..., :3] *= (1 - sh[..., None]); mol[..., 3] = np.maximum(mol[..., 3], sh)
mol[..., :3] = mol[..., :3] * (1 - bb[..., None]) + 255 * bb[..., None]; mol[..., 3] = np.maximum(mol[..., 3], bb)
Image.fromarray(np.dstack([np.clip(np.where(mol[..., 3:4] > 0, mol[..., :3], 0), 0, 255), np.clip(mol[..., 3] * 255, 0, 255)]).astype(np.uint8), "RGBA").save(O / "moldura_jm.png")
# ---------- TRANSMISIÓN ELIMINADA ----------
fs = pf(62); t1, t2 = "TRANSMISIÓN", "ELIMINADA"; w = int(max(fs.getlength(t1), fs.getlength(t2))) + 80; h = 200
st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
d.rounded_rectangle((6, 6, w - 7, h - 7), 18, fill=(0, 0, 0, 160), outline=(235, 25, 25, 255), width=10)
d.text((w // 2, 66), t1, font=fs, anchor="mm", fill=(235, 25, 25, 255)); d.text((w // 2, 138), t2, font=fs, anchor="mm", fill=(235, 25, 25, 255))
st = st.rotate(-7, expand=True, resample=Image.BICUBIC); sombra(st, 8, 140).save(O / "eliminado.png")
# ---------- DEUTERONOMIO 8:18 ----------
tx = "DEUTERONOMIO 8:18"; s = 70; fsm = pf(s)
while fsm.getlength(tx) > 600: s -= 2; fsm = pf(s)
w = int(fsm.getlength(tx)) + 70
sm = Image.new("RGBA", (w, 130), (0, 0, 0, 0)); d = ImageDraw.Draw(sm)
d.rounded_rectangle((4, 4, w - 5, 125), 24, fill=(0, 0, 0, 175), outline=(255, 214, 0, 255), width=5)
d.text((w // 2, 68), tx, font=fsm, anchor="mm", fill=(255, 214, 0, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
sombra(sm, 8, 150).save(O / "deut.png")
V4 = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\ov")
for n in ("en_vivo.png", "toca.png", "seta.png"): shutil.copy(V4 / n, O / n)
shutil.copy(Path(r"C:\Users\PICHAU\Downloads\SB-ES_PADRE-CAPTURADO\corpo\_trab\ov\selo10.png"), O / "selo10.png")
# prévia: câmera com faixa + rodapé | Juan com moldura | original
b = Image.open(P / "ref" / "o_3.5.png").convert("RGBA"); b.alpha_composite(Image.open(O / "rodape.png")); b.alpha_composite(Image.open(O / "faixa.png")); b.alpha_composite(Image.open(O / "selo10.png"))
a = av.convert("RGBA"); a.alpha_composite(Image.open(O / "moldura_jm.png")); a.alpha_composite(Image.open(O / "deut.png"), (360 - w // 2, 300))
c = Image.new("RGB", (2160, 1280)); c.paste(b.convert("RGB"), (0, 0)); c.paste(a.convert("RGB"), (720, 0)); c.paste(Image.open(P / "ref" / "p_25.0.png").convert("RGB"), (1440, 0))
c.resize((1620, 960)).save(P / "ref" / "ov_previa.jpg")
print("ok", lines, s)
