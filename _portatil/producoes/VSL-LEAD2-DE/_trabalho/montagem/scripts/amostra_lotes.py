import sys, cv2, numpy as np, json
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\VSL-LEAD2-DE\_trabalho\montagem\scripts")
from vslcomum import *
L = {t["id"]: t for t in json.load(open(T/"voz"/"lotes.json", encoding="utf-8"))["trechos"]}
ids = sys.argv[1:]
rows = []
for i in ids:
    t = L[i]; lote = t["lote"]
    p = T/"lipsync"/f"LOTE_{lote}"/f"{i}.mp4"
    k = 60
    fl = ler(p, None, k+1)[k]
    tn = t["novo_ini"] + k/30
    to = novo2orig(tn)
    fb = ler(BASE, to, 1)[0]
    d = np.abs(fl.astype(int)-fb.astype(int)).sum(2); d = np.clip(d*3,0,255).astype(np.uint8)
    d = cv2.cvtColor(d, cv2.COLOR_GRAY2BGR)
    row = np.hstack([fl, fb, d]); cv2.putText(row, f"{i} lote{lote} {t['cena']}", (10,40), 0, 1.2, (0,255,255), 3)
    rows.append(cv2.resize(row, None, fx=0.4, fy=0.4))
cv2.imwrite(str(M/"chk"/"amostra_lotes.jpg"), np.vstack(rows))
