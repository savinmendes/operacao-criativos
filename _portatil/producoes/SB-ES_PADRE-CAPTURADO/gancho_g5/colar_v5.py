# -*- coding: utf-8 -*-
"""Cola gancho_G5.mp4 + ../corpo/corpo_a_partir_selfie.mp4 -> V5_NOTICIA-TV.mp4 (corte seco, áudio sem salto:
1 passada com concat de filtro, micro-fade de 15 ms na emenda, -reinit_filter 0)."""
import subprocess, json
from pathlib import Path
AQ = Path(__file__).resolve().parent
G = AQ / "gancho_G5.mp4"; C = AQ.parent / "corpo" / "corpo_a_partir_selfie.mp4"; OUT = AQ / "V5_NOTICIA-TV.mp4"
def dur(p, s="format"):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())
dg = dur(G)
f = (f"[0:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v0];[1:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v1];"
     f"[v0][v1]concat=n=2:v=1:a=0[v];"
     f"[0:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=out:st={dg-0.10:.3f}:d=0.10[a0];"
     f"[1:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:st=0:d=0.03[a1];[a0][a1]concat=n=2:v=0:a=1[a]")
cmd = ["ffmpeg", "-v", "error", "-y", "-reinit_filter", "0", "-i", str(G), "-reinit_filter", "0", "-i", str(C),
       "-filter_complex", f, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
       "-profile:v", "high", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709",
       "-color_trc", "bt709", "-color_range", "tv", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2",
       "-movflags", "+faststart", str(OUT)]
subprocess.run(cmd, check=True)
print("ok", OUT, "gancho", dg, "corpo", dur(C), "total", dur(OUT))
