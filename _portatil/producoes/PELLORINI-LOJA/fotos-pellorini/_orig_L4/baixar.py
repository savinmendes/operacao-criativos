import json,urllib.request,io,os
from PIL import Image
J=json.load(open('resultado_L4.json',encoding='utf-8'))
for e in J:
  n=f"{e['handle']}_{e['pos']}"
  p=f'_orig_L4/{n}.png'
  if not os.path.exists(p):
    d=urllib.request.urlopen(urllib.request.Request(e['url_original'],headers={'User-Agent':'Mozilla/5.0'})).read()
    Image.open(io.BytesIO(d)).convert('RGB').save(p)
  o=Image.open(p);g=Image.open(f'{n}.jpg')
  print(n,o.size,g.size)
  S=700;im=Image.new('RGB',(2*S,S));im.paste(o.convert('RGB').resize((S,S)),(0,0));im.paste(g.convert('RGB').resize((S,S)),(S,0));im.save(f'_orig_L4/ov_{n}.jpg',quality=85)
