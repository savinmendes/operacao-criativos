# Legenda PL no estilo do AD ES: caixa alta, branco com brilho escuro, palavra-chave colorida, 1-2 linhas por bloco,
# posição por cena (como no ES). Blocos aparecem na 1ª palavra; palavra-chave em cor fixa.
import json, re
W=json.load(open("palavras_pl.json",encoding="utf-8")); TOTAL=31.60
# cortes de cena do ES e y do centro da legenda (px no quadro 1080x1920)
CENAS=[(0,5.067,1515),(5.067,10.0,1545),(10.0,14.6,1170),(14.6,18.667,1260),(18.667,22.967,1230),(22.967,26.1,1185),(26.1,99,1545)]
# blocos (n palavras) — quebra natural de frase
BLOCOS="""JEŚLI MNIE|ZIGNORUJESZ|NIE BĘDĘ MIAŁ WYBORU|I ODDAM KOMUŚ INNEMU|CUD|KTÓREGO TAK BARDZO|POTRZEBUJESZ|TO TWOJA|OSTATNIA SZANSA|BY OTRZYMAĆ TO|CO DLA CIEBIE|PRZYGOTOWAŁEM|JEZUS CIĘ WYBRAŁ|PRZYNIÓSŁ CI|POTĘŻNY DAR|DZIŚ USŁYSZYSZ|STAROŻYTNĄ|ZAGINIONĄ MODLITWĘ|Z BIBLII|KTÓRA SPROWADZI|NA TWOJE ŻYCIE|DESZCZ|BŁOGOSŁAWIEŃSTW|I CUDÓW|NIE ODRZUCAJ MNIE|ZNOWU|DOTKNIJ|DOWIEDZ SIĘ WIĘCEJ|PONIŻEJ I|DOŁĄCZ DO|MODLITWY NA ŻYWO|ODBIERZ SWÓJ CUD|ZANIM BĘDZIE|ZA PÓŹNO""".split("|")
TAM=[len(x.split()) for x in BLOCOS]
COR={"ZIGNORUJESZ":"R","CUD":"R","CUDÓW":"R","OSTATNIA":"R","SZANSA":"R","PRZYGOTOWAŁEM":"Y","WYBRAŁ":"Y","DAR":"R","USŁYSZYSZ":"Y",
     "MODLITWĘ":"Y","MODLITWY":"Y","BŁOGOSŁAWIEŃSTW":"G","ŻYCIE":"R","ODRZUCAJ":"R","ŻYWO":"Y","PÓŹNO":"R"}
HEX={"R":"&H2626FF&","Y":"&H2EF2FF&","G":"&H3DE65A&","W":"&HFFFFFF&"}
assert sum(TAM)==len(W),(sum(TAM),len(W))
bl=[];k=0
for t in TAM: bl.append(W[k:k+t]); k+=t
def disp(w): return re.sub(r"[.,…!?:«»]","",w).upper()
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: G,Poppins,84,&H00FFFFFF,&H00FFFFFF,&H30000000,&H00000000,0,0,0,0,100,100,1,0,1,12,0,5,50,50,0,1
Style: C,Poppins,84,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,1,0,1,2,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
lin=[]; txt=[]
for i,b in enumerate(bl):
    a=b[0][1]-0.05; z=bl[i+1][0][1]-0.05 if i+1<len(bl) else TOTAL
    z=min(z,b[-1][2]+0.8) if i+1<len(bl) else TOTAL
    # não atravessa corte de cena
    t0=b[0][1]+0.12  # bloco que começa colado antes de um corte usa a posição da cena seguinte
    cen=next(c for c in CENAS if c[0]<=t0<c[1]); y=cen[2]; a=max(a,cen[0]) if a<cen[0] else a
    if b[-1][2]<=cen[1]: z=min(z,cen[1])  # não atravessa corte de cena
    if i+1<len(bl) and cen[0]<=bl[i+1][0][1]-0.05<cen[1]<bl[i+1][0][1]+0.12: z=cen[1]  # próximo bloco só entra no corte: sem buraco
    ws=[disp(w[0]) for w in b]
    linhas=[ws]
    if len(" ".join(ws))>16 and len(ws)>=2:
        h=(len(ws)+1)//2; linhas=[ws[:h],ws[h:]]
    NL=chr(92)+"N"
    s=NL.join(" ".join(l) for l in linhas)
    pos="{"+chr(92)+"an5"+chr(92)+"pos(540,"+str(y)+")"+chr(92)+"fad(40,0)"
    sc="DOWIEDZ" in ws
    cor=lambda x: "{"+chr(92)+"c"+HEX["Y" if sc else COR.get(x,"W")]+"}"+x
    corpo=NL.join(" ".join(cor(x) for x in l) for l in linhas)
    lin.append(f"Dialogue: 0,{ts(a)},{ts(z)},G,,0,0,0,,{pos}\blur9\3c&H000000&}}{s}")
    lin.append(f"Dialogue: 1,{ts(a)},{ts(z)},C,,0,0,0,,{pos}\blur1}}{corpo}")
    txt.append((round(a,2),round(z,2),s))
open("leg_pl.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
for x in txt: print(x)
