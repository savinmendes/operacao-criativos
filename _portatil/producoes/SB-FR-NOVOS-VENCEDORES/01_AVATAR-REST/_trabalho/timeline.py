# Linha do tempo FR: cenas (fonte -> saída, com fator de alongamento) + falas FR posicionadas -> timeline.json, audio/voz_fr.wav, palavras_fr.json
import json, subprocess, numpy as np, soundfile as sf
from palavras import palavras
SR=48000; TOTAL=62.3
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
# (arquivo, ini_rel, fim_rel, inicio_abs_da_1a_palavra, personagem)
FALAS=[("hook",0.04,4.16,0.09,"comerciante"),("hook",4.76,7.70,5.20,"comerciante"),
 ("temo",0.04,17.83,10.84,"comerciante"),
 ("padre",0.08,3.47,29.10,"padre"),("padre",4.08,5.26,33.00,"padre"),("padre",5.77,8.89,34.70,"padre"),
 ("padre",9.50,15.15,38.25,"padre"),("padre",15.76,18.55,44.25,"padre"),("padre",19.25,22.85,47.60,"padre"),
 ("padre",23.66,28.22,51.60,"padre"),("padre",28.92,33.99,56.60,"padre")]
# (nome, out_ini, out_fim, src_ini, src_dur, lipsync)
CENAS=[("S0_ajoelhado",0,4.9,0,4.9,None),("S1_ajoelhado2",4.9,8.7,6.3,3.8,None),("S2_rest_cheio",8.7,10.7,11.9,2.0,None),
 ("S3_selfieA1",10.7,14.33,14.5,3.63,"comerciante"),("S3_selfieA2",14.33,17.15,18.133,2.817,"comerciante"),
 ("S4_mulher_cel",17.15,19.1,22.68,1.95,None),("S5_selfieB1",19.1,22.85,24.633,3.75,"comerciante"),
 ("S5_selfieB2",22.85,25.1,29.17,2.25,"comerciante"),("S6_rest_cheio2",25.1,29.0,31.6,3.9,None),
 ("S7_padre1",29.0,32.75,37.1,3.6,"padre"),("S8_multidao",32.75,34.6,40.7,1.85,None),("S9_jesus_bau",34.6,38.05,42.7,3.2,None),
 ("S10_padre2",38.05,40.9,45.9,2.85,"padre"),("S11_casa",40.9,44.9,49.1,3.45,None),("S12_padre3",44.9,47.1,52.567,2.2,"padre"),
 ("S13_chave",47.1,49.85,54.767,2.75,None),("S14_porta",49.85,51.4,59.8,1.55,None),("S15_padre4",51.4,54.36,61.833,2.7,"padre"),
 ("S16_monge",54.36,56.35,64.533,1.8,None),("S17_padre5",56.35,58.75,66.333,2.4,"padre"),("S18_altar",58.75,TOTAL,69.133,2.533,None)]
FPS=30
cen=[]
for nm,a,b,s,d,ls in CENAS:
    st=(b-a)/d; mx=1.25 if not ls else 1.10
    frz=0.0
    if st>mx: frz=(b-a)-d*mx; st=mx
    cen.append(dict(nome=nm,out_ini=a,out_fim=b,src_ini=s,src_dur=d,fator=round(st,4),congela=round(frz,3),lipsync=ls))
    print(f"{nm:16s} out {a:6.2f}-{b:6.2f} ({b-a:4.2f}) src {s:6.2f}+{d:4.2f} fator {st:.3f} congela {frz:.2f} {ls or ''}")
voz=np.zeros((int(TOTAL*SR),2),np.float32); W=[]
cache={}
for arq,i0,i1,ab,per in FALAS:
    if arq not in cache: cache[arq]=(load(f"audio/{arq}_fr.mp3"),palavras(f"audio/{arq}_fr.alinhamento.json"))
    au,pw=cache[arq]; off=ab-i0
    a0=max(0,i0-0.06); a1=i1+0.15
    seg=au[int(a0*SR):int(a1*SR)].copy(); n=len(seg); f=int(0.01*SR); seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    p=int((a0+off)*SR); voz[p:p+n]+=seg[:len(voz)-p]
    for w,s,e in pw:
        if s>=i0-0.01 and e<=i1+0.01: W.append([w,round(s+off,3),round(e+off,3),per])
sf.write("audio/voz_fr.wav",voz,SR)
json.dump(W,open("palavras_fr.json","w",encoding="utf-8"),ensure_ascii=False)
json.dump(dict(total=TOTAL,fps=FPS,cenas=cen),open("timeline.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
# checa palavra atravessando corte
for c in cen:
    for w,s,e,p in W:
        if s<c["out_fim"]<e: print("corte no meio de",w,c["nome"],c["out_fim"])
print(len(W),"palavras")
