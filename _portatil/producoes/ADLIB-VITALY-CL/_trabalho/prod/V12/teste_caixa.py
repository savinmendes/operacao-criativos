import cv2, numpy as np, caixas as C
V=r"C:\Users\PICHAU\Downloads\ADLIB-VITALY-CL\VIDEOS\12 - Mi Camino al Bienestar - 1313049140654830.mp4"
cap=cv2.VideoCapture(V)
def fr(n): cap.set(1,n); return cap.read()[1]
f=fr(500)
o=C.cola_caixa_branca(f.copy(),(68,50,652,155),14,[("4 EXTRACTOS QUE",27,66,547-172),("DISUELVEN LOS BLOQUEOS",27,112,636-84)])
o=C.cola_caixa_verde(o,["cuatro extractos naturales","entran a tu torrente"],998,41,min_box=C.bbox_verde(f),pad_x=26,alt=124)
g=fr(1100)
p=C.cola_caixa_branca(g.copy(),(25,42,694,105),14,[("4 HIERBAS · 1 FÓRMULA · 20 GOTAS",24,66,677-42)])
p=C.cola_caixa_verde(p,["Lymphoria tiene las cuatro","hierbas en una sola fórmula"],998,41,min_box=C.bbox_verde(g),pad_x=26,alt=124)
cv2.imwrite("chk/teste_caixas.jpg",np.hstack([f,o,g,p]))
