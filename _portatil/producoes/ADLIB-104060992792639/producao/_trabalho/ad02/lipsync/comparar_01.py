# -*- coding: utf-8 -*-
"""Compara a base_lipsync.mp4 do 02 (quadro q+44) com a base_lipsync.mp4 atual do AD 01 (quadro q), q >= 242,
na regiao do rosto (y 250-700, x 250-600). Imprime a diferenca media por trecho do AD 01 e os quadros-limite que diferem."""
import json, cv2, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parent.parent; A1 = AD.parent / "ad01"; OFF = 44
seg = json.loads((A1 / "segmentos.json").read_text())["segmentos"]
c1 = cv2.VideoCapture(str(A1 / "base_lipsync.mp4")); c2 = cv2.VideoCapture(str(AD / "base_lipsync.mp4"))
c1.set(cv2.CAP_PROP_POS_FRAMES, 242); c2.set(cv2.CAP_PROP_POS_FRAMES, 242 + OFF)
d = {}
q = 242
while q <= 3472:
    ok1, f1 = c1.read(); ok2, f2 = c2.read()
    if not (ok1 and ok2): break
    d[q] = float(np.abs(f1[250:700, 250:600].astype(np.int16) - f2[250:700, 250:600]).mean()); q += 1
for s in seg:
    xs = [d[k] for k in range(max(242, s["quadro_ini"]), s["quadro_fim"] + 1) if k in d]
    if not xs: continue
    alto = [k for k in range(max(242, s["quadro_ini"]), s["quadro_fim"] + 1) if d.get(k, 0) > 1.5]
    print(f"{s['nome']} q{s['quadro_ini']}-{s['quadro_fim']}: media {np.mean(xs):.2f} max {np.max(xs):.2f} | >1.5: {len(alto)} q"
          + (f" ({alto[0]}..{alto[-1]})" if alto else ""))
