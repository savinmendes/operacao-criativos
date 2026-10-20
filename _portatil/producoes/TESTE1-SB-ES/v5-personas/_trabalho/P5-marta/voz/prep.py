# -*- coding: utf-8 -*-
"""mp3 ElevenLabs -> wav 48k com pausas internas <= CAP (0,22 s; 0,25 em reticências) e palavras json ajustadas. atempo opcional."""
import json, subprocess, sys
import numpy as np
from pathlib import Path
from pal import palavras
AQ = Path(__file__).resolve().parent; SR = 48000
ATEMPO = {"R00": 1.14}
def proc(i):
    x = np.frombuffer(subprocess.run(["ffmpeg","-v","error","-i",str(AQ/f"{i}.mp3"),"-ac","1","-ar",str(SR),"-f","f32le","-"],capture_output=True).stdout,np.float32).copy()
    W = palavras(AQ/f"{i}.alinhamento.json")
    segs = []; shift = 0.0; out = []; cur = 0
    NW = []
    for k,(w,s,e) in enumerate(W):
        NW.append([w, s-shift, e-shift])
        if k+1 < len(W):
            g = W[k+1][1]-e; cap = 0.25 if w.endswith(("...","…")) else 0.22
            if g > cap:
                a = e + 0.04; b = a + (g-cap)    # remove o meio da pausa
                ia, ib = int(a*SR), int(b*SR); xf = int(0.01*SR)
                out.append(x[cur:ia-xf]); w_ = np.linspace(0,1,xf); out.append(x[ia-xf:ia]*(1-w_)+x[ib-xf:ib]*w_); cur = ib
                shift += b-a
    fim = W[-1][2] + 0.12
    out.append(x[cur:int((fim+shift)*SR)]) if False else out.append(x[cur:int(min(len(x)/SR, W[-1][2]+0.12+0)*SR)])
    y = np.concatenate(out); f = int(0.03*SR); y[-f:] *= np.linspace(1,0,f)
    raw = AQ/f"{i}.f32"; raw.write_bytes(y.astype(np.float32).tobytes())
    at = ATEMPO.get(i, 1.0)
    subprocess.run(["ffmpeg","-v","error","-y","-f","f32le","-ar",str(SR),"-ac","1","-i",str(raw),*(["-af",f"atempo={at}"] if at!=1 else []),"-ac","2","-ar",str(SR),"-c:a","pcm_s16le",str(AQ/f"{i}.wav")],check=True); raw.unlink()
    P = [dict(w=w, ini=round(s/at,3), fim=round(e/at,3)) for w,s,e in NW]
    (AQ/f"{i}.json").write_text(json.dumps(dict(palavras=P, dur=len(y)/SR/at), ensure_ascii=False, indent=0), encoding="utf-8")
    print(i, round(len(y)/SR/at,2), P[-1])
for i in (sys.argv[1:] or ["R00","R01","CTA","M1","M2","M3","M4","M5"]): proc(i)
