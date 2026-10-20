import subprocess,io
from PIL import Image,ImageDraw
def frames(V,t0,n,box):
    b=subprocess.run(["ffmpeg","-v","error","-ss",f"{t0:.3f}","-i",V,"-frames:v",str(n),"-vf",f"crop={box[2]}:{box[3]}:{box[0]}:{box[1]}","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
    out=[];i=0
    while True:
        j=b.find(b"\x89PNG",i+1)
        out.append(Image.open(io.BytesIO(b[i:j if j>0 else None])).convert("RGB"))
        if j<0:break
        i=j
    return out
IT=r"C:\Users\PICHAU\Downloads\SB-IT-OFERTA-LIVE\01_ADS-9\SB-IT-ADS-9.mp4"
EN=r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\01_ADS-9\SB-EN-ADS-9.mp4"
for nm,V in (("it",IT),("en",EN)):
    fs=frames(V,97.50,12,(0,300,720,300))
    S=Image.new("RGB",(360*4,150*3))
    for k,f in enumerate(fs[:12]):
        f=f.resize((360,150));ImageDraw.Draw(f).text((3,3),f"{97.5+k/30:.2f}",fill=(255,255,0));S.paste(f,((k%4)*360,(k//4)*150))
    S.save(f"badge_{nm}.jpg")
