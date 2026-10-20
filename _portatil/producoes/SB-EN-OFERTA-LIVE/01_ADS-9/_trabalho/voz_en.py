# Monta a voz EN na linha do tempo do FR: cada segmento começa no início da frase FR correspondente
import json, subprocess, numpy as np, soundfile as sf
from palavras import palavras
SR = 48000; TOTAL = 102.866
S = json.load(open("segmentos_en.json", encoding="utf-8"))
def load(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
v = np.zeros((int(TOTAL * SR), 2), np.float32); pal = []; fins = []
for i, (a, b, t) in enumerate(S):
    x = load(f"audio/s{i:02d}.mp3"); pw = palavras(f"audio/s{i:02d}.alinhamento.json", a)
    fim = pw[-1][2] - a + 0.12; x = x[:int(fim * SR)]
    f = int(0.02 * SR); x[-f:] *= np.linspace(1, 0, f)[:, None]
    k = int(a * SR); v[k:k + len(x)] += x
    pal += pw; fins.append(round(a + fim, 2))
    if i + 1 < len(S): assert a + fim < S[i + 1][0] - 0.1, (i, a + fim, S[i + 1][0])
sf.write("audio/voz_en.wav", v, SR)
json.dump(pal, open("audio/palavras_en.json", "w", encoding="utf-8"), ensure_ascii=False)
print("fins", fins)
