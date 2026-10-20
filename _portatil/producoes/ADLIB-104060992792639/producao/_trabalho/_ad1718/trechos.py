# -*- coding: utf-8 -*-
"""Trechos para o revisar_ad --lipsync (igual ao ad17/lipsync/trechos.py, generico p/ 17 e 18, caminhos absolutos):
<saida>/full_<s> (base + ES), orig_<s> (original + PT), es_<s>.wav, rosto = mediana das caixas. Grava <saida>/lipsync_arg.txt.
Uso: python trechos.py NN base.mp4 pasta_saida"""
import sys, json, subprocess, numpy as np
from pathlib import Path
NN, BASE, OUT = sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
T = Path(__file__).resolve().parent.parent; AD = T / f"ad{NN}"; AQ = AD / "lipsync"; CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
ORIG = T.parent.parent / "UNICOS_HD" / f"{NN}.mp4"; itens = []
for s in CFG["segs"]:
    n, a, b = s["nome"], s["a"], s["b"]; t0, d = a / FPS, (b - a) / FPS
    C = np.load(AQ / s.get("cx", f"caixas_{n}.npy")); mx, my, fw, fh = np.median(C[:, 4:8], 0)
    ro = [int(mx - 0.65 * fw), int(my - 0.8 * fh), int(1.3 * fw), int(1.25 * fh)]
    full, orig, es = OUT / f"full_{n}.mp4", OUT / f"orig_{n}.mp4", OUT / f"es_{n}.wav"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t0}","-t",f"{d}","-i",str(AD/"narracao_es.wav"),"-ac","1","-ar","48000",str(es)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(BASE),"-i",str(es),"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v]","-map","[v]","-map","1:a","-c:v","libx264","-crf","14","-c:a","aac",str(full)],check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(ORIG),"-i",str(AD/"_audio"/"orig.wav"),"-filter_complex",
        f"[0:v]fps={FPS},trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v];[1:a]atrim={t0}:{t0+d},asetpts=PTS-STARTPTS[a]","-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-c:a","aac",str(orig)],check=True)
    itens.append(f"{full}:{es}:{orig}:{';'.join(map(str, ro))}")
(OUT / "lipsync_arg.txt").write_text(",".join(itens), encoding="utf-8"); print(len(itens), "trechos")
