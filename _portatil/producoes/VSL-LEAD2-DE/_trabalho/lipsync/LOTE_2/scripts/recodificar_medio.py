# refaz so o encode dos trechos padre_medio (YUV intacto + etiqueta bt709/tv via h264_metadata) e confere a luma
import json, subprocess, sys
from pathlib import Path
R = Path(r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\lipsync\LOTE_2")
TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
def y(p):
    o = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-vf", "crop=200:150:500:200,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-",
        "-frames:v", "30", "-f", "null", "-"], capture_output=True, text=True).stdout
    v = [float(l.split("=")[1]) for l in o.splitlines() if "YAVG" in l]; return sum(v) / len(v)
out = {}
for x in json.load(open(R / "plano.json")):
    i = x["id"]; ls = R / "out" / f"ls_{i}.mp4"
    if x["crop"] or not ls.exists() or (len(sys.argv) > 1 and i not in sys.argv[1:]): continue
    vf = f"tpad=stop_mode=clone:stop=4,trim=end_frame={x['N']},setpts=PTS-STARTPTS"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ls), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "14", "-preset", "medium",
        "-pix_fmt", "yuv420p", *TAG, str(R / f"{i}.mp4")], check=True)
    out[i] = (round(y(R / "in" / f"es_{i}.mp4"), 2), round(y(R / f"{i}.mp4"), 2)); print(i, out[i], flush=True)
json.dump(out, open(R / "_tmp" / "luma.json", "w"), indent=1)
