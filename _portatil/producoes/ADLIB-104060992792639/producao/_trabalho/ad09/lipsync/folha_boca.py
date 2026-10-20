"""Folha de boca: final (cima) x original (baixo), de k em k quadros, com marca da voz ES (verde) e PT (vermelho).
Uso: python folha_boca.py NN saida.jpg q_ini q_fim passo x,y,w,h"""
import sys, cv2, numpy as np, subprocess
NN, out, a, b, p = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
x, y, w, h = [int(v) for v in sys.argv[6].split(",")]
def env(f):
    r = subprocess.run(["ffmpeg","-v","error","-i",f,"-ac","1","-ar","24000","-f","s16le","-"],capture_output=True).stdout
    s = np.frombuffer(r, np.int16).astype(np.float32); n = len(s) // 1000
    e = np.sqrt((s[:n*1000].reshape(n, 1000) ** 2).mean(1)); return e / (e.max() + 1e-6)
ees, ept = env("../narracao_es.wav"), env("../_audio/demucs/htdemucs/orig/vocals.wav")
c1 = cv2.VideoCapture("../base_lipsync.mp4"); c2 = cv2.VideoCapture(f"../../../../UNICOS_HD/{NN}.mp4")
cols = []
for k in range(a, b + 1, p):
    c1.set(cv2.CAP_PROP_POS_FRAMES, k); c2.set(cv2.CAP_PROP_POS_FRAMES, k)
    _, f1 = c1.read(); _, f2 = c2.read()
    t1, t2 = cv2.resize(f1[y:y+h, x:x+w], (120, 120)), cv2.resize(f2[y:y+h, x:x+w], (120, 120))
    bar = np.zeros((14, 120, 3), np.uint8)
    if k < len(ees) and ees[k] > 0.05: bar[:7] = (0, 200, 0)
    if k < len(ept) and ept[k] > 0.05: bar[7:] = (0, 0, 220)
    cv2.putText(t1, f"{k/24:.2f}", (2, 12), 0, 0.4, (0, 255, 255), 1)
    cols.append(np.vstack([t1, bar, t2]))
C = 12; rows = []
while len(cols) % C: cols.append(np.zeros_like(cols[0]))
for i in range(0, len(cols), C): rows.append(np.hstack(cols[i:i+C]))
cv2.imwrite(out, np.vstack(rows)); print(out)
