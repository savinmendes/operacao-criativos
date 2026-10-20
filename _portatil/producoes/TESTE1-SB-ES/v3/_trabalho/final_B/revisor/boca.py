import sys,subprocess,numpy as np,cv2
V=r'C:/Users/PICHAU/Downloads/TESTE1-SB-ES/v4/SB-ES_NOTICIA-AURELIO_B-ORACION-COMPLETA_FICTICIO.mp4'
out=sys.argv[1];fs=[int(x) for x in sys.argv[2:]]
sel='+'.join('eq(n'+chr(92)+',%d)'%f for f in fs)
w,h=200,220
p=subprocess.run(['ffmpeg','-v','error','-i',V,'-vf',f"select='{sel}',crop=200:220:250:410",'-fps_mode','passthrough','-f','rawvideo','-pix_fmt','bgr24','-'],capture_output=True)
a=np.frombuffer(p.stdout,np.uint8).reshape(-1,h,w,3).copy()
for im,f in zip(a,fs): cv2.putText(im,f'{f/30:.2f}',(3,14),0,0.45,(0,255,255),1)
cols=10;rows=(len(a)+cols-1)//cols
g=np.zeros((rows*h,cols*w,3),np.uint8)
for i,im in enumerate(a): g[(i//cols)*h:(i//cols+1)*h,(i%cols)*w:(i%cols+1)*w]=im
cv2.imwrite(out,g)
