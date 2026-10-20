# -*- coding: utf-8 -*-
"""Narração do motorista de app: v2 [0, 11.90) (reza) + f3 nova + v2 [18.85, fim] (frases 4-5 + sacerdote)."""
import json, subprocess, sys
from pathlib import Path
import numpy as np, soundfile as sf
AQ = Path(__file__).resolve().parent
sys.path.insert(0, str(AQ.parent / "voz"))
import montar_vozes as mv
SR = mv.SR
V2 = AQ.parent / "voz" / "v2"
nar = mv.carregar(V2 / "narracao_completa.mp3")
W = json.loads((V2 / "narracao_completa.palavras.json").read_text(encoding="utf-8"))
f3 = mv.normalizar(mv.carregar(AQ / "f3.mp3"), -18.0)
w3 = mv.palavras(AQ / "f3.alinhamento.json")
# trecho útil da f3
a3 = max(0.0, w3[0]["ini"] - 0.06); b3 = min(len(f3) / SR, w3[-1]["fim"] + 0.12)
seg3 = f3[int(a3 * SR):int(b3 * SR)]
A_FIM, B_INI = 11.90, 18.85
t3 = 11.97 - 0.06            # "Yo" cai no mesmo ponto da v2
pausa = 0.32
parte1 = nar[:int(A_FIM * SR)]
pad1 = np.zeros((int(t3 * SR) - len(parte1),) + nar.shape[1:], np.float32)
p = np.zeros((int(pausa * SR),) + nar.shape[1:], np.float32)
if seg3.ndim != nar.ndim:
    seg3 = seg3 if nar.ndim == 1 else np.repeat(seg3[:, None], nar.shape[1], 1)
f = int(0.008 * SR); seg3 = seg3.copy(); seg3[:f] *= np.linspace(0, 1, f).reshape(-1, *([1] * (seg3.ndim - 1))); seg3[-f:] *= np.linspace(1, 0, f).reshape(-1, *([1] * (seg3.ndim - 1)))
parte3 = nar[int(B_INI * SR):]
tot = np.concatenate([parte1, pad1, seg3, p, parte3])
desl = (t3 + len(seg3) / SR + pausa) - B_INI
sf.write(AQ / "narracao_completa.wav", tot, SR)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ / "narracao_completa.wav"), "-c:a", "libmp3lame", "-b:a", "192k",
                str(AQ / "narracao_completa.mp3")], check=True)
(AQ / "narracao_completa.wav").unlink()
out = [w for w in W if w["fim"] <= A_FIM]
for w in w3:
    out.append(dict(w=w["w"], ini=round(w["ini"] - a3 + t3, 3), fim=round(w["fim"] - a3 + t3, 3), personagem="comerciante", parte="selfie"))
out += [dict(w, ini=round(w["ini"] + desl, 3), fim=round(w["fim"] + desl, 3)) for w in W if w["ini"] >= B_INI]
(AQ / "narracao_completa.palavras.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
TL = json.loads((V2 / "timeline.json").read_text())
info = {"desl": round(desl, 3), "sacerdote_offset": round(TL["sacerdote_offset"] + desl, 3), "total": round(len(tot) / SR, 3),
        "f3_ini": t3, "f3_fim": round(t3 + len(seg3) / SR, 3)}
(AQ / "timeline.json").write_text(json.dumps(info, indent=1), encoding="utf-8")
# áudio da selfie para o HeyGen: de 11.75 até o fim de "abrirse."
abr = [w for w in out if w["w"].startswith("abrirse")][0]["fim"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "11.75", "-to", f"{abr + 0.35:.3f}", "-i", str(AQ / "narracao_completa.mp3"),
                "-c:a", "libmp3lame", "-b:a", "192k", str(AQ / "selfie_app.mp3")], check=True)
print(info, "abrirse", abr)
for w in out[18:40]: print(w["w"], w["ini"], w["fim"])
