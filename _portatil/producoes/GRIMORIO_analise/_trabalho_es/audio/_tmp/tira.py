import sys, numpy as np, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\GRIMORIO_analise\_trabalho_es\audio"); import cor
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas"); import checar_lipsync as cl
import librosa
nome, passo = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 3
B = cor.ler(f"out/{nome}.mp4")
y, sr = librosa.load(f"in/es_{nome}.mp3", sr=16000); hop = sr // 30
env = np.array([np.sqrt(np.mean(y[k*hop:(k+1)*hop]**2)) for k in range(len(B))]); env = env / env.max()
d = cl.Rastreador(); p = d.pontos(cv2.cvtColor(B[len(B)//2], cv2.COLOR_RGB2BGR)); m = p[[13,14,61,291]].mean(0); x, yy = int(m[0]), int(m[1])
tiles = []
for k in range(0, len(B), passo):
    t = B[k][yy-50:yy+50, x-80:x+80].copy()
    bar = np.zeros((14, 160, 3), np.uint8); bar[:, :int(160*env[k])] = (255, 200, 0)
    tiles.append(np.vstack([t, bar]))
rows = [np.hstack(tiles[i:i+16]) for i in range(0, len(tiles), 16)]
W = max(r.shape[1] for r in rows); rows = [np.pad(r, ((0, 3), (0, W - r.shape[1]), (0, 0))) for r in rows]
cv2.imwrite(f"../_tmp/tira_{nome}.jpg", cv2.cvtColor(np.vstack(rows), cv2.COLOR_RGB2BGR))
