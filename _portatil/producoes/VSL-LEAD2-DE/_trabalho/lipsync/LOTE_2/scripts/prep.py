# -*- coding: utf-8 -*-
"""Entradas do lipsync do LOTE 2. Gera in/es_<id>.mp4 (trecho do original esticado pelo fator, audio ES esticado
com atempo; pulpito: recorte 270x360 do rosto ampliado 2x), in/base_<id>.mp4 (quadro inteiro esticado, sem audio,
so p/ colar de volta) e in/de_<id>.mp3 (narracao DE nos tempos da timeline nova). Trecho < 3 s: padding clone."""
import json, subprocess, sys
from pathlib import Path
SRC = r"C:\Users\PICHAU\Downloads\Lead 2.mp4"
NARR = r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\voz\narracao_de_completa.wav"
R = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\lipsync\LOTE_2"); D = R / "in"; D.mkdir(exist_ok=True)
CROP = (245, 10, 270, 360)   # pulpito: rosto ~100 px -> 2x
MIN_Q = 90
d = json.load(open(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\voz\lotes.json", encoding="utf-8"))
so = set(sys.argv[1:]); plano = []
for x in d["trechos"]:
    if x["lote"] != 2 or (so and x["id"] not in so): continue
    q0, q1 = round(x["novo_ini"] * 30), round(x["novo_fim"] * 30); N = q1 - q0; NP = max(N, MIN_Q)
    oi, od, f = x["orig_ini"], x["orig_fim"] - x["orig_ini"], x["fator"]
    pad = NP - N
    vf = f"setpts=(PTS-STARTPTS)*{f},fps=30"
    if pad: vf += f",tpad=stop_mode=clone:stop={pad + 30}"
    vf += f",trim=end_frame={NP},setpts=PTS-STARTPTS"
    vcrop = vf + (",crop=%d:%d:%d:%d,scale=%d:%d:flags=lanczos" % (CROP[2], CROP[3], CROP[0], CROP[1], CROP[2]*2, CROP[3]*2) if x["cena"] == "padre_pulpito" else "")
    T = NP / 30
    af = f"asetpts=PTS-STARTPTS,atempo={1/f:.6f},apad,atrim=0:{T:.4f}"
    i = x["id"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{oi:.3f}", "-t", f"{od + 0.5:.3f}", "-i", SRC,
        "-filter_complex", f"[0:v]{vcrop}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "14",
        "-preset", "medium", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
        "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", str(D / f"es_{i}.mp4")], check=True)
    if x["cena"] == "padre_pulpito":
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{oi:.3f}", "-t", f"{od + 0.5:.3f}", "-i", SRC, "-vf", vf, "-an",
            "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
            "-color_primaries", "bt709", "-color_trc", "bt709", str(D / f"base_{i}.mp4")], check=True)
    t0 = q0 / 30
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", NARR, "-af", f"atrim={t0:.5f}:{q1/30:.5f},asetpts=PTS-STARTPTS,apad,atrim=0:{T:.4f}",
        "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(D / f"de_{i}.mp3")], check=True)
    n = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries",
        "stream=nb_read_frames", "-of", "csv=p=0", str(D / f"es_{i}.mp4")]))
    plano.append({"id": i, "cena": x["cena"], "q0": q0, "q1": q1, "N": N, "NP": NP, "quadros_in": n,
                  "crop": list(CROP) if x["cena"] == "padre_pulpito" else None})
    print(i, x["cena"], N, NP, n, "OK" if n == NP else "!!", flush=True)
if not so: json.dump(plano, open(R / "plano.json", "w"), indent=1)
