import sys,json
from PIL import Image,ImageDraw
# crops.py out H q:x0:y0:x1:y1 ...
out,H=sys.argv[1],int(sys.argv[2]); ims=[]
for a in sys.argv[3:]:
    q,x0,y0,x1,y1=map(int,a.split(':'))
    im=Image.open('f/%05d.jpg'%(q+1)).crop((x0,y0,x1,y1)); im=im.resize((int(im.width*H/im.height),H),Image.LANCZOS)
    d=ImageDraw.Draw(im); m,s=divmod(q/30,60); d.rectangle((0,0,150,22),fill=0); d.text((3,3),'%d:%05.2f #%d'%(m,s,q),fill=(255,255,0)); ims.append(im)
W=sum(i.width for i in ims); o=Image.new('RGB',(W,H)); x=0
for i in ims: o.paste(i,(x,0)); x+=i.width
o.save('s/'+out+'.jpg',quality=90)
