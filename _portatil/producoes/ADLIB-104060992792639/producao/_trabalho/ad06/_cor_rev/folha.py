# folha visual: original x antes x depois (finais de 30 fps; original de 24 fps no mesmo tempo). Sem abrir video.
import subprocess, cv2, numpy as np
from pathlib import Path
AD = Path(__file__).resolve().parent.parent; P = AD.parents[2]
FIN = P / "producao" / "AD 06 - ORACION-NUDO-ES-LATAM.mp4"; ANT = AD / "_antes_cor" / "AD 06 - ORACION-NUDO-ES-LATAM.mp4"; ORI = P / "UNICOS_HD" / "06.mp4"
def q(p, t):
    b = subprocess.run(["ffmpeg","-v","error","-ss",f"{t:.3f}","-i",str(p),"-frames:v","1","-f","image2pipe","-vcodec","png","-"], capture_output=True).stdout
    return cv2.imdecode(np.frombuffer(b, np.uint8), 1)
# (tempo, recorte x,y,w,h, rotulo)
L = [(4.0,(300,450,320,320),"v1 varal"),(13.0,(330,250,220,220),"w1"),(22.0,(330,250,220,220),"w2"),(33.0,(330,250,220,220),"w3"),
     (38.8,(0,0,720,1280),"w4 close corda"),(43.0,(330,250,220,220),"w5"),(52.5,(150,150,450,450),"w6 zoom"),(66.0,(330,250,220,220),"w8"),
     (81.0,(0,0,720,1280),"w11 close corda"),(90.0,(0,560,720,720),"setas"),(98.0,(330,250,220,220),"w15"),(8.6,(0,700,720,580),"clarao")]
rows = []
for t, (x, y, w, h), r in L:
    ims = []
    for p in (ORI, ANT, FIN):
        f = q(p, t)[y:y+h, x:x+w]; s = 300 / max(w, h); f = cv2.resize(f, (int(w*s), int(h*s)), interpolation=cv2.INTER_AREA)
        c = np.zeros((300, 300, 3), np.uint8); c[:f.shape[0], :f.shape[1]] = f; ims.append(c)
    row = np.hstack(ims); cv2.putText(row, f"{r} {t}s", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2); rows.append(row)
hd = np.zeros((30, 900, 3), np.uint8)
for i, s in enumerate(["ORIGINAL", "ANTES", "DEPOIS"]): cv2.putText(hd, s, (i*300+90, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
A = np.vstack([hd] + rows[:6]); B = np.vstack([hd] + rows[6:])
cv2.imwrite(str(AD / "_cor_rev" / "folha_cor_1.jpg"), A, [cv2.IMWRITE_JPEG_QUALITY, 88]); cv2.imwrite(str(AD / "_cor_rev" / "folha_cor_2.jpg"), B, [cv2.IMWRITE_JPEG_QUALITY, 88]); print("ok")
