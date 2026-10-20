# -*- coding: utf-8 -*-
"""Gera os estáticos (feed 4:5 1080x1350 e carrossel 1:1 1080x1080) da podadora a partir de quadros reais.
Quadro -> recorte sem o aviso em inglês do rodapé -> Real-ESRGAN 2x -> 1080 -> manchete + selo COD."""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

E = Path(__file__).resolve().parent
KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import overlays as OV  # noqa: E402

RE = KIT / "_ferramentas_extras" / "realesrgan" / "realesrgan-ncnn-vulkan.exe"
FB = str(KIT / "fonts" / "Poppins-Bold.ttf")
OUT = E.parent.parent / "estaticos"
OUT.mkdir(exist_ok=True)
(E / "up").mkdir(exist_ok=True)
SELO = ["DESPACHO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"]


def quadro(nome, w, h, y0=None, x0=None):
    """Recorta w×h (proporção alvo) de um quadro 720x1280 sem passar de y=1150 (aviso em inglês) e sobe para 1080."""
    src = Image.open(E / "q" / f"{nome}.png").convert("RGB")
    ratio = w / h
    cw = 720 if ratio <= 720 / 1150 * 1.0 + 9 else 720
    ch = int(cw / ratio)
    if ch > 1150:
        ch = 1150; cw = int(ch * ratio)
    x0 = (720 - cw) // 2 if x0 is None else x0
    y0 = max(0, min(1150 - ch, (1150 - ch) if y0 is None else y0))
    c = src.crop((x0, y0, x0 + cw, y0 + ch))
    tmp, up = E / "up" / f"{nome}_{w}x{h}_in.png", E / "up" / f"{nome}_{w}x{h}_up.png"
    c.save(tmp)
    if not up.exists():
        subprocess.run([str(RE), "-i", str(tmp), "-o", str(up), "-s", "2", "-n", "realesr-animevideov3"],
                       check=True, capture_output=True)
    return Image.open(up).convert("RGB").resize((w, h), Image.LANCZOS)


def colar_png(base, png, x, y, larg=None):
    im = Image.open(png).convert("RGBA")
    if larg:
        im = im.resize((larg, int(im.height * larg / im.width)), Image.LANCZOS)
    base.alpha_composite(im, (int(x if x is not None else (base.width - im.width) / 2), int(y)))
    return im.height


def peca(nome_saida, quadro_nome, w, h, manchete, y_manchete=60, selo=True, y0=None, rodape=None):
    base = quadro(quadro_nome, w, h, y0=y0).convert("RGBA")
    m = OV.manchete(manchete, str(E / "up" / f"m_{nome_saida}.png"), px=60, maxw=900)
    colar_png(base, m, None, y_manchete)
    if selo:
        s = OV.selo(SELO, str(E / "up" / "selo.png"))
        colar_png(base, s, None, h - 330, larg=620)
    if rodape:
        d = ImageDraw.Draw(base)
        f = ImageFont.truetype(FB, 34)
        tw = d.textlength(rodape, font=f)
        d.rounded_rectangle([(w - tw) / 2 - 24, h - 92, (w + tw) / 2 + 24, h - 36], radius=14, fill=(0, 0, 0, 200))
        d.text(((w - tw) / 2, h - 88), rodape, font=f, fill=(255, 255, 255, 255))
    base.convert("RGB").save(OUT / f"{nome_saida}.jpg", quality=92)
    print("ok", nome_saida)


