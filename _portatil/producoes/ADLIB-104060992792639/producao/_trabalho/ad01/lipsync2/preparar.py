# -*- coding: utf-8 -*-
"""Entrada recortada so no rosto da mulher (sem o Jesus): recorte 288x512 (9:16) em (318,196) da base limpa,
faixa do canto sup. esquerdo (resto de barba/cabelo do Jesus) preenchida com inpaint, escala 2,5x -> 720x1280.
Uso: python preparar.py nome qini qfim audio(pt|none|sil)  -> in/crop_<nome>_<audio>.mp4 e in/es_<nome>.mp3"""
import sys, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent; (AQ / "in").mkdir(exist_ok=True)
X0, Y0, W, H = 318, 196, 288, 512
nome, a, b, aud = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
t0, t1 = a / 30, (b + 1) / 30
m = np.zeros((H, W), np.uint8); m[0:345 - Y0, 0:352 - X0] = 255
cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
out = AQ / "in" / f"crop_{nome}_{aud}.mp4"; tmp = AQ / "in" / f"_v_{nome}.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    "-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p","-color_range","tv","-colorspace","bt709",
    "-color_primaries","bt709","-color_trc","bt709",str(tmp)], stdin=subprocess.PIPE)
for k in range(a, b + 1):
    ok, f = cap.read(); assert ok
    c = cv2.inpaint(np.ascontiguousarray(f[Y0:Y0+H, X0:X0+W]), m, 5, cv2.INPAINT_TELEA)
    ff.stdin.write(cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4).tobytes())
ff.stdin.close(); ff.wait()
if aud == "pt":
    ain = ["-i", str(AD.parent.parent.parent / "UNICOS_HD/01.mp4")]; amap = ["-filter_complex", f"[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]", "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
elif aud == "sil":
    ain = ["-f", "lavfi", "-t", f"{t1-t0}", "-i", "anullsrc=r=48000:cl=stereo"]; amap = ["-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "128k"]
else:
    ain = []; amap = ["-map", "0:v"]
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),*ain,*amap,"-c:v","copy","-shortest" if aud!="none" else "-y",str(out)], check=True)
tmp.unlink()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/"narracao_es.wav"),"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS",
    "-ac","1","-c:a","libmp3lame","-b:a","192k",str(AQ/"in"/f"es_{nome}.mp3")], check=True)
print(out, out.stat().st_size)
