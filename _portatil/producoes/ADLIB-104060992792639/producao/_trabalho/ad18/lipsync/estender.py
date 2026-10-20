# -*- coding: utf-8 -*-
"""Estende um trecho de lipsync alem do fim da saida do HeyGen (quadros onde a boca original ainda fala PT mas o ES
ja acabou): junta a saida (n quadros) + recorte da base nos quadros [b, b+extra) com a ultima caixa, audio ES com
silencio, e passa o fechar_crop.py (boca fechada do proprio trecho nas pausas). Gera out/ls_<seg>_X.mp4 e
caixas_<seg>_X.npy. Uso: python estender.py seg extra"""
import json, sys, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
nm, extra = sys.argv[1], int(sys.argv[2]); s = [x for x in CFG["segs"] if x["nome"] == nm][0]
a = s["a"]
C = np.load(AQ / f"caixas_{nm}.npy"); n = len(C); b = a + n; CX = np.vstack([C, np.repeat(C[-1:], extra, 0)]); np.save(AQ / f"caixas_{nm}_X.npy", CX)
def warp(f, x0, y0, w, h):
    M = np.float32([[720 / w, 0, -x0 * 720 / w], [0, 1280 / h, -y0 * 1280 / h]])
    return cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
ls = cv2.VideoCapture(str(AQ / "out" / f"ls_{nm}.mp4")); base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); base.set(1, b)
tmp = AQ / "out" / f"_tmp_{nm}.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
    "-c:v","libx264","-crf","12","-pix_fmt","yuv420p",str(tmp)], stdin=subprocess.PIPE)
for k in range(n): ok, f = ls.read(); ff.stdin.write(f.tobytes())
for k in range(extra): ok, f = base.read(); ff.stdin.write(warp(f, *C[-1, :4]).tobytes())
ff.stdin.close(); ff.wait()
es = AQ / "out" / f"_es_{nm}.wav"; d = (n + extra) / FPS
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",f"atrim={a/FPS:.4f}:{a/FPS+d:.4f},asetpts=PTS-STARTPTS",
    "-ac","1",str(es)], check=True)
subprocess.run([sys.executable, str(AQ / "fechar_crop.py"), str(tmp), str(es), str(AQ / "out" / f"ls_{nm}_X.mp4"), str(FPS)], check=True)
print("ok", nm, n, "+", extra)
