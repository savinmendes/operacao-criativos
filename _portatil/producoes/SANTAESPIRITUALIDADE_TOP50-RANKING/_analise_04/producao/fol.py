import subprocess, numpy as np, sys
from PIL import Image, ImageDraw, ImageFont
src, a, b, step, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
w, h = 144, 256
raw = subprocess.run(["ffmpeg","-v","error","-ss",str(a),"-i",src,"-t",str(b-a),"-vf",f"fps={1/step},scale={w}:{h}","-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
fr = np.frombuffer(raw,np.uint8).reshape(-1,h,w,3); cols=10; rows=(len(fr)+cols-1)//cols
im = Image.new("RGB",(cols*w,rows*h)); d=ImageDraw.Draw(im); f=ImageFont.truetype("arial.ttf",20)
for i,x in enumerate(fr):
    im.paste(Image.fromarray(x),((i%cols)*w,(i//cols)*h)); d.text(((i%cols)*w+3,(i//cols)*h+3),f"{a+i*step:.1f}",font=f,fill=(255,255,0),stroke_width=2,stroke_fill=(0,0,0))
im.save(out, quality=85)
