import json,sys
from PIL import Image, ImageDraw
d=json.load(open('whisper.json',encoding='utf-8'))
W=[(w[0],w[1],w[2]) for s in d for w in s['w']]
def fala(t):
    for a,b,x in W:
        if a-0.03<=t<=b+0.03: return x.strip()
    return ""
def tira(nome,t0,t1,box,passo=2,esc=1.0,cols=12):
    qs=list(range(round(t0*30),round(t1*30),passo))
    x0,y0,x1,y1=box; w=int((x1-x0)*esc); h=int((y1-y0)*esc)
    rows=(len(qs)+cols-1)//cols
    im=Image.new("RGB",(cols*w,rows*(h+26)),"black"); dr=ImageDraw.Draw(im)
    for k,q in enumerate(qs):
        fr=Image.open(f"f/{q+1:05d}.jpg").crop(box).resize((w,h))
        x=(k%cols)*w; y=(k//cols)*(h+26)
        im.paste(fr,(x,y+26)); f=fala(q/30)
        dr.text((x+2,y+1),f"{q/30:.2f}",fill="yellow"); dr.text((x+2,y+12),f[:14] if f else "--",fill="lime" if f else "red")
    im.save(nome,quality=88)
a=sys.argv
tira(a[1],float(a[2]),float(a[3]),tuple(map(int,a[4].split(','))),int(a[5]),float(a[6]),int(a[7]))
