# OCR a cada 0,5 s no vídeo final; lista textos e marca palavras PT suspeitas
import subprocess, sys, numpy as np, re
from rapidocr_onnxruntime import RapidOCR
v = sys.argv[1]; ocr = RapidOCR()
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", v, "-vf", "fps=2,format=rgb24", "-f", "rawvideo", "-"], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720, 3)
PT = re.compile(r"\b(você|voce|nunca vai|ninguém|ninguem|sobrevive|porque eu|demitida|minha|loja|agora|oração|oracao|aconteceu|revoltem|grimório|grimorio|sonhos|patrão|patrao|falindo|banida|bênçãos|bencaos|são bento|sao bento|elite religiosa|missa|mensagens no|não|nao|então|tá|ensinou|silenciado|dívidas|escassez|prosperidade|julio|padresf)\b", re.I)
sus = 0
for i, f in enumerate(F):
    r, _ = ocr(f[:, :, ::-1])
    txt = " | ".join(x[1] for x in (r or []) if x[2] > 0.6)
    hit = PT.findall(txt)
    if hit: sus += 1
    print(f"{i/2:6.1f} {'**PT** ' + str(hit) if hit else ''} {txt[:160]}")
print("quadros com PT suspeito:", sus)
