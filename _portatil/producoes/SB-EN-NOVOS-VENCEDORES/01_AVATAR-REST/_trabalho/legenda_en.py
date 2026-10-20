# Legenda EN no estilo do AD ES (igual legenda_fr.py): caixa alta, Poppins ExtraBold, branco com contorno preto grosso e 1 palavra
# amarela, blocos de 1-3 palavras (1 linha) que não atravessam corte de cena. Sobe quando a faixa do CTA aparece.
import json, re, sys
W=json.load(open("palavras_en.json",encoding="utf-8")); T=json.load(open("timeline.json",encoding="utf-8"))
CTA_INI=float(sys.argv[1]) if len(sys.argv)>1 else 43.92   # setas do CTA aparecem (fonte 55,33 s)
cortes=[c["out_ini"] for c in T["cenas"]][1:]
P=[list(x) for x in W]
def disp(w): return re.sub(r"[.,…!?;:]","",w).upper()
STOP=set("THE A AN OF TO AND I MY ME YOU YOUR IS ON IN FROM THIS THAT IT IF CAN WILL FOR BY ABOUT DURING WITH HE BUT WAY".split())
AMAR={"GLORIOUS","SAINT","BENEDICT","MEDAL","ENGRAVED","DELIVER","HARDSHIP","HELP","SIX","MONTHS","CUSTOMERS","CLOSING","BUSINESS","LIVE",
      "STREAM","PRIEST","EXACT","PEACE","DOORS","OPEN","LAST","GOD","JESUS","CHOSE","POWERFUL","GIFT","TODAY","LOST","PRAYER","SHOWER",
      "MIRACLES","REJECT","MIRACLE","DOOR","FOREVER","NOW","BROADCAST","LEARN","MORE","JOIN","WORDS","AGAIN"}
U=[]; k=0
while k<len(P):
    d=disp(P[k][0])
    if d=="SAINT" and k+1<len(P): U.append([P[k],P[k+1]]); k+=2; continue
    if d=="LEARN" and k+1<len(P) and disp(P[k+1][0])=="MORE": U.append([P[k],P[k+1]]); k+=2; continue
    U.append([P[k]]); k+=1
blocos=[]; cur=[]
def ntx(ws): return " ".join(disp(y[0]) for y in ws)
from PIL import ImageFont
FNT=ImageFont.truetype("fonts/Poppins-ExtraBold.ttf",112)
def larg(ws): return 99 if FNT.getlength(ntx(ws))+20>960 else len(ntx(ws))
for u in U:
    if cur:
        cruza=any(cur[0][1]<c<=u[0][1]+0.02 for c in cortes)
        gap=u[0][1]-cur[-1][2]
        if len(cur)+len(u)>3 or larg(cur+u)>16 or cruza or gap>0.35 or re.search(r"[.,!?]$",cur[-1][0]) or u[0][3]!=cur[-1][3]:
            mov=[]
            while len(cur)>1 and disp(cur[-1][0]) in STOP and not re.search(r"[.,!?]$",cur[-1][0]) and not cruza and gap<=0.35 and larg([cur[-1]]+mov+u)<=16:
                mov.insert(0,cur.pop())
            blocos.append(cur); cur=mov
    cur=cur+u
if cur: blocos.append(cur)
k=0
while k<len(blocos)-1:
    b=blocos[k]
    if len(b)==1 and (disp(b[0][0]) in STOP or b[0][2]-b[0][1]<0.2) and blocos[k+1][0][3]==b[0][3] and blocos[k+1][0][1]-b[0][2]<0.4 \
       and larg(b+blocos[k+1])<=16 and not any(b[0][1]<c<=blocos[k+1][0][1]+0.02 for c in cortes):
        blocos[k+1]=b+blocos[k+1]; del blocos[k]; continue
    # palavra funcional sozinha e curtíssima que não cabe no seguinte: puxa a última palavra do bloco anterior
    if len(b)==1 and disp(b[0][0]) in STOP and k>0 and len(blocos[k-1])>1 and blocos[k-1][-1][3]==b[0][3] and b[0][1]-blocos[k-1][-1][2]<0.2:
        blocos[k]=[blocos[k-1].pop()]+b
    k+=1
# passada final: bloco de 1 palavra com < 0,2 s junta com o seguinte (ou o anterior) se couber e não houver corte
k=0
while k<len(blocos):
    b=blocos[k]
    if len(b)==1 and b[0][2]-b[0][1]<0.2:
        nx=blocos[k+1] if k+1<len(blocos) else None; pv=blocos[k-1] if k>0 else None
        if nx and nx[0][3]==b[0][3] and larg(b+nx)<=16 and not any(b[0][1]<c<=nx[0][1]+0.02 for c in cortes):
            blocos[k+1]=b+nx; del blocos[k]; continue
        if pv and pv[-1][3]==b[0][3] and larg(pv+b)<=16 and not any(pv[0][1]<c<=b[0][1]+0.02 for c in cortes):
            pv.extend(b); del blocos[k]; continue
    k+=1
def ts(t):
    t=max(0,t); h=int(t//3600); m=int(t%3600//60); s=t%60; return f"{h}:{m:02d}:{s:05.2f}"
head="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Poppins ExtraBold,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,10,4,5,30,30,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
def ini(b):
    a=b[0][1]-0.04
    for c in cortes:
        if 0<c-a<0.07: a=c          # não acende 1 quadro antes do corte
    return a
lin=[]; rel=[]
for i,b in enumerate(blocos):
    a=ini(b)
    z=ini(blocos[i+1]) if i+1<len(blocos) else T["total"]
    z=min(z,b[-1][2]+0.45)
    for c in cortes:
        if a<c<z and c-a>0.25: z=min(z,c)
    if i+1<len(blocos) and 0<ini(blocos[i+1])-z<0.15: z=ini(blocos[i+1])   # sem buraco de 1-3 quadros entre blocos
    y=1230 if a>=CTA_INI-0.15 else 1389
    ws=[disp(w[0]) for w in b]
    if "LEARN" in ws: am=["LEARN","MORE"]
    else:
        am=[x for x in ws if x in AMAR]
        if not am:
            cand=[x for x in ws if x not in STOP]; am=[max(cand,key=len)] if cand else []
        am=am[-1:]
    corpo=" ".join((r"{\c&H55E3FB&}"+x+r"{\c&HFFFFFF&}") if x in am else x for x in ws)
    lin.append(rf"Dialogue: 0,{ts(a)},{ts(z)},L,,0,0,0,,{{\an5\pos(540,{y})}}{corpo}")
    rel.append((round(a,2),round(z,2)," ".join(ws)))
lin.append(rf"Dialogue: 0,{ts(CTA_INI)},{ts(T['total']+1)},L,,0,0,0,,{{\an5\pos(540,1519)\fad(120,0)\fs96}}TAP {{\c&H55E3FB&}}“LEARN MORE”")
open("leg_en.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
for r in rel: print(r)
