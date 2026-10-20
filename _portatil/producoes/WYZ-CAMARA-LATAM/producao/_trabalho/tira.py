import subprocess, sys, numpy as np
from PIL import Image
v, y0, y1, passo, saida = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
h = y1 - y0
raw = subprocess.run(['ffmpeg','-v','error','-threads','4','-i',v,'-vf',f'fps={1/passo},crop=720:{h}:0:{y0},scale=360:{h//2}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
fr = np.frombuffer(raw,np.uint8).reshape(-1,h//2,360,3)
cols = 3; rows = -(-len(fr)//cols)
c = Image.new('RGB',(360*cols, rows*(h//2+2)),'red')
for i,f in enumerate(fr): c.paste(Image.fromarray(f),((i%cols)*360,(i//cols)*(h//2+2)))
c.save(saida); print(len(fr),'quadros')
