# -*- coding: utf-8 -*-
"""Linha do tempo da fala v3: abre com 1 s de tela dividida (repórter entra em 1,10 s); dono e Juan J04-J10 iguais à v2;
J11 vira J11a («Por eso… paso a paso.») + JN («Imagina pagar la última cuota…», avatar C) + J11b («Vuelve…»); J12 depois.
Grava voz3.wav e tempos3.json (com «mapa» das fontes de avatar)."""
import json, numpy as np, soundfile as sf, librosa
from pathlib import Path
P = Path(__file__).resolve().parent; TT = P / "tts"; SR = 44100
def pal_local(k):
    al = json.load(open(TT / f"{k}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]; out = []; w = ""
    for c, x, y in zip(ch, s, e):
        if c.isspace():
            if w: out.append([w, ws, we]); w = ""
        else:
            if not w: ws = x
            w += c; we = y
    if w: out.append([w, ws, we])
    return out
def palavras(k, a, b, off):
    return [dict(w=w, ini=round(max(x, a) - a + off, 3), fim=round(min(y, b) - a + off, 3)) for w, x, y in pal_local(k) if x >= a - 0.25 and x < b]
def trecho(k, a, b):
    y, _ = librosa.load(TT / f"{k}.mp3", sr=SR); s = y[int(a * SR):int(b * SR)].copy(); n = int(.008 * SR)
    s[:n] *= np.linspace(0, 1, n); s[-n:] *= np.linspace(1, 0, n); return s
def extensao(k):
    y, _ = librosa.load(TT / f"{k}.mp3", sr=SR)
    db = 20 * np.log10(librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0] + 1e-9); on = np.where(db > -40)[0]
    return max(0, on[0] * 256 / SR - 0.03), min(len(y) / SR, on[-1] * 256 / SR + 1024 / SR + 0.06)
V2 = json.load(open(P / "tempos_v2.json", encoding="utf-8"))
L2 = {}
for l in V2["linhas"]: L2.setdefault(l["k"], []).append(l)
PL = [("R1", 0.0, 4.98, 1.10, "rep"), ("D1", 0.0, 5.60, 6.75, "due"), ("D2", 0.0, 5.48, 12.70, "due"), ("D2", 5.90, 11.10, 18.50, "due")]
for k in ["J04", "J05", "J06", "J07", "J08", "J09", "J10"]:
    a, b = extensao(k); PL.append((k, a, b, L2[k][0]["ini"], "jm"))
# J11 partido
a, b = extensao("J11"); w = pal_local("J11")
fim_paso = next(we for ww, ws, we in w if ww.startswith("paso.")) + 0.06
ini_vuelve = next(ws for ww, ws, we in w if ww.startswith("Vuelve")) - 0.03
t = L2["J11"][0]["ini"]
PL.append(("J11", a, fim_paso, t, "jm")); t += fim_paso - a + 0.30
an, bn = extensao("JN"); PL.append(("JN", an, bn, round(t, 3), "jmC")); t += bn - an + 0.30
PL.append(("J11", ini_vuelve, b, round(t, 3), "jm")); t += b - ini_vuelve + 0.30
a12, b12 = extensao("J12"); PL.append(("J12", a12, b12, round(t, 3), "jm")); t += b12 - a12
FIM = t
N = int((FIM + 1.0) * SR); V = np.zeros(N); pal = []; lin = []
for k, a, b, t0, q in PL:
    s = trecho(k, a, b); V[int(t0 * SR):int(t0 * SR) + len(s)] += s
    nome = k if not (k == "J11") else ("J11a" if a < 1 else "J11b")
    lin.append(dict(k=nome, quem=q, ini=t0, fim=round(t0 + len(s) / SR, 3), a=round(a, 3)))
    for p in palavras(k, a, b, t0): p["linha"] = nome; p["quem"] = q; pal.append(p)
sf.write(P / "voz3.wav", V, SR, subtype="PCM_16")
# mapa do avatar: tempo global -> (video, tempo no video). Na v2 o B tinha J11 inteiro a partir de L2 J11 ini.
old_vuelve = L2["J11"][0]["ini"] + (ini_vuelve - extensao("J11")[0])
new_vuelve = next(l["ini"] for l in lin if l["k"] == "J11b")
DELTA = new_vuelve - old_vuelve
C = json.load(open(P / "v3" / "C.json", encoding="utf-8"))
jn = next(l for l in lin if l["k"] == "JN")
json.dump(dict(linhas=lin, palavras=pal, fim_fala=round(FIM, 3), delta=round(DELTA, 3), jn_ini=jn["ini"], jn_fim=jn["fim"],
               c_off=round(jn["ini"] - C["JN"]["ini_c"], 3), j11b_ini=new_vuelve),
          open(P / "tempos3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print("fim fala", round(FIM, 2), "delta", round(DELTA, 3), [(l["k"], l["ini"], l["fim"]) for l in lin][-5:])
