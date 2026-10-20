# Legenda EN no estilo do ADS 20 ES: gancho = Poppins Bold pequena (branco + palavra falada amarela);
# ceu = Anton caixa alta, contorno preto, palavra falada amarela, blocos <=3 palavras/18 chars. PlayRes 720x1280.
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
T=json.load(open("tempos.json")); TOTAL=T["TOTAL"]; HK=T["HK"]; C0=T["C0"]
LEG.MAX_PAL=3; LEG.MAX_CHR=16
hook=palavras("audio/hook1_en.alinhamento.json",0.08)+palavras("audio/hook2_en.alinhamento.json",2.55)
corpo=palavras("audio/corpo_en_p.alinhamento.json",C0)
def disp(w): return re.sub(r"[.,…!?:]","",w).upper()
AM=r"{\c&H00FFFF&}"; BR=r"{\c&HFFFFFF&}"
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 720
PlayResY: 1280
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: H,Poppins,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,3,0,1,0,3,5,20,20,0,1
Style: S,Anton,116,&H00FFFFFF,&H00FFFFFF,&H00141414,&H90000000,0,0,0,0,112,100,0,0,1,5,4,5,20,20,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ts=LEG._ts; lin=[]; txt=[]
def emite(bl, estilo, y, fim_ult, pop):
    for i,b in enumerate(bl):
        ini=b[0][1]
        fim=min(bl[i+1][0][1], b[-1][2]+0.6) if i+1<len(bl) else fim_ult
        txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
        for k,w in enumerate(b):
            a=ini if k==0 else w[1]; z=b[k+1][1] if k+1<len(b) else fim
            if z<=a: continue
            partes=[(AM if j==k else BR)+disp(x[0]) for j,x in enumerate(b)]
            p=r"{\an5\pos(360,"+str(y)+")"+((r"\fscx85\fscy85\t(0,90,\fscx105\fscy105)\t(90,160,\fscx100\fscy100)" if (k==0 and pop) else "")+"}")
            lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},{estilo},,0,0,0,,{p}{' '.join(partes)}")
emite(LEG._blocos([tuple(p) for p in hook]),"H",1003,HK,False)
# corpo: CTA em blocos fixos
pal=[list(p) for p in corpo]
ia=next(i for i,w in enumerate(pal) if disp(w[0])=="TAP")
cta=pal[ia:ia+4]  # TAP LEARN MORE BELOW
bl=LEG._blocos([tuple(p) for p in pal[:ia]])+[[tuple(x) for x in cta[:3]],[tuple(cta[3])]]+LEG._blocos([tuple(p) for p in pal[ia+4:]])
def junta(bl):
    out=[]
    for i,b in enumerate(bl):
        dur=(bl[i+1][0][1] if i+1<len(bl) else TOTAL)-b[0][1]
        if len(b)==1 and dur<0.35 and out and len(" ".join(x[0] for x in out[-1]+b))<=19 and not out[-1][-1][0].endswith((".", "?", "!", ":")):
            out[-1]=out[-1]+b
        elif out and len(out[-1])==1 and (b[0][1]-out[-1][0][1])<0.35 and len(" ".join(x[0] for x in out[-1]+b))<=19:
            out[-1]=out[-1]+b
        else: out.append(list(b))
    return out
bl=junta(bl)
bl[0][0]=(bl[0][0][0],HK,bl[0][0][2])  # 1o bloco do ceu entra no corte (cobre a faixa do LaMa)
emite(bl,"S",1003,TOTAL,True)
open("leg_en.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_en.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(txt),"blocos; CTA em",pal[ia][1])
for x in txt[:8]+txt[-12:]: print(x)
