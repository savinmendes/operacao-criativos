# Legenda karaokê no estilo do AD ES/FR: Poppins ExtraBold 83 caixa alta, branco + palavra falada em amarelo, centro y=1465
import json,re,sys
sys.path.insert(0,r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import legenda as LEG
W=[tuple(w) for w in json.load(open('audio/voz_en_words.json',encoding='utf-8'))]
TL=json.load(open('timeline.json')); total=TL['total']
def disp(w): return re.sub(r"[.,!?«»<>…]","",w).upper().replace("'","’")
TAM=[3,3,3,3,3,3, 3,3,3,3,2, 3, 3,2,3, 1,3,3,2,1,3,2,1, 3,3,2, 3,2,3,2, 2,2,3,1]
assert sum(TAM)==len(W),(sum(TAM),len(W))
BL=[];k=0
for t in TAM: BL.append(W[k:k+t]); k+=t
Y=1465; FS=83
head=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: C,Poppins ExtraBold,{FS},&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0,0,1,6,3,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
AM=r"{\c&H31C7FD&}"; BR=r"{\c&HFFFFFF&}"; ts=LEG._ts
L=[]
for k,b in enumerate(BL):
    ini=0.0 if k==0 else (b[0][1]-0.2 if b[0][0]=='Tap' else b[0][1])
    nxt=BL[k+1][0][1] if k+1<len(BL) else total
    fim=min(nxt,b[-1][2]+0.6) if k+1<len(BL) else total
    for j,w in enumerate(b):
        a=ini if j==0 else w[1]; e=b[j+1][1] if j+1<len(b) else fim
        if e<=a: continue
        partes=[(AM if jj==j else BR)+disp(x[0]) for jj,x in enumerate(b)]
        pop=r"{\an5\pos(540,%d)"%Y
        if j==0: pop+=r"\fscx80\fscy80\t(0,90,\fscx106\fscy106)\t(90,160,\fscx100\fscy100)"
        pop+="}"
        L.append(f"Dialogue: 0,{ts(a)},{ts(e)},C,,0,0,0,,{pop}{' '.join(partes)}")
open('leg_en.ass','w',encoding='utf-8').write(head+"\n".join(L)+"\n")
for b in BL: print(round(b[0][1],2),' '.join(disp(x[0]) for x in b))
