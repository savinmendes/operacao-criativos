# -*- coding: utf-8 -*-
"""Sobreposições do Ranking 02 (720x1280): faixa vermelha ES (cobre a PT 72-649 x 160-315), moldura da live do Juan
no layout do padre original (julio_padresf -> padre.juanmendez), TRANSMISIÓN ELIMINADA. EN VIVO / TOCA / seta / selo reaproveitados."""
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
rng = np.random.default_rng(5); W, H = 720, 1280
# ---------- faixa vermelha (papel rasgado), opaca, maior que a PT ----------
x0, x1, y0, y1 = 58, 662, 146, 330
pts = []
for x in np.linspace(x0, x1, 40): pts.append((x, y0 + rng.uniform(-5, 0)))
for y in np.linspace(y0, y1, 12): pts.append((x1 + rng.uniform(0, 6), y))
for x in np.linspace(x1, x0, 40): pts.append((x, y1 + rng.uniform(0, 6)))
for y in np.linspace(y1, y0, 12): pts.append((x0 + rng.uniform(-6, 0), y))
ban = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ban); d.polygon(pts, fill=(205, 12, 16, 255))
arr = np.asarray(ban).astype(np.int16); noise = rng.normal(0, 6, arr.shape[:2]).astype(np.int16)
for k in range(3): arr[..., k] = np.clip(arr[..., k] + noise * (arr[..., 3] > 0), 0, 255)
ban = Image.fromarray(arr.astype(np.uint8), "RGBA"); d = ImageDraw.Draw(ban)
L = ["MUJER ES HUMILLADA POR SU JEFE", "Y MINUTOS DESPUÉS ALGO", "IMPACTANTE SUCEDE"]
fs = 40; f = pf(fs)
while max(f.getlength(t) for t in L) > (x1 - x0 - 44): fs -= 1; f = pf(fs)
for k, t in enumerate(L):
    d.text((360, 188 + k * 52), t, font=f, anchor="mm", fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(60, 0, 0, 255))
sombra(ban, 5, 120, 3).save(O / "faixa.png")
# ---------- moldura da live (layout do julio_padresf, nome padre.juanmendez) ----------
REF = np.asarray(Image.open(P / "avatar" / "o_40.5.png").convert("RGB")).astype(np.float32)
mol = np.zeros((H, W, 4), np.float32)
yy, xx = np.mgrid[0:H, 0:W]; CX, CY = 101.0, 88.0; dd = np.sqrt((xx - CX) ** 2 + (yy - CY) ** 2)
av = Image.open(P / "avatar" / "jm_a.png").convert("RGB")
fc = np.asarray(av.crop((222, 168, 412, 358)).resize((84, 84), Image.LANCZOS)).astype(np.float32)
ph = np.zeros((H, W, 3), np.float32); ph[int(CY) - 42:int(CY) + 42, int(CX) - 42:int(CX) + 42] = fc
a_ph = np.clip(41.5 - dd, 0, 1); mol[..., :3] = ph * a_ph[..., None]; mol[..., 3] = a_ph
a_ring = np.clip(dd - 41.5, 0, 1) * np.clip(47.0 - dd, 0, 1)
mol[..., :3] = mol[..., :3] * (1 - a_ring[..., None]) + REF * a_ring[..., None]; mol[..., 3] = np.maximum(mol[..., 3], a_ring)
def copia_rr(box, r=5):
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle(box, r, fill=255); m = np.asarray(m, np.float32) / 255
    mol[..., :3] = mol[..., :3] * (1 - m[..., None]) + REF * m[..., None]; mol[..., 3] = np.maximum(mol[..., 3], m)
