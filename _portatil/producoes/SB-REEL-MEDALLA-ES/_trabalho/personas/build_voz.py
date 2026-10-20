# -*- coding: utf-8 -*-
"""Narração de uma persona: reza (falas 1-2, eleven_v3) + selfie (falas 3-5, pausas apertadas) + sacerdote da v2 (idêntico).
python build_voz.py <slug>  -> <slug>/narracao_completa.mp3, .palavras.json, timeline.json, selfie_tight.mp3"""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
AQ = Path(__file__).resolve().parent
TR = AQ.parent
sys.path.insert(0, str(TR / "voz"))
import montar_vozes as mv
SR = mv.SR
slug = sys.argv[1]; P = AQ / slug
V2 = TR / "voz" / "v2"
SAC_V2 = 35.06
PAUSA_MAX, PAUSA_ALVO = 0.42, 0.30


def fade(y, ms=8):
    f = int(ms / 1000 * SR); y = y.copy()
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y


# reza
a = mv.normalizar(mv.carregar(P / "reza.mp3"), -20.0)
wa = mv.palavras(P / "reza.alinhamento.json")
a0 = max(0.0, wa[0]["ini"] - 0.12); a1 = min(len(a) / SR, wa[-1]["fim"] + 0.30)
lead = 0.20
reza = np.concatenate([np.zeros(int(lead * SR), np.float32), fade(a[int(a0 * SR):int(a1 * SR)])])
out = [dict(w=w["w"], ini=round(w["ini"] - a0 + lead, 3), fim=round(w["fim"] - a0 + lead, 3), personagem="persona", parte="reza") for w in wa]
C = round(len(reza) / SR + 0.15, 2)

# selfie com pausas apertadas
b = mv.normalizar(mv.carregar(P / "selfie.mp3"), -18.0)
wb = mv.palavras(P / "selfie.alinhamento.json")
pedacos, ws_sel, t = [], [], 0.0
cur0 = max(0.0, wb[0]["ini"] - 0.08)
grupos = [[wb[0]]]
for w0, w1 in zip(wb, wb[1:]):
    if w1["ini"] - w0["fim"] > PAUSA_MAX:
        grupos.append([w1])
    else:
        grupos[-1].append(w1)
for k, g in enumerate(grupos):
    s0 = max(0.0, g[0]["ini"] - (0.08 if k == 0 else PAUSA_ALVO / 2))
    s1 = min(len(b) / SR, g[-1]["fim"] + (0.25 if k == len(grupos) - 1 else PAUSA_ALVO / 2))
    seg = fade(b[int(s0 * SR):int(s1 * SR)])
    for w in g:
        ws_sel.append(dict(w=w["w"], ini=round(w["ini"] - s0 + t, 3), fim=round(w["fim"] - s0 + t, 3)))
    pedacos.append(seg); t += len(seg) / SR
sel = np.concatenate(pedacos)
sf.write(P / "selfie_tight.wav", sel, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "selfie_tight.wav"), "-c:a", "libmp3lame", "-b:a", "192k", str(P / "selfie_tight.mp3")], check=True)
(P / "selfie_tight.wav").unlink()

# sacerdote (v2, idêntico)
nar2 = mv.carregar(V2 / "narracao_completa.mp3")
sac = nar2[int(SAC_V2 * SR):]
W2 = json.loads((V2 / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
SAC = round(C + len(sel) / SR + 1.30, 3)

tot_n = int(SAC * SR) + len(sac)
tot = np.zeros(tot_n, np.float32)
tot[:len(reza)] = reza
tot[int(C * SR):int(C * SR) + len(sel)] = sel
tot[int(SAC * SR):int(SAC * SR) + len(sac)] = sac
for w in ws_sel:
    out.append(dict(w=w["w"], ini=round(w["ini"] + C, 3), fim=round(w["fim"] + C, 3), personagem="persona", parte="selfie"))
out += [dict(w, ini=round(w["ini"] - SAC_V2 + SAC, 3), fim=round(w["fim"] - SAC_V2 + SAC, 3)) for w in W2 if w.get("personagem") == "sacerdote"]
sf.write(P / "narracao_completa.wav", tot, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(P / "narracao_completa.wav"), "-c:a", "libmp3lame", "-b:a", "192k", str(P / "narracao_completa.mp3")], check=True)
(P / "narracao_completa.wav").unlink()
(P / "narracao_completa.palavras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
info = {"C": C, "selfie_dur": round(len(sel) / SR, 3), "sac": SAC, "desl_sac": round(SAC - SAC_V2, 3), "total": round(tot_n / SR, 3)}
(P / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
print(slug, info, "grupos", len(grupos))
