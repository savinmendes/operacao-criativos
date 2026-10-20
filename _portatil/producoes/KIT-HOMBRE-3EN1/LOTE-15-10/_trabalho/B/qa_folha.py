import cv2, sys
from PIL import Image, ImageDraw
v, out = sys.argv[1], sys.argv[2]; passo = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
cap = cv2.VideoCapture(v); fps = cap.get(5); n = int(cap.get(7)); ims = []; t = 0.0
while t < n / fps - 0.01:
    cap.set(cv2.CAP_PROP_POS_FRAMES, int(round(t * fps))); ok, f = cap.read()
    if not ok: break
    im = Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).resize((216, 384))
    d = ImageDraw.Draw(im); d.rectangle((0, 0, 44, 16), fill="black"); d.text((3, 2), f"{t:.1f}", fill="yellow")
    ims.append(im); t += passo
cols = 7; rows = (len(ims) + cols - 1) // cols
c = Image.new("RGB", (216 * cols, 384 * rows))
for i, im in enumerate(ims): c.paste(im, ((i % cols) * 216, (i // cols) * 384))
c.save(out, quality=85)
