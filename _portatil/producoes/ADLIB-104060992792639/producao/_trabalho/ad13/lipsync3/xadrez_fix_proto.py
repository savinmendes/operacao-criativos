import cv2, numpy as np, sys
sys.path.insert(0, r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13\lipsync3")
from comum3 import quadros
AD=r"C:\Users\PICHAU\Downloads\ADLIB-104060992792639\producao\_trabalho\ad13"
K=np.array([[1,-1],[-1,1]],float)
Y0,Y1,X0,X1=400,520,220,340
def resp(f):
    g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY).astype(float); return np.abs(cv2.filter2D(g,-1,K))
def consertar(f,b):
    """f: quadro final, b: base_sem_legenda no mesmo quadro (referencia de textura). Retorna quadro corrigido, n px mascarados."""
    c=f[Y0:Y1,X0:X1].copy(); rb=cv2.blur(resp(b[Y0:Y1,X0:X1]),(5,5)); rf=cv2.blur(resp(c),(5,5))
    m=((rf-rb)>4).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_OPEN,np.ones((2,2),np.uint8))
    n=int(m.sum())
    if n<6: return f,0
    m=cv2.dilate(m,np.ones((5,5),np.uint8))
    inp=cv2.inpaint(c,m*255,4,cv2.INPAINT_TELEA)
    w=cv2.GaussianBlur(m.astype(np.float32),(0,0),2.0)[...,None]; w=np.clip(w*1.5,0,1)
    o=f.copy(); o[Y0:Y1,X0:X1]=np.clip(inp*w+c*(1-w),0,255).astype(np.uint8); return o,n
if __name__=="__main__":
    a,b=1052,1082
    F=list(quadros(AD+r"\base_lipsync.mp4",a,b-a)); B=list(quadros(AD+r"\base_sem_legenda.mp4",a,b-a))
    rows=[]
    for i,(f,bb) in enumerate(zip(F,B)):
        o,n=consertar(f,bb)
        c=cv2.resize(o[Y0:Y1,X0:X1],None,fx=3,fy=3,interpolation=cv2.INTER_NEAREST)
        cv2.putText(c,f"{a+i} {n}",(5,25),0,0.8,(0,255,255),2); rows.append(c)
    g=np.vstack([np.hstack(rows[i:i+6]) for i in range(0,len(rows),6)]); cv2.imwrite("fix.jpg",g)
