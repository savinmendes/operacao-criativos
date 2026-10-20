# -*- coding: utf-8 -*-
"""Uso: python recolocar.py AD_DIR [saida]  -> AD_DIR/base_lipsync.mp4 (24 fps)
Cada trecho: lipsync/out/ls_<nome>.mp4 (recorte) reamostrado no tempo p/ o n exato de quadros (sem congelar),
colado na base so na boca/queixo (elipse suave pelos landmarks da base). Emenda sem corte de camera: crossfade 2 quadros.
Opcional lipsync/plano.json: {"nome": "arquivo.mp4@k"} (k = descarta k primeiros quadros)."""
import sys, json, subprocess, numpy as np, cv2
from pathlib import Path
import rosto as R
AD = Path(sys.argv[1]); OUT = sys.argv[2] if len(sys.argv) > 2 else str(AD / "base_lipsync.mp4")
L = Path(__file__).resolve().parent
seg = json.loads((AD / "segmentos.json").read_text())["segmentos"]; N = json.loads((AD / "segmentos.json").read_text())["n"]
pl = AD / "lipsync" / "plano.json"; plano = json.loads(pl.read_text()) if pl.exists() else {}
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
    "-c:v","libx264","-crf","12","-preset","medium","-threads","4","-pix_fmt","yuv420p",*COR,"-an",OUT], stdin=subprocess.PIPE)
base = cv2.VideoCapture(str(AD / "base_sem_legenda.mp4")); i = 0; prev = None; log = []
def trecho(s, bases):
    nome = s["nome"]; n = len(bases); spec = plano.get(nome, f"ls_{nome}.mp4"); k = 0
    if "@" in spec: spec, k = spec.split("@"); k = int(k)
    p = AD / "lipsync" / "out" / spec
    if not p.exists(): log.append(f"{nome}: SEM SAIDA, base"); return bases
    g = R.ler(p)[k:]; m = len(g); g = R.reamostrar(g, n)
    geo = np.load(AD / "lipsync" / "in" / f"geo_{nome}.npz"); B, P = geo["B"], geo["P"]
    out = [R.colar(b, gg, B[j], None if np.isnan(P[j]).any() else P[j]) for j, (b, gg) in enumerate(zip(bases, g))]
    log.append(f"{nome}: {m}->{n} quadros"); return out
for s in seg:
    a, b = s["quadro_ini"], s["quadro_fim"]
    if prev is not None and i < a:
        for f in prev[0]: ff.stdin.write(f.tobytes())
        prev = None
    while i < a:
        ok, f = base.read(); ff.stdin.write(f.tobytes()); i += 1
    bases = []
    for _ in range(a, b + 1):
        ok, f = base.read(); bases.append(f); i += 1
    fr = trecho(s, bases)
    if prev is not None:
        corte = np.abs(prev[1].astype(np.float32) - bases[0]).mean() > 10
        if not corte:
            Lf, Rf = prev[0][-1].astype(np.float32), fr[0].astype(np.float32)
            prev[0][-1] = np.clip(Lf * 2 / 3 + Rf / 3, 0, 255).astype(np.uint8); fr[0] = np.clip(Lf / 3 + Rf * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"  emenda q{a}: {'corte' if corte else 'crossfade 2q'}")
        for f in prev[0]: ff.stdin.write(f.tobytes())
    prev = (fr, bases[-1])
if prev is not None:
    for f in prev[0]: ff.stdin.write(f.tobytes())
while i < N:
    ok, f = base.read()
    if not ok: break
    ff.stdin.write(f.tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("\n".join(log)); print("quadros", i)
