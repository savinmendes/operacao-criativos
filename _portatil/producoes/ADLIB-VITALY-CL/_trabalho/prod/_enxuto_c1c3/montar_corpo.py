# -*- coding: utf-8 -*-
"""Corpo 9:16 (1080x1920, 30 fps, bt709) a partir de um plano: segmentos de vídeo na linha do tempo da narração
+ áudio = narração (-16 LUFS) + música (-32 LUFS) contínua.
  python montar_corpo.py plano.json
plano: {"narr": "narr.mp3", "cauda": 0.7, "musica": [arquivo, t0] | null, "saida": "corpo.mp4",
        "segs": [{"f": arquivo, "t0": 0.0, "t1": 2.5, "ss": 0.0, "vel": 1.0, "crop": "x,y,w,h", "sync": false,
                  "zoom": 1.0}]}
  - t0/t1 = tempo no corpo; o último segmento vai até o fim (narração + cauda).
  - sync=true (avatar): ss = t0 (o vídeo do avatar segue o tempo da narração).
  - Fonte curta: desacelera até vel 0,6 e congela o último quadro se ainda faltar.
  - zoom: punch-in leve (1.0 = sem).
"""
import json, subprocess, sys
from pathlib import Path

PL = Path(sys.argv[1]).resolve(); D = PL.parent
R = json.load(open(PL, encoding="utf-8"))
P = lambda p: str((D / p).resolve()) if not Path(p).is_absolute() else p  # noqa: E731


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout.split()[0])


narr = P(R["narr"]); D_total = dur(narr) + R.get("cauda", 0.7)
segs = R["segs"]
segs[-1]["t1"] = D_total
ins, fc = [], []
for k, s in enumerate(segs):
    f = P(s["f"]); seg = s["t1"] - s["t0"]
    ss = s["t0"] if s.get("sync") else s.get("ss", 0.0)
    df = dur(f)
    disp = max(0.1, min(df, s.get("ate", df)) - ss - 0.04)
    vel = s.get("vel", 1.0)
    if disp / vel < seg:  # fonte curta -> desacelera (vel menor) até 0.6, depois congela
        vel = max(0.6, disp / seg)
    fim = (f":end={s['ate']:.3f}" if "ate" in s else "")
    chain = f"trim=start={ss:.3f}{fim},setpts=(PTS-STARTPTS)/{vel:.4f},tpad=stop_mode=clone:stop_duration={seg + 1:.3f},trim=0:{seg:.3f},setpts=PTS-STARTPTS"
    if s.get("crop"):
        x, y, w, h = s["crop"].split(","); chain += f",crop={w}:{h}:{x}:{y}"
    chain += ",scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
    z = s.get("zoom", 1.0)
    if z != 1.0:
        chain += f",scale=iw*{z}:ih*{z},crop=1080:1920"
    ins += ["-i", f]
    fc.append(f"[{k}:v]{chain},fps=30,setsar=1,format=yuv420p[v{k}]")
n = len(segs)
fc.append("".join(f"[v{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0[v]")
ins += ["-i", narr]
fc.append(f"[{n}:a]aresample=48000,loudnorm=I=-16:TP=-2:LRA=11,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={D_total:.3f}[voz]")
if R.get("musica"):
    src, t0 = R["musica"]
    ins += ["-stream_loop", "6", "-ss", f"{t0:.3f}", "-i", P(src)]
    fc.append(f"[{n + 1}:a]atrim=0:{D_total + 0.5:.3f},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,"
              f"loudnorm=I=-32:TP=-9:LRA=11,aresample=48000,afade=t=in:d=0.3,afade=t=out:st={D_total - 0.6:.3f}:d=0.6[mus]")
    fc.append(f"[voz][mus]amix=inputs=2:duration=first:normalize=0,atrim=0:{D_total:.3f}[a]")
else:
    fc.append(f"[voz]atrim=0:{D_total:.3f}[a]")
out = P(R.get("saida", "corpo.mp4"))
cmd = ["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
       "-t", f"{D_total:.3f}", "-threads", "3", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
       "-r", "30", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out]
subprocess.run(cmd, check=True)
print("ok", out, f"{D_total:.2f}s")
