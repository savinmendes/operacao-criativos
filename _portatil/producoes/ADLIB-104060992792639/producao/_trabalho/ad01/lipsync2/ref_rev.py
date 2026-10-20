# -*- coding: utf-8 -*-
"""Audio de referencia com a MESMA atividade de fala do ES: cada trecho de fala do ES invertido no lugar.
O HeyGen usa a fala original do video para saber QUANDO o personagem fala (fora disso devolve a boca de entrada);
com o PT, ele sincroniza so onde o PT falava. Uso: python ref_rev.py nome qini qfim -> in/crop_<nome>_rev.mp4"""
import sys, subprocess, numpy as np, soundfile as sf
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
nome, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
x, sr = sf.read(str(AD / "narracao_es.wav"), always_2d=True); x = x.mean(1)
seg = x[int(a / 30 * sr):int((b + 1) / 30 * sr)].copy()
h = int(sr * 0.02); e = np.array([np.sqrt(np.mean(seg[i:i + h] ** 2)) for i in range(0, len(seg), h)])
db = 20 * np.log10(e + 1e-6); fala = db > db.max() - 35
y = seg.copy(); k = 0
while k < len(fala):
    if fala[k]:
        j = k
        while j < len(fala) and fala[j]: j += 1
        s0, s1 = k * h, min(len(seg), j * h); y[s0:s1] = seg[s0:s1][::-1]; k = j
    else: k += 1
w = AQ / "in" / f"_rev_{nome}.wav"; sf.write(str(w), y, sr)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AQ/"in"/f"crop_{nome}_none.mp4"),"-i",str(w),"-map","0:v","-map","1:a",
    "-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(AQ/"in"/f"crop_{nome}_rev.mp4")], check=True)
print(AQ/"in"/f"crop_{nome}_rev.mp4", (AQ/"in"/f"crop_{nome}_rev.mp4").stat().st_size)
