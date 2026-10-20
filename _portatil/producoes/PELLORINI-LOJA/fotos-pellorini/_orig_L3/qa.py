# uso: python qa.py handle pos url_png  -> salva jpg final + comparativo
import sys,urllib.request,io
from PIL import Image,ImageDraw
h,p,url=sys.argv[1],sys.argv[2],sys.argv[3]
base='C:/Users/PICHAU/Downloads/PELLORINI-LOJA/fotos-pellorini/'
o=Image.open(f'{base}_orig_L3/{h}_{p}.png').convert('RGB')
n=Image.open(f'{base}_orig_L3/{h}_{p}_gen.png').convert('RGB')
print('orig',o.size,'novo',n.size)


nn=n.resize(o.size)
W=o.width
# full side by side + zoom grid (lid upper, roll left, card bottom) relative crops
S=900
top=Image.new('RGB',(S*2,S),'white');top.paste(o.resize((S,S)),(0,0));top.paste(nn.resize((S,S)),(S,0))
regs=[(0.1,0.0,0.9,0.45),(0.0,0.35,0.55,0.75),(0.0,0.65,0.75,1.0),(0.3,0.4,0.8,0.85)]
rows=[top]
for r in regs:
    b=tuple(int(v*W) for v in r)
    a=o.crop(b);c=nn.crop(b);sc=S/a.width
    a=a.resize((S,int(a.height*sc)));c=c.resize((S,int(c.height*sc)))
    im=Image.new('RGB',(S*2,a.height),'white');im.paste(a,(0,0));im.paste(c,(S,0));rows.append(im)
H=sum(r.height for r in rows);out=Image.new('RGB',(S*2,H),'white');y=0
for r in rows: out.paste(r,(0,y));y+=r.height
out.save(f'{base}_comparar/{h}_{p}.jpg',quality=80)
