# Áudio EN pela RECEITA_LIMPAR_CHIADO.md (_chiado/chiado.py): limpar_voz em cada fonte (hook/temo/padre, com o próprio
# alinhamento; pré-normalizadas a -18 LUFS) -> montagem na timeline EN (mesmas FALAS do timeline_en.py; jump cuts já embutidos)
# -> ganho estático igual por personagem (-16,5 LUFS) -> trilha demucs limpar_trilha (+afftdn) -32 LUFS + dip 3 dB -> finalizar_mix -16.
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import filtro, load, palavras, limpar_voz, limpar_trilha, ganho_lufs, dip_pausas, finalizar_mix, lufs, true_peak_db, SR
T=json.load(open("timeline.json",encoding="utf-8")); TOTAL=T["total"]; NT=int(round(TOTAL*SR))
L={}
for nm in ["hook","temo","padre"]:
    x=ganho_lufs(load(f"audio/{nm}_en.mp3"),-18); L[nm]=limpar_voz(x,palavras(f"audio/{nm}_en.alinhamento.json"))
V={k:np.zeros((NT,2),np.float32) for k in ("comerciante","padre")}; MK=np.zeros(NT,np.float32)
for arq,i0,i1,ab,per in T["falas"]:
    au,mk=L[arq]; off=ab-i0; a0=max(0,i0-0.03); a1=i1+0.03
    seg=au[int(a0*SR):int(a1*SR)].copy(); m=mk[int(a0*SR):int(a1*SR)]; n=len(seg); f=int(0.01*SR)
    seg[:f]*=np.linspace(0,1,f)[:,None]; seg[-f:]*=np.linspace(1,0,f)[:,None]
    p=int(round((a0+off)*SR)); V[per][p:p+n]+=seg[:NT-p]; MK[p:p+n]=np.maximum(MK[p:p+n],m[:NT-p])
print("LUFS antes: comerciante %.1f padre %.1f"%(lufs(V["comerciante"]),lufs(V["padre"])))
voz=ganho_lufs(V["comerciante"],-16.5)+ganho_lufs(V["padre"],-16.5)
bed=load(r"demucs/htdemucs/es/no_vocals.wav")[:NT]; bed=filtro(limpar_trilha(bed),"afftdn=nr=12:nf=-55:tn=1")
fi=int(0.05*SR); fo=int(0.8*SR); bed[:fi]*=np.linspace(0,1,fi)[:,None]; bed[-fo:]*=np.linspace(1,0,fo)[:,None]
bed=dip_pausas(ganho_lufs(bed,-32),MK,3)
mix=np.zeros((NT,2),np.float32); mix[:len(voz)]+=voz; mix[:len(bed)]+=bed
mix=finalizar_mix(mix)
print("mix LUFS %.1f TP %.1f dBTP dur %.3f"%(lufs(mix),true_peak_db(mix),len(mix)/SR))
sf.write("audio/mix_en.wav",mix,SR,subtype="FLOAT"); sf.write("audio/voz_limpa_en.wav",voz,SR,subtype="FLOAT")
