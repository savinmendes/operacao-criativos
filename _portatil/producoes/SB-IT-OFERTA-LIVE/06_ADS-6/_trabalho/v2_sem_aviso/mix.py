# Receita RECEITA_LIMPAR_CHIADO: limpar_voz (gate >5k + silencio fora da fala + EQ) e finalizar_mix -16 LUFS (sem loudnorm dinamico). Sem trilha (o AD so tem voz).
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
v=load("audio/voz_emendada.wav"); pw=palavras("audio/narracao_it.alinhamento.json")
vz,mk=limpar_voz(v,pw); vz=ganho_lufs(vz,-16.5); mix=finalizar_mix(vz)
TOTAL=float(sys.argv[1]); n=int(round(TOTAL*SR)); mix=np.pad(mix,((0,max(0,n-len(mix))),(0,0)))[:n]
sf.write("audio/mix_v2.wav",mix,SR,subtype="FLOAT")
print("LUFS",round(lufs(mix),2),"TP",round(true_peak_db(mix),2),"metricas antes",metricas(v),"depois",metricas(mix))
