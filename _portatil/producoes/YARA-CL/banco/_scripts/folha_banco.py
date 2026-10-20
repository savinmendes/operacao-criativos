# folha_banco.py [--qa] -> folha_banco.jpg (1 quadro do meio por take) ou _folhas/qa_*.jpg (3 quadros por take)
import json, subprocess, sys, os, io
from PIL import Image, ImageDraw, ImageFont
B = r"C:\Users\PICHAU\Downloads\YARA-CL\banco"
idx = json.load(open(os.path.join(B, "indice.json"), encoding="utf-8"))
qa = "--qa" in sys.argv
try:
    F = ImageFont.truetype("arialbd.ttf", 22); f2 = ImageFont.truetype("arial.ttf", 15)
except Exception:
    F = f2 = ImageFont.load_default()
def quadro(v, t, w):
    o = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", v, "-frames:v", "1", "-vf", f"scale={w}:-2", "-f", "image2", "-c:v", "png", "-"], capture_output=True).stdout
    return Image.open(io.BytesIO(o)).convert("RGB")
if not qa:
    w = 216; cols = 10; tiles = []
    for e in idx:
        im = quadro(os.path.join(B, e["arquivo"]), e["duracao_s"] / 2, w)
        d = ImageDraw.Draw(im); d.rectangle([0, 0, w, 30], fill=(0, 0, 0))
        d.text((5, 3), e["arquivo"].replace(".mp4", ""), fill="yellow", font=F)
        d.rectangle([0, im.height - 22, w, im.height], fill=(0, 0, 0))
        d.text((4, im.height - 20), e["acao"][:30], fill="white", font=f2)
        tiles.append(im)
    rows = (len(tiles) + cols - 1) // cols; h = tiles[0].height
    s = Image.new("RGB", (cols * w, rows * h), "black")
    for i, im in enumerate(tiles): s.paste(im, ((i % cols) * w, (i // cols) * h))
    s.save(os.path.join(B, "folha_banco.jpg"), quality=85); print("ok", len(tiles))
else:
    w = 150; grupos = {}
    for e in idx: grupos.setdefault(e["arquivo"].split("_")[0], []).append(e)
    for g, es in grupos.items():
        rows = []
        for e in es:
            v = os.path.join(B, e["arquivo"]); D = e["duracao_s"]
            ims = [quadro(v, t, w) for t in (0.05, D * 0.25, D * 0.5, D * 0.75, max(D - 0.1, 0))]
            r = Image.new("RGB", (w * 5, ims[0].height), "black")
            for i, im in enumerate(ims): r.paste(im, (i * w, 0))
            ImageDraw.Draw(r).text((4, 2), e["arquivo"], fill="yellow", font=f2); rows.append(r)
        cols = 2; rh = rows[0].height; n = (len(rows) + 1) // 2
        s = Image.new("RGB", (w * 5 * cols + 10, n * rh), "black")
        for i, r in enumerate(rows): s.paste(r, ((i % cols) * (w * 5 + 10), (i // cols) * rh))
        s.save(os.path.join(B, "_folhas", f"qa_{g}.jpg"), quality=80); print(g, len(rows))
