import subprocess,numpy as np,sys
V="v2.mp4"
W,H=144,256
p=subprocess.run(['ffmpeg','-v','error','-i',V,'-vf',f'scale={W}:{H}:flags=area','-pix_fmt','rgb24','-f','rawvideo','-'],capture_output=True)
a=np.frombuffer(p.stdout,np.uint8).reshape(-1,H,W,3)
np.save('fr.npy',a);print(a.shape)
