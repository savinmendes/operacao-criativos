# -*- coding: utf-8 -*-
"""Legenda em caixa palavra a palavra, estilo da selfie do v4 (audio/legenda_es.py, estilo 'c'): maiúsculas, Open Sans SemiBold 44,
caixa preta arredondada justa no texto, caixa roxa na palavra falada. Gera 1 PNG por estado e devolve [(png, ini, fim)]."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
FONTE = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
CAIXA_COR = (14, 14, 14, 252); RAIO = 18
def fonte(tam, peso):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f
F_C = fonte(44, "SemiBold")
def render(ws, ativo, base):
    im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im); f = F_C
    esp = f.getlength(" "); larg = [f.getlength(w) for w in ws]; tot = sum(larg) + esp * (len(ws) - 1)
    x = 360 - tot / 2; pos = []
    for L in larg: pos.append(x); x += L + esp
    d.rounded_rectangle((int(360 - tot / 2 - 26), base - 40 - 16, int(360 + tot / 2 + 26), base + 14 + 12), RAIO, fill=CAIXA_COR)
    x0 = pos[ativo]; d.rounded_rectangle([x0 - 8, base - 54, x0 + larg[ativo] + 8, base + 10], 6, fill=(113, 13, 220, 255))
    for (w, x0) in zip(ws, pos): d.text((x0, base), w, font=f, anchor="ls", fill=(255, 255, 255, 255))
    return im
def gerar(blocos, pasta, base=1178, fim_extra=0.35):
    """blocos = [[(palavra, ini), ...], ...] em tempo do gancho. Último bloco termina em fim_ultimo (passado como palavra ('', t))."""
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True); out = []
    for k, b in enumerate(blocos):
        ws = [w for w, _ in b if w]; ts = [t for w, t in b if w]
        fim_bloco = blocos[k + 1][0][1] if k + 1 < len(blocos) else b[-1][1]
        for i in range(len(ws)):
            ini = 0.0 if (k == 0 and i == 0) else ts[i]
            fim = ts[i + 1] if i + 1 < len(ws) else fim_bloco
            p = pasta / f"leg_{k:02d}_{i}.png"; render(ws, i, base).save(p); out.append((str(p), ini, fim))
    return out
