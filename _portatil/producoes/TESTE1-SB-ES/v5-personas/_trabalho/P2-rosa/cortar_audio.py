# -*- coding: utf-8 -*-
"""Recorta cada bloco: P (em tela, HeyGen) pausas internas <= 0,25 s; V (off) pausas naturais (so limita a 0,45 s).
Saida: P -> audio/<id>.wav ; V -> vo_<id>.wav ; audio/itens.json {texto, dur, palavras, pausas}"""
import json, subprocess, sys, numpy as np
from pathlib import Path
AQ = Path(__file__).resolve().parent; A = AQ / "audio"; SR = 48000
sys.path.insert(0, "C:/Users/PICHAU/Downloads/TESTE1-SB-ES/_trabalho/voz"); from palavras import palavras
def load(p):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
LEAD, TAIL, F = 0.10, 0.18, int(0.006 * SR)
out = {}
for b in json.loads((AQ / "blocos.json").read_text(encoding="utf-8")):
    iid, av = b["id"], b["tela"]; a = load(A / f"{iid}.mp3"); W = palavras(A / f"{iid}.alinhamento.json")
    MAXP = 0.25 if av else 0.45
    t0 = max(W[0]["ini"] - LEAD, 0); t1 = min(W[-1]["fim"] + TAIL, len(a) / SR)
    cortes = []
    for x, y in zip(W, W[1:]):
        g = y["ini"] - x["fim"]
        if g > MAXP: rem = g - MAXP; c0 = x["fim"] + MAXP / 2; cortes.append((c0, c0 + rem))
    partes, t = [], t0
    for c0, c1 in cortes: partes.append(a[int(t * SR):int(c0 * SR)].copy()); t = c1
    partes.append(a[int(t * SR):int(t1 * SR)].copy())
    for k, p in enumerate(partes):
        if k > 0: p[:F] *= np.linspace(0, 1, F)[:, None]
        if k < len(partes) - 1: p[-F:] *= np.linspace(1, 0, F)[:, None]
    y = np.concatenate(partes); n = int(0.01 * SR); y[:n] *= np.linspace(0, 1, n)[:, None]; y[-n:] *= np.linspace(1, 0, n)[:, None]
    def m(tt): return round(tt - t0 - sum(min(max(tt - c0, 0), c1 - c0) for c0, c1 in cortes), 3)
    WW = [dict(w=w["w"], ini=m(w["ini"]), fim=m(w["fim"])) for w in W]
    dur = round(len(y) / SR, 3)
    pausas = [[0.0, WW[0]["ini"]]] + [[x["fim"], z["ini"]] for x, z in zip(WW, WW[1:]) if z["ini"] - x["fim"] >= 0.15] + [[WW[-1]["fim"], dur]]
    raw = A / "_t.f32"; raw.write_bytes(y.astype(np.float32).tobytes())
    dst = (A / f"{iid}.wav") if av else (AQ / f"vo_{iid}.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw), "-c:a", "pcm_s16le", str(dst)]); raw.unlink()
    if av: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(dst), "-c:a", "libmp3lame", "-b:a", "192k", str(A / f"{iid}_up.mp3")])
    out[iid] = dict(arquivo=dst.name, texto=b["texto"], tts=b.get("tts"), dur=dur, palavras=WW,
                    pausas=[[round(p, 3), round(q, 3)] for p, q in pausas], avatar=av, cortes=len(cortes))
    print(f"{iid} {dur:6.2f}s cortes={len(cortes)} pausas={[(round(p,2),round(q,2)) for p,q in pausas[1:-1]]}")
json.dump(out, open(A / "itens.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
