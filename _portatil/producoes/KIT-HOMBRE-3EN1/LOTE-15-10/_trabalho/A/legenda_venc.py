# Legenda no estilo do vencedor: blocos de ate 3 palavras, palavra falada em amarelo. Uso: python legenda_venc.py palavras.json saida.ass [fim]
import json, sys, re
pal = json.load(open(sys.argv[1], encoding="utf-8")); fim = float(sys.argv[3]) if len(sys.argv) > 3 else pal[-1][1] + 0.3
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def limpa(w): return re.sub(r"[^\wÁÉÍÓÚÑÜáéíóúñü¿?¡!]", "", w).strip("¿?¡!").upper()
blocos = []; cur = []
for p in pal:
    w = limpa(p[2])
    if not w: continue
    novo = cur + [(w, p[0], p[1])]
    if cur and (len(novo) > 3 or len(" ".join(x[0] for x in novo)) > 20 or p[0] - cur[-1][2] > 0.28):
        blocos.append(cur); cur = [(w, p[0], p[1])]
    else: cur = novo
    if re.search(r"[.?!,]$", p[2].strip()) and cur: blocos.append(cur); cur = []
if cur: blocos.append(cur)
ev = []
AM = "{" + chr(92) + "c&H00F0F5&}"; BR = "{" + chr(92) + "c&HFFFFFF&}"; POS = "{" + chr(92) + "pos(360,%d)}" % int(__import__("os").environ.get("LEG_Y", "843"))
for bi, b in enumerate(blocos):
    nb = blocos[bi + 1][0][1] if bi + 1 < len(blocos) else fim
    for wi, (w, a, e) in enumerate(b):
        t1 = b[wi + 1][1] if wi + 1 < len(b) else min(nb, e + 0.6) if bi + 1 < len(blocos) else fim
        if bi + 1 < len(blocos) and wi + 1 == len(b): t1 = nb
        txt = " ".join((AM + x + BR) if k == wi else x for k, (x, _, _) in enumerate(b))
        ev.append(f"Dialogue: 0,{ts(a)},{ts(t1)},C,,0,0,0,,{POS}{txt}")
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins,70,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,3.6,1.5,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(sys.argv[2], "w", encoding="utf-8").write(hdr + "\n".join(ev) + "\n")
print(len(blocos), "blocos:", [" ".join(x[0] for x in b) for b in blocos])
