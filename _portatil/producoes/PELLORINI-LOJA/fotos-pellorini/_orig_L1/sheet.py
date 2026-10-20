from PIL import Image,ImageDraw
import glob,os
fs=sorted(glob.glob('../_comparar/*_zoom.jpg'))+sorted(glob.glob('../_comparar/*_card.jpg'))
for s in range(0,len(fs),5):
    ims=[Image.open(f) for f in fs[s:s+5]]
    W=900;H=sum(i.height+30 for i in ims)
    c=Image.new('RGB',(W,H),'white');d=ImageDraw.Draw(c);y=0
    for f,i in zip(fs[s:s+5],ims):
        d.text((5,y+5),os.path.basename(f),fill='red');y+=30;c.paste(i,(0,y));y+=i.height
    c.save(f'../_comparar/_sheet{s//5}.jpg',quality=85);print(s//5,[os.path.basename(f) for f in fs[s:s+5]],H)
