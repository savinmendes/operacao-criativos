# -*- coding: utf-8 -*-
"""Tentativa 3: a legenda queimada branca passa em cima da boca (y~600-660) e os jobs 1 e 2 voltaram com a boca intacta.
Uso: python sem_legenda.py q_ini q_fim NOME  (padrao 990 1062 C). Tentativa 4 (D): 1006-1081, comecando num quadro com a boca visivel.
Apaga a legenda (mascara fixa: pixels claros em >=90% dos quadros, dilatada) com LaMa nos quadros q990-1061,
quadro inteiro 720x1280, cor exata (comum3). Saida in/orig_C.mp4 (audio ORIGINAL) + in/novo_C.mp3. Rodar com o python do _vg."""
import sys, subprocess, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, ".")
import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama
from pathlib import Path
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(".").resolve()
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
a, b = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (990, 1062); NM = sys.argv[3] if len(sys.argv) > 3 else "C"; n = b - a; t0, d = a / 30, n / 30
fr = list(quadros(SRC, a, n))
st = np.stack([f.min(2) for f in fr[::2]]); leg = ((st > 215).mean(0) > 0.9).astype(np.uint8); leg[:500] = 0; leg[760:] = 0
leg = cv2.dilate(leg, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
np.save("mascara_legenda.npy", leg); print("mascara px", int(leg.sum()), flush=True)
lama = SimpleLama()
y0, y1 = 520, 740  # so a faixa da legenda vai para o LaMa (com contexto)
tmp = AQ / "in" / "_v.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,str(tmp)], stdin=subprocess.PIPE)
for k, f in enumerate(fr):
    roi = f[y0 - 100:y1 + 100]; m = leg[y0 - 100:y1 + 100] * 255
    r = np.array(lama(Image.fromarray(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)), Image.fromarray(m)))[:roi.shape[0], :roi.shape[1]]
    r = cv2.cvtColor(r, cv2.COLOR_RGB2BGR); o = f.copy(); mm = (m > 0)[..., None]
    o[y0 - 100:y1 + 100] = np.where(mm, r, roi)
    ff.stdin.write(o.tobytes())
    if k % 10 == 0: print(k, "/", n, flush=True)
ff.stdin.close(); ff.wait()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "orig.wav"),"-filter_complex",
    f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}[a]","-map","0:v","-map","[a]",
    "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{d:.4f}",str(AQ / "in" / f"orig_{NM}.mp4")], check=True)
tmp.unlink()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AQ / "voz_A.wav"),"-af",f"atrim={t0-32.42:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}","-t",f"{d:.4f}",
    "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / f"novo_{NM}.mp3")], check=True)
print("ok")
