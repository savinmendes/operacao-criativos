# -*- coding: utf-8 -*-
"""Remove de imagens/ o que não está citado no anuncios.md atual e refaz as folhas de contato."""
import os, re, glob
from PIL import Image, ImageDraw
for md in sorted(glob.glob("*/anuncios.md")):
    pasta = os.path.dirname(md)
    txt = open(md, encoding="utf-8").read()
    usados = set(re.findall(r"(\d{3}_[a-z_]+_\d+d_\d+(?:_c\d+)?\.jpg)(?! \(repetida\))", txt))
    d = os.path.join(pasta, "imagens"); tudo = os.listdir(d)
    rem = [f for f in tudo if f not in usados]
    for f in rem: os.remove(os.path.join(d, f))
    for f in glob.glob(os.path.join(pasta, "folha_*.jpg")): os.remove(f)
    fotos = sorted(f for f in os.listdir(d) if f.endswith(".jpg"))
    for fo in range(0, len(fotos), 24):
        lote = fotos[fo:fo+24]; W = 300; cols = 6; rows = (len(lote)+cols-1)//cols
        folha = Image.new("RGB", (cols*W, rows*(W+28)), "white"); dr = ImageDraw.Draw(folha)
        for i, f in enumerate(lote):
            im = Image.open(os.path.join(d, f)); im.thumbnail((W, W))
            x, y = (i % cols)*W, (i//cols)*(W+28)
            folha.paste(im, (x + (W-im.width)//2, y + (W-im.height)//2))
            dr.text((x+4, y+W+6), "_".join(f.split("_")[:3]), fill="black")
        folha.save(os.path.join(pasta, f"folha_{fo//24+1:02d}.jpg"), quality=85)
    print(f"{pasta:15} removidas {len(rem):5} | ficaram {len(fotos):5} | folhas {(len(fotos)+23)//24}")
