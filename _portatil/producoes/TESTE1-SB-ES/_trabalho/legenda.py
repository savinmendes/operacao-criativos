# -*- coding: utf-8 -*-
"""Legenda ES palavra a palavra PELO ROTEIRO (tempos do alinhamento ElevenLabs) no estilo do original:
minúsculas, sem pontuação, branca com contorno preto, palavra falada em amarelo, 2-3 palavras, centro y=932 (720x1280).
-> mont/leg.ass + mont/leg_blocos.json"""
import json, re
from pathlib import Path
import plano
AQ = Path(__file__).resolve().parent; M = AQ / "mont"
FS, Y, Y_BOARD, Y_CTA = 64, 932, 1000, 858
MAXP, MAXC = 3, 18
SUB = {"ígnes": "ignes", "véritas": "veritas", "siléntium": "silentium", "gládius": "gladius", "fortitúdo": "fortitudo",
       "custódia": "custodia", "sánctitas": "sanctitas", "spíritus": "spiritus", "triúmfus": "triumphus"}
JUNTAR = [(["novecientos", "dieciocho"], "918"), (["cuatrocientos", "noventa", "y", "siete"], "497"), (["doce"], "12"),
          (["san", "benito"], "san benito"), (["en", "vivo"], "en vivo"), (["ver", "más"], "ver más"), (["don", "aurelio"], "don aurelio")]

def limpa(w): return re.sub(r"[.,;:!?¡¿«»…\"]", "", w).lower()

def palavras():
    out = []
    for i, d in plano.LIN.items():
        P = [dict(w=limpa(p["w"]), raw=p["w"], ini=d["T0"] + p["ini"], fim=d["T0"] + p["fim"], linha=i) for p in d["palavras"]]
        P = [dict(p, w=SUB.get(p["w"], p["w"])) for p in P if p["w"]]
        k = 0; res = []
        while k < len(P):
            for seq, rep in JUNTAR:
                if [x["w"] for x in P[k:k + len(seq)]] == seq:
                    res.append(dict(P[k], w=rep, fim=P[k + len(seq) - 1]["fim"], raw=P[k + len(seq) - 1]["raw"])); k += len(seq); break
            else:
                res.append(P[k]); k += 1
        out += res
    return out

def blocos(W):
    B, cur = [], []
    for w in W:
        cand = cur + [w]; txt = " ".join(x["w"] for x in cand)
        if cur and (len(cand) > MAXP or len(txt) > MAXC or cur[-1]["linha"] != w["linha"] or w["ini"] - cur[-1]["fim"] > 0.6):
            B.append(cur); cand = [w]
        cur = cand
        if re.search(r"[.!?…:;]$", w["raw"]) or (w["raw"].endswith(",") and len(cur) >= 2): B.append(cur); cur = []
    if cur: B.append(cur)
    fix = []
    for b in B:   # palavra solta curta junta com a anterior se couber
        if fix and len(b) == 1 and len(fix[-1]) < MAXP and fix[-1][-1]["linha"] == b[0]["linha"] and not re.search(r"[.!?…:;]$", fix[-1][-1]["raw"]) \
                and len(" ".join(x["w"] for x in fix[-1] + b)) <= MAXC and b[0]["ini"] - fix[-1][-1]["fim"] < 0.4:
            fix[-1] = fix[-1] + b
        else: fix.append(b)
    return fix

def ts(t): return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"

if __name__ == "__main__":
    S = plano.segmentos(); board = next(c for c in S if c.get("board"))
    B = blocos(palavras()); ev = []; meta = []
    for i, b in enumerate(B):
        ini = b[0]["ini"] - 0.04; prox = B[i + 1][0]["ini"] - 0.04 if i + 1 < len(B) else plano.TOTAL
        fim = min(prox, b[-1]["fim"] + 0.45)
        y = Y_CTA if ini >= plano.CTA_T - 0.1 else (Y_BOARD if board["T"] - 0.05 <= ini < board["fim"] else Y)
        meta.append(dict(ini=round(ini, 3), fim=round(fim, 3), texto=" ".join(x["w"] for x in b), y=y))
        for j, w in enumerate(b):
            a = ini if j == 0 else w["ini"] - 0.04; e = (b[j + 1]["ini"] - 0.04) if j + 1 < len(b) else fim
            if e <= a: continue
            txt = " ".join((r"{\c&H00FFFF&}" if jj == j else r"{\c&HFFFFFF&}") + x["w"] for jj, x in enumerate(b))
            pop = r"\fscx85\fscy85\t(0,80,\fscx104\fscy104)\t(80,140,\fscx100\fscy100)" if j == 0 else ""
            tag = "{" + r"\an5\pos" + f"(360,{y}){pop}" + "}"
            ev.append(f"Dialogue: 0,{ts(a)},{ts(e)},L,,0,0,0,,{tag}{txt}")
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins SemiBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,3.2,2,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    (M / "leg.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    json.dump(meta, open(M / "leg_blocos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(len(B), "blocos;", len(ev), "eventos")
    for m in meta[:12] + meta[60:70]: print(m)
