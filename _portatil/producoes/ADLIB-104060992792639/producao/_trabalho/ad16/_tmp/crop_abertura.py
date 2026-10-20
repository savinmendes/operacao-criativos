# Transicao 292-297 (glitch do original, mostrava o plano aberto da cadeira): troca por dissolve A(291 recortado)->B(298) com clarao quente.
# Abertura (q0-291, cadeira de rodas): recorte 360x640 em (200,180) ampliado 2x -> base_sem_legenda_crop.mp4
import cv2, subprocess, numpy as np
cap = cv2.VideoCapture("base_sem_legenda.mp4")
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-an","-threads","4",
    "-c:v","libx264","-crf","12","-preset","medium","-pix_fmt","yuv420p",*COR,"base_sem_legenda_crop.mp4"], stdin=subprocess.PIPE)
fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
for k in range(292):
    fr[k] = cv2.resize(fr[k][180:820, 200:560], (720, 1280), interpolation=cv2.INTER_LANCZOS4)
A, B = fr[291].astype(np.float32), fr[298].astype(np.float32); flash = np.full_like(A, 0); flash[:] = (200, 225, 255)
for k in range(292, 298):
    t = (k - 291) / 7; w = 0.55 * np.sin(np.pi * t)
    fr[k] = np.clip((A * (1 - t) + B * t) * (1 - w) + flash * w, 0, 255).astype(np.uint8)
for f in fr: ff.stdin.write(f.tobytes())
k = len(fr)
ff.stdin.close(); ff.wait(); print("ok", k)
