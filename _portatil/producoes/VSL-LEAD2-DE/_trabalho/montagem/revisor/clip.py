import sys,subprocess,glob,os,shutil
from PIL import Image,ImageDraw
a,d,fps,name=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
shutil.rmtree('ev',ignore_errors=True);os.makedirs('ev')
subprocess.run(["ffmpeg","-v","error","-y","-ss",str(a),"-t",str(d),"-i",r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\VSL-LEAD2-DE.mp4","-vf",f"fps={fps},scale=150:200","ev/%04d.png"])
fs=sorted(glob.glob('ev/*.png'));cols=10;rows=(len(fs)+cols-1)//cols
o=Image.new('RGB',(cols*150,rows*200))
for i,f in enumerate(fs):
    im=Image.open(f);dr=ImageDraw.Draw(im);t=a+i/fps;dr.rectangle([0,185,60,200],fill='yellow');dr.text((2,186),f"{int(t//60)}:{t%60:05.2f}",fill='black');o.paste(im,((i%cols)*150,(i//cols)*200))
o.save(f'z/{name}.jpg',quality=85)
