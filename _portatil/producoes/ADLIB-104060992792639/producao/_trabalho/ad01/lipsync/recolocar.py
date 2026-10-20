# -*- coding: utf-8 -*-
"""Recoloca os trechos com lipsync (ls_sNN.mp4) na base_sem_legenda.mp4, quadro a quadro (30 fps).
Do lipsync vem só a parte de cima (rosto); a faixa da legenda (y>=800) continua a da base limpa,
com transição suave em y 760-800. Saída: ../base_lipsync.mp4 (sem áudio, cor bt709 tv)."""
import json, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
seg = json.loads((AD / "segmentos.json").read_text())["segmentos"]
w = np.zeros((1280, 1, 1), np.float32); w[800:] = 1; w[760:800, 0, 0] = np.linspace(0, 1, 40)
mapa = {}
for s in seg:
    p = AQ / f"ls_{s['nome']}.mp4"
    if p.exists(): mapa[s["nome"]] = (s, p)
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4"))
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
cur = None; i = 0; trocados = 0
while True:
    ok, f = base.read()
    if not ok: break
    s = next((v for v in mapa.values() if v[0]["quadro_ini"] <= i <= v[0]["quadro_fim"]), None)
    if s:
        if cur is None or cur[0] != s[0]["nome"]:
            cur = (s[0]["nome"], cv2.VideoCapture(str(s[1]))); ultimo = None
        ok2, g = cur[1].read()
        if ok2: ultimo = g
        g = ultimo if ultimo is not None else f
        if g.shape != f.shape: g = cv2.resize(g, (720, 1280), interpolation=cv2.INTER_LANCZOS4)
        f = np.clip(g * (1 - w) + f * w, 0, 255).astype(np.uint8); trocados += 1
    ff.stdin.write(f.tobytes()); i += 1
ff.stdin.close(); ff.wait()
print("ok quadros", i, "com lipsync", trocados, "trechos", sorted(mapa))
