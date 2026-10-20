import sys
from PIL import Image,ImageDraw
k,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6]); src=sys.argv[6] if len(sys.argv)>6 else '../'+k+'.jpg'
im=Image.open(src).crop((x0,y0,x1,y1)); s=800/im.width; im=im.resize((800,int(im.height*s))); d=ImageDraw.Draw(im)
for x in range((x0//50+1)*50,x1,50): X=(x-x0)*s; d.line([(X,0),(X,im.height)],fill=(255,0,0) if x%100==0 else (255,150,150),width=1); d.text((X+2,2),str(x),fill='yellow') if x%100==0 else None
for y in range((y0//50+1)*50,y1,50): Y=(y-y0)*s; d.line([(0,Y),(800,Y)],fill=(255,0,0) if y%100==0 else (255,150,150),width=1); d.text((2,Y+2),str(y),fill='yellow') if y%100==0 else None
im.save('../_comparar/_grid_'+k+'.jpg',quality=88)
