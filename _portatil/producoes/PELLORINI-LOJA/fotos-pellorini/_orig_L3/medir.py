import json,urllib.request,io
from PIL import Image
L=json.load(open('lotes/L3_caramelo-b.json'))
R={"1:1":1,"4:5":.8,"3:4":.75,"2:3":2/3,"9:16":9/16,"16:9":16/9}
for it in L:
    u=it['url']+('&' if '?' in it['url'] else '?')+'width=2048'
    d=urllib.request.urlopen(u).read()
    im=Image.open(io.BytesIO(d)).convert('RGB')
    im.save(f"_orig_L3/{it['handle']}_{it['pos']}.png")
    r=im.width/im.height
    best=min(R,key=lambda k:abs(R[k]-r))
    print(it['handle'],it['pos'],im.size,round(r,3),best)
