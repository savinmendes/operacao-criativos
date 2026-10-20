# Compoe o corpo: avatar HeyGen (base, tela cheia) + takes sem rosto por cima nos tempos da fala.
# Audio = narracao ElevenLabs (a mesma enviada ao HeyGen), normalizada a -15 LUFS; 0,6 s de cauda.
#   python compor.py config.json
import json, subprocess, sys
from pathlib import Path
C = json.load(open(sys.argv[1], encoding="utf-8"))
D = Path(sys.argv[1]).parent
narr = D / C["narr"]
dn = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(narr)],
                          capture_output=True, text=True).stdout)
total = round(dn + C.get("cauda", 0.6), 3)
ins = ["-i", str(D / C["avatar"]), "-i", str(narr)]
fc = [f"[0:v]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,fps=30,"
      f"tpad=stop_mode=clone:stop_duration=3,trim=0:{total},setpts=PTS-STARTPTS[v0]"]
for k, (f, t0) in enumerate(C["takes"]):
    ins += ["-i", str(D / f)]
    fc.append(f"[{k + 2}:v]setpts=PTS-STARTPTS+{t0}/TB[t{k}]")
    fc.append(f"[v{k}][t{k}]overlay=0:0:eof_action=pass[v{k + 1}]")
n = len(C["takes"])
fc.append(f"[1:a]loudnorm=I=-15:TP=-1.5:LRA=11,aresample=48000,apad,atrim=0:{total}[a]")
out = D / "corpo.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", *ins, "-filter_complex", ";".join(fc),
                "-map", f"[v{n}]", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                "-t", str(total), str(out)], check=True)
print("ok", out, total)
