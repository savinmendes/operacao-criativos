import os, matplotlib
from PIL import Image, ImageDraw, ImageFont
dj=os.path.join(os.path.dirname(matplotlib.__file__),'mpl-data','fonts','ttf','DejaVuSans.ttf')
src=Image.open('q/full_123.6.png').crop((40,740,680,850))
rows=[src]
for nm,p in [('OpenSans','fonts/OpenSans.ttf'),('NotoSans','fonts/NotoSans.ttf'),('DejaVu',dj),('Verdana','C:/Windows/Fonts/verdana.ttf')]:
    f=ImageFont.truetype(p,46)
    try: f.set_variation_by_name('Regular')
    except: pass
    c=Image.new('RGB',src.size,(150,40,150)); d=ImageDraw.Draw(c)
    for i,t in enumerate(['deixar o grimório','sagrado']):
        b=d.textbbox((0,0),t,font=f); d.text((320-(b[2]-b[0])/2-b[0],5+i*52),t,font=f,fill='white')
    d.text((5,80),nm,fill='yellow'); rows.append(c)
o=Image.new('RGB',(src.width,sum(r.height for r in rows))); y=0
for r in rows: o.paste(r,(0,y)); y+=r.height
o.save('q/fontcmp2.png')
