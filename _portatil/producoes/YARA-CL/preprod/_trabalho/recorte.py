# Recorta os 3 frascos de produto_1.jpg (sem titulo nem pilulas de nome) com rembg (isnet/u2net local, gratis)
import sys
from PIL import Image
from rembg import remove, new_session
src = Image.open(r"C:\Users\PICHAU\Downloads\YARA-CL\_ref\produto_1.jpg").convert("RGB")
# regiao dos frascos (2048px): abaixo do titulo, acima das pilulas YARA/YARA MOI/YARA ELIXIR
box = (200, 300, 1990, 1490)
c = src.crop(box)
modelo = sys.argv[1] if len(sys.argv) > 1 else "isnet-general-use"
out = remove(c, session=new_session(modelo), alpha_matting=False)
out.save(r"C:\Users\PICHAU\Downloads\YARA-CL\preprod\_trabalho\recorte_" + modelo + ".png")
print(out.size, out.getbbox())
