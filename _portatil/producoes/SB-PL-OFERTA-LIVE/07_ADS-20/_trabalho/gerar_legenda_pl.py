# Legenda PL no estilo do ADS 20 ES: gancho = Poppins Bold pequena (branco + palavra falada amarela);
# ceu = Anton caixa alta, contorno preto, palavra falada amarela, blocos <=3 palavras/18 chars. PlayRes 720x1280.
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
T=json.load(open("tempos.json")); TOTAL=T["TOTAL"]; HK=T["HK"]; C0=T["C0"]
LEG.MAX_PAL=3; LEG.MAX_CHR=16
hook=palavras("audio/hook1_pl.alinhamento.json",0.08)+palavras("audio/hook2_pl.alinhamento.json",2.55)
corpo=palavras("audio/corpo_pl_p.alinhamento.json",C0)
def disp(w): return re.sub(r"[.,…!?:]","",w).replace("«",chr(0x201E)).replace("»",chr(0x201D)).upper()
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
from PIL import ImageFont, ImageDraw, Image
_F={"S":(ImageFont.truetype("fonts/Anton-Regular.ttf",67),1.12),"H":(ImageFont.truetype("fonts/Poppins-Bold.ttf",49),1.0)}
_D=ImageDraw.Draw(Image.new("RGB",(4,4)))
def larg(t,est):
    f,sx=_F[est]; b=_D.textbbox((0,0),t,font=f); return (b[2]-b[0])*sx
def emite(bl, estilo, y, fim_ult, pop):
    for i,b in enumerate(bl):
        ini=b[0][1]
        fim=min(bl[i+1][0][1], b[-1][2]+0.6) if i+1<len(bl) else fim_ult
        txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
        L=larg(" ".join(disp(w[0]) for w in b),estilo); esc=min(100,int(66000/L)) if L>0 else 100
        if esc<100: print("encolhe",esc," ".join(disp(w[0]) for w in b))
        for k,w in enumerate(b):
            a=ini if k==0 else w[1]; z=b[k+1][1] if k+1<len(b) else fim
            if z<=a: continue
            partes=[(AM if j==k else BR)+disp(x[0]) for j,x in enumerate(b)]
            p=r"{\an5\pos(360,"+str(y)+")"+(rf"\fscx{int(112*esc/100)}" if esc<100 and estilo=="S" else "")+((r"\fscx85\fscy85\t(0,90,\fscx105\fscy105)\t(90,160,\fscx100\fscy100)" if (k==0 and pop and esc>=100) else "")+"}")
            lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},{estilo},,0,0,0,,{p}{' '.join(partes)}")
emite(LEG._blocos([tuple(p) for p in hook]),"H",1003,HK-0.04,False)
# corpo: CTA em blocos fixos
pal=[list(p) for p in corpo]
ia=next(i for i,w in enumerate(pal) if disp(w[0])=="DOTKNIJ")
cta=pal[ia:ia+5]  # DOTKNIJ «DOWIEDZ SIĘ WIĘCEJ» PONIŻEJ
bl=LEG._blocos([tuple(p) for p in pal[:ia]])+[[tuple(cta[0])],[tuple(x) for x in cta[1:4]],[tuple(cta[4])]]+LEG._blocos([tuple(p) for p in pal[ia+5:]])
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
# nao deixar preposicao/conjuncao curta no fim do bloco (NA | ZYWO): passa p/ o bloco seguinte
PREP={"NA","DO","O","W","Z","ZE","I","A","OD","PO","PRZY","PRZEZ","DLA","NIE","TO","CO","ŻE","BY","ABY","BO","TAK"}
for i in range(len(bl)-1):
    b=bl[i]
    if len(b)>1 and disp(b[-1][0]) in PREP and not b[-1][0].endswith((",",".",":")) and len(" ".join(disp(x[0]) for x in [b[-1]]+list(bl[i+1])))<=19:
        bl[i+1]=[b[-1]]+list(bl[i+1]); bl[i]=b[:-1]
for i in range(len(bl)-2,-1,-1):
    if len(bl[i])==1 and bl[i+1][0][1]-bl[i][0][1]<0.3 and len(" ".join(disp(x[0]) for x in list(bl[i])+list(bl[i+1])))<=19:
        bl[i+1]=list(bl[i])+list(bl[i+1]); del bl[i]
bl[0][0]=(bl[0][0][0],HK,bl[0][0][2])  # 1o bloco do ceu entra no corte (cobre a faixa do LaMa)
emite(bl,"S",1003,TOTAL,True)
open("leg_pl.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_pl.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(len(txt),"blocos; CTA em",pal[ia][1])
for x in txt[:8]+txt[-12:]: print(x)
