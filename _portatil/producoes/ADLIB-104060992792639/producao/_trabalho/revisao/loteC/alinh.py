# confere se o tempo do final = tempo do original (MAE de quadros reduzidos, com busca de deslocamento)
import sys, cv2, numpy as np
from pathlib import Path
P = Path(r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639")
def fr(path, t):
    c = cv2.VideoCapture(str(path)); c.set(cv2.CAP_PROP_POS_MSEC, t*1000); ok, f = c.read()
    return cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (72, 128)).astype(float) if ok else None
for NN in sys.argv[1:]:
    fin = next((P/"producao").glob(f"AD {NN} - *-ES-LATAM.mp4")); ori = P/"UNICOS_HD"/f"{NN}.mp4"
    dur = cv2.VideoCapture(str(fin)).get(cv2.CAP_PROP_FRAME_COUNT)/30
    out = []
    for t in np.linspace(2, dur-2, 9):
        a = fr(fin, t)
        best = min(((np.mean(np.abs(a - fr(ori, t+dt))), dt) for dt in (-1, -0.5, 0, 0.5, 1, 2, 5, 10, 20) if fr(ori, t+dt) is not None))
        out.append(f"{t:.0f}s:{np.mean(np.abs(a-fr(ori,t))):.0f}/best{best[1]:+}({best[0]:.0f})")
    print(NN, " ".join(out))
