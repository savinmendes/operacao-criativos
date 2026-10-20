import subprocess,numpy as np,sys
from PIL import Image,ImageDraw
V=sys.argv[1]; W,H=1080,1920
p=subprocess.run(["ffmpeg","-v","error","-i",V,"-f","rawvideo","-pix_fmt","rgb24","-"],capture_output=True).stdout
fr=np.frombuffer(p,np.uint8).reshape(-1,H,W,3); print(len(fr))
np.save("luma.npy",fr.mean(axis=(1,2,3)))
# mosaics every 0.5s (15 frames), 8x2 per image, 270x480
idx=list(range(0,len(fr),15))+[len(fr)-1]
for k in range(0,len(idx),16):
  im=Image.new("RGB",(270*8,480*2))
  for j,i in enumerate(idx[k:k+16]):
    t=Image.fromarray(fr[i]).resize((270,480)); d=ImageDraw.Draw(t); d.rectangle([0,0,70,18],fill=(0,0,0)); d.text((3,3),f"{i/30:.2f}",fill=(255,0,0))
    im.paste(t,((j%8)*270,(j//8)*480))
  im.save(f"mos_{k//16:02d}.jpg",quality=85)
# subtitle-area larger crops: bottom half area
for k in range(0,len(idx),12):
  im=Image.new("RGB",(540*3,480*4))
  for j,i in enumerate(idx[k:k+12]):
    t=Image.fromarray(fr[i][960:1920]).resize((540,480)); d=ImageDraw.Draw(t); d.rectangle([0,0,70,18],fill=(0,0,0)); d.text((3,3),f"{i/30:.2f}",fill=(255,0,0))
    im.paste(t,((j%3)*540,(j//3)*480))
  im.save(f"leg_{k//12:02d}.jpg",quality=85)
# mouth crops every frame in face ranges
for n,(a,b) in enumerate([(0,5.7),(5.7,10.1),(15.4,18.1),(22.9,26.95)]):
  fs=list(range(int(a*30),min(int(b*30),len(fr)),2))
  cols=10; rows=(len(fs)+cols-1)//cols
  im=Image.new("RGB",(200*cols,150*rows))
  for j,i in enumerate(fs):
    t=Image.fromarray(fr[i][720:1050,280:800]).resize((200,127)); 
    c=Image.new("RGB",(200,150)); c.paste(t,(0,0)); d=ImageDraw.Draw(c); d.text((3,130),f"{i/30:.2f}",fill=(255,255,0))
    im.paste(c,((j%cols)*200,(j//cols)*150))
  im.save(f"boca_{n}.jpg",quality=85)
d=np.abs(np.diff(fr[:,::8,::8].astype(np.int16),axis=0)).mean(axis=(1,2,3))
np.save("diff.npy",d)
for i in np.argsort(d)[::-1][:20]: print(f"cut {i+1} t={(i+1)/30:.2f} d={d[i]:.1f}")
# arrow check: last 20 frames yellow pixel count in lower area
for i in [690,700,len(fr)-30,len(fr)-1]:
  f=fr[i].astype(int); y=(f[...,0]>200)&(f[...,1]>180)&(f[...,2]<90); print("yellow",i/30,y.sum(), np.argwhere(y).mean(0) if y.sum() else None)
