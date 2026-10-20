import re, json, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho\corpo")
from comum_pl import palavras
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"
mapa = json.load(open(T + r"\corpo\mapa.json"))
FS = 64; Y = 845
HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,1,4,3,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
AM = r"{\c&H0000E4FF&}"; BR = r"{\c&H00FFFFFF&}"
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
def limpa(w): return re.sub(r"[.,?!:;—–\"„”]", "", w).upper()
PREP = {'w','z','i','a','o','u','od','na','do','po','dla','przy','bo','ze','we'}
def blocos(ws):
    out = []; cur = []
    for w in ws:
        txt = limpa(w[2])
        if not txt: continue
        cand = cur + [(w[0], w[1], txt)]
        if cur and (len(cand) > 3 or len(" ".join(x[2] for x in cand)) > 18):
            if len(cur) > 1 and cur[-1][2].lower() in PREP:
                out.append(cur[:-1]); cand = [cur[-1], (w[0], w[1], txt)]
            else:
                out.append(cur); cand = [(w[0], w[1], txt)]
        cur = cand
        if re.search(r"[.?!,]$", w[2]): out.append(cur); cur = []
    if cur: out.append(cur)
    return out
def eventos(ws, off, mapa_txt=None, fim_max=None):
    if mapa_txt: ws = [[a, b, re.sub(r"^[^.,?!]+", lambda m: mapa_txt.get(m.group(0).lower(), m.group(0)), w)] for a, b, w in ws]
    bl = blocos(ws); ev = []
    for i, b in enumerate(bl):
        nxt = bl[i+1][0][0] if i + 1 < len(bl) else None
        fim_b = b[-1][1] + 0.25
        if nxt is not None: fim_b = min(max(fim_b, b[-1][1]), nxt) if nxt - b[-1][1] < 0.6 else b[-1][1] + 0.25
        if fim_max: fim_b = min(fim_b, fim_max - off)
        for j, (a, e, t) in enumerate(b):
            st = a; en = b[j+1][0] if j + 1 < len(b) else fim_b
            txt = " ".join((AM + x[2] + BR) if k == j else x[2] for k, x in enumerate(b))
            pop = r"{\fscx82\fscy82\t(0,90,\fscx100\fscy100)}" if j == 0 else ""
            ev.append(f"Dialogue: 0,{ts(st+off)},{ts(en+off)},L,,0,0,0,,{{\pos(360,{Y})}}{pop}{txt}")
    return ev
def gerar(saida, hook_len, hook_alin=None, mapa_txt=None, hook_off=0.0):
    ev = []
    if hook_alin: ev += eventos(palavras(hook_alin), hook_off, mapa_txt, fim_max=hook_len)
    ev += eventos(palavras(T + r"\audio\corpo_vera.alinhamento.json"), hook_len + mapa["D"], {"klab": "Club"})
    open(saida, "w", encoding="utf-8").write(HEAD + "\n".join(ev) + "\n")
A = T + r"\audio"
M = {"trzy": "3", "jednych": "1", "sto": "100"}
gerar("leg_17.ass", 8.0667, A + r"\hook17_cristina.alinhamento.json", M)
gerar("leg_18.ass", 8.0667, A + r"\hook18_jessica.alinhamento.json", M, 0.45)
gerar("leg_t1.ass", 3.5667, A + r"\hook_danca_vera.alinhamento.json", {"trzy": "3"})
gerar("leg_t3.ass", 3.5667, A + r"\hook_danca_vera.alinhamento.json", {"trzy": "3"})
gerar("leg_pf7.ass", 7.8333)
