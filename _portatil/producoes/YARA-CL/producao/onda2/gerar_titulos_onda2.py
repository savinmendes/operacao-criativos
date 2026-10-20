# -*- coding: utf-8 -*-
"""Títulos/overlays da onda 2 (720x1280, identidade preto/dourado do lote, SEM PREÇO). Local (PIL), sem custo.
Gera em overlays/: titulo_C2..C7.png, C1_t1..t5.png (texto do C1 sem fala) e C3_n1/n2/n3.png (contador)."""
import sys
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "edicao" / "_trabalho"))
import gerar_overlays_sem_preco as g  # noqa: E402

OUT = Path(__file__).resolve().parent / "overlays"
OUT.mkdir(exist_ok=True)
W, H = g.W, g.H


def novo():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def cx(im, el, y):
    im.alpha_composite(el, ((W - el.width) // 2, int(y)))
    return int(y) + el.height


def caber(el, maxw=680):
    if el.width <= maxw:
        return el
    return el.resize((maxw, int(el.height * maxw / el.width)), Image.LANCZOS)


def faixa(txt, tam, cor=None, fundo=None, ang=0):
    return caber(g.faixa_texto(txt, g.AN, tam, cor or g.OURO, fundo or g.PRETO, padx=20, pady=7, angulo=ang,
                               contorno=g.OURO))


def contorno(txt, tam, cor=None, ang=0, sw=8):
    return caber(g.texto_contorno(txt, g.AN, tam, cor or g.BRANCO, sw=sw, angulo=ang))


def salvar(im, nome):
    im.save(OUT / nome)


def titulos():
    # C2: especialista, rosto no meio -> topo
    im = novo(); y = cx(im, faixa("¿CUÁL ELEGIR?", 96, ang=-2), 40); cx(im, contorno("UNO PARA CADA MOMENTO", 64, g.OURO2), y)
    salvar(im, "titulo_C2.png")
    # C4: amiga no carro -> topo
    im = novo(); cx(im, faixa("¿QUÉ PERFUME TRAES?", 84, ang=2), 40); salvar(im, "titulo_C4.png")
    # C5: educativo
    im = novo(); y = cx(im, faixa("ERROR #1", 100, g.BRANCO, g.VERM, ang=-3), 40)
    cx(im, contorno("CON TU PERFUME", 80), y); salvar(im, "titulo_C5.png")
    # C6: Natal (abre no B-roll do kit)
    im = novo(); y = cx(im, faixa("REGALO DE NAVIDAD", 88, ang=-2), 40)
    cx(im, contorno("RESUELTO", 110, g.OURO2), y); salvar(im, "titulo_C6.png")
    # C7
    im = novo(); y = cx(im, faixa("¿CUÁNTO PAGUÉ?", 96, ang=2), 40)
    cx(im, contorno("NADIE ME CREE", 76, g.OURO2), y); salvar(im, "titulo_C7.png")
    # C3: abre no kit
    im = novo(); y = cx(im, faixa("BLACK FRIDAY", 110, ang=-3), 40)
    cx(im, contorno("PAGA 2 · LLEVA 3", 90, g.OURO2), y); salvar(im, "titulo_C3.png")


def c1():
    textos = [("POV: HUELES A", "VAINILLA Y MANDARINA"), ("…O A", "JAZMÍN Y CARAMELO"),
              ("…O A FRUTOS ROJOS", "PARA LA NOCHE"), ("¿POR QUÉ ELEGIR", "UNO SOLO?")]
    for i, (a, b) in enumerate(textos, 1):
        im = novo(); y = cx(im, contorno(a, 78), 150); cx(im, faixa(b, 72, ang=-2), y + 6)
        salvar(im, f"C1_t{i}.png")
    im = novo(); y = cx(im, faixa("BLACK FRIDAY", 110, ang=-3), 140)
    y = cx(im, contorno("PAGAS 2", 130), y); y = cx(im, contorno("TE LLEVAS 3", 120, g.OURO2), y - 10)
    cx(im, faixa("PAGAS AL RECIBIR", 60, g.BRANCO, g.VERM), y + 10)
    salvar(im, "C1_t5.png")


def c3():
    for i, txt in enumerate(["1", "2", "¡GRATIS!"], 1):
        im = novo()
        el = contorno(txt, 260 if i < 3 else 150, g.BRANCO if i < 3 else g.OURO2, sw=12)
        cx(im, el, 160)
        salvar(im, f"C3_n{i}.png")


if __name__ == "__main__":
    titulos(); c1(); c3()
    print(sorted(p.name for p in OUT.glob("*.png")))
