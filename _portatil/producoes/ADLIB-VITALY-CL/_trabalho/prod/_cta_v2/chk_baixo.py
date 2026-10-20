import subprocess, io, sys
from PIL import Image, ImageDraw
rows=[]
for f in sys.argv[2:]:
    d=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout)
    ims=[]; t=0.05
    while t<d-0.05 and len(ims)<16:
        p=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.2f}","-i",f,"-frames:v","1","-vf","scale=240:-2,crop=240:ih*0.5:0:ih*0.5","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        ims.append(Image.open(io.BytesIO(p)).convert("RGB")); t+=d/16
    h=ims[0].height; r=Image.new("RGB",(240*16,h+14)); [r.paste(im,(i*240,14)) for i,im in enumerate(ims)]
    ImageDraw.Draw(r).text((2,1),"/".join(f.replace("\\","/").split("/")[-3:]),fill=(255,255,0)); rows.append(r)
o=Image.new("RGB",(rows[0].width,sum(r.height for r in rows))); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.save(sys.argv[1],quality=75)
