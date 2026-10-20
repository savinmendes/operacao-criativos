# -*- coding: utf-8 -*-
"""Overlays Black Friday do kit Yara (720x1280). Gratis, local (PIL).
Saidas em preprod/: banner_topo.png, sticker_kit.png, selo_bf.png, cta_final.png, preview_overlays.jpg"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import subprocess

OUT = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod")
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
PB, PS, PM, AN = (str(KIT / f) for f in ("Poppins-Bold.ttf", "Poppins-SemiBold.ttf", "Poppins-Medium.ttf", "Anton-Regular.ttf"))
F = lambda p, s: ImageFont.truetype(p, s)
PRETO = (10, 10, 10, 255)
OURO = (232, 186, 74, 255)
OURO2 = (255, 214, 0, 255)  # amarelo da legenda
BRANCO = (255, 255, 255, 255)
SS = 3  # supersampling


def caminhao(d, x, y, s, cor):
    """caminhao de entrega desenhado (s = largura)"""
    k = s / 100
    d.rounded_rectangle((x, y, x + 60 * k, y + 40 * k), 4 * k, fill=cor)              # bau
    d.polygon([(x + 63 * k, y + 12 * k), (x + 85 * k, y + 12 * k), (x + 99 * k, y + 26 * k),
               (x + 99 * k, y + 40 * k), (x + 63 * k, y + 40 * k)], fill=cor)          # cabine
    d.polygon([(x + 68 * k, y + 16 * k), (x + 83 * k, y + 16 * k), (x + 92 * k, y + 26 * k),
               (x + 68 * k, y + 26 * k)], fill=PRETO)                                   # janela
    for cx in (x + 18 * k, x + 80 * k):
        d.ellipse((cx - 10 * k, y + 32 * k, cx + 10 * k, y + 52 * k), fill=PRETO, outline=cor, width=int(4 * k))
    for i, ln in enumerate((10, 22, 14)):                                                # linhas de velocidade
        d.rounded_rectangle((x - (ln + 8) * k, y + (8 + 11 * i) * k, x - 6 * k, y + (12 + 11 * i) * k), 2 * k, fill=cor)


def banner_topo():
    w, h = 470, 92
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), 16 * SS, fill=PRETO, outline=OURO, width=3 * SS)
    # selo BLACK FRIDAY (dourado) a esquerda
    d.rounded_rectangle((8 * SS, 8 * SS, 132 * SS, (h - 8) * SS), 10 * SS, fill=OURO)
    for i, t in enumerate(("BLACK", "FRIDAY")):
        f = F(AN, 31 * SS)
        tw = d.textlength(t, font=f)
        d.text(((70 * SS) - tw / 2, (11 + i * 35) * SS), t, font=f, fill=PRETO)
    # textos
    d.text((146 * SS, 14 * SS), "PAGO CONTRA ENTREGA", font=F(PB, 22 * SS), fill=BRANCO)
    d.text((146 * SS, 46 * SS), "ENVÍO GRATIS", font=F(PB, 24 * SS), fill=OURO2)
    caminhao(d, 368 * SS, 50 * SS, 84 * SS, OURO)
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / "banner_topo.png")
    return im


def sticker():
    rc = Image.open(OUT / "_trabalho" / "recorte_u2net.png").convert("RGBA")
    a = rc.split()[3].point(lambda v: 0 if v < 40 else (255 if v > 215 else v))
    rc.putalpha(a)
    rc = rc.crop(rc.getbbox())
    # sombra suave + escala para ~420 px de largura (rodape, igual ao vencedor)
    alvo_w = 420
    rc = rc.resize((alvo_w, int(rc.height * alvo_w / rc.width)), Image.LANCZOS)
    pad = 14
    base = Image.new("RGBA", (rc.width + 2 * pad, rc.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh.paste((0, 0, 0, 150), (pad + 3, pad + 5), rc.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    base = Image.alpha_composite(base, sh)
    base.alpha_composite(rc, (pad, pad))
    base.save(OUT / "sticker_kit.png")
    return base


def selo():
    s = 250
    im = Image.new("RGBA", (s * SS, s * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    S = s * SS
    d.ellipse((0, 0, S - 1, S - 1), fill=OURO)
    d.ellipse((7 * SS, 7 * SS, S - 7 * SS, S - 7 * SS), fill=PRETO)
    d.ellipse((14 * SS, 14 * SS, S - 14 * SS, S - 14 * SS), outline=OURO, width=2 * SS)

    def centro(t, f, y, cor):
        tw = d.textlength(t, font=f)
        d.text(((S - tw) / 2, y * SS), t, font=f, fill=cor)
    centro("BLACK", F(AN, 44 * SS), 34, OURO)
    centro("FRIDAY", F(AN, 44 * SS), 80, OURO)
    d.rectangle((52 * SS, 136 * SS, (s - 52) * SS, 138 * SS), fill=OURO)
    centro("KIT 3 PERFUMES", F(PB, 19 * SS), 144, BRANCO)
    centro("$59.900", F(PB, 38 * SS), 166, OURO2)
    im = im.resize((s, s), Image.LANCZOS)
    im.save(OUT / "selo_bf.png")
    return im


def cta_final(stk):
    W, H = 720, 1280
    im = Image.new("RGBA", (W, H), PRETO)
    # fundo: preto com brilho dourado radial no centro
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((60, 370, 660, 970), fill=(232, 186, 74, 110))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    im = Image.alpha_composite(im, glow)
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, W - 25, H - 25), outline=OURO, width=3)

    def centro(t, f, y, cor):
        tw = d.textlength(t, font=f)
        d.text(((W - tw) / 2, y), t, font=f, fill=cor)
    centro("BLACK FRIDAY", F(AN, 120), 110, OURO)
    centro("KIT 3 PERFUMES ÁRABES LATTAFA", F(PS, 30), 265, BRANCO)
    # packshot grande
    rc = Image.open(OUT / "_trabalho" / "recorte_u2net.png").convert("RGBA")
    a = rc.split()[3].point(lambda v: 0 if v < 40 else (255 if v > 215 else v)); rc.putalpha(a)
    rc = rc.crop(rc.getbbox())
    pw = 640
    rc = rc.resize((pw, int(rc.height * pw / rc.width)), Image.LANCZOS)
    im.alpha_composite(rc, ((W - pw) // 2, 340))
    y = 340 + rc.height + 24
    d = ImageDraw.Draw(im)
    centro("Yara · Yara Moi · Yara Elixir", F(PB, 38), y, BRANCO)
    centro("100 ml cada uno", F(PM, 28), y + 54, (210, 210, 210, 255))
    # preco
    f = F(AN, 150)
    centro("$59.900", f, y + 104, OURO2)
    # faixa inferior
    fy = y + 300
    d.rounded_rectangle((60, fy, W - 60, fy + 120), 22, fill=OURO)
    centro("Pagas al recibir", F(PB, 42), fy + 10, PRETO)
    centro("Envío gratis", F(PB, 42), fy + 62, PRETO)
    im.convert("RGB").save(OUT / "cta_final.png")
    return im, fy + 120


def preview(ban, stk, sel, cta):
    q = OUT / "_trabalho" / "quadro_venc.jpg"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "20", "-i",
                    r"C:\Users\PICHAU\Downloads\YARA-CL\_ref\venc_122121238455420219.mp4", "-frames:v", "1", str(q)], check=True)
    fr = Image.open(q).convert("RGBA").resize((720, 1280))
    # cobre banner/sticker antigos do vencedor so para o preview ficar legivel
    d = ImageDraw.Draw(fr)
    fr.alpha_composite(ban, (16, 16))
    fr.alpha_composite(stk, ((720 - stk.width) // 2, 1280 - stk.height - 70))
    fr.alpha_composite(sel, (720 - sel.width - 16, 140))
    # amostra de legenda (estilo kit: branco, contorno preto, 1 palavra amarela)
    f = F(PB, 71)
    t1, t2 = "YARA ", "ELIXIR"
    x = (720 - d.textlength(t1 + t2, font=f)) / 2
    d.text((x, 670), t1, font=f, fill=BRANCO, stroke_width=6, stroke_fill=PRETO)
    d.text((x + d.textlength(t1, font=f), 670), t2, font=f, fill=OURO2, stroke_width=6, stroke_fill=PRETO)
    sheet = Image.new("RGB", (1460, 1280), (40, 40, 40))
    sheet.paste(fr.convert("RGB"), (0, 0))
    sheet.paste(cta.convert("RGB"), (740, 0))
    sheet.save(OUT / "preview_overlays.jpg", quality=90)


if __name__ == "__main__":
    b = banner_topo(); s = sticker(); se = selo(); c, fim = cta_final(s)
    print("banner", b.size, "sticker", s.size, "selo", se.size, "cta fim y", fim)
    preview(b, s, se, c)
