# -*- coding: utf-8 -*-
"""AD 23 (já é Lymphoria, sem oferta falada): vídeo ampliado + setas de CTA a partir de "Dejé el enlace abajo"
+ selo universal reduzido (abaixo da legenda queimada, acima das setas). Finaliza pelo kit."""
import subprocess
import sys
from pathlib import Path

from PIL import Image

KIT = Path(r"C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos")
sys.path.insert(0, str(KIT / "ferramentas"))
import overlays as OV  # noqa: E402
import finalizar as FIN  # noqa: E402

W = Path(__file__).parent
SAIDA = r"C:\Users\PICHAU\Downloads\LHYMPORIA AD 01-20\lymphoria\AD 23 - LYMPHORIA-SUPERMERCADO-ES-LATAM.mp4"
T_CTA = 538.3          # "Dejé el enlace abajo"
ESC = 0.62

selo = OV.selo(["ENVÍO GRATIS A DOMICILIO", "PAGO CONTRA", "ENTREGA", "¡PAGAS AL RECIBIR!"], str(W / "selo.png"))
im = Image.open(selo)
im = im.resize((int(im.width * ESC), int(im.height * ESC)), Image.LANCZOS)
im.save(W / "selo_p.png")
x_selo = (1080 - im.width) // 2
seta = OV.seta(str(W / "seta.png"))
fc = (f"[0:v][1:v]overlay={x_selo}:1385:enable='gte(t,{T_CTA})'[a];"
      f"[a][2:v]overlay=300:'1640+20*sin(3*PI*t)':enable='gte(t,{T_CTA})'[b];"
      f"[b][3:v]overlay=610:'1640+20*sin(3*PI*t)':enable='gte(t,{T_CTA})'[v]")
bruto = W / "bruto.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "parte1_up.mp4"), "-i", str(W / "selo_p.png"),
                "-i", seta, "-i", seta, "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
                "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", str(bruto)],
               check=True)
FIN.encode(str(bruto), SAIDA, 30)
FIN.revisar(SAIDA, str(Path(SAIDA).with_suffix("")) + "_frames.jpg", [5.0, 300.0, T_CTA + 1.0, -1.0])
