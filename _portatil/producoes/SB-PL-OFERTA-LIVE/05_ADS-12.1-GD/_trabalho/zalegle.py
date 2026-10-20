# Corrige o carimbo "OVERDUTE" (original) para "ZALEGŁE" (IT): apaga o carimbo inteiro (LaMa) e redesenha
# moldura + texto no mesmo lugar, mesma cor, inclinação e desfoque. O plano do gancho é estático.
import warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
from simple_lama_inpainting import SimpleLama
from comum3 import quadros
f=list(quadros("fontes/es.mp4",75,1))[0]
X0,Y0,X1,Y1=460,360,720,480
c=f[Y0:Y1,X0:X1].copy(); hsv=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)
red=(((hsv[...,0]<12)|(hsv[...,0]>165))&(hsv[...,1]>60)).astype(np.uint8)
m=np.zeros_like(red); m[398-Y0:442-Y0, 496-X0:720-X0]=1
m=cv2.dilate(red,np.ones((9,9),np.uint8))&m | (m*0)
m[401-Y0:440-Y0, 499-X0:720-X0]=1
lama=SimpleLama(); r=lama(Image.fromarray(cv2.cvtColor(c,cv2.COLOR_BGR2RGB)),Image.fromarray(m*255))
lim=cv2.cvtColor(np.array(r),cv2.COLOR_RGB2BGR)[:c.shape[0],:c.shape[1]]
px=c[red>0]; v=px.sum(1); cor=px[v<=np.percentile(v,10)].mean(0)
S=4; W,H=(X1-X0)*S,(Y1-Y0)*S; big=Image.new("L",(W,H),0); d=ImageDraw.Draw(big)
# moldura: x 502-714, y 404-436 (medido no original)
bx0,by0,bx1,by1=(502-X0)*S,(405-Y0)*S,(714-X0)*S,(435-Y0)*S
d.rectangle([bx0,by0,bx1,by1],outline=255,width=4*S)
fnt=ImageFont.truetype(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf",30*S)
txt="ZALEGŁE"; bb=d.textbbox((0,0),txt,font=fnt)
img=Image.new("L",(bb[2]-bb[0],bb[3]-bb[1]),0); ImageDraw.Draw(img).text((-bb[0],-bb[1]),txt,font=fnt,fill=255)
img=img.resize((176*S,20*S),Image.LANCZOS)
cx,cy=(608-X0)*S,(420-Y0)*S; big.paste(img,(cx-img.width//2,cy-img.height//2),img)
big=big.rotate(-2.0,resample=Image.BICUBIC,center=(cx,cy))
a=np.array(big.resize((X1-X0,Y1-Y0),Image.LANCZOS)).astype(np.float32)/255
a=cv2.GaussianBlur(a,(0,0),1.6)[...,None]*1.0
out=np.clip(lim*(1-a)+cor*a,0,255).astype(np.uint8)
mk=cv2.GaussianBlur(m.astype(np.float32),(0,0),2)  # máscara de colagem
np.save("zalegle_patch.npy",out); np.save("zalegle_mask.npy",np.maximum(mk,(a[...,0]>0.02).astype(np.float32)))
cv2.imwrite("folhas/zalegle_fix.png",cv2.resize(np.vstack([c,lim,out]),None,fx=2,fy=2))
print("cor",cor)
