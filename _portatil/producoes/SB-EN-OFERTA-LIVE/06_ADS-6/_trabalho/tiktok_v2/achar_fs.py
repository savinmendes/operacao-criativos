import subprocess,numpy as np
from PIL import Image
ref=np.array(Image.open("card_en_v2_ORIGINAL_ref.png")).astype(int)
for fs in range(40,90):
    subprocess.run(["python","card_v2_sem_emoji.py","_t.png",str(fs),"One last warning","Stay until the end and","pay close attention"],capture_output=True)
    try: t=np.array(Image.open("_t.png")).astype(int)
    except: continue
    print(fs,np.abs(t-ref).mean())
