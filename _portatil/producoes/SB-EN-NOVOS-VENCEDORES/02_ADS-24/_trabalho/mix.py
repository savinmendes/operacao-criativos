# Mix EN: vozes limpas (receita chiado) por personagem, mesmo LUFS; trilha demucs remapeada por plano (atempo)
import sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
from mapa import ES, EN, O, TOTAL
OV=0.05
v=load("audio/velho.mp3"); a=load("audio/anjo.mp3")
vc,_=limpar_voz(v,palavras("audio/velho.alinhamento.json")); ac,_=limpar_voz(a,palavras("audio/anjo.alinhamento.json"))
vc=ganho_lufs(vc,-16.5); ac=ganho_lufs(ac,-16.5)    # iguala as duas vozes
N=int(round(TOTAL*SR)); voz=np.zeros((N,2),np.float32)
def put(x,t0):
    i=int(round(t0*SR)); m=min(len(x),N-i); voz[i:i+m]+=x[:m]
put(vc,OV); put(ac,O); sf.write("audio/voz_limpa.wav",voz,SR)
pw=palavras("audio/velho.alinhamento.json",OV)+palavras("audio/anjo.alinhamento.json",O)
mk,_=mascara_fala(voz,pw,pre=0.05,pos=0.08,rel_db=35,abs_db=-50,dil=0.02)
# trilha: cada trecho entre cortes vira atempo(ES->EN)
parts=[]; fl=[]
for k,(e0,e1,n0,n1) in enumerate(zip(ES[:-1],ES[1:],EN[:-1],EN[1:])):
    f=(e1-e0)/(n1-n0)
    fl.append(f"[0:a]atrim={e0}:{e1},asetpts=PTS-STARTPTS,atempo={f:.5f},apad,atrim=0:{n1-n0:.5f}[p{k}]")
fc=";".join(fl)+";"+"".join(f"[p{k}]" for k in range(len(fl)))+f"concat=n={len(fl)}:v=0:a=1[o]"
subprocess.run(["ffmpeg","-v","error","-y","-i","demucs/htdemucs/es_st/no_vocals.wav","-filter_complex",fc,"-map","[o]","-ar",str(SR),"audio/trilha_en_raw.wav"],check=True)
bed=load("audio/trilha_en_raw.wav")[:N]; b=np.zeros_like(voz); b[:len(bed)]=bed
b=limpar_trilha(b); voz=ganho_lufs(voz,-16.5); b=ganho_lufs(b,-32); b=dip_pausas(b,mk,3)
fa=int((TOTAL-1.5)*SR); b[fa:]*=np.linspace(1,0,len(b)-fa)[:,None]
mix=finalizar_mix(voz+b); sf.write("audio/mix_en.wav",mix,SR)
print("ok",len(mix)/SR,"LUFS",round(lufs(mix),2),"TP",round(true_peak_db(mix),2),"velho",round(lufs(vc),1),"anjo",round(lufs(ac),1))
