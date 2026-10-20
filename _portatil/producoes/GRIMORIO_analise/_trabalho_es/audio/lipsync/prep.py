# -*- coding: utf-8 -*-
"""Entradas do lipsync: in/pt_<nome>.mp4 (vídeo recortado no rosto, com o ÁUDIO ORIGINAL PT) + in/es_<nome>.mp3 (voz ES do mesmo trecho).
uso: python prep.py <video_base> nome [nome...]"""
import sys, json, subprocess
from pathlib import Path
AQ = Path(__file__).resolve().parent
ORIG = r"C:\Users\PICHAU\Downloads\GRIMORIO V2.mp4"
base = sys.argv[1]; so = set(sys.argv[2:])
C = json.load(open(AQ / "segs.json", encoding="utf-8"))
IN = "scale=in_color_matrix=bt709:in_range=full:out_color_matrix=bt709:out_range=tv:flags=accurate_rnd+full_chroma_int"
for s in C["segs"]:
    if so and s["nome"] not in so: continue
    q0, q1 = s["q0"], s["q1"]; t0, t1 = q0 / 30, (q1 + 1) / 30
    vf = r"select='between(n\,%d\,%d)',setpts=N/30/TB" % (q0, q1)
    if s.get("crop"):
        x, y, w, h = s["crop"]; vf += f",crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos"
    vf += "," + IN + ",format=yuv420p"
    out = AQ / "in" / f"pt_{s['nome']}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-i", ORIG, "-filter_complex",
                    f"[0:v]{vf}[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]", "-map", "[v]", "-map", "[a]", "-r", "30",
                    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-color_range", "tv", "-colorspace", "bt709",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-threads", "4", "-c:a", "aac", "-b:a", "192k", str(out)], check=True)
    o = s.get("es_off", 0)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(AQ.parent / "voz_es.wav"), "-af", f"atrim={t0 + o}:{t1 + o},asetpts=PTS-STARTPTS",
                    "-ac", "1", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", str(AQ / "in" / f"es_{s['nome']}.mp3")], check=True)
    n = int(subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(out)]))
    print(s["nome"], f"{t0:.3f}-{t1:.3f}", "quadros", n, "esperado", q1 - q0 + 1, out.stat().st_size, (AQ / "in" / f"es_{s['nome']}.mp3").stat().st_size)
