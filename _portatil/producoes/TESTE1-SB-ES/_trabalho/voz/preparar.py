# -*- coding: utf-8 -*-
"""Encurta pausas longas dentro de cada fala (corte no meio do silêncio, com micro-fade) -> voz/c/<id>.wav + <id>.json (palavras)."""
import json, subprocess, numpy as np
from pathlib import Path
from palavras import palavras
AQ = Path(__file__).resolve().parent; SR = 48000
MAXP = {"default": 0.40}; ALVO = {"default": 0.36, "L08": 0.55}
def load(p):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
for f in json.loads((AQ / "falas.json").read_text(encoding="utf-8")):
    i = f["id"]; a = load(AQ / f"{i}.mp3"); P = palavras(AQ / f"{i}.alinhamento.json")
    alvo = ALVO.get(i, ALVO["default"]); cortes = []
    for x, y in zip(P, P[1:]):
        g = y["ini"] - x["fim"]
        if g > max(alvo, MAXP["default"]):
            rem = g - alvo; c0 = x["fim"] + (g - rem) / 2; cortes.append((c0, c0 + rem))
    # aplica cortes
    partes = []; t = 0.0; fade = int(0.008 * SR)
    for c0, c1 in cortes:
        partes.append(a[int(t * SR):int(c0 * SR)]); t = c1
    partes.append(a[int(t * SR):])
    for k in range(len(partes) - 1):  # micro-fade nas emendas
        if len(partes[k]) > fade: partes[k][-fade:] *= np.linspace(1, 0, fade)[:, None]
        if len(partes[k + 1]) > fade: partes[k + 1][:fade] *= np.linspace(0, 1, fade)[:, None]
    out = np.concatenate(partes)
    def mapa(tt):
        d = sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes); return round(tt - d, 3)
    W = [dict(w=p["w"], ini=mapa(p["ini"]), fim=mapa(p["fim"])) for p in P]
    # corta o fim 0.12 s depois da última palavra, começo mantido
    out = out[:int((W[-1]["fim"] + 0.12) * SR)]
    raw = AQ / "c" / f"{i}.f32"; raw.write_bytes(out.astype(np.float32).tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-c:a", "pcm_s16le", str(AQ / "c" / f"{i}.wav")])
    raw.unlink()
    json.dump(dict(id=i, p=f["p"], dur=round(len(out) / SR, 3), palavras=W), open(AQ / "c" / f"{i}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(i, f"{len(a)/SR:.2f} -> {len(out)/SR:.2f}  ({len(cortes)} pausas)")
