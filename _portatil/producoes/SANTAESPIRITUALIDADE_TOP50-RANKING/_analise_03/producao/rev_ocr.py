# OCR a cada 0,5 s no vídeo final; lista textos e marca palavras PT suspeitas
import subprocess, sys, numpy as np, re
from rapidocr_onnxruntime import RapidOCR
v = sys.argv[1]; ocr = RapidOCR()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "fps=2,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
PT = re.compile(r"\b(você|voce|demitida|mulher|surpreendida|inacreditável|inacreditavel|acontece|aconteceu|oração|oracao|grimório|grimorio|são bento|sao bento|proposta|emprego|ligação|ligacao|após|apos|seguida|gente|olha|absurdo|comigo|paulo|paulorb|bisbo|silenciar|relatos|congresso|bênçãos|bencaos|prosperidade|dívidas|dividas|pobreza|não|nao|então|jn|vezes|ganho|perfil|disponível|disponivel)\b", re.I)
sus = 0
for i, f in enumerate(F):
    r, _ = ocr(f[:, :, ::-1])
    txt = " | ".join(x[1] for x in (r or []) if x[2] > 0.6)
    hit = PT.findall(txt)
    if hit: sus += 1
    print(f"{i/2:6.1f} {'**PT** ' + str(hit) if hit else ''} {txt[:160]}")
print("quadros com PT suspeito:", sus)
