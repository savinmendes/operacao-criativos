from PIL import Image, ImageDraw, ImageFont
import numpy as np
NAVY = (16, 48, 85)
src = Image.open(r"..\estudo\body20.png").convert("RGB")
im = Image.new("RGBA", (720, 1280), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
W = 530; y0, y1 = 28, 116
d.rounded_rectangle([-30, y0, W, y1], radius=20, fill=NAVY + (255,))
f1 = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 26)
f2 = ImageFont.truetype(r"C:\Windows\Fonts\segoeuib.ttf", 19)
d.text((40, 61), "PŁATNOŚĆ PRZY ODBIORZE", font=f1, fill="white", anchor="lm")
d.text((40, 90), "WYSYŁKA W 24 GODZINY", font=f2, fill="white", anchor="lm")
print("larg1", d.textlength("PŁATNOŚĆ PRZY ODBIORZE", font=f1), "larg2", d.textlength("WYSYŁKA W 24 GODZINY", font=f2))
# caminhao do original (branco sobre azul) -> alfa pelo brilho
tr = np.array(src.crop((360, 44, 460, 102))).astype(float); lum = tr.mean(2)
a = np.clip((lum - 70) / (230 - 70), 0, 1)
t = np.zeros((tr.shape[0], tr.shape[1], 4), np.uint8); t[..., :3] = 255; t[..., 3] = (a * 255).astype(np.uint8)
im.alpha_composite(Image.fromarray(t), (W - 112, 44))
im.save("selo_pl.png")
prev = src.convert("RGBA"); prev.alpha_composite(im); prev.crop((0, 0, 720, 160)).resize((1440, 320)).save("selo_prev.png")
