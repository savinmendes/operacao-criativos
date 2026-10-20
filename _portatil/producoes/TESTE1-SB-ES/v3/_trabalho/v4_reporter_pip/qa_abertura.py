# -*- coding: utf-8 -*-
"""QA da abertura com a reportera: whisper medium es dos primeiros 20 s, folha 0-10 s a 30 fps (PiP e quadro inteiro),
verde residual na caixa do PiP, salto de pts do áudio. Uso: python qa_abertura.py <video_final.mp4> <tag>"""
import sys, json, subprocess
from pathlib import Path
import numpy as np, cv2
V = Path(sys.argv[1]); TAG = sys.argv[2]; Q = Path(__file__).resolve().parent / "qa"; Q.mkdir(exist_ok=True)
Y0 = 297 + 300                  # caixa do PiP no quadro final 720x1280
cmd = ["ffmpeg", "-v", "error", "-t", "10", "-i", str(V), "-vf", "fps=30", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
raw = subprocess.run(cmd, capture_output=True).stdout; fr = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
pip = [cv2.resize(f[Y0:Y0 + 540, 0:304], (114, 202)) for f in fr]
for k, p in enumerate(pip): cv2.putText(p, f"{k / 30:.2f}", (2, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
rows = [np.hstack(pip[i:i + 20] + [np.zeros_like(pip[0])] * (20 - len(pip[i:i + 20]))) for i in range(0, len(pip), 20)]
cv2.imwrite(str(Q / f"{TAG}_pip_0-10s_30fps.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
full = [cv2.resize(f, (180, 320)) for f in fr[::6]]
rows = [np.hstack(full[i:i + 10] + [np.zeros_like(full[0])] * (10 - len(full[i:i + 10]))) for i in range(0, len(full), 10)]
cv2.imwrite(str(Q / f"{TAG}_quadro_0-10s_5fps.jpg"), np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
verde = []
for k, f in enumerate(fr[:130]):
    x = f[Y0:Y0 + 540, 0:290].astype(np.int16); b, g, r = x[..., 0], x[..., 1], x[..., 2]
    verde.append(int(((g - np.maximum(r, b)) > 40).sum()))
ref = []
for k, f in enumerate(fr[130:200]):
    x = f[Y0:Y0 + 540, 0:290].astype(np.int16); ref.append(int(((x[..., 1] - np.maximum(x[..., 0], x[..., 2])) > 40).sum()))
p = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(V)],
                   capture_output=True, text=True).stdout.split()
t = np.array([float(x.strip(",")) for x in p if x.strip(",")]); d = np.diff(t); saltos = [(round(float(t[i]), 3), round(float(d[i]), 3)) for i in np.where(d > 0.05)[0]]
from faster_whisper import WhisperModel
subprocess.run(["ffmpeg", "-v", "error", "-y", "-t", "20", "-i", str(V), "-ac", "1", "-ar", "16000", str(Q / f"{TAG}_20s.wav")], check=True)
m = WhisperModel("medium", device="cpu", compute_type="int8")
seg, _ = m.transcribe(str(Q / f"{TAG}_20s.wav"), language="es", word_timestamps=True, beam_size=5)
W = [(w.word.strip(), round(w.start, 2), round(w.end, 2)) for s in seg for w in s.words]
res = dict(video=str(V), verde_pip_px_max_0_4s=max(verde), verde_pip_px_media_0_4s=round(float(np.mean(verde)), 1),
           verde_ref_sem_pip=max(ref), saltos_pts_audio=saltos, whisper_20s=" ".join(w[0] for w in W), palavras=W)
(Q / f"{TAG}_qa.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: v for k, v in res.items() if k != "palavras"}, ensure_ascii=False, indent=1))
print([w for w in W if w[1] < 9.5])