copia_rr((84, 122, 120, 137), 4)          # etiqueta LIVE sob o círculo
copia_rr((520, 62, 586, 112), 4)          # LIVE
copia_rr((595, 63, 661, 112), 5)          # olho + contagem
fo = ImageFont.truetype(OS, 68)
nm = Image.new("RGBA", (W * 2, 140), (0, 0, 0, 0)); ImageDraw.Draw(nm).text((350, 70), "padre.juanmendez", font=fo, anchor="lm", fill=(255, 255, 255, 255))
nm = nm.resize((W, 70), Image.LANCZOS); nma = np.zeros((H, W, 4), np.float32); nma[53:123] = np.asarray(nm, np.float32)
xfim = 175 + ImageFont.truetype(OS, 34).getlength("padre.juanmendez")
sh = cv2.GaussianBlur(nma[..., 3], (0, 0), 2.0) / 255 * 0.45
mol[..., :3] *= (1 - sh[..., None]); mol[..., 3] = np.maximum(mol[..., 3], sh)
ta = nma[..., 3] / 255; mol[..., :3] = mol[..., :3] * (1 - ta[..., None]) + 255 * ta[..., None]; mol[..., 3] = np.maximum(mol[..., 3], ta)
bx, by = int(xfim + 16), 89
yb, xb = np.mgrid[0:26, 0:26]; ba = np.clip(11.5 - np.sqrt((yb - 12.5) ** 2 + (xb - 12.5) ** 2), 0, 1)
bm = np.zeros((H, W), np.float32); bm[by - 13:by + 13, bx - 13:bx + 13] = ba
bc = np.zeros((H, W, 3), np.float32); bc[by - 13:by + 13, bx - 13:bx + 13] = REF[89 - 13:89 + 13, 387 - 13:387 + 13]
mol[..., :3] = mol[..., :3] * (1 - bm[..., None]) + bc * bm[..., None]; mol[..., 3] = np.maximum(mol[..., 3], bm)
# barra de comentário + reticências + coração + avião (como no original)
bb = Image.new("L", (W * 2, H * 2), 0); db = ImageDraw.Draw(bb)
db.rounded_rectangle((32, 2320, 1140, 2470), 75, outline=255, width=5)
for x in (1032, 1054, 1076): db.ellipse((x - 5, 2389, x + 5, 2399), fill=255)
tt = np.linspace(0, 2 * np.pi, 200); hx = 16 * np.sin(tt) ** 3; hy = -(13 * np.cos(tt) - 5 * np.cos(2 * tt) - 2 * np.cos(3 * tt) - np.cos(4 * tt))
db.line([(1234 + 2.9 * a, 2388 + 2.9 * b) for a, b in zip(hx, hy)], fill=255, width=5, joint="curve")
db.line([(1306, 2356), (1406, 2356), (1354, 2440), (1342, 2392), (1306, 2356)], fill=255, width=5, joint="curve")
db.line([(1342, 2392), (1406, 2356)], fill=255, width=4)
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
V4 = Path(r"C:\Users\PICHAU\Downloads\VIDEO-04-ADAPTAR_analise\producao\ov")
for n in ("en_vivo.png", "toca.png", "seta.png"): shutil.copy(V4 / n, O / n)
shutil.copy(Path(r"C:\Users\PICHAU\Downloads\SB-ES_PADRE-CAPTURADO\corpo\_trab\ov\selo10.png"), O / "selo10.png")
# prévia: briga com faixa + Juan com moldura
import subprocess
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "2.5", "-i", str(P.parents[1] / "02_331k_DR0OM-REWzS.mp4"), "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
b = Image.fromarray(np.frombuffer(raw, np.uint8).reshape(H, W, 3)).convert("RGBA"); b.alpha_composite(Image.open(O / "faixa.png")); b.alpha_composite(Image.open(O / "selo10.png"))
a = av.convert("RGBA"); a.alpha_composite(Image.open(O / "moldura_jm.png"))
c = Image.new("RGB", (1440, 1280)); c.paste(b.convert("RGB"), (0, 0)); c.paste(a.convert("RGB"), (720, 0)); c.resize((1080, 960)).save(P / "ref" / "ov_previa.jpg")
print("ok", fs if isinstance(fs, int) else "")
