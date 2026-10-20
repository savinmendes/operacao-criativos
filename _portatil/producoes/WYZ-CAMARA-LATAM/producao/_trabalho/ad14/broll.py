# Gera os takes sem rosto (720x1280, 30 fps, sem audio) com recorte que tira a legenda em ingles
# e desfoque das gravacoes (rostos de terceiros).
import subprocess, sys
from pathlib import Path
O = Path(r"C:\Users\PICHAU\Downloads\WYZ-CAMARA-LATAM\originais")
def take(src, ini, fim, crop, blur, out, vel=1.0):
    # blur: (x0,y0,x1,y1) em coords do original, aplicado antes do recorte
    x, y, w, h = crop
    dur = fim - ini
    if blur:
        bx0, by0, bx1, by1 = blur
        fc = (f"[0:v]split[a][b];[b]crop={bx1-bx0}:{by1-by0}:{bx0}:{by0},gblur=sigma=5[bl];"
              f"[a][bl]overlay={bx0}:{by0}[m];[m]crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos,setsar=1,"
              f"setpts=(PTS-STARTPTS)/{vel},fps=30[v]")
    else:
        fc = f"[0:v]crop={w}:{h}:{x}:{y},scale=720:1280:flags=lanczos,setsar=1,setpts=(PTS-STARTPTS)/{vel},fps=30[v]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-threads", "4", "-ss", f"{ini}", "-t", f"{dur}", "-i", str(O / src),
                    "-filter_complex", fc, "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                    "-pix_fmt", "yuv420p", str(out)], check=True)
    print(out, subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)],
                              capture_output=True, text=True).stdout.strip())
if __name__ == "__main__":
    D = Path(__file__).parent
    # B1: gravacoes sobre as maos (360/2K/IA) - inset desfocado; recorte tira cabelo do criador (topo) e a legenda (base)
    take("14.mp4", 9.70, 17.40, (138, 150, 444, 790), (30, 150, 690, 528), D / "b1.mp4")
    # B2: instalacao na parede (sem inset); B3: gravacoes sobre a parede (inset aparece em 32.80) - desfocado
    take("14.mp4", 28.45, 32.78, (90, 0, 540, 960), None, D / "b2.mp4", vel=0.85)
    # 32.8-34.9 cortado: menor de idade (terceiro) em tela cheia, de costas
    take("14.mp4", 34.95, 38.60, (90, 0, 540, 960), (46, 156, 690, 516), D / "b3.mp4", vel=0.85)
