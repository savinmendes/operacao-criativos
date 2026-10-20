import subprocess,sys
from PIL import Image,ImageDraw
V=r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4"
pts=[(75,'p'),(125,'p'),(200,'p'),(245,'w1'),(282,'m'),(298,'m'),(316,'w2'),(372,'p'),(455,'p'),(545,'p'),(690,'p'),(790,'p'),(905,'p'),(1030,'p'),(1110,'p'),(1290,'p'),(1500,'p'),(1640,'p'),(1745,'p'),(1915,'c'),(2010,'c'),(2150,'c'),(2270,'c'),(1446,'p')]
box={'p':(170,20,470,320),'w1':(170,330,470,630),'m':(200,20,500,320),'w2':(60,150,660,750),'c':(100,0,520,420)}
ims=[]
for t,k in pts:
    f=f"mouth/{t}.png"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",V,"-frames:v","1",f],check=True)
    im=Image.open(f).crop(box[k]).resize((360,360));d=ImageDraw.Draw(im);d.rectangle([0,0,70,20],fill='yellow');d.text((3,3),f"{int(t//60):02d}:{t%60:04.1f}",fill='black');ims.append(im)
for s in range(0,len(ims),8):
    out=Image.new('RGB',(4*360,2*360))
    for i,im in enumerate(ims[s:s+8]): out.paste(im,((i%4)*360,(i//4)*360))
    out.save(f"mouth/sheet{s//8}.jpg",quality=90)
