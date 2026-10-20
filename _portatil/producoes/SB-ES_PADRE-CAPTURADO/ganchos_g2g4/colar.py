# -*- coding: utf-8 -*-
"""Cola gancho + corpo_a_partir_selfie.mp4 (corte seco no vídeo; no áudio, micro-fade de 15 ms em cada lado para não estalar).
uso: python colar.py gancho.mp4 corpo.mp4 saida.mp4"""
import sys, subprocess
g, c, out = sys.argv[1:4]
fc = ("[0:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v0];[1:v]fps=30,scale=720:1280,setsar=1,format=yuv420p[v1];"
      "[0:a]aresample=44100,aformat=channel_layouts=stereo,areverse,afade=t=in:d=0.015,areverse[a0];"
      "[1:a]aresample=44100,aformat=channel_layouts=stereo,afade=t=in:d=0.015[a1];"
      "[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", g, "-i", c, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "2700k", "-bufsize", "5400k", "-pix_fmt", "yuv420p", "-r", "30",
                "-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
                "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-ac", "2", "-movflags", "+faststart", out], check=True)
print("ok", out)
