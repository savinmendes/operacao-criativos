from rembg import remove, new_session
from PIL import Image
s=new_session("u2net"); s2=new_session("isnet-general-use")
b=Image.open("bateria_02.jpg").convert("RGB").crop((20,540,520,880))
k=Image.open("kit04.jpg").convert("RGB")
for nm,img in [("bat_a",b),("bat_b",k.crop((170,800,720,1230))),("carr",k.crop((0,630,440,1040)))]:
    for mn,ss in [("u",s),("i",s2)]:
        remove(img,session=ss).save(f"{nm}_{mn}.png")
fs=["bat_a_u","bat_a_i","bat_b_u","bat_b_i","carr_u","carr_i"]
ims=[Image.open(f+".png") for f in fs]
W=sum(i.width for i in ims);H=max(i.height for i in ims)
c=Image.new("RGB",(W,H),(60,140,60));x=0
for i in ims: c.paste(i,(x,0),i);x+=i.width
c.resize((W//2,H//2)).save("cuts3.jpg")
