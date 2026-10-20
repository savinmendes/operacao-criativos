# Legenda IT no estilo do ADS 7 ES: Arial Black caixa alta, 2 linhas, palavra falada em verde com brilho,
# palavras-chave em vermelho, demais em branco; contorno escuro.
import re, json
from palavras import palavras
TOTAL=24.60; Y=1420
pal=palavras("audio/narr_it_v2.alinhamento.json")
def disp(w): return re.sub(r"[.,…!?]","",w).upper()
bl=[];cur=[]
for w in pal:
    txt=" ".join(disp(x[0]) for x in cur+[w])
    if cur and (len(cur)>=4 or len(txt)>22): bl.append(cur);cur=[]
    cur.append(w)
    if w[0].endswith((".",",","!","?","...")): bl.append(cur);cur=[]
if cur: bl.append(cur)
RED={"DONO","DIRETTA","PREGHIERA","FINANZIARIA","BENEDIZIONE","IGNORARE","SOTTO","SCOPRI"}
G=r"{\c&H2EF02E&}"; W=r"{\c&HFFFFFF&}"; R=r"{\c&H2020FF&}"
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Arial Black,98,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,1,0,1,6,3,5,40,40,0,1
Style: G,Arial Black,98,&HA02EF02E,&HA02EF02E,&H602EF02E,&HFF000000,0,0,0,0,100,100,1,0,1,14,0,5,40,40,0,1
"""
def ts(t): h,m,s=int(t//3600),int(t%3600//60),t%60; return f"{h}:{m:02d}:{s:05.2f}"
lin=[];txts=[]
for i,b in enumerate(bl):
    ini=b[0][1]; nxt=bl[i+1][0][1] if i+1<len(bl) else TOTAL
    fim=min(nxt,b[-1][2]+0.6) if i+1<len(bl) else TOTAL
    ws=[disp(w[0]) for w in b]
    quebra=(len(ws)+1)//2 if (len(ws)>=3 or len(" ".join(ws))>13) and len(ws)>1 else len(ws)
    if 1<quebra<len(ws) and len(" ".join(ws[quebra:]))<=2: quebra-=1  # evita palavra de 1-2 letras sozinha na 2a linha
    txts.append((round(ini,2),round(fim,2)," ".join(ws)))
    for k,w in enumerate(b):
        a=ini if k==0 else w[1]; z=b[k+1][1] if k+1<len(b) else fim
        if z<=a: continue
        partes=[]
        for j,x in enumerate(ws):
            c=G if j==k else (R if x in RED else W)
            partes.append(c+x+(r"\N" if j==quebra-1 and j<len(ws)-1 else " "))
        t="".join(partes).rstrip()
        pos=r"{\an5\pos(540,"+str(Y)+")"+(r"\fscx85\fscy85\t(0,90,\fscx105\fscy105)\t(90,160,\fscx100\fscy100)" if k==0 else "")+"}"
        glow=r"{\an5\pos(540,"+str(Y)+r")\blur12"+(r"\fscx85\fscy85\t(0,90,\fscx105\fscy105)\t(90,160,\fscx100\fscy100)" if k==0 else "")+"}"
        gtxt="".join((x+(r"\N" if j==quebra-1 and j<len(ws)-1 else " ")) for j,x in enumerate(ws)).rstrip()
        lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},G,,0,0,0,,{glow}{gtxt}")
        lin.append(f"Dialogue: 1,{ts(a)},{ts(z)},C,,0,0,0,,{pos}{t}")
open("leg_it.ass","w",encoding="utf-8").write(head+"\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"+"\n".join(lin)+"\n")
json.dump(txts,open("blocos_it.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
for x in txts: print(x)
