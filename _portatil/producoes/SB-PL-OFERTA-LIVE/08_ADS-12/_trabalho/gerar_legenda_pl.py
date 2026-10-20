# Legenda PL no estilo do AD ES 12: Poppins Bold caixa alta, branco com sombra difusa, palavras-chave coloridas, blocos <=3 palavras
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
CJ=json.load(open("cortes_pl.json")); TOTAL=CJ["C"][-1]
Y=1160
pal=[list(p) for p in palavras("audio/voz_pl_p.alinhamento.json")]
def disp(w): return re.sub(r'[.,…!?]','',w.replace(',,','«')).upper().replace('"','»')
VM=r"{\c&H2020F0&}"; AM=r"{\c&H00F0FF&}"; VD=r"{\c&H28E040&}"; BR=r"{\c&HFFFFFF&}"
COR={"CUD":VM,"CUDÓW":VM,"DAR":VM,"ŻYCIE":VM,"OSTATNIA":VM,"PRZYGOTOWAŁEM":AM,"WYBRAŁ":AM,"USŁYSZYSZ":AM,"MODLITWĘ":AM,"MODLITWY":AM,"BŁOGOSŁAWIEŃSTW":VD,"ŻYWO":VD}
TAM=[3,4,3,2,3,1,3,3,4,1,3,2,2,2,1,2,2,2,3,2,2,3,1,1,3,1,2,2,2,3,2,2]
assert sum(TAM)==len(pal),(sum(TAM),len(pal))
bl=[];k=0
for t in TAM: bl.append(pal[k:k+t]); k+=t
head=f"""[Script Info]
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
lin=[]; txt=[]
for i,b in enumerate(bl):
    ini=b[0][1]-0.03
    fim=min(bl[i+1][0][1]-0.03, b[-1][2]+0.7) if i+1<len(bl) else TOTAL
    for cc in CJ["C"][1:-1]:
        if ini<cc-0.2 and fim>cc: fim=cc-0.01   # bloco nao invade a cena seguinte
    cta=any(disp(w[0])=="«DOWIEDZ" for w in b)
    s=" ".join((AM if cta and disp(w[0]) in ("«DOWIEDZ","SIĘ","WIĘCEJ»") else COR.get(disp(w[0]),BR))+disp(w[0])+BR for w in b)
    txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
    lin.append(f"Dialogue: 0,{LEG._ts(ini)},{LEG._ts(fim)},C,,0,0,0,,"+r"{\an5\pos(540,"+str(1560 if ini>=CJ["C"][5]-0.1 else Y)+r")\blur3\fscx85\fscy85\t(0,100,\fscx104\fscy104)\t(100,170,\fscx100\fscy100)}"+s)
open("leg_pl.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_pl.json","w",encoding="utf-8"),indent=0)
for x in txt: print(x)
