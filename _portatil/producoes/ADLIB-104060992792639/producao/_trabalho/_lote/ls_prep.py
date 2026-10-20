# -*- coding: utf-8 -*-
"""Prepara as entradas do lipsync HeyGen. Uso (na pasta adNN): python ls_prep.py lipsync/segs.json [nome ...]
segs.json: {"orig": "../../../UNICOS_HD/NN.mp4", "base": "base_sem_legenda.mp4", "narr": "narracao_es.wav",
  "segs": [{"nome": "s1", "q0": 0, "q1": 140, "crop": null | [x, y, w, h] (9:16), "cola": [cx, cy, ax, ay]}]}
Gera lipsync/in/pt_<nome>.mp4 (video da base, recortado/escalado p/ 720x1280 se crop, com o AUDIO ORIGINAL PT)
e lipsync/in/es_<nome>.mp3 (narracao ES do mesmo intervalo). q1 inclusivo."""
import sys, json, subprocess
from pathlib import Path
cfg = json.load(open(sys.argv[1], encoding="utf-8")); so = set(sys.argv[2:])
D = Path("lipsync/in"); D.mkdir(parents=True, exist_ok=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
for s in cfg["segs"]:
    if so and s["nome"] not in so: continue
    q0, q1 = s["q0"], s["q1"]; t0, t1 = q0 / 30, (q1 + 1) / 30
    vf = r"select='between(n\,%d\,%d)',setpts=N/30/TB" % (q0, q1)
    if s.get("crop"):
        x, y, w, h = s["crop"]; vf += f",crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    out = D / f"pt_{s['nome']}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",cfg["base"],"-i",cfg["orig"],"-filter_complex",
        f"[0:v]{vf}[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]","-map","[v]","-map","[a]","-r","30",
        "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-threads","4","-c:a","aac","-b:a","192k",str(out)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",cfg["narr"],"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS","-ac","1",
        "-c:a","libmp3lame","-b:a","192k",str(D / f"es_{s['nome']}.mp3")],check=True)
    n = int(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v","-show_entries","stream=nb_read_frames","-of","csv=p=0",str(out)]))
    print(s["nome"], f"{t0:.3f}-{t1:.3f}s", "quadros", n, "esperado", q1 - q0 + 1, out.stat().st_size)
