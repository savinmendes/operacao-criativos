import subprocess, io, sys
from PIL import Image
f, out = sys.argv[1], sys.argv[2]; ts=[float(x) for x in sys.argv[3].split(",")]
ims=[]
for t in ts:
    p=subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",f,"-frames:v","1","-vf","scale=240:-2","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    ims.append(Image.open(io.BytesIO(p)).convert("RGB"))
cols=8; w,h=ims[0].size; rows=(len(ims)+cols-1)//cols; o=Image.new("RGB",(w*cols,h*rows))
for i,im in enumerate(ims): o.paste(im,((i%cols)*w,(i//cols)*h))
o.save(out,quality=85)
