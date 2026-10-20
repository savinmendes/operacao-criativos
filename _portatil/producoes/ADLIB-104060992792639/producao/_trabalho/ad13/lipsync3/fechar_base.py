# -*- coding: utf-8 -*-
"""Plano B sem credito nos trechos que nao foram refeitos (j1, w13): recorta [a,b) da base_lipsync.mp4, roda o fechar3.py
(boca fechada da propria tomada nas pausas do ES) e devolve os quadros na base_lipsync.mp4.
Uso: python fechar_base.py nome a b cortes_locais janela [esq]"""
import sys, subprocess, cv2, os
from comum3 import quadros, ENC_VF, ENC_TAG
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
nm, a, b, cortes, jan = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]; esq = sys.argv[6:] 
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
clip = AQ / "out" / f"base_{nm}.mp4"; es = AQ / "out" / f"es_{nm}.wav"; fx = AQ / "out" / f"base_{nm}_F.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "base_lipsync.mp4"),"-vf",f"trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS","-an","-c:v","libx264","-crf","10","-threads","4",str(clip)], check=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",f"atrim={a/30:.4f}:{b/30:.4f},asetpts=PTS-STARTPTS","-ac","1",str(es)], check=True)
subprocess.run([sys.executable, str(AQ / "fechar3.py"), str(clip), str(es), str(fx), "30", cortes, jan, *esq], check=True, env=dict(os.environ, PYTHONIOENCODING="utf-8"))
n = int(cv2.VideoCapture(str(AD / "base_lipsync.mp4")).get(7)); src = quadros(AD / "base_lipsync.mp4"); g = quadros(fx)
tmp = AD / "base_lipsync_tmp.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",*ENC_VF,"-threads","4","-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(tmp)], stdin=subprocess.PIPE)
for i in range(n):
    f = next(src)
    if a <= i < b:
        f2 = next(g, None)
        if f2 is not None: f = f2
    ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); src.close(); os.replace(tmp, AD / "base_lipsync.mp4"); print("ok", nm, a, b, n)
