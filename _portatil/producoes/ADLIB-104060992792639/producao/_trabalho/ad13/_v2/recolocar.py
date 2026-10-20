# -*- coding: utf-8 -*-
"""Recoloca os segmentos com lipsync na base_sem_legenda.mp4, quadro a quadro (30 fps).
Uso: python recolocar.py [nome=arquivo[@k] ...]  (segmento sem arquivo -> usa o original)
  @k descarta os k primeiros quadros da saida do HeyGen (quadro solto).
  v2: se o trecho voltar com m != n quadros, ele e REAMOSTRADO no tempo (setpts*n/m + fps=30 + trim exato),
  em vez de congelar o ultimo quadro.
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
        arq, _, pula = troca[nome].partition("@")
        pula = int(pula or 0)
        idx = len(ins) // 2
        ins += ["-i", arq]
        m = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                                "stream=nb_read_frames", "-of", "csv=p=0", arq], capture_output=True, text=True).stdout.strip()) - pula
        print(nome, "quadros", m, "->", n, f"(pula {pula})" if pula else "")
        fc.append(f"[{idx}:v]fps=30,trim=start_frame={pula},setpts=(PTS-STARTPTS)*{n}/{m},fps=30,{norm},"
                  f"tpad=stop_mode=clone:stop=2,trim=end_frame={n},setpts=PTS-STARTPTS[p{k}]")
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
