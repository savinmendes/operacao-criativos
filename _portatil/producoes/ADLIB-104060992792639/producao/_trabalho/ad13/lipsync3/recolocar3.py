# -*- coding: utf-8 -*-
"""v3 AD 13: parte da base_lipsync da v2 (_v2/base_lipsync.mp4: j1, w01, w02, w08, w10 v2, w13) e troca os trechos de
segs.json pela saida speed (recorte) colada na base_sem_legenda so na boca/queixo. Se a saida vier com menos quadros,
REAMOSTRA no tempo (nunca congela). Emenda com trecho vizinho sem corte de camera: crossfade de 2 quadros.
Uso: python recolocar3.py [seg=arquivo[@k] ...]  -> ../base_lipsync.mp4 (30 fps, bt709 tv, sem audio)"""
import json, sys, subprocess, cv2, numpy as np
from pathlib import Path
from comum3 import ler, reamostrar, colar, quadros, ENC_VF, ENC_TAG, desvio_cor, corrigir
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
troca = dict(a.split("=", 1) for a in sys.argv[1:])
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
NT = int(cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")).get(7))
v2 = quadros(AD / "_v2" / "base_lipsync.mp4"); bs = quadros(AD / "base_sem_legenda.mp4")
novo, dono = {}, {}
for s in CFG["segs"]:
    nm = s["nome"]; arq = troca.get(nm, str(AQ / "out" / f"ls_{nm}.mp4")); p, _, k = arq.partition("@")
    g = ler(p, int(k or 0)); m = len(g); n = s["b"] - s["a"]; g = reamostrar(g, n); C = np.load(AQ / f"caixas_{nm}.npy"); dv = desvio_cor(nm, s["a"], AQ, AD); g = corrigir(g, dv)
    print(nm, Path(p).name, m, "->", n, "quadros; desvio de cor BGR", dv.round(2), flush=True)
    for j in range(n): novo[s["a"] + j] = (g[j], C[j]); dono[s["a"] + j] = nm
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(AD / "base_lipsync.mp4")], stdin=subprocess.PIPE)
prev_out = prev_base = None; prev_novo = None; log = []
for i in range(NT):
    fv2 = next(v2); fb = next(bs)
    if i in novo: out = colar(fb, *novo[i])
    else: out = fv2
    eh = dono.get(i)
    if prev_out is not None and eh != prev_novo:   # emenda v2 <-> v3
        corte = np.abs(fb.astype(np.float32) - prev_base).mean() > 10
        if not corte:
            L, R = prev_out.astype(np.float32), out.astype(np.float32)
            prev_out = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); out = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"emenda q{i}: {'corte' if corte else 'crossfade 2q'}")
    if prev_out is not None: ff.stdin.write(prev_out.tobytes())
    prev_out, prev_base, prev_novo = out, fb.astype(np.float32), eh
ff.stdin.write(prev_out.tobytes()); ff.stdin.close(); ff.wait()
print("\n".join(log)); print("ok quadros", NT)
