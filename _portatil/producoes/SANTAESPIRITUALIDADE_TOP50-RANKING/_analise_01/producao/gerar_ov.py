# -*- coding: utf-8 -*-
"""Sobreposições do Ranking 01 (720x1280): faixa vermelha ES, rodapé de telejornal ES (logo inventado), moldura da live do Juan
no layout do original do frade, TRANSMISIÓN ELIMINADA, SALMO 112:3. EN VIVO / TOCA / seta / selo vêm dos lotes anteriores."""
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
rng = np.random.default_rng(3)
# ---------- faixa vermelha (papel rasgado) ----------
W, H = 720, 1280
x0, x1, y0, y1 = 66, 654, 138, 312
pts = []
for x in np.linspace(x0, x1, 40): pts.append((x, y0 + rng.uniform(-5, 5)))
for y in np.linspace(y0, y1, 12): pts.append((x1 + rng.uniform(-6, 6), y))
for x in np.linspace(x1, x0, 40): pts.append((x, y1 + rng.uniform(-6, 6)))
for y in np.linspace(y1, y0, 12): pts.append((x0 + rng.uniform(-6, 6), y))
ban = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ban)
d.polygon(pts, fill=(205, 12, 16, 255))
# textura leve
arr = np.asarray(ban).astype(np.int16); noise = rng.normal(0, 6, arr.shape[:2]).astype(np.int16)
for k in range(3): arr[..., k] = np.clip(arr[..., k] + noise * (arr[..., 3] > 0), 0, 255)
ban = Image.fromarray(arr.astype(np.uint8), "RGBA"); d = ImageDraw.Draw(ban)
L = ["HOMBRE REZA LA ORACIÓN", "DE SAN BENITO Y ALGO", "IMPACTANTE SUCEDE"]
fs = 36; f = pf(fs)
while max(f.getlength(t) for t in L) > (x1 - x0 - 40): fs -= 1; f = pf(fs)
for k, t in enumerate(L):
    d.text((360, 176 + k * 49), t, font=f, anchor="mm", fill=(255, 226, 0, 255), stroke_width=3, stroke_fill=(70, 0, 0, 255))
sombra(ban, 5, 120, 3).save(O / "faixa.png")
# ---------- rodapé telejornal ----------
rod = np.zeros((H, W, 4), np.float32)
for y in range(955, H):
    c = (0, 49, 172) if y < 1120 else (7, 53, 146)
    a = 1.0 if y >= 980 else (y - 955) / 25
    rod[y, :, :3] = c; rod[y, :, 3] = a
rod = Image.fromarray(np.clip(rod * [1, 1, 1, 255], 0, 255).astype(np.uint8), "RGBA"); d = ImageDraw.Draw(rod)
# logo inventado "NV" (prata, como o JG do original) + "NOTIVISIÓN"
lg = Image.new("RGBA", (240, 160), (0, 0, 0, 0)); dl = ImageDraw.Draw(lg)
dl.text((120, 66), "NV", font=pf(104), anchor="mm", fill=(255, 255, 255, 255))
grad = np.linspace(255, 175, 160)[:, None] * np.ones((160, 240)); la = np.asarray(lg).astype(np.float32)
for k in range(3): la[..., k] = np.minimum(la[..., k], grad)
lg = Image.fromarray(la.astype(np.uint8), "RGBA"); dl = ImageDraw.Draw(lg)
dl.text((120, 136), "NOTIVISIÓN", font=pf(22, "Bold"), anchor="mm", fill=(255, 255, 255, 235))
rod.alpha_composite(sombra(lg, 4, 110, 2), (45, 1018))
d.line((278, 992, 278, 1242), fill=(255, 255, 255, 255), width=3)
txt = "DUEÑO DE RESTAURANTE REZA LA ORACIÓN DE SAN BENITO Y MINUTOS DESPUÉS SU LOCAL SE LLENA DE CLIENTES"
fr = pf(25, "Bold"); lines = []; cur = ""
for w in txt.split():
    t = (cur + " " + w).strip()
    if fr.getlength(t) > 395: lines.append(cur); cur = w
    else: cur = t
