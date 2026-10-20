# reconstroi o mix v1 (cadeia antiga) e compara com o audio do mp4 atual
import sys, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho\chiado")
from linha_voz import *
v, T = linha(*fontes()); sf.write("chiado/voz_v1.wav", v, SR)
subprocess.run(["ffmpeg","-v","error","-y","-i","C:/Users/PICHAU/Downloads/SB-EN-OFERTA-LIVE/07_ADS-20/_trabalho/demucs/htdemucs/es_st/no_vocals.wav","-t",str(T),"-af",f"afade=t=out:st={T-1.5}:d=1.5,volume=14.200000000000003dB,aresample=48000","-ac","2","chiado/trilha_v1.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","chiado/voz_v1.wav","-af","loudnorm=I=-17:TP=-2:LRA=11,aresample=48000","-ac","2","chiado/voz_n_v1.wav"],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","chiado/voz_n_v1.wav","-i","chiado/trilha_v1.wav","-filter_complex","[0][1]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95","-ar","48000","chiado/mix_v1.wav"],check=True)
a = load("chiado/mix_v1.wav"); b = load("../SB-FR-ADS-20.mp4")
n = min(len(a), len(b)); a = a[:n, 0]; b = b[:n, 0]
# alinhamento fino (atraso do aac)
best = max(range(-3000, 3001, 1), key=lambda d: np.dot(a[48000*10:48000*20], b[48000*10+d:48000*20+d]))
bb = b[max(0,best):]; aa = a[:len(bb)]
print("len mix", len(a)/SR, "mp4", len(b)/SR, "atraso", best, "corr", np.corrcoef(aa[:len(bb)], bb[:len(aa)])[0,1])
