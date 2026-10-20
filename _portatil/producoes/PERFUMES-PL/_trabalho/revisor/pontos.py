import cv2, numpy as np, subprocess, sys
W,H=720,200; Y0=740
for n in sys.argv[1:]:
    p=subprocess.Popen(['ffmpeg','-v','error','-i',rf'C:\Users\PICHAU\Downloads\PERFUMES-PL\PARA-SUBIR\{n}.mp4','-vf',f'fps=10,crop={W}:{H}:0:{Y0}','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
    k=0; hits=[]
    while True:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        im=np.frombuffer(b,np.uint8).reshape(H,W,3); g=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        dark=(g<55).astype(np.uint8)
        nl,lab,st,cen=cv2.connectedComponentsWithStats(dark,8)
        for j in range(1,nl):
            x,y,w,h,a=st[j]
            if 15<=a<=250 and w<=22 and h<=22 and x>3 and x+w<W-3 and y>3 and y+h<H-3:
                ring=cv2.dilate((lab==j).astype(np.uint8),np.ones((15,15),np.uint8))-cv2.dilate((lab==j).astype(np.uint8),np.ones((5,5),np.uint8))
                m=g[ring>0]
                if m.mean()>120 and m.min()>60:
                    hits.append((k/10,int(x),int(y+Y0),int(a)))
        k+=1
    print(n, len(hits))
    for h in hits: print('  ',h)
