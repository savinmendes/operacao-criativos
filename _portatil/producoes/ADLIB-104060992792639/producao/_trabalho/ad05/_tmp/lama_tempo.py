import time,warnings,cv2,numpy as np,torch,sys
warnings.filterwarnings("ignore"); torch.set_num_threads(int(sys.argv[1]))
from simple_lama_inpainting import SimpleLama
from PIL import Image
lama=SimpleLama()
c=cv2.VideoCapture('../../../UNICOS_HD/05.mp4'); c.set(1,500); ok,f=c.read()
for (h,w) in [(410,720),(288,640),(256,512)]:
    img=np.ascontiguousarray(f[820:820+h,0:w]); m=np.zeros((h,w),np.uint8); m[60:180,40:w-40]=255
    t=time.time()
    for _ in range(2): lama(Image.fromarray(img),Image.fromarray(m))
    print(h,w,round((time.time()-t)/2,2),flush=True)
