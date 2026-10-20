import os,sys,glob
from PIL import Image,ImageDraw,ImageFont
src,out,step,cols,rows,w,h=sys.argv[1],sys.argv[2],float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7])
os.makedirs(out,exist_ok=True)
fs=sorted(glob.glob(src+'/*.jpg'));n=cols*rows
try: font=ImageFont.truetype('arial.ttf',16)
except: font=ImageFont.load_default()
for s in range(0,len(fs),n):
    im=Image.new('RGB',(cols*w,rows*h),'black');d=ImageDraw.Draw(im)
    for i,f in enumerate(fs[s:s+n]):
        t=(s+i)*step
        im.paste(Image.open(f).resize((w,h)),((i%cols)*w,(i//cols)*h))
        x,y=(i%cols)*w,(i//cols)*h
        d.rectangle([x,y+h-20,x+60,y+h],fill='yellow');d.text((x+2,y+h-19),f"{int(t//60):02d}:{int(t%60):02d}",fill='black',font=font)
    a=s*step;im.save(f"{out}/sheet_{int(a//60):02d}m{int(a%60):02d}.jpg",quality=85)
