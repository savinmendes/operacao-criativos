# -*- coding: utf-8 -*-
"""Overlays do gancho G5 (Noticia TV): faixa ÚLTIMA HORA, selo VIDEO DE FIELES e legenda em caixa palavra a palavra (estilo v4)."""
import json, re, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
AQ = Path(__file__).resolve().parent
OUT = AQ / "overlays"; OUT.mkdir(exist_ok=True)
FONTE = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
W, H = 720, 1280
def fonte(tam, peso):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f

def faixa():
    """lower third de telejornal: etiqueta 'ÚLTIMA HORA' + barra vermelha com a manchete em 2 linhas"""
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y0 = 870
    fe = fonte(30, "ExtraBold")
    d.rectangle([24, y0, 24 + int(fe.getlength("ÚLTIMA HORA")) + 36, y0 + 48], fill=(255, 255, 255, 255))
    d.text((42, y0 + 24), "ÚLTIMA HORA", font=fe, anchor="lm", fill=(196, 0, 0, 255))
    fm = fonte(38, "Bold")
    linhas = ["SACERDOTE RETIRADO DE SU PARROQUIA", "POR ENSEÑAR UNA ORACIÓN"]
    # ajusta a fonte para caber em 672 px
    while max(fm.getlength(l) for l in linhas) > 660:
        fm = fonte(fm.size - 1, "Bold")
    y1 = y0 + 48
    d.rectangle([0, y1, W, y1 + 116], fill=(200, 8, 8, 248))
    d.rectangle([0, y1 + 116, W, y1 + 122], fill=(255, 255, 255, 235))
    for i, l in enumerate(linhas):
        d.text((24, y1 + 32 + i * 52), l, font=fm, anchor="lm", fill=(255, 255, 255, 255))
    im.save(OUT / "faixa_ultima_hora.png")
    return y1 + 122

def selo_fieles():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    f = fonte(24, "Bold"); t = "VIDEO DE FIELES"
    x0, y0 = 22, 60
    w = int(f.getlength(t)) + 44
    d.rounded_rectangle([x0, y0, x0 + w, y0 + 40], 6, fill=(200, 8, 8, 235))
    d.ellipse([x0 + 12, y0 + 15, x0 + 22, y0 + 25], fill=(255, 255, 255, 255))
    d.text((x0 + 30, y0 + 20), t, font=f, anchor="lm", fill=(255, 255, 255, 255))
    im.save(OUT / "selo_video_fieles.png")

F_G = fonte(46, "SemiBold"); CAIXA = (14, 14, 14, 252)
def legenda(palavras, base_ancora, base_ins, t_ins):
    """palavras: [{w, ini, fim}] em tempo do gancho. blocos <=3 palavras / 16 car. -> PNGs + lista (png, ini, fim)"""
    out, cur = [], []
    for p in palavras:
        cur.append(p); txt = " ".join(x["w"] for x in cur)
        if len(cur) >= 3 or len(txt) >= 16 or re.search(r"[,.:;!?]$", p["w"]):
            out.append(cur); cur = []
    if cur: out.append(cur)
    itens = []
    for k, b in enumerate(out):
        fim_b = min(out[k + 1][0]["ini"] if k + 1 < len(out) else 1e9, b[-1]["fim"] + 0.45)
        ws = [re.sub(r"[,.:;!?¡¿]+", "", x["w"]).upper() for x in b]
        base = base_ins if b[0]["ini"] >= t_ins - 0.05 else base_ancora
        for j, x in enumerate(b):
            ini = 0.0 if (k == 0 and j == 0) else x["ini"]
            fim = b[j + 1]["ini"] if j + 1 < len(b) else fim_b
            im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            esp = F_G.getlength(" "); larg = [F_G.getlength(w) for w in ws]; tot = sum(larg) + esp * (len(ws) - 1)
            d.rounded_rectangle((int(360 - tot / 2 - 26), base - 38 - 16, int(360 + tot / 2 + 26), base + 14 + 12), 18, fill=CAIXA)
            xx = 360 - tot / 2
            for i, (w, L) in enumerate(zip(ws, larg)):
                d.text((xx, base), w, font=F_G, anchor="ls", fill=(244, 242, 23, 255) if i == j else (255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
                xx += L + esp
            p = OUT / f"leg_{k:02d}_{j}.png"; im.save(p)
            itens.append({"png": str(p), "ini": round(ini, 3), "fim": round(fim, 3)})
    return itens

if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    yb = faixa(); selo_fieles()
    itens = legenda(cfg["palavras"], cfg["base_ancora"], cfg["base_ins"], cfg["t_ins"])
    json.dump(itens, open(OUT / "legenda_itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("faixa ate y", yb, "| legenda:", len(itens), "pngs")
