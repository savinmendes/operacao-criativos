"""Lote B (compliance): apaga os frascos de remedio (e a tampa solta) da mesa de cabeceira na abertura do quarto
(q24 0-232, ate o fim da transicao com brilho). Mascara fixa (a mesa quase nao se move no plano), dilatada 9 px,
LaMa na GPU num recorte da mesa, EMA leve no tempo. Le _antes_loteB/base_sem_legenda.mp4 -> base_sem_legenda.mp4.
Uso: _vg python _tmp/loteB/frascos_lama.py"""
import time, subprocess, warnings; warnings.filterwarnings("ignore")
import cv2, numpy as np, torch
from PIL import Image
from simple_lama_inpainting import SimpleLama
ULT = 232; Y0, Y1, X0, X1 = 880, 1240, 400, 720
SRC, OUT = "_antes_loteB/base_sem_legenda.mp4", "base_sem_legenda.mp4"
M = np.zeros((1280, 720), np.uint8)
for (a, b, c, d) in [(518, 990, 564, 1090), (533, 1018, 592, 1124), (576, 1028, 639, 1132), (573, 1070, 644, 1110), (482, 1046, 600, 1104)]:
    cv2.rectangle(M, (a, b), (c, d), 1, -1)
M = cv2.dilate(M, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19)))   # ~9 px de cada lado
np.save("_tmp/loteB/frascos_mask.npy", M)
lama = SimpleLama(); print("cuda", torch.cuda.is_available(), flush=True)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","24","-i","-","-an",
    "-threads","4","-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,OUT], stdin=subprocess.PIPE)
cap = cv2.VideoCapture(SRC); ema = None; t0 = time.time(); i = 0
mk = M[Y0:Y1, X0:X1]; mf = mk.astype(np.float32); a = np.maximum(cv2.GaussianBlur(mf, (11, 11), 0), mf)[..., None]
while True:
    ok, f = cap.read()
    if not ok: break
    if i <= ULT:
        crop = f[Y0:Y1, X0:X1].copy()
        r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(mk * 255))
        r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
        ema = r if ema is None else 0.6 * r + 0.4 * ema
        f[Y0:Y1, X0:X1] = np.clip(ema * a + crop * (1 - a), 0, 255).astype(np.uint8)
        if (i + 1) % 50 == 0: print(f"[{i+1}/{ULT+1}] {100*(i+1)//(ULT+1)}% falta ~{(time.time()-t0)/(i+1)*(ULT-i):.0f} s", flush=True)
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
ff.stdin.close(); ff.wait(); print("ok", i, time.time() - t0)
