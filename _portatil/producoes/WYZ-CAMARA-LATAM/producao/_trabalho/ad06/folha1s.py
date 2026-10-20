import subprocess, sys, tempfile, os
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]
d = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",v],capture_output=True,text=True).stdout)
ts = [x+0.0 for x in range(int(d)+1) if x < d-0.05]; ts[-1:] = [ts[-1], d-0.1]
tw, th, cols = 180, 320, 9
rows = (len(ts)+cols-1)//cols
g = Image.new("RGB", (tw*cols, th*rows))
tmp = tempfile.mkdtemp()
for i,t in enumerate(ts):
    p = os.path.join(tmp, "f.png")
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.2f}","-i",v,"-frames:v","1","-vf",f"scale={tw}:{th}",p])
    im = Image.open(p).convert("RGB"); ImageDraw.Draw(im).text((4,4), f"{t:.1f}", fill=(255,255,0))
    g.paste(im, ((i%cols)*tw, (i//cols)*th))
g.save(out, quality=85)
