# -*- coding: utf-8 -*-
"""Upscale 2x (Real-ESRGAN animevideov3, mesmo motor do kit upscale_video.py) -> 720x1280, cor bt601/tv FIXA.
Uso: python upscale720.py entrada.mp4 saida.mp4 [--ss 0] [--t N] [--crop W:H:X:Y]
Le os quadros com in_color_matrix=bt601 e grava com out_color_matrix=bt601 + etiqueta bt709 (armadilha da cor do CLAUDE.md).
Saida sem audio, 30 fps, crf 12 (intermediario)."""
import argparse, shutil, subprocess, tempfile, time
from pathlib import Path
import cv2, numpy as np

RE = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\_ferramentas_extras\realesrgan\realesrgan-ncnn-vulkan.exe")
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]

ap = argparse.ArgumentParser()
ap.add_argument("entrada"); ap.add_argument("saida")
ap.add_argument("--ss", type=float, default=0.0); ap.add_argument("--t", type=float, default=None)
ap.add_argument("--crop", default=None)
a = ap.parse_args()
wk = Path(tempfile.mkdtemp(prefix="up720_")); fin, fout = wk / "in", wk / "out"; fin.mkdir(); fout.mkdir()
vf = (f"crop={a.crop}," if a.crop else "") + "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=rgb24"
cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a.ss:.3f}", "-i", a.entrada]
if a.t: cmd += ["-t", f"{a.t:.3f}"]
cmd += ["-vf", vf, "-fps_mode", "passthrough", str(fin / "%05d.png")]
t0 = time.time(); subprocess.run(cmd, check=True)
n = len(list(fin.glob("*.png"))); print(f"{n} quadros extraidos", flush=True)
subprocess.run([str(RE), "-i", str(fin), "-o", str(fout), "-n", "realesr-animevideov3", "-s", "2", "-f", "png"], check=True, capture_output=True)
print(f"realesrgan ok {time.time()-t0:.0f}s", flush=True)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30", "-i", "-",
                       "-an", *ENC_VF, "-c:v", "libx264", "-crf", "12", "-preset", "medium", *ENC_TAG, a.saida], stdin=subprocess.PIPE)
for p in sorted(fout.glob("*.png")):
    f = cv2.imread(str(p)).astype(np.float32); f = cv2.resize(f, (720, 1280), interpolation=cv2.INTER_AREA)
    o = cv2.resize(cv2.imread(str(fin / p.name)).astype(np.float32), (720, 1280), interpolation=cv2.INTER_CUBIC)
    # o Real-ESRGAN clareia ~2-3 niveis: troca a baixa frequencia pela do original (mantem o detalhe novo)
    f = np.clip(f - cv2.GaussianBlur(f, (0, 0), 6) + cv2.GaussianBlur(o, (0, 0), 6), 0, 255).astype(np.uint8)
    ff.stdin.write(np.ascontiguousarray(f).tobytes())
ff.stdin.close(); ff.wait(); shutil.rmtree(wk, ignore_errors=True)
print(f"ok {a.saida} {n} quadros {time.time()-t0:.0f}s", flush=True)
