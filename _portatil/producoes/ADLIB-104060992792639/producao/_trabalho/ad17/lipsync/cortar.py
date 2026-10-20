# -*- coding: utf-8 -*-
"""Entrada do HeyGen: recorte que segue o rosto da mulher (caixas_<seg>.npy), escalado para 720x1280, da base sem legenda,
com o AUDIO ORIGINAL PT do trecho; o espanhol sai separado (es_<seg>.mp3). Trechos < 3 s completados com o ultimo quadro
(e silencio). Uso: python lipsync/cortar.py [seg ...]"""
import json, sys, subprocess, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
SRC = CFG.get("src", "../../../UNICOS_HD/17.mp4")
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
def warp(f, x0, y0, w, h):
    M = np.float32([[720 / w, 0, -x0 * 720 / w], [0, 1280 / h, -y0 * 1280 / h]])
    return cv2.warpAffine(f, M, (720, 1280), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
alvo = set(sys.argv[1:])
for s in CFG["segs"]:
    if alvo and s["nome"] not in alvo: continue
    a, b, nm = s["a"], s["b"], s["nome"]; n = b - a; npad = max(n, int(3.05 * FPS) + 1)
    C = np.load(AQ / s.get("cx", f"caixas_{nm}.npy"))
    cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
    tmp = AQ / "in" / f"_v_{nm}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-threads","4","-c:v","libx264","-crf","13","-preset","medium","-pix_fmt","yuv420p",*COR,str(tmp)], stdin=subprocess.PIPE)
    last = None
    for k in range(npad):
        if k < n:
            ok, f = cap.read(); assert ok, (nm, k)
            x0, y0, w, h = C[k, :4]; last = warp(f, x0, y0, w, h)
        ff.stdin.write(last.tobytes())
    ff.stdin.close(); ff.wait()
    t0, d, dp = a / FPS, n / FPS, npad / FPS
    out = AQ / "in" / f"pt_{nm}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",SRC,"-filter_complex",
        f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={dp:.4f}[a]","-map","0:v","-map","[a]",
        "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dp:.4f}",str(out)], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",
        f"atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={dp:.4f}","-t",f"{dp:.4f}",
        "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / f"es_{nm}.mp3")], check=True)
    print(nm, n, "->", npad, out.stat().st_size, flush=True)
