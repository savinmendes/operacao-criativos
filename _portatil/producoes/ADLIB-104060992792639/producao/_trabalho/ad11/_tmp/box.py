import cv2, numpy as np
cap=cv2.VideoCapture('UNICOS_HD/11.mp4'); n=int(cap.get(7))
acc=np.zeros((1280,720),np.float32); cnt=0
for i in range(0,n,10):
    cap.set(1,i); ok,f=cap.read()
    if not ok: break
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY)
    bright=(g>200)
    dark=cv2.dilate((g<60).astype(np.uint8),np.ones((5,5)))>0
    m=bright & dark  # bright next to dark outline
    acc+=m; cnt+=1
p=acc/cnt
rows=p.sum(1); cols=p.sum(0)
ys=np.where(rows>rows.max()*0.05)[0]; xs=np.where(cols>cols.max()*0.05)[0]
print('frames',cnt,'y',ys.min(),ys.max(),'x',xs.min(),xs.max())
for y in range(780,1020,10): print(y, round(rows[y:y+10].sum(),2))
cv2.imwrite('producao/_trabalho/ad11/_tmp/heat.png',(p/p.max()*255).astype(np.uint8))
