from rembg import remove, new_session
from PIL import Image
im=Image.open("kit04.jpg").convert("RGB")
crops={"carregador":(im.crop((0,640,430,1020))),}
m=Image.open("maleta_02.jpg").convert("RGB"); crops["maleta"]=m
b=Image.open("bateria_02.jpg").convert("RGB"); crops["bateria"]=b.crop((380,560,720,920))
for mod in ["u2net","isnet-general-use"]:
    s=new_session(mod)
    for k,v in crops.items():
        o=remove(v,session=s); o.save(f"{k}_{mod}.png")
# preview
import glob
fs=sorted(glob.glob("*_u2net.png")+glob.glob("*_isnet-general-use.png"))
ims=[Image.open(f) for f in fs]
H=max(i.height for i in ims);W=sum(i.width for i in ims)
c=Image.new("RGB",(W,H),(60,140,60));x=0
for i in ims: c.paste(i,(x,0),i);x+=i.width
c.resize((W//2,H//2)).save("cuts2.jpg");print(fs)
