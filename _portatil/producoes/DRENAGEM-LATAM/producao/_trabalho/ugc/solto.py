import cv2,json,sys,glob,numpy as np
nn=sys.argv[1]
f=glob.glob(f'../../UGC {nn} - *.mp4')[0]
ins=json.load(open(f'ugc{nn}/insertos.json'))
c=cv2.VideoCapture(f);fps=c.get(5)
for t0,d,cl in ins:
    for b in (t0,t0+d):
        i0=int(b*fps)-3;c.set(1,i0);fr=[]
        for k in range(7):
            ok,im=c.read();fr.append(cv2.resize(im,(90,160)).astype(float))
        df=[np.abs(fr[k+1]-fr[k]).mean() for k in range(6)]
        print(cl,f'{b:.2f}',' '.join(f'{x:.0f}' for x in df))
