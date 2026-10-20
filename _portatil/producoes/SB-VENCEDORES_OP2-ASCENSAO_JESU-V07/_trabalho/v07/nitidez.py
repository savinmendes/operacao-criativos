import sys, cv2, numpy as np
sys.path.insert(0, r'C:\Users\PICHAU\Downloads\Produtividade com ia\kit-edicao-criativos\ferramentas')
import checar_lipsync as cl
det=cl.Rastreador()
def med(v,a,b):
    c=cv2.VideoCapture(v); out=[]
    for t in np.arange(a,b,0.2):
        c.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=c.read()
        det.caixa=None; det.espera=0; p=det.pontos(f)
        if p is None: continue
        x0,y0=p.min(0); x1,y1=p.max(0); cx,cy=(x0+x1)/2,(y0+y1)/2; s=max(x1-x0,y1-y0)*0.75
        g=cv2.cvtColor(f[int(max(0,cy-s)):int(cy+s), int(max(0,cx-s)):int(cx+s)],cv2.COLOR_BGR2GRAY)
        out.append(cv2.Laplacian(cv2.resize(g,(400,400)),cv2.CV_64F).var())
    return np.median(out)
FR=sys.argv[1]
for n,(fa,fb),(ea,eb) in [('gancho',(0.2,5.4),(0.2,5.9)),('coroa1',(5.8,9.0),(6.4,10.1)),('coroa2',(15.3,19.7),(15.6,19.2)),('coroa3',(25.3,27.5),(25.7,28.7))]:
    print(n,'FR %.0f'%med(FR,fa,fb),'ES %.0f'%med('es.mp4',ea,eb))
