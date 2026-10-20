# Legenda FR no estilo do AD ES: caixa alta, Poppins ExtraBold, branco com contorno preto grosso e 1 palavra amarela,
# blocos de 1-3 palavras (1 linha) que não atravessam corte de cena. y por trecho (sobe quando a faixa do CTA aparece).
import json, re, sys
W=json.load(open("palavras_fr.json",encoding="utf-8")); T=json.load(open("timeline.json",encoding="utf-8"))
CTA_INI=float(sys.argv[1]) if len(sys.argv)>1 else 47.67   # saída: quando a faixa/setas aparecem
cortes=[c["out_ini"] for c in T["cenas"]][1:]
# junta guillemets
P=[]
for w,s,e,p in W:
    if w in ("«","<<"): P.append(["«",s,e,p]); continue
    if w=="»" and P: P[-1][0]+="»"; P[-1][2]=e; continue
    if P and P[-1][0]=="«": P[-1]=["«"+w,P[-1][1],e,p]; continue
    P.append([w,s,e,p])
def disp(w): return re.sub(r"[.,…!?;:]","",w).upper()
STOP=set("LE LA LES DE DU DES UN UNE ET EN À A AU SUR TA TON TU TE T'A IL QUI QUE NE PAS SI MON MA MES CE CETTE J'AI SANS POUR DANS EST ONT SE".split())
AMAR={"GLORIEUX","SAINT","BENOÎT","MÉDAILLE","DÉLIVRE-MOI","MISÈRE","AIDE-MOI","SIX","CLIENTS","FERMER","COMMERCE","JOUR","DIRECT","PRÊTRE",
      "EXACTE","PAIX","PETIT","PORTES","S'OUVRIR","DERNIÈRE","DIEU","JÉSUS","CHOISI","CADEAU","PUISSANT","TOI","VIDÉO","ÉCOUTER","PRIÈRE",
      "PERDUE","PLUIE","MIRACLES","REFUSES","MIRACLE","PORTE","TOUJOURS","MOMENT","DIFFUSÉE","«EN","SAVOIR","PLUS»","REJOINS","PRONONCE","GRAVÉES","PAROLES"}
# unidades indivisíveis: SAINT BENOÎT, «EN SAVOIR PLUS»
U=[]; k=0
while k<len(P):
    x=P[k]
    if disp(x[0])=="SAINT" and k+1<len(P): U.append([P[k],P[k+1]]); k+=2; continue
    if disp(x[0])=="«EN" and k+2<len(P): U.append(P[k:k+3]); k+=3; continue
    U.append([x]); k+=1
blocos=[]; cur=[]
def ntx(ws): return " ".join(disp(y[0]) for y in ws)
for u in U:
    if cur:
        cruza=any(cur[0][1]<c<=u[0][1]+0.02 for c in cortes)
        gap=u[0][1]-cur[-1][2]
        if len(cur)+len(u)>3 or len(ntx(cur+u))>16 or cruza or gap>0.35 or re.search(r"[.,!?]$",cur[-1][0]) or u[0][3]!=cur[-1][3]:
            # palavra funcional no fim passa para o bloco seguinte (se não houver corte/pausa)
            mov=[]
            while len(cur)>1 and disp(cur[-1][0]) in STOP and not re.search(r"[.,!?]$",cur[-1][0]) and not cruza and gap<=0.35 and len(ntx([cur[-1]]+mov+u))<=16:
                mov.insert(0,cur.pop())
            blocos.append(cur); cur=mov
    cur=cur+u
if cur: blocos.append(cur)
# bloco de 1 palavra funcional (ou curtíssimo) junta com o seguinte
k=0
while k<len(blocos)-1:
    b=blocos[k]
    if len(b)==1 and (disp(b[0][0]) in STOP or b[0][2]-b[0][1]<0.2) and blocos[k+1][0][3]==b[0][3] and blocos[k+1][0][1]-b[0][2]<0.4:
        blocos[k+1]=b+blocos[k+1]; del blocos[k]; continue
    k+=1
# guillemets: «EN SAVOIR PLUS» sempre junto num bloco
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
lin=[]; rel=[]
for i,b in enumerate(blocos):
    a=b[0][1]-0.04
    z=blocos[i+1][0][1]-0.04 if i+1<len(blocos) else T["total"]
    z=min(z,b[-1][2]+0.45)
    for c in cortes:
        if a<c<z and c-a>0.25: z=min(z,c)
    y=1230 if a>=CTA_INI-0.15 else 1389
    ws=[disp(w[0]) for w in b]
    am=[x for x in ws if x in AMAR]
    if not am:
        cand=[x for x in ws if x not in STOP]
        am=[max(cand,key=len)] if cand else []
    if "«EN" in ws or "SAVOIR" in ws: am=[x for x in ws if x in ("«EN","SAVOIR","PLUS»")]
    else: am=am[-1:]
    corpo=" ".join((r"{\c&H55E3FB&}"+x+r"{\c&HFFFFFF&}") if x in am else x for x in ws)
    lin.append(rf"Dialogue: 0,{ts(a)},{ts(z)},L,,0,0,0,,{{\an5\pos(540,{y})}}{corpo}")
    corpo=corpo.replace('«EN','« EN').replace('PLUS»','PLUS »')
    lin[-1]=lin[-1].replace('«EN','« EN').replace('PLUS»','PLUS »')
    rel.append((round(a,2),round(z,2)," ".join(ws)))
lin.append(rf"Dialogue: 0,{ts(CTA_INI)},{ts(T['total']+1)},L,,0,0,0,,{{\an5\pos(540,1519)\fad(120,0)\fs104}}APPUIE SUR {{\c&H55E3FB&}}« EN SAVOIR PLUS »")
open("leg_fr.ass","w",encoding="utf-8").write(head+"\n".join(lin)+"\n")
for r in rel: print(r)
