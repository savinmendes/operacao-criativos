# Legenda EN no estilo do ADS 24 ES: caixa alta MontserratXB, contorno preto, palavra falada colorida
# (cor do bloco alterna vermelho/amarelo/verde), 2 linhas. Gancho do senhor: caixa branca pequena (PNG).
import re, json
from PIL import Image, ImageDraw, ImageFont
from palavras import palavras
from mapa import O, TOTAL
V=palavras("audio/velho.alinhamento.json",0.05); A=palavras("audio/anjo.alinhamento.json",O)
# junta "eleven eleven" -> 11:11
W=[]; i=0
while i<len(A):
    if A[i][0].lower().startswith("eleven") and i+1<len(A) and A[i+1][0].lower().startswith("eleven"):
        W.append(["11:11",A[i][1],A[i+1][2]]); i+=2
    else: W.append(A[i]); i+=1
def disp(w): return re.sub(r"[.,…!?:;]$","",w).upper().replace("’","'")
FNT=ImageFont.truetype("fonts/MontserratXB.ttf",72)
def larg(s): return FNT.getlength(s)
# blocos
import math
cl=[]; cur=[]
for w in W:
    cur.append(w)
    if w[0].endswith((".","!","?",":",",")): cl.append(cur); cur=[]
if cur: cl.append(cur)
bl=[]
for c in cl:
    n=len(c); L=len(" ".join(disp(x[0]) for x in c))
    k=max(math.ceil(n/4),math.ceil(L/20),1)
    base=n//k; extra=n%k; cuts=[]; i0=0
    for j in range(k-1):
        i0+=base+(1 if j<extra else 0); cuts.append(i0)
    FRACA={"is","a","an","the","to","of","for","you","can","that","and","in","with","has","have","your","this","its","it's","be","been","will","must","who","about","since","our","my"}
    PAR={("saint","benedict"),("live","prayer"),("learn","more"),("11:11","portal"),("guardian","angel"),("ask","for"),("waiting","for"),("long","for")}
    def ruim(i):
        a=disp(c[i-1][0]).lower(); b=disp(c[i][0]).lower() if i<n else ""
        return a in FRACA or (a,b) in PAR
    for q,ct in enumerate(cuts):
        lo=(cuts[q-1] if q else 0)+1; hi=(cuts[q+1] if q+1<len(cuts) else n)-1
        if ruim(ct):
            for d in (1,-1,2,-2):
                t=ct+d
                if lo+1<=t<=hi-1 and not ruim(t) and len(" ".join(disp(x[0]) for x in c[(cuts[q-1] if q else 0):t]))<=24 and len(" ".join(disp(x[0]) for x in c[t:(cuts[q+1] if q+1<len(cuts) else n)]))<=24:
                    cuts[q]=t; break
    i0=0
    for ct in cuts+[n]:
        bl.append(c[i0:ct]); i0=ct
CORES=[r"&H2A20E5&", r"&H00F2FF&", r"&H3BD43B&"]  # vermelho, amarelo, verde (BGR)
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,MontserratXB,72,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,5,3,5,10,10,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
lin=[]; txt=[]
for i,b in enumerate(bl):
    ini=b[0][1]; fim=min(bl[i+1][0][1], b[-1][2]+0.7) if i+1<len(bl) else TOTAL
    if i==0: ini=max(ini,5.90)  # entra com o anjo
    pals=[disp(x[0]) for x in b]; s=" ".join(pals)
    if len(s)<=13 or len(pals)==1: quebra=None
    else: quebra=2 if len(pals)>=3 else 1
    cor=CORES[i%3]; txt.append((round(ini,2),round(fim,2),s))
    # escala se alguma linha passar de 680 px
    linhas=[" ".join(pals[:quebra])," ".join(pals[quebra:])] if quebra else [s]
    esc=min(100,int(100*680/max(larg(l) for l in linhas)))
    for k,w in enumerate(b):
        a=ini if k==0 else w[1]; z=b[k+1][1] if k+1<len(b) else fim
        if z<=a: continue
        partes=[]
        for j,p in enumerate(pals):
            sep=r"\N" if (quebra and j==quebra) else (" " if j else "")
            partes.append(sep+(r"{\c"+cor+"}" if j==k else r"{\c&HFFFFFF&}")+p)
        tag=r"{\an5\pos(360,1000)\fscx"+str(esc)+r"\fscy"+str(esc)+"}"
        lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},S,,0,0,0,,{tag}{''.join(partes)}")
open("leg_en.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_en.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
# gancho: caixas brancas
def caixa(linhas,dest):
    f=ImageFont.truetype("fonts/Poppins-Bold.ttf",30); pad=14; lh=38
    w=int(max(f.getlength(l) for l in linhas))+2*pad; h=lh*len(linhas)+2*pad-6
    img=Image.new("RGBA",(720,200),(0,0,0,0)); d=ImageDraw.Draw(img)
    x0=(720-w)//2; d.rounded_rectangle([x0,0,x0+w,h],radius=10,fill=(255,255,255,255))
    for n,l in enumerate(linhas):
        lw=f.getlength(l); d.text(((720-lw)/2,pad-6+n*lh),l,font=f,fill=(0,0,0,255))
    img.save(dest)
caixa(["you have 60 seconds"],"hook1.png"); caixa(["then I'll pass this blessing","on to someone else"],"hook2.png")
t2=next(w[1] for w in V if w[0].lower().startswith("then"))
json.dump({"t2":t2,"fim":V[-1][2]+0.15},open("hook_t.json","w"))
print(len(txt),"blocos; hook2 em",t2)
for x in txt: print(x)
