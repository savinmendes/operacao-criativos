# Legenda PL no estilo do AD ES: Anton (condensada), caixa alta, branco + palavra falada em amarelo (#F0FF25), contorno preto
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
FS=int(sys.argv[1]) if len(sys.argv)>1 else 120
TOTAL=float(sys.argv[2]) if len(sys.argv)>2 else 999
Y=1496
LEG.MAX_PAL=3; LEG.MAX_CHR=16
pal=[tuple(p) for p in palavras("audio/narracao_pl.alinhamento.json",0)]
def disp(w): return re.sub(r"[.,…!?:;\"«»]","",w).upper()
bl=LEG._blocos(pal)
AM=r"{\c&H25FFF0&}"; BR=r"{\c&HFFFFFF&}"
head=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Anton,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,6,3,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ts=LEG._ts; lin=[]; txt=[]
for i,b in enumerate(bl):
    ini=b[0][1]
    fim=bl[i+1][0][1] if i+1<len(bl) else TOTAL
    fim=min(fim,b[-1][2]+0.5)
    txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
    for k,w in enumerate(b):
        a=ini if k==0 else w[1]
        z=b[k+1][1] if k+1<len(b) else fim
        if z<=a: continue
        partes=[(AM if j==k else BR)+disp(x[0]) for j,x in enumerate(b)]
        pop=(r"\fscx85\fscy85\t(0,90,\fscx104\fscy104)\t(90,160,\fscx100\fscy100)" if k==0 else "")
        tag="{"+r"\an5\pos(540,"+str(Y)+")"+pop+"}"
        lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},C,,0,0,0,,"+tag+" ".join(partes))
open("leg_pl.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_pl.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(bl),"blocos; maior:",max(txt,key=lambda x:len(x[2])))
