# Áudio v3 pela RECEITA_LIMPAR_CHIADO.md (_chiado/chiado.py): limpar_voz em cada fonte (hook/temo/padre, cada uma com o
# próprio alinhamento) -> montagem na timeline FR (igual timeline.py) -> ganho estático por personagem (-16,5 LUFS)
#    (padre vem do TTS a -43 LUFS: cada fonte é pré-normalizada a -18 LUFS antes da limpeza, que usa limiares absolutos)
# -> jump cuts (amostras removidas, igual final.sh) -> trilha limpar_trilha -32 LUFS + dip 3 dB nas pausas -> finalizar_mix -16.
import sys, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import filtro, load, palavras, limpar_voz, limpar_trilha, ganho_lufs, dip_pausas, finalizar_mix, lufs, true_peak_db, SR
TOTAL=62.3; NTOT=int(TOTAL*SR)
L={}
for nm in ["hook","temo","padre"]:
    x=ganho_lufs(load(f"../audio/{nm}_fr.mp3"),-18); L[nm]=limpar_voz(x,palavras(f"../audio/{nm}_fr.alinhamento.json"))
FALAS=[("hook",0.04,4.16,0.09,"c"),("hook",4.76,7.70,5.20,"c"),("temo",0.04,17.83,10.84,"c"),
 ("padre",0.08,3.47,29.10,"p"),("padre",4.08,5.26,33.00,"p"),("padre",5.77,8.89,34.70,"p"),
 ("padre",9.50,15.15,38.25,"p"),("padre",15.76,18.55,44.25,"p"),("padre",19.25,22.85,47.60,"p"),
 ("padre",23.66,28.22,51.60,"p"),("padre",28.92,33.99,56.60,"p")]
V={k:np.zeros((NTOT,2),np.float32) for k in "cp"}; MK=np.zeros(NTOT,np.float32)
for arq,i0,i1,ab,per in FALAS:
    au,mk=L[arq]; off=ab-i0; a0=max(0,i0-0.06); a1=i1+0.15
    seg=au[int(a0*SR):int(a1*SR)].copy(); m=mk[int(a0*SR):int(a1*SR)]; n=len(seg); f=int(0.01*SR)
    seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    p=int((a0+off)*SR); V[per][p:p+n]+=seg[:NTOT-p]; MK[p:p+n]=np.maximum(MK[p:p+n],m[:NTOT-p])
voz=ganho_lufs(V["c"],-16.5)+ganho_lufs(V["p"],-16.5)
print("LUFS com %.1f padre %.1f"%(lufs(V["c"]),lufs(V["p"])))
# jump cuts: quadros 386-401 e 465-478 saem
def corta(x):
    keep=np.ones(len(x),bool); x=x.copy(); f=int(0.008*SR)
    for a,b in [(386,402),(465,479)]:
        i,j=int(round(a/30*SR)),int(round(b/30*SR)); keep[i:j]=False
        if x.ndim>1:   # rampas de 8 ms dos dois lados do corte (sem clique na emenda)
            x[i-f:i]*=np.linspace(1,0,f)[:,None]; x[j:j+f]*=np.linspace(0,1,f)[:,None]
    return x[keep]
TOT=round(62.3-30/30,3); NT=int(round(TOT*SR))
voz=corta(voz)[:NT]; MK=corta(MK)[:NT]
bed=load("../demucs/htdemucs/es/no_vocals.wav")[:NT]; bed=filtro(limpar_trilha(bed),"afftdn=nr=12:nf=-55:tn=1")   # + afftdn: tapete -10 dB nas pausas (medido)
fi=int(0.05*SR); fo=int(0.8*SR); bed[:fi]*=np.linspace(0,1,fi)[:,None]; bed[-fo:]*=np.linspace(1,0,fo)[:,None]
bed=dip_pausas(ganho_lufs(bed,-32),MK,3)
mix=np.zeros((NT,2),np.float32); mix[:len(voz)]+=voz; mix[:len(bed)]+=bed
mix=finalizar_mix(mix)
print("mix LUFS %.1f TP %.1f dBTP dur %.3f"%(lufs(mix),true_peak_db(mix),len(mix)/SR))
sf.write("mix_v3.wav",mix,SR,subtype="FLOAT"); sf.write("voz_v3.wav",voz,SR,subtype="FLOAT")
