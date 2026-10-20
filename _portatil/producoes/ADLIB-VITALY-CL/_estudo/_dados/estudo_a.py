import glob, os, subprocess, io, json, sys
from PIL import Image, ImageDraw, ImageFont
B = r"C:/Users/PICHAU/Downloads/ADLIB-VITALY-CL"
OUT = B + "/_estudo"; D = OUT + "/_dados"
NUMS = sys.argv[1].split(",")
f = ImageFont.truetype("arialbd.ttf", 20)
vids = {n: glob.glob(B + f"/VIDEOS/{n} - *.mp4")[0] for n in NUMS}
# 1) whisper
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=3)
for i, (n, p) in enumerate(vids.items(), 1):
    js = f"{D}/V{n}_whisper.json"
    if os.path.exists(js): continue
    segs, info = m.transcribe(p, language="es", word_timestamps=True, vad_filter=False)
    res = [{"ini": round(s.start,2), "fim": round(s.end,2), "txt": s.text.strip(),
            "words": [[round(w.start,2), round(w.end,2), w.word] for w in s.words]} for s in segs]
    json.dump(res, open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[whisper {i}/{len(vids)}] V{n} ok", flush=True)
del m
# 2) frames 1/s + contact sheet
for n, p in vids.items():
    fd = f"{D}/V{n}_frames"; os.makedirs(fd, exist_ok=True)
    if not glob.glob(fd + "/*.jpg"):
        subprocess.run(["ffmpeg","-v","error","-i",p,"-vf","fps=1:start_time=0,scale=720:-2","-q:v","3",fd+"/f%03d.jpg"])
    fr = sorted(glob.glob(fd + "/*.jpg"))
    cols, W, H = 8, 200, 356
    rows = (len(fr)+cols-1)//cols
    S = Image.new("RGB", (cols*W, rows*(H+26)), "white"); d = ImageDraw.Draw(S)
    for k, fp in enumerate(fr):
        im = Image.open(fp).convert("RGB"); im.thumbnail((W, H))
        x = (k%cols)*W; y = (k//cols)*(H+26)
        S.paste(im, (x+(W-im.width)//2, y+26)); d.text((x+4, y+3), f"{k}s", fill="red", font=f)
    S.save(f"{OUT}/folhas/V{n}_folha.jpg", quality=85)
    print(f"[folha] V{n} {len(fr)} quadros", flush=True)
# 3) OCR (sequential)
from rapidocr_onnxruntime import RapidOCR
ocr = RapidOCR()
for n in vids:
    js = f"{D}/V{n}_ocr.json"
    if os.path.exists(js): continue
    out = []
    for k, fp in enumerate(sorted(glob.glob(f"{D}/V{n}_frames/*.jpg"))):
        r, _ = ocr(fp)
        out.append({"t": k, "txt": [[x[1], round(float(x[2]),2), [int(x[0][0][1]), int(x[0][2][1])]] for x in (r or [])]})
    json.dump(out, open(js, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[ocr] V{n} ok", flush=True)
