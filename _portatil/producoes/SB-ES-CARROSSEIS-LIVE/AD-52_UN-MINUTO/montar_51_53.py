# -*- coding: utf-8 -*-
"""Monta as lâminas 1080x1350 dos ADs 51, 52 e 53 (San Benito ES, oferta oração ao vivo).
Uso: python montar_51_53.py <51|52|53|todos>
Base: imagens geradas no ElevenLabs (gpt-image-2.5-sunburst) em AD-NN_*/_base/, upscale local Real-ESRGAN.
Todo texto é desenhado aqui (Poppins-Bold; setas → ↓ desenhadas como no _ferramentas/carrossel.py).
Cópia idêntica deste script fica em cada pasta de AD."""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

RAIZ = "C:/Users/PICHAU/Downloads/SB-ES-CARROSSEIS-LIVE"
FERR = RAIZ + "/_ferramentas"
FONTE = FERR + "/Poppins-Bold.ttf"
FONTE_MAO = "C:/Windows/Fonts/Inkfree.ttf"   # "escrito à caneta" na palma (AD 51)
W, H = 1080, 1350
OURO = (240, 200, 125)
BRANCO = (255, 255, 255)
VERMELHO = (220, 30, 30)
MARROM = (62, 34, 14)
SETAS = {"→", "↓"}
PASTA = {51: RAIZ + "/AD-51_SENAL-DE-DIOS", 52: RAIZ + "/AD-52_UN-MINUTO", 53: RAIZ + "/AD-53_MANDO-AVISAR"}


# ---------------- texto ----------------
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


def linhas_equilibradas(d, texto, f, tam, largura):
    out = []
    for par in texto.split("\n"):
        n = len(quebrar(d, par, f, tam, largura))
        lw = largura
        while lw > 260 and len(quebrar(d, par, f, tam, lw - 10)) == n:
            lw -= 10
        out += quebrar(d, par, f, tam, lw)
    return out


def seta_texto(d, x, ytop, tam, tipo, cor):
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


def bloco(im, texto, caixa, cor, tam=56, minimo=26, sombra=None, entrelinha=1.28, fonte=FONTE, alinhar="centro"):
    """Escreve 'texto' centralizado dentro de caixa=(x0,y0,x1,y1); encolhe até caber. Devolve (y_ini, y_fim, tam)."""
    x0, y0, x1, y1 = caixa
    d = ImageDraw.Draw(im)
    while True:
        f = ImageFont.truetype(fonte, tam)
        linhas = linhas_equilibradas(d, texto, f, tam, x1 - x0)
        passo = int(tam * entrelinha)
        alt = len(linhas) * passo - int(tam * (entrelinha - 1.0))
        if (alt <= y1 - y0 and all(larg_linha(d, l, f, tam) <= x1 - x0 for l in linhas)) or tam <= minimo:
            break
        tam -= 2
    topo = y0 + (y1 - y0 - alt) // 2 if alinhar == "centro" else y0
    esp = d.textlength(" ", font=f)
    if sombra:
        cam = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(cam)
    for k, toks in enumerate(linhas):
        if not toks:
            continue
        y = topo + k * passo
        x = x0 + (x1 - x0 - larg_linha(d, toks, f, tam)) / 2
        for t in toks:
            for (dd, c) in ([(ds, sombra)] if sombra else []) + [(None, cor)]:
                if dd is None:
                    continue
                if t in SETAS:
                    seta_texto(dd, x + 3, y + 3, tam, t, c)
                else:
                    dd.text((x + 3, y + 3), t, font=f, fill=c)
            x += larg_token(d, t, f, tam) + esp
    if sombra:
        cam = cam.filter(ImageFilter.GaussianBlur(6))
        im.paste(cam, (0, 0), cam)
        d = ImageDraw.Draw(im)
    for k, toks in enumerate(linhas):
        if not toks:
            continue
        y = topo + k * passo
        x = x0 + (x1 - x0 - larg_linha(d, toks, f, tam)) / 2
        for t in toks:
            if t in SETAS:
                seta_texto(d, x, y, tam, t, cor)
            else:
                d.text((x, y), t, font=f, fill=cor)
            x += larg_token(d, t, f, tam) + esp
    return topo, topo + alt, tam


