import json,requests,io
from PIL import Image
L=json.load(open(r"C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini\lotes\L1_verde-agua.json"))
R={"1:1":1,"4:5":.8,"3:4":.75,"2:3":2/3,"9:16":9/16,"16:9":16/9}
for it in L:
    u=it["url"]; sep="&" if "?" in u else "?"
    b=requests.get(u+sep+"width=2048",timeout=60).content
    im=Image.open(io.BytesIO(b)).convert("RGB")
    im.save(rf"C:\Users\PICHAU\Downloads\PELLORINI-LOJA\fotos-pellorini\_orig_L1\{it['handle']}_{it['pos']}.jpg",quality=95)
    r=im.width/im.height
    ar=min(R,key=lambda k:abs(R[k]-r))
    print(it['handle'],it['pos'],im.size,round(r,3),ar)
