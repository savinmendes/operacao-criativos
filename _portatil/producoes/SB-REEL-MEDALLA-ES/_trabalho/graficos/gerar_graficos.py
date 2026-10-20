# -*- coding: utf-8 -*-
"""Gráficos PNG transparentes 1080x1920 do reel SB Medalla (sem custo, PIL).
Rodar: python gerar_graficos.py  (na pasta graficos/)"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = Path(__file__).resolve().parent
FON = AQUI.parent / "fonts"
W, H = 1080, 1920
AMARELO = (254, 229, 84, 255)      # #FEE554
VERMELHO = (226, 30, 45, 255)
OURO = (246, 214, 140, 255)        # dourado/creme
ESCURO = (20, 16, 10, 255)

LATIM = [
    ("Crux sancta sit mihi lux", "La santa cruz sea mi luz"),
    ("Non draco sit mihi dux", "Que el mal no sea mi guía"),
    ("Vade retro, Satana", "¡Apártate, Satanás!"),
    ("Numquam suade mihi vana", "Nunca me aconsejes cosas vanas"),
    ("Sunt mala quae libas", "Es malo lo que me ofreces"),
    ("Ipse venena bibas", "Bebe tú mismo tu veneno"),
]


def F(peso, tam):
    return ImageFont.truetype(str(FON / f"Poppins-{peso}.ttf"), tam)


def tela():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def larg(d, t, f, sw=0):
    b = d.textbbox((0, 0), t, font=f, stroke_width=sw)
    return b[2] - b[0], b[3] - b[1], b


def texto_c(d, cx, cy, t, f, fill, sw=0, sf=None):
    """texto centrado (horizontal e vertical pela caixa real)."""
    w, h, b = larg(d, t, f, sw)
    d.text((cx - w / 2 - b[0], cy - h / 2 - b[1]), t, font=f, fill=fill, stroke_width=sw, stroke_fill=sf)


def caber(d, t, peso, tam, maxw, sw=0):
    while tam > 20 and larg(d, t, F(peso, tam), sw)[0] > maxw:
        tam -= 2
    return F(peso, tam)


def sombra(im, raio=10, alfa=150, desloc=(0, 6)):
    """sombra suave sob o conteúdo opaco da camada."""
    a = im.split()[3].point(lambda v: min(255, v) * alfa // 255)
    s = Image.new("RGBA", im.size, (0, 0, 0, 0))
    s.putalpha(a)
    s = s.filter(ImageFilter.GaussianBlur(raio))
    out = tela()
    out.alpha_composite(s, desloc)
    out.alpha_composite(im)
    return out


# ---------------------------------------------------------------- selo
def selo():
    im = tela(); d = ImageDraw.Draw(im)
    f = F("Bold", 36)
    t = "VIDEO FICTICIO"
    w, h, b = larg(d, t, f)
    px, py = 22, 12
    x1 = W - 40; x0 = x1 - w - 2 * px
    y0 = 64; y1 = y0 + h + 2 * py
    d.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(0, 0, 0, 179))  # 70%
    d.text((x0 + px - b[0], y0 + py - b[1]), t, font=f, fill=(255, 255, 255, 255))
    im.save(AQUI / "selo_ficticio.png")
    return (x0, y0, x1, y1)


# ---------------------------------------------------------------- título do gancho
def titulo():
    im = tela(); d = ImageDraw.Draw(im)
    linhas = [("ALGO INESPERADO PASÓ", (255, 255, 255, 255), VERMELHO),
              ("DURANTE LA ORACIÓN", (255, 255, 255, 255), (15, 15, 15, 255)),
              ("A SAN BENITO", VERMELHO, (255, 255, 255, 255))]
    f = F("ExtraBold", 60)
    alt, gap = 76, 8
    y = 1150 + (200 - (3 * alt + 2 * gap)) // 2 + 6
    for t, fundo, cor in linhas:
        w, h, b = larg(d, t, f)
        x0 = (W - w) // 2 - 26; x1 = (W + w) // 2 + 26
        d.rectangle([x0, y, x1, y + alt], fill=fundo)
        texto_c(d, W / 2, y + alt / 2, t, f, cor)
        y += alt + gap
    sombra(im, 8, 140, (0, 5)).save(AQUI / "titulo_gancho.png")


# ---------------------------------------------------------------- moldura EN VIVO
def coracao(d, cx, cy, r, cor, contorno=None, lw=0):
    # dois círculos + triângulo
    pts = []
    import math
    for i in range(0, 361, 3):
        t = math.radians(i)
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * r / 17, cy + y * r / 17))
    d.polygon(pts, fill=cor, outline=contorno, width=lw)


def compartilhar(d, cx, cy, s, cor):
    # seta curva estilo "encaminhar": corpo + ponta
    lw = max(4, s // 9)
    d.arc([cx - s * 0.95, cy - s * 0.15, cx + s * 0.35, cy + s * 1.15], 200, 290, fill=cor, width=lw)
    d.polygon([(cx + s * 0.05, cy - s * 0.55), (cx + s * 0.75, cy - s * 0.02), (cx + s * 0.05, cy + s * 0.5)], fill=cor)


def olho(d, cx, cy, s, cor):
    d.ellipse([cx - s, cy - s * 0.6, cx + s, cy + s * 0.6], outline=cor, width=4)
    d.ellipse([cx - s * 0.32, cy - s * 0.32, cx + s * 0.32, cy + s * 0.32], fill=cor)


def moldura(selo_box):
    im = tela()
    # degradês discretos topo/base p/ leitura
    g = Image.new("L", (1, 256))
    for i in range(256):
        g.putpixel((0, i), int(110 * (1 - i / 255) ** 1.6))
    top = g.resize((W, 260)); bot = g.transpose(Image.FLIP_TOP_BOTTOM).resize((W, 240))
    camada = tela()
    camada.paste((0, 0, 0, 255), (0, 0, W, 260), top)
    camada.paste((0, 0, 0, 255), (0, H - 240, W, H), bot)
    im.alpha_composite(camada)
    d = ImageDraw.Draw(im)

    # --- linha de topo (y 130-196), toda à esquerda do selo
    cy = 163
    ax, ar = 40 + 33, 33
    d.ellipse([ax - ar - 3, cy - ar - 3, ax + ar + 3, cy + ar + 3], fill=VERMELHO)       # anel "ao vivo"
    d.ellipse([ax - ar, cy - ar, ax + ar, cy + ar], fill=(150, 150, 158, 255))            # avatar genérico
    d.ellipse([ax - 12, cy - 22, ax + 12, cy + 2], fill=(235, 235, 240, 255))             # cabeça
    d.pieslice([ax - 24, cy + 4, ax + 24, cy + 52], 180, 360, fill=(235, 235, 240, 255))  # ombros
    # recorta ombros para dentro do círculo
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).ellipse([ax - ar, cy - ar, ax + ar, cy + ar], fill=255)
    fora = Image.new("L", (W, H), 0); ImageDraw.Draw(fora).rectangle([ax - ar, cy + 2, ax + ar, cy + 60], fill=255)
    # (o pieslice já fica quase todo dentro; o resto é encoberto pela borda)
    d.ellipse([ax - ar - 3, cy - ar - 3, ax + ar + 3, cy + ar + 3], outline=VERMELHO, width=4)

    x = ax + ar + 18
    fn = F("SemiBold", 27)
    d.text((x, cy - 36), "Sacerdote", font=F("Bold", 30), fill=(255, 255, 255, 255),
           stroke_width=1, stroke_fill=(0, 0, 0, 120))
    d.text((x, cy + 2), "(personaje ficticio)", font=F("Medium", 22), fill=(235, 235, 235, 255))
    nome_w = max(larg(d, "Sacerdote", F("Bold", 30))[0], larg(d, "(personaje ficticio)", F("Medium", 22))[0])

    x = x + nome_w + 22
    fv = F("Bold", 25)
    t = "EN VIVO"
    w, h, b = larg(d, t, fv)
    d.rounded_rectangle([x, cy - 22, x + w + 30, cy + 22], radius=7, fill=VERMELHO)
    texto_c(d, x + (w + 30) / 2, cy, t, fv, (255, 255, 255, 255))
    x = x + w + 30 + 12
    t = "1,2 mil"
    fe = F("SemiBold", 25)
    w2, _, _ = larg(d, t, fe)
    d.rounded_rectangle([x, cy - 22, x + w2 + 66, cy + 22], radius=7, fill=(0, 0, 0, 140))
    olho(d, x + 26, cy, 15, (255, 255, 255, 255))
    texto_c(d, x + 50 + w2 / 2, cy, t, fe, (255, 255, 255, 255))
    fim_topo = x + w2 + 66
    assert fim_topo < selo_box[0] - 10 or cy - 22 > selo_box[3] + 6, (fim_topo, selo_box)
    # botão fechar (X) não, para não parecer interface real.

    # --- barra de comentários (y 1800-1880)
    y0, y1 = 1806, 1874
    d.rounded_rectangle([40, y0, 790, y1], radius=34, fill=(0, 0, 0, 90), outline=(255, 255, 255, 200), width=3)
    d.text((76, (y0 + y1) / 2), "Comentar…", font=F("Medium", 30), fill=(255, 255, 255, 230), anchor="lm")
    coracao(d, 870, 1838, 30, (255, 255, 255, 0), (255, 255, 255, 255), 5)
    coracao(d, 870, 1838, 30, None, (255, 255, 255, 255), 5)
    compartilhar(d, 985, 1846, 40, (255, 255, 255, 255))
    im.save(AQUI / "moldura_envivo.png")
    return fim_topo


# ---------------------------------------------------------------- cartões latim
def cartao_latim(i, lat, trad):
    im = tela(); d = ImageDraw.Draw(im)
    fl = caber(d, lat, "ExtraBold", 76, 900, 4)
    ft = caber(d, trad, "SemiBold", 46, 900, 3)
    hl = larg(d, lat, fl, 4)[1]; ht = larg(d, trad, ft, 3)[1]
    cx, cy = W / 2, 960
    alt = hl + ht + 36 + 2 * 46
    x0, x1 = 50, W - 50
    y0 = cy - alt / 2; y1 = cy + alt / 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(10, 8, 4, 165), outline=(246, 214, 140, 200), width=3)
    # filete dourado
    d.line([(W / 2 - 120, y0 + 46 + hl + 18), (W / 2 + 120, y0 + 46 + hl + 18)], fill=(246, 214, 140, 160), width=3)
    texto_c(d, cx, y0 + 46 + hl / 2, lat, fl, OURO, 4, ESCURO)
    texto_c(d, cx, y1 - 46 - ht / 2, trad, ft, (255, 255, 255, 255), 3, ESCURO)
    sombra(im, 14, 120, (0, 8)).save(AQUI / f"latim_{i:02d}.png")


def lista_latim(ativa):
    """ativa = 1..6 (0 = nenhuma destacada)."""
    im = tela(); d = ImageDraw.Draw(im)
    y0, y1 = 470, 1330
    d.rounded_rectangle([40, y0, W - 40, y1], radius=32, fill=(10, 8, 4, 170), outline=(246, 214, 140, 170), width=3)
    passo = (y1 - y0 - 60) / 6
    for k, (lat, trad) in enumerate(LATIM, 1):
        cy = y0 + 30 + passo * (k - 0.5)
        on = k == ativa
        fl = caber(d, lat, "ExtraBold", 58 if on else 52, 940, 3)
        ft = caber(d, trad, "SemiBold", 32 if on else 29, 940, 2)
        cl = AMARELO if on else (255, 255, 255, 153)
        ct = (255, 255, 255, 255) if on else (255, 255, 255, 120)
        if on:
            d.rounded_rectangle([60, cy - passo / 2 + 6, W - 60, cy + passo / 2 - 6], radius=22,
                                fill=(254, 229, 84, 38), outline=(254, 229, 84, 210), width=3)
        texto_c(d, W / 2, cy - 20, lat, fl, cl, 3 if on else 0, ESCURO if on else None)
        texto_c(d, W / 2, cy + 30, trad, ft, ct, 2 if on else 0, ESCURO if on else None)
    nome = "latim_lista.png" if ativa == 0 else f"latim_lista_{ativa}.png"
    sombra(im, 14, 110, (0, 8)).save(AQUI / nome)


# ---------------------------------------------------------------- CTA
def seta(w=170, h=200):
    S = 4
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    def P(pts): return [(x * S * w / 190, y * S * h / 225) for x, y in pts]
    d.polygon(P([(60, 8), (130, 8), (130, 112), (178, 112), (95, 215), (12, 112), (60, 112)]), fill=ESCURO)
    d.polygon(P([(67, 15), (123, 15), (123, 119), (163, 119), (95, 203), (27, 119), (67, 119)]), fill=AMARELO)
    d.polygon(P([(67, 15), (123, 15), (123, 60), (67, 60)]), fill=(255, 241, 160, 255))
    return im.resize((w, h), Image.LANCZOS)


def cta():
    im = tela(); d = ImageDraw.Draw(im)
    f = F("ExtraBold", 64)
    partes = [("TOCA ", (255, 255, 255, 255)), ("«VER MÁS»", AMARELO), (" AQUÍ ABAJO", (255, 255, 255, 255))]
    tot = sum(larg(d, t, f, 6)[0] for t, _ in partes)
    if tot > 1000:
        f = caber(d, "TOCA «VER MÁS» AQUÍ ABAJO", "ExtraBold", 64, 1000, 6)
        tot = sum(larg(d, t, f, 6)[0] for t, _ in partes)
    x = (W - tot) / 2; cy = 1572
    for t, c in partes:
        w, h, b = larg(d, t, f, 6)
        d.text((x, cy), t, font=f, fill=c, stroke_width=6, stroke_fill=ESCURO, anchor="lm")
        x += d.textlength(t, font=f)
    s = seta(150, 176)
    for cx in (385, 695):
        im.alpha_composite(s, (int(cx - 75), 1620))
    sombra(im, 8, 130, (0, 5)).save(AQUI / "cta_vermas.png")


# ---------------------------------------------------------------- prévia
def amostra_legenda(im, txt="CRUX SANCTA", amarelo="SANCTA"):
    d = ImageDraw.Draw(im); f = F("ExtraBold", 83)
    pal = txt.split(); tot = d.textlength(" ".join(pal), font=f); x = (W - tot) / 2
    for p in pal:
        d.text((x, 1460), p, font=f, fill=AMARELO if p == amarelo else (255, 255, 255, 255),
               stroke_width=6, stroke_fill=(0, 0, 0, 255), anchor="lm")
        x += d.textlength(p + " ", font=f)


def previa():
    def fundo():
        b = Image.new("RGBA", (W, H), (120, 120, 120, 255)); d = ImageDraw.Draw(b)
        for y in range(0, H, 120):
            for x in range(0, W, 120):
                if (x // 120 + y // 120) % 2:
                    d.rectangle([x, y, x + 119, y + 119], fill=(105, 105, 105, 255))
        return b
    L = lambda n: Image.open(AQUI / n)
    paineis = [
        ("gancho", ["moldura_envivo.png", "selo_ficticio.png", "titulo_gancho.png"], None),
        ("latim_01", ["moldura_envivo.png", "selo_ficticio.png", "latim_01.png"], ("CRUX SANCTA", "SANCTA")),
        ("latim_04", ["moldura_envivo.png", "selo_ficticio.png", "latim_04.png"], ("NUMQUAM SUADE", "SUADE")),
        ("lista_3", ["moldura_envivo.png", "selo_ficticio.png", "latim_lista_3.png"], ("VADE RETRO", "RETRO")),
        ("cta", ["moldura_envivo.png", "selo_ficticio.png", "cta_vermas.png"], ("TOCA EL BOTÓN", "TOCA")),
    ]
    esc = 0.36; pw, ph = int(W * esc), int(H * esc)
    folha = Image.new("RGB", (pw * len(paineis) + 20 * (len(paineis) + 1), ph + 70), (30, 30, 30))
    dd = ImageDraw.Draw(folha)
    for k, (nome, camadas, leg) in enumerate(paineis):
        b = fundo()
        for c in camadas:
            b.alpha_composite(L(c))
        if leg:
            amostra_legenda(b, *leg)
        x = 20 + k * (pw + 20)
        folha.paste(b.convert("RGB").resize((pw, ph), Image.LANCZOS), (x, 50))
        dd.text((x, 12), nome, font=F("SemiBold", 26), fill=(240, 240, 240))
    folha.save(AQUI / "previa.jpg", quality=90)


if __name__ == "__main__":
    sb = selo()
    titulo()
    moldura(sb)
    for i, (lat, trad) in enumerate(LATIM, 1):
        cartao_latim(i, lat, trad)
    for a in range(0, 7):
        lista_latim(a)
    cta()
    previa()
    print("ok")
