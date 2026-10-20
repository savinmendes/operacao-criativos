# -*- coding: utf-8 -*-
"""Overlays Black Friday SEM PRECO (oferta paga 2 lleva 3) do kit Yara, 720x1280. Local (PIL), sem custo.
Base: preprod/_trabalho/gerar_overlays.py (mesma identidade preto + dourado).
Saidas em producao/edicao/: selo_bf.png, titulo_abertura.png, cta_final.png, banner_topo.png, sticker_kit.png,
preview_overlays.jpg"""
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PRE = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod")
OUT = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\producao\edicao")
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
PB, PS, PM, AN = (str(KIT / f) for f in ("Poppins-Bold.ttf", "Poppins-SemiBold.ttf", "Poppins-Medium.ttf", "Anton-Regular.ttf"))
F = lambda p, s: ImageFont.truetype(p, s)
PRETO = (10, 10, 10, 255)
OURO = (232, 186, 74, 255)
OURO2 = (255, 214, 0, 255)
BRANCO = (255, 255, 255, 255)
VERM = (214, 24, 32, 255)
SS = 3
W, H = 720, 1280


def recorte():
    rc = Image.open(PRE / "_trabalho" / "recorte_u2net.png").convert("RGBA")
    a = rc.split()[3].point(lambda v: 0 if v < 40 else (255 if v > 215 else v))
    rc.putalpha(a)
    return rc.crop(rc.getbbox())


def centro(d, t, f, y, cor, cx, **kw):
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, y), t, font=f, fill=cor, **kw)


def selo():
    s = 250
    S = s * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((0, 0, S - 1, S - 1), fill=OURO)
    d.ellipse((7 * SS, 7 * SS, S - 7 * SS, S - 7 * SS), fill=PRETO)
    d.ellipse((14 * SS, 14 * SS, S - 14 * SS, S - 14 * SS), outline=OURO, width=2 * SS)
    centro(d, "BLACK", F(AN, 44 * SS), 30 * SS, OURO, S / 2)
    centro(d, "FRIDAY", F(AN, 44 * SS), 76 * SS, OURO, S / 2)
    d.rectangle((52 * SS, 134 * SS, (s - 52) * SS, 136 * SS), fill=OURO)
    centro(d, "PAGA 2", F(AN, 36 * SS), 140 * SS, OURO2, S / 2)
    centro(d, "LLEVA 3", F(AN, 36 * SS), 182 * SS, BRANCO, S / 2)
    im = im.resize((s, s), Image.LANCZOS)
    im.save(OUT / "selo_bf.png")
    return im


