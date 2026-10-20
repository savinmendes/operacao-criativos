# -*- coding: utf-8 -*-
"""Audio final: narracao DE (ja limpa, -16,5 LUFS) + no_vocals retimed por secao (atempo), limpa (chiado.py), -32 LUFS,
dip 3 dB nas pausas, corte em T0, mix -16 LUFS / TP <= -1,5. Saida: audio/mix_final.wav (48 kHz estereo)."""
import sys, json, subprocess, numpy as np, soundfile as sf
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\SB-FR-NOVOS-VENCEDORES\_chiado")
from vslcomum import T, M, TL, SEC
from chiado import load, limpar_trilha, lufs, ganho_lufs, finalizar_mix, dip_pausas, true_peak_db, SR
P = json.load(open(M / "params.json"))
T0, NF = P["T0"], P["NF"]
A = M / "audio"; A.mkdir(exist_ok=True)
DUR = NF / 30.0
NV = str(T / "base" / "audio" / "no_vocals.wav")

# 1) trilha retimed (so secoes que tocam depois de T0)
partes = []
for s in SEC:
    if s["novo_fim"] <= T0 - 1: continue
    d = s["src_fim"] - s["src_ini"]; n = int(round((s["novo_fim"] - s["novo_ini"]) * SR))
    af = f"atrim={s['src_ini']}:{s['src_fim']},asetpts=PTS-STARTPTS,aresample={SR}"
    if abs(s["fator"] - 1) > 1e-4: af += f",atempo={1 / s['fator']:.6f}"
    x = load(NV, ch=2, af=af)
    x = x[:n] if len(x) >= n else np.vstack([x, np.zeros((n - len(x), 2), np.float32)])
    partes.append((s, x))
bed = []; prev = None
for s, x in partes:
    if prev is not None and abs(prev["src_fim"] - s["src_ini"]) > 0.05:  # salto no original (corte do Papa): micro-fades
        r = int(0.12 * SR); bed[-1][-r:] *= np.linspace(1, 0, r)[:, None]; x[:r] *= np.linspace(0, 1, r)[:, None]
    bed.append(x); prev = s
bed = np.vstack(bed)
ini = int(round((T0 - partes[0][0]["novo_ini"]) * SR))
bed = bed[ini:ini + int(round(DUR * SR))]
if len(bed) < int(round(DUR * SR)): bed = np.vstack([bed, np.zeros((int(round(DUR * SR)) - len(bed), 2), np.float32)])
print("trilha retimed", len(bed) / SR, flush=True)

# 2) limpar trilha em blocos de 120 s (2 s de sobreposicao, crossfade linear)
B, O = 120 * SR, 2 * SR
out = np.zeros_like(bed); wsum = np.zeros(len(bed), np.float32)
for a in range(0, len(bed), B):
    s0 = max(0, a - O); e0 = min(len(bed), a + B + O)
    y = limpar_trilha(bed[s0:e0])[:e0 - s0]
    w = np.ones(e0 - s0, np.float32)
    if s0 > 0: w[:2 * O] = np.linspace(0, 1, 2 * O)
    if e0 < len(bed): w[-2 * O:] = np.linspace(1, 0, 2 * O)
    out[s0:e0] += y * w[:, None]; wsum[s0:e0] += w
    print("limpa trilha", a // SR, flush=True)
bed = out / np.maximum(wsum, 1e-6)[:, None]
bed = ganho_lufs(bed, -32.0)

# 3) voz
v, sr = sf.read(str(T / "voz" / "narracao_de_completa.wav"), dtype="float32")
assert sr == SR
v = v[int(round(T0 * SR)):]
n = len(bed)
v = v[:n] if len(v) >= n else np.concatenate([v, np.zeros(n - len(v), np.float32)])
# mascara de fala (alinhamento)
mk = np.zeros(n, np.float32)
for w in json.load(open(T / "voz" / "alinhamento_de.json", encoding="utf-8"))["palavras"]:
    a = int((w["ini"] - T0 - 0.05) * SR); b = int((w["fim"] - T0 + 0.08) * SR)
    if b > 0 and a < n: mk[max(0, a):min(n, b)] = 1
bed = dip_pausas(bed, mk, 3)
# fade-in inicial 0,3 s (so trilha; a voz comeca em ~0,48 s) e fade-out final 1 s
r = int(0.3 * SR); bed[:r] *= np.linspace(0, 1, r)[:, None]
r = int(1.0 * SR); bed[-r:] *= np.linspace(1, 0, r)[:, None]
mix = bed + v[:, None]
mix = finalizar_mix(mix, alvo=-16.0, tp=-1.5)
sf.write(str(A / "mix_final.wav"), mix, SR, subtype="PCM_24")
sf.write(str(A / "trilha_limpa_32.wav"), bed, SR, subtype="PCM_24")
print("dur", len(mix) / SR, "LUFS", round(lufs(mix), 2), "TP", round(true_peak_db(mix), 2), "trilha LUFS", round(lufs(bed), 1))
