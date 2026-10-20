# desfoca marcas de terceiros (cerveja, roupa) na cena S3 antes do Kling
from PIL import Image, ImageFilter
im = Image.open("cenas/S3_celulares.png").convert("RGB")
caixas = [(0, 950, 40, 1035), (232, 972, 300, 1080), (440, 1140, 522, 1235), (695, 1140, 720, 1235),
          (360, 715, 425, 745), (180, 728, 230, 760), (505, 700, 565, 770)]
for b in caixas:
    r = im.crop(b).filter(ImageFilter.GaussianBlur(9)); im.paste(r, b)
im.save("cenas/S3_celulares_limpa.png")
