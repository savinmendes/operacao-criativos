# uso: python comparar.py <chave> <url_png>
import sys,requests,io
from PIL import Image,ImageDraw
D=r"C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini"
k,u=sys.argv[1],sys.argv[2]
new=Image.open(io.BytesIO(requests.get(u,timeout=120).content)).convert("RGB")
new.save(rf"{D}\{k}.jpg",quality=94)
org=Image.open(rf"{D}\_orig_L1\{k}.jpg").convert("RGB")
print(k,"orig",org.size,"novo",new.size, "ratio", round(new.width/new.height,3))
W=900
a=org.resize((W,int(W*org.height/org.width))); b=new.resize((W,int(W*new.height/new.width)))
h=max(a.height,b.height)
c=Image.new("RGB",(2*W+10,h),"white"); c.paste(a,(0,0)); c.paste(b,(W+10,0))
c.save(rf"{D}\_comparar\{k}.jpg",quality=88)
