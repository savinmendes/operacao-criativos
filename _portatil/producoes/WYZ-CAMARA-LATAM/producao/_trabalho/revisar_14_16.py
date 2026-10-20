# Revisao: whisper es + en, busca de termos proibidos, folha de contato 1 q/s, silencio no fim.
import json, re, subprocess, sys
from pathlib import Path
from faster_whisper import WhisperModel
from PIL import Image, ImageDraw
v = Path(sys.argv[1]); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
res = {}
for lang in ("es", "en"):
    segs, info = m.transcribe(str(v), language=lang, vad_filter=False, beam_size=5)
    res[lang] = " ".join(s.text.strip() for s in segs)
proib = r"precio|\$|d[oó]lar|descuento|oferta|navidad|año nuevo|tiktok|link|enlace|carrito|naranja|agotad|stock|wyze\.com|semanas sin sol|sin sol|pies|chile|m[eé]xico|colombia|per[uú]|estados unidos|am[eé]rica|garant|env[ií]o|gratis"
res["proibidos_es"] = sorted(set(x.lower() for x in re.findall(proib, res["es"], re.I)))
# silencio no fim
r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(v), "-af", "silencedetect=n=-45dB:d=0.8", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
res["silencios"] = re.findall(r"silence_(?:start|end): [0-9.]+", r)
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(v)],
                         capture_output=True, text=True).stdout); res["duracao"] = d
# folha 1 q/s
fr = out / "fr"; fr.mkdir(exist_ok=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-i", str(v), "-vf", "fps=1,scale=180:-1", str(fr / "%03d.jpg")], check=True)
fs = sorted(fr.glob("*.jpg")); ims = [Image.open(f) for f in fs]; w, h = ims[0].size; cols = 10
M = Image.new("RGB", (w * cols, h * ((len(ims) + cols - 1) // cols)))
for i, im in enumerate(ims):
    ImageDraw.Draw(im).text((4, 4), f"{i}s", fill=(255, 255, 0)); M.paste(im, ((i % cols) * w, (i // cols) * h))
M.save(out / "folha_1s.jpg")
json.dump(res, open(out / "revisao.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
