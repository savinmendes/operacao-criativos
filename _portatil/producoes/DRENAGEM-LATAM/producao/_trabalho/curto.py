# -*- coding: utf-8 -*-
"""Versão CURTA: corta trechos (ini-fim, s) de um parte1.mp4 já tratado, concatena com fade de 25 ms no áudio
e monta com o fim universal.  python curto.py <pasta_ad> <narr_fim.mp3> "<saida>" ini-fim ini-fim ..."""
import subprocess, sys
from pathlib import Path
TRAB = Path(__file__).parent
pasta = Path(sys.argv[1]).resolve(); narr = str(Path(sys.argv[2]).resolve()); saida = sys.argv[3]; segs = sys.argv[4:]
cur = pasta / "curto"; cur.mkdir(exist_ok=True)
lst = []
for i, s in enumerate(segs):
    a, b = map(float, s.split("-")); d = b - a
    o = cur / f"s{i}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(pasta / "parte1.mp4"), "-t", f"{d:.3f}",
                    "-af", f"afade=t=in:d=0.025,afade=t=out:st={d-0.04:.3f}:d=0.04", "-c:v", "libx264", "-crf", "15",
                    "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(o)], check=True)
    lst.append(f"file '{o.as_posix()}'")
(cur / "lista.txt").write_text("\n".join(lst), encoding="utf-8")
p1 = cur / "parte1_curto.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(cur / "lista.txt"), "-c", "copy", str(p1)], check=True)
subprocess.run([sys.executable, str(TRAB / "montar_fim_universal.py"), str(cur), str(p1), narr, saida, "--res", "720"], check=True)
