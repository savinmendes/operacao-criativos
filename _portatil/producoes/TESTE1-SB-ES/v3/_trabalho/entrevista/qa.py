# -*- coding: utf-8 -*-
"""QA de um take: whisper es (palavras) vs texto, folhas de boca (inicio/fim/pausas) e regiao extra (colar).
Uso: python qa.py <id> take.mp4 boca=x0,y0,x1,y1 [extra=x0,y0,x1,y1]"""
import sys, json, re, unicodedata, subprocess, cv2, numpy as np
from pathlib import Path
from faster_whisper import WhisperModel
AQ = Path(__file__).resolve().parent; QA = AQ / "qa"; QA.mkdir(exist_ok=True)
i, v = sys.argv[1], sys.argv[2]; kw = dict(a.split("=") for a in sys.argv[3:])
P = json.loads((AQ / "audio" / "partes.json").read_text(encoding="utf-8"))[i]
def norm(s): return re.sub(r"[^a-z0-9 ]", "", unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()).split()
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(v, language="es", word_timestamps=True, beam_size=5, initial_prompt="Grimorio Sagrado y Secreto de San Benito. Don Aurelio.")
W = [dict(w=w.word.strip(), ini=round(w.start, 3), fim=round(w.end, 3), p=round(w.probability, 2)) for s in segs for w in s.words]
txt = " ".join(w["w"] for w in W); a, b = norm(P["texto"]), norm(txt)
import difflib
sm = difflib.SequenceMatcher(None, a, b); dif = [(op, " ".join(a[i1:i2]), " ".join(b[j1:j2])) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
cap = cv2.VideoCapture(v); fps = cap.get(cv2.CAP_PROP_FPS); N = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W0, H0 = int(cap.get(3)), int(cap.get(4)); frames = []
while True:
    ok, f = cap.read()
    if not ok: break
    frames.append(f)
dur = len(frames) / fps
ad = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout.strip() or 0)
def sheet(nome, ivs, box, cols=10, w=180):
    x0, y0, x1, y1 = map(int, box.split(",")); tiles = []
    for k, f in enumerate(frames):
        t = k / fps
        if any(p <= t <= q for p, q in ivs):
            c = cv2.resize(f[y0:y1, x0:x1], (w, int(w * (y1 - y0) / (x1 - x0))))
            cv2.putText(c, f"{t:.2f}", (3, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2); tiles.append(c)
    if not tiles: return
    h = tiles[0].shape[0]; rows = (len(tiles) + cols - 1) // cols; img = np.zeros((rows * h, cols * w, 3), np.uint8)
    for k, c in enumerate(tiles): img[k // cols * h:(k // cols + 1) * h, k % cols * w:(k % cols + 1) * w] = c
    cv2.imwrite(str(QA / f"{i}_{nome}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 85])
ivs = [(0, 0.45), (dur - 0.6, dur)] + [(p - 0.06, q + 0.06) for p, q in P["pausas_restantes"]]
sheet("boca", ivs, kw["boca"])
if "extra" in kw: sheet("colar", [(t, t + 0.001) for t in np.arange(0, dur, 0.4)], kw["extra"], cols=8, w=160)
# quadro inteiro a cada ~1/6
idx = np.linspace(0, len(frames) - 1, 6).astype(int)
cv2.imwrite(str(QA / f"{i}_full.jpg"), np.hstack([cv2.resize(frames[k], (240, int(240 * H0 / W0))) for k in idx]), [cv2.IMWRITE_JPEG_QUALITY, 85])
cv2.imwrite(str(QA / f"{i}_f1.png"), frames[min(len(frames) - 1, int(fps))])
res = dict(id=i, take=Path(v).name, res=f"{W0}x{H0}", fps=round(fps, 3), quadros=len(frames), dur_video=round(dur, 3), dur_audio=round(ad, 3),
           dur_audio_enviado=P["dur"], whisper=txt, diferencas=dif, palavras_whisper=W)
json.dump(res, open(QA / f"{i}_whisper.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(json.dumps({k: res[k] for k in res if k != "palavras_whisper"}, ensure_ascii=False))
