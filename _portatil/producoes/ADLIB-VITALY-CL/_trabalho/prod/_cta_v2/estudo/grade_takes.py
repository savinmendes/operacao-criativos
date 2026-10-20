import subprocess, io, sys, glob
from pathlib import Path
from PIL import Image, ImageDraw
fs = sorted(glob.glob(r"C:/Users/PICHAU/Downloads/LHYMPORIA AD 01-20/lymphoria/_trabalho/ad*/flora*/*_edit*.mp4")) + sorted(glob.glob(r"C:/Users/PICHAU/Downloads/DRENAGEM-LATAM/producao/_trabalho/ugc/prod/*.mp4"))
def dur(f): return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout or 0)
w=150; ims=[]; lab=[]
for i,f in enumerate(fs):
    d=dur(f); row=[]
    for fr in (0.15,0.5,0.85):
        p=subprocess.run(["ffmpeg","-v","error","-ss",f"{d*fr:.2f}","-i",f,"-frames:v","1","-vf",f"scale={w}:-2","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        row.append(Image.open(io.BytesIO(p)).convert("RGB") if p else Image.new("RGB",(w,266)))
    im=Image.new("RGB",(w*3,row[0].height)); [im.paste(r,(k*w,0)) for k,r in enumerate(row)]
    dd=ImageDraw.Draw(im); n=f"{i} "+"/".join(Path(f).parts[-3:])+f" {d:.1f}s"; dd.rectangle((0,0,w*3,14),fill=(0,0,0)); dd.text((2,1),n[-75:],fill=(255,255,0))
    ims.append(im); print(i,f,round(d,2))
cols=4; H=ims[0].height
for part in range(0,len(ims),20):
    sub=ims[part:part+20]; rows=(len(sub)+cols-1)//cols
    out=Image.new("RGB",(w*3*cols,H*rows))
    for j,im in enumerate(sub): out.paste(im.resize((w*3,H)),((j%cols)*w*3,(j//cols)*H))
    out.save(rf"{sys.argv[1]}\takes_{part//20}.jpg",quality=80)
