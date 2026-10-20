# Legenda no estilo do AD ES: Poppins Bold 60, caixa alta, branco + palavra falada em amarelo, blocos <=3 palavras/16 chars
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
from PIL import ImageFont
HOOK_DUR=float(sys.argv[1]) if len(sys.argv)>1 else 3.30
TOTAL=float(sys.argv[2]) if len(sys.argv)>2 else 27.98
Y=int(sys.argv[3]) if len(sys.argv)>3 else 1463
pal=palavras("audio/hook_fr.alinhamento.json",0)+palavras("audio/corpo_fr.alinhamento.json",HOOK_DUR)
# limpa: tira « » e pontuação de exibição, mas guarda fim de frase para quebrar bloco
out=[]
for w,s,e in pal:
    if w in ("<<",">>","«","»"): continue
    out.append([w,s,e])
pal=out
def disp(w): return re.sub(r"[.,…!?«»<>]","",w).upper()
# blocos do kit (<=3 palavras, <=16 chars, quebra em pontuação), com o CTA fixo
bl=LEG._blocos([tuple(p) for p in pal])
fix=[]
for b in bl:
    t=" ".join(disp(w[0]) for w in b)
    if t.startswith("TOUCHE") or (len(b)>0 and disp(b[0][0]) in ("EN","SAVOIR","PLUS","MAINTENANT") and any(disp(x[0])=="SAVOIR" for x in pal if abs(x[1]-b[0][1])<2)):
        fix.extend([[x] for x in b])
    else: fix.append(b)
# reagrupa CTA: TOUCHE | EN SAVOIR PLUS | MAINTENANT
bl=[]; i=0
while i<len(fix):
    b=fix[i]
    if len(b)==1 and disp(b[0][0])=="EN" and i+2<len(fix) and disp(fix[i+1][0][0])=="SAVOIR":
        bl.append(fix[i]+fix[i+1]+fix[i+2]); i+=3
    else: bl.append(b); i+=1
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
open("leg_fr.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(blocos_txt,open("blocos_fr.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
for x in blocos_txt: print(x)
