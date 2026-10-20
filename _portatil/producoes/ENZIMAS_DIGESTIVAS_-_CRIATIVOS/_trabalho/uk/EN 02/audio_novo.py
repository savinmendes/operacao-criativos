# -*- coding: utf-8 -*-
"""Monta a trilha nova: fora dos trechos = audio original intocado; dentro = fundo demucs (no_vocals) + voz clonada
(ganho igualado em LUFS ao trecho original). Crossfade de 30 ms nas emendas (que caem em pausa).
Gera audio_uk.wav, voz_A.mp3 / voz_B.mp3 (so a voz nova, alinhada ao trecho, para o HeyGen) e orig_A/B.wav."""
import subprocess, numpy as np, soundfile as sf, json
SR = 44100
def load(p, extra=()):
    r = subprocess.run(["ffmpeg","-v","error","-i",p,*extra,"-ar",str(SR),"-ac","2","-f","f32le","-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).copy()
orig = load("orig.wav"); bg = load("demucs/htdemucs/orig/no_vocals.wav")
n = len(orig); bg = np.pad(bg, ((0, max(0, n - len(bg))), (0, 0)))[:n]
# trechos: janela [t0,t1] em s, tts, inicio do arquivo tts na linha do tempo, filtro, ganho dB
SEG = json.load(open("trechos.json"))
out = orig.copy(); xf = int(0.03 * SR)
for s in SEG:
    v = load(s["tts"], ["-af", s.get("af", "anull")]) * (10 ** (s["ganho_db"] / 20))
    a, b = int(s["t0"] * SR), min(n, int(s["t1"] * SR)); p0 = int(s["pos"] * SR)
    voz = np.zeros_like(orig); e = min(n, p0 + len(v)); voz[p0:e] = v[:e - p0]
    novo = bg + voz
    w = np.ones(n, np.float32) * 0; w[a:b] = 1
    w[a:a + xf] = np.linspace(0, 1, xf)
    if b < n: w[b - xf:b] = np.linspace(1, 0, xf)
    out = out * (1 - w[:, None]) + novo * w[:, None]
    sf.write(f"voz_{s['nome']}.wav", voz[a:b], SR)
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"voz_{s['nome']}.wav","-ac","1","-c:a","libmp3lame","-b:a","192k",f"voz_{s['nome']}.mp3"], check=True)
    sf.write(f"orig_{s['nome']}.wav", orig[a:b], SR)
    print(s["nome"], "voz termina em", round(e / SR, 2), "janela", s["t0"], s["t1"])
sf.write("audio_uk.wav", np.clip(out, -1, 1), SR, subtype="PCM_16")
print("ok", n / SR)
