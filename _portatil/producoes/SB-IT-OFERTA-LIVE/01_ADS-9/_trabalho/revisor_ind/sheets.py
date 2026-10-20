import subprocess,sys,io
from PIL import Image,ImageDraw
V=r"C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\01_ADS-9\SB-IT-ADS-9.mp4"
def fr(t):
    b=subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",V,"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    return Image.open(io.BytesIO(b)).convert("RGB")
def sheet(times,box,name,cols,scale=1.0):
    ims=[]
    for t in times:
        im=fr(t).crop(box); im=im.resize((int(im.width*scale),int(im.height*scale)))
        d=ImageDraw.Draw(im); d.rectangle((0,0,70,18),fill=(0,0,0)); d.text((2,2),f"{t:.2f}",fill=(255,255,0)); ims.append(im)
    w,h=ims[0].size; rows=(len(ims)+cols-1)//cols
    S=Image.new("RGB",(w*cols,h*rows))
    for i,im in enumerate(ims): S.paste(im,((i%cols)*w,(i//cols)*h))
    S.save(name,quality=90)
cap=[11.5,7.2,8.5,42.5,65.5,71.9,78.7,83.0,84.5,91.5,93.2,95.8,101.0, 85.5,87.8,79.6]
sheet(cap,(0,880,720,1040),"cap.jpg",2)
seams=[2.37,9.6,19.4,29.1,39.3,48.0,58.8,68.4,74.1,81.7,89.6,97.77]
ts=[]
for s in seams: ts+= [s-1/30,s,s+1/30]
sheet(ts,(200,300,520,760),"seams.jpg",6,0.6)
mouth=[3.0,14.0,36.0,52.4,66.0,86.0]
sheet(mouth,(250,450,470,690),"mouth.jpg",3,1.5)
sheet([82.3,88.0,96.0,97.5,97.8,98.5,100.5,102.7],(0,0,720,1280),"end.jpg",4,0.45)
