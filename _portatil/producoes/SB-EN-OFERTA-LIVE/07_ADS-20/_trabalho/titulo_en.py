# Caixa de titulo EN no lugar da ES (mesma geometria; linha de emojis original fica intacta)
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
f=cv2.imread('b_90.png'); W,H=720,1280
bg=np.percentile(f[270:400,30:700].reshape(-1,3),85,axis=0); print('branco',bg)
img=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(img)
COR=(int(bg[2]),int(bg[1]),int(bg[0]),255)
d.rounded_rectangle([55,195,666,272],radius=16,fill=COR)
d.rounded_rectangle([8,262,718,408],radius=16,fill=COR)
fn=ImageFont.truetype(r'C:\Windows\Fonts\segoeuib.ttf',47)
def centro(txt,yc,x0=0,x1=W):
    b=d.textbbox((0,0),txt,font=fn); w=b[2]-b[0]
    x=(x0+x1)/2-w/2-b[0]; d.text((x,yc-(b[1]+b[3])/2),txt,font=fn,fill=(10,10,10,255)); return x+b[0],x+b[2]
# linha 1 com os !! originais recortados
ex=Image.fromarray(cv2.cvtColor(f[208:259,90:140],cv2.COLOR_BGR2RGB)).convert('RGBA')
t='One last warning'; b=d.textbbox((0,0),t,font=fn); w=b[2]-b[0]; tot=w+2*50+2*8
x0=W/2-tot/2
img.paste(ex,(int(x0),208)); xa,xb=centro(t,234,x0+58,x0+58+w); img.paste(ex,(int(x0+58+w+8),208))
centro('Stay until the end and',300); centro('pay close attention',366)
img.save('titulo_en.png')
c=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).convert('RGBA'); c.alpha_composite(img); c.convert('RGB').crop((0,150,720,520)).save('titulo_prev.png')
