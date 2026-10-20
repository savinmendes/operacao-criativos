# -*- coding: utf-8 -*-
"""Gráficos FR (mesmo estilo/posição dos ES de _trabalho/graficos). Rodar: python gerar_graficos_fr.py"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[2] / "graficos"))
import gerar_graficos as g
from PIL import Image, ImageDraw

B = (255, 255, 255, 255)
NBSP = " "


def selo_mini():
    im = g.tela(); d = ImageDraw.Draw(im)
    f = g.F("Bold", 18); t = "VIDÉO FICTIVE"
    w, h, b = g.larg(d, t, f)
    px, py = 11, 6
    x1 = g.W - 20; x0 = x1 - w - 2 * px
    y0 = 4; y1 = y0 + h + 2 * py
    d.rounded_rectangle([x0, y0, x1, y1], radius=5, fill=(0, 0, 0, 179))
    d.text((x0 + px - b[0], y0 + py - b[1]), t, font=f, fill=B)
    im.save(AQUI / "selo_ficticio_mini_fr.png")
    return (x0, y0, x1, y1)


def titulo():
    im = g.tela(); d = ImageDraw.Draw(im)
    linhas = [("QUELQUE CHOSE D'INATTENDU", B, g.VERMELHO),
              ("EST ARRIVÉ PENDANT", B, (15, 15, 15, 255)),
              ("LA PRIÈRE À SAINT BENOÎT", g.VERMELHO, B)]
    # mesma fonte do ES (ExtraBold 60); reduz igual nas 3 linhas só se a maior passar de 960 px
    tam = 60
    # caixa mais larga <= ~900 px (ES: 824) p/ não cobrir mais o personagem que o título ES
    while max(g.larg(d, t, g.F("ExtraBold", tam))[0] for t, _, _ in linhas) > 848:
        tam -= 2
    f = g.F("ExtraBold", tam)
    alt, gap = round(90 * tam / 60), 8  # ES usa 76 (fonte 60); +14 px p/ caber os acentos (É, È, À, Î)
    desl = round(5 * tam / 60)
    # centro vertical pela altura das maiúsculas sem acento (acentos sobem sem deslocar a linha)
    ref = d.textbbox((0, 0), "HQUELPNT", font=f)
    y = 1150 + (200 - (3 * alt + 2 * gap)) // 2 + 6
    for t, fundo, cor in linhas:
        w = g.larg(d, t, f)[0]
        x0 = (g.W - w) // 2 - 26; x1 = (g.W + w) // 2 + 26
        d.rectangle([x0, y, x1, y + alt], fill=fundo)
        b = d.textbbox((0, 0), t, font=f)
        cy = y + alt / 2 + desl  # maiúsculas 5 px abaixo do centro: sobra espaço p/ o acento
        d.text((g.W / 2 - w / 2 - b[0], cy - (ref[1] + ref[3]) / 2), t, font=f, fill=cor)
        topo = cy - (ref[1] + ref[3]) / 2 + b[1]
        assert topo >= y + 4, (t, topo, y)  # acento não sai da faixa
        y += alt + gap
    g.sombra(im, 8, 140, (0, 5)).save(AQUI / "titulo_gancho_fr.png")
    return tam


def cta():
    partes = [("APPUIE SUR ", B), ("«" + NBSP + "EN SAVOIR PLUS" + NBSP + "»", g.AMARELO)]
    im = g.tela(); d = ImageDraw.Draw(im)
    f = g.F("ExtraBold", 64)
    tot = sum(g.larg(d, t, f, 6)[0] for t, _ in partes)
    if tot > 1000:
        f = g.caber(d, "".join(t for t, _ in partes), "ExtraBold", 64, 1000, 6)
    tot = sum(d.textlength(t, font=f) for t, _ in partes)
    x = (g.W - tot) / 2; cy = 1572
    for t, c in partes:
        d.text((x, cy), t, font=f, fill=c, stroke_width=6, stroke_fill=g.ESCURO, anchor="lm")
        x += d.textlength(t, font=f)
    txt = g.sombra(im, 8, 130, (0, 5)); txt.save(AQUI / "cta_txt_ensavoirplus_fr.png")
    se = g.tela(); s = g.seta(150, 176)
    for cx in (385, 695):
        se.alpha_composite(s, (int(cx - 75), 1620))
    se = g.sombra(se, 8, 130, (0, 5)); se.save(AQUI / "cta_setas_fr.png")
    un = txt.copy(); un.alpha_composite(se); un.save(AQUI / "cta_ensavoirplus_unico_fr.png")
    return f.size


def previa():
    def fundo():
        b = Image.new("RGBA", (g.W, g.H), (120, 120, 120, 255)); dd = ImageDraw.Draw(b)
        for y in range(0, g.H, 120):
            for x in range(0, g.W, 120):
                if (x // 120 + y // 120) % 2:
                    dd.rectangle([x, y, x + 119, y + 119], fill=(105, 105, 105, 255))
        return b
    paineis = [("gancho", ["selo_ficticio_mini_fr.png", "titulo_gancho_fr.png"]),
               ("cta", ["selo_ficticio_mini_fr.png", "cta_ensavoirplus_unico_fr.png"])]
    esc = 0.5; pw, ph = int(g.W * esc), int(g.H * esc)
    folha = Image.new("RGB", (pw * 2 + 60, ph + 70), (30, 30, 30)); dd = ImageDraw.Draw(folha)
    for k, (nome, cam) in enumerate(paineis):
        b = fundo()
        for c in cam:
            b.alpha_composite(Image.open(AQUI / c))
        x = 20 + k * (pw + 20)
        folha.paste(b.convert("RGB").resize((pw, ph), Image.LANCZOS), (x, 50))
        dd.text((x, 12), nome, font=g.F("SemiBold", 26), fill=(240, 240, 240))
    folha.save(AQUI / "previa.jpg", quality=90)
    # zooms 1:1 dos textos para conferir acentos
    z = []
    for nome, box in [("titulo_gancho_fr.png", (60, 1100, 1020, 1420)), ("cta_ensavoirplus_unico_fr.png", (20, 1480, 1060, 1820)),
                      ("selo_ficticio_mini_fr.png", (860, 0, 1080, 40))]:
        b = fundo(); b.alpha_composite(Image.open(AQUI / nome)); z.append(b.crop(box).convert("RGB"))
    z[2] = z[2].resize((z[2].width * 4, z[2].height * 4), Image.LANCZOS)
    W2 = max(i.width for i in z); H2 = sum(i.height for i in z) + 40
    zz = Image.new("RGB", (W2, H2), (30, 30, 30)); y = 0
    for i in z:
        zz.paste(i, (0, y)); y += i.height + 20
    zz.save(AQUI / "previa_zoom.jpg", quality=92)


if __name__ == "__main__":
    print("selo", selo_mini())
    print("titulo fonte", titulo())
    print("cta fonte", cta())
    previa()
    print("ok")
