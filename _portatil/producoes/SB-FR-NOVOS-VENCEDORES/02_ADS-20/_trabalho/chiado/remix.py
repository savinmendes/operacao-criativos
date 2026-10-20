# v2 sem chiado do ADS-20: limpa gancho (Jesus) e corpo (Brian) separadamente, refaz a linha do tempo do voz_fr.py
# (mesmos cortes, assert contra tempos.json) e a trilha (demucs es_st) com a mesma janela/fade do mix_fr.py
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\02_ADS-20\_trabalho\chiado")
from chiado import *
from linha_voz import linha, fontes, W, C0
DIP = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
h1, h2, c = fontes()
A = W + r"\audio"
h1c, _ = limpar_voz(h1, palavras(A + r"\hook1_fr.alinhamento.json"))
h2c, _ = limpar_voz(h2, palavras(A + r"\hook2_fr.alinhamento.json"))
cc, _ = limpar_voz(c, palavras(A + r"\corpo_fr.alinhamento.json"))
voz, T = linha(h1c, h2c, cc); sf.write(W + r"\chiado\voz_limpa.wav", voz, SR)
# mascara de fala na linha do tempo final (para o dip da trilha)
pw = palavras(A + r"\hook1_fr.alinhamento.json", 0.08) + palavras(A + r"\hook2_fr.alinhamento.json", 2.45) + palavras(A + r"\corpo_fr_p.alinhamento.json", C0)
mk, _ = mascara_fala(voz, pw, pre=0.05, pos=0.08, rel_db=35, abs_db=-50, dil=0.02)
bed = load(r"C:/Users/PICHAU/Downloads/SB-EN-OFERTA-LIVE/07_ADS-20/_trabalho/demucs/htdemucs/es_st/no_vocals.wav")[:int(T * SR)]
bed = limpar_trilha(bed)
n = len(voz); b = np.zeros_like(voz); b[:min(n, len(bed))] = bed[:n]
voz = ganho_lufs(voz, -16.5); b = ganho_lufs(b, -32)          # v1: voz -17 (loudnorm dinamico) e trilha ~-32
b = dip_pausas(b, mk, DIP)
fa = int((T - 1.5) * SR); b[fa:] *= np.linspace(1, 0, len(b) - fa)[:, None]   # mesmo fade de 1,5 s
mix = finalizar_mix(voz + b)
sf.write(W + r"\chiado\mix_fr_v2.wav", mix, SR)
print("ok", len(mix) / SR, "T", T, "LUFS", round(lufs(mix), 2), "TP", round(true_peak_db(mix), 2), "fala%", round(mk.mean() * 100, 1))
# a v1 saiu 238 amostras (~5 ms) atrasada pelo alimiter sem compensacao de latencia; mantemos a sincronia da v1
D = 238; mix = np.concatenate([np.zeros((D, 2), np.float32), mix[:-D]])
sf.write(W + r"\chiado\mix_fr_v2.wav", mix, SR); print("deslocado +", D, "amostras (igual a v1)")
