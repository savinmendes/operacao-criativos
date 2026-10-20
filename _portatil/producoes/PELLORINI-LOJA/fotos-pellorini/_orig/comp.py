import urllib.request,io,sys
from PIL import Image,ImageDraw
J={'pellorini-silk-cleaning-cloth_0':('877f9961-81bf-4510-94a3-1c124fcf3bda',(0.45,0.55,0.85,0.85)),
'pellorini-silk-cleaning-cloth_1':('5a542549-b149-4713-a2e3-6dc537077fb1',(0.35,0.50,0.85,0.85)),
'pellorini-silk-cleaning-cloth_2':('85eff520-27c3-4886-9733-5fa6f59d9daa',(0.25,0.40,0.75,0.75)),
'premium-pellorini-box_0':('e5323855-e9af-43fb-abb7-1f441e5d2cbd',(0.10,0.25,0.50,0.50)),
'premium-pellorini-box_1':('6c488e8c-318a-4501-bf09-565f7ea9d6e4',(0.25,0.25,0.75,0.55)),
'pellorini-parchment-gift-bag_0':('741aee45-82ca-4794-a3ea-dbf7974b024c',(0.30,0.35,0.85,0.72)),
'pellorini-parchment-gift-bag_1':('282481bc-f731-414f-ba97-508b45e55ca4',(0.05,0.20,0.95,0.70)),}
only=sys.argv[1:]
for k,(u,box) in J.items():
  if only and k not in only: continue
  d=urllib.request.urlopen(urllib.request.Request(f'https://media.flora.ai/node-inputs/2026/10/11/anonymous/{u}.png',headers={'User-Agent':'Mozilla/5.0'})).read()
  B=Image.open(io.BytesIO(d)).convert('RGB'); A=Image.open(f'_orig/{k}.png').convert('RGB')
  print(k,'out',B.size,'orig',A.size)
  B.save(f'{k}.jpg',quality=94)
  S=900; a=A.resize((S,S)); b=B.resize((S,S))
  def cr(im): w,h=im.size; c=im.crop((int(box[0]*w),int(box[1]*h),int(box[2]*w),int(box[3]*h))); r=S/c.width; return c.resize((S,int(c.height*r)))
  ca,cb=cr(A),cr(B)
  W=Image.new('RGB',(2*S+10,S+ca.height+10),'white')
  W.paste(a,(0,0));W.paste(b,(S+10,0));W.paste(ca,(0,S+10));W.paste(cb,(S+10,S+10))
  W.save(f'_comparar/{k}.jpg',quality=88)
