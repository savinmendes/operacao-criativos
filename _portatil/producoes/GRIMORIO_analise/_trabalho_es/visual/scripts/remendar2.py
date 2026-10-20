# -*- coding: utf-8 -*-
"""Troca nas duas bases os quadros refeitos pelo LaMa com a máscara estendida (ext_frames). Na base_visual_es reaplica
o desfoque das regras do compor_visual (detecção no original) e a arroba; quadros do cartão (1452-1810) ficam como estão."""
import sys, subprocess, numpy as np, cv2, os
from pathlib import Path
AQ = Path(__file__).resolve().parent.parent; ORIG = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
src = open(Path(__file__).parent / "compor_visual.py", encoding="utf-8").read()
ns = {"__file__": str(Path(__file__).parent / "compor_visual.py")}; exec(compile(src[:src.index("# ---------- laço ----------")], "cv", "exec"), ns)
IDX = np.load(AQ / "_tmp" / "ext_idx.npy").tolist(); FR = np.load(AQ / "_tmp" / "ext_frames.npy", mmap_mode="r"); P = {k: j for j, k in enumerate(IDX)}
def rd(p, rng): return subprocess.Popen(["ffmpeg","-v","error","-i",p,"-vf",f"scale=in_color_matrix=bt709:in_range={rng}:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
def remendar(nome, visual):
    ent = str(AQ / nome); tmp = str(AQ / ("_r_" + nome)); tv = tmp.replace(".mp4", "_v.mp4")
    d, o = rd(ent, "tv"), rd(ORIG, "full")
    enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
        "-vf","scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",tv],stdin=subprocess.PIPE)
    T = 720*1280*3; i = 0; n = 0
    while True:
        b, bo = d.stdout.read(T), o.stdout.read(T)
        if len(b) < T: break
        f = np.frombuffer(b, np.uint8).reshape(1280,720,3)
        if i in P and not (visual and 1452 <= i <= 1810):
            f = np.array(FR[P[i]]); n += 1
            if visual:
                fo = np.frombuffer(bo, np.uint8).reshape(1280,720,3)
                for a, bb, modo, sig, kw in ns["REGRAS"]:
                    if a <= i <= bb: f = ns["desfocar"](f, ns["TOPO"] if modo == "tudo" else ns["papel"](fo, **kw), sig)
                f, _ = ns["arroba"](f)
        enc.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    subprocess.run(["ffmpeg","-v","error","-y","-i",tv,"-i",ORIG,"-map","0:v","-map","1:a","-c","copy","-movflags","+faststart",tmp],check=True)
    os.remove(tv); os.replace(tmp, ent); print("ok", nome, i, "trocados", n)
if "sem" in sys.argv: remendar("base_sem_legenda.mp4", False)
if "visual" in sys.argv: remendar("base_visual_es.mp4", True)
