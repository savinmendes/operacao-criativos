# Legenda FR no estilo do ES (Poppins Bold caixa alta, sombra difusa, palavras-chave coloridas).
# Na abertura (PiP) a legenda fica pequena dentro do quadro do Jesus, como no 13.13F original.
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
BS = chr(92)
CJ = json.load(open("cortes_fr.json")); C = CJ["C"]; SW = CJ["SW"]; TOTAL = C[-1]
pal = [list(p) for p in palavras("audio/voz_fr_p.alinhamento.json")]
m = []
for p in pal:   # junta as aspas francesas na palavra vizinha
    if p[0] == "«": m.append(["«", p[1], p[2]]); continue
    if p[0] == "»": m[-1][0] += "»"; m[-1][2] = p[2]; continue
    if m and m[-1][0] == "«": m[-1][0] = "«" + p[0]; m[-1][2] = p[2]; continue
    m.append(p)
pal = m
GR = ["Si tu m'ignores...", "je n'aurai pas", "d'autre choix", "que d'accorder", "le miracle", "dont tu as", "tant besoin", "à quelqu'un d'autre.",
      "C'est ta", "dernière chance", "de recevoir", "ce que j'ai", "préparé pour toi.", "Jésus t'a choisi.", "Il t'a apporté", "un puissant cadeau.",
      "Aujourd'hui,", "tu vas entendre", "une ancienne prière", "perdue de la Bible,", "qui libérera", "une pluie", "de bénédictions", "et de miracles", "sur ta vie.",
      "Ne me rejette plus.", "Appuie sur", "«En savoir plus»", "ci-dessous,", "et rejoins", "la prière", "en direct.", "Reçois ton miracle", "avant qu'il ne soit", "trop tard."]
bl = []; k = 0
for g in GR:
    n = len(g.split()); b = pal[k:k + n]
    assert " ".join(x[0] for x in b) == g, (g, [x[0] for x in b]); bl.append(b); k += n
assert k == len(pal)
def disp(w): return re.sub(r"[.,…!?]", "", w).upper().replace("«", "« ").replace("»", " »")
def cor(h): return "{" + BS + "c&H" + h + "&}"
VM, AM, VD, BR = cor("2020F0"), cor("00F0FF"), cor("28E040"), cor("FFFFFF")
COR = {"MIRACLE": VM, "CHANCE": VM, "PRÉPARÉ": AM, "CHOISI": AM, "CADEAU": VM, "ENTENDRE": AM, "PRIÈRE": AM,
       "BÉNÉDICTIONS": VD, "MIRACLES": VM, "VIE": VM, "DIRECT": VD, "TARD": VM}
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins,92,&H00FFFFFF,&H00FFFFFF,&H90000000,&H70000000,1,0,0,0,100,100,1,0,1,6,3,5,90,90,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
S = 0.6093; PX = round(1.5 * (281.03 + S * 360)); PY = round(1.5 * (680.26 + S * 1160 / 1.5))
lin = []; txt = []
for i, b in enumerate(bl):
    ini = max(0, b[0][1] - 0.03)
    fim = min(bl[i + 1][0][1] - 0.03, b[-1][2] + 0.7) if i + 1 < len(bl) else TOTAL
    for cc in [SW] + C[1:-1]:
        if ini < cc - 0.2 and fim > cc: fim = cc - 0.01
    words = [disp(w[0]) for w in b]
    cta = any("SAVOIR" in w for w in words)
    s = " ".join((AM if cta else COR.get(w, BR)) + w + BR for w in words)
    txt.append((round(ini, 2), round(fim, 2), " ".join(words)))
    if ini < SW - 0.1: x, y, sc, bb = PX, PY, S, 2
    else: x, y, sc, bb = 540, (1560 if ini >= C[5] - 0.1 else 1160), 1.0, 3
    a, b2, c3 = round(85 * sc), round(104 * sc), round(100 * sc)
    tag = ("{" + BS + "an5" + BS + f"pos({x},{y})" + BS + f"blur{bb}" + BS + f"fscx{a}" + BS + f"fscy{a}"
           + BS + "t(0,100," + BS + f"fscx{b2}" + BS + f"fscy{b2})" + BS + "t(100,170," + BS + f"fscx{c3}" + BS + f"fscy{c3})" + "}")
    lin.append(f"Dialogue: 0,{LEG._ts(ini)},{LEG._ts(fim)},C,,0,0,0,," + tag + s)
open("leg_fr.ass", "w", encoding="utf-8").write(head + "\n".join(lin) + "\n")
json.dump(txt, open("blocos_fr.json", "w", encoding="utf-8"), indent=0, ensure_ascii=False)
for x in txt: print(x)
