# -*- coding: utf-8 -*-
"""Normaliza b-rolls: 720x1280, 30 fps, yuv420p com pixels em matriz bt601/tv (convencao do projeto: etiqueta bt709/tv
so no bitstream, igual ao comum3.ENC_TAG), sem audio.
modos: video (trecho de mp4) | kb (imagem parada com Ken Burns) | png (tela estática com zoom lento, ex. print)"""
import subprocess, json, sys
from pathlib import Path
TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
ENC = ["-c:v", "libx264", "-crf", "14", "-preset", "slow", "-pix_fmt", "yuv420p", "-an", "-movflags", "+faststart"]
def run(c):
    r = subprocess.run(c, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode: print(" ".join(c)); print(r.stderr[-2000:]); sys.exit(1)
def probe_cs(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=color_space", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return r.stdout.strip()
def video(src, out, a, b, matriz_in=None, vel=1.0, crop=None):
    """matriz_in: None = mantém os valores YUV (fonte já na convenção bt601); 'bt709' = converte bt709->bt601"""
    vf = []
    vf.append(f"crop={crop}" if crop else "crop='min(iw,ih*9/16)':'min(ih,iw*16/9)'")
    if vel != 1.0: vf.append(f"setpts=PTS/{vel}")
    if matriz_in:
        vf.append(f"scale=720:1280:flags=lanczos+accurate_rnd+full_chroma_int:in_color_matrix={matriz_in}:out_color_matrix=bt601:in_range=tv:out_range=tv")
    else:
        vf.append("scale=720:1280:flags=lanczos+accurate_rnd+full_chroma_int")
    vf += ["fps=30", "format=yuv420p"]
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-to", f"{b:.3f}", "-i", str(src), "-vf", ",".join(vf), *ENC, *TAG, str(out)])
def kb(img, out, dur, z0=1.0, z1=1.12, x0=0.5, y0=0.5, x1=0.5, y1=0.5):
    """Ken Burns: zoom de z0 a z1 e centro (x,y relativos) interpolado; RGB->YUV em bt601"""
    n = int(round(dur * 30))
    zexp = f"({z0}+({z1}-{z0})*on/{n - 1})"
    xc = f"({x0}+({x1}-{x0})*on/{n - 1})"; yc = f"({y0}+({y1}-{y0})*on/{n - 1})"
    vf = (f"crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=2160:3840:flags=lanczos,zoompan=z='{zexp}':x='iw*{xc}-iw/zoom/2':y='ih*{yc}-ih/zoom/2':d={n}:s=720x1280:fps=30,"
          "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", str(img), "-vf", vf, "-frames:v", str(n), *ENC, *TAG, str(out)])
if __name__ == "__main__":
    pass
