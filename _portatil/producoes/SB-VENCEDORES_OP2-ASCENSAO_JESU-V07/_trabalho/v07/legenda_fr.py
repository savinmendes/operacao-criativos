# Legenda karaokê no estilo do AD ES: Poppins Bold caixa alta, branco + palavra falada em amarelo, centro y=1465
import json,re
W=json.load(open('audio/voz_fr_words.json',encoding='utf-8'))
TL=json.load(open('timeline.json'))
BL=[[0,1,2],[3,4],[5],[6,7],[8,9],[10,11],[12,13,14],[15,16],[17,18,19],[20,21,22],[23,24,25],[26,27],[28,29],
[30,31,32],[33,34,35],[36,37],[38],[39,40],[41,42],[43,44,45],[46,47],[48],[49,50],[51,52],[53,54],[55,56],[57,58],[59,60],
[61,62],[63,64,65],[66,67],[68,69],[70,71],[72,73],[75,76,77],[79],[80,81,82],[83,84],[85,86],[87,88,89],[90,91]]
assert sorted(sum(BL,[]))==[i for i in range(92) if i not in (74,78)]
def txt(i): return re.sub(r"[.,!?«»<>]","",W[i][0]).upper().replace("'","’")
def ts(t): h=int(t//3600);m=int(t%3600//60);s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
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
AM=r"{\c&H31C7FD&}"; BR=r"{\c&HFFFFFF&}"
L=[]
total=TL['total']
for k,b in enumerate(BL):
    ini=0.0 if k==0 else W[b[0]][1]
    nxt=W[BL[k+1][0]][1] if k+1<len(BL) else total
    fim=min(nxt, W[b[-1]][2]+0.6) if k+1<len(BL) else total
    for j,i in enumerate(b):
        a=ini if j==0 else W[i][1]; e=W[b[j+1]][1] if j+1<len(b) else fim
        partes=[(AM if ii==i else BR)+txt(ii) for ii in b]
        pop=r"{\an5\pos(540,%d)"%Y
        if j==0: pop+=r"\fscx80\fscy80\t(0,90,\fscx106\fscy106)\t(90,160,\fscx100\fscy100)"
        pop+="}"
        L.append(f"Dialogue: 0,{ts(a)},{ts(e)},C,,0,0,0,,{pop}{' '.join(partes)}")
open('leg_fr.ass','w',encoding='utf-8').write(head+"\n".join(L)+"\n")
print(len(L),'eventos')
