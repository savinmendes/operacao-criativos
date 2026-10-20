# -*- coding: utf-8 -*-
"""Corta L05 em A (ate 'olvidado de mi.'), NARR ('Rezaba ... cambiaba.') e B ('Hasta que ... creer.'), e L06 inteiro.
Encurta pausas > MAXP (energia) para MAXP e remapeia os tempos por palavra. Saida: audio/*.wav + audio/partes.json"""
import json, subprocess
from pathlib import Path
import numpy as np
AQ = Path(__file__).resolve().parent; VOZ = AQ.parents[2] / "_trabalho" / "voz" / "c"; OUT = AQ / "audio"
SR, MAXP, LEAD, TAIL = 48000, 0.25, 0.12, 0.20

def load(p):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy()

def save(a, p):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-c:a", "pcm_s16le", str(p)],
                   input=a.astype(np.float32).tobytes(), check=True)

def silencios(a, thr_db=-42, hop=0.01):
    h = int(hop * SR); n = len(a) // h
    rms = np.sqrt(np.mean(a[:n * h].reshape(n, h) ** 2, 1) + 1e-12); db = 20 * np.log10(rms)
    ref = np.percentile(db, 95); sil = db < max(thr_db, ref - 35)
    runs, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]: j += 1
            runs.append((i * hop, j * hop)); i = j
        else: i += 1
    return runs

def parte(nome, src, t0, t1, words):
    a = load(src); s0, s1 = int(t0 * SR), int(t1 * SR); seg = a[s0:s1]
    # mapa de corte: lista de (ini,fim) removidos (tempo relativo ao segmento)
    rem = []
    for x, y in silencios(seg):
        if y - x > MAXP and x > 0.05 and y < (t1 - t0) - 0.05:   # pausa interna
            c = (x + y) / 2; rem.append((c - (y - x - MAXP) / 2, c + (y - x - MAXP) / 2))
    keep, cur = [], 0.0
    for x, y in rem: keep.append((cur, x)); cur = y
    keep.append((cur, t1 - t0))
    xf = int(0.008 * SR); out = np.zeros(0, np.float32)
    for x, y in keep:
        p = seg[int(x * SR):int(y * SR)].copy()
        if len(out) and xf:
            p[:xf] *= np.linspace(0, 1, xf); out[-xf:] *= np.linspace(1, 0, xf)
            out = np.concatenate([out[:-xf], out[-xf:] + p[:xf], p[xf:]])
        else: out = np.concatenate([out, p])
    def m(t):  # tempo relativo -> tempo novo
        t = t - t0; d = 0.0
        for x, y in rem:
            if t >= y: d += y - x
            elif t > x: d += t - x
        return round(t - d, 3)
    save(out, OUT / f"{nome}.wav")
    W = [dict(w=w["w"], ini=m(w["ini"]), fim=m(w["fim"])) for w in words]
    # pausas finais (>= 0.18 s) no audio enviado, para conferir sorriso
    pz = [(round(x, 3), round(y, 3)) for x, y in silencios(out) if y - x >= 0.15]
    print(nome, f"{len(out) / SR:.2f}s", "removido", [(round(x, 2), round(y, 2)) for x, y in rem])
    return dict(arquivo=f"audio/{nome}.wav", fonte=str(src.name), corte_fonte=[t0, t1], dur=round(len(out) / SR, 3),
                removidos_rel=[[round(x, 3), round(y, 3)] for x, y in rem], palavras=W, pausas=pz)

L5 = json.loads((VOZ / "L05.json").read_text(encoding="utf-8"))["palavras"]
L6d = json.loads((VOZ / "L06.json").read_text(encoding="utf-8")); L6 = L6d["palavras"]
iR = next(i for i, w in enumerate(L5) if w["w"].startswith("Rezaba")); iH = next(i for i, w in enumerate(L5) if w["w"] == "Hasta")
A, N, B = L5[:iR], L5[iR:iH], L5[iH:]
res = {
  "A": parte("L05a", VOZ / "L05.wav", max(0, A[0]["ini"] - LEAD), A[-1]["fim"] + TAIL, A),
  "NARR": parte("L05_narr_rezaba", VOZ / "L05.wav", N[0]["ini"] - 0.08, N[-1]["fim"] + 0.15, N),
  "B": parte("L05b", VOZ / "L05.wav", B[0]["ini"] - LEAD, B[-1]["fim"] + TAIL, B),
  "C": parte("L06", VOZ / "L06.wav", max(0, L6[0]["ini"] - LEAD), L6[-1]["fim"] + TAIL, L6),
}
(OUT / "partes.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
