# -*- coding: utf-8 -*-
"""Remove a legenda queimada (branca/amarela com contorno preto) do B-roll do vencedor com LaMa (GPU).
Uso (_vg python): limpar_leg.py entrada.mp4 saida.mp4 de ate
Mascara: dentro da faixa y 470..640, pixels claros (branco ou amarelo) vizinhos de contorno escuro, dilatados.
Cor bt601/tv fixa na leitura e na gravacao (licao do lote Oracion)."""
import sys, subprocess, time, warnings
warnings.filterwarnings("ignore")
import cv2, numpy as np
from PIL import Image
from simple_lama_inpainting import SimpleLama

src, dst, de, ate = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
Y0, Y1 = 780, 915
ENC_VF = ["-vf", "scale=out_color_matrix=bt601:out_range=tv:flags=accurate_rnd+full_chroma_int,format=yuv420p"]
ENC_TAG = ["-bsf:v", "h264_metadata=video_full_range_flag=0:colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1"]
pr = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(de), "-t", str(ate - de), "-i", src, "-vf",
                       "scale=in_color_matrix=bt601:in_range=tv:flags=accurate_rnd+full_chroma_int,format=bgr24",
                       "-fps_mode", "passthrough", "-f", "rawvideo", "-"], stdout=subprocess.PIPE)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "720x1280", "-r", "30",
                       "-i", "-", "-an", *ENC_VF, "-c:v", "libx264", "-crf", "14", "-preset", "medium", *ENC_TAG, dst],
                      stdin=subprocess.PIPE)
lama = SimpleLama()


def mascara(f):
    m = np.zeros((1280, 720), np.uint8)
    roi = f[Y0:Y1]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    H, S, V = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    branco = (V >= 200) & (S <= 60)
    amarelo = (H >= 18) & (H <= 38) & (S >= 110) & (V >= 170)
    escuro = cv2.dilate((V < 55).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    core = ((branco | amarelo) & escuro).astype(np.uint8)
    # so linhas com bastante texto (evita reflexo isolado)
    lin = core.sum(1)
    ok = np.convolve(lin, np.ones(15), "same") > 60
    core[~ok] = 0
    d = cv2.dilate(core, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))
    d = cv2.morphologyEx(d, cv2.MORPH_CLOSE, np.ones((9, 25), np.uint8))
    m[Y0:Y1] = d
    return m


T = 720 * 1280 * 3
i, t0 = 0, time.time()
while True:
    buf = pr.stdout.read(T)
    if len(buf) < T:
        break
    f = np.frombuffer(buf, np.uint8).reshape(1280, 720, 3).copy()
    m = mascara(f)
    if m.sum():
        a0, a1 = Y0 - 100, Y1 + 100
        crop = f[a0:a1]
        r = lama(Image.fromarray(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)), Image.fromarray(m[a0:a1] * 255))
        r = cv2.cvtColor(np.array(r), cv2.COLOR_RGB2BGR)[:crop.shape[0], :crop.shape[1]].astype(np.float32)
        al = np.maximum(cv2.GaussianBlur(m[a0:a1].astype(np.float32), (11, 11), 0), m[a0:a1])[..., None]
        f[a0:a1] = np.clip(r * al + crop * (1 - al), 0, 255).astype(np.uint8)
    ff.stdin.write(f.tobytes())
    i += 1
pr.kill(); ff.stdin.close(); ff.wait()
print("ok", dst, i, "quadros", round(time.time() - t0), "s")
