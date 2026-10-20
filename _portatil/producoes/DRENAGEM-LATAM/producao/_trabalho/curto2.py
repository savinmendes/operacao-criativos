# -*- coding: utf-8 -*-
"""Versão CURTA (variante): junta trechos de um vídeo já tratado (+ gancho opcional antes) e cola o fim universal.
  python curto2.py <pasta_ad> <fonte_tratada.mp4> "<saida final.mp4>" ini-fim ini-fim ... [--hook hook.mp4] [--so-parte1]
Trabalha em <pasta_ad>/curto/ (não mexe na versão longa). Narração do fim: <pasta_ad>/narr_fim.mp3. Use caminhos absolutos."""
import subprocess
import sys
from pathlib import Path

TRAB = Path(__file__).parent
args = list(sys.argv[1:])
hook = None
if "--hook" in args:
    i = args.index("--hook")
    hook = args[i + 1]
    del args[i:i + 2]
so = "--so-parte1" in args
args = [a for a in args if a != "--so-parte1"]
pasta, fonte, saida, *segs = args
pasta = Path(pasta).resolve()
C = pasta / "curto"
C.mkdir(exist_ok=True)


def run(*a):
    subprocess.run([str(x) for x in a], check=True)


partes = [Path(hook).resolve()] if hook else []
for i, s in enumerate(segs):
    a, b = map(float, s.split("-"))
    o = C / f"s{i}.mp4"
    run("ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", fonte, "-vf", "fps=30,setpts=PTS-STARTPTS",
        "-af", "aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:d=0.04,"
        f"afade=t=out:st={max(0, b - a - 0.06):.3f}:d=0.06",
        "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", o)
    partes.append(o)
p1 = C / "parte1_curto.mp4"
ins = sum([["-i", str(p)] for p in partes], [])
fc = "".join(f"[{i}:v][{i}:a]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=1[v][a]"
run("ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "15",
    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", p1)
print("parte1_curto", subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p1)],
                                     capture_output=True, text=True).stdout.strip(), flush=True)
if not so:
    run(sys.executable, TRAB / "montar_fim_universal.py", C, p1, pasta / "narr_fim.mp3", Path(saida).resolve(), "--res", "720")
