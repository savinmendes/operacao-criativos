"""Troca o light-leak do original (q284-292, 2 clarões que o revisar_ad acusa como quadro solto) por um flash branco suave
entre o ultimo quadro limpo da tomada 1 (q283) e o 1o da tomada 2 (q293). Reescreve base_lipsync.mp4 (copia em _tmp)."""
import shutil, subprocess, cv2, numpy as np
shutil.copy("base_lipsync.mp4", "_tmp/base_lipsync_sem_flash.mp4")
cap = cv2.VideoCapture("_tmp/base_lipsync_sem_flash.mp4"); fr = []
while True:
    ok, f = cap.read()
    if not ok: break
    fr.append(f)
A, B = fr[283].astype(np.float32), fr[293].astype(np.float32)
for k in range(284, 293):
    t = (k - 283) / 10; src = A if t < 0.5 else B; w = 0.92 * np.sin(np.pi * t)
    fr[k] = np.clip(src * (1 - w) + np.array([235, 245, 250], np.float32) * w, 0, 255).astype(np.uint8)
COR = ["-color_range","tv","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709"]
ff = subprocess.Popen(["ffmpeg","-v","error","-y","-f","rawvideo","-pix_fmt","bgr24","-s","720x1280","-r","30","-i","-","-threads","4",
    "-c:v","libx264","-crf","14","-preset","medium","-pix_fmt","yuv420p",*COR,"-an","base_lipsync.mp4"], stdin=subprocess.PIPE)
for f in fr: ff.stdin.write(f.tobytes())
ff.stdin.close(); ff.wait(); print("ok", len(fr))
