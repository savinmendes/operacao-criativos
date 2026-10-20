import cv2,numpy as np,json
R={'selo':(600,292,356,0,10),'envivo':(1700,198,262,30,56),'nome':(1700,15,190,28,58),'coment':(1700,15,230,578,610),'header':(600,0,300,18,52),'header2':(600,0,300,18,52)}
T={}
for k,(fr,x0,x1,y0,y1) in R.items():
    T[k]=cv2.imread(f'f/{fr:05d}.jpg',0)[y0:y1,x0:x1]
S={k:[] for k in R}
for i in range(5085):
    g=cv2.imread(f'f/{i:05d}.jpg',0)
    for k,(fr,x0,x1,y0,y1) in R.items():
        reg=g[max(0,y0-4):y1+4,max(0,x0-4):x1+4]
        S[k].append(float(cv2.matchTemplate(reg,T[k],cv2.TM_CCOEFF_NORMED).max()))
np.save('ui.npy',np.array([S[k] for k in R]))
tl=json.load(open('../timeline_v3.json',encoding='utf-8'))
for k in R:
    a=np.array(S[k]); print(k,'min',a.min().round(2), 'frames<0.6:',int((a<0.6).sum()))
