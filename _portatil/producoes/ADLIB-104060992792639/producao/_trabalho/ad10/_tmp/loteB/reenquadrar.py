# -*- coding: utf-8 -*-
"""Lote B (compliance): a abertura (q24 0-232, o plano do hospital ate o fim da transicao com brilho) vira um
enquadramento so na personagem: recorte 320x569 em (400,230) ampliado 2,25x (Lanczos). Sai leito, idoso, tubo e
monitores. Aplicado sobre a base JA sincronizada (_antes_loteB/base_lipsync.mp4) -> ../../base_lipsync.mp4.
Tambem gera o original PT recortado igual (lipsync/chk/orig_h0_crop.mp4) para a checagem do h0."""
import cv2, subprocess, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parents[2]
X, Y, W, H, ULT = 400, 230, 320, 569, 232
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def rec(f): return cv2.resize(f[Y:Y + H, X:X + W], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
def proc(src, dst, ate=None, extra=[]):
    cap = cv2.VideoCapture(str(src))
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",*extra,
        "-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,str(dst)], stdin=subprocess.PIPE)
    k = 0
    while True:
        ok, f = cap.read()
        if not ok or (ate is not None and k >= ate): break
        ff.stdin.write((rec(f) if k <= ULT else f).tobytes()); k += 1
    ff.stdin.close(); ff.wait(); return k
print("base", proc(AD / "_antes_loteB" / "base_lipsync.mp4", AD / "base_lipsync.mp4", extra=["-an"]))
o = AD / "lipsync" / "chk" / "orig_h0.mp4"
if o.exists():
    t = AD / "lipsync" / "chk" / "_orig_h0_v.mp4"
    print("orig", proc(o, t, extra=["-an"]))
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(t),"-i",str(o),"-map","0:v","-map","1:a","-c","copy",str(AD/"lipsync"/"chk"/"orig_h0_crop.mp4")],check=True)
    t.unlink()
