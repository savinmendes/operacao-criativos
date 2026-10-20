import os, glob
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("arial.ttf", 22)
for d in sorted(glob.glob("frames/*")):
    id_ = os.path.basename(d); fs = sorted(glob.glob(d + "/f_*.jpg"))
    ims = [Image.open(f) for f in fs]; w = 240; h = int(ims[0].height * w / ims[0].width)
    cols = 6; rows = (len(ims) + cols - 1) // cols
    S = Image.new("RGB", (cols * w, rows * h), "black"); dr = ImageDraw.Draw(S)
    for i, im in enumerate(ims):
        x, y = (i % cols) * w, (i // cols) * h; S.paste(im.resize((w, h)), (x, y))
        dr.rectangle([x, y, x + 60, y + 28], fill="black"); dr.text((x + 4, y + 2), f"{i}s", fill="yellow", font=F)
    S.save(f"folhas/{id_}_folha.jpg", quality=85)
