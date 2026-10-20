# Correção 20/10 (PL_PF-7): trilha nova limpa (ElevenLabs Music) no lugar da trilha separada pelo demucs (que chiava).
# Hook (sem fala) com a música presente; corpo com a mesma música a -32 LUFS sob a voz, com dip nas pausas.
# Rodar a partir de kit-edicao-criativos (usa tts_elevenlabs.chave()).
import sys, json, numpy as np, soundfile as sf, requests, subprocess
from pathlib import Path
sys.path.insert(0, "ferramentas"); import tts_elevenlabs as T11
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from chiado import *
T = r"C:\Users\PICHAU\Downloads\PERFUMES-PL\_trabalho"
M = Path(T + r"\mix\musica_pf7_nova.mp3")
HOOK = 7.8333
mapa = json.load(open(T + r"\corpo\mapa.json")); D = mapa["D"]; FIM = mapa["fim"]
TOTAL = HOOK + FIM
if not M.exists():
    r = requests.post("https://api.elevenlabs.io/v1/music", headers={"xi-api-key": T11.chave(), "Content-Type": "application/json"},
                      json={"prompt": "Instrumental only, no vocals. Modern luxury men's perfume commercial: smooth seductive deep house / R&B groove, "
                                      "warm sub bass, soft claps, silky synth pads, confident and sensual, clean polished mix, steady energy from the first second, no build-up silence.",
                            "music_length_ms": int((TOTAL + 1.5) * 1000)}, timeout=600)
    if r.status_code != 200: raise SystemExit(f"music {r.status_code}: {r.text[:300]}")
    M.write_bytes(r.content); print("musica gerada", len(r.content))
mus = load(str(M))
n = int(round(TOTAL * SR)); mus = mus[:n]
if len(mus) < n: mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
H = int(round(HOOK * SR))
# voz do corpo (mesma limpeza do audio_mix.py)
vc = load(T + r"\audio\corpo_vera.mp3"); vc, mkc = limpar_voz(vc, palavras(T + r"\audio\corpo_vera.alinhamento.json")); vc = ganho_lufs(vc, -16.5)
hook = ganho_lufs(mus[:H].copy(), -21.0)
corpo_m = ganho_lufs(mus[H:].copy(), -32.0)
# rampa de 1 s no fim do hook descendo ao nível do corpo
g = 10 ** ((-32.0 - (-21.0)) / 20); k = int(1.0 * SR)
hook[-k:] *= np.linspace(1.0, g * (np.sqrt(np.mean(mus[H:H+SR]**2)) / (np.sqrt(np.mean(mus[H-SR:H]**2)) + 1e-9)) ** 0 , k)[:, None]
hook[:int(0.05 * SR)] *= np.linspace(0, 1, int(0.05 * SR))[:, None]
mk = np.zeros(len(corpo_m), bool); n0 = int(round(D * SR)); mm = mkc[:len(corpo_m) - n0]; mk[n0:n0 + len(mm)] = mm
corpo_m = dip_pausas(corpo_m, mk, 3)
corpo = corpo_m.copy(); vv = vc[:len(corpo) - n0]; corpo[n0:n0 + len(vv)] += vv
k2 = int(0.6 * SR); corpo[-k2:] *= np.linspace(1, 0, k2)[:, None]
mix = finalizar_mix(np.concatenate([hook, corpo]))
sf.write(T + r"\mix\mix_pf7_musica-nova.wav", mix, SR, subtype="PCM_24")
print("ok", round(len(mix) / SR, 3), "LUFS", round(lufs(mix), 1))
