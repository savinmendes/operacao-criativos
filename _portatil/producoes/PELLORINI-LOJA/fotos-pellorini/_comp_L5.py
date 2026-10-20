import sys
from PIL import Image,ImageDraw
S=2048/400
B={("pellorini-abito-limited-edition",8):[(200,35,160,50),(80,385,160,40)],
("pellorini-milano-carbon",1):[(220,78,160,50)],
("pellorini-milano-carbon",17):[(230,90,160,50)],
("pellorini-milano-iced",16):[(230,55,160,50),(30,280,60,120)],
("pellorini-napoli",1):[(200,320,400,160)],
("pellorini-napoli",14):[(240,10,200,40),(200,360,400,80)],
("pellorini-napoli",15):[(240,35,160,50)],
("pellorini-napoli",16):[(255,40,160,50),(60,300,120,80)],
("pellorini-napoli",2):[(230,125,160,50)],
("pellorini-napoli",3):[(240,70,160,50),(50,270,100,80),(370,380,60,40)]}
def comp(h,p,gen,out):
    o=Image.open(f"_orig_L5/{h}_{p}.png").convert('RGB'); g=Image.open(gen).convert('RGB').resize(o.size)
    W=800; top=Image.new('RGB',(W*2,W),'white'); top.paste(o.resize((W,W)),(0,0)); top.paste(g.resize((W,W)),(W,0))
    rows=[top]
    for cx,cy,w,hh in B[(h,p)]:
        box=tuple(int(v*S) for v in (max(cx-w/2,0),max(cy-hh/2,0),min(cx+w/2,400),min(cy+hh/2,400)))
        a=o.crop(box); b=g.crop(box); sc=W/a.width; sz=(W,int(a.height*sc))
        r=Image.new('RGB',(W*2,sz[1]),'white'); r.paste(a.resize(sz),(0,0)); r.paste(b.resize(sz),(W,0)); rows.append(r)
    H=sum(r.height for r in rows); c=Image.new('RGB',(W*2,H),'white'); y=0
    for r in rows: c.paste(r,(0,y)); y+=r.height
    c.save(out,quality=88)
if __name__=='__main__':
    h,p,gen=sys.argv[1],int(sys.argv[2]),sys.argv[3]
    comp(h,p,gen,f"_comparar/{h}_{p}.jpg")
