# -*- coding: utf-8 -*-
"""Legenda palavra a palavra no estilo do v4 (legenda_es.py), com estilo/geometria por palavra (timeline de saída).
st 'c' = padre chorando (maiúsculas, caixa roxa na palavra falada, baseline 1178); 'r' = padre de roxo (Open Sans 53, caixa fixa)."""
import re
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONTE = r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_colar\fonts\OpenSans.ttf"
CAIXA_COR = (14, 14, 14, 252); RAIO = 18
def fonte(tam, peso):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f
F_C = fonte(44, "SemiBold"); F_R = fonte(53, "Regular")
GEO = {"c": (1178, None), "r": (819, (36, 748, 684, 864)), "rm": (937, (96, 884, 624, 964))}
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p)
        txt = " ".join(x["w"] for x in cur)
        fim = re.search(r"[,.:;!?»…]+$", p["w"]) is not None
        if len(cur) >= 3 or len(txt) >= 16 or fim:
            out.append(cur); cur = []
    if cur: out.append(cur)
    res = []
    for b in out:
        if res and len(b) == 1 and len(b[0]["w"]) <= 3 and len(" ".join(x["w"] for x in res[-1] + b)) <= 20 and not re.search(r"[,.:;!?»…]$", res[-1][-1]["w"]):
            res[-1] = res[-1] + b
        else: res.append(b)
    return res
def limpa(w, st):
    w = w.strip().replace("…", "")
    if st == "r":
        w = re.sub(r"[,.:;]+$", "", w); w = w.replace("¡", "").replace("!", "").replace("¿", "").replace("?", "")
        w = re.sub(r"[,.:;]+(»)$", r"\1", w)
        return w
    return re.sub(r"[,.:;!?¡¿«»]+", "", w).upper()
class Legenda:
    def __init__(self, grupos):
        """grupos: lista de (seg_ini, seg_fim, [ {w, ini, fim, st, geo} ]) em tempo de saída"""
        self.bl = []
        for s0, s1, pal in grupos:
            bs = blocos(pal)
            for i, b in enumerate(bs):
                ini = max(s0, b[0]["ini"] - 0.03); prox = bs[i + 1][0]["ini"] if i + 1 < len(bs) else 1e9
                fim = min(prox, b[-1]["fim"] + 0.45, s1)
                if i == 0: ini = s0
                self.bl.append({"ini": ini, "fim": fim, "st": b[0]["st"], "geo": b[0]["geo"], "ws": [(limpa(x["w"], b[0]["st"]), x["ini"]) for x in b]})
    def estado(self, t):
        for k, b in enumerate(self.bl):
            if b["ini"] <= t < b["fim"]:
                ativo = max([i for i, (_, wi) in enumerate(b["ws"]) if wi <= t] or [0]) if b["st"] == "c" else -1
                return (k, ativo)
        return None
    @lru_cache(maxsize=64)
    def imagem(self, k, ativo):
        b = self.bl[k]; ws = [w for w, _ in b["ws"] if w]; st = b["st"]
        base, cx = GEO[b["geo"]]
        im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        f = F_C if st == "c" else F_R
        esp = f.getlength(" "); larg = [f.getlength(w) for w in ws]; tot = sum(larg) + esp * (len(ws) - 1)
        x = 360 - tot / 2; pos = []
        for L in larg: pos.append(x); x += L + esp
        asc = {"c": 40, "r": 46}[st]; desc = {"c": 14, "r": 16}[st]
        caixa = cx if cx else (int(360 - tot / 2 - 26), base - asc - 16, int(360 + tot / 2 + 26), base + desc + 12)
        d.rounded_rectangle(caixa, RAIO, fill=CAIXA_COR)
        if st == "r":
            t = " ".join(ws)
            sh = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            ds.text((361, base + 2), t, font=F_R, anchor="ms", fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(2.2))
            im = Image.alpha_composite(im, sh); ImageDraw.Draw(im).text((360, base), t, font=F_R, anchor="ms", fill=(255, 255, 255, 255))
            return im
        if 0 <= ativo < len(ws):
            x0 = pos[ativo]; d.rounded_rectangle([x0 - 8, base - 54, x0 + larg[ativo] + 8, base + 10], 6, fill=(113, 13, 220, 255))
        for (w, x0) in zip(ws, pos): d.text((x0, base), w, font=f, anchor="ls", fill=(255, 255, 255, 255))
        return im
    def em(self, t):
        e = self.estado(t)
        return None if e is None else self.imagem(*e)
    def caixa(self, geo): return GEO[geo][1]
