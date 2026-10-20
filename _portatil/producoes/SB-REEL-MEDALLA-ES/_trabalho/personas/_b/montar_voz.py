# -*- coding: utf-8 -*-
"""Narração de uma persona: f1+f2 (reza) + f3..f5 (selfie) da voz da persona + sacerdote da v2 (idêntico).
Uso: python montar_voz.py <slug>   (gera <slug>/narracao_completa.mp3, palavras.json, timeline.json, selfie.mp3)"""
import json, re, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
AQ = Path(__file__).resolve().parent.parent
TR = AQ.parent
sys.path.insert(0, str(TR / "voz"))
import montar_vozes as mv
SR = mv.SR
slug = sys.argv[1]; P = AQ / slug
V2 = TR / "voz" / "v2"
nar = mv.carregar(V2 / "narracao_completa.mp3")
W2 = json.loads((V2 / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
SAC_V2 = 35.06          # sacerdote_offset da v2
SAC_CORTE = 34.85       # corta a v2 aqui (silêncio antes de "Esta")


def fala(k, alvo):
    x = mv.normalizar(mv.carregar(P / f"{k}.mp3"), alvo)
    w = mv.palavras(P / f"{k}.alinhamento.json")
    a = max(0.0, w[0]["ini"] - 0.06); b = min(len(x) / SR, w[-1]["fim"] + 0.12)
    seg = x[int(a * SR):int(b * SR)].copy()
    f = int(0.008 * SR); seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
    return seg, [dict(w=q["w"], ini=q["ini"] - a, fim=q["fim"] - a) for q in w]


partes, out, t = [], [], 0.0


def put(seg, ws, parte, k):
    global t
    for q in ws:
        out.append(dict(w=q["w"], ini=round(q["ini"] + t, 3), fim=round(q["fim"] + t, 3), personagem=slug, parte=parte, fala=k))
    partes.append(seg); t += len(seg) / SR


def pausa(s):
    global t
    partes.append(np.zeros(int(round(s * SR)), np.float32)); t += int(round(s * SR)) / SR


pausa(0.21)
put(*fala("f1", -20.0), "reza", "f1"); pausa(1.10)
put(*fala("f2", -20.0), "reza", "f2")
C = round(t + 0.45, 2)
pausa(C + 0.11 - t)
for k in ("f3", "f4", "f5"):
    put(*fala(k, -18.0), "selfie", k)
    pausa(0.35)
fim_selfie = out[-1]["fim"]
sac_ini = t
partes.append(nar[int(SAC_CORTE * SR):]); t += len(nar[int(SAC_CORTE * SR):]) / SR
desl = sac_ini - SAC_CORTE
out += [dict(w, ini=round(w["ini"] + desl, 3), fim=round(w["fim"] + desl, 3)) for w in W2 if w["ini"] >= SAC_V2]
tot = np.concatenate(partes)
sf.write(P / "narracao_completa.wav", tot, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "narracao_completa.wav"), "-c:a", "libmp3lame", "-b:a", "192k",
                str(P / "narracao_completa.mp3")], check=True)
(P / "narracao_completa.wav").unlink()
(P / "narracao_completa.palavras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
SELF0 = round(C - 0.05, 3)
info = {"C": C, "selfie_ini": SELF0, "fim_selfie": fim_selfie, "desl": round(desl, 3),
        "sacerdote_offset": round(SAC_V2 + desl, 3), "total": round(len(tot) / SR, 3)}
(P / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{SELF0:.3f}", "-to", f"{fim_selfie + 0.35:.3f}", "-i", str(P / "narracao_completa.mp3"),
                "-c:a", "libmp3lame", "-b:a", "192k", str(P / "selfie.mp3")], check=True)
print(slug, info)
print(" ".join(f"{w['w']}[{w['ini']:.2f}-{w['fim']:.2f}]" for w in out if w.get("fala")))
