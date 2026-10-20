# Legenda EN no estilo do AD ES 12: Poppins Bold caixa alta, branco com sombra difusa, palavras-chave coloridas, blocos <=3 palavras
import sys, re, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas")
import legenda as LEG
from palavras import palavras
CJ=json.load(open("cortes_en.json")); TOTAL=CJ["C"][-1]
Y=1160
pal=[list(p) for p in palavras("audio/voz_en_p.alinhamento.json")]
def disp(w): return re.sub(r"[.,…!?]","",w).upper()
VM=r"{\c&H2020F0&}"; AM=r"{\c&H00F0FF&}"; VD=r"{\c&H28E040&}"; BR=r"{\c&HFFFFFF&}"
COR={"MIRACLE":VM,"PREPARED":AM,"GIFT":VM,"HEAR":AM,"PRAYER":AM,"BLESSINGS":VD,"LIFE":VM,"LEARN":AM,"MORE":AM,"NOW":VD,"CHOSEN":AM,"LAST":VM}
TAM=[4,4,3,2,4,3,3,2,2,4,2,4,4,3,4,4,3,3,4,2,3,4,4,5,2,3,4]
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
    s=" ".join((COR.get(disp(w[0]),BR))+disp(w[0])+BR for w in b)
    txt.append((round(ini,2),round(fim,2)," ".join(disp(w[0]) for w in b)))
    lin.append(f"Dialogue: 0,{LEG._ts(ini)},{LEG._ts(fim)},C,,0,0,0,,"+r"{\an5\pos(540,"+str(1560 if ini>=CJ["C"][5]-0.1 else Y)+r")\blur3\fscx85\fscy85\t(0,100,\fscx104\fscy104)\t(100,170,\fscx100\fscy100)}"+s)
open("leg_en.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
json.dump(txt,open("blocos_en.json","w",encoding="utf-8"),indent=0)
for x in txt: print(x)
