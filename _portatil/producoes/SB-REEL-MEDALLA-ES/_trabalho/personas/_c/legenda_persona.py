# -*- coding: utf-8 -*-
"""[legenda_v2.py: copia do legenda.py p/ a v2 -> mont2/leg_v2.ass; tempos mapeados por montar_v2.S]
Legenda karaokê SB (adaptada de SB-VENCEDORES.../v07/legenda_fr.py).
Lê voz/narracao_completa.palavras.json (linha do tempo única) e gera:
  voz/legenda_blocos.json  -> blocos de até 3 palavras/16 caracteres, com tempos por palavra
  voz/legenda.ass          -> Poppins ExtraBold 83, caixa alta, branco + palavra falada amarela, centro y=1460
Nos trechos em latim só entra o latim (a tradução está no cartão latim_XX.png).
Rodar na pasta _trabalho:  python legenda.py
"""
import json, re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
V = AQUI / "voz"
import sys as _s
_s.path.insert(0, str(AQUI))
import montar as MV
V = AQUI / "voz"
W = json.loads((V / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
for _w in W:
    _w["ini"] = MV.S(_w["ini"]); _w["fim"] = MV.S(_w["fim"])
TOTAL = MV.TOTAL
CTA_T, Y_CTA = MV.CTA1, 1330
OUTD = AQUI / "mont"; OUTD.mkdir(exist_ok=True)
MAXP, MAXC = 3, 16
Y, FS = 1460, 120  # 83 saia pequeno no libass (Poppins: ascender+descender ~1,5 em)


def limpa(w):
    return re.sub(r"[.,;:!?¡¿«»<>…]", "", w).upper()


def quebra_forte(w):
    return bool(re.search(r"[.!?…:;]$", w))


def quebra_fraca(w):
    return w.endswith(",")


# palavras visíveis (sem tradução do latim)
vis0 = [w for w in W if w.get("papel") != "traducao"]
# junta pares que não podem quebrar (San Benito, en vivo, Ver más) num único token
JUNTA = {("san", "benito"), ("en", "vivo"), ("<<ver", "más"), ("«ver", "más")}
vis = []
for w in vis0:
    if vis and (re.sub(r"[^\w<«]", "", vis[-1]["w"].lower()), re.sub(r"[^\w]", "", w["w"].lower())) in JUNTA             and not re.search(r"[.,!?]$", vis[-1]["w"]):
        vis[-1] = dict(vis[-1], w=vis[-1]["w"] + " " + w["w"], fim=w["fim"])
    else:
        vis.append(dict(w))

blocos, cur = [], []
for k, w in enumerate(vis):
    cand = cur + [w]
    txt = " ".join(limpa(x["w"]) for x in cand)
    mudou_contexto = cur and (cur[-1].get("linha") != w.get("linha") or cur[-1].get("personagem") != w.get("personagem"))
    if cur and (len(cand) > MAXP or len(txt) > MAXC or mudou_contexto):
        blocos.append(cur); cur = [w]
    else:
        cur = cand
    if quebra_forte(w["w"]) or (quebra_fraca(w["w"]) and len(cur) >= 2):
        blocos.append(cur); cur = []
if cur:
    blocos.append(cur)

# evita bloco de 1 palavra curta "pendurada" juntando com o anterior quando cabe
fix = []
for b in blocos:
    if fix and len(b) == 1 and len(fix[-1]) < MAXP and not quebra_forte(fix[-1][-1]["w"]) \
            and len(" ".join(limpa(x["w"]) for x in fix[-1] + b)) <= MAXC \
            and fix[-1][-1].get("linha") == b[0].get("linha"):
        fix[-1] = fix[-1] + b
    else:
        fix.append(b)
blocos = fix

saida = []
for i, b in enumerate(blocos):
    ini = b[0]["ini"]
    prox = blocos[i + 1][0]["ini"] if i + 1 < len(blocos) else TOTAL
    fim = min(prox, b[-1]["fim"] + 0.6) if i + 1 < len(blocos) else min(TOTAL, b[-1]["fim"] + 0.8)
    saida.append({
        "i": i + 1, "ini": round(ini, 3), "fim": round(fim, 3),
        "texto": " ".join(limpa(x["w"]) for x in b),
        "personagem": b[0].get("personagem"),
        "latim": bool(b[0].get("latim")), "linha_latim": b[0].get("linha"),
        "palavras": [{"w": limpa(x["w"]), "ini": x["ini"], "fim": x["fim"]} for x in b],
    })
(OUTD / "leg_v2_blocos.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1), encoding="utf-8")


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins ExtraBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
AM = r"{\c&H54E5FE&}"; BR = r"{\c&HFFFFFF&}"  # amarelo #FEE554
L = []
for b in saida:
    p = b["palavras"]
    for j, w in enumerate(p):
        a = b["ini"] if j == 0 else w["ini"]
        e = p[j + 1]["ini"] if j + 1 < len(p) else b["fim"]
        if e <= a:
            continue
        partes = [(AM if jj == j else BR) + x["w"] for jj, x in enumerate(p)]
        pop = r"{\an5\pos(540,%d)" % (Y_CTA if a >= CTA_T - 0.05 else Y)
        if j == 0:
            pop += r"\fscx80\fscy80\t(0,90,\fscx106\fscy106)\t(90,160,\fscx100\fscy100)"
        pop += "}"
        L.append(f"Dialogue: 0,{ts(a)},{ts(e)},C,,0,0,0,,{pop}{' '.join(partes)}")
(OUTD / "leg_v2.ass").write_text(head + "\n".join(L) + "\n", encoding="utf-8")
print(len(saida), "blocos,", len(L), "eventos")
