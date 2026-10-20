# -*- coding: utf-8 -*-
"""Monta lâminas 1080x1350 no estilo 'fundo preto + santo no canto + texto dourado' a partir de um JSON.
Uso: python carrossel.py receita.json
receita: {"santo": "santo.png", "saida": "pasta",
          "slides": [{"texto": "...", "seta": false, "tamanho": 52, "y": 470, "largura": 680}, ...]}
- "→" e "↓" no texto viram setas desenhadas (a Poppins não tem esses glifos).
- O bloco de texto é centralizado em "y" e o tamanho encolhe sozinho até caber entre a linha
  pontilhada de cima e o topo do santo (com margem).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
OURO = (240, 200, 125)
VERMELHO = (220, 30, 30)
FONTE = os.path.join(os.path.dirname(__file__), "Poppins-Bold.ttf")
Y_LINHA_TOPO = 92
Y_LINHA_BASE = H - 100
SANTO_LARG = 455          # largura do santo na lâmina
MARGEM = 46               # folga mínima entre texto e santo / linha
SETAS = {"→", "↓"}


def pontilhado(d, y):
    for x in range(6, W, 17):
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=OURO)


def larg_token(d, t, f, tam):
    return int(tam * 0.85) if t in SETAS else d.textlength(t, font=f)


def larg_linha(d, toks, f, tam):
    esp = d.textlength(" ", font=f)
    return sum(larg_token(d, t, f, tam) for t in toks) + esp * max(len(toks) - 1, 0)


def quebrar(d, texto, f, tam, largura):
    linhas = []
    for par in texto.split("\n"):
        atual = []
        for p in par.split():
            if atual and larg_linha(d, atual + [p], f, tam) > largura:
                # não deixa a seta sozinha numa linha
                if p in SETAS:
                    ult = atual.pop()
                    linhas.append(atual)
                    atual = [ult, p]
                    continue
                linhas.append(atual)
                atual = [p]
            else:
                atual.append(p)
        linhas.append(atual)
    return linhas


def seta_texto(d, x, ybase, tam, tipo):
    """seta dourada do tamanho da letra; x = esquerda, ybase = topo da linha."""
    w = int(tam * 0.85)
    cy = ybase + int(tam * 0.62)
    e = max(4, tam // 9)
    if tipo == "→":
        d.rectangle([x, cy - e, x + w - tam * 0.32, cy + e], fill=OURO)
        d.polygon([(x + w - tam * 0.42, cy - tam * 0.30), (x + w, cy), (x + w - tam * 0.42, cy + tam * 0.30)], fill=OURO)
    else:
        cx = x + w // 2
        top, bot = cy - tam * 0.42, cy + tam * 0.36
        d.rectangle([cx - e, top, cx + e, bot - tam * 0.28], fill=OURO)
        d.polygon([(cx - tam * 0.30, bot - tam * 0.38), (cx + tam * 0.30, bot - tam * 0.38), (cx, bot)], fill=OURO)


def seta_cta(d, cx, cy, s):
    # seta vermelha grande apontando para baixo (CTA do último slide)
    d.rectangle([cx - s // 3, cy - 2 * s, cx + s // 3, cy - s // 2], fill=VERMELHO)
    d.polygon([(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)], fill=VERMELHO)


def montar(r):
    santo = Image.open(r["santo"]).convert("RGBA")
    sw = SANTO_LARG
    sh = int(santo.height * sw / santo.width)
    s = santo.resize((sw, sh), Image.LANCZOS)
    santo_topo = H - sh
    os.makedirs(r["saida"], exist_ok=True)
    for i, sl in enumerate(r["slides"], 1):
        im = Image.new("RGB", (W, H), (0, 0, 0))
        d = ImageDraw.Draw(im)
        pontilhado(d, Y_LINHA_TOPO)
        pontilhado(d, Y_LINHA_BASE)
        im.paste(s, (0, santo_topo), s)          # santo por cima da linha de baixo
        d = ImageDraw.Draw(im)

        tam = sl.get("tamanho", 52)
        largura = sl.get("largura", 680)
        lim_cima = Y_LINHA_TOPO + MARGEM + 10
        lim_baixo = santo_topo - MARGEM
        while True:
            f = ImageFont.truetype(FONTE, tam)
            # equilibra as linhas de cada parágrafo (evita palavra órfã):
            # menor largura que mantém o nº de linhas daquele parágrafo
            linhas = []
            for par in sl["texto"].split("\n"):
                n = len(quebrar(d, par, f, tam, largura))
                lw = largura
                while lw > 300 and len(quebrar(d, par, f, tam, lw - 10)) == n:
                    lw -= 10
                linhas += quebrar(d, par, f, tam, lw)
            passo = int(tam * 1.30)
            alt = len(linhas) * passo
            topo = sl.get("y", 520) - alt // 2
            topo = max(topo, lim_cima)
            topo = min(topo, lim_baixo - alt)
            if topo >= lim_cima or tam <= 30:
                break
            tam -= 2
        esp = d.textlength(" ", font=f)
        for k, toks in enumerate(linhas):
            if not toks:
                continue
            y = topo + k * passo
            x = (W - larg_linha(d, toks, f, tam)) / 2
            for t in toks:
                if t in SETAS:
                    seta_texto(d, x, y, tam, t)
                else:
                    d.text((x, y), t, font=f, fill=OURO)
                x += larg_token(d, t, f, tam) + esp
        fim_texto = topo + alt
        if sl.get("seta"):
            cy = max(fim_texto + 150, santo_topo + 110)
            for cx in (int(W * 0.64), int(W * 0.84)):
                seta_cta(d, cx, cy, 40)
        im.save(os.path.join(r["saida"], f"slide{i}.png"))
        print(f"ok slide{i}: tam={tam} linhas={len(linhas)} texto y {topo}-{fim_texto} | santo topo {santo_topo}")


if __name__ == "__main__":
    montar(json.load(open(sys.argv[1], encoding="utf-8")))
