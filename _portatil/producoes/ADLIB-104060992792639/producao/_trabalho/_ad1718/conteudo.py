# Mede se o degrau que sobrou e conteudo (boca nova x boca original) e nao cor: HeyGen saida - entrada (mesmo dominio),
# dentro da elipse da boca x anel fora dela, por trecho.
import sys, json, cv2, numpy as np
from pathlib import Path
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
NN = sys.argv[1]; AQ = Path(__file__).resolve().parent.parent / f"ad{NN}" / "lipsync"; CFG = json.loads((AQ / "segs.json").read_text())
for s in CFG["segs"]:
    nm = s["nome"]
    if len(sys.argv) > 2 and nm not in sys.argv[2:]: continue
    C = np.load(AQ / s.get("cx", f"caixas_{nm}.npy")); arq = {"s00": "ls_s00_loteB.mp4"}.get(nm, f"ls_{nm}.mp4") if NN == "17" else f"ls_{nm}.mp4"
    o = list(quadros(AQ / "out" / arq, 0, len(C))); p = list(quadros(AQ / "in" / f"pt_{nm}.mp4", 0, len(C))); r = []
    for k in range(0, min(len(o), len(p)), 3):
        x0, y0, w, h, mx, my, fw, fh = C[k]; sc = 720 / w; c = (int((mx - x0) * sc), int((my + 0.02 * fh - y0) * sc)); ax = (int(0.40 * fw * sc), int(0.30 * fh * sc))
        e = np.zeros((1280, 720), np.uint8); cv2.ellipse(e, c, (int(ax[0] * 0.7), int(ax[1] * 0.7)), 0, 0, 360, 1, -1)
        a = np.zeros((1280, 720), np.uint8); cv2.ellipse(a, c, (int(ax[0] * 1.8), int(ax[1] * 1.8)), 0, 0, 360, 1, -1); a = (a > 0) & (e == 0)
        yo = cv2.cvtColor(o[k], cv2.COLOR_BGR2GRAY).astype(float); yp = cv2.cvtColor(p[k], cv2.COLOR_BGR2GRAY).astype(float)
        r.append(((yo - yp)[e > 0].mean(), (yo - yp)[a].mean()))
    r = np.median(np.array(r), 0); print(f"{nm}: saida-entrada boca {r[0]:+.1f} anel {r[1]:+.1f} -> conteudo {r[0]-r[1]:+.1f}")