def antes_depois(nome_saida, antes, depois, w=1080, h=1350):
    base = Image.new("RGBA", (w, h))
    a = quadro(antes, w // 2, h, y0=None)
    b = quadro(depois, w // 2, h, y0=None)
    base.paste(a, (0, 0)); base.paste(b, (w // 2, 0))
    d = ImageDraw.Draw(base)
    d.rectangle([w // 2 - 4, 0, w // 2 + 4, h], fill=(255, 255, 255, 255))
    f = ImageFont.truetype(FB, 64)
    for txt, cx, cor in (("ANTES", w // 4, (220, 30, 30, 255)), ("DESPUÉS", 3 * w // 4, (20, 150, 60, 255))):
        tw = d.textlength(txt, font=f)
        d.rounded_rectangle([cx - tw / 2 - 26, 60, cx + tw / 2 + 26, 150], radius=18, fill=cor)
        d.text((cx - tw / 2, 68), txt, font=f, fill=(255, 255, 255, 255))
    s = OV.selo(SELO, str(E / "up" / "selo.png"))
    colar_png(base, s, None, h - 330, larg=620)
    base.convert("RGB").save(OUT / f"{nome_saida}.jpg", quality=92)
    print("ok", nome_saida)


def oferta(nome_saida, fundo, w=1080, h=1080):
    base = quadro(fundo, w, h).filter(ImageFilter.GaussianBlur(14)).convert("RGBA")
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 120)); base.alpha_composite(ov)
    d = ImageDraw.Draw(base)
    f1, f2 = ImageFont.truetype(FB, 64), ImageFont.truetype(FB, 46)
    linhas = [("Podadora inalámbrica", f1, False), ("de césped con ruedas", f1, False), ("", f2, False),
              ("Despacho gratis", f2, True), ("Pagas al recibir", f2, True), ("90 días de garantía", f2, True)]
    y = 170
    for t, f, chk in linhas:
        if t:
            tw = d.textlength(t, font=f) + (62 if chk else 0)
            x = (w - tw) / 2
            if chk:  # check verde desenhado (a fonte não tem o caractere)
                cy = y + f.size * 0.62
                d.ellipse([x, cy - 22, x + 44, cy + 22], fill=(30, 170, 70, 255))
                d.line([(x + 11, cy), (x + 19, cy + 9), (x + 34, cy - 10)], fill=(255, 255, 255, 255), width=6)
                x += 62
            d.text((x, y), t, font=f, fill=(255, 255, 255, 255))
        y += int(f.size * 1.35)
    seta = OV.seta(str(E / "up" / "seta.png"))
    f3 = ImageFont.truetype(FB, 54)
    t = "Toca \"Comprar\" y pide la tuya"
    tw = d.textlength(t, font=f3)
    d.rounded_rectangle([(w - tw) / 2 - 30, 760, (w + tw) / 2 + 30, 850], radius=20, fill=(255, 214, 0, 255))
    d.text(((w - tw) / 2, 772), t, font=f3, fill=(0, 0, 0, 255))
    colar_png(base, seta, None, 870, larg=130)
    base.convert("RGB").save(OUT / f"{nome_saida}.jpg", quality=92)
    print("ok", nome_saida)


# feed 4:5
peca("01_feed_pasto-alto", "t30_50", 1080, 1350, "¿El pasto se te fue de las manos? 🌿")
peca("02_feed_3-en-1", "t15_50", 1080, 1350, "Cortapasto, orilladora y bordeadora: 3 EN 1")
peca("03_feed_ruedas", "t27_50", 1080, 1350, "Con ruedas: no cargas el peso, solo la guías")
peca("04_feed_cuchilla", "t28_50", 1080, 1350, "Cuchilla de metal: olvídate del hilo que se corta")
peca("05_feed_kit", "t31_50", 1080, 1350, "Mira todo lo que trae la caja 📦")
peca("06_feed_sin-bencina", "t8_50", 1080, 1350, "Sin bencina. Sin cables. Sin cuerda.")
peca("07_feed_orillas", "t6_50", 1080, 1350, "Para orillas, veredas y rincones del patio")
# carrossel 1:1
peca("carrusel_1_podadora", "t43_50", 1080, 1080, "Podadora inalámbrica de césped con ruedas", selo=False, rodape="Desliza para ver  »")
peca("carrusel_2_3-en-1", "t26_50", 1080, 1080, "3 en 1: corta, orilla y bordea", selo=False)
peca("carrusel_3_baterias", "t41_50", 1080, 1080, "2 baterías de 21 V incluidas 🔋", selo=False)
oferta("carrusel_4_oferta", "t6_50")
