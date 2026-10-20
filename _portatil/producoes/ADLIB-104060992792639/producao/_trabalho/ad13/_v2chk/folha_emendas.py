# folha 1 em 1 quadro em volta de cada emenda do AD final (4 antes, 4 depois); dif. de quadro anotada
import cv2, numpy as np
FIN = r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\AD 13 - ORACION-PAZ-ES-LATAM.mp4"
CORTES = [198,211,455,692,873,1003,1307,1414,1590,1794,1909,2013,2285,2517,2667,2949,3192,3480]
c = cv2.VideoCapture(FIN); F = []
while True:
    ok, f = c.read()
    if not ok: break
    F.append(cv2.resize(f, (108, 192)))
linhas = []
for b in CORTES:
    tiles = []
    for i in range(b-4, b+5):
        if not (0 <= i < len(F)): tiles.append(np.zeros((212,108,3),np.uint8)); continue
        t = F[i].copy()
        d = np.abs(F[i].astype(float)-F[i-1].astype(float)).mean() if i > 0 else 0
        if i == b: cv2.rectangle(t,(0,0),(107,191),(0,255,255),2)
        lab = np.full((20,108,3),255,np.uint8)
        cv2.putText(lab, f"{i/30:.2f} d{d:.0f}", (2,14), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0,0,0), 1)
        tiles.append(np.vstack([t, lab]))
    linhas.append(np.hstack(tiles))
for k in range(0, len(linhas), 9):
    cv2.imwrite(f"emendas_{k//9+1}.jpg", np.vstack(linhas[k:k+9]), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(len(F))
