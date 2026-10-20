# legenda ES no estilo do original: minusculas/maiusculas como escritas, branco com contorno preto, 1 palavra vermelha por bloco
import json, re, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
from PIL import ImageFont
from comum import ANTON
PX, Y, MAXW = 84, 1200, 900
pal = [(w, a, b) for w, a, b, q, i in json.load(open("palavras_final.json", encoding="utf-8"))]
def limpa(w): return re.sub(r"[^\wáéíóúñü]", "", w.lower())
def blocos(pal):
    bl, cur = [], []
    for w in pal:
        txt = " ".join(x[0] for x in cur + [w])
        if cur and (len(cur) >= 3 or len(txt) > 18): bl.append(cur); cur = []
        cur.append(w)
        if w[0].endswith((".", ":", ",", "?", "!")): bl.append(cur); cur = []
    if cur: bl.append(cur)
    return bl
f = ImageFont.truetype(str(ANTON), PX); asc, desc = f.getmetrics()
def ts(t): return f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Anton,{asc+desc},&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,1,0,1,7,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
VERM, BR = r"{\c&H1A1AE6&}", r"{\c&HFFFFFF&}"
L = []; bl = blocos(pal)
for i, b in enumerate(bl):
    ini = b[0][1]; fim = bl[i+1][0][1] if i + 1 < len(bl) else b[-1][2] + 0.6
    fim = min(fim, b[-1][2] + 0.5)
    txt = " ".join(w[0] for w in b); larg = f.getlength(txt)
    esc = min(100, int(100 * MAXW / larg)) if larg > MAXW else 100
    cand = [w for w in b if len(limpa(w[0])) >= 4]
    alvo = max(cand, key=lambda w: len(limpa(w[0]))) if cand else None
    partes = [(VERM if w is alvo else BR) + w[0] for w in b]
    pop = (r"{\an5\pos(540," + str(Y) + r")\fscx" + str(int(esc*.8)) + r"\fscy" + str(int(esc*.8)) +
           r"\t(0,90,\fscx" + str(esc+6) + r"\fscy" + str(esc+6) + r")\t(90,160,\fscx" + str(esc) + r"\fscy" + str(esc) + r")}")
    L.append(f"Dialogue: 0,{ts(ini)},{ts(fim)},C,,0,0,0,,{pop}{' '.join(partes)}")
open("leg_es.ass", "w", encoding="utf-8").write(head + "\n".join(L) + "\n")
print(len(L), "blocos")
