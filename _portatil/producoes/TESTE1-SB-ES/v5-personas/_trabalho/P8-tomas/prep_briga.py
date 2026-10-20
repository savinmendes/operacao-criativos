# -*- coding: utf-8 -*-
"""Seedance da briga -> takes/briga_ret.mp4 (+ .wav): ação 0-A s em câmera lenta (minterpolate) até a reportera terminar a
frase do PiP (o chofer grita '¡Bájate!' já em 2,78 s no take), depois velocidade normal até FIM. Gera também o mapa de tempo."""
import json, subprocess, sys
AQ = __import__("pathlib").Path(__file__).resolve().parent; T = AQ / "takes"; SRC = T / "seedance_briga.mp4"
A = 2.70; OUT_A = 4.45; FIM = 8.90; r = A / OUT_A
def run(c):
    p = subprocess.run([str(x) for x in c], capture_output=True, text=True)
    if p.returncode: print(p.stderr[-2000:]); sys.exit(1)
fa = (f"[0:v]trim=0:{A},setpts=(PTS-STARTPTS)/{r:.5f},minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop=12,trim=end_frame={round(OUT_A*30)},setpts=PTS-STARTPTS[a];"
      f"[0:v]trim={A}:{FIM},setpts=PTS-STARTPTS,fps=30[b];[a][b]concat=n=2:v=1:a=0[v];"
      f"[0:a]atrim=0:{A},asetpts=PTS-STARTPTS,atempo={r:.5f},apad,atrim=0:{OUT_A}[x];[0:a]atrim={A}:{FIM},asetpts=PTS-STARTPTS[y];[x][y]concat=n=2:v=0:a=1[au]")
run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", fa, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-crf", "10", "-preset", "fast",
     "-c:a", "pcm_s16le", "-ar", "48000", T / "briga_ret.mov"])
json.dump(dict(A=A, OUT_A=OUT_A, FIM=FIM, r=r, desloc=OUT_A - A), open(T / "briga_ret.json", "w"), indent=1)
print("ok", OUT_A + FIM - A)
