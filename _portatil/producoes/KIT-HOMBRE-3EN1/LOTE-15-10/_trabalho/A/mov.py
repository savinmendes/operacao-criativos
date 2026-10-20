import cv2,numpy as np,sys
cap=cv2.VideoCapture(sys.argv[1]);fr=[]
while True:
    ok,f=cap.read()
    if not ok:break
    fr.append(cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(np.float32))
print(len(fr),fr[0].shape)
y0,y1,x0,x1=150,290,120,600
r0=fr[0][y0:y1,x0:x1]
for i in range(0,len(fr),12):
    s,_=cv2.phaseCorrelate(r0,fr[i][y0:y1,x0:x1]); print(i,round(s[0],2),round(s[1],2), round(float(np.abs(fr[i][y0:y1,x0:x1]-r0).mean()),2))
