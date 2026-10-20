# -*- coding: utf-8 -*-
"""Monta ../base_lipsync.mp4 (24 fps, bt709/tv) a partir da base sem legenda:
- cada trecho: saída do HeyGen (out/ls_sNN.mp4, ou plano.json p/ refações) reamostrada no tempo p/ o nº exato de quadros
  e colada só na boca/queixo (colar.py);
- quadros 0-3 (mini-tomada antes do 1º corte, boca PT) = 1º quadro do s01 colado (congelado 4 q, sem fala);
- emendas sem corte de câmera: crossfade de 2 quadros; até o quadro FIM."""
import json, subprocess, sys, cv2, numpy as np
from pathlib import Path
import colar as C
AQ = Path(__file__).parent; AD = AQ.parent
segs = json.loads((AD / "segmentos.json").read_text())["segmentos"]
plano = json.loads((AQ / "plano.json").read_text()) if (AQ / "plano.json").exists() else {}
FIM = int(sys.argv[1]); CANTO = {"s01": None}
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4"))
todos = [base.read()[1] for _ in range(FIM)]
pos = {}
for s in segs:
    nome, a, n = s["nome"], s["quadro_ini"], s["n"]
    p = AQ / plano.get(nome, f"out/ls_{nome}.mp4")
    g = C.ler(p)
    g = C.reamostrar(g[:n] if s["pad"] else g, n)
    col = C.colador(nome, s["caixa"], CANTO.get(nome, (342, 575)))
    for k in range(n):
        q = a + k
        if q < FIM: todos[q] = col(todos[q], g[k])
    print(nome, len(g), flush=True)
for q in range(segs[0]["quadro_ini"]): todos[q] = todos[segs[0]["quadro_ini"]].copy()
orig = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); ob = [orig.read()[1] for _ in range(FIM)]
log = []
for s in segs[1:]:
    a = s["quadro_ini"]
    if a >= FIM: continue
    corte = np.abs(ob[a - 1].astype(np.float32) - ob[a]).mean() > 10
    if not corte:
        L, R = todos[a - 1].astype(np.float32), todos[a].astype(np.float32)
        todos[a - 1] = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); todos[a] = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
    log.append(f"{s['nome']} q{a}: {'corte' if corte else 'crossfade 2q'}")
for f in todos: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("\n".join(log)); print("ok", len(todos))
