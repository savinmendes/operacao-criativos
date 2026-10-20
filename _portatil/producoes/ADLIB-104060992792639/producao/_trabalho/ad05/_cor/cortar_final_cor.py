# -*- coding: utf-8 -*-
"""Corta o AD 05 FINAL (lote A) nos 11 trechos de lipsync da revisao (c1 incluido, so no rosto da Clara) + original PT
(base_sem_legenda_lama + orig_novo.wav) + voz ES do personagem, para o revisar_ad --lipsync. Gera med/lipsync_arg.txt.
Uso: python cortar_final.py [video_final] [pasta_saida]"""
import subprocess, sys
from pathlib import Path
L = Path(__file__).resolve().parent; AD = L.parent; FPS = 24
FIN = Path(sys.argv[1]) if len(sys.argv) > 1 else AD.parent.parent / "AD 05 - ORACION-FAMILIA-ES-LATAM.mp4"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else L / "med"; OUT.mkdir(exist_ok=True)
D = "40;280;260;300"
T = [("c1",0,75,"clara","380;0;300;320"),("c2",286,430,"clara",None),("c3",430,653,"clara",None),
     ("m3",653,893,"marido",None),("m4",893,1129,"marido",None),("m5",1129,1271,"marido",None),
     ("d1",1302,1474,"desatadora",D),("d2",1474,1712,"desatadora",D),("d3",1712,1992,"desatadora",D),
     ("d4",1992,2150,"desatadora",D),("d5",2150,2292,"desatadora",D)]
parts = []
for n, a, b, q, ro in T:
    t0, t1 = a / FPS, b / FPS
    for src, out, aud in [(FIN, OUT / f"fin_{n}.mp4", None), (AD / "_antes_cor" / "base_sem_legenda_lama.mp4", OUT / f"pt_{n}.mp4", AD / "_audio/orig_novo.wav")]:
        cmd = ["ffmpeg","-v","error","-y","-i",str(src)] + (["-i",str(aud)] if aud else []) + ["-filter_complex",
               f"[0:v]fps={FPS},trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v]" + (f";[1:a]atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB[a]" if aud else ""),
               "-map","[v]"] + (["-map","[a]","-c:a","aac"] if aud else ["-an"]) + ["-c:v","libx264","-crf","12","-threads","4",str(out)]
        subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD / f"narr_{q}.wav"),"-af",f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB",str(OUT / f"es_{n}.wav")], check=True)
    parts.append(f"fin_{n}.mp4:es_{n}.wav:pt_{n}.mp4" + (f":{ro}" if ro else ""))
(OUT / "lipsync_arg.txt").write_text(",".join(parts), encoding="utf-8"); print(len(parts), "trechos em", OUT)
