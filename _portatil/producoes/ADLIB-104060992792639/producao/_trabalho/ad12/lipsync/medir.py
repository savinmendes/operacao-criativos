# -*- coding: utf-8 -*-
"""Uso: python medir.py AD_DIR nome [arquivo_saida.mp4[@k]] -> cola na base (out/full_<nome>.mp4) e roda checar_lipsync com --rosto."""
import sys, json, subprocess, os, numpy as np
from pathlib import Path
import rosto as R
AD = Path(sys.argv[1]); nome = sys.argv[2]; spec = sys.argv[3] if len(sys.argv) > 3 else f"ls_{nome}.mp4"; k = 0
if "@" in spec: spec, k = spec.split("@"); k = int(k)
s = {x["nome"]: x for x in json.loads((AD / "segmentos.json").read_text())["segmentos"]}[nome]
a, b = s["quadro_ini"], s["quadro_fim"]; n = b - a + 1
O = AD / "lipsync" / "out"; I = AD / "lipsync" / "in"
g = R.ler(O / spec)[k:]; m = len(g); g = R.reamostrar(g, n); bases = R.ler(AD / "base_sem_legenda.mp4", a, n)
geo = np.load(I / f"geo_{nome}.npz"); B, P = geo["B"], geo["P"]
full = O / f"full_{nome}.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-i",str(I / f"es_{nome}.mp3"),
    "-map","0:v","-map","1:a","-c:v","libx264","-crf","14","-threads","4","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(full)], stdin=subprocess.PIPE)
for j in range(n): ff.stdin.write(R.colar(bases[j], g[j], B[j], None if np.isnan(P[j]).any() else P[j]).tobytes())
ff.stdin.close(); ff.wait()
Pv = P[~np.isnan(P).any(axis=(1, 2))]; x0, y0 = Pv[:, :, 0].min(), Pv[:, :, 1].min(); x1, y1 = Pv[:, :, 0].max(), Pv[:, :, 1].max()
ro = f"{int(x0-20)},{int(y0-20)},{int(x1-x0+40)},{int(y1-y0+40)}"
print(f"{nome}: saida {m} quadros -> {n}; rosto {ro}", flush=True)
r = subprocess.run([sys.executable, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py", str(full),
    "--audio-novo", str(I / f"es_{nome}.mp3"), "--original", str(I / f"pt_{nome}.mp4"), "--rosto", ro], capture_output=True, text=True, encoding="utf-8", errors="ignore",
    env=dict(os.environ, PYTHONIOENCODING="utf-8"))
print("\n".join(l for l in r.stdout.splitlines() if l.strip() and not l.startswith(("W0000", "I0000"))))
