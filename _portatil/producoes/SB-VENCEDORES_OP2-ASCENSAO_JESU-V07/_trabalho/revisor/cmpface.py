import sys, cv2, numpy as np
sys.path.insert(0, r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
R=r'C:\Users\PICHAU\Downloads\SB-VENCEDORES_OP2-ASCENSAO_JESU-V07'
pairs=[(sys.argv[1],sys.argv[2])]
fr_v, es_v = sys.argv[1], sys.argv[2]; out=sys.argv[3]
times=[tuple(map(float,x.split(':'))) for x in sys.argv[4:]]
def grab(v,t):
    c=cv2.VideoCapture(v); c.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=c.read(); c.release(); return f
det=cl.Rastreador()
rows=[]
for tf,te in times:
    tiles=[]
    for v,t in ((fr_v,tf),(es_v,te)):
        f=grab(v,t); det.caixa=None; det.espera=0
        p=det.pontos(f)
        if p is None: tiles.append(np.zeros((500,500,3),np.uint8)); continue
        x0,y0=p.min(0); x1,y1=p.max(0); cx,cy=(x0+x1)/2,(y0+y1)/2; s=max(x1-x0,y1-y0)*0.75
        c=f[int(max(0,cy-s)):int(cy+s), int(max(0,cx-s)):int(cx+s)]
        g=cv2.cvtColor(c,cv2.COLOR_BGR2GRAY); lap=cv2.Laplacian(cv2.resize(g,(400,400)),cv2.CV_64F).var()
        c=cv2.resize(c,(500,500))
        cv2.rectangle(c,(0,0),(500,26),(0,0,0),-1)
        cv2.putText(c,f"{'FR' if v==fr_v else 'ES'} {t:.2f}s nitidez {lap:.0f} luma {g.mean():.0f}",(5,19),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),1)
        tiles.append(c)
    rows.append(np.hstack(tiles))
cv2.imwrite(out,np.vstack(rows)); print(out)
