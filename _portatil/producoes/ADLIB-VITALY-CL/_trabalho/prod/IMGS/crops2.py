import glob, json
from PIL import Image
SRC = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL/IMAGENS/"
C = json.load(open("crops.json"))
R = {"07":1.0,"06":2/3,"21":2/3}
out={}
for n,(x0,y0,x1,y1) in C.items():
    f = glob.glob(SRC+n+" - *.jpg")[0]
    im = Image.open(f).convert("RGB"); W,H = im.size
    r = R.get(n, 9/16)
    w,h = x1-x0, y1-y0
    if w/h < r:
        nw = round(h*r); cx=(x0+x1)/2
        x0 = round(cx-nw/2); x1 = x0+nw
        if x0<0: x1-=x0; x0=0
        if x1>W: x0-=x1-W; x1=W
    else:
        nh = round(w/r); cy=(y0+y1)/2
        y0 = round(cy-nh/2); y1=y0+nh
        if y0<0: y1-=y0; y0=0
        if y1>H: y0-=y1-H; y1=H
    out[n]=(x0,y0,x1,y1)
    c=im.crop((x0,y0,x1,y1)); c.save(f"crops/{n}.png")
    print(n,(x0,y0,x1,y1),c.size,round(c.size[0]/c.size[1],3))
json.dump(out,open("crops.json","w"))
