# Legenda PL no estilo do AD FR: caixa alta branca centralizada (y≈0,75), palavras ainda não faladas esmaecidas, sombra cinza
import json, re
TOTAL = 102.866; Y = 1440; LIVE = 97.75   # legenda some antes do 1o quadro da live (2933)
pal = json.load(open("audio/palavras_pl.json", encoding="utf-8"))
for i in range(len(pal) - 2):   # nome do botao numa peca so: «Dowiedz się więcej»
    if pal[i][0].startswith("«") and pal[i + 2][0].startswith("więcej"):
        pal[i:i + 3] = [[" ".join(x[0] for x in pal[i:i + 3]), pal[i][1], pal[i + 2][2]]]; break
def disp(w): return re.sub(r"[.,…!?\"]", "", w).upper().replace("...", "")
FUNC = {"I","W","Z","NA","DO","CI","TO","NIE","A","ŻE","CO","BO","MI","ZA","PRZEZ","TEN","TAK","JUŻ","JAK","CIĘ","PO"}
blocos = []; cur = []
for k, (w, s, e) in enumerate(pal):
    d = disp(w)
    if not d: continue
    txt = " ".join(disp(x[0]) for x in cur + [[w]])
    if cur and (len(txt) > 21 or len(cur) >= 4):
        j = len(cur)
        while j > 1 and disp(cur[j - 1][0]) in FUNC: j -= 1   # palavras funcionais no fim vao p/ o bloco seguinte
        blocos.append(cur[:j]); cur = cur[j:]
    cur.append([w, s, e])
    nxt = pal[k + 1][1] if k + 1 < len(pal) else 99
    if re.search(r"[.,!?…]$", w): blocos.append(cur); cur = []
if cur: blocos.append(cur)
head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins,100,&H00FFFFFF,&H00FFFFFF,&H70505050,&H90404040,-1,0,0,0,100,100,0,0,1,3,4,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"
lin = []; out = []
for i, b in enumerate(blocos):
    ini = b[0][1]
    fim = min(blocos[i + 1][0][1], b[-1][2] + 0.6) if i + 1 < len(blocos) else min(b[-1][2] + 0.6, LIVE)
    out.append([round(ini, 2), round(fim, 2), " ".join(disp(w[0]) for w in b)])
    for k, w in enumerate(b):
        a = ini if k == 0 else w[1]; z = b[k + 1][1] if k + 1 < len(b) else fim
        if z <= a: continue
        partes = [(r"{\alpha&H00&}" if j <= k else r"{\alpha&HA0&\3a&HF0&\4a&HF0&}") + disp(x[0]) for j, x in enumerate(b)]
        pop = r"\fscx90\fscy90\t(0,100,\fscx100\fscy100)" if k == 0 else ""
        lin.append("Dialogue: 0," + ts(a) + "," + ts(z) + ",C,,0,0,0,,{" + r"\an5\pos(540," + str(Y) + ")" + pop + "}" + " ".join(partes))
open("leg_pl.ass", "w", encoding="utf-8").write(head + "\n".join(lin) + "\n")
json.dump(out, open("blocos_pl.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for x in out: print(x)
