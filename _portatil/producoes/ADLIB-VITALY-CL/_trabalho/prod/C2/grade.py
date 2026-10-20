import subprocess, sys
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; ts = [float(x) for x in sys.argv[3].split(",")]
ims = []
for t in ts:
    r = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",v,"-frames:v","1","-vf","scale=240:-2","-f","image2pipe","-vcodec","png","-"],capture_output=True)
    from io import BytesIO; im = Image.open(BytesIO(r.stdout)).convert("RGB"); d = ImageDraw.Draw(im); d.rectangle([0,0,70,18],fill=(0,0,0)); d.text((3,3),f"{t:.2f}",fill=(255,255,0)); ims.append(im)
c = 8; w, h = ims[0].size; g = Image.new("RGB",(w*c, h*((len(ims)+c-1)//c)))
for i, im in enumerate(ims): g.paste(im, ((i%c)*w, (i//c)*h))
g.save(out, quality=85)
