# Cartão de título PL no mesmo estilo do original (caixas brancas arredondadas, texto preto, ‼️ vermelhos e linha de emojis do original)
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
Y0=250
med=cv2.imread("card_med.png"); st=cv2.imread("card_static.png",0)
m=cv2.morphologyEx(st,cv2.MORPH_CLOSE,np.ones((25,25),np.uint8))
cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
alpha=np.zeros_like(m); cv2.drawContours(alpha,[max(cs,key=cv2.contourArea)],-1,255,-1)
alpha=cv2.erode(alpha,np.ones((3,3),np.uint8))
alpha=cv2.dilate(alpha,np.ones((5,5),np.uint8))  # cobre a borda antiga com folga
# vermelhos (‼️) da linha 1
hsv=cv2.cvtColor(med,cv2.COLOR_BGR2HSV)
red=(((hsv[...,0]<10)|(hsv[...,0]>170))&(hsv[...,1]>120)&(hsv[...,2]>120)).astype(np.uint8)
red[180:]=0
n,lab,stt,_=cv2.connectedComponentsWithStats(red)
xs=[(stt[k,0],stt[k,0]+stt[k,2]) for k in range(1,n) if stt[k,4]>30]
xs.sort(); print("red comps",xs)
ys=np.where(red.any(1))[0]; ry0,ry1=ys.min()-3,ys.max()+4
le=[a for a in xs if a[0]<540]; ri=[a for a in xs if a[0]>540]
L=(min(a[0] for a in le)-4,max(a[1] for a in le)+4); R=(min(a[0] for a in ri)-4,max(a[1] for a in ri)+4)
excl=med[ry0:ry1,L[0]:L[1]].copy(); excr=med[ry0:ry1,R[0]:R[1]].copy()
img=med.copy()
# branqueia as linhas de texto (até a linha de emojis, y<612-250)
EMO=612-Y0
wh=(alpha>0); wh[EMO:]=False
img[wh]=255
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB); pil=Image.fromarray(img); d=ImageDraw.Draw(pil)
F=ImageFont.truetype(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf",60)
def centro(txt,y,f=F):
    w=d.textlength(txt,font=f); x=540-w/2; d.text((x,y),txt,font=f,fill=(0,0,0)); return x,w
# linha 1: ‼️ Ostatnie ostrzeżenie ‼️
t1="Ostatnie ostrzeżenie"; w1=d.textlength(t1,font=F); ew=excl.shape[1]; gap=12
tot=ew+gap+w1+gap+excr.shape[1]; x0=540-tot/2
cy=(ry0+ry1)/2
d.text((x0+ew+gap,cy-41),t1,font=F,fill=(0,0,0))
img=np.array(pil)
xl=int(round(x0)); img[ry0:ry1,xl:xl+ew]=cv2.cvtColor(excl,cv2.COLOR_BGR2RGB)
xr=int(round(x0+ew+gap+w1+gap)); img[ry0:ry1,xr:xr+excr.shape[1]]=cv2.cvtColor(excr,cv2.COLOR_BGR2RGB)
pil=Image.fromarray(img); d=ImageDraw.Draw(pil)
centro("Zostań do samego końca",440-Y0-44+6)
centro("i słuchaj bardzo uważnie",535-Y0-44+6)
out=np.dstack([np.array(pil),alpha])
full=np.zeros((1920,1080,4),np.uint8); full[Y0:Y0+out.shape[0]]=out
Image.fromarray(full).save("card_pl.png"); print("ok",ry0+Y0,ry1+Y0)
