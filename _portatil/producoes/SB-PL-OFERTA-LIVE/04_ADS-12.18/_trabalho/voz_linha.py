# Frases PL na linha do tempo. Cena 1 alongada 5.067->5.6 s (s1 a 0.905x) e cena 7 5.4->6.5 s (montada sem os trechos
# de sorriso do original: ver heygen_in_pl.py), para caber o polones com uma pausa real no meio.
# -> audio/voz_pl.wav + audio/palavras_pl.json + cortes_pl.json
import soundfile as sf, numpy as np, subprocess, json
from palavras import palavras
SR=48000; TOTAL=33.133
CUTS=[0,5.6,10.533,15.133,19.2,23.5,26.633,TOTAL]
INI={"p1":0.0,"p2":6.25,"p3":10.8,"p4":12.8,"p5":15.9,"p6":23.65,"p7":26.733}
PAUSA={"p1":[("zignorujesz,",0.32)],"p7":[("żywo.",0.25)]}
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
v=np.zeros((int(TOTAL*SR),2),np.float32); pal=[]
for k,t0 in INI.items():
    a=load(f"audio/{k}.mp3"); pw=palavras(f"audio/{k}.alinhamento.json")
    ins=[]
    for w,d in PAUSA.get(k,[]):
        q=[i for i,x in enumerate(pw) if x[0]==w][0]; ins.append(((pw[q][2]+pw[q+1][1])/2,d))
    out=[];prev=0
    for t,d in ins:
        i=int(t*SR); out+=[a[prev:i],np.zeros((int(d*SR),2),np.float32)]; prev=i
    out.append(a[prev:]); a=np.concatenate(out)
    sh=lambda x: x+sum(d for t,d in ins if x>=t)
    i=int(t0*SR); n=min(len(a),len(v)-i); v[i:i+n]+=a[:n]
    for w,s,e in pw: pal.append([w,round(sh(s)+t0,3),round(sh(e)+t0,3),k])
    print(k,t0,"->",round(t0+len(a)/SR,2),"fala ate",round(sh(pw[-1][2])+t0,2))
sf.write("audio/voz_pl.wav",v,SR)
json.dump(pal,open("audio/palavras_pl.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
json.dump(CUTS,open("cortes_pl.json","w"))
