import cv2,json,numpy as np
V="C:/Users/PICHAU/Downloads/TESTE1-SB-ES/v3/SB-ES_NOTICIA-AURELIO_v3_FICTICIO.mp4"
tl=json.load(open('../timeline_v3.json',encoding='utf-8'))
P=tl['planos']
reg={'R':(300,560,330,600),'A':(380,720,380,800),'P':(200,520,330,720)}
want={}
for p in P:
    it=p['item']
    if p.get('broll') and 'insert_P06' not in p['broll']: continue
    k=None
    if it.startswith('R0'):k='R'
    elif it.startswith('A0'):k='A'
    elif it.startswith('P0'):k='P'
    if k is None: continue
    for i in range(p['q0'],p['q0']+p['n']): want[i]=k
cap=cv2.VideoCapture(V);i=0
import os;os.makedirs('m',exist_ok=True)
while True:
    ok,fr=cap.read()
    if not ok:break
    if i in want:
        x0,x1,y0,y1=reg[want[i]]
        cv2.imwrite(f'm/{i:05d}.jpg',fr[y0:y1,x0:x1],[cv2.IMWRITE_JPEG_QUALITY,85])
    i+=1
print(i,len(want))
