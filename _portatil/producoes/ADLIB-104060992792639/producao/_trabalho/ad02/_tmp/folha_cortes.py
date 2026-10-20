"""Folha de 1 em 1 quadro em volta de cada corte: python folha_cortes.py video.mp4 saida.jpg q1,q2,...  (q-3 .. q+3 por linha)"""
import sys, cv2, numpy as np
v,out,qs=sys.argv[1],sys.argv[2],[int(x) for x in sys.argv[3].split(",")]
cap=cv2.VideoCapture(v); rows=[]
for q in qs:
    r=[]
    for k in range(q-3,q+4):
        cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,k)); ok,f=cap.read()
        f=cv2.resize(f,(144,256)) if ok else np.zeros((256,144,3),np.uint8)
        cv2.putText(f,str(k),(4,16),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),1)
        if k==q: cv2.rectangle(f,(0,0),(143,255),(0,0,255),2)
        r.append(f)
    rows.append(np.hstack(r))
cv2.imwrite(out,np.vstack(rows)); print(out)
