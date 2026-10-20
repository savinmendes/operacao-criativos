# -*- coding: utf-8 -*-
"""Remendo final nas duas bases: quadros 4554-4644 (fim, luz dourada) trocados pelo LaMa com máscara retangular;
na base_visual_es também a arroba nesses quadros e desfoque leve das traduções na fusão do cartão (1796-1810)."""
import sys, subprocess, numpy as np, cv2, os
from pathlib import Path
AQ = Path(__file__).resolve().parent.parent
ORIG = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
FIM = np.load(AQ / "_tmp" / "fim_frames.npy"); A = 4554
RI = np.load(AQ / "_tmp" / "residuos_idx.npy").tolist(); RF = np.load(AQ / "_tmp" / "residuos_frames.npy", mmap_mode="r"); RP = {k: j for j, k in enumerate(RI)}
src = open(Path(__file__).parent / "compor_visual.py", encoding="utf-8").read()
ns = {"__file__": str(Path(__file__).parent / "compor_visual.py")}; exec(compile(src[:src.index("# ---------- desfoques ----------")], "cv", "exec"), ns)
arroba = ns["arroba"]
def remendar(nome, visual):
    ent = str(AQ / nome); tmp = str(AQ / ("_r_" + nome)); tv = tmp.replace(".mp4", "_v.mp4")
    dec = subprocess.Popen(["ffmpeg","-v","error","-i",ent,"-vf","scale=in_color_matrix=bt709:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
        "-vf","scale=out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p",
        "-c:v","libx264","-crf","12","-preset","medium","-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",tv],stdin=subprocess.PIPE)
    T = 720*1280*3; i = 0
    while True:
        b = dec.stdout.read(T)
        if len(b) < T: break
        f = np.frombuffer(b, np.uint8).reshape(1280,720,3)
        if i >= A:
            f = FIM[i - A].copy()
            if visual: f, _ = arroba(f)
        elif i in RP:
            f = np.array(RF[RP[i]])
            if visual: f, _ = arroba(f)
        elif visual and "desf" in sys.argv and 1796 <= i <= 1810:
            f = f.copy(); y0, y1, x0, x1 = 400, 905, 362, 630
            m = np.zeros((1280,720), np.float32); m[y0:y1, x0:x1] = 1; m = cv2.GaussianBlur(m, (0,0), 6)[..., None]
            bl = cv2.GaussianBlur(f, (0,0), 3.5)
            f = np.clip(bl*m + f*(1-m), 0, 255).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
    enc.stdin.close(); enc.wait()
    subprocess.run(["ffmpeg","-v","error","-y","-i",tv,"-i",ORIG,"-map","0:v","-map","1:a","-c","copy","-movflags","+faststart",tmp],check=True)
    os.remove(tv); os.replace(tmp, ent); print("ok", nome, i)
import sys as _s
if "sem" in _s.argv: remendar("base_sem_legenda.mp4", False)
if "visual" in _s.argv: remendar("base_visual_es.mp4", True)
