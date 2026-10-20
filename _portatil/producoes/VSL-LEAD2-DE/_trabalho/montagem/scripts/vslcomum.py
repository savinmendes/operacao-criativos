# -*- coding: utf-8 -*-
import json, subprocess, numpy as np
from pathlib import Path
T = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho")
M = T / "montagem"
BASE = T / "base" / "base_limpa_live.mp4"
W, H, FPS = 720, 960, 30
TL = json.load(open(T / "voz" / "timeline_de.json", encoding="utf-8"))
SEC = TL["secoes_video"]

def novo2orig(tn):
    for s in SEC:
        if s["novo_ini"] - 1e-6 <= tn < s["novo_fim"] + 1e-6:
            return s["src_ini"] + (tn - s["novo_ini"]) / s["fator"]
    s = SEC[-1]
    return s["src_fim"]

READ_VF = f"scale={W}:{H}:in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int+lanczos,format=bgr24"

def ler(p, ss=None, n=None):
    cmd = ["ffmpeg", "-v", "error"]
    if ss is not None: cmd += ["-ss", f"{ss:.4f}"]
    cmd += ["-i", str(p), "-vf", READ_VF, "-fps_mode", "passthrough"]
    if n is not None: cmd += ["-frames:v", str(n)]
    cmd += ["-f", "rawvideo", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    t = W * H * 3; out = []
    while True:
        b = pr.stdout.read(t)
        if len(b) < t: break
        out.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    pr.stdout.close(); pr.wait(); return out
