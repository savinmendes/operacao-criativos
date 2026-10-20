# -*- coding: utf-8 -*-
"""Lâminas 1080x1350 com IMAGEM gerada (sem texto) + texto por script (agente AD 54-56).
Baseado no carrossel.py do AD 50 (mesma fonte e setas desenhadas), mas com fundo de foto.
Uso: python lamina_foto.py receita.json
receita: {"saida": "pasta", "fonte": "Poppins-Bold.ttf",
  "slides": [{
     "img": "arquivo.png",
     "modo": "topo" | "cheia",      # topo: imagem em cima, degradê pro preto embaixo; cheia: imagem na lâmina toda
     "alt_img": 980,                # (topo) altura da imagem na lâmina
     "cx": 0.5,                     # centro horizontal do recorte (0-1 da imagem original)
     "cy": 0.5,                     # (cheia) centro vertical
     "zoom": 1.0,                   # zoom extra
     "escurecer": 0.0,              # 0-1, véu preto por cima da imagem
     "desfocar": 0,                 # raio de blur
     "fundo": [r,g,b],              # (topo) cor do fundo abaixo da imagem (padrão preto)
     "veu_base": [y0, y1, alfa],    # (opcional) degradê preto de y0 a y1 até alfa (0-255), sólido abaixo de y1
     "blocos": [{"texto": "...", "caixa": [x0, y0, x1, y1], "tamanho": 54, "cor": [255,255,255],
                 "alinhar": "centro"|"esquerda", "valign": "centro"|"topo"|"base", "entrelinha": 1.25}],
     "seta_cta": [y_centro, [x1, x2]]   # setas vermelhas apontando pra baixo
  }]}
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
VERMELHO = (220, 30, 30)
SETAS = {"→", "↓"}
AQUI = os.path.dirname(os.path.abspath(__file__))


def base(sl, raiz):
    im = Image.open(os.path.join(raiz, sl["img"])).convert("RGB")
    z = sl.get("zoom", 1.0)
    fundo = tuple(sl.get("fundo", (0, 0, 0)))
    canvas = Image.new("RGB", (W, H), fundo)
    if sl.get("modo", "topo") == "cheia":
        esc = max(W / im.width, H / im.height) * z
        r = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
        x0 = int(min(max(sl.get("cx", 0.5) * r.width - W / 2, 0), r.width - W))
        y0 = int(min(max(sl.get("cy", 0.5) * r.height - H / 2, 0), r.height - H))
        canvas.paste(r.crop((x0, y0, x0 + W, y0 + H)), (0, 0))
    else:
        ah = sl.get("alt_img", 980)
        esc = max(ah / im.height, W / im.width) * z
        r = im.resize((round(im.width * esc), round(im.height * esc)), Image.LANCZOS)
        x0 = int(min(max(sl.get("cx", 0.5) * r.width - W / 2, 0), r.width - W))
        y0 = int(min(max(sl.get("cy", 0.0) * r.height - ah / 2, 0), r.height - ah)) if "cy" in sl else 0
        canvas.paste(r.crop((x0, y0, x0 + W, y0 + ah)), (0, 0))
        # degradê da base da imagem para o preto
        fade = sl.get("fade", 260)
        g = Image.new("L", (1, fade))
        for k in range(fade):
            g.putpixel((0, k), int(255 * (k / fade) ** 1.3))
        preto = Image.new("RGB", (W, fade), fundo)
        canvas.paste(preto, (0, ah - fade), g.resize((W, fade)))
    canvas = canvas.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    if sl.get("desfocar"):
        canvas = canvas.filter(ImageFilter.GaussianBlur(sl["desfocar"]))
    if sl.get("escurecer"):
        canvas = Image.blend(canvas, Image.new("RGB", (W, H), (0, 0, 0)), sl["escurecer"])
    if sl.get("veu_base"):
        y0, y1, a = sl["veu_base"]
        m = Image.new("L", (W, H), 0)
        dm = ImageDraw.Draw(m)
        for y in range(y0, H):
            v = a if y >= y1 else int(a * ((y - y0) / max(y1 - y0, 1)) ** 1.2)
            dm.line([(0, y), (W, y)], fill=v)
        canvas.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), m)
    return canvas


def larg_token(d, t, f, tam):
    return int(tam * 0.85) if t in SETAS else d.textlength(t, font=f)


def larg_linha(d, toks, f, tam):
    esp = d.textlength(" ", font=f)
    return sum(larg_token(d, t, f, tam) for t in toks) + esp * max(len(toks) - 1, 0)


def quebrar(d, texto, f, tam, largura):
    linhas = []
    for par in texto.split("\n"):
        atual = []
        for p in [q for q in par.split(" ") if q]:
            if atual and larg_linha(d, atual + [p], f, tam) > largura:
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


def seta_texto(d, x, ybase, tam, tipo, cor, contorno):
    w = int(tam * 0.85)
    cy = ybase + int(tam * 0.62)
    e = max(4, tam // 9)
    for (c, s) in ((contorno, 3), (cor, 0)):
        if tipo == "→":
            d.rectangle([x - s, cy - e - s, x + w - tam * 0.32 + s, cy + e + s], fill=c)
            d.polygon([(x + w - tam * 0.42 - s, cy - tam * 0.30 - s * 1.6), (x + w + s * 1.6, cy),
                       (x + w - tam * 0.42 - s, cy + tam * 0.30 + s * 1.6)], fill=c)
        else:
            cx = x + w // 2
            top, bot = cy - tam * 0.42, cy + tam * 0.36
            d.rectangle([cx - e - s, top - s, cx + e + s, bot - tam * 0.28 + s], fill=c)
            d.polygon([(cx - tam * 0.30 - s * 1.6, bot - tam * 0.38 - s), (cx + tam * 0.30 + s * 1.6, bot - tam * 0.38 - s),
                       (cx, bot + s * 1.6)], fill=c)


def seta_cta(d, cx, cy, s):
    d.rectangle([cx - s // 3, cy - 2 * s, cx + s // 3, cy - s // 2], fill=VERMELHO)
    d.polygon([(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)], fill=VERMELHO)


def bloco(im, b, fonte):
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = b["caixa"]
    largura, altura = x1 - x0, y1 - y0
    tam = b.get("tamanho", 54)
    ent = b.get("entrelinha", 1.25)
    cor = tuple(b.get("cor", (255, 255, 255)))
    contorno = tuple(b.get("contorno", (0, 0, 0)))
    while True:
        f = ImageFont.truetype(fonte, tam)
        linhas = []
        for par in b["texto"].split("\n"):
            n = len(quebrar(d, par, f, tam, largura))
            lw = largura
            if b.get("equilibrar", True):
                while lw > 260 and len(quebrar(d, par, f, tam, lw - 10)) == n:
                    lw -= 10
            linhas += quebrar(d, par, f, tam, lw)
        passo = int(tam * ent)
        alt = len(linhas) * passo - int(tam * (ent - 1.0))
        maxw = max(larg_linha(d, l, f, tam) for l in linhas if l) if any(linhas) else 0
        if (alt <= altura and maxw <= largura) or tam <= 26:
            break
        tam -= 2
    va = b.get("valign", "centro")
    topo = y0 if va == "topo" else (y1 - alt if va == "base" else y0 + (altura - alt) // 2)
    esp = d.textlength(" ", font=f)
    sw = max(2, tam // 14)
    for k, toks in enumerate(linhas):
        if not toks:
            continue
        y = topo + k * passo
        lw = larg_linha(d, toks, f, tam)
        x = x0 if b.get("alinhar") == "esquerda" else x0 + (largura - lw) / 2
        for t in toks:
            if t in SETAS:
                seta_texto(d, x, y, tam, t, cor, contorno)
            else:
                d.text((x, y), t, font=f, fill=cor, stroke_width=sw, stroke_fill=contorno)
            x += larg_token(d, t, f, tam) + esp
    return tam, topo, topo + alt


def montar(r, raiz):
    fonte = os.path.join(raiz, r.get("fonte", "Poppins-Bold.ttf"))
    saida = os.path.join(raiz, r["saida"])
    os.makedirs(saida, exist_ok=True)
    for i, sl in enumerate(r["slides"], 1):
        im = base(sl, raiz)
        info = []
        for b in sl.get("blocos", []):
            info.append(bloco(im, b, fonte))
        if sl.get("seta_cta"):
            d = ImageDraw.Draw(im)
            cy, xs = sl["seta_cta"]
            for cx in xs:
                seta_cta(d, cx, cy, sl.get("seta_tam", 40))
        im.save(os.path.join(saida, f"slide{i}.png"))
        print(f"ok slide{i}: " + " | ".join(f"tam={t} y {a}-{b_}" for t, a, b_ in info))


if __name__ == "__main__":
    rec = os.path.abspath(sys.argv[1])
    montar(json.load(open(rec, encoding="utf-8")), os.path.dirname(rec))
