from rembg import remove, new_session
from PIL import Image
s=new_session("isnet-general-use")
for n in ["taladro_02","taladro_01","maleta_02","kit04","bateria_02"]:
    im=Image.open(n+".jpg").convert("RGB")
    out=remove(im,session=s)
    out.save(n+"_cut.png"); print(n, out.getbbox())
