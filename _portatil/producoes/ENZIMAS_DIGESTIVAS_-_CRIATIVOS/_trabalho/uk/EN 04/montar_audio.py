# -*- coding: utf-8 -*-
"""Saida final do EN 04 UK: video ORIGINAL copiado sem recodificar (cor e quadros identicos) + audio_uk.wav
(fora do trecho 32,42-36,03 s = original intocado; dentro = fundo demucs + voz clonada). Os 3 jobs de lipsync
voltaram com a boca intacta; a boca so aparece ~1 s (q1019-1048) e la a fala nova coincide com a antiga
("they're still ... and I'm pretty"), so "in stock" x "available" difere (~0,4 s)."""
import subprocess
from pathlib import Path
AQ = Path(__file__).parent
SRC = AQ.parent.parent.parent / "INGLES" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE.mp4"
DST = AQ.parent.parent.parent / "UK" / "EN 04 - ENZIMAS-BARRIGA-POS-RESTAURANTE - UK.mp4"
subprocess.run(["ffmpeg","-v","error","-y","-i",str(SRC),"-i",str(AQ / "audio_uk.wav"),"-map","0:v","-map","1:a","-c:v","copy",
    "-c:a","aac","-b:a","128k","-ar","44100","-movflags","+faststart",str(DST)], check=True)
print("ok", DST, DST.stat().st_size)
