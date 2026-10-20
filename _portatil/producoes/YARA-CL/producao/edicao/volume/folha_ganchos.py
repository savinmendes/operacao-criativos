# folha comparando os 3 primeiros segundos dos 5 ganchos (1 linha por gancho, quadro a cada 0,3 s)
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
V = Path(r"C:\Users\PICHAU\Downloads\YARA-CL\entregas\volume")
TS = [round(0.0 + 0.3 * i, 2) for i in range(11)]  # 0 .. 3,0 s
w, h = 180, 320
f = ImageFont.truetype(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\fonts\Poppins-Bold.ttf", 22)
sheet = Image.new("RGB", (70 + len(TS) * w, 30 + 5 * h), (30, 30, 30))
d = ImageDraw.Draw(sheet)
for j, t in enumerate(TS):
    d.text((70 + j * w + 60, 2), f"{t:.1f}s", font=f, fill=(255, 255, 0))
for i in range(5):
    v = V / f"YARA-BF_H{i + 1}_sem-musica.mp4"
    sel = "+".join(f"eq(n\,{int(round(t * 30))})" for t in TS)
    tmp = V / "_tmp_row.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(v), "-vf", f"select='{sel}',scale={w}:{h},tile={len(TS)}x1",
                    "-frames:v", "1", "-fps_mode", "passthrough", str(tmp)], check=True)
    sheet.paste(Image.open(tmp), (70, 30 + i * h))
    d.text((8, 30 + i * h + h // 2 - 12), f"H{i + 1}", font=f, fill=(255, 255, 0))
    tmp.unlink()
sheet.save(V / "folha_ganchos_3s.jpg", quality=85)
print(V / "folha_ganchos_3s.jpg")
