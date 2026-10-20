# folha de boca (original x antes x depois) centrada no rosto do revisor (escolha_06.json), 1 quadro por trecho
import subprocess, json, cv2, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parent.parent; P = AD.parents[2]
FIN = P / "producao" / "AD 06 - ORACION-NUDO-ES-LATAM.mp4"; ANT = AD / "_antes_cor" / "AD 06 - ORACION-NUDO-ES-LATAM.mp4"; ORI = P / "UNICOS_HD" / "06.mp4"
esc = json.loads((AD.parent / "revisao" / "loteC" / "escolha_06.json").read_text())
def q(p, t):
    b = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(p),"-frames:v","1","-f","image2pipe","-vcodec","png","-"], capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(b, np.uint8), 1)
rows = []
for nm in ["v1","w1","w3","w5","w6","w9","w12","w15","w17"]:
    t = esc[nm][2]; qq, cx, cy, L = t[len(t) // 2]; tt = qq / 30
    s = 1.5 * L; x0, y0 = int(max(0, cx - s / 2)), int(max(0, cy - 0.55 * s))
    ims = []
    for p in (ORI, ANT, FIN):
        f = q(p, tt)[y0:y0 + int(s), x0:x0 + int(s)]; ims.append(cv2.resize(f, (300, 300), interpolation=cv2.INTER_CUBIC))
    row = np.hstack(ims); cv2.putText(row, f"{nm} {tt:.2f}s", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2); rows.append(row)
hd = np.zeros((30, 900, 3), np.uint8)
for i, s in enumerate(["ORIGINAL", "ANTES", "DEPOIS"]): cv2.putText(hd, s, (i*300+90, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
cv2.imwrite(str(AD / "_cor_rev" / "folha_cor_bocas.jpg"), np.vstack([hd] + rows), [cv2.IMWRITE_JPEG_QUALITY, 88]); print("ok")
