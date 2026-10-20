# folha de contato da região da boca com o tempo: python boca.py video x y w h [fps] [ini] [fim]
import sys, subprocess, numpy as np, cv2
v, x, y, w, h = sys.argv[1], *map(int, sys.argv[2:6]); fps = float(sys.argv[6]) if len(sys.argv) > 6 else 6
ini = float(sys.argv[7]) if len(sys.argv) > 7 else 0; fim = float(sys.argv[8]) if len(sys.argv) > 8 else 999
p = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ini), "-to", str(fim), "-i", v, "-vf", f"fps={fps},crop={w}:{h}:{x}:{y}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
F = np.frombuffer(p, np.uint8).reshape(-1, h, w, 3).copy(); cols = 12; out = []
for k, f in enumerate(F): cv2.putText(f, f"{ini + k / fps:.2f}", (2, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
rows = [np.hstack(list(F[i:i + cols]) + [np.zeros_like(F[0])] * (cols - len(F[i:i + cols]))) for i in range(0, len(F), cols)]
cv2.imwrite(v.rsplit(".", 1)[0] + "_boca.jpg", np.vstack(rows)); print(len(F))
