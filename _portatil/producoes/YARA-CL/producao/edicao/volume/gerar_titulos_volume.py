# -*- coding: utf-8 -*-
"""Titulos de abertura dos ganchos H2-H5 + rotulos do H5 (720x1280, mesma identidade preto/dourado, SEM PRECO).
Base: ../_trabalho/gerar_overlays_sem_preco.py. Local (PIL), sem custo."""
import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_trabalho"))
import gerar_overlays_sem_preco as g

OUT = Path(__file__).resolve().parent
W, H = g.W, g.H


def cx(im, el, y):
    im.alpha_composite(el, ((W - el.width) // 2, int(y)))
    return int(y) + el.height


def caber(el, maxw=690):
    if el.width <= maxw:
        return el
    return el.resize((maxw, int(el.height * maxw / el.width)), Image.LANCZOS)


def h2():
    """consultora pequena no balcao (rosto ~y 320-576 apos punch-in): PAGA 2 em cima, LLEVA 3 embaixo"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bf = caber(g.faixa_texto("BLACK FRIDAY", g.AN, 70, g.OURO, g.PRETO, padx=18, pady=6, angulo=3, contorno=g.OURO), 520)
    y = cx(im, bf, 40)
    cx(im, caber(g.texto_contorno("PAGA 2", g.AN, 150, g.BRANCO, sw=10, angulo=3)), y - 10)
    l3 = caber(g.texto_contorno("LLEVA 3", g.AN, 170, g.OURO2, sw=11, angulo=-3))
    y = cx(im, l3, 720)
    cx(im, g.faixa_texto("EL TERCERO GRATIS", g.AN, 56, g.BRANCO, g.VERM, padx=20, pady=6, angulo=-3), y - 25)
    im.save(OUT / "titulo_H2.png")
    return im


def h3():
    """close da consultora cheirando o frasco: rosto/frasco ocupam y ~120-1080 -> texto no topo (cabelo) e no rodape"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx(im, caber(g.faixa_texto("¿YA PROBASTE", g.AN, 92, g.OURO, g.PRETO, padx=22, pady=8, angulo=-2, contorno=g.OURO)), 40)
    lp = caber(g.texto_contorno("LOS PERFUMES", g.AN, 110, g.BRANCO, sw=9, angulo=-2))
    y = cx(im, lp, 1010)
    cx(im, caber(g.texto_contorno("ÁRABES?", g.AN, 120, g.OURO2, sw=10, angulo=-2)), y - 40)
    im.save(OUT / "titulo_H3.png")
    return im


def h4():
    """B-roll de unboxing (maos/caixa no centro)"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cx(im, g.faixa_texto("LIQUIDACIÓN", g.AN, 96, g.BRANCO, g.VERM, padx=24, pady=8, angulo=-3), 70)
    bf = caber(g.faixa_texto("BLACK FRIDAY", g.AN, 118, g.OURO, g.PRETO, padx=22, pady=8, angulo=3, contorno=g.OURO))
    y = cx(im, bf, 930)
    cx(im, g.texto_contorno("PAGA 2 · LLEVA 3", g.AN, 80, g.OURO2, sw=7), y - 6)
    im.save(OUT / "titulo_H4.png")
    return im


def h5():
    """3 closes de frasco: rotulo no topo (png por segmento), este titulo fixo no rodape"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    y = cx(im, caber(g.texto_contorno("3 PERFUMES ÁRABES", g.AN, 84, g.BRANCO, sw=7)), 960)
    cx(im, caber(g.faixa_texto("PAGA 2 · LLEVA 3", g.AN, 78, g.OURO2, g.PRETO, padx=24, pady=8, contorno=g.OURO)), y - 4)
    im.save(OUT / "titulo_H5.png")
    rot = {}
    for nome, arq in (("YARA", "rotulo_yara.png"), ("YARA MOI", "rotulo_moi.png"), ("YARA ELIXIR", "rotulo_elixir.png")):
        r = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        cx(r, caber(g.faixa_texto(nome, g.AN, 120, g.OURO, g.PRETO, padx=26, pady=8, angulo=-3, contorno=g.OURO)), 150)
        r.save(OUT / arq)
        rot[nome] = r
    return im, rot


if __name__ == "__main__":
    a, b, c = h2(), h3(), h4()
    d, rot = h5()
    # previa sobre quadros reais
    import subprocess
    def q(v, t):
        p = OUT / "_q.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", v, "-frames:v", "1", "-vf",
                        "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280", str(p)], check=True)
        return Image.open(p).convert("RGBA")
    T = r"C:\Users\PICHAU\Downloads\YARA-CL\producao\takes"
    B = r"C:\Users\PICHAU\Downloads\YARA-CL\banco"
    pares = [(q(T + r"\T10_cta.mp4", 1.0), a), (q(T + r"\T4_yara_close.mp4", 0.6), b),
             (q(B + r"\yara_03.mp4", 0.6), c), (q(B + r"\yara_04.mp4", 1.3), Image.alpha_composite(d, rot["YARA"]))]
    sheet = Image.new("RGB", (4 * 360 + 30, 640), (40, 40, 40))
    for i, (bg, ov) in enumerate(pares):
        bg.alpha_composite(ov)
        sheet.paste(bg.convert("RGB").resize((360, 640)), (i * 370, 0))
    sheet.save(OUT / "preview_titulos.jpg", quality=88)
    print("ok")
