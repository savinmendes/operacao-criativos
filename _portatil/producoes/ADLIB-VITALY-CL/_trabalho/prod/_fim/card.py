from PIL import Image, ImageDraw, ImageFilter
F = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts"
from PIL import ImageFont
def f(n, s): return ImageFont.truetype(F+"\\"+n, s)
S = 1600
kit = Image.open(r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\_trabalho\ad04\kit3_quadrado.jpg").convert("RGB")
c = Image.new("RGB", (S, S), (246, 241, 226))
bg = kit.resize((S, S)).crop((0, 0, S, 720)).filter(ImageFilter.GaussianBlur(30))
c.paste(bg, (0, 0))
k = kit.resize((700, 700)); c.paste(k, ((S-700)//2, 10))
d = ImageDraw.Draw(c)
G = (22, 74, 52); CREAM = (246, 241, 226)
d.rectangle([0, 720, S, 800], fill=G)
t = "OFERTA LYMPHORIA"
d.text((S//2, 760), t, font=f("Poppins-Bold.ttf", 60), fill=CREAM, anchor="mm")
rows = [("Compre 1, Reciba 2", "$34.990"), ("Compre 2, Reciba 4", "$59.990"), ("Compre 3, Reciba 6", "$79.990")]
y = 840
for i, (a, b) in enumerate(rows):
    box = [70, y, S - 70, y + 170]
    if i == 0:
        d.rounded_rectangle(box, 30, fill=(255, 214, 64), outline=G, width=6)
    else:
        d.rounded_rectangle(box, 30, fill=(255, 255, 255), outline=G, width=4)
    d.text((120, y + 85), a, font=f("Poppins-Bold.ttf", 66), fill=G, anchor="lm")
    d.text((S - 120, y + 85), b, font=f("Poppins-Bold.ttf", 78), fill=(180, 20, 20), anchor="rm")
    y += 200
d.text((S//2, 1490), "Envío gratis · Pagas al recibir · Garantía 90 días", font=f("Poppins-SemiBold.ttf", 52), fill=G, anchor="mm")
c.save("oferta_card.jpg", quality=95)
