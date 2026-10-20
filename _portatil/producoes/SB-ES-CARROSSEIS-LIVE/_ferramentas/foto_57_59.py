# -*- coding: utf-8 -*-
"""Lâminas 1080x1350 com FOTO de fundo (AD 57-59). Não substitui o carrossel.py do AD 50.
Uso: python foto_57_59.py receita.json

receita: {"saida": "pasta", "slides": [ {
   "fundo": "img.png",            # imagem base (qualquer tamanho; cobre 1080x1350)
   "cx": 0.5, "cy": 0.5,          # centro do recorte (relativo à imagem base)
   "zoom": 1.0,                   # >1 aproxima
   "desfoque": 0, "escurecer": 0.0,
   "grad_topo": 0, "grad_base": 0,          # altura (px) do degradê escuro em cima / embaixo
   "grad_forca": 0.85,
   "santo": {"x": 0, "largura": 430},       # opcional: santo.png colado no canto inferior
   "textos": [ {"texto": "...", "y": 140, "tamanho": 80, "largura": 960, "x": 540,
                "alt_max": 300, "cor": "branco|ouro|amarelo", "alinhar": "centro|esq|dir",
                "ancora": "centro|topo|base"} ],
   "lista": {"itens": [...], "x": 110, "y0": 140, "y1": 1230, "largura": 860, "tamanho": 34},
   "setas_cta": {"y": 1250, "xs": [690, 900], "s": 40}
} ] }
- "→" e "↓" viram setas desenhadas (a Poppins não tem esses glifos).
- Palavra com prefixo "^" sai em amarelo (destaque), ex.: "^AHORA".
- O texto encolhe sozinho até caber em largura x alt_max.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1350
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, "Poppins-Bold.ttf")
SANTO = os.path.join(AQUI, "santo.png")
CORES = {"branco": (255, 255, 255), "ouro": (240, 200, 125), "amarelo": (255, 214, 0)}
VERMELHO = (220, 30, 30)
SETAS = {"→", "↓"}


def cobrir(img, cx, cy, zoom):
    esc = max(W / img.width, H / img.height) * zoom
    nw, nh = round(img.width * esc), round(img.height * esc)
    im = img.resize((nw, nh), Image.LANCZOS)
    x0 = min(max(round(cx * nw - W / 2), 0), nw - W)
    y0 = min(max(round(cy * nh - H / 2), 0), nh - H)
    return im.crop((x0, y0, x0 + W, y0 + H))


def degrade(im, alt, topo, forca):
    if alt <= 0:
        return im
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for i in range(alt):
        a = int(255 * forca * (1 - i / alt) ** 1.4)
        y = i if topo else H - 1 - i
        d.line([(0, y), (W, y)], fill=a)
    preto = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(preto, im, mask)


def lt(d, t, f, tam):
    return int(tam * 0.85) if t in SETAS else d.textlength(t.lstrip("^"), font=f)


def ll(d, toks, f, tam):
    esp = d.textlength(" ", font=f)
    return sum(lt(d, t, f, tam) for t in toks) + esp * max(len(toks) - 1, 0)


def quebrar(d, texto, f, tam, largura):
    linhas = []
    for par in texto.split("\n"):
        atual = []
        for p in par.split():
            if atual and ll(d, atual + [p], f, tam) > largura:
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


def seta(d, x, ytop, tam, tipo, cor):
    w = int(tam * 0.85)
    cy = ytop + int(tam * 0.62)
    e = max(4, tam // 9)
    if tipo == "→":
        d.rectangle([x, cy - e, x + w - tam * 0.32, cy + e], fill=cor)
        d.polygon([(x + w - tam * 0.42, cy - tam * 0.30), (x + w, cy), (x + w - tam * 0.42, cy + tam * 0.30)], fill=cor)
    else:
        cx = x + w // 2
        top, bot = cy - tam * 0.42, cy + tam * 0.36
        d.rectangle([cx - e, top, cx + e, bot - tam * 0.28], fill=cor)
        d.polygon([(cx - tam * 0.30, bot - tam * 0.38), (cx + tam * 0.30, bot - tam * 0.38), (cx, bot)], fill=cor)


def seta_cta(d, cx, cy, s):
    d.rectangle([cx - s // 3, cy - 2 * s, cx + s // 3, cy - s // 2], fill=VERMELHO)
    d.polygon([(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)], fill=VERMELHO)


def layout(d, texto, tam, largura, alt_max):
    while True:
        f = ImageFont.truetype(FONTE, tam)
        linhas = []
        for par in texto.split("\n"):
            n = len(quebrar(d, par, f, tam, largura))
            lw = largura
            while lw > 300 and len(quebrar(d, par, f, tam, lw - 10)) == n:
                lw -= 10
            linhas += quebrar(d, par, f, tam, lw)
        passo = int(tam * 1.22)
        alt = len(linhas) * passo
        if alt <= alt_max or tam <= 26:
            return f, tam, linhas, passo, alt
        tam -= 2


def desenhar_texto(im, bl):
    """texto com sombra suave (camada borrada) por baixo."""
    d = ImageDraw.Draw(im)
    tam0 = bl.get("tamanho", 60)
    largura = bl.get("largura", 960)
    f, tam, linhas, passo, alt = layout(d, bl["texto"], tam0, largura, bl.get("alt_max", 9999))
    anc = bl.get("ancora", "centro")
    y = bl["y"]
    topo = y - alt // 2 if anc == "centro" else (y if anc == "topo" else y - alt)
    cor = CORES[bl.get("cor", "branco")]
    xc = bl.get("x", W // 2)
    alin = bl.get("alinhar", "centro")
    sombra = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sombra)
    ops = []
    esp = d.textlength(" ", font=f)
    for k, toks in enumerate(linhas):
        if not toks:
            continue
        yy = topo + k * passo
        x = xc if alin == "esq" else (xc - ll(d, toks, f, tam) if alin == "dir" else xc - ll(d, toks, f, tam) / 2)
        for t in toks:
            c = CORES["amarelo"] if t.startswith("^") else cor
            ops.append((x, yy, t, c))
            if t in SETAS:
                seta(ds, x + 2, yy + 3, tam, t, 255)
            else:
                ds.text((x + 2, yy + 3), t.lstrip("^"), font=f, fill=255)
            x += lt(d, t, f, tam) + esp
    sombra = sombra.filter(ImageFilter.GaussianBlur(max(4, tam // 10)))
    im.paste((0, 0, 0), (0, 0), sombra.point(lambda v: min(255, int(v * 1.6))))
    d = ImageDraw.Draw(im)
    for x, yy, t, c in ops:
        if t in SETAS:
            seta(d, x, yy, tam, t, c)
        else:
            d.text((x, yy), t.lstrip("^"), font=f, fill=c)
    return tam, topo, topo + alt


def desenhar_lista(im, ls):
    """lista numerada alinhada à esquerda; número em ouro."""
    d = ImageDraw.Draw(im)
    tam = ls.get("tamanho", 34)
    x0, y0, y1, larg = ls["x"], ls["y0"], ls["y1"], ls["largura"]
    while True:
        f = ImageFont.truetype(FONTE, tam)
        blocos = []
        for i, it in enumerate(ls["itens"], 1):
            num = f"{i}."
            wn = d.textlength(num + " ", font=f)
            ls_ = quebrar(d, it, f, tam, larg - wn)
            blocos.append((num, wn, ls_))
        passo = int(tam * 1.18)
        gap = int(tam * 0.62)
        alt = sum(len(b[2]) * passo for b in blocos) + gap * (len(blocos) - 1)
        if alt <= (y1 - y0) or tam <= 22:
            break
        tam -= 1
    y = y0 + ((y1 - y0) - alt) // 2
    sombra = Image.new("L", (W, H), 0)
    ds = ImageDraw.Draw(sombra)
    ops = []
    for num, wn, linhas in blocos:
        ops.append((x0, y, num, CORES["ouro"]))
        for k, toks in enumerate(linhas):
            ops.append((x0 + wn, y + k * passo, " ".join(toks), CORES["branco"]))
        y += len(linhas) * passo + gap
    for x, yy, t, c in ops:
        ds.text((x + 2, yy + 3), t, font=f, fill=255)
    sombra = sombra.filter(ImageFilter.GaussianBlur(4))
    im.paste((0, 0, 0), (0, 0), sombra.point(lambda v: min(255, int(v * 1.6))))
    d = ImageDraw.Draw(im)
    for x, yy, t, c in ops:
        d.text((x, yy), t, font=f, fill=c)
    return tam, alt


def montar(r):
    os.makedirs(r["saida"], exist_ok=True)
    for i, sl in enumerate(r["slides"], 1):
        base = Image.open(sl["fundo"]).convert("RGB")
        im = cobrir(base, sl.get("cx", 0.5), sl.get("cy", 0.5), sl.get("zoom", 1.0))
        if sl.get("desfoque"):
            im = im.filter(ImageFilter.GaussianBlur(sl["desfoque"]))
        if sl.get("escurecer"):
            im = Image.blend(im, Image.new("RGB", (W, H), (0, 0, 0)), sl["escurecer"])
        fz = sl.get("grad_forca", 0.85)
        im = degrade(im, sl.get("grad_topo", 0), True, fz)
        im = degrade(im, sl.get("grad_base", 0), False, fz)
        if sl.get("santo"):
            s = Image.open(SANTO).convert("RGBA")
            sw = sl["santo"].get("largura", 430)
            sh = int(s.height * sw / s.width)
            s = s.resize((sw, sh), Image.LANCZOS)
            im.paste(s, (sl["santo"].get("x", 0), H - sh), s)
        info = []
        for bl in sl.get("textos", []):
            info.append(desenhar_texto(im, bl))
        if sl.get("lista"):
            info.append(desenhar_lista(im, sl["lista"]))
        if sl.get("setas_cta"):
            c = sl["setas_cta"]
            d = ImageDraw.Draw(im)
            for cx in c.get("xs", [690, 900]):
                seta_cta(d, cx, c["y"], c.get("s", 40))
        im.save(os.path.join(r["saida"], f"slide{i}.png"))
        print(f"ok slide{i}: {info}")
    # folha de contato
    ims = [Image.open(os.path.join(r["saida"], f"slide{i}.png")) for i in range(1, len(r["slides"]) + 1)]
    tw, th = 540, 675
    folha = Image.new("RGB", (tw * len(ims) + 10 * (len(ims) - 1), th), (60, 60, 60))
    for k, m in enumerate(ims):
        folha.paste(m.resize((tw, th), Image.LANCZOS), (k * (tw + 10), 0))
    folha.save(os.path.join(r["saida"], "_contato.jpg"), quality=88)


if __name__ == "__main__":
    montar(json.load(open(sys.argv[1], encoding="utf-8")))
