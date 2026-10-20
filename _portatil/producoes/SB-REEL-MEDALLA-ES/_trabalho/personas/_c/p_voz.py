# -*- coding: utf-8 -*-
"""Narração da persona: reza (v3, falas 1+2) + selfie (falas 3-5) + sacerdote idêntico à v2.
uso: python p_voz.py <slug>  -> <slug>/voz/narracao_completa.mp3 + .palavras.json + timeline.json + selfie_heygen.mp3"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
AQ = Path(__file__).resolve().parent
TR = AQ.parents[1]
sys.path.insert(0, str(TR / "voz"))
import montar_vozes as mv
SR = mv.SR
slug = sys.argv[1]
V = AQ.parent / slug / "voz"
V2 = TR / "voz" / "v2"

def corta(x, ws, pad0=0.06, pad1=0.15):
    a = max(0.0, ws[0]["ini"] - pad0); b = min(len(x) / SR, ws[-1]["fim"] + pad1)
    y = x[int(a * SR):int(b * SR)].copy(); f = int(0.008 * SR)
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y, a

rz = mv.normalizar(mv.carregar(V / "reza.mp3"), -20.0); wr = mv.palavras(V / "reza.alinhamento.json")
sl = mv.normalizar(mv.carregar(V / "selfie.mp3"), -18.0); ws = mv.palavras(V / "selfie.alinhamento.json")
nar = mv.carregar(V2 / "narracao_completa.mp3")
W2 = json.loads((V2 / "narracao_completa.palavras.json").read_text(encoding="utf-8"))

# reza começa como na v2 (1ª palavra em ~0,27 s)
yr, ar = corta(rz, wr, pad0=0.20)
t_r = 0.27 - (wr[0]["ini"] - ar)
R = t_r + len(yr) / SR
C = round(max(R + 0.30, 10.0), 2)
ys, as_ = corta(ws, ws) if False else corta(sl, ws)
t_s = C + 0.17 - (ws[0]["ini"] - as_)
E5 = t_s + (ws[-1]["fim"] - as_)
B0 = 34.75                      # v2: depois de "abrirse." (34,40) e antes do sacerdote (35,09)
t_b = E5 + 0.35
sac = nar[int(B0 * SR):]
tot = np.zeros(int((t_b + len(sac) / SR) * SR) + 10, np.float32)
def put(x, t):
    i = int(round(t * SR)); tot[i:i + len(x)] += x
put(yr, t_r); put(ys, t_s); put(sac, t_b)
sf.write(V / "narracao_completa.wav", tot, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "narracao_completa.wav"), "-c:a", "libmp3lame", "-b:a", "192k",
                str(V / "narracao_completa.mp3")], check=True)
(V / "narracao_completa.wav").unlink()
out = [dict(w=w["w"], ini=round(w["ini"] - ar + t_r, 3), fim=round(w["fim"] - ar + t_r, 3), personagem=slug, parte="reza") for w in wr]
out += [dict(w=w["w"], ini=round(w["ini"] - as_ + t_s, 3), fim=round(w["fim"] - as_ + t_s, 3), personagem=slug, parte="selfie") for w in ws]
desl = t_b - B0
out += [dict(w, ini=round(w["ini"] + desl, 3), fim=round(w["fim"] + desl, 3)) for w in W2 if w["ini"] >= B0]
(V / "narracao_completa.palavras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
TL = json.loads((V2 / "timeline.json").read_text())
SELF0 = round(C - 0.05, 3)
info = {"C": C, "reza_fim": round(R, 3), "selfie_ini": round(t_s, 3), "selfie_fim": round(E5, 3), "self0": SELF0,
        "desl": round(desl, 3), "sacerdote_offset": round(TL["sacerdote_offset"] + desl, 3), "total": round(len(tot) / SR, 3)}
(V / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{SELF0:.3f}", "-to", f"{E5 + 0.35:.3f}", "-i", str(V / "narracao_completa.mp3"),
                "-c:a", "libmp3lame", "-b:a", "192k", str(V / "selfie_heygen.mp3")], check=True)
print(slug, info)