def faixa_texto(texto, fonte, px, cor_txt, cor_fundo, padx=26, pady=10, angulo=0, contorno=None):
    """faixa (retangulo) com texto, em supersampling, opcionalmente girada"""
    f = F(fonte, px * SS)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), texto, font=f)
    w, h = r - l + 2 * padx * SS, b - t + 2 * pady * SS
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if cor_fundo:
        d.rectangle((0, 0, w - 1, h - 1), fill=cor_fundo)
        if contorno:
            d.rectangle((0, 0, w - 1, h - 1), outline=contorno, width=4 * SS)
    d.text((padx * SS - l, pady * SS - t), texto, font=f, fill=cor_txt)
    if angulo:
        im = im.rotate(angulo, resample=Image.BICUBIC, expand=True)
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def texto_contorno(texto, fonte, px, cor, contorno=PRETO, sw=8, angulo=0):
    f = F(fonte, px * SS)
    tmp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), texto, font=f, stroke_width=sw * SS)
    im = Image.new("RGBA", (r - l + 20 * SS, b - t + 20 * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # sombra
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((10 * SS - l + 4 * SS, 10 * SS - t + 6 * SS), texto, font=f, fill=(0, 0, 0, 170),
                            stroke_width=sw * SS, stroke_fill=(0, 0, 0, 170))
    sh = sh.filter(ImageFilter.GaussianBlur(4 * SS))
    im = Image.alpha_composite(im, sh)
    d = ImageDraw.Draw(im)
    d.text((10 * SS - l, 10 * SS - t), texto, font=f, fill=cor, stroke_width=sw * SS, stroke_fill=contorno)
    if angulo:
        im = im.rotate(angulo, resample=Image.BICUBIC, expand=True)
    return im.resize((im.width // SS, im.height // SS), Image.LANCZOS)


def titulo_abertura():
    """Titulo grande dos 1,5 s iniciais. Rosto da consultora fica em y ~0,25-0,45 (320-576 px):
    BLACK FRIDAY acima (y<=300), PAGA 2 LLEVA 3 + LIQUIDACION abaixo (y>=620)."""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # bloco de cima: faixa preta com borda dourada, levemente inclinada
    bf = faixa_texto("BLACK FRIDAY", AN, 118, OURO, PRETO, padx=22, pady=8, angulo=3, contorno=OURO)
    bf = bf.resize((min(bf.width, 690), int(bf.height * min(bf.width, 690) / bf.width)), Image.LANCZOS)
    im.alpha_composite(bf, ((W - bf.width) // 2, 70))
    # bloco de baixo
    p2 = texto_contorno("PAGA 2", AN, 132, BRANCO, sw=9, angulo=-3)
    l3 = texto_contorno("LLEVA 3", AN, 150, OURO2, sw=10, angulo=-3)
    im.alpha_composite(p2, ((W - p2.width) // 2, 625))
    im.alpha_composite(l3, ((W - l3.width) // 2, 625 + p2.height - 40))
    lq = faixa_texto("LIQUIDACIÓN", AN, 64, BRANCO, VERM, padx=22, pady=6, angulo=-3)
    y_lq = 625 + p2.height - 40 + l3.height - 20
    im.alpha_composite(lq, ((W - lq.width) // 2, y_lq))
    print("titulo: BF ate y", 70 + bf.height, "| bloco de baixo", 625, "->", y_lq + lq.height)
    im.save(OUT / "titulo_abertura.png")
    return im


def cta_final():
    im = Image.new("RGBA", (W, H), PRETO)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((60, 420, 660, 1020), fill=(232, 186, 74, 110))
    im = Image.alpha_composite(im, glow.filter(ImageFilter.GaussianBlur(120)))
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, W - 25, H - 25), outline=OURO, width=3)
    centro(d, "BLACK FRIDAY", F(AN, 120), 165, OURO, W / 2)
    lq = faixa_texto("LIQUIDACIÓN", AN, 46, BRANCO, VERM, padx=18, pady=4)
    im.alpha_composite(lq, ((W - lq.width) // 2, 325))
    rc = recorte()
    pw = 620
    rc = rc.resize((pw, int(rc.height * pw / rc.width)), Image.LANCZOS)
    y0 = 415
    im.alpha_composite(rc, ((W - pw) // 2, y0))
    y = y0 + rc.height + 18
    d = ImageDraw.Draw(im)
    centro(d, "Yara · Yara Moi · Yara Elixir", F(PB, 38), y, BRANCO, W / 2)
    t = texto_contorno("Paga 2 · Lleva 3", AN, 104, OURO2, sw=0)
    im.alpha_composite(t, ((W - t.width) // 2, y + 56))
    fy = y + 56 + t.height + 14
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((50, fy, W - 50, fy + 76), 22, fill=OURO)
    centro(d, "Pagas al recibir · Envío gratis", F(PB, 34), fy + 16, PRETO, W / 2)
    print("cta: faixa termina em y", fy + 76)
    im.convert("RGB").save(OUT / "cta_final.png")
    return im


def preview(ban, stk, sel, tit, cta):
    q = Image.open(r"C:\Users\PICHAU\Downloads\YARA-CL\teste\cena_v1_prev.jpg").convert("RGBA").resize((W, H))
    a = q.copy()
    a.alpha_composite(tit)
    # guia do rosto (0,25-0,45) so no preview
    g = ImageDraw.Draw(a)
    g.rectangle((250, 320, 470, 576), outline=(0, 255, 0, 255), width=2)
    b = q.copy()
    b.alpha_composite(ban, (16, 16))
    b.alpha_composite(sel, (W - sel.width - 16, 130))
    b.alpha_composite(stk, ((W - stk.width) // 2, H - stk.height - 40))
    sheet = Image.new("RGB", (3 * W + 40, H), (40, 40, 40))
    sheet.paste(a.convert("RGB"), (0, 0))
    sheet.paste(b.convert("RGB"), (W + 20, 0))
    sheet.paste(cta.convert("RGB"), (2 * W + 40, 0))
    sheet.save(OUT / "preview_overlays.jpg", quality=88)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for n in ("banner_topo.png", "sticker_kit.png"):
        shutil.copy2(PRE / n, OUT / n)
    ban = Image.open(OUT / "banner_topo.png").convert("RGBA")
    stk = Image.open(OUT / "sticker_kit.png").convert("RGBA")
    preview(ban, stk, selo(), titulo_abertura(), cta_final())
