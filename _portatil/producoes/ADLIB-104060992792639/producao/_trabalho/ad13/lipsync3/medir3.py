# -*- coding: utf-8 -*-
"""Uso: python medir3.py seg [arquivo_saida.mp4[@k]]
Cola a saida (recorte) na base so na boca/queixo (mesma conta do recolocar.py), grava out/full_<seg>.mp4 com o ES,
gera in/orig_<seg>.mp4 (base inteira + PT) e roda checar_lipsync --rosto (rosto da mulher, rosto_<seg>.txt)."""
import sys, json, subprocess, os, cv2, numpy as np
from pathlib import Path
AQ = Path(__file__).parent; AD = AQ.parent
CFG = json.loads((AQ / "segs.json").read_text()); FPS = CFG["fps"]
nm = sys.argv[1]; spec = sys.argv[2] if len(sys.argv) > 2 else str(AQ / "out" / f"ls_{nm}.mp4")
s = [x for x in CFG["segs"] if x["nome"] == nm][0]; a, b = s["a"], s["b"]; n = b - a
from comum3 import ler, reamostrar, colar, quadros, desvio_cor, corrigir
p, _, k = spec.partition("@"); g = ler(p, int(k or 0)); m0 = len(g); g = reamostrar(g, n)
C = np.load(AQ / f"caixas_{nm}.npy"); g = corrigir(g, desvio_cor(nm, a, AQ, AD))
bq = quadros(AD / "base_sem_legenda.mp4", a, n)
full = AQ / "out" / f"full_{nm}.mp4"; es = AQ / "in" / f"es_{nm}.mp3"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r",str(FPS),"-i","-","-i",str(es),
    "-map","0:v","-map","1:a","-c:v","libx264","-crf","14","-threads","4","-pix_fmt","yuv420p","-c:a","aac","-shortest",str(full)], stdin=subprocess.PIPE)
for j in range(n):
    f = next(bq); ff.stdin.write(colar(f, g[j], C[j]).tobytes())
ff.stdin.close(); ff.wait()
orig = AQ / "in" / f"orig_{nm}.mp4"
if not orig.exists():
    t0, t1 = a / FPS, b / FPS
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "base_sem_legenda.mp4"),"-i",CFG["src"],"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v];[1:a]atrim={t0:.4f}:{t1:.4f},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-threads","4","-c:a","aac",str(orig)], check=True)
ro = (AQ / f"rosto_{nm}.txt").read_text().strip()
r = subprocess.run([sys.executable, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py", str(full),
    "--audio-novo", str(es), "--original", str(orig), "--rosto", ro], capture_output=True, text=True, encoding="utf-8", errors="ignore",
    env=dict(os.environ, PYTHONIOENCODING="utf-8"))
print(f"== {nm}: saida {m0} q -> {n}; rosto {ro}")
print("\n".join(l for l in r.stdout.splitlines() if l.strip() and not l.startswith(("W0000", "I0000"))))
