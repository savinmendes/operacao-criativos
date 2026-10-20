# -*- coding: utf-8 -*-
"""Monta o EN 02 UK: original quadro a quadro (cor exata, comum3) + boca/queixo do HeyGen nos trechos A e B
(caixas_<seg>.npy, correcao de desvio de cor medida fora da boca) + painel de avaliacoes sem "United States"
(painel.py) + trilha audio_uk.wav. Crossfade de 2 quadros nas emendas sem corte de camera."""
import subprocess, json, cv2, numpy as np
from pathlib import Path
from comum3 import quadros, ler, reamostrar, colar, ENC_VF, ENC_TAG
import painel as P
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 02 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA.mp4"
DST = AQ.parent.parent.parent / "UK" / "EN 02 - ENZIMAS-TRUQUE-6-MESES-GRAVIDA - UK.mp4"
SEGS = [("A", 1611, 1702), ("B", 3341, 3600)]
NT = 3600
def desvio(nm, g):
    """media (entrada recortada - saida HeyGen) fora da regiao da boca, em quadros amostrados"""
    e = list(quadros(AQ / "in" / f"orig_{nm}.mp4"))
    d = []
    for k in range(0, len(g), 10):
        a, b = e[k].astype(np.float32), g[k].astype(np.float32)
        d.append(np.concatenate([(a - b)[60:300].reshape(-1, 3), (a - b)[1000:1240].reshape(-1, 3)]).mean(0))
    return np.median(d, 0)
novo = {}
for nm, a, b in SEGS:
    g = ler(AQ / "out" / f"ls_{nm}.mp4"); n = b - a; m = len(g); g = reamostrar(g, n)
    dv = desvio(nm, g); g = [np.clip(f.astype(np.float32) + dv, 0, 255).astype(np.uint8) for f in g]
    C = np.load(AQ / f"caixas_{nm}.npy")
    print(nm, m, "->", n, "quadros; desvio de cor BGR", dv.round(2), flush=True)
    for j in range(n): novo[a + j] = (g[j], C[j], nm)
DST.parent.mkdir(exist_ok=True)
tmp = AQ / "video_uk_sem_audio.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","18","-preset","slow","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(tmp)], stdin=subprocess.PIPE)
prev_out = prev_base = prev_dono = None; log = []
for i, fb in enumerate(quadros(SRC)):
    if i in novo:
        g, c, dono = novo[i]; out = colar(fb, g, c)
    else:
        out = fb; dono = None
    if P.Q0 <= i < P.Q1:
        out = out.copy(); out[P.Y0 - 1:P.Y1 + 1, P.X0 - 1:P.X1 + 1] = fb[P.Y0 - 1:P.Y1 + 1, P.X0 - 1:P.X1 + 1]
        out, _ = P.limpar(out)
    if prev_out is not None and dono != prev_dono:
        corte = np.abs(fb.astype(np.float32) - prev_base).mean() > 10
        if not corte:
            L, R = prev_out.astype(np.float32), out.astype(np.float32)
            prev_out = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); out = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"emenda q{i} ({i/30:.2f}s): {'corte' if corte else 'crossfade 2q'}")
    if prev_out is not None: ff.stdin.write(prev_out.tobytes())
    prev_out, prev_base, prev_dono = out, fb.astype(np.float32), dono
ff.stdin.write(prev_out.tobytes()); ff.stdin.close(); ff.wait()
print("\n".join(log), "| quadros", i + 1)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "audio_uk.wav"),"-map","0:v","-map","1:a","-c:v","copy",
    "-c:a","aac","-b:a","128k","-ar","44100","-movflags","+faststart",str(DST)], check=True)
print("ok", DST, DST.stat().st_size)
