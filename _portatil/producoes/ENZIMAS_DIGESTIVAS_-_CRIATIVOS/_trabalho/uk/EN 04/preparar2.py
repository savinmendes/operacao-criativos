# -*- coding: utf-8 -*-
"""Tentativa 2: o job com quadro inteiro (rosto enorme, boca coberta pelo frasco em metade dos quadros) voltou com a
boca intacta. Agora: so q990-1062 (boca visivel), quadro reduzido a 0,6 e centralizado com borda lisa (cor da parede; a borda refletida duplicava o rosto)
(rosto menor e inteiro no quadro), audio ORIGINAL no video e voz nova separada. Cor exata (comum3)."""
import subprocess, cv2
from pathlib import Path
from comum3 import quadros, ENC_VF, ENC_TAG
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
a, b = 990, 1062; n = b - a; t0, d = a / 30, n / 30; S = 0.6
W, H = int(720 * S), int(1280 * S); OX, OY = (720 - W) // 2, (1280 - H) // 2
tmp = AQ / "in" / "_v.mp4"
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-",
    *ENC_VF,"-threads","4","-c:v","libx264","-crf","12","-preset","medium",*ENC_TAG,str(tmp)], stdin=subprocess.PIPE)
for f in quadros(SRC, a, n):
    s = cv2.resize(f, (W, H), interpolation=cv2.INTER_AREA)
    ff.stdin.write(cv2.copyMakeBorder(s, OY, 1280 - H - OY, OX, 720 - W - OX, cv2.BORDER_CONSTANT, value=(150, 165, 180)).tobytes())
ff.stdin.close(); ff.wait()
subprocess.run(["ffmpeg","-v","error","-y","-i",str(tmp),"-i",str(AQ / "orig.wav"),"-filter_complex",
    f"[1:a]atrim={t0:.4f}:{t0+d:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}[a]","-map","0:v","-map","[a]",
    "-c:v","copy","-c:a","aac","-b:a","192k","-t",f"{d:.4f}",str(AQ / "in" / "orig_B.mp4")], check=True)
tmp.unlink()
off = t0 - 32.42
subprocess.run(["ffmpeg","-v","error","-y","-i",str(AQ / "voz_A.wav"),"-af",f"atrim={off:.4f},asetpts=PTS-STARTPTS,apad=whole_dur={d:.4f}","-t",f"{d:.4f}",
    "-ac","1","-ar","44100","-c:a","libmp3lame","-b:a","192k",str(AQ / "in" / "novo_B.mp3")], check=True)
print(n, d, W, H, OX, OY)
