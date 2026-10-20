# Correção pedida em 20/10: o hook do PL_PF-7 (0–7,83 s) estava mudo.
# Coloca a trilha do corpo já no hook (o mesmo no_vocals, terminando exatamente onde a trilha do corpo começa),
# mais alta sem fala (-24 LUFS) e descendo até o nível do corpo no último 1 s. O corpo fica intacto.
import sys, numpy as np, soundfile as sf, subprocess
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"
HOOK = 7.8333; CORTE = 8.0667          # o corpo usa a trilha a partir de CORTE
mix = sf.read(T + r"\mix\mix_pf7.wav", always_2d=True)[0]
nv = load(T + r"\demucs\sep\htdemucs\PFMascLatam17\no_vocals.wav")
hb = limpar_trilha(nv[int(round((CORTE - HOOK) * SR)):int(round(CORTE * SR))])
hb = ganho_lufs(hb, -24.0)
n = len(hb); k = int(1.0 * SR)
env = np.ones(n); env[-k:] = np.linspace(1.0, 10 ** (-8 / 20), k)   # -24 -> ~-32 (nível do corpo)
env[:int(0.15 * SR)] *= np.linspace(0, 1, int(0.15 * SR))
H = int(round(HOOK * SR)); hb = (hb * env[:, None])[:H]
out = mix.copy(); out[:len(hb)] += hb
pk = np.abs(out).max()
if pk > 0.98: out *= 0.98 / pk
sf.write(T + r"\mix\mix_pf7_hook-trilha.wav", out, SR, subtype="PCM_24")
print("ok", round(len(out) / SR, 3), "pico", round(float(pk), 3), "LUFS", round(lufs(out), 1))
