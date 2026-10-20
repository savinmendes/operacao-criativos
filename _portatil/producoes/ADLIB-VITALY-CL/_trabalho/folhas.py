import glob, os, subprocess, io
from PIL import Image, ImageDraw, ImageFont
B = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL"
f = ImageFont.truetype("arialbd.ttf", 22)
def sheet(items, out, cols=5, W=300, H=533):
    rows = (len(items)+cols-1)//cols
    S = Image.new("RGB", (cols*W, rows*(H+34)), "white"); d = ImageDraw.Draw(S)
    for k, (lab, im) in enumerate(items):
        im.thumbnail((W, H)); x = (k%cols)*W; y = (k//cols)*(H+34)
        S.paste(im, (x+(W-im.width)//2, y+34)); d.text((x+6, y+5), lab, fill="black", font=f)
    S.save(out, quality=88)
vids = []
for p in sorted(glob.glob(B+"/VIDEOS/*.mp4")):
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
    fr = []
    for t in (0.5, dur*0.5):
        b = subprocess.run(["ffmpeg","-v","error","-ss",str(t),"-i",p,"-frames:v","1","-f","image2pipe","-vcodec","png","-"],capture_output=True).stdout
        fr.append(Image.open(io.BytesIO(b)).convert("RGB"))
    n = os.path.basename(p)[:2]
    vids.append((f"{n} ({dur:.0f}s) ini", fr[0])); vids.append((f"{n} meio", fr[1]))
sheet(vids, B+"/00-folha-videos.jpg", cols=6, W=240, H=427)
ims = [(os.path.basename(p)[:2], Image.open(p).convert("RGB")) for p in sorted(glob.glob(B+"/IMAGENS/*.jpg"))]
sheet(ims, B+"/00-folha-imagens.jpg", cols=5, W=300, H=400)
