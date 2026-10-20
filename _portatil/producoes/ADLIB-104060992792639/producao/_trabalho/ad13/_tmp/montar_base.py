"""Monta base_sem_legenda.mp4 do 13 (720x1280, 30 fps, sem audio).
- Legenda PT (faixa y 972-1024) e mao-icone (98-104 s): LaMa local por quadro, so dentro da mascara.
- 2517-2667 (cena com pessoa real parecida com apresentadora de TV): recorte do quarto (crucifixo/cama), sem a pessoa, push-in lento.
Uso: python _tmp/montar_base.py ini fim saida.mp4  (faixa de quadros [ini, fim))"""
import subprocess, sys, warnings
import cv2, numpy as np, torch
from PIL import Image
warnings.filterwarnings("ignore")
torch.set_num_threads(int(sys.argv[4]) if len(sys.argv) > 4 else 8)
from simple_lama_inpainting import SimpleLama
A, B, OUT = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
W, H = 720, 1280
BM = np.load('_tmp/boxmasks.npy')
lama = SimpleLama()
C0, C1 = 840, 1200
AMB0, AMB1 = 2517, 2668          # [AMB0, AMB1)
MAO0, MAO1 = 2950, 3112


def zoom_recorte(f, x, y, w, h, z):
    cx, cy = x + w / 2, y + h / 2
    w2, h2 = w / z, h / z
    M = np.float32([[W / w2, 0, -(cx - w2 / 2) * W / w2], [0, H / h2, -(cy - h2 / 2) * H / h2]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)


c = cv2.VideoCapture('../../../UNICOS_HD/13.mp4'); c.set(cv2.CAP_PROP_POS_FRAMES, A)
cz = cv2.VideoCapture('../../../UNICOS_HD/13.mp4')
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                       "-i", "-", "-an", "-c:v", "libx264", "-crf", "13", "-preset", "medium", "-pix_fmt", "yuv420p", OUT],
                      stdin=subprocess.PIPE)
for i in range(A, B):
    ok, f = c.read()
    if not ok:
        break
    if AMB0 <= i < AMB1:
        k = (i - AMB0) / (AMB1 - AMB0 - 1)
        g = zoom_recorte(f, 30, 0, 270, 480, 1.0 + 0.07 * k)
        g = cv2.addWeighted(g, 1.5, cv2.GaussianBlur(g, (0, 0), 1.6), -0.5, 0)   # leve nitidez
    else:
        mk = np.zeros((C1 - C0, W), np.uint8)
        mk[960 - C0:1030 - C0] = BM[i]
        if MAO0 <= i < MAO1:
            mk[1000 - C0:1158 - C0, 278:432] = 1
        if mk.any():
            crop = f[C0:C1].copy()
            mk = cv2.dilate(mk, np.ones((5, 5), np.uint8))
            r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
            r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]]
            a = cv2.GaussianBlur(mk.astype(np.float32), (9, 9), 0)[..., None]
            a = np.maximum(a, mk[..., None].astype(np.float32))
            g = f.copy(); g[C0:C1] = np.clip(r * a + crop * (1 - a), 0, 255).astype(np.uint8)
        else:
            g = f
    ff.stdin.write(np.ascontiguousarray(g).tobytes())
    if (i - A) % 100 == 0:
        print(f"[{i - A}/{B - A}] {100 * (i - A) // (B - A)}%", flush=True)
ff.stdin.close(); ff.wait()
print("ok", OUT)
