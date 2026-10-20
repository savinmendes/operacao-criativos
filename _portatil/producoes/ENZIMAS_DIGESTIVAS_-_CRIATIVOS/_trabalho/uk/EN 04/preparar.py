# -*- coding: utf-8 -*-
"""Entrada do HeyGen: quadro inteiro (rosto unico e grande, sem recorte) q973-1081 com o AUDIO ORIGINAL do trecho,
cor exata (comum3). novo_A.mp3 = so a voz nova do mesmo intervalo."""
import subprocess
from pathlib import Path
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
a, b = 973, 1081; n = b - a; t0, d = a / 30, n / 30
tmp = AQ / "in" / "_v.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,str(tmp)], stdin=subprocess.PIPE)
for f in quadros(SRC, a, n): ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "orig.wav"),"-filter_complex",
    f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}[a]","-map","0:v","-map","[a]",
    "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{d:.4f}",str(AQ / "in" / "orig_A.mp4")], check=True)
tmp.unlink()
off = t0 - 32.42
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AQ / "voz_A.wav"),"-af",f"atrim={off:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}","-t",f"{d:.4f}",
    "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / "novo_A.mp3")], check=True)
print(n, "quadros", d)
