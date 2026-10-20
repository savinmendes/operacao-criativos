# uso: folha.py nome t0 t1 passo cols largura [x0 y0 x1 y1]
import sys,os
from PIL import Image,ImageDraw,ImageFont
D=os.path.dirname(os.path.abspath(__file__))
nome,t0,t1,passo,cols,w=sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
box=tuple(map(int,sys.argv[7:11])) if len(sys.argv)>7 else None
q0=int(round(t0*30)); q1=int(round(t1*30))
idx=list(range(q0,q1+1,passo))
ims=[]
for q in idx:
    p=os.path.join(D,'f','%05d.jpg'%(q+1))
    if not os.path.exists(p): continue
    im=Image.open(p)
    if box: im=im.crop(box)
    h=int(im.height*w/im.width); im=im.resize((w,h))
    d=ImageDraw.Draw(im); m,s=divmod(q/30,60)
    try: f=ImageFont.truetype('arial.ttf',max(12,w//14))
    except: f=None
    txt='%d:%05.2f #%d'%(m,s,q)
    d.rectangle((0,0,w,max(14,w//12)),fill=(0,0,0)); d.text((2,0),txt,fill=(255,255,0),font=f)
    ims.append(im)
rows=(len(ims)+cols-1)//cols; h=ims[0].height
out=Image.new('RGB',(cols*w,rows*h),(40,40,40))
for i,im in enumerate(ims): out.paste(im,((i%cols)*w,(i//cols)*h))
out.save(os.path.join(D,'s',nome+'.jpg'),quality=85); print(nome,len(ims),out.size)
