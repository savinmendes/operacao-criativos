import sys
from PIL import Image, ImageDraw
def tira(nome,t0,t1,passo=3,y0=0,y1=1280,esc=0.25,cols=10):
    qs=list(range(int(t0*30),int(t1*30)+1,passo))
    w=int(720*esc); h=int((y1-y0)*esc)
    rows=(len(qs)+cols-1)//cols
    im=Image.new("RGB",(cols*w,rows*(h+14)),"black"); d=ImageDraw.Draw(im)
    for k,q in enumerate(qs):
        fr=Image.open(f"f/{q+1:05d}.jpg").crop((0,y0,720,y1)).resize((w,h))
        x=(k%cols)*w; y=(k//cols)*(h+14)
        im.paste(fr,(x,y+14)); d.text((x+2,y+1),f"{q} {q/30:.2f}",fill="yellow")
    im.save(nome,quality=85)
a=sys.argv
tira(a[1],float(a[2]),float(a[3]),int(a[4]),int(a[5]),int(a[6]),float(a[7]),int(a[8]))
