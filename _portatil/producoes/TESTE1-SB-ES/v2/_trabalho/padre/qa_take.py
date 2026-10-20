# -*- coding: utf-8 -*-
"""QA de um take: folha com rosto em início/pausas/fim + tira de boca a cada 2 quadros + energia de movimento da boca.
Uso: python qa_take.py P1   (lê takes/P1_raw.mp4 e audio/itens.json)"""
import sys, json, subprocess, numpy as np
from pathlib import Path
from PIL import Image, ImageDraw
AQ = Path(__file__).resolve().parent; iid = sys.argv[1]; vid = AQ / "takes" / f"{iid}_raw.mp4"
it = json.load(open(AQ / "audio" / "itens.json", encoding="utf-8"))[iid]
pr = json.loads(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height,r_frame_rate", "-of", "json", str(vid)], capture_output=True, text=True).stdout)["streams"][0]
W, H = pr["width"], pr["height"]; fps = eval(pr["r_frame_rate"])
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(vid), "-vf", "scale=720:1280", "-pix_fmt", "rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
FACE = (250, 380, 470, 700); MOUTH = (300, 545, 420, 625)   # em 720x1280
def crop(f, b): return Image.fromarray(f[b[1]:b[3], b[0]:b[2]])
# energia de movimento da boca por quadro
mo = np.array([np.abs(F[k + 1, MOUTH[1]:MOUTH[3], MOUTH[0]:MOUTH[2]].astype(int) - F[k, MOUTH[1]:MOUTH[3], MOUTH[0]:MOUTH[2]].astype(int)).mean() for k in range(len(F) - 1)])
marcas = [("ini", 0.0), ("ini+.1", 0.1)] + [(f"pausa {a:.2f}-{b:.2f}", (a + b) / 2) for a, b in it["pausas"][1:-1]] + [("fim-.1", it["dur"] - 0.1), ("fim", len(F) / fps - 0.02)]
tiles = []
for nome, t in marcas:
    k = min(int(t * fps), len(F) - 1); im = crop(F[k], FACE).resize((220, 320)); d = ImageDraw.Draw(im); d.rectangle((0, 0, 220, 18), fill=(0, 0, 0)); d.text((3, 3), f"{nome} q{k}", fill=(255, 255, 0)); tiles.append(im)
cols = min(len(tiles), 6); rows = (len(tiles) + cols - 1) // cols
S = Image.new("RGB", (cols * 220, rows * 320)); [S.paste(t, ((i % cols) * 220, (i // cols) * 320)) for i, t in enumerate(tiles)]
S.save(AQ / "qa" / f"{iid}_pausas.jpg", quality=88)
# tira de boca: todos os quadros (a cada 2), 20 por linha
ks = list(range(0, len(F), 2)); cw, ch = 120, 80; cols = 20; rows = (len(ks) + cols - 1) // cols
T = Image.new("RGB", (cols * cw, rows * (ch + 12)), (30, 30, 30)); d = ImageDraw.Draw(T)
for i, k in enumerate(ks):
    x, y = (i % cols) * cw, (i // cols) * (ch + 12); T.paste(crop(F[k], MOUTH), (x, y + 12)); d.text((x + 2, y), f"{k / fps:.2f}", fill=(255, 255, 255))
T.save(AQ / "qa" / f"{iid}_boca.jpg", quality=85)
print(f"{iid}: {W}x{H} {fps:.2f}fps {len(F)} quadros ({len(F) / fps:.2f}s, audio {it['dur']}s)")
for a, b in it["pausas"]:
    ka, kb = int(a * fps), max(int(b * fps), int(a * fps) + 1); print(f"  pausa {a:.2f}-{b:.2f} mov boca {mo[ka:kb].mean():.2f}")
print(f"  mov médio em fala {mo.mean():.2f}")
