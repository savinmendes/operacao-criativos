"""Refaz a cena do quarto (quadros 2517-2667) na base_sem_legenda.mp4 a partir de UM quadro parado (2560) do original,
recortado sem a pessoa (crucifixo + cabeceira) com push-in lento. Evita a transicao espelhada e a costura lateral do original."""
import subprocess, cv2, numpy as np, os
W, H = 720, 1280; A0, A1 = 2517, 2668
c = cv2.VideoCapture('../../../UNICOS_HD/13.mp4'); c.set(cv2.CAP_PROP_POS_FRAMES, 2560); ok, src = c.read()
def zoom_recorte(f, x, y, w, h, z):
    cx, cy = x + w / 2, y + h / 2; w2, h2 = w / z, h / z
    M = np.float32([[W / w2, 0, -(cx - w2 / 2) * W / w2], [0, H / h2, -(cy - h2 / 2) * H / h2]])
    return cv2.warpAffine(f, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
b = cv2.VideoCapture('base_sem_legenda.mp4')
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                       "-an", "-c:v", "libx264", "-crf", "13", "-preset", "medium", "-pix_fmt", "yuv420p", "_tmp/base_nova.mp4"], stdin=subprocess.PIPE)
i = 0
while True:
    ok, f = b.read()
    if not ok: break
    if A0 <= i < A1:
        k = (i - A0) / (A1 - A0 - 1)
        g = zoom_recorte(src, 30, 0, 270, 480, 1.0 + 0.08 * k)
        f = cv2.addWeighted(g, 1.5, cv2.GaussianBlur(g, (0, 0), 1.6), -0.5, 0)
    ff.stdin.write(np.ascontiguousarray(f).tobytes()); i += 1
ff.stdin.close(); ff.wait(); print('quadros', i)
os.replace('_tmp/base_nova.mp4', 'base_sem_legenda.mp4')
cv2.imwrite('_tmp/quarto_src.jpg', cv2.resize(zoom_recorte(src, 30, 0, 270, 480, 1.0), (360, 640)))
