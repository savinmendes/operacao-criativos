# Recria o vídeo 44 (imagem 01 animada) a partir da imagem 01 traduzida: itens entram como no original.
import subprocess
from PIL import Image
src = Image.open("../../../ES-LATAM/IMAGENS/01 AD - ES.jpg").convert("RGB").resize((720, 720), Image.LANCZOS)
S = 720 / 1080
pills = [(393, 466), (488, 561), (583, 656), (678, 751), (773, 846)]
X0, X1 = int(50 * S), int(550 * S)
# (início, fim) da entrada de cada item (wipe esq.->dir.), tempos do original 44 (24 fps)
anim = [(0.0, 0.04), (0.12, 0.25), (0.17, 0.33), (0.54, 0.67), (0.75, 0.92)]
FPS, DUR = 30, 3.375
n = int(round(DUR * FPS))
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "720x720", "-r", str(FPS),
                      "-i", "-", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", "base.mp4"], stdin=subprocess.PIPE)
for i in range(n):
    t = i / FPS
    fr = src.copy()
    if i > 0:  # 1º quadro mostra tudo (miniatura), como no original
        for (y0, y1), (a, b) in zip(pills, anim):
            f = 1.0 if t >= b else (0.0 if t < a else (t - a) / (b - a))
            ya, yb = int(y0 * S) - 3, int(y1 * S) + 3
            xr = X0 + int((X1 - X0) * f)
            if xr < X1:
                fr.paste((255, 255, 255), (xr, ya, X1, yb))
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
print("ok base.mp4", n, "quadros")
