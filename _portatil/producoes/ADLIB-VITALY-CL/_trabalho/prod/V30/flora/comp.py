# -*- coding: utf-8 -*-
"""Take Kling (já encaixado) + legenda branca e foto 'antes' do original (cap.mp4) por cima, só onde existem."""
import subprocess, cv2, numpy as np
o = cv2.VideoCapture("t1.mp4"); e = cv2.VideoCapture("t1_enc.mp4")
W, H = 720, 1280
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30",
                       "-i", "-", "-c:v", "libx264", "-crf", "15", "-pix_fmt", "yuv420p", "t1_comp.mp4"], stdin=subprocess.PIPE)
for i in range(82):
    _, a = o.read(); ok, b = e.read()
    if not ok: b = a
    m = np.zeros((H, W), np.uint8)
    # caixa branca da legenda (região 20..520 x 755..990): brancos + fecho para englobar as letras pretas
    reg = (a[755:990, 20:520].min(2) > 225).astype(np.uint8)
    if reg.mean() > 0.25:
        reg = cv2.morphologyEx(reg, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
        m[755:990, 20:520] = reg
    # foto do "antes" (moldura vermelho-escura no canto direito) enquanto estiver na tela
    ph = a[560:600, 420:640].astype(int)
    if i <= 14 and (ph[..., 2] > ph[..., 1] + 25).mean() > 0.3:
        m[552:1112, 398:662] = 1
    mf = cv2.GaussianBlur(m.astype(np.float32), (5, 5), 0)[..., None]
    q = (a * mf + b * (1 - mf)).astype(np.uint8)
    ff.stdin.write(q.tobytes())
ff.stdin.close(); ff.wait(); print("ok")
