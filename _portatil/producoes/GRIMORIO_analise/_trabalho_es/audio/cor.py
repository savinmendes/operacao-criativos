# -*- coding: utf-8 -*-
"""Leitura/gravação de quadros com matriz FIXA (bt709 + faixa da etiqueta do arquivo; a saída sai bt709 full como o original).
Mesma matriz na ida e na volta -> sem deriva de cor a cada passada."""
import subprocess, json, numpy as np
def info(p):
    o = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
        "stream=width,height,r_frame_rate,color_range,pix_fmt", "-of", "json", str(p)], capture_output=True, text=True).stdout)["streams"][0]
    full = o.get("color_range") == "pc" or o.get("pix_fmt", "").startswith("yuvj")
    a, b = o["r_frame_rate"].split("/")
    return int(o["width"]), int(o["height"]), int(a) / int(b), full
def vf_ler(full):
    return f"scale=in_color_matrix=bt709:in_range={'full' if full else 'limited'}:flags=accurate_rnd+full_chroma_int+bitexact,format=rgb24"
def ler(p, q0=None, q1=None):
    w, h, f, full = info(p)
    sel = (r"select='between(n\,%d\,%d)'," % (q0, q1)) if q0 is not None else ""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", sel + vf_ler(full), "-fps_mode", "passthrough",
                        "-f", "rawvideo", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, h, w, 3)
VF_ESC = "scale=out_color_matrix=bt709:out_range=full:flags=accurate_rnd+full_chroma_int+bitexact,format=yuvj420p"
TAGS = ["-color_range", "pc", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
def escritor(dest, w=720, h=1280, fps=30, crf=10, preset="medium"):
    return subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}", "-r", str(fps), "-i", "-",
                             "-vf", VF_ESC, "-c:v", "libx264", "-crf", str(crf), "-preset", preset, *TAGS, str(dest)], stdin=subprocess.PIPE)
