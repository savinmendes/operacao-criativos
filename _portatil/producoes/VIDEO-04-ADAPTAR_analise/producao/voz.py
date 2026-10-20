# -*- coding: utf-8 -*-
"""Linha do tempo da voz: junta L01..L13 com pausas curtas; grava voz.wav, palavras.json (tempo global) e as partes p/ HeyGen (A: L1-L7, B: L8-L13)."""
import json, re, numpy as np, soundfile as sf, librosa, subprocess
from pathlib import Path
P = Path(__file__).resolve().parent; TT = P / "tts"; SR = 44100
GAP = {2: .22, 3: .25, 4: .30, 5: .30, 6: .28, 7: .15, 8: .45, 9: .30, 10: .30, 11: .28, 12: .28, 13: .25}   # pausa ANTES da linha
PRE, POS = 0.25, 0.40
def palavras(al, off):
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]; out = []; w = ""; ws = None
    for c, a, b in zip(ch, s, e):
        if c.isspace():
            if w: out.append(dict(w=w, ini=ws + off, fim=we + off)); w = ""
        else:
            if not w: ws = a
            w += c; we = b
    if w: out.append(dict(w=w, ini=ws + off, fim=we + off))
    return out
voz = []; t = 0.0; lin = []; pal = []
for i in range(1, 14):
    y, _ = librosa.load(TT / f"L{i:02d}.mp3", sr=SR, mono=True)
    db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0] + 1e-9); on = np.where(db > -40)[0]
    a = max(0, on[0] * 256 / SR - 0.03); b = min(len(y) / SR, on[-1] * 256 / SR + 1024 / SR + 0.06)
    seg = y[int(a * SR): int(b * SR)].copy(); k = int(.006 * SR); seg[:k] *= np.linspace(0, 1, k); seg[-k:] *= np.linspace(1, 0, int(k))
    if i > 1: t += GAP[i]
    lin.append(dict(i=i, ini=round(t, 3), fim=round(t + len(seg) / SR, 3)))
    al = json.load(open(TT / f"L{i:02d}.alinhamento.json", encoding="utf-8"))
    for p in palavras(al, t - a): p["linha"] = i; pal.append(p)
    voz.append((t, seg)); t += len(seg) / SR
N = int((t + 1.0) * SR); V = np.zeros(N)
for t0, s in voz: V[int(t0 * SR): int(t0 * SR) + len(s)] += s
sf.write(P / "voz.wav", V, SR, subtype="PCM_16")
json.dump(dict(linhas=lin, palavras=[{k: (round(v, 3) if isinstance(v, float) else v) for k, v in p.items()} for p in pal], fim_fala=round(t, 3)),
          open(P / "tempos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
# partes HeyGen
for nome, l0, l1 in (("A", 1, 7), ("B", 8, 13)):
    a = lin[l0 - 1]["ini"]; b = lin[l1 - 1]["fim"]
    seg = np.concatenate([np.zeros(int(PRE * SR)), V[int(a * SR): int(b * SR)], np.zeros(int(POS * SR))])
    sf.write(P / "avatar" / f"{nome}.wav", seg, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "avatar" / f"{nome}.wav"), "-b:a", "192k", str(P / "avatar" / f"{nome}.mp3")], check=True)
    print(nome, "voz", round(a, 3), "->", round(b, 3), "dur heygen", round(len(seg) / SR, 2))
print("fala termina em", round(t, 2), "| linhas:", [(l["i"], l["ini"]) for l in lin])
