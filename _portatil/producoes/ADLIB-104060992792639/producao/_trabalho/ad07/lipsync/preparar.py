# -*- coding: utf-8 -*-
"""Entrada do HeyGen recortada só no rosto da Desatadora (Jesus fora / canto inpaint), escala p/ 720x1280, 24 fps,
com o ÁUDIO ORIGINAL PT do trecho; o ES vai separado (es_sNN.mp3). Trechos < 3 s são completados com o último quadro.
Uso: python preparar.py [sNN ...]"""
import sys, json, subprocess, cv2, numpy as np
from pathlib import Path
from segs import SEGS, FPS
AQ = Path(__file__).parent; AD = AQ.parent; SRC = AD.parent.parent.parent / "UNICOS_HD/07.mp4"
(AQ / "in").mkdir(exist_ok=True)
def caixa(k):
    if k == 8 and "--grande" in sys.argv: return (262, 330, 324, 576, (342, 575))
    # (x0, y0, w, h, canto_jesus) canto = (x1, y1) em px da base a apagar (x < x1 e y < y1)
    if k == 1: return (330, 300, 270, 480, None)
    return (290, 360, 270, 480, (342, 575))
def gerar(k):
    a, b = SEGS[k - 1]; nome = f"s{k:02d}"; X0, Y0, W, H, canto = caixa(k)
    m = np.zeros((H, W), np.uint8)
    if canto: m[0:canto[1] - Y0, 0:canto[0] - X0] = 255
    cap = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); cap.set(cv2.CAP_PROP_POS_FRAMES, a)
    n = b - a + 1; npad = max(0, int(np.ceil(3.0 * FPS)) - n) + (3 if n < 72 else 0)
    tmp = AQ / "in" / f"_v_{nome}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-",
        "-threads","4","-c:v","libx264","-crf","12","-preset","slow","-pix_fmt","yuv420p","-color_range","tv","-colorspace","bt709",
        "-color_primaries","bt709","-color_trc","bt709",str(tmp)], stdin=subprocess.PIPE)
    last = None
    for q in range(a, b + 1):
        ok, f = cap.read(); assert ok
        c = np.ascontiguousarray(f[Y0:Y0+H, X0:X0+W])
        if canto: c = cv2.inpaint(c, m, 5, cv2.INPAINT_TELEA)
        last = cv2.resize(c, (720, 1280), interpolation=cv2.INTER_LANCZOS4); ff.stdin.write(last.tobytes())
    for _ in range(npad): ff.stdin.write(last.tobytes())
    ff.stdin.close(); ff.wait()
    t0 = a / FPS; dur = (n + npad) / FPS; t1r = (b + 1) / FPS
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(SRC),"-filter_complex",
        f"[1:a]atrim={t0}:{t1r},asetpts=PTS-STARTPTS,apad=whole_dur={dur}[a]","-map","0:v","-map","[a]",
        "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{dur}",str(AQ / "in" / (f"pt_{nome}" + ("g" if "--grande" in sys.argv else "") + ".mp4"))], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",
        f"atrim={t0}:{t1r},asetpts=PTS-STARTPTS,apad=whole_dur={dur}","-ac","1","-c:a","libmp3lame","-b:a","192k",
        str(AQ / "in" / f"es_{nome}.mp3")], check=True)
    print(nome, a, b, n, "pad", npad, flush=True)
    return {"nome": nome, "quadro_ini": a, "quadro_fim": b, "n": n, "pad": npad, "caixa": [X0, Y0, W, H]}
so = [a for a in sys.argv[1:] if not a.startswith("--")]
segs = []
for k in range(1, len(SEGS) + 1):
    if so and f"s{k:02d}" not in so: continue
    segs.append(gerar(k))
if not so: json.dump({"fps": FPS, "segmentos": segs}, open(AD / "segmentos.json", "w"), indent=1)
