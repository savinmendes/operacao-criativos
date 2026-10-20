# -*- coding: utf-8 -*-
"""Lote B: tira o "hoy" do b12 sem mudar o tempo. Troca "el que más aprieta tu vida hoy." (86,52-88,36 s) por um TTS novo
"el que más aprieta tu vida." (tts/b12h.mp3, mesma voz), começando no mesmo ponto. O resto da narração fica idêntico.
Lê/escreve ../narracao_es.wav e ../narracao_es.alinhamento.json e atualiza tempos_reais.json (b12)."""
import json, subprocess, numpy as np, soundfile as sf
from pathlib import Path
A = Path(__file__).resolve().parent; AD = A.parent
src = AD / "_antes_loteB" / "narracao_es.wav"; srcal = AD / "_antes_loteB" / "narracao_es.alinhamento.json"
x, sr = sf.read(src); x = x.copy()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(A/"tts/b12h.mp3"),"-ar",str(sr),"-ac","1",str(A/"tts/b12h.wav")],check=True)
y, _ = sf.read(A / "tts/b12h.wav")
al = json.load(open(srcal, encoding="utf-8")); C, S, E = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
txt = "".join(C); i0 = txt.find("el que más aprieta tu vida hoy."); i1 = i0 + len("el que más aprieta tu vida hoy.")
t0, t1 = S[i0], E[i1 - 1]
nl = json.load(open(A / "tts/b12h.alinhamento.json", encoding="utf-8"))
nc, ns, ne = nl["characters"], nl["character_start_times_seconds"], nl["character_end_times_seconds"]
k = [j for j in range(len(nc)) if not nc[j].isspace()]; k0, k1 = k[0], k[-1]
off = t0 - ns[k0]
rms = lambda v: np.sqrt(np.mean(v[np.abs(v) > 0.01] ** 2))
g = rms(x[int(t0*sr):int(t1*sr)]) / rms(y)
a, b = int((t0 - 0.03) * sr), int((t1 + 0.20) * sr)   # apaga a frase antiga (o b13 começa em 88,78 s)
f = int(0.01 * sr); x[a-f:a] *= np.linspace(1, 0, f); x[a:b] = 0; x[b:b+f] *= np.linspace(0, 1, f)
p = int(round(off * sr)); x[p:p+len(y)] += y * g
sf.write(AD / "narracao_es.wav", np.clip(x, -1, 1), sr, subtype="PCM_16")
C2 = C[:i0] + nc[k0:k1+1] + C[i1:]
S2 = S[:i0] + [round(ns[j] + off, 3) for j in range(k0, k1+1)] + S[i1:]
E2 = E[:i0] + [round(ne[j] + off, 3) for j in range(k0, k1+1)] + E[i1:]
(AD / "narracao_es.alinhamento.json").write_text(json.dumps({"characters": C2, "character_start_times_seconds": S2, "character_end_times_seconds": E2}, ensure_ascii=False), encoding="utf-8")
T = json.load(open(AD / "_antes_loteB" / "tempos_reais.json", encoding="utf-8"))
for t in T:
    if t["id"] == "b12": t["texto"] = t["texto"].replace("tu vida hoy.", "tu vida."); t["fim"] = round(ne[k1] + off, 2)
json.dump(T, open(A / "tempos_reais.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"frase antiga {t0:.3f}-{t1:.3f}; nova {ns[k0]+off:.3f}-{ne[k1]+off:.3f}; ganho {g:.2f}")
