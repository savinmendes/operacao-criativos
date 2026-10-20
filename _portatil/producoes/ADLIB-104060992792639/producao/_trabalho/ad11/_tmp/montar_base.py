"""Monta ad11/base_sem_legenda.mp4 (720x1280, 30 fps, sem áudio).
- 0-264 menina e 265-270 flash: LaMa local (simple-lama) com máscara retangular por linha de legenda.
- 271-358, 462-935, 1138-fim mulher: placa limpa temporal (vem de _tmp/semleg_v2.mp4).
- 359-461 (cédulas R$100): zoom lento num recorte do olival (fundo da cena da mulher, sem rosto).
- 936-1137 crossfade + b-roll do mercado: recorte da parte de cima (y 0-836) com zoom 1,53x, sem a faixa da legenda.
"""
import subprocess, warnings
import cv2
import numpy as np
from PIL import Image

warnings.filterwarnings("ignore")
from simple_lama_inpainting import SimpleLama

ORIG = '../../../UNICOS_HD/11.mp4'
V2 = '_tmp/semleg_v2.mp4'
OUT = 'base_sem_legenda.mp4'
W, H = 720, 1280
BM = np.load('_tmp/boxmasks.npy')
lama = SimpleLama()
# quadros da mulher com braço/mão passando pela faixa (placa estática não serve): usa LaMa
MOV = np.load('_tmp/mov.npy')
USA_LAMA = np.zeros(len(MOV), bool)
for j in np.nonzero(MOV > 12)[0]:
    USA_LAMA[max(0, j - 6):j + 7] = True
print("quadros da mulher com LaMa:", int((USA_LAMA & (MOV >= 0)).sum()))
ema = None


def ler(src):
    c = cv2.VideoCapture(src)
    fr = []
    while True:
        ok, f = c.read()
        if not ok:
            break
        fr.append(f)
    return fr


co, cv, cz = cv2.VideoCapture(ORIG), cv2.VideoCapture(V2), cv2.VideoCapture(ORIG)
N = int(co.get(cv2.CAP_PROP_FRAME_COUNT))
assert int(cv.get(cv2.CAP_PROP_FRAME_COUNT)) == N
for _ in range(462):
    cz.read()


def lama_faixa(f, m):
    crop = f[680:1136].copy()
    mk = np.zeros(crop.shape[:2], np.uint8)
    mk[836 - 680:980 - 680] = cv2.dilate(m.astype(np.uint8), np.ones((7, 7), np.uint8))
    r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
    r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
    g = f.copy()
    # só troca a área da máscara (com borda suave), o resto fica idêntico ao original
    a = cv2.GaussianBlur(mk.astype(np.float32), (9, 9), 0)[..., None]
    a = np.maximum(a, mk[..., None].astype(np.float32))
    g[680:1136] = np.clip(r * a + crop * (1 - a), 0, 255).astype(np.uint8)
    return g


def zoom_recorte(f, x, y, w, h, z):
    """recorta (x,y,w,h) com zoom z em torno do centro e escala para 720x1280"""
    cx, cy = x + w / 2, y + h / 2
    w2, h2 = w / z, h / z
    M = np.float32([[W / w2, 0, -(cx - w2 / 2) * W / w2], [0, H / h2, -(cy - h2 / 2) * H / h2]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)


ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                       "-r", "30", "-i", "-", "-an", "-c:v", "libx264", "-crf", "14", "-preset", "slow",
                       "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
for i in range(N):
    ok1, fo = co.read(); ok2, fv = cv.read()
    if not ok1:
        break
    if i <= 264:
        g = lama_faixa(fo, BM[i])
        # suaviza o tremor do preenchimento entre quadros (câmera quase parada na menina)
        faixa = g[836:980].astype(np.float32)
        ema = faixa if ema is None else 0.5 * faixa + 0.5 * ema
        mk = cv2.dilate(BM[i].astype(np.uint8), np.ones((7, 7), np.uint8)).astype(np.float32)
        a = cv2.GaussianBlur(mk, (9, 9), 0)[..., None]
        g[836:980] = np.clip(ema * a + faixa * (1 - a), 0, 255).astype(np.uint8)
    elif i <= 270:
        g = lama_faixa(fo, BM[i] | BM[264] | BM[271])
    elif 359 <= i <= 461:
        k = i - 359                       # 0..102
        ok3, src = cz.read()               # olival da cena da mulher (15,4 s em diante), canto sup. direito
        z = 1.0 + 0.08 * k / 102          # push-in lento
        g = zoom_recorte(src, 500, 0, 220, 391, z)
    elif 936 <= i <= 1137:
        t = i / 30.0
        # janela 358x636 (y 196-832, acima da faixa da legenda) seguindo o rosto da moça
        kt = [31.2, 32.0, 33.0, 34.0, 35.0, 36.0, 37.0, 37.5, 37.95]
        kx = [0.0, 0.0, 60.0, 80.0, 40.0, 10.0, 40.0, 180.0, 250.0]
        x0 = float(np.interp(t, kt, kx))
        g = zoom_recorte(fo, x0, 196, 358, 636, 1.0)
    elif MOV[i] >= 0 and USA_LAMA[i]:
        g = lama_faixa(fo, BM[i])
    else:
        g = fv
    ff.stdin.write(np.ascontiguousarray(g).tobytes())
    if i % 60 == 0:
        print(f"[{i}/{N}] {100 * i // N}%", flush=True)
ff.stdin.close()
ff.wait()
print("ok", OUT)
