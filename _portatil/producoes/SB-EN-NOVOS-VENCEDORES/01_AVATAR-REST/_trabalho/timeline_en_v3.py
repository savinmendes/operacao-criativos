# Linha do tempo EN: cenas (fonte -> saída) + falas EN posicionadas -> timeline.json, audio/voz_en.wav, palavras_en.json, padre/hg_trechos.json
# Jump cuts já embutidos: cada frase do depoimento entra numa cena/tomada própria, sem as pausas longas.
import json, subprocess, re, numpy as np, soundfile as sf
from palavras import palavras
SR=48000; TOTAL=56.70; FPS=30
def load(p):
    raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-ac","2","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout
    return np.frombuffer(raw,np.float32).reshape(-1,2).copy()
# (arquivo, ini_rel, fim_rel, inicio_abs_de_ini_rel, personagem)
FALAS=[("hook",0.06,5.75,0.03,"comerciante"),("hook",6.45,10.78,6.16,"comerciante"),
 ("temo",0.03,2.10,10.80,"comerciante"),("temo",2.46,4.43,13.09,"comerciante"),("temo",5.16,6.81,15.31,"comerciante"),
 ("temo",7.05,10.05,17.18,"comerciante"),("temo",10.66,12.44,20.41,"comerciante"),("temo",12.80,15.61,22.51,"comerciante"),
 ("padre",0.02,3.13,25.91,"padre"),("padre",3.75,5.29,29.54,"padre"),("padre",5.65,8.82,31.40,"padre"),
 ("padre",9.55,15.16,35.09,"padre"),("padre",15.89,18.22,41.22,"padre"),("padre",18.95,22.15,44.07,"padre"),
 ("padre",22.76,26.97,47.74,"padre"),("padre",27.41,31.10,52.37,"padre")]
# (nome, out_ini, out_fim, src_ini, src_dur, lipsync)   src_dur = tamanho útil da tomada na fonte
CENAS=[("S0_ajoelhado",0,4.9,0,4.9,None),("S1_ajoelhado2",4.9,8.7,6.3,3.8,None),("S2_rest_cheio",8.7,10.7,11.9,2.0,None),
 ("S3_selfieA1",10.7,12.98,18.9,2.28,"comerciante"),("S3_selfieA2",12.98,15.20,14.5,2.22,"comerciante"),
 ("S4_mulher_cel",15.20,17.07,22.72,1.87,None),("S5_selfieB1",17.07,20.30,24.7,3.23,"comerciante"),
 ("S5_selfieB2",20.30,22.35,29.5,2.05,"comerciante"),("S6_rest_cheio2",22.35,25.88,31.65,3.6,None),
 ("S7_padre1",25.88,29.15,37.1,3.27,"padre"),("S8_multidao",29.15,31.40,40.7,1.95,None),("S9_jesus_bau",31.40,35.06,42.7,3.15,None),
 ("S10_padre2",35.06,37.49,45.9,3.2,"padre"),("S11_casa",37.49,41.19,49.1,3.45,None),("S12_padre3",41.19,43.65,52.567,2.15,"padre"),
 ("S13_chave",43.65,46.40,54.767,2.75,None),("S14_porta",46.40,47.71,59.8,1.95,None),("S15_padre4",47.71,50.18,61.833,2.65,"padre"),
 ("S16_monge",50.18,52.34,64.533,1.75,None),("S17_padre5",52.34,53.98,66.333,2.6,"padre"),("S18_altar",53.98,TOTAL,69.133,2.5,None)]
cen=[]
for nm,a,b,s,d,ls in CENAS:
    st=(b-a)/d; mx=1.25 if not ls else 1.10
    if ls=="padre": st=1.0; d=min(d,b-a)          # padre é refeito do zero (HeyGen); a base só serve para as setas
    elif st<1: st=1.0; d=b-a
    frz=0.0
    if st>mx: frz=(b-a)-d*mx; st=mx
    cen.append(dict(nome=nm,out_ini=a,out_fim=b,src_ini=s,src_dur=round(d,4),fator=round(st,4),congela=round(frz,3),lipsync=ls))
    print(f"{nm:16s} out {a:6.2f}-{b:6.2f} ({b-a:4.2f}) src {s:6.2f}+{d:4.2f} fator {st:.3f} congela {frz:.2f} {ls or ''}")
voz=np.zeros((int(TOTAL*SR),2),np.float32); W=[]; cache={}
for arq,i0,i1,ab,per in FALAS:
    if arq not in cache: cache[arq]=(load(f"audio/{arq}_en.mp3"),[w for w in palavras(f"audio/{arq}_en.alinhamento.json") if re.search(r"\w",w[0])])
    au,pw=cache[arq]; off=ab-i0
    a0=max(0,i0-0.03); a1=i1+0.03
    seg=au[int(a0*SR):int(a1*SR)].copy(); n=len(seg); f=int(0.01*SR); seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    p=int((a0+off)*SR); voz[p:p+n]+=seg[:len(voz)-p]
    for w,s,e in pw:
        if s>=i0-0.01 and e<=i1+0.01: W.append([w,round(s+off,3),round(e+off,3),per])
sf.write("audio/voz_en.wav",voz,SR)
json.dump(W,open("palavras_en.json","w",encoding="utf-8"),ensure_ascii=False)
json.dump(dict(total=TOTAL,fps=FPS,cenas=cen,falas=FALAS),open("timeline.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
for c in cen:
    for w,s,e,p in W:
        if s<c["out_fim"]<e or s<c["out_ini"]<e: print("CORTE NO MEIO de",w,c["nome"],c["out_ini"],c["out_fim"])
    ws=[w for w in W if c["out_ini"]<=w[1]<c["out_fim"]]
    print(f"  {c['nome']:16s}", " ".join(w[0] for w in ws)[:110])
print(len(W),"palavras; fim fala",max(w[2] for w in W))
