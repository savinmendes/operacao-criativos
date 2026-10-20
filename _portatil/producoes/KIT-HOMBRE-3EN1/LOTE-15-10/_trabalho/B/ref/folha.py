import cv2, sys
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(v); fps = cap.get(5); n = int(cap.get(7)); dur = n / fps
ims = []
t = 0.0
while t < dur:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps)); ok, f = cap.read()
    if not ok: break
    im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).resize((144, 256))
    ImageDraw.Draw(im).rectangle((0, 0, 40, 16), fill="black"); ImageDraw.Draw(im).text((3, 2), f"{t:.0f}", fill="yellow")
    ims.append(im); t += 1
cols = 10; rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (144 * cols, 256 * rows))
for i, im in enumerate(ims): c.paste(im, ((i % cols) * 144, (i // cols) * 256))
c.save(out)
