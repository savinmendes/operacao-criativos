# Compoe o AD FR 13.13F.
# 0..SW  : abertura do 13.13F sem legenda (LaMa) + boca/queixo do lipsync A (tela cheia) reduzido para o PiP e colado
# SW..C1 : lipsync A tela cheia (quadros 175+ da base), remendado com a base na faixa da antiga legenda ES
# B..E   : base limpa do ADS 12 (cena E a ~0,98x se precisar); F: lipsync F remendado
import numpy as np, subprocess, json, sys, cv2
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros, ENC_TAG
W, H, FPS = 720, 1280, 30
CJ = json.load(open("cortes_fr.json")); C, ES, SW = CJ["C"], CJ["ES"], CJ["SW"]; TOTAL = C[-1]
INF = json.load(open("heygen_in/info.json")); FS = INF["FS"]; n1 = INF["n1"]
AIDX = json.load(open("heygen_in/A_idx.json"))["A_idx"]
LAMA = r"C:\Users\PICHAU\Downloads\SB-EN-OFERTA-LIVE\08_ADS-12\_trabalho\lama"
BASE = LAMA + r"\base_limpa2.mp4"
A = sys.argv[1] if len(sys.argv) > 1 else "heygen/A_heygen.mp4"
F = sys.argv[2] if len(sys.argv) > 2 else "heygen/F_heygen.mp4"
SAIDA = sys.argv[3] if len(sys.argv) > 3 else "bruto_fr.mp4"
B = list(quadros(BASE)); PIP = list(quadros("lama/pip_limpa.mp4")); SRC = list(quadros("src13.mp4", 0, n1 + 2))
class Seq:
    def __init__(s, p): s.f = list(quadros(p))
    def get(s, i): return s.f[min(i, len(s.f) - 1)]
fa = Seq(A); ff = Seq(F)
M1 = np.load(LAMA + r"\mask_v1.npy"); M2 = np.load(LAMA + r"\mask.npy")
def mk(i):
    m = (np.unpackbits(M1[i])[:H * W].reshape(H, W) | np.unpackbits(M2[i])[:H * W].reshape(H, W)).astype(np.uint8)
    m = cv2.dilate(m, np.ones((15, 15), np.uint8)).astype(np.float32); return cv2.GaussianBlur(m, (0, 0), 5)[..., None]
DV = {}
def dcor(img, b, key):
    if key not in DV:
        DV[key] = (b[700:1250].astype(np.float32) - img[700:1250].astype(np.float32)).mean(axis=(0, 1)); print("desvio cor", key, DV[key])
    return np.clip(img.astype(np.float32) + DV[key], 0, 255)
def remenda(img, i, key):
    i = min(i, 944); b = B[i]; m = mk(i); img = dcor(img, b, key)
    return np.clip(b * m + img * (1 - m), 0, 255).astype(np.uint8)
# --- PiP: transformacao base(tela cheia) -> 13.13F e ajuste de cor (o PiP do 13.13F tem outra gradacao)
S = 0.6093; MW = np.float32([[S, 0, 281.03], [0, S, 680.26]])
fx = []; fy = []
for n in range(0, n1, 6):
    w = cv2.warpAffine(B[n], MW, (W, H), flags=cv2.INTER_AREA)
    fx.append(w[740:1000, 430:640].reshape(-1, 3).astype(np.float32)); fy.append(SRC[n][740:1000, 430:640].reshape(-1, 3).astype(np.float32))
fx = np.concatenate(fx); fy = np.concatenate(fy)
GA = []
qs = np.linspace(0, 100, 101)
for c in range(3):   # LUT por canal por quantis (gradacao nao linear do PiP; independe de alinhamento fino)
    px = np.percentile(fx[:, c], qs); py = np.percentile(fy[:, c], qs); px = np.maximum.accumulate(px + np.arange(101) * 1e-3)
    GA.append(np.clip(np.interp(np.arange(256), px, py), 0, 255).astype(np.float32))
print("LUT PiP (0,64,128,192,255)", [[round(float(g[v]), 1) for v in (0, 64, 128, 192, 255)] for g in GA])
# mascara da boca/queixo no quadro tela cheia (boca do Jesus ~ (380,395)); elipse suave
MB = np.zeros((H, W), np.float32); cv2.ellipse(MB, (380, 415), (120, 100), 0, 0, 360, 1.0, -1); MB = cv2.GaussianBlur(MB, (0, 0), 18)
def pip(n):
    # cola a boca/queixo do HeyGen (gradacao do PiP aplicada por LUT) direto sobre o 13.13F limpo
    g = np.clip(dcor(fa.get(n), B[AIDX[n]], "A"), 0, 255).astype(np.uint8)
    g = np.dstack([GA[c][g[..., c]] for c in range(3)])
    gw = cv2.warpAffine(g, MW, (W, H), flags=cv2.INTER_AREA)
    mb = MB
    if 38 <= n <= 64:   # dedo na frente da boca: o HeyGen apagou o dedo -> fica o pixel original onde ha dedo
        gb = cv2.cvtColor(B[AIDX[n]], cv2.COLOR_BGR2GRAY); fm = np.zeros((H, W), np.uint8)
        fm[300:620, 425:640] = (gb[300:620, 425:640] > 72).astype(np.uint8)
        fm = cv2.morphologyEx(fm, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        fm = cv2.GaussianBlur(cv2.dilate(fm, np.ones((25, 25), np.uint8)).astype(np.float32), (0, 0), 5)
        mb = MB * (1 - fm)
    mw = cv2.warpAffine(mb, MW, (W, H), flags=cv2.INTER_LINEAR)[..., None]
    return np.clip(gw * mw + PIP[n].astype(np.float32) * (1 - mw), 0, 255).astype(np.uint8)
import os
N = int(os.environ.get("LIM", round(TOTAL * FPS)))
vf = ("[0:v]scale=1080:1920:flags=lanczos,ass=leg_fr.ass:fontsdir=fonts,"
      "scale=720:1280:flags=lanczos:out_color_matrix=bt601:out_range=tv,format=yuv420p[v]")
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
      "-i", "audio/mix_fr.wav", "-filter_complex", vf, "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-crf", "17", "-preset", "medium",
      *ENC_TAG, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-t", f"{N/FPS:.3f}", "-movflags", "+faststart", SAIDA], stdin=subprocess.PIPE)
def pega(x):
    j = int(np.floor(x)); a = x - j; j = min(j, 944); f0 = B[j]
    if a < 0.05: return f0
    return cv2.addWeighted(f0, 1 - a, B[min(j + 1, 944)], a, 0)
for n in range(N):
    t = n / FPS; k = max(i for i in range(6) if C[i] <= t + 1e-6); u = t - C[k]
    if k == 0:
        img = pip(n) if n < n1 else remenda(fa.get(n), AIDX[min(n, len(AIDX) - 1)], "A")
    elif k == 5:
        j = int(round(u * FPS)); img = remenda(ff.get(j), 783 + int(round(j / FS)), "F")
    elif k == 4:
        sp = min(1.0, (ES[5] - ES[4] - 0.05) / (C[5] - C[4])); img = pega((ES[4] + u * sp) * FPS)
    else: img = pega((ES[k] + u) * FPS)
    enc.stdin.write(np.ascontiguousarray(img).tobytes())
enc.stdin.close(); enc.wait(); print("ok", SAIDA, N)
