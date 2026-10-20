import glob, json
from PIL import Image
SRC = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL/IMAGENS/"
CROPS = {
 "02": (0,60,500,1350),
 "04": (1060,590,1580,1990),
 "06": (1040,1095,1480,1822),
 "07": (120,600,1330,1730),
 "08": (760,1130,1060,1870),
 "13": (640,860,950,1500),
 "15": (640,560,990,1520),
 "16": (700,430,930,1030),
 "18": (920,1120,1180,1890),
 "21": (330,495,760,1180),
 "27": (330,700,780,1660),
 "28": (1260,1100,1560,1890),
}
json.dump(CROPS, open("crops.json","w"))
for n,b in CROPS.items():
    f = glob.glob(SRC+n+" - *.jpg")[0]
    im = Image.open(f).convert("RGB")
    c = im.crop(b); c.save(f"crops/{n}.png")
    print(n, im.size, c.size, round(c.size[0]/c.size[1],3))
