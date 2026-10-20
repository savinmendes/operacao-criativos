# v2 sem chiado: limpa voz (voz_fr.wav, ja na linha do tempo) e trilha demucs, refaz o mix igual ao mix_fr.py
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
W = r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\03_ADS-13.13F-REZA-MUJER\_trabalho"
DIP = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0     # dB a mais de reducao da trilha nas pausas da voz
CJ = json.load(open(W + r"\cortes_fr.json")); C, ES = CJ["C"], CJ["ES"]
voz = load(W + r"\audio\voz_fr.wav"); pw = palavras(W + r"\audio\voz_fr_p.alinhamento.json")
vz, mk = limpar_voz(voz, pw); sf.write(W + r"\chiado\voz_limpa.wav", vz, SR)
bed = load(W + r"\demucs\htdemucs\src13_audio\no_vocals.wav"); bed = limpar_trilha(bed); sf.write(W + r"\chiado\no_vocals_limpa.wav", bed, SR)
# mesma montagem de trilha do mix_fr.py
out = np.zeros_like(vz); fade = int(0.05 * SR)
for k in range(6):
    n = int((C[k + 1] - C[k]) * SR); a = int(ES[k] * SR)
    seg = np.zeros((n + fade, 2), np.float32); src = bed[a:a + n + fade]; seg[:len(src)] = src
    env = np.ones(n + fade, np.float32); env[-fade:] = np.linspace(1, 0, fade)
    if k > 0: env[:fade] = np.linspace(0, 1, fade)
    s = int(C[k] * SR); e = min(len(out), s + n + fade); out[s:e] += (seg * env[:, None])[:e - s]
vz = ganho_lufs(vz, -16); out = ganho_lufs(out, -32)
out = dip_pausas(out, mk, DIP)
fa = len(out) - int(0.6 * SR); out[fa:] *= np.linspace(1, 0, len(out) - fa)[:, None]
mix = finalizar_mix(vz + out)
sf.write(W + r"\chiado\mix_fr_v2.wav", mix, SR)
print("ok", len(mix) / SR, "LUFS", round(lufs(mix), 2), "TP", round(true_peak_db(mix), 2), "fala%", round(mk.mean() * 100, 1))
