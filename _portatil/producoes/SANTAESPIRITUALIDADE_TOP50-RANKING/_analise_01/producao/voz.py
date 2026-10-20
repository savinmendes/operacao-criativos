# -*- coding: utf-8 -*-
"""Linha do tempo da fala ES (global): repórter, dono, Juan. Grava voz.wav, tempos.json e avatar/A.wav, B.wav (Juan, p/ HeyGen)."""
import json, subprocess, numpy as np, soundfile as sf, librosa
from pathlib import Path
P = Path(__file__).resolve().parent; TT = P / "tts"; SR = 44100
def palavras(k, a, b, off):
    al = json.load(open(TT / f"{k}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]; out = []; w = ""
    for c, x, y in zip(ch, s, e):
        if c.isspace():
            if w: out.append([w, ws, we]); w = ""
        else:
            if not w: ws = x
            w += c; we = y
    if w: out.append([w, ws, we])
    return [dict(w=w, ini=round(max(x, a) - a + off, 3), fim=round(min(y, b) - a + off, 3)) for w, x, y in out if x >= a - 0.25 and x < b]
def trecho(k, a, b):
    y, _ = librosa.load(TT / f"{k}.mp3", sr=SR); s = y[int(a * SR):int(b * SR)].copy(); n = int(.008 * SR)
    s[:n] *= np.linspace(0, 1, n); s[-n:] *= np.linspace(1, 0, n); return s
def extensao(k):
    y, _ = librosa.load(TT / f"{k}.mp3", sr=SR)
    db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0] + 1e-9); on = np.where(db > -40)[0]
    return max(0, on[0] * 256 / SR - 0.03), min(len(y) / SR, on[-1] * 256 / SR + 1024 / SR + 0.06)
# (chave, ini no audio, fim no audio, tempo global, quem)
PL = [("R1", 0.0, 4.98, 0.10, "rep"),
      ("D1", 0.0, 5.60, 6.75, "due"),
      ("D2", 0.0, 5.48, 12.70, "due"),
      ("D2", 5.90, 11.10, 18.50, "due")]
t = 24.05; GAP = {"J05": .30, "J06": .30, "J07": .45, "J08": .40, "J09": .30, "J10": .30, "J11": .30, "J12": .30}
for k in ["J04", "J05", "J06", "J07", "J08", "J09", "J10", "J11", "J12"]:
    a, b = extensao(k); t += GAP.get(k, 0); PL.append((k, a, b, round(t, 3), "jm")); t += b - a
FIM_FALA = t
N = int((FIM_FALA + 1.0) * SR); V = np.zeros(N); pal = []; lin = []
for k, a, b, t0, q in PL:
    s = trecho(k, a, b); V[int(t0 * SR):int(t0 * SR) + len(s)] += s
    lin.append(dict(k=k, quem=q, ini=t0, fim=round(t0 + len(s) / SR, 3), a=a))
    for p in palavras(k, a, b, t0): p["linha"] = k; p["quem"] = q; pal.append(p)
sf.write(P / "voz.wav", V, SR, subtype="PCM_16")
json.dump(dict(linhas=lin, palavras=pal, fim_fala=round(FIM_FALA, 3)), open(P / "tempos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
# partes Juan p/ HeyGen: A = J04..J07, B = J08..J12 (pre 0.25 s, pos 0.40 s)
(P / "avatar").mkdir(exist_ok=True)
for nome, l0, l1 in (("A", "J04", "J07"), ("B", "J08", "J12")):
    a = next(l["ini"] for l in lin if l["k"] == l0); b = next(l["fim"] for l in lin if l["k"] == l1)
    seg = np.concatenate([np.zeros(int(.25 * SR)), V[int(a * SR):int(b * SR)], np.zeros(int(.40 * SR))])
    sf.write(P / "avatar" / f"{nome}.wav", seg, SR, subtype="PCM_16")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "avatar" / f"{nome}.wav"), "-b:a", "192k", str(P / "avatar" / f"{nome}.mp3")], check=True)
    print(nome, a, b, "dur", round(len(seg) / SR, 2), "offset (global = t_avatar - 0.25 + a)")
print("fim fala", round(FIM_FALA, 2), [(l["k"], l["ini"], l["fim"]) for l in lin])
