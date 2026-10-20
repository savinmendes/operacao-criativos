# -*- coding: utf-8 -*-
"""Legenda ES palavra a palavra (v2): texto dentro de CAIXA opaca de cantos arredondados que esconde a faixa da legenda PT antiga.
Estilos: gancho (maiúsculas, palavra falada amarela), padre chorando (maiúsculas, caixa roxa na palavra), padre de roxo (Open Sans 53)."""
import json, re
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
AQ = Path(__file__).resolve().parent
FONTE = str(AQ.parent.parent / "_trabalho_colar" / "fonts" / "OpenSans.ttf")
FIM_GANCHO, FIM_CHORA = 7.38, 21.95
S = 4.0; PROD = (3779 / 30, 3921 / 30 + S)
CAIXA_COR = (14, 14, 14, 252); RAIO = 18
def fonte(tam, peso):
    f = ImageFont.truetype(FONTE, tam); f.set_variation_by_name(peso); return f
F_G = fonte(40, "SemiBold"); F_C = fonte(44, "SemiBold"); F_R = fonte(53, "Regular")
def estilo(t): return "g" if t < FIM_GANCHO else ("c" if t < FIM_CHORA else "r")
# geometria por trecho (tempo FINAL): baseline, caixa fixa (x0,y0,x1,y1) ou None = caixa justa no texto
def geo(t, st):
    if st == "g":
        if t < 4.10: return 689, (56, 630, 664, 726)          # cobre a faixa PT apagada (repórter fala; padre ao fundo)
        return 1228, None                                     # avatar do grito: legenda na faixa preta de baixo, longe do rosto
    if st == "c": return 1178, None                           # avatar do padre chorando: no peito, abaixo do queixo
    if PROD[0] <= t < PROD[1]: return 836, None               # tela do produto: sem legenda PT por baixo
    if 76.03 <= t < 87.4: return 937, (96, 884, 624, 964)     # molduras pretas (monge/manuscrito/procissão)
    return 819, (36, 748, 684, 864)                           # padre de roxo / b-rolls
def blocos(pal):
    out, cur = [], []
    for p in pal:
        cur.append(p)
        txt = " ".join(x["w"] for x in cur)
        fim = re.search(r"[,.:;!?]$", p["w"]) is not None
        if len(cur) >= 3 or len(txt) >= 16 or fim:
            out.append(cur); cur = []
    if cur: out.append(cur)
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
        pal = [p for p in pal if not (48.2 <= p["ini"] < 61.4)]  # cartão das 12 palavras: o original não tem legenda
        self.bl = []
        bs = blocos(pal)
        for i, b in enumerate(bs):
            ini = b[0]["ini"]; prox = bs[i + 1][0]["ini"] if i + 1 < len(bs) else 1e9
            fim = min(prox, b[-1]["fim"] + 0.45)
            st = estilo(ini)
            if i == 0: ini = 0.0
            if st == "r" and ini < 22.25: ini = 22.25              # fusão padre chorando -> roxo: sem caixa sobre o rosto que sai
            if st == "g": fim = min(fim, FIM_GANCHO if ini >= 4.10 else 4.10)
            if st == "c": fim = min(fim, FIM_CHORA)
            self.bl.append({"ini": ini, "fim": fim, "st": st, "ws": [(limpa(x["w"], st), x["ini"]) for x in b]})
    def estado(self, t):
        for k, b in enumerate(self.bl):
            if b["ini"] <= t < b["fim"]:
                ativo = max([i for i, (_, wi) in enumerate(b["ws"]) if wi <= t] or [0]) if b["st"] in "gc" else -1
                return (k, ativo)
        return None
    def caixa_fixa(self, t):
        """caixa da faixa PT (para mostrar mesmo sem texto ES quando sobra borrão na base)"""
        return geo(t, estilo(t))[1]
    @lru_cache(maxsize=64)
    def imagem(self, k, ativo):
        b = self.bl[k]; ws = [w for w, _ in b["ws"] if w]; st = b["st"]
        base, cx = geo(b["ini"], st)
        im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        f = F_G if st == "g" else (F_C if st == "c" else F_R)
        esp = f.getlength(" "); larg = [f.getlength(w) for w in ws]; tot = sum(larg) + esp * (len(ws) - 1)
        x = 360 - tot / 2; pos = []
        for L in larg: pos.append(x); x += L + esp
        asc = {"g": 34, "c": 40, "r": 46}[st]; desc = {"g": 12, "c": 14, "r": 16}[st]
        caixa = cx if cx else (int(360 - tot / 2 - 26), base - asc - 16, int(360 + tot / 2 + 26), base + desc + 12)
        d.rounded_rectangle(caixa, RAIO, fill=CAIXA_COR)
        if st == "r":
            t = " ".join(ws)
            sh = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
            ds.text((361, base + 2), t, font=F_R, anchor="ms", fill=(0, 0, 0, 200)); sh = sh.filter(ImageFilter.GaussianBlur(2.2))
            im = Image.alpha_composite(im, sh); ImageDraw.Draw(im).text((360, base), t, font=F_R, anchor="ms", fill=(255, 255, 255, 255))
            return im
        if st == "g":
            for i, (w, x0) in enumerate(zip(ws, pos)):
                d.text((x0, base), w, font=f, anchor="ls", fill=(244, 242, 23, 255) if i == ativo else (255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        else:
            if 0 <= ativo < len(ws):
                x0 = pos[ativo]; d.rounded_rectangle([x0 - 8, base - 54, x0 + larg[ativo] + 8, base + 10], 6, fill=(113, 13, 220, 255))
            for (w, x0) in zip(ws, pos): d.text((x0, base), w, font=f, anchor="ls", fill=(255, 255, 255, 255))
        return im
    def em(self, t):
        e = self.estado(t)
        return None if e is None else self.imagem(*e)
