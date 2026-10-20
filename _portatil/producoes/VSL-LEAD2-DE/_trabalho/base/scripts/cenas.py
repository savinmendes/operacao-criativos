import numpy as np, cv2, json, subprocess
a=np.load("cenas/thumbs.npy")
small=np.array([cv2.resize(x[20:180],(24,32)).astype(np.float32).ravel() for x in a]); small-=small.mean(1,keepdims=True); small/=np.linalg.norm(small,axis=1,keepdims=True)+1e-6
refs={"igreja_geral":[217,221,224,2151,2154],"padre_altar":[230,240,250,300],"pulpito_vazio":[280,458],"padre_pulpito":[757,822,1017,1935,2140,285,315,507,553],
"padre_medio":[400,420,470,495,990,1100,1200,1400,1500,1650,2000,2100,980,1078,1191,1378,1598],
"igreja_altar_padre":[440,450],"papa":[340,360,380],"dep_mulher_casa":[600],"dep_homem_terno":[620,640,660],"dep_mulher_oculos":[680,690,700],"padre_close":[2200,2300,2450],"estatua":[2147,583]}
R=[];L=[]
for k,ts in refs.items():
    for t in ts: R.append(small[int(t*2)]); L.append(k)
sim=small@np.array(R).T
fig=(small@small[[2,6,40,180]].T).max(1)
lab=[("abertura_figura_branca" if fig[i]>0.6 else "abertura_broll") if i/2<206 else L[sim[i].argmax()] for i in range(len(a))]
# suaviza: runs < 2 s absorvidos pelo vizinho anterior
def runs(lab):
    r=[];s=0
    for i in range(1,len(lab)+1):
        if i==len(lab) or lab[i]!=lab[s]: r.append([s,i,lab[s]]); s=i
    return r
for _ in range(3):
    rr=runs(lab)
    for k,(s,e,l) in enumerate(rr):
        if e-s<(2 if l.startswith('abertura') else 4) and k>0:
            for i in range(s,e): lab[i]=rr[k-1][2]
rr=runs(lab)
# refina fronteira no quadro de maior diferenca (30 fps) em +-1.2 s
def refinar(t):
    t0=max(0,t-1.2)
    p=subprocess.run(["ffmpeg","-v","error","-ss",f"{t0:.3f}","-i",r"C:\Users\PICHAU\Downloads\Lead 2.mp4","-t","2.4","-vf","scale=90:120,format=gray","-f","rawvideo","-"],capture_output=True).stdout
    f=np.frombuffer(p,np.uint8).reshape(-1,120,90)[:,10:95].astype(np.float32); d=np.abs(np.diff(f,axis=0)).mean((1,2))
    j=int(d.argmax())+1; return round(t0+j/30,3), float(d.max())
cenas=[]
for s,e,l in rr:
    cenas.append({"ini":s/2,"fim":e/2,"tipo":l})
for k in range(1,len(cenas)):
    t,dm=refinar(cenas[k]["ini"]); 
    if dm>8: cenas[k]["ini"]=t; cenas[k-1]["fim"]=t
    else: cenas[k]["fronteira_suave"]=True; cenas[k-1]["fim"]=cenas[k]["ini"]
cenas[-1]["fim"]=2563.3
cenas=[c for c in cenas if c["fim"]-c["ini"]>0.05]
for k in range(1,len(cenas)): cenas[k]["ini"]=cenas[k-1]["fim"]
GRUPO={"abertura_broll":"abertura b-roll","abertura_figura_branca":"abertura: apresentador de batina branca (parece um Papa; CONFIRMAR com a pessoa)","igreja_geral":"b-roll igreja","estatua":"b-roll igreja","pulpito_vazio":"b-roll igreja",
"papa":"PAPA (cortar)","dep_mulher_casa":"depoimento","dep_homem_terno":"depoimento","dep_mulher_oculos":"depoimento",
"padre_medio":"padre plano medio","padre_pulpito":"padre plano medio (pulpito, mais aberto)","padre_altar":"padre plano medio (altar, livro)",
"igreja_altar_padre":"padre plano geral (pequeno, sem lipsync)","padre_close":"padre close"}
for c in cenas:
    c["grupo"]=GRUPO[c["tipo"]]; c["ini_q"]=round(c["ini"]*30); c["fim_q"]=round(c["fim"]*30)
    m=lambda x:f"{int(x//60):02d}:{x%60:05.2f}"; c["ini_mmss"]=m(c["ini"]); c["fim_mmss"]=m(c["fim"])
json.dump({"fonte":r"C:\Users\PICHAU\Downloads\Lead 2.mp4","fps":30,"nota":"rotulos automaticos (similaridade com quadros de referencia, 2 fps) + fronteira refinada no quadro de maior diferenca; 'fronteira_suave' = transicao gradual (fusao), conferir a olho","cenas":cenas},open("cenas.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for c in cenas: print(c["ini_mmss"],c["fim_mmss"],round(c["fim"]-c["ini"],1),c["tipo"],"*" if c.get("fronteira_suave") else "")
