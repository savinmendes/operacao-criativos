# -*- coding: utf-8 -*-
"""Legenda ES palavra a palavra nos 3 estilos do original (gancho / padre chorando / padre de roxo)."""
import json, re
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent
FONTE = str(AQ.parent.parent / "_trabalho_colar" / "fonts" / "OpenSans.ttf")
FIM_GANCHO, FIM_CHORA = 7.38, 21.95
def fonte(tam, peso):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f
F_G = fonte(40, "SemiBold"); F_C = fonte(44, "SemiBold"); F_R = fonte(53, "Regular")
def estilo(t): return "g" if t < FIM_GANCHO else ("c" if t < FIM_CHORA else "r")
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p)
        txt = " ".join(x["w"] for x in cur)
        fim = re.search(r"[,.:;!?]$", p["w"]) is not None
        if len(cur) >= 3 or len(txt) >= 16 or fim:
            out.append(cur); cur = []
    if cur: out.append(cur)
    # não deixa 1 palavra curta sozinha se couber no anterior
    res = []
    for b in out:
        if res and len(b) == 1 and len(b[0]["w"]) <= 3 and len(" ".join(x["w"] for x in res[-1] + b)) <= 20 and not re.search(r"[,.:;!?]$", res[-1][-1]["w"]) and estilo(res[-1][0]["ini"]) == estilo(b[0]["ini"]):
            res[-1] = res[-1] + b
        else: res.append(b)
    return res
def limpa(w, st):
    w = w.strip()
    w = re.sub(r"[,.:;]+$", "", w) if st == "r" else re.sub(r"[,.:;!?¡¿]+", "", w)
    if st == "r": w = w.replace("¡", "").replace("!", "").replace("¿", "").replace("?", "")
    return w.upper() if st in "gc" else w
class Legenda:
    def __init__(self, pal_json):
        pal = json.load(open(pal_json, encoding="utf-8"))
        self.bl = []
        pal = [p for p in pal if not (48.2 <= p["ini"] < 61.4)]  # cartão das 12 palavras: o original não tem legenda
        bs = blocos(pal)
        for i, b in enumerate(bs):
            ini = b[0]["ini"]; prox = bs[i + 1][0]["ini"] if i + 1 < len(bs) else 1e9
            fim = min(prox, b[-1]["fim"] + 0.45)
            st = estilo(ini)
            # bloco não atravessa troca de estilo
            if st == "g": fim = min(fim, FIM_GANCHO)
            if st == "c": fim = min(fim, FIM_CHORA)
            self.bl.append({"ini": ini, "fim": fim, "st": st, "ws": [(limpa(x["w"], st), x["ini"]) for x in b]})
    def estado(self, t):
        for k, b in enumerate(self.bl):
            if b["ini"] <= t < b["fim"]:
                ativo = max(i for i, (_, wi) in enumerate(b["ws"]) if wi <= t) if b["st"] in "gc" else -1
                return (k, ativo)
        return None
    @lru_cache(maxsize=64)
    def imagem(self, k, ativo):
        b = self.bl[k]; ws = [w for w, _ in b["ws"] if w]; st = b["st"]
        im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0))
        if st == "r":
            t = " ".join(ws); yb = 937 if 76.03 <= b["ini"] < 87.4 else 819
            sh = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
            d.text((361, yb + 2), t, font=F_R, anchor="ms", fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(2.2))
            ImageDraw.Draw(sh).text((360, yb), t, font=F_R, anchor="ms", fill=(255, 255, 255, 255))
            return sh
        f = F_G if st == "g" else F_C; base = 689 if st == "g" else 1081
        d = ImageDraw.Draw(im); esp = f.getlength(" ")
        larg = [f.getlength(w) for w in ws]; tot = sum(larg) + esp * (len(ws) - 1); x = 360 - tot / 2
        pos = []
        for w, L in zip(ws, larg): pos.append(x); x += L + esp
        if st == "g":
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            for (w, x0) in zip(ws, pos): ds.text((x0, base), w, font=f, anchor="ls", fill=(0, 0, 0, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
            sh = sh.filter(ImageFilter.GaussianBlur(1.6)); im = Image.alpha_composite(im, sh); d = ImageDraw.Draw(im)
            for i, (w, x0) in enumerate(zip(ws, pos)):
                d.text((x0, base), w, font=f, anchor="ls", fill=(244, 242, 23, 255) if i == ativo else (255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        else:
            sh = Image.new("RGBA", im.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            for (w, x0) in zip(ws, pos): ds.text((x0 + 1, base + 2), w, font=f, anchor="ls", fill=(0, 0, 0, 170))
            sh = sh.filter(ImageFilter.GaussianBlur(2.5)); im = Image.alpha_composite(im, sh); d = ImageDraw.Draw(im)
            if 0 <= ativo < len(ws):
                x0 = pos[ativo]; d.rectangle([x0 - 8, base - 61, x0 + larg[ativo] + 8, base + 8], fill=(113, 13, 220, 255))
            for (w, x0) in zip(ws, pos): d.text((x0, base), w, font=f, anchor="ls", fill=(255, 255, 255, 255))
        return im
    def em(self, t):
        e = self.estado(t)
        return None if e is None else self.imagem(*e)
