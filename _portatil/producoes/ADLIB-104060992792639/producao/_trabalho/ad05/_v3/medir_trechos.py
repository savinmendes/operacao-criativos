# -*- coding: utf-8 -*-
"""Corta da base_lipsync.mp4 (v3) os trechos da revisão (mesmos limites) + original PT + voz ES do personagem, e roda o checar_lipsync."""
import subprocess, sys
from pathlib import Path
V = Path(__file__).parent; AD = V.parent; FPS = 24
K = r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas\checar_lipsync.py"
T = [("m1",87,119,"marido",None),("m3",653,893,"marido",None),("m4",893,1129,"marido",None),("m5",1129,1271,"marido",None),
     ("d1",1302,1474,"desatadora","40,280,260,300"),("d2",1474,1712,"desatadora","40,280,260,300"),
     ("c2",286,430,"clara",None),("c3",430,653,"clara",None),("d3",1712,1992,"desatadora","40,280,260,300"),
     ("d4",1992,2150,"desatadora","40,280,260,300"),("d5",2150,2298,"desatadora","40,280,260,300")]
if len(sys.argv) > 1: T = [t for t in T if t[0] in sys.argv[1].split(",")]
for n,a,b,q,ro in T:
    t0,t1 = a/FPS,b/FPS
    for src,out,aud in [(AD/"base_lipsync.mp4",V/"med"/f"fin_{n}.mp4",None),(AD/"base_sem_legenda_lama.mp4",V/"med"/f"pt_{n}.mp4",AD/"_audio/orig_novo.wav")]:
        cmd = ["ffmpeg","-v","error","-y","-i",str(src)] + (["-i",str(aud)] if aud else []) + ["-filter_complex",
               f"[0:v]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS[v]" + (f";[1:a]atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB[a]" if aud else ""),
               "-map","[v]"] + (["-map","[a]","-c:a","aac"] if aud else []) + ["-c:v","libx264","-crf","12","-threads","4",str(out)]
        subprocess.run(cmd, check=True)
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(AD/f"narr_{q}.wav"),"-af",f"atrim={t0:.4f}:{t1:.4f},asetpts=N/SR/TB",str(V/"med"/f"es_{n}.wav")],check=True)
    r = subprocess.run([sys.executable,K,str(V/"med"/f"fin_{n}.mp4"),"--audio-novo",str(V/"med"/f"es_{n}.wav"),"--original",str(V/"med"/f"pt_{n}.mp4")]+(["--rosto",ro] if ro else []),
                       capture_output=True,text=True,encoding="utf-8",errors="ignore")
    print("==",n,f"{t0:.2f}-{t1:.2f}s"); print("\n".join(l for l in r.stdout.splitlines() if l.strip()), flush=True)
