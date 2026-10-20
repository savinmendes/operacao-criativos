# Legenda no estilo do AD ES: Poppins Bold 60, caixa alta, branco + palavra falada em amarelo, blocos <=3 palavras/16 chars
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
from PIL import ImageFont
HOOK_DUR=float(sys.argv[1]) if len(sys.argv)>1 else 3.30
TOTAL=float(sys.argv[2]) if len(sys.argv)>2 else 27.98
Y=int(sys.argv[3]) if len(sys.argv)>3 else 1463
CORPO_AL=sys.argv[4] if len(sys.argv)>4 else "audio/corpo_pl_p.alinhamento.json"
pal=palavras("audio/hook_pl.alinhamento.json",0)+palavras(CORPO_AL,HOOK_DUR)
# limpa: tira « » e pontuação de exibição, mas guarda fim de frase para quebrar bloco
out=[]
for w,s,e in pal:
    if w in ("<<",">>","«","»"): continue
    out.append([w,s,e])
pal=out
def disp(w): return re.sub(r"[.,…!?«»<>]","",w).upper()
# blocos do kit (<=3 palavras, <=16 chars, quebra em pontuação); CTA em blocos fixos
ia=next(i for i,w in enumerate(pal) if disp(w[0])=="DOTKNIJ")
im=next(i for i,w in enumerate(pal) if i>ia and disp(w[0])=="ŻYWO")
cta=pal[ia:im+1]
tam=[1,3,1,2,2,2]; grupos=[]; k=0
for t in tam: grupos.append(cta[k:k+t]); k+=t
assert k==len(cta), [c[0] for c in cta]
# PL: blocos definidos à mão (nº de palavras por bloco) para não quebrar sintagmas (ŚWIĘTEGO BENEDYKTA, NIE ODRZUCISZ, W TEN SPOSÓB)
TAM=[3,3,3, 3,3,1,2,3, 1,2, 1,2,3, 2,1,1,2,2,2, 3,2,2]+tam+[3,2,2,2]
assert sum(TAM)==len(pal),(sum(TAM),len(pal))
bl=[];k=0
for t in TAM: bl.append([tuple(x) for x in pal[k:k+t]]); k+=t
f=ImageFont.truetype(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf",60)
asc,desc=f.getmetrics(); fs=round((asc+desc)*1.34)
AM=r"{\c&H56E6FF&}"; BR=r"{\c&HFFFFFF&}"
head=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins,{fs},&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,7,4,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ts=LEG._ts
lin=[]; blocos_txt=[]
for i,b in enumerate(bl):
    ini=b[0][1]
    fim=bl[i+1][0][1] if i+1<len(bl) else TOTAL
    fim=min(fim,b[-1][2]+0.6) if i+1<len(bl) else TOTAL
    blocos_txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
    for k,w in enumerate(b):
        a=ini if k==0 else w[1]
        z=b[k+1][1] if k+1<len(b) else fim
        if z<=a: continue
        partes=[(AM if j==k else BR)+disp(x[0]) for j,x in enumerate(b)]
        pos=r"{\an5\pos(540,"+str(Y)+")"
        pop=(r"\fscx80\fscy80\t(0,90,\fscx106\fscy106)\t(90,160,\fscx100\fscy100)" if k==0 else "")+"}"
        lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},C,,0,0,0,,{pos}{pop}{' '.join(partes)}")
open(sys.argv[5] if len(sys.argv)>5 else "leg_pl.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(blocos_txt,open("blocos_pl.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
for x in blocos_txt: print(x)
