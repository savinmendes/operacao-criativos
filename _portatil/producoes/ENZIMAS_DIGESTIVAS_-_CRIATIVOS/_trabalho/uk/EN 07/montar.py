# -*- coding: utf-8 -*-
"""Monta a versao UK: original quadro a quadro (cor exata, comum3) + boca/queixo do HeyGen nos trechos
(caixas_<seg>.npy, correcao de desvio de cor medida fora da boca) + capturas de tela sem interface do TikTok
(ov_patches.npz, de ov_limpar.py) + trilha audio_uk.wav. Crossfade de 2 quadros nas emendas sem corte de camera.
Uso: python montar.py   (config em cfg_montar.json: src, dst, segs [[nome,a,b],...])"""
import subprocess, json, numpy as np
from pathlib import Path
from comum3 import quadros, ler, reamostrar, colar, ENC_VF, ENC_TAG
AQ = Path(__file__).parent
CFG = json.load(open(AQ / "cfg_montar.json", encoding="utf-8"))
SRC = AQ.parent.parent.parent / "INGLES" / CFG["src"]
DST = AQ.parent.parent.parent / "UK" / CFG["dst"]
SEGS = CFG["segs"]
def desvio(nm, g):
    e = list(quadros(AQ / "in" / f"orig_{nm}.mp4")); d = []
    for k in range(0, len(g), 10):
        a, b = e[k].astype(np.float32), g[k].astype(np.float32)
        d.append(np.concatenate([(a - b)[60:300].reshape(-1, 3), (a - b)[1000:1240].reshape(-1, 3)]).mean(0))
    return np.median(d, 0)
novo = {}
for nm, a, b in SEGS:
    g = ler(AQ / "out" / f"ls_{nm}.mp4"); n = b - a; m = len(g); g = reamostrar(g, n)
    dv = desvio(nm, g); g = [np.clip(f.astype(np.float32) + dv, 0, 255).astype(np.uint8) for f in g]
    C = np.load(AQ / f"caixas_{nm}.npy")
    print(nm, m, "->", n, "quadros; desvio de cor BGR", dv.round(2), flush=True)
    for j in range(n): novo[a + j] = (g[j], C[j], nm)
OVS = []
for nmz in ("ov_patches.npz", "ov_patches2.npz"):
    if (AQ / nmz).exists():
        OV = np.load(AQ / nmz); OVS.append((OV["caixa"], dict(zip(OV["qs"].tolist(), OV["ps"]))))
tmp = AQ / "video_uk_sem_audio.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","18","-preset","slow","-pix_fmt","yuv420p",*ENC_TAG,"-an",str(tmp)], stdin=subprocess.PIPE)
prev_out = prev_base = prev_dono = None; log = []
for i, fb in enumerate(quadros(SRC)):
    if i in novo:
        g, c, dono = novo[i]; out = colar(fb, g, c)
    else:
        out = fb; dono = None
    for (OX0, OY0, OX1, OY1), OVP in OVS:
        if i in OVP:   # so os pixels que a limpeza mudou (as caixas de patches diferentes se sobrepoem)
            p = OVP[i]; mud = np.any(p != fb[OY0:OY1, OX0:OX1], axis=2)[..., None]
            out = out.copy(); out[OY0:OY1, OX0:OX1] = np.where(mud, p, out[OY0:OY1, OX0:OX1])
    if prev_out is not None and dono != prev_dono:
        corte = np.abs(fb.astype(np.float32) - prev_base).mean() > 10
        if not corte:
            L, R = prev_out.astype(np.float32), out.astype(np.float32)
            prev_out = np.clip(L * 2 / 3 + R / 3, 0, 255).astype(np.uint8); out = np.clip(L / 3 + R * 2 / 3, 0, 255).astype(np.uint8)
        log.append(f"emenda q{i} ({i/30:.2f}s): {'corte' if corte else 'crossfade 2q'}")
    if prev_out is not None: ff.stdin.write(prev_out.tobytes())
    prev_out, prev_base, prev_dono = out, fb.astype(np.float32), dono
ff.stdin.write(prev_out.tobytes()); ff.stdin.close(); ff.wait()
print("\n".join(log), "| quadros", i + 1)
DST.parent.mkdir(exist_ok=True)
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "audio_uk.wav"),"-map","0:v","-map","1:a","-c:v","copy",
    "-c:a","aac","-b:a","128k","-ar","44100","-movflags","+faststart","-shortest",str(DST)], check=True)
print("ok", DST, DST.stat().st_size)
