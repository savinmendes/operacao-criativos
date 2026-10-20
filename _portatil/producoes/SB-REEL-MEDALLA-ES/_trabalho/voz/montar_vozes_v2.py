# -*- coding: utf-8 -*-
"""v2: comerciante = reza (com_a_v3, igual à v1) + selfie nova (v2/com_b2); sacerdote = v2/sac2 (texto novo).
Saídas em voz/v2/: comerciante.*, sacerdote.*, narracao_completa.mp3/.palavras.json, timeline.json"""
import json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import montar_vozes as mv

V1 = Path(__file__).resolve().parent
V2 = V1 / "v2"
mv.AQUI = V2
SR = mv.SR

a = mv.normalizar(mv.carregar(mv.P / "com_a_v3.mp3"), -20.0)
wa = mv.palavras(mv.P / "com_a_v3.alinhamento.json")
b = mv.normalizar(mv.carregar(V2 / "com_b2.mp3"), -18.0)
wb = mv.palavras(V2 / "com_b2.alinhamento.json")
T = mv.Trilha()
y, w, t0 = mv.trecho(a, wa, 0, len(wa)); T.add(y, w, t0, {"personagem": "comerciante", "parte": "reza"})
T.silencio(max(0.0, 11.9 - T.t))
y, w, t0 = mv.trecho(b, wb, 0, len(wb)); T.add(y, w, t0, {"personagem": "comerciante", "parte": "selfie"})
com = T.salvar("comerciante"); com_ws = T.ws

s = mv.normalizar(mv.carregar(V2 / "sac2.mp3"))
ws = mv.palavras(V2 / "sac2.alinhamento.json")
S = mv.Trilha()
y, w, t0 = mv.trecho(s, ws, 0, len(ws)); S.add(y, w, t0, {"personagem": "sacerdote"})
sac = S.salvar("sacerdote")

gap = 0.45
off = len(com) / SR + gap
tot = np.concatenate([com, np.zeros(int(gap * SR), np.float32), sac])
sf.write(V2 / "narracao_completa.wav", tot, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V2 / "narracao_completa.wav"), "-c:a", "libmp3lame",
                "-b:a", "192k", str(V2 / "narracao_completa.mp3")], check=True)
(V2 / "narracao_completa.wav").unlink()
allw = [dict(w) for w in com_ws] + [dict(w, ini=round(w["ini"] + off, 3), fim=round(w["fim"] + off, 3)) for w in S.ws]
(V2 / "narracao_completa.palavras.json").write_text(json.dumps(allw, ensure_ascii=False, indent=1), encoding="utf-8")
info = {"comerciante_dur": round(len(com) / SR, 2), "sacerdote_dur": round(len(sac) / SR, 2),
        "sacerdote_offset": round(off, 2), "total": round(len(tot) / SR, 2)}
(V2 / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
print(info)
