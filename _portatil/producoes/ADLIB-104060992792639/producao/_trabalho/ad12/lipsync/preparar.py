# -*- coding: utf-8 -*-
"""Uso: python preparar.py AD_DIR video_pt.mp4 nome [nome...]
Para cada trecho de AD_DIR/segmentos.json: recorte que acompanha o rosto da Desatadora (base_sem_legenda.mp4),
720x1280 24 fps + audio PT original do trecho -> lipsync/in/crop_<nome>.mp4 ; ES do trecho -> in/es_<nome>.mp3 ;
caixas e landmarks em in/geo_<nome>.npz"""
import sys, json, subprocess, numpy as np
from pathlib import Path
import rosto as R
AD = Path(sys.argv[1]); VPT = sys.argv[2]; nomes = sys.argv[3:]
I = AD / "lipsync" / "in"; I.mkdir(parents=True, exist_ok=True)
seg = {s["nome"]: s for s in json.loads((AD / "segmentos.json").read_text())["segmentos"]}
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
for nome in nomes:
    s = seg[nome]; a, b = s["quadro_ini"], s["quadro_fim"]; n = b - a + 1; t0, t1 = a / 24, (b + 1) / 24
    fr = R.ler(AD / "base_sem_legenda.mp4", a, n); B, P = R.caixas(fr)
    np.savez(I / f"geo_{nome}.npz", B=np.array(B), P=np.array([p if p is not None else np.full((478, 2), np.nan) for p in P]))
    tmp = I / f"_v_{nome}.mp4"
    ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-",
        "-c:v","libx264","-crf","14","-preset","medium","-threads","4","-pix_fmt","yuv420p",*COR,str(tmp)], stdin=subprocess.PIPE)
    for f, bx in zip(fr, B): ff.stdin.write(R.recortar(f, bx).tobytes())
    ff.stdin.close(); ff.wait()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",VPT,"-filter_complex",f"[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k","-shortest",str(I / f"crop_{nome}.mp4")], check=True)
    tmp.unlink()
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "narracao_es.wav"),"-af",f"atrim={t0}:{t1},asetpts=PTS-STARTPTS",
        "-ac","1","-c:a","libmp3lame","-b:a","192k",str(I / f"es_{nome}.mp3")], check=True)
    # trecho original (base, quadro inteiro) com PT, para o checar_lipsync
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / "base_sem_legenda.mp4"),"-i",VPT,"-filter_complex",
        f"[0:v]trim=start_frame={a}:end_frame={b+1},setpts=PTS-STARTPTS[v];[1:a]atrim={t0}:{t1},asetpts=PTS-STARTPTS[a]",
        "-map","[v]","-map","[a]","-c:v","libx264","-crf","14","-threads","4","-c:a","aac",*COR,str(I / f"pt_{nome}.mp4")], check=True)
    bb = np.array(B); print(nome, n, "quadros", f"caixa w {bb[:,2].min():.0f}-{bb[:,2].max():.0f}", "sem rosto:", sum(p is None for p in P), flush=True)
