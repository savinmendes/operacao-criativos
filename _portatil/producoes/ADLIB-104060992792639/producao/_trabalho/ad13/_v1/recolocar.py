# -*- coding: utf-8 -*-
"""Recoloca os segmentos com lipsync na base_sem_legenda.mp4, quadro a quadro (30 fps).
Uso: python recolocar.py [nome=arquivo ...]  (segmento sem arquivo -> usa o original)
Saída: ../base_lipsync.mp4 (sem áudio, cor bt709 tv)."""
import json, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).parent
AD = AQUI.parent
seg = json.loads((AD / "segmentos.json").read_text(encoding="utf-8"))
NTOT = 3613
troca = dict(a.split("=", 1) for a in sys.argv[1:])

COR = ["-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
ins = ["-i", str(AD / "base_sem_legenda.mp4")]
fc, partes = [], []
cursor, k = 0, 0
norm = "scale=720:1280:flags=lanczos,setsar=1,format=yuv420p"
for s in seg["segmentos"]:
    a, b = s["quadro_ini"], s["quadro_fim"] + 1      # [a, b)
    nome = Path(s["arquivo"]).stem.replace("seg_", "")
    if a > cursor:
        fc.append(f"[0:v]trim=start_frame={cursor}:end_frame={a},setpts=PTS-STARTPTS,{norm}[p{k}]")
        partes.append(f"[p{k}]"); k += 1
    n = b - a
    if nome in troca:
        idx = len(ins) // 2
        ins += ["-i", troca[nome]]
        fc.append(f"[{idx}:v]fps=30,setpts=PTS-STARTPTS,{norm},tpad=stop_mode=clone:stop_duration=1,"
                  f"trim=end_frame={n},setpts=PTS-STARTPTS[p{k}]")
    else:
        fc.append(f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,{norm}[p{k}]")
    partes.append(f"[p{k}]"); k += 1
    cursor = b
if cursor < NTOT:
    fc.append(f"[0:v]trim=start_frame={cursor}:end_frame={NTOT},setpts=PTS-STARTPTS,{norm}[p{k}]")
    partes.append(f"[p{k}]"); k += 1
fc.append("".join(partes) + f"concat=n={len(partes)}:v=1:a=0,setparams=range=tv:colorspace=bt709:color_primaries=bt709:color_trc=bt709[v]")
out = AD / "base_lipsync.mp4"
cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-r", "30",
       "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-pix_fmt", "yuv420p", *COR, "-an", str(out)]
subprocess.run(cmd, check=True)
r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=nb_read_frames,duration",
                    "-of", "csv=p=0", str(out)], capture_output=True, text=True).stdout.strip()
print("ok", out, r)
