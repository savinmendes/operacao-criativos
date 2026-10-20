# -*- coding: utf-8 -*-
"""PNGs 720x1280 dos ganchos G2/G4: moldura de live (estilo v4, arroba nova), título G2, cartão TRANSMISIÓN INTERRUMPIDA, mão (borrão escuro)."""
import shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W = Path(__file__).resolve().parent; O = W / "overlays"; O.mkdir(exist_ok=True)
OS = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
POP = Path(r"C:\Users\PICHAU\Downloads\SB-REEL-MEDALLA-ES\_trabalho\fonts")
def os_(sz, peso="SemiBold"):
    f = ImageFont.truetype(OS, sz); f.set_variation_by_name(peso); return f
def pop(sz, n="Bold"): return ImageFont.truetype(str(POP / f"Poppins-{n}.ttf"), sz)
shutil.copy(r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\visual\overlays\selo_ficticio_mini_es.png", O / "selo.png")
S = 3  # supersampling
def grad(w, h, c0, c1):
    g = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(g)
    for x in range(w):
        t = x / max(1, w - 1); d.line([(x, 0), (x, h)], fill=tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3)) + (255,))
    return g
def pill(w, h, r, fill_img):
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); out.paste(fill_img, (0, 0), m); return out
# ---------- moldura da live ----------
im = Image.new("RGBA", (720 * S, 1280 * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
# sombra leve no topo para legibilidade
sh = Image.new("RGBA", (720 * S, 170 * S), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
for y in range(170 * S): ds.line([(0, y), (720 * S, y)], fill=(0, 0, 0, int(95 * (1 - y / (170 * S)))))
im.alpha_composite(sh, (0, 0))
# avatar redondo com anel gradiente
cx, cy, R = 90 * S, 62 * S, 50 * S
anel = grad(2 * R, 2 * R, (255, 170, 40), (190, 30, 200)); m = Image.new("L", (2 * R, 2 * R), 0); ImageDraw.Draw(m).ellipse([0, 0, 2 * R - 1, 2 * R - 1], fill=255)
ring = Image.new("RGBA", (2 * R, 2 * R), (0, 0, 0, 0)); ring.paste(anel, (0, 0), m); im.alpha_composite(ring, (cx - R, cy - R))
r2 = R - 4 * S; foto = Image.open(W / "img" / "g4_b.png").convert("RGBA").crop((190, 120, 530, 460)).resize((2 * r2, 2 * r2), Image.LANCZOS)
m2 = Image.new("L", (2 * r2, 2 * r2), 0); ImageDraw.Draw(m2).ellipse([0, 0, 2 * r2 - 1, 2 * r2 - 1], fill=255)
im.paste(foto, (cx - r2, cy - r2), m2)
# selo EN VIVO sob o avatar
f = pop(13 * S, "Bold"); t = "EN VIVO"; b = d.textbbox((0, 0), t, font=f); w, h = b[2] - b[0] + 16 * S, 19 * S
p = pill(w, h, 4 * S, grad(w, h, (238, 40, 90), (200, 30, 190))); im.alpha_composite(p, (cx - w // 2, 104 * S))
d.text((cx, 104 * S + h // 2), t, font=f, anchor="mm", fill="white")
# arroba + verificado
f = os_(26 * S, "SemiBold"); arroba = "padre.joel_"
d.text((186 * S, 80 * S), arroba, font=f, anchor="ls", fill=(255, 255, 255, 255))
xa = 186 * S + d.textlength(arroba, font=f) + 16 * S
d.ellipse([xa - 9 * S, 62 * S - 9 * S, xa + 9 * S, 62 * S + 9 * S], fill=(56, 151, 240, 255))
d.line([(xa - 4 * S, 62 * S), (xa - 1 * S, 65 * S), (xa + 5 * S, 58 * S)], fill="white", width=2 * S)
# badges à direita: 🔴 EN VIVO + olho com contador
f = pop(12 * S, "SemiBold"); t = "EN VIVO"; w, h = 70 * S, 28 * S
p = pill(w, h, 4 * S, grad(w, h, (240, 40, 80), (190, 30, 200))); x0 = 560 * S; im.alpha_composite(p, (x0, 59 * S))
d.ellipse([x0 + 8 * S, 59 * S + 10 * S, x0 + 16 * S, 59 * S + 18 * S], fill="white")
d.text((x0 + 42 * S, 59 * S + h // 2), t, font=f, anchor="mm", fill="white")
x1 = x0 + w + 4 * S; w2 = 66 * S
d.rounded_rectangle([x1, 59 * S, x1 + w2, 59 * S + h], 4 * S, fill=(20, 20, 20, 200))
d.ellipse([x1 + 8 * S, 68 * S, x1 + 22 * S, 78 * S], outline="white", width=2 * S); d.ellipse([x1 + 13 * S, 71 * S, x1 + 17 * S, 75 * S], fill="white")
d.text((x1 + 44 * S, 59 * S + h // 2), "2,4 mil", font=pop(10 * S, "Medium"), anchor="mm", fill="white")
im.resize((720, 1280), Image.LANCZOS).save(O / "moldura_live.png")
# ---------- título G2 ----------
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
f = os_(50, "Bold"); t = "SU ÚLTIMO VIDEO"; L = d.textlength(t, font=f)
d.rounded_rectangle([360 - L / 2 - 28, 30, 360 + L / 2 + 28, 108], 14, fill=(0, 0, 0, 235))
d.text((360, 89), t, font=f, anchor="ms", fill=(244, 230, 20, 255))
im.save(O / "titulo_g2.png")
# ---------- cartão TRANSMISIÓN INTERRUMPIDA ----------
im = Image.new("RGBA", (720, 1280), (6, 6, 8, 255)); d = ImageDraw.Draw(im)
# ícone: sinal cortado
cx, cy = 360, 520
for i, r in enumerate((90, 62, 34)):
    d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=(200, 200, 200, 255), width=12)
d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(200, 200, 200, 255))
d.line([(cx - 95, cy - 100), (cx + 95, cy + 40)], fill=(230, 40, 40, 255), width=14)
f = os_(52, "Bold")
d.text((360, 700), "TRANSMISIÓN", font=f, anchor="ms", fill=(255, 255, 255, 255))
d.text((360, 766), "INTERRUMPIDA", font=f, anchor="ms", fill=(255, 255, 255, 255))
d.text((360, 830), "Se perdió la conexión con el anfitrión", font=os_(28, "Regular"), anchor="ms", fill=(170, 170, 170, 255))
im.save(O / "interrompida.png")
# ---------- mão (silhueta escura borrada que passa na frente da lente) ----------
im = Image.new("RGBA", (900, 1500), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
d.ellipse([150, 250, 800, 1150], fill=(35, 22, 16, 250)); d.rounded_rectangle([420, 700, 900, 1500], 120, fill=(30, 20, 14, 250))
for k in range(4): d.rounded_rectangle([110 + k * 30, 320 + k * 170, 470, 440 + k * 170], 60, fill=(48, 30, 22, 250))
im.filter(ImageFilter.GaussianBlur(38)).save(O / "mao.png")
print("ok")
