# -*- coding: utf-8 -*-
"""Realce das palavras de fim de frase que o TTS deixou muito baixas (ex.: "pasa limpiecita", "se carga", "torque").
Mede, por palavra (alinhamento ElevenLabs), o percentil 90 do RMS em quadros de 20 ms; palavra com 3+ letras mais de
8 dB abaixo da mediana do arquivo ganha +(deficit - 4) dB (max 12 dB) com rampas de 30 ms. Nao altera voz/ (original):
grava edicao/_audio/<id>_nv.wav + <id>_nv.alinhamento.json.
  python fix_voz.py corpo_1 corpo_2 trad_38 gancho_3_pega"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

VOZ = Path(r"C:\Users\PICHAU\Downloads\DEWALT-ADS\voz")
AUD = Path(__file__).resolve().parent / "_audio"
SR = 48000


def palavras(al):
    a = json.load(open(al, encoding="utf-8"))
    ws, cur = [], None
    for c, s, e in zip(a["characters"], a["character_start_times_seconds"], a["character_end_times_seconds"]):
        if c.isspace():
            if cur:
                ws.append(cur)
            cur = None
        elif cur is None:
            cur = [c, s, e]
        else:
            cur[0] += c
            cur[2] = e
    if cur:
        ws.append(cur)
    return ws


def nivel(x, s, e, H=960):
    seg = x[int(s * SR):int(e * SR)].mean(1)
    n = len(seg) // H
    if n < 3:
        return None
    return float(np.percentile(20 * np.log10(np.sqrt((seg[:n * H].reshape(n, H) ** 2).mean(1)) + 1e-9), 90))


AUD.mkdir(exist_ok=True)
rel = {}
for iid in sys.argv[1:]:
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(VOZ / f"{iid}.mp3"), "-ac", "2", "-ar", str(SR),
                                      "-f", "f32le", "-"], capture_output=True, check=True).stdout,
                      np.float32).reshape(-1, 2).astype(np.float64)
    ws = palavras(VOZ / f"{iid}.alinhamento.json")
    nv = [(w, s, e, nivel(x, s, e)) for w, s, e in ws]
    med = float(np.median([v for *_, v in nv if v is not None]))
    g = np.zeros(len(x))
    feitos = []
    for w, s, e, v in nv:
        if v is None or len(re.sub(r"\W", "", w)) < 3 or v > med - 8:
            continue
        db = min(12.0, med - 4 - v)
        a, b = int((s - 0.03) * SR), int((e + 0.05) * SR)
        r = int(0.03 * SR)
        env = np.full(b - a, db)
        env[:r] = np.linspace(0, db, r)
        env[-r:] = np.linspace(db, 0, r)
        g[a:b] = np.maximum(g[a:b], env)
        feitos.append((w, round(s, 2), round(v - med, 1), round(db, 1)))
    y = x * (10 ** (g / 20))[:, None]
    pk = np.abs(y).max()
    if pk > 0.97:
        y *= 0.97 / pk
    out = AUD / f"{iid}_nv.wav"
    sf.write(out, y.astype(np.float32), SR, subtype="FLOAT")
    shutil.copy(VOZ / f"{iid}.alinhamento.json", AUD / f"{iid}_nv.alinhamento.json")
    rel[iid] = feitos
    print(iid, "mediana", round(med, 1), "realces:", feitos)
json.dump(rel, open(AUD / "fix_voz.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
