# folha da boca nas pausas (itens.json) + 1o/último quadro de um take HeyGen
import sys, json, subprocess
from PIL import Image
i, f = sys.argv[1], sys.argv[2]; box = [int(x) for x in sys.argv[3].split(",")]  # x,y,w,h no 720x1280
it = json.load(open("audio/itens.json", encoding="utf-8"))[i]
ts = [0.0] + [round((a + b) / 2, 2) for a, b in it["pausas"][1:-1]] + [it["palavras"][-1]["fim"] + 0.1]
ims = []
for t in ts:
    o = f"qa/_{i}_{t}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", o]); im = Image.open(o)
    ims.append(im.crop((box[0], box[1], box[0] + box[2], box[1] + box[3])).resize((160, 160)))
s = Image.new("RGB", (160 * len(ims), 160))
for k, im in enumerate(ims): s.paste(im, (160 * k, 0))
s.save(f"qa/{i}_pausas.jpg"); print(i, ts)
