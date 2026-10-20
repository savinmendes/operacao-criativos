# -*- coding: utf-8 -*-
"""Gráficos 720x1280 RGBA do TESTE1-SB-ES (PIL, sem custo): selo, moldura do post, moldura EN VIVO, CTA."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent; W, H = 720, 1280
WF = Path(r"C:\Windows\Fonts")
def P(peso, t): return ImageFont.truetype(str(AQ / f"Poppins-{peso}.ttf"), t)
def SG(n, t): return ImageFont.truetype(str(WF / n), t)
def tela(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def caber(d, txt, fn, tam, maxw):
    while d.textlength(txt, font=fn(tam)) > maxw and tam > 8: tam -= 0.5
    return fn(tam)

# ---------- selo VIDEO FICTICIO: colado no topo, só cantos de baixo arredondados
def selo():
    im = tela(); d = ImageDraw.Draw(im); f = P("Bold", 12); t = "VIDEO FICTICIO"
    b = d.textbbox((0, 0), t, font=f); w, h = b[2] - b[0], b[3] - b[1]
    px, py = 8, 4; x1 = W - 13; x0 = x1 - w - 2 * px; y0 = 0; y1 = h + 2 * py
    d.rounded_rectangle([x0, y0 - 6, x1, y1], radius=5, fill=(0, 0, 0, 179))
    im2 = tela(); im2.paste(im.crop((0, 0, W, y1 + 1)), (0, 0))  # corta a parte de cima (cantos de cima ficam retos)
    d = ImageDraw.Draw(im2); d.text((x0 + px - b[0], y0 + py - b[1]), t, font=f, fill=(255, 255, 255, 255))
    im2.save(AQ / "selo.png"); return (x0, y0, x1, y1)

# ---------- moldura do post: "Fe en Noticias" + chamada
def header():
    im = tela(); d = ImageDraw.Draw(im)
    d.rectangle([145, 146, 648, 197], fill=(251, 251, 251, 255))
    d.rectangle([145, 197, 715, 238], fill=(251, 251, 251, 255))
    ft = caber(d, "Fe en Noticias", lambda s: P("SemiBold", s), 40, 252)
    d.text((156, 186), "Fe en Noticias", font=ft, fill=(11, 11, 11, 255), anchor="ls")
    t = "Trabajador es humillado y algo impactante sucede"
    fs = caber(d, t, lambda s: P("Medium", s), 26, 520)
    d.text((153, 223), t, font=fs, fill=(22, 22, 22, 255), anchor="ls")
    im.save(AQ / "header.png")

# ---------- moldura EN VIVO (só os elementos traduzidos; o resto da moldura original fica)
def live():
    im = tela(); d = ImageDraw.Draw(im)
    rosa = (236, 45, 118, 255)
    d.rounded_rectangle([400, 60, 517, 111], radius=7, fill=rosa)
    fb = SG("seguisb.ttf", 23)
    d.text((458.5, 86), "EN VIVO", font=fb, fill=(255, 255, 255, 255), anchor="mm")
    fn = caber(d, "P. Andrés Molina", lambda s: SG("seguisb.ttf", s), 30, 212)
    nome = "P. Andrés Molina"
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((126, 92), nome, font=fn, fill=(0, 0, 0, 110), anchor="ls"); sh = sh.filter(ImageFilter.GaussianBlur(1.5))
    im.alpha_composite(sh)
    d = ImageDraw.Draw(im); d.text((126, 92), nome, font=fn, fill=(250, 250, 250, 245), anchor="ls")
    xe = 126 + d.textlength(nome, font=fn) + 10
    d.line([(xe, 80), (xe + 7, 87), (xe + 14, 80)], fill=(245, 245, 245, 235), width=2)
    fc = SG("segoeui.ttf", 19)
    d.text((63, 1198), "Comentarios desactivados", font=fc, fill=(235, 235, 235, 215), anchor="ls")
    im.save(AQ / "live_ui.png")

# ---------- CTA (estilo cta_vermas do Medalla, 720p): texto + 2 setas amarelas
AMARELO = (254, 229, 84, 255); ESC = (20, 16, 10, 255)
def seta(w, h):
    s = Image.new("RGBA", (w + 12, h + 12), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    hw = w * 0.36; cx = (w + 12) / 2; corpo = h * 0.5
    pts = [(cx - hw / 2, 6), (cx + hw / 2, 6), (cx + hw / 2, 6 + corpo), (cx + w / 2, 6 + corpo), (cx, 6 + h), (cx - w / 2, 6 + corpo), (cx - hw / 2, 6 + corpo)]
    d.polygon(pts, fill=ESC); 
    inner = [(x + (2 if x < cx else -2 if x > cx else 0), y) for x, y in pts]
    s2 = Image.new("RGBA", s.size, (0, 0, 0, 0)); d2 = ImageDraw.Draw(s2)
    k = 5; pin = [(cx - hw / 2 + k, 6 + k), (cx + hw / 2 - k, 6 + k), (cx + hw / 2 - k, 6 + corpo + k * 0.6), (cx + w / 2 - k * 2.2, 6 + corpo + k * 0.6),
                  (cx, 6 + h - k * 1.8), (cx - w / 2 + k * 2.2, 6 + corpo + k * 0.6), (cx - hw / 2 + k, 6 + corpo + k * 0.6)]
    d2.polygon(pin, fill=AMARELO)
    d2.rectangle([cx - hw / 2 + k, 6 + k, cx + hw / 2 - k, 6 + k + 14], fill=(255, 243, 160, 255))
    s.alpha_composite(s2); return s
def sombra(im, raio=6, alfa=130, desl=(0, 4)):
    a = im.split()[3].point(lambda v: v * alfa // 255); s = Image.new("RGBA", im.size, (0, 0, 0, 0)); s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(raio)); o = tela(); o.alpha_composite(s, desl); o.alpha_composite(im); return o
def cta():
    im = tela(); d = ImageDraw.Draw(im); f = P("ExtraBold", 46)
    partes = [("TOCA ", (255, 255, 255, 255)), ("«VER MÁS»", AMARELO)]
    tot = sum(d.textlength(t, font=f) for t, _ in partes); x = (W - tot) / 2; cy = 1000
    for t, c in partes:
        d.text((x, cy), t, font=f, fill=c, stroke_width=4, stroke_fill=ESC, anchor="lm"); x += d.textlength(t, font=f)
    sombra(im).save(AQ / "cta_txt.png")
    im = tela(); s = seta(96, 112)
    for cx in (250, 470): im.alpha_composite(s, (int(cx - s.size[0] / 2), 1032))
    sombra(im).save(AQ / "cta_setas.png")

if __name__ == "__main__":
    print("selo", selo()); header(); live(); cta(); print("ok")
