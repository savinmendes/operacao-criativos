# uso: python zoom.py <chave> x0 y0 x1 y1  (frações 0-1)
import sys
from PIL import Image
D=r"C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini"
k=sys.argv[1]; x0,y0,x1,y1=map(float,sys.argv[2:6]); suf=sys.argv[6] if len(sys.argv)>6 else "zoom"
o=Image.open(rf"{D}\_orig_L1\{k}.jpg"); n=Image.open(rf"{D}\{k}.jpg")
def cr(im):
    W,H=im.size; c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
    s=900/c.width; return c.resize((900,int(c.height*s)))
a,b=cr(o),cr(n)
c=Image.new("RGB",(900,a.height+b.height+10),"white"); c.paste(a,(0,0)); c.paste(b,(0,a.height+10))
c.save(rf"{D}\_comparar\{k}_{suf}.jpg",quality=90)
