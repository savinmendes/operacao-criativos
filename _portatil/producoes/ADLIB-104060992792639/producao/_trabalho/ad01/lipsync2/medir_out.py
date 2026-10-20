# -*- coding: utf-8 -*-
"""Uso: python medir_out.py nome qini parte1.mp4 [parte2.mp4 ...]  (partes consecutivas a partir de qini)
Cola cada parte na base (reamostrando p/ o n de quadros esperado = quadros da entrada crop) e mede o indice."""
import sys, json, cv2, numpy as np, subprocess
from pathlib import Path
import colar as C, medir as Me, fechar as Fe
FECHAR = '--fechar' in sys.argv
if FECHAR: sys.argv.remove('--fechar')
AQ = Path(__file__).parent; AD = AQ.parent
nome, q0, partes = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
seg = {s["nome"]: s for s in json.loads((AD / "segmentos.json").read_text())["segmentos"]}
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); base.set(cv2.CAP_PROP_POS_FRAMES, q0)
out = AQ / "out" / f"full_{nome}.mp4"
pass
FF = lambda: subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-c:v","libx264","-crf","14","-pix_fmt","yuv420p",str(out)], stdin=subprocess.PIPE)

info = []; todos = []
for p in partes:
    p = Path(p); n = int(p.stem.split("_n")[-1]) if "_n" in p.stem else None
    fr = C.ler(p); n = n or len(fr); info.append(f"{p.name}:{len(fr)}->{n}")
    for g in C.reamostrar(fr, n):
        ok, b = base.read(); todos.append(C.colar(b, g))
lg = []
if FECHAR: todos = Fe.fechar(todos, q0, lg); nome += "_F"; out = out.with_name(f"full_{nome}.mp4")
ff = FF()
for f in todos: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait()
ab = Me.aberturas(out)
r = Me.medir(ab, q0)
print(chr(10).join(lg)); print(f"{nome}: idxES={r['idxES']:.2f} idxPT={r['idxPT']:.2f} corrES={r['corrES']:.2f} corrPT={r['corrPT']:.2f} pausaq={r['qpausa']} q={r['q']} det={r['detect']:.0%} | {' '.join(info)}")
