# -*- coding: utf-8 -*-
"""Encurta pausas internas (> MAXP -> MAXP) e remapeia o alinhamento ElevenLabs. Divide em partes (jobs HeyGen <= ~12 s)
nas fronteiras de frase. Saída: <id>.wav + <id>.json (palavras) para cada parte. Uso: python prep.py"""
import json, subprocess
from pathlib import Path
import numpy as np
AQ = Path(__file__).resolve().parent; SR = 48000
# id -> (maxp, partes: lista de (nome, 1ª palavra, última palavra) por índice de palavra) ; None = 1 parte só
CFG = {"R00": (0.16, None), "R01": (0.25, None), "CTA": (0.25, None), "C": (0.25, "auto"), "P": (0.25, "auto")}
LIM = 11.5

def load(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()

def save(a, p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-ac", "2", "-c:a", "pcm_s16le", str(p)],
                   input=a.astype(np.float32).tobytes(), check=True)

def palavras(i):
    d = json.loads((AQ / f"{i}.alinhamento.json").read_text(encoding="utf-8")); W = []; cur = None
    for ch, s, e in zip(d["characters"], d["character_start_times_seconds"], d["character_end_times_seconds"]):
        if ch.isspace():
            if cur: W.append(cur); cur = None
            continue
        if cur is None: cur = [ch, s, e]
        else: cur[0] += ch; cur[2] = e
    if cur: W.append(cur)
    return [dict(w=w, ini=a, fim=b) for w, a, b in W]

def silencios(a, hop=0.01):
    h = int(hop * SR); n = len(a) // h
    db = 20 * np.log10(np.sqrt(np.mean(a[:n * h].reshape(n, h) ** 2, 1) + 1e-12)); ref = np.percentile(db, 95); sil = db < ref - 32
    R, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            R.append((i * hop, j * hop)); i = j
        else: i += 1
    return R

def comprime(a, W, maxp, lead=0.10, tail=0.18):
    t0 = max(0, W[0]["ini"] - lead); t1 = min(len(a) / SR, W[-1]["fim"] + tail)
    seg = a[int(t0 * SR):int(t1 * SR)]; rem = []
    for x, y in silencios(seg):
        # só pausas ENTRE palavras (não corta dentro de palavra)
        if y - x > maxp and x > 0.05 and y < (t1 - t0) - 0.05:
            c = (x + y) / 2; d = (y - x - maxp) / 2; rem.append((c - d, c + d))
    keep, cur = [], 0.0
    for x, y in rem: keep.append((cur, x)); cur = y
    keep.append((cur, t1 - t0)); xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for x, y in keep:
        p = seg[int(x * SR):int(y * SR)].copy()
        if len(out):
            p[:xf] *= np.linspace(0, 1, xf); out[-xf:] *= np.linspace(1, 0, xf); out = np.concatenate([out[:-xf], out[-xf:] + p[:xf], p[xf:]])
        else: out = p
    def m(t):
        t = t - t0; d = 0.0
        for x, y in rem:
            if t >= y: d += y - x
            elif t > x: d += t - x
        return round(max(0.0, t - d), 3)
    f = int(0.03 * SR); out[-f:] *= np.linspace(1, 0, f)
    return out, [dict(w=w["w"], ini=m(w["ini"]), fim=m(w["fim"])) for w in W]

res = {}
for i, (maxp, partes) in CFG.items():
    a = load(AQ / f"{i}.mp3"); W = palavras(i)
    if partes == "auto":       # frases -> agrupa em partes <= LIM s
        fr, cur = [], []
        for w in W:
            cur.append(w)
            if w["w"][-1] in ".?!": fr.append(cur); cur = []
        if cur: fr.append(cur)
        grupos, g = [], []
        for f_ in fr:
            if g and f_[-1]["fim"] - g[0]["ini"] > LIM: grupos.append(g); g = []
            g = g + f_
        grupos.append(g)
    else: grupos = [W]
    for k, g in enumerate(grupos):
        nome = i if len(grupos) == 1 else f"{i}{k + 1}"
        o, P = comprime(a, g, maxp); save(o, AQ / f"{nome}.wav")
        (AQ / f"{nome}.json").write_text(json.dumps(dict(texto=" ".join(w["w"] for w in g), dur=round(len(o) / SR, 3), palavras=P), ensure_ascii=False, indent=0), encoding="utf-8")
        res[nome] = round(len(o) / SR, 2); print(nome, res[nome], " ".join(w["w"] for w in g))
print("total", round(sum(res.values()), 2))