def seta_cta(d, cx, cy, s, cor=VERMELHO):
    d.rectangle([cx - s // 3, cy - 2 * s, cx + s // 3, cy - s // 2], fill=cor)
    d.polygon([(cx - s, cy - s // 2), (cx + s, cy - s // 2), (cx, cy + s)], fill=cor)


def seta_longa(d, cx, cy, comp, cor=BRANCO, esp=5):
    """seta branca fina →, como nas referências (indicar deslizar)."""
    x0, x1 = cx - comp // 2, cx + comp // 2
    d.rectangle([x0, cy - esp // 2, x1 - 18, cy + esp // 2], fill=cor)
    d.polygon([(x1 - 26, cy - 14), (x1, cy), (x1 - 26, cy + 14)], fill=cor)


# ---------------- imagem ----------------
def base(caminho, cx=0.5, cy=0.5, larg_rel=None):
    """Recorta 4:5 da imagem (já com upscale) e redimensiona para 1080x1350.
    larg_rel: fração da largura usada no recorte (<= altura*0.8/largura); padrão = máximo possível."""
    im = Image.open(caminho).convert("RGB")
    w, h = im.size
    cw = int(min(h * 0.8, w) if larg_rel is None else w * larg_rel)
    ch = int(cw * 1.25)
    ch = min(ch, h); cw = int(ch * 0.8)
    x = int(min(max(cx * w - cw / 2, 0), w - cw))
    y = int(min(max(cy * h - ch / 2, 0), h - ch))
    return im.crop((x, y, x + cw, y + ch)).resize((W, H), Image.LANCZOS)


def base_estendida(caminho, x0, lado, ext_baixo, faixa=120):
    """Recorte quadrado (x0, lado) da imagem 2x -> 1080x1080 e estica as últimas 'faixa' linhas
    para completar 1350 (fundo/pergaminho/hábito liso na base)."""
    im = Image.open(caminho).convert("RGB")
    h = im.height
    q = im.crop((x0, h - lado, x0 + lado, h)).resize((W, W), Image.LANCZOS)
    out = Image.new("RGB", (W, H))
    corte = W - faixa
    out.paste(q.crop((0, 0, W, corte)), (0, 0))
    out.paste(q.crop((0, corte, W, W)).resize((W, H - corte), Image.LANCZOS), (0, corte))
    return out


def base_parchment(caminho, borda=0.24):
    """Junta a faixa esquerda e a direita (com os cantos de moedas/trevos) num 4:5, emenda suave."""
    im = Image.open(caminho).convert("RGB")
    w, h = im.size
    cw = int(h * 0.8)
    meia = cw // 2
    esq = im.crop((0, 0, meia + 60, h))
    dir_ = im.crop((w - meia - 60, 0, w, h))
    out = Image.new("RGB", (cw, h))
    out.paste(esq, (0, 0))
    mask = Image.linear_gradient("L").rotate(90).resize((120, h))   # 0 à esquerda -> 255 à direita
    tmp = out.crop((meia - 60, 0, meia + 60, h))
    tmp.paste(dir_.crop((0, 0, 120, h)), (0, 0), mask)
    out.paste(dir_, (meia - 60, 0))
    out.paste(tmp, (meia - 60, 0))
    return out.resize((W, H), Image.LANCZOS)


def base_quadrada_topo(caminho, x0, lado=1440):
    """Recorte quadrado da imagem 2x -> 1080x1080 no topo; base preta de 270 px para o texto."""
    im = Image.open(caminho).convert("RGB")
    q = im.crop((x0, im.height - lado, x0 + lado, im.height)).resize((W, W), Image.LANCZOS)
    out = Image.new("RGB", (W, H), (0, 0, 0))
    out.paste(q, (0, 0))
    return out


def degrade_baixo(im, ini, fim=H, cor=(0, 0, 0), alfa_max=235):
    cam = Image.new("RGBA", (W, H), cor + (0,))
    d = ImageDraw.Draw(cam)
    for y in range(ini, fim):
        a = int(alfa_max * min(1, (y - ini) / max(1, (fim - ini) * 0.55)))
        d.line([(0, y), (W, y)], fill=cor + (a,))
    im.paste(cam, (0, 0), cam)


def texto_na_palma(im, texto, centro, larg, angulo, tam, cor=(25, 40, 135)):
    """Texto 'à caneta' na palma: camada girada, levemente borrada, multiplicada sobre a pele."""
    cam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(cam)
    f = ImageFont.truetype(FONTE_MAO, tam)
    linhas = texto.split("\n")
    passo = int(tam * 1.18)
    alt = passo * len(linhas)
    y = centro[1] - alt // 2
    for ln in linhas:
        lw = d.textlength(ln, font=f)
        d.text((centro[0] - lw / 2, y), ln, font=f, fill=cor + (215,), stroke_width=1, stroke_fill=cor + (215,))
        y += passo
    cam = cam.rotate(angulo, resample=Image.BICUBIC, center=centro)
    cam = cam.filter(ImageFilter.GaussianBlur(0.7))
    im.paste(cam, (0, 0), cam)


# ---------------- slide CTA estilo AD 50 (fundo preto + santo no canto) ----------------
def slide_cta_santo(texto, saida, y_centro=520):
    santo = Image.open(FERR + "/santo.png").convert("RGBA")
    sw = 455
    sh = int(santo.height * sw / santo.width)
    s = santo.resize((sw, sh), Image.LANCZOS)
    im = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(im)
    for yl in (92, H - 100):
        for x in range(6, W, 17):
            d.ellipse([x - 5, yl - 5, x + 5, yl + 5], fill=OURO)
    im.paste(s, (0, H - sh), s)
    t0, t1, tam = bloco(im, texto, (200, 92 + 56, 880, H - sh - 46), OURO, tam=54)
    d = ImageDraw.Draw(im)
    cy = max(t1 + 150, H - sh + 110)
    for cx in (int(W * 0.64), int(W * 0.84)):
        seta_cta(d, cx, cy, 40)
    im.save(saida)
    print("ok", saida, "tam", tam, "texto", t0, t1)


# ---------------- ADs ----------------
def ad51():
    p = PASTA[51]
    # 1: palma + medalha
    im = base(p + "/_base/palma_x2.png", **CFG51["palma"])
    texto_na_palma(im, "¿PEDISTE UNA\nSEÑAL DE DIOS?\nDESLIZA PARA\nVER LA RESPUESTA", **CFG51["palma_txt"])
    im.save(p + "/slide1.png")
    # 2: santo com pergaminho
    im = base_estendida(p + "/_base/pergaminho_x2.png", **CFG51["santo"])
    bloco(im, "SÉ TODO LO QUE ESTÁS PASANDO.\n"
              "RECIBE LA BENDICIÓN DE SAN BENITO Y COMPÁRTELA CON QUIEN NECESITA PROSPERIDAD.\n"
              "LAS BENDICIONES SE MULTIPLICAN CUANDO SE COMPARTEN. RECIBIRÁS UNA SORPRESA INESPERADA →",
          CFG51["caixa_pergaminho"], MARROM, tam=44, entrelinha=1.25)
    im.save(p + "/slide2.png")
    # 3: CTA live
    slide_cta_santo("¿PEDISTE UNA SEÑAL? ESTÁ SUCEDIENDO AHORA: LA ORACIÓN DE SAN BENITO SE ESTÁ REZANDO EN VIVO.\n\n"
                    "TOCA EN «MÁS INFORMACIÓN» Y ÚNETE ↓", p + "/slide3.png")


def ad52():
    p = PASTA[52]
    for i, (arq, txt) in enumerate([("lagrima_x2.png", "¿TIENES UN MINUTO PARA SAN BENITO?"),
                                    ("olhos_x2.png", "ENTONCES HAGAMOS ESTA ORACIÓN")], 1):
        im = base_quadrada_topo(p + "/_base/" + arq, **CFG52["retrato"])
        degrade_baixo(im, 820, 1080, alfa_max=255)
        t0, t1, _ = bloco(im, txt, (110, 1060, 970, 1220), BRANCO, tam=60, sombra=(0, 0, 0, 255))
        seta_longa(ImageDraw.Draw(im), W // 2, t1 + 70, 260)
        im.save(p + f"/slide{i}.png")
    perg = p + "/_base/parchment_x2.png"
    im = base_parchment(perg)
    bloco(im, "OH GLORIOSO SAN BENITO, ROMPE LAS CADENAS DE LA ESCASEZ QUE ME ATAN. "
              "ABRE LOS CAMINOS DE LA PROVISIÓN Y LA ABUNDANCIA. LÍBRAME DE TODA DEUDA Y OPRESIÓN FINANCIERA. "
              "QUE TU CRUZ SAGRADA SEA MI LUZ EN LA OSCURIDAD. AMÉN.\n\nDESLIZA →",
          CFG52["caixa_parchment"], MARROM, tam=54)
    im.save(p + "/slide3.png")
    im = base_parchment(perg)
    t0, t1, _ = bloco(im, "ESTA ORACIÓN SE ESTÁ REZANDO EN VIVO EN ESTE MOMENTO.\n\n"
                          "TOCA EN «MÁS INFORMACIÓN» Y REZA CON NOSOTROS AHORA ↓",
                      CFG52["caixa_cta"], MARROM, tam=60)
    d = ImageDraw.Draw(im)
    for cx in (int(W * 0.38), int(W * 0.62)):
        seta_cta(d, cx, CFG52["y_setas"], 44)
    im.save(p + "/slide4.png")


def ad53():
    p = PASTA[53]
    im = base(p + "/_base/medalha_x2.png", **CFG53["base"])
    degrade_baixo(im, CFG53["deg"])
    t0, t1, _ = bloco(im, "SAN BENITO CON SU MEDALLA MANDÓ AVISAR: LOS CAMINOS DE TU VIDA FINANCIERA SE VAN A ABRIR.",
                      CFG53["caixa"], BRANCO, tam=60, sombra=(0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    a0, a1, _ = bloco(im, "CREE Y CONFIRMA: ¡AMÉN!", (140, t1 + 22, 940, t1 + 72), OURO, tam=36)
    c0, c1, _ = bloco(im, "LA ORACIÓN DE SAN BENITO SE ESTÁ REZANDO EN VIVO AHORA. "
                          "TOCA EN «MÁS INFORMACIÓN» Y ENTRA ↓",
                      (150, a1 + 26, 760, H - 40), OURO, tam=32, minimo=24)
    d = ImageDraw.Draw(im)
    for cx in (850, 960):
        seta_cta(d, cx, (c0 + c1) // 2 + 18, 30)
    im.save(p + "/slide1.png")


# parâmetros de recorte/caixa (ajustados olhando cada imagem)
CFG51 = {"palma": {"cx": 0.43}, "palma_txt": {"centro": (430, 900), "larg": 400, "angulo": 8, "tam": 56},
         "santo": {"x0": 460, "lado": 1440, "ext_baixo": 270}, "caixa_pergaminho": (300, 560, 920, 1290)}
CFG52 = {"retrato": {"x0": 860}, "caixa_parchment": (130, 170, 950, 1180), "caixa_cta": (130, 260, 950, 860), "y_setas": 1060}
CFG53 = {"base": {"cx": 0.44}, "deg": 760, "caixa": (80, 930, 1000, 1130)}

if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "todos"
    for n, fn in ((51, ad51), (52, ad52), (53, ad53)):
        if alvo in ("todos", str(n)):
            fn()
