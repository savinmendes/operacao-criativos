# Correção 20/10 (PL_PF-7 hook falado): voz Lily no hook (pausas encurtadas, início 0,15 s) + música nova (musica_pf7_nova.mp3).
# Hook: música a -31 LUFS sob a fala (sobe só nos 0,15 s antes da fala; nada depois, a fala vai até ~7,4 s); corpo idêntico ao pf7_musica_nova.py.
import sys, json, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"; P = T + r"\pf7hook"
HOOK = 7.8333; VOZ_INI = 0.15
mapa = json.load(open(T + r"\corpo\mapa.json")); D = mapa["D"]; FIM = mapa["fim"]
TOTAL = HOOK + FIM
mus = load(T + r"\mix\musica_pf7_nova.mp3")
n = int(round(TOTAL * SR)); mus = mus[:n]
if len(mus) < n: mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
H = int(round(HOOK * SR))
# voz do hook
vh = load(P + r"\hookpf7_lily_curta.wav"); pwh = palavras(P + r"\hookpf7_lily_curta.alinhamento.json")
vh, mkh = limpar_voz(vh, pwh); vh = ganho_lufs(vh, -16.5)
# voz do corpo (igual)
vc = load(T + r"\audio\corpo_vera.mp3"); vc, mkc = limpar_voz(vc, palavras(T + r"\audio\corpo_vera.alinhamento.json")); vc = ganho_lufs(vc, -16.5)
hook_m = ganho_lufs(mus[:H].copy(), -31.0)
hook_m[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
corpo_m = ganho_lufs(mus[H:].copy(), -32.0)
mk = np.zeros(len(corpo_m), bool); n0 = int(round(D * SR)); mm = mkc[:len(corpo_m) - n0]; mk[n0:n0 + len(mm)] = mm
corpo_m = dip_pausas(corpo_m, mk, 3)
corpo = corpo_m.copy(); vv = vc[:len(corpo) - n0]; corpo[n0:n0 + len(vv)] += vv
k2 = int(0.6 * SR); corpo[-k2:] *= np.linspace(1, 0, k2)[:, None]
hook = hook_m.copy(); i0 = int(round(VOZ_INI * SR)); v = vh[:H - i0]; hook[i0:i0 + len(v)] += v
mix = finalizar_mix(np.concatenate([hook, corpo]))
sf.write(P + r"\mix_pf7_hook-falado.wav", mix, SR, subtype="PCM_24")
print("ok", round(len(mix) / SR, 3), "LUFS", round(lufs(mix), 1), "musica hook", round(lufs(hook_m), 1), "voz hook", round(lufs(vh), 1))
