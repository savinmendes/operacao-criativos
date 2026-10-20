# -*- coding: utf-8 -*-
"""Rua sem a mulher antiga: LaMa (GPU) por quadro na região do PiP com w/velha.npy -> w/rua.mp4 (0..N, 720x1280, bt601 fixo).
Uso: _vg python lama_rua.py"""
import sys, warnings; warnings.filterwarnings("ignore")
import numpy as np, cv2, subprocess
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_VF, ENC_TAG
from PIL import Image
from simple_lama_inpainting import SimpleLama
from pathlib import Path
AQ = Path(__file__).resolve().parent; BASE = AQ.parents[2] / "_trabalho" / "lama" / "base_limpa.mp4"
M = np.load(AQ / "w" / "velha.npy"); N = len(M); lama = SimpleLama()
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                       *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, "-an", str(AQ / "w" / "rua.mp4")], stdin=subprocess.PIPE)
A0, A1, B1 = 300, 1232, 520          # recorte y0:y1, x0:x1 p/ LaMa (múltiplos de 8)
for q, f in enumerate(quadros(str(BASE), 0, N)):
    crop = f[A0:A1, :B1].copy(); mk = (M[q][A0:A1, :B1] * 255).astype(np.uint8)
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    o = f.copy(); sel = M[q][A0:A1, :B1] > 0; o[A0:A1, :B1][sel] = r[sel]
    ff.stdin.write(np.ascontiguousarray(o).tobytes())
    if q % 20 == 0: print(q, flush=True)
ff.stdin.close(); ff.wait(); print("ok", N)
