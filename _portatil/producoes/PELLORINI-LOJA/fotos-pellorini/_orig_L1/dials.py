import sys
from PIL import Image,ImageDraw
D={'pellorini-argento_1':(947,1075,110),'pellorini-dante_1':(742,1357,330),'pellorini-dante_6':(998,1075,120),
'pellorini-dante_8':(998,1485,260),'pellorini-forte_2':(947,1229,120),'pellorini-lucent_1':(794,1485,280),
'pellorini-lucent_11':(1050,1408,230),'pellorini-lucent_4':(1050,1152,110),'pellorini-maretti_10':(1050,1126,170),
'pellorini-veloce_1':(972,1280,120),'pellorini-venti_2':(896,1229,110),'titan_1':(1024,1024,140)}
ks=sys.argv[1:] or list(D); S=400
c=Image.new('RGB',(2*S*3+20,(S+20)*((len(ks)+2)//3)),'white');d=ImageDraw.Draw(c)
for i,k in enumerate(ks):
    cx,cy,r=D[k];r=int(r*1.3);box=(cx-r,cy-r,cx+r,cy+r)
    o=Image.open(k+'.jpg').crop(box).resize((S,S));n=Image.open('../'+k+'.jpg').crop(box).resize((S,S))
    x=(i%3)*(2*S+10);y=(i//3)*(S+20)
    d.text((x+3,y+2),k,fill='red');c.paste(o,(x,y+18));c.paste(n,(x+S,y+18))
c.save('../_comparar/_L1_dialsheet.jpg',quality=88)
