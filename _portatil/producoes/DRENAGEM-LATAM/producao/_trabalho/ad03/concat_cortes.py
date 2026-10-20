# -*- coding: utf-8 -*-
"""python concat_cortes.py entrada.mp4 cortes.json saida.mp4 [--crf 15]
Concatena trechos [ini,fim] (s) com micro-fade de áudio (12 ms) nas emendas; vídeo 30 fps cortado em quadro inteiro."""
import json, subprocess, sys
src, cj, out = sys.argv[1:4]
crf = sys.argv[sys.argv.index('--crf') + 1] if '--crf' in sys.argv else '15'
seg = json.load(open(cj))
f = []
for i, g in enumerate(seg):
    s, e = g[0], g[1]
    s = round(s * 30) / 30; e = round(e * 30) / 30; d = e - s
    vs = round(g[2] * 30) / 30 if len(g) > 2 and g[2] else s   # vídeo pode começar/terminar no corte de cena
    ve = round(g[3] * 30) / 30 if len(g) > 3 and g[3] else e   # (o buraco vira quadro congelado)
    pad = ""
    if vs > s or ve < e:
        pad = f",tpad=start_mode=clone:start_duration={vs - s:.4f}:stop_mode=clone:stop_duration={e - ve:.4f}"
    f.append(f"[0:v]trim=start={vs:.4f}:end={ve:.4f},setpts=PTS-STARTPTS{pad},trim=duration={d:.4f}[v{i}]")
    f.append(f"[0:a]atrim=start={s:.4f}:end={e:.4f},asetpts=PTS-STARTPTS,afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.4f}:d=0.012[a{i}]")
f.append("".join(f"[v{i}][a{i}]" for i in range(len(seg))) + f"concat=n={len(seg)}:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]",
                "-r", "30", "-c:v", "libx264", "-crf", crf, "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out], check=True)
print("ok", out)
