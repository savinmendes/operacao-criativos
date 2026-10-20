# -*- coding: utf-8 -*-
"""Monta narracao_es.wav (+ um wav por personagem) e o alinhamento no tempo do video.
Uso: python narracao.py pecas.json
pecas.json: {"dur": 18.07, "tts": "_audio/tts", "saida": ".", "pecas": [
   {"b": "b0", "pos": 0.05, "tempo": 1.06, "quem": "MULHER", "cortes": [[ini, fim], ...]}  # cortes em s do arquivo original
]}
O tempo (atempo) e os cortes sao aplicados ao audio e ao alinhamento por caractere. -16 LUFS por bloco."""
import json, re, subprocess, sys, tempfile, os
from pathlib import Path
import numpy as np, soundfile as sf
cfg = json.load(open(sys.argv[1], encoding="utf-8")); R = Path(sys.argv[1]).resolve().parent
T = R / cfg["tts"]; OUT = R / cfg.get("saida", "."); DUR = cfg["dur"]; SR = 48000
tmp = Path(tempfile.mkdtemp())
def lufs(f):
    o = subprocess.run(["ffmpeg","-i",str(f),"-af","ebur128","-f","null","-"],capture_output=True,text=True,encoding="utf-8",errors="ignore").stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])
def mapa(t, cortes, tempo):
    """tempo no arquivo original -> tempo na peca processada (cortes removidos, depois atempo)"""
    d = 0.0
    for a, b in cortes:
        if t >= b: d += b - a
        elif t > a: d += t - a
    return (t - d) / tempo
pistas = {}; C, S, E = [], [], []; tempos = []
for p in cfg["pecas"]:
    b = p["b"]; tempo = p.get("tempo", 1.0); cortes = sorted(p.get("cortes", []))
    src = T / f"{b}.mp3"; w = tmp / f"{b}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(src),"-ar",str(SR),"-ac","1",str(w)],check=True)
    x, _ = sf.read(w)
    keep = np.ones(len(x), bool)
    for a, c in cortes:
        ia, ic = int(a*SR), int(c*SR); keep[ia:ic] = False
        k = int(0.01*SR)  # micro fade na emenda
        if ia-k > 0: x[ia-k:ia] *= np.linspace(1, 0, k)
        if ic+k < len(x): x[ic:ic+k] *= np.linspace(0, 1, k)
    x = x[keep]; sf.write(w, x, SR)
    w2 = tmp / f"{b}_t.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(w),"-af",f"atempo={tempo}","-ar",str(SR),str(w2)],check=True)
    g = -16.0 - lufs(w2); y, _ = sf.read(w2); y = y * 10**(g/20)
    i0 = int(round(p["pos"]*SR)); q = p.get("quem", "MULHER")
    for nome in ("ALL", q):
        if nome not in pistas: pistas[nome] = np.zeros(int(round(DUR*SR)) + SR*2)
        pistas[nome][i0:i0+len(y)] += y
    al = json.load(open(T / f"{b}.alinhamento.json", encoding="utf-8"))
    ch, s, e = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    idx = [i for i in range(len(ch)) if ch[i].isspace() or not any(a <= s[i] < c for a, c in cortes)]
    while idx and ch[idx[0]].isspace(): idx.pop(0)
    while idx and ch[idx[-1]].isspace(): idx.pop()
    if C: C.append(" "); S.append(E[-1]); E.append(E[-1])
    n0 = len(C)
    for i in idx:
        C.append(ch[i]); S.append(round(p["pos"] + mapa(s[i], cortes, tempo), 3)); E.append(round(p["pos"] + mapa(e[i], cortes, tempo), 3))
    tempos.append({"b": b, "quem": q, "texto": "".join(C[n0:]), "ini": S[n0], "fim": E[-1], "fim_audio": round(p["pos"] + len(y)/SR, 3)})
n = int(round(DUR*SR))
for nome, y in pistas.items():
    f = OUT / ("narracao_es.wav" if nome == "ALL" else f"narr_{nome.lower()}.wav")
    sf.write(f, np.clip(y[:n], -1, 1), SR, subtype="PCM_16"); print(f.name, round(n/SR, 3))
(OUT / "narracao_es.alinhamento.json").write_text(json.dumps({"characters":C,"character_start_times_seconds":S,"character_end_times_seconds":E},ensure_ascii=False),encoding="utf-8")
json.dump(tempos, open(OUT / "tempos_reais.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
for t in tempos: print(t["b"], t["quem"], t["ini"], t["fim"], t["fim_audio"], t["texto"][:70])
