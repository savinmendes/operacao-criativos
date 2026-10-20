import sys,glob,os
from PIL import Image,ImageDraw,ImageFont
pat,out,cols,rows=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
fs=sorted(glob.glob(pat)); font=ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf",20)
n=cols*rows
for k in range(0,len(fs),n):
    ch=fs[k:k+n]; im0=Image.open(ch[0]); w,h=im0.size
    sh=Image.new("RGB",(cols*w,rows*h))
    for i,f in enumerate(ch):
        t=int(os.path.basename(f).split("_")[1].split(".")[0])
        im=Image.open(f); d=ImageDraw.Draw(im); d.rectangle([0,0,80,24],fill="black"); d.text((3,1),f"{t//60:02d}:{t%60:02d}",fill="yellow",font=font)
        sh.paste(im,((i%cols)*w,(i//cols)*h))
    sh.save(out.replace(".jpg",f"_{k//n+1:02d}.jpg"),quality=80)
