import sys,json,numpy as np,cv2
sys.path.insert(0,r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho")
from comum3 import quadros
v=r"C:\Users\PICHAU\Downloads\SB-EN-NOVOS-VENCEDORES\01_AVATAR-REST\_trabalho\SB-EN-AVATAR-REST_v2.mp4"
cuts=[4.9,8.7,10.7,12.98,15.2,17.07,20.3,22.35,25.88,29.15,31.4,35.06,37.49,41.19,43.65,46.4,47.71,50.18,52.34,53.98]
need={}
for c in cuts:
    n=round(c*30)
    for k in range(n-3,n+4): need[k]=None
for k in [0,1700,1699,1325,1330,1600]: need[k]=None
for i,f in enumerate(quadros(v,w=1080,h=1920)):
    if i in need: need[i]=f
json.dump([k for k in need],open("jpg/_idx.json","w"))
def lab(im,t):
    cv2.putText(im,t,(8,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,0),5);cv2.putText(im,t,(8,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,255),2);return im
rows=[]
for j,c in enumerate(cuts):
    n=round(c*30)
    row=np.hstack([lab(cv2.resize(need[k],(216,384),interpolation=cv2.INTER_AREA),f"{k} {k/30:.2f}") for k in range(n-3,n+4)])
    rows.append(row)
for g in range(0,len(rows),5):
    cv2.imwrite(f"jpg/cortes_{g//5+1}.jpg",np.vstack(rows[g:g+5]),[cv2.IMWRITE_JPEG_QUALITY,85])
cv2.imwrite("jpg/q1700_ultimo.jpg",need[1700]);cv2.imwrite("jpg/q0_primeiro.jpg",need[0]);cv2.imwrite("jpg/q1330.jpg",need[1330])
np.save("jpg/_ult.npy",need[1700])
