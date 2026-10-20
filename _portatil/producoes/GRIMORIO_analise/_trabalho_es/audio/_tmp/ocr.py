import sys, re, numpy as np
sys.path.insert(0, "."); import cor
from rapidocr_onnxruntime import RapidOCR
o = RapidOCR()
F = r"C:\Users\PICHAU\Downloads\GRIMORIO V2 - ES COLAR (VIDEO FICTICIO).mp4"
import subprocess
r = subprocess.run(["ffmpeg","-v","error","-i",F,"-vf","fps=2,"+cor.vf_ler(True),"-f","rawvideo","-"],capture_output=True).stdout
A = np.frombuffer(r,np.uint8).reshape(-1,1280,720,3)
PT = re.compile(r"(ção|ções|ões|não|você|paulo|perfil|palavra|oração|bênç|são |brasil|prosperidadesv|sagradoverso|relato|acesse|seguidores|mensagem|obrigad|abraço|senhor|muito|deus)", re.I)
todos = []
for i, f in enumerate(A):
    res, _ = o(f[:, :, ::-1])
    for b, t, c in (res or []):
        if c > 0.6: todos.append((i/2, t))
        if c > 0.6 and PT.search(t): print(f"{i/2:6.1f}s  PT? {t!r} ({c:.2f})")
open("rev2/ocr_todos.txt","w",encoding="utf-8").write("\n".join(f"{t:.1f}\t{x}" for t,x in todos))
print("ok", len(A), "quadros")
