# v2: audio do corpo = narracao_es.wav (x0,7443) + fundo do demucs no_vocals (x1,0515), atraso de 239 amostras (48 kHz),
# cortado 0,7 s depois da ultima fala (119,77 s), fade de 0,3 s. Ganhos e atraso medidos no audio_corpo.wav da v1
# (minimos quadrados, residuo 0,0002). Uso: python _audio/montar_corpo_audio.py narr.wav saida.wav
import sys
import numpy as np, soundfile as sf, subprocess, tempfile, os
narr, saida = sys.argv[1], sys.argv[2]
SR, L, FIM, FADE = 48000, 239, 119.77, 0.3
tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg","-v","error","-y","-i",narr,"-ar","48000","-ac","1",os.path.join(tmp,"n.wav")],check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i","_audio/demucs/htdemucs/orig/no_vocals.wav","-ar","48000","-ac","2",os.path.join(tmp,"f.wav")],check=True)
n,_ = sf.read(os.path.join(tmp,"n.wav")); f,_ = sf.read(os.path.join(tmp,"f.wav"))
m = int(round(FIM*SR))
n = np.concatenate([np.zeros(L), n])[:m]; f = np.concatenate([np.zeros((L,2)), f])[:m]
o = 0.74425*n[:,None] + 1.0515*f
k = int(FADE*SR); o[-k:] *= np.linspace(1,0,k)[:,None]
sf.write(saida, np.clip(o,-1,1), SR, subtype="PCM_16")
print("ok", saida, len(o)/SR)
