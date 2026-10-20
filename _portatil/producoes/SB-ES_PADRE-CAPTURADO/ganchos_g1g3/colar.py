# -*- coding: utf-8 -*-
"""Cola gancho + corpo_a_partir_selfie.mp4 em uma única passada (decodifica os dois, concat de vídeo e áudio, 1 encode).
Corte seco no vídeo; no áudio, micro-fade de 8 ms dos dois lados da emenda (sem crossfade, para não encurtar nem
dessincronizar). Saída H.264 high 30 fps yuv420p + AAC 48 kHz estéreo. Confere duração e salto de pts no áudio.
uso: python colar.py gancho.mp4 corpo.mp4 saida.mp4"""
import sys, json, subprocess
g, c, out = sys.argv[1:4]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def dur(p, s):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", s, "-show_entries", "stream=duration", "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(r.stdout.strip().splitlines()[0])
dg = dur(g, "v:0")
fc = (f"[0:v]fps=30,setpts=PTS-STARTPTS,format=yuv420p[v0];[1:v]fps=30,setpts=PTS-STARTPTS,format=yuv420p[v1];"
      f"[0:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{dg:.4f},apad=whole_dur={dg:.4f},asetpts=PTS-STARTPTS,afade=t=out:st={dg-0.008:.4f}:d=0.008[a0];"
      f"[1:a]aresample=48000,aformat=channel_layouts=stereo,asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.008[a1];"
      f"[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", g, "-i", c, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "slow", *ENC_TAG,
                "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", out], check=True)
dv, da, dc = dur(out, "v:0"), dur(out, "a:0"), dur(c, "v:0")
# salto de pts no áudio
r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "packet=pts_time,duration_time", "-of", "csv=p=0", out], capture_output=True, text=True)
pk = [tuple(map(float, l.split(",")[:2])) for l in r.stdout.split() if l.count(",") >= 1]
saltos = [(round(a[0], 3), round(b[0] - a[0] - a[1], 3)) for a, b in zip(pk, pk[1:]) if abs(b[0] - a[0] - a[1]) > 0.01]
print(json.dumps({"saida": out, "gancho": round(dg, 3), "corpo": round(dc, 3), "video": round(dv, 3), "audio": round(da, 3),
                  "saltos_pts_audio": saltos[:5]}, ensure_ascii=False))
