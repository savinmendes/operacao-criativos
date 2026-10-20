import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
im = np.asarray(Image.open('q/full_131.0.png').convert('RGB')).astype(int)
reg = im[775:830, 140:600]
m = (reg.min(axis=2) > 235)
ys, xs = np.where(m)
print('bbox', xs.min()+140, xs.max()+140, ys.min()+775, ys.max()+775)
x0,x1,y0,y1 = xs.min()+140, xs.max()+140, ys.min()+775, ys.max()+775
crop = Image.open('q/full_131.0.png').crop((x0-10,y0-10,x1+10,y1+10))
rows=[crop.resize((crop.width*3,crop.height*3))]
for nm in ['OpenSans','NotoSans','Roboto']:
    best=None
    for sz in range(30,70):
        f=ImageFont.truetype(f'fonts/{nm}.ttf',sz)
        try: f.set_variation_by_name('Regular')
        except Exception as e: pass
        d=ImageDraw.Draw(Image.new('L',(10,10)))
        b=d.textbbox((0,0),'por quanto tempo',font=f)
        if best is None or abs((b[2]-b[0])-(x1-x0))<best[0]: best=(abs((b[2]-b[0])-(x1-x0)),sz,b)
    sz=best[1]; f=ImageFont.truetype(f'fonts/{nm}.ttf',sz)
    try: f.set_variation_by_name('Regular')
    except: pass
    b=best[2]; print(nm, sz, 'w',b[2]-b[0],'h',b[3]-b[1],'target h',y1-y0)
    c=Image.new('RGB',crop.size,(120,40,120)); d=ImageDraw.Draw(c)
    d.text((10-b[0],10-b[1]),'por quanto tempo',font=f,fill='white',stroke_width=1,stroke_fill=(40,40,40))
    rows.append(c.resize((c.width*3,c.height*3)))
o=Image.new('RGB',(rows[0].width,sum(r.height for r in rows))); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.save('q/fontcmp.png')