lines.append(cur)
yt = 1117 - (len(lines) - 1) * 33 / 2
for k, t in enumerate(lines): d.text((296, yt + k * 33), t, font=fr, anchor="lm", fill=(255, 255, 255, 255))
rod.save(O / "rodape.png")
# ---------- moldura da live (layout do frade, arroba padre.juanmendez) ----------
REF = np.asarray(Image.open(P / "ref" / "o_30.png").convert("RGB")).astype(np.float32)
mol = np.zeros((H, W, 4), np.float32)
yy, xx = np.mgrid[0:H, 0:W]; CX, CY = 85.0, 97.0; dd = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
# foto do perfil: rosto do Juan (retrato base)
av = Image.open(P / "avatar" / "jm_frade_b.png").convert("RGB"); s = 720 / av.width; av = av.resize((720, int(av.height * s)), Image.LANCZOS)
fc = np.asarray(av.crop((360 - 120, 70, 360 + 120, 310)).resize((82, 82), Image.LANCZOS)).astype(np.float32)
ph = np.zeros((H, W, 3), np.float32); ph[int(CY) - 41:int(CY) + 41, int(CX) - 41:int(CX) + 41] = fc
a_ph = np.clip(40.5 - dd, 0, 1); mol[..., :3] = ph * a_ph[..., None]; mol[..., 3] = a_ph
a_ring = np.clip(dd - 40.5, 0, 1) * np.clip(46.5 - dd, 0, 1)
mol[..., :3] = mol[..., :3] * (1 - a_ring[..., None]) + REF * a_ring[..., None]; mol[..., 3] = np.maximum(mol[..., 3], a_ring)
def copia_rr(box, r=5):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255); m = np.asarray(m, np.float32) / 255
    mol[..., :3] = mol[..., :3] * (1 - m[..., None]) + REF * m[..., None]; mol[..., 3] = np.maximum(mol[..., 3], m)
