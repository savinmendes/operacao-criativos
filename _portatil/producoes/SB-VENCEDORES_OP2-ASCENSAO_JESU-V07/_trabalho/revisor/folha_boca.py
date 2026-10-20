import sys, json, numpy as np, cv2
sys.path.insert(0, r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
video, lipjson, a, b, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
step = int(sys.argv[6]) if len(sys.argv)>6 else 3
d=json.load(open(lipjson)); fps=d['fps']; env=np.array(d['env'])
fala=cl.mascara_fala(env)
det=cl.Rastreador()
cap=cv2.VideoCapture(video); cap.set(cv2.CAP_PROP_POS_FRAMES, int(a*fps))
tiles=[]; k=int(a*fps); last=None
while k < int(b*fps):
    ok, f = cap.read()
    if not ok: break
    pts = det.pontos(f)
    if pts is not None:
        x0,y0,x1,y1 = cl._caixa(pts, cl.LABIOS_EXT, 0.6, f.shape); last=(x0,y0,x1,y1)
    if (k-int(a*fps)) % step == 0 and last is not None:
        x0,y0,x1,y1=last; cx,cy=(x0+x1)//2,(y0+y1)//2; w=max(x1-x0,60); h=int(w*0.6)
        c=f[max(0,cy-h//2):cy+h//2, max(0,cx-w//2):cx+w//2]
        c=cv2.resize(c,(200,120))
        lab='FALA' if fala[min(k,len(fala)-1)] else 'pausa'
        col=(0,255,0) if lab=='FALA' else (0,0,255)
        cv2.rectangle(c,(0,0),(200,18),(0,0,0),-1)
        cv2.putText(c,f'{k/fps:.2f} {lab}',(3,14),cv2.FONT_HERSHEY_SIMPLEX,0.45,col,1)
        tiles.append(c)
    k+=1
cols=10
while len(tiles)%cols: tiles.append(np.zeros_like(tiles[0]))
rows=[np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]
cv2.imwrite(out, np.vstack(rows)); print(out, len(tiles))
