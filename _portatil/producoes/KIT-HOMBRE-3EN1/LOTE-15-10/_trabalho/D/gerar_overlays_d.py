# -*- coding: utf-8 -*-
"""Overlays do agente D (perfumes arabes, kit hombre 3en1, COD Chile), 720x1280, PIL local, sem custo.
Saidas em overlays/:
  banner_topo.png      selo COD fixo no topo (PAGO CONTRA ENTREGA / ENVIO EN 24 HORAS, azul-marinho + caminhao)
  sticker_kit.png      os 3 frascos recortados do n2 (rodape)
  frascos_rodape.png   tela cheia 720x1280 so com os frascos no rodape (para o CTA)
  m7_tit.png           titulo de abertura do M7 (inclui o banner)
  m7_armaf/asad/9pm.png  nome + 3 adjetivos (tela cheia)
  m7_cta.png / m6_cta.png  CTA final (banner + oferta + frascos no rodape + setas)
  m6_tit_11.png / m6_tit_12.png  titulo do gancho (inclui o banner)
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

D = Path(__file__).resolve().parent
OUT = D / "overlays"
OUT.mkdir(exist_ok=True)
FD = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts")
PB, PS, AN = (str(FD / f) for f in ("Poppins-Bold.ttf", "Poppins-SemiBold.ttf", "Anton-Regular.ttf"))
F = lambda p, s: ImageFont.truetype(p, s)
W, H = 720, 1280
NAVY = (12, 30, 66, 255)
BRANCO = (255, 255, 255, 255)
OURO = (232, 190, 92, 255)
AMA = (255, 214, 0, 255)
VERM = (230, 30, 40, 255)
SS = 3


def sombra(im, r=10, off=(0, 5), alpha=170):
    pad = 3 * r
    base = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.split()[3].point(lambda v: v * alpha // 255))
    base.alpha_composite(sh, (pad + off[0], pad + off[1]))
    base = base.filter(ImageFilter.GaussianBlur(r))
    base.alpha_composite(im, (pad, pad))
    return base, pad


def caminhao(d, x, y, s, cor):
    """caminhao simples (bau + cabine + 2 rodas), s = escala px"""
    d.rectangle((x, y, x + 3.0 * s, y + 1.8 * s), fill=cor)
    d.polygon([(x + 3.15 * s, y + 0.5 * s), (x + 4.0 * s, y + 0.5 * s), (x + 4.6 * s, y + 1.1 * s),
               (x + 4.6 * s, y + 1.8 * s), (x + 3.15 * s, y + 1.8 * s)], fill=cor)
    for cx in (x + 0.8 * s, x + 3.7 * s):
        d.ellipse((cx - 0.45 * s, y + 1.6 * s, cx + 0.45 * s, y + 2.5 * s), fill=cor)
    for k in range(3):  # tracos de velocidade
        yy = y + (0.3 + 0.55 * k) * s
        d.line((x - (1.6 - 0.3 * k) * s, yy, x - 0.3 * s, yy), fill=cor, width=max(2, int(0.18 * s)))


def banner():
    w, h = 478, 86
    im = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w * SS - 1, h * SS - 1), 14 * SS, fill=NAVY, outline=(255, 255, 255, 230), width=2 * SS)
    d.text((22 * SS, 10 * SS), "PAGO CONTRA ENTREGA", font=F(PB, 27 * SS), fill=BRANCO)
    d.text((22 * SS, 45 * SS), "ENVÍO EN 24 HORAS", font=F(PB, 25 * SS), fill=AMA)
    caminhao(d, 395 * SS, 26 * SS, 14 * SS, BRANCO)
    im = im.resize((w, h), Image.LANCZOS)
    im.save(OUT / "banner_topo.png")
    return im


def com_banner(im):
    im.alpha_composite(Image.open(OUT / "banner_topo.png"), (16, 16))
    return im


def recorte_frascos():
    """recorta os 3 frascos do n2 (fundo branco) com flood fill a partir das bordas"""
    src = Image.open(r"C:\Users\PICHAU\Downloads\KIT-HOMBRE-3EN1\flora\image_n2.png").convert("RGB")
    a = np.asarray(src).astype(np.int16)
    branco = (a.min(axis=2) > 236)
    from scipy import ndimage
    lab, _ = ndimage.label(branco)
    bordas = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fundo = np.isin(lab, list(bordas))
    alpha = np.where(fundo, 0, 255).astype(np.uint8)
    alpha = np.asarray(Image.fromarray(alpha).filter(ImageFilter.GaussianBlur(0.8)))
    rgba = np.dstack([np.asarray(src), alpha])
    im = Image.fromarray(rgba, "RGBA")
    bb = im.getbbox()
    im = im.crop(bb)
    im.save(OUT / "frascos_recorte.png")
    return im


def sticker(fr, larg=560):
    k = larg / fr.width
    s = fr.resize((larg, int(fr.height * k)), Image.LANCZOS)
    c, pad = sombra(s, r=12, off=(0, 8), alpha=200)
    c.save(OUT / "sticker_kit.png")
    return c


def frascos_rodape(fr, larg=520, base=1262):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    k = larg / fr.width
    s = fr.resize((larg, int(fr.height * k)), Image.LANCZOS)
    c, pad = sombra(s, r=12, off=(0, 8), alpha=200)
    im.alpha_composite(c, ((W - c.width) // 2, base - s.height - pad))
    return im, base - s.height


def texto_c(d, t, f, y, cor, contorno=0, cor_c=(0, 0, 0, 255)):
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, y), t, font=f, fill=cor, stroke_width=contorno, stroke_fill=cor_c)


def perfume(nome_arq, marca, nome, adjs, y=150):
    im = Image.new("RGBA", (W * SS, H * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    def tc(t, f, yy, cor, sw):
        tw = d.textlength(t, font=f)
        d.text(((W * SS - tw) / 2, yy), t, font=f, fill=cor, stroke_width=sw, stroke_fill=(0, 0, 0, 255))
    tc(marca.upper(), F(PS, 30 * SS), (y) * SS, (235, 235, 235, 255), 2 * SS)
    tc(nome.upper(), F(AN, 84 * SS), (y + 38) * SS, OURO, 4 * SS)
    tc("  ·  ".join(a.upper() for a in adjs), F(PB, 31 * SS), (y + 150) * SS, BRANCO, 3 * SS)
    im = im.resize((W, H), Image.LANCZOS)
    im = com_banner(im)
    im.save(OUT / f"{nome_arq}.png")
    return im


def setas(im, y=1015):
    """2 setas vermelhas apontando para baixo (botao real do anuncio)"""
    d = ImageDraw.Draw(im)
    for cx in (150, 570):
        pts = [(cx - 26, y), (cx + 26, y), (cx + 26, y + 46), (cx + 52, y + 46), (cx, y + 100), (cx - 52, y + 46),
               (cx - 26, y + 46)]
        d.polygon(pts, fill=VERM, outline=(255, 255, 255, 255), width=3)
    return im


def cta(nome_arq, fr, linha1="3 PERFUMES", linha2="AL PRECIO DE 1", sub="PAGA AL RECIBIR", fundo_escuro=True):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if fundo_escuro:  # degrade escuro para o texto ler sobre qualquer video
        g = np.zeros((H, W, 4), np.uint8)
        al = np.clip((np.linspace(0, 1, H) * 1.0) * 0 + 150, 0, 255).astype(np.uint8)
        g[..., 3] = al[:, None]
        im = Image.fromarray(g, "RGBA")
    d = ImageDraw.Draw(im)
    texto_c(d, linha1, F(AN, 108), 250, OURO, 5)
    texto_c(d, linha2, F(AN, 108), 370, BRANCO, 5)
    f = F(PB, 44)
    tw = d.textlength(sub, font=f)
    d.rounded_rectangle(((W - tw) / 2 - 26, 518, (W + tw) / 2 + 26, 590), 18, fill=AMA)
    d.text(((W - tw) / 2, 524), sub, font=f, fill=(10, 10, 10, 255))
    texto_c(d, "Club de Nuit Intense · Asad · 9PM", F(PS, 30), 618, BRANCO, 2)
    rod, topo = frascos_rodape(fr, larg=500)
    im.alpha_composite(rod)
    setas(im, y=topo - 150)
    im = com_banner(im)
    im.save(OUT / f"{nome_arq}.png")
    return im


def titulo(nome_arq, linhas, cores, y=210, px=92, caixa=True):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    f = F(AN, px)
    yy = y
    for t, c in zip(linhas, cores):
        tw = d.textlength(t, font=f)
        bb = d.textbbox((0, 0), t, font=f)
        if caixa:
            d.rounded_rectangle(((W - tw) / 2 - 22, yy - 6, (W + tw) / 2 + 22, yy + bb[3] + 10), 14,
                                fill=(0, 0, 0, 215))
        d.text(((W - tw) / 2, yy), t, font=f, fill=c, stroke_width=3, stroke_fill=(0, 0, 0, 255))
        yy += bb[3] + 22
    im = com_banner(im)
    im.save(OUT / f"{nome_arq}.png")
    return im


if __name__ == "__main__":
    banner()
    fr = recorte_frascos()
    sticker(fr)
    titulo("m7_tit", ["POV:", "HUELES A..."], [BRANCO, OURO], y=140, px=120, caixa=False)
    perfume("m7_armaf", "Armaf", "Club de Nuit Intense", ["fresco", "masculino", "poderoso"])
    perfume("m7_asad", "Lattafa", "Asad", ["intenso", "sofisticado", "seductor"])
    perfume("m7_9pm", "Afnan", "9PM", ["elegante", "moderno", "refinado"])
    cta("m7_cta", fr)
    cta("m6_cta", fr)
    titulo("m6_tit_11", ["PRUEBA A CIEGAS", "3 PERFUMES ÁRABES"], [AMA, BRANCO], y=150, px=78)
    titulo("m6_tit_12", ["NO SABÍA", "QUÉ ESTABA OLIENDO"], [AMA, BRANCO], y=150, px=78)
    # previa
    prev = Image.new("RGB", (W * 4 // 2, H // 2 * 2), (60, 60, 60))
    nomes = ["m7_tit", "m7_armaf", "m7_cta", "m6_tit_11"]
    bg = Image.open(D / "imagens" / "m7_asad.png").convert("RGBA")
    for k, n in enumerate(nomes):
        b = bg.copy()
        b.alpha_composite(Image.open(OUT / f"{n}.png"))
        prev.paste(b.convert("RGB").resize((W // 2, H // 2)), ((k % 4) * W // 2, 0))
    b = Image.open(D / "imagens" / "m6_amigos.png").convert("RGBA")
    b.alpha_composite(Image.open(OUT / "m6_cta.png"))
    prev.paste(b.convert("RGB").resize((W // 2, H // 2)), (0, H // 2))
    b = Image.open(D / "imagens" / "m6_amigos.png").convert("RGBA")
    b.alpha_composite(Image.open(OUT / "m6_tit_12.png"))
    prev.paste(b.convert("RGB").resize((W // 2, H // 2)), (W // 2, H // 2))
    b = Image.open(D / "imagens" / "m7_9pm.png").convert("RGBA")
    b.alpha_composite(Image.open(OUT / "m7_9pm.png"))
    prev.paste(b.convert("RGB").resize((W // 2, H // 2)), (W, H // 2))
    b = Image.open(D / "imagens" / "m7_armaf.png").convert("RGBA")
    st = Image.open(OUT / "sticker_kit.png")
    b.alpha_composite(st, ((W - st.width) // 2, H - st.height - 40))
    b.alpha_composite(Image.open(OUT / "banner_topo.png"), (16, 16))
    prev.paste(b.convert("RGB").resize((W // 2, H // 2)), (3 * W // 2, H // 2))
    prev.save(OUT / "_preview.jpg", quality=88)
    print("ok")