copia_rr((68, 131, 103, 145), 4)          # etiqueta LIVE sob o círculo
copia_rr((509, 71, 571, 115), 6)          # LIVE
copia_rr((581, 73, 653, 114), 6)          # olho + contagem
# selo azul de verificado (copiado do original) depois do nome
fo = ImageFont.truetype(OS, 34); fo.set_variation_by_name("Regular")
nm = Image.new("RGBA", (W * 2, 120), (0, 0, 0, 0)); ImageDraw.Draw(nm).text((290, 2 * 52), "padre.juanmendez", font=ImageFont.truetype(OS, 68), anchor="ls", fill=(255, 255, 255, 255))
nm = nm.resize((W, 60), Image.LANCZOS); nma = np.zeros((H, W, 4), np.float32); nma[50:110] = np.asarray(nm, np.float32)
xfim = 145 + ImageFont.truetype(OS, 34).getlength("padre.juanmendez")
sh = cv2.GaussianBlur(nma[..., 3], (0, 0), 2.0) / 255 * 0.45
mol[..., :3] *= (1 - sh[..., None]); mol[..., 3] = np.maximum(mol[..., 3], sh)
ta = nma[..., 3] / 255; mol[..., :3] = mol[..., :3] * (1 - ta[..., None]) + 255 * ta[..., None]; mol[..., 3] = np.maximum(mol[..., 3], ta)
bx, by = int(xfim + 22), 91
yb, xb = np.mgrid[0:24, 0:24]; ba = np.clip(10.4 - np.sqrt((yb - 11.5) ** 2 + (xb - 11.5) ** 2), 0, 1)
bm = np.zeros((H, W), np.float32); bm[by - 12:by + 12, bx - 12:bx + 12] = ba
bc = np.zeros((H, W, 3), np.float32); bc[by - 12:by + 12, bx - 12:bx + 12] = REF[91 - 12:91 + 12, 381 - 12:381 + 12]
mol[..., :3] = mol[..., :3] * (1 - bm[..., None]) + bc * bm[..., None]; mol[..., 3] = np.maximum(mol[..., 3], bm)
# barra de comentário + coração (desenhados no lugar do original: pílula 26-601 x 1180-1259, coração em 662,1220)
bb = Image.new("L", (W * 2, H * 2), 0); db = ImageDraw.Draw(bb)
db.rounded_rectangle((52, 2360, 1202, 2518), 79, outline=255, width=5)
for x in (1098, 1112 + 14, 1154): db.ellipse((x - 5, 2435, x + 5, 2445), fill=255)
tt = np.linspace(0, 2 * np.pi, 200); hx = 16 * np.sin(tt) ** 3; hy = -(13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt))
db.line([(1324 + 2.7 * a, 2436 + 2.7 * b) for a, b in zip(hx, hy)], fill=255, width=5, joint="curve")
bb = np.asarray(bb.resize((W, H), Image.LANCZOS), np.float32) / 255 * 0.92
sh = cv2.GaussianBlur(bb, (0, 0), 1.5) * 0.35
mol[..., :3] *= (1 - sh[..., None]); mol[..., 3] = np.maximum(mol[..., 3], sh)
mol[..., :3] = mol[..., :3] * (1 - bb[..., None]) + 255 * bb[..., None]; mol[..., 3] = np.maximum(mol[..., 3], bb)
o = mol.copy(); a3 = np.maximum(o[..., 3:4], 1e-6); o[..., :3] = np.where(o[..., 3:4] > 0, o[..., :3] / a3 * (o[..., 3:4] > 0), 0)
o[..., :3] = np.where(o[..., 3:4] > 0, mol[..., :3], 0)
Image.fromarray(np.dstack([np.clip(o[..., :3], 0, 255), np.clip(mol[..., 3] * 255, 0, 255)]).astype(np.uint8), "RGBA").save(O / "moldura_jm.png")
# ---------- TRANSMISIÓN ELIMINADA (carimbo) ----------
fs = pf(62); t1, t2 = "TRANSMISIÓN", "ELIMINADA"; w = int(max(fs.getlength(t1), fs.getlength(t2))) + 80; h = 200
st = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
d.rounded_rectangle((6, 6, w - 7, h - 7), 18, fill=(0, 0, 0, 160), outline=(235, 25, 25, 255), width=10)
d.text((w // 2, 66), t1, font=fs, anchor="mm", fill=(235, 25, 25, 255)); d.text((w // 2, 138), t2, font=fs, anchor="mm", fill=(235, 25, 25, 255))
st = st.rotate(-7, expand=True, resample=Image.BICUBIC); sombra(st, 8, 140).save(O / "eliminado.png")
# ---------- SALMO 112:3 ----------
fsm = pf(92); w = int(fsm.getlength("SALMO 112:3")) + 90
sm = Image.new("RGBA", (w, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(sm)
d.rounded_rectangle((4, 4, w - 5, 145), 24, fill=(0, 0, 0, 175), outline=(255, 214, 0, 255), width=5)
d.text((w // 2, 78), "SALMO 112:3", font=fsm, anchor="mm", fill=(255, 214, 0, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
sombra(sm, 8, 150).save(O / "salmo.png")
# ---------- reaproveitados ----------
V4 = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\ov")
for n in ("en_vivo.png", "toca.png", "seta.png"): shutil.copy(V4 / n, O / n)
shutil.copy(Path(r"C:\Users\PICHAU\Downloads\SB-ES_PADRE-CAPTURADO\corpo\_trab\ov\selo10.png"), O / "selo10.png")
# prévia
b = Image.open(P / "broll" / "news" / "limpo" / "f_0100.png").convert("RGBA"); b.alpha_composite(Image.open(O / "rodape.png")); b.alpha_composite(Image.open(O / "faixa.png"))
a = av.crop((0, 0, 720, 1280)).convert("RGBA") if av.height >= 1280 else av.resize((720, 1280)).convert("RGBA"); a.alpha_composite(Image.open(O / "moldura_jm.png"))
c = Image.new("RGB", (1440, 1280)); c.paste(b.convert("RGB"), (0, 0)); c.paste(a.convert("RGB"), (720, 0)); c.resize((1080, 960)).save(P / "ref" / "ov_previa.jpg")
print("ok", lines)
